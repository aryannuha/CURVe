from ultralytics import YOLO
import cv2
import math
import numpy as np
import time
import serial
from picamera2 import Picamera2
from libcamera import controls

# Function to perform handshake with Arduino
def handshake_with_arduino():
    while True:
        ser.write(b'H')  # Send handshake signal
        if ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            if response == "ACK":
                print("Handshake successful")
                break
        time.sleep(1)  # Wait for a second before retrying

# Initialize serial connection with Arduino
ser = serial.Serial("/dev/ttyACM0", 115200)
time.sleep(1)  # Wait briefly for the serial connection to stabilize

# called handshake function
handshake_with_arduino()

# Read image from Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (480, 480)}))
picam2.start()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

# Set desired video dimensions
desired_width = 480
desired_height = 480

# Load YOLO model
model = YOLO('verynew.onnx', task='detect')

# Object classes
classNames = ["bucket", "gate", "obstacle"]

# Variables for calculating FPS
fps_start_time = time.time()
fps_frame_counter = 0
fps = 0

# Variables for direction
arah = ""
# arah_sebelumnya = ""

# Variables for mission state
gate1_passed = False
obstacle_avoided = False
gate3_passed = False
barang_dijatuhkan = False

# Variables to track data transmission
data_sent_time = 0
data_send_interval = 1  # Interval for data transmission in seconds

# Function to process the frame
def process_frame(img, model, classNames, desired_width, desired_height):
    global arah, gate1_passed, obstacle_avoided, gate3_passed, barang_dijatuhkan
    image_center_x = int(img.shape[1] / 2)
    image_center_y = int(img.shape[0] / 2)
    
    results = model(img, conf=0.85, imgsz=320)
    
    for r in results:
        boxes = r.boxes
        
        if not boxes:  # If no objects are detected
            arah = 'w'  # Move forward
            if gate1_passed:
                arah = 'w'  # Move forward
            elif obstacle_avoided:
                arah = 'p'  # Right
            elif gate3_passed:
                arah = 'o'  # Left diagonal
            return img, False
        
        for box in boxes:  # If objects are detected
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # draw rectangle based on coordinate object detected
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            
            # variable of center dot object
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # confidence value
            confidence = math.ceil((box.conf * 100)) / 100
            print("Confidence --->", confidence)

            # name of object
            cls = int(box.cls)
            print("Class name -->", classNames[cls])

            if classNames[cls] == "gate" and not gate1_passed:
                width_gate1 = x2 - x1
                if center_x > image_center_x + 30:
                    arah = 'd'  # Right
                elif center_x < image_center_x - 30:
                    arah = 'a'  # Left
                else:
                    arah = 'w'  # Forward
                    
                if width_gate1 > 0.9 * desired_width:
                    gate1_passed = True
                    print("Gate 1 passed!")

            elif classNames[cls] == "obstacle" and not obstacle_avoided:
                width_obstacle = x2 - x1
                if width_obstacle < 0.3 * desired_width:
                    if center_x > image_center_x + 30:
                        arah = 'd'  # Right
                    elif center_x < image_center_x - 30:
                        arah = 'a'  # Left
                    else:
                        arah = 'w'  # Forward
                else:
                    arah = 'd'  # Right
                    obstacle_avoided = True
                    print("Obstacle avoided!")

            elif classNames[cls] == "gate" and obstacle_avoided and not gate3_passed:
                width_gate3 = x2 - x1
                # if center_x > image_center_x + 30:
                #     arah = 'd'  # Right
                # elif center_x < image_center_x - 30:
                #     arah = 'a'  # Left
                # else:
                #     arah = 'b'  # Forward
                # arah = 'w'
                    
                if width_gate3 > 0.9 * desired_width:
                    gate3_passed = True
                    arah = 'w'
                    print("Gate 3 passed!")
                else:
                    arah = 'w'

            elif classNames[cls] == "bucket" and obstacle_avoided and gate3_passed and not barang_dijatuhkan:
                width_bucket = x2 - x1
                if width_bucket < desired_width * 0.9:
                    if center_x > image_center_x + 30:
                        arah = 'd'  # Right
                    elif center_x < image_center_x - 30:
                        arah = 'a'  # Left
                    else:
                        arah = 'b'  # Forward
                else:
                    arah = 's'  # Stop
                    barang_dijatuhkan = True
                    print("Barang successfully dropped")
                    return img, True  # Return True to signal stop
            
            org = [x1 + 10, y1 - 10]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (0, 255, 0)
            thickness = 2
            
            cv2.circle(img, (center_x, center_y), 5, (0, 255, 0), -1) # draw circle in the middle of object
            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness) # write classname above object
    
    return img, False  # Return False to continue reading

while True:
    img = picam2.capture_array()
    if img is None:
        print("Error: Cannot read video frame.")
        break
    
    img = cv2.resize(img, (desired_width, desired_height))
    
    img, stop_signal = process_frame(img, model, classNames, desired_width, desired_height)
    
    # stop_signel return true then camera reading stop
    if stop_signal:
        print("Mission complete: 'stop' condition reached.")
        break
    
    current_time = time.time()
    if (current_time - data_sent_time) > data_send_interval:
        print(f"Sending data: {arah}")
        ser.write(arah.encode())
        data_sent_time = current_time
    
    image_center_x = int(img.shape[1] / 2)
    image_center_y = int(img.shape[0] / 2)
    cv2.line(img, (image_center_x - 30, image_center_y), (image_center_x + 30, image_center_y), (0, 255, 127), 2)
    cv2.line(img, (image_center_x, image_center_y - 30), (image_center_x, image_center_y + 30), (0, 255, 127), 2)
    
    fps_frame_counter += 1
    if time.time() - fps_start_time >= 1:
        fps = fps_frame_counter
        fps_frame_counter = 0
        fps_start_time = time.time()
    
    cv2.putText(img, f"Direction: {arah}", (470, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2) # write arah in frame
    cv2.putText(img, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2) # write fps in frame
    cv2.putText(img, f"gate1_passed: {gate1_passed}", (10, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2) # write condition of gate1_passed
    cv2.putText(img, f"obstacle: {obstacle_avoided}", (10, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2) # write condition of obstacle_avoided
    cv2.putText(img, f"gate3_passed: {gate3_passed}", (10, 410), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2) # write condition of gate3_passed
    cv2.putText(img, f"bucket: {barang_dijatuhkan}", (10, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2) # write condition of barang_dijatuhkan
    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
