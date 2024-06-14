from ultralytics import YOLO
import cv2
import math 
import numpy as np
import time
import serial

# Inisialisasi koneksi serial dengan Arduino
# ser = serial.Serial("COM5", 9600)  # Ganti dengan port serial yang sesuai
# time.sleep(2)  # Tunggu sebentar agar koneksi serial stabil

# Baca video
cap = cv2.VideoCapture("video/testvid.mp4")
if not cap.isOpened():
    print("Error: Tidak dapat membuka video.")
    exit()

# Mengatur dimensi video
desired_width = 640
desired_height = 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

# Load model YOLO
model = YOLO('palingBaru.onnx', task='detect')

# Object classes
classNames = ["bucket", "gate", "obstacle"]

# Variabel untuk menghitung FPS
fps_start_time = time.time()
fps_frame_counter = 0
fps = 0

# Variabel arah gerak
arah = ""

# Fungsi untuk memproses frame
def process_frame(img, model, classNames, desired_width, desired_height):
    global arah
    image_center_x = int(img.shape[1] / 2)
    image_center_y = int(img.shape[0] / 2)
    
    results = model(img, conf=0.85, imgsz=352)
    
    for r in results:
        boxes = r.boxes
        
        if not boxes:
            arah = "unfound"
        
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            confidence = math.ceil((box.conf * 100)) / 100
            print("Confidence --->", confidence)

            cls = int(box.cls)
            print("Class name -->", classNames[cls])

            if classNames[cls] == "bucket":
                total_width = x2 - x1
                if total_width < desired_width * 0.5:
                    if center_x > image_center_x + 30:
                        arah = 'kanan'
                    elif center_x < image_center_x - 30:
                        arah = 'kiri'
                    else:
                        arah = 'maju'
                else:
                    arah = 'stop'
                    return img, True  # Mengembalikan True untuk menandakan penghentian
                # print("bucket")
            elif classNames[cls] == "gate":
                if center_x > image_center_x + 30:
                    arah = 'kanan'
                elif center_x < image_center_x - 30:
                    arah = 'kiri'
                else:
                    arah = 'maju'
                # print("gate")
            elif classNames[cls] == "obstacle":
                arah = "kanan"
                # print("obstacle")
            
            org = [x1 + 10, y1 - 10]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (0, 255, 0)
            thickness = 2
            
            cv2.circle(img, (center_x, center_y), 5, (0, 255, 0), -1)
            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
    
    return img, False  # Mengembalikan False untuk melanjutkan pembacaan

while True: 
    success, img = cap.read()
    if not success:
        print("Error: Tidak dapat membaca frame video.")
        break
    
    img = cv2.resize(img, (desired_width, desired_height))
    
    img, stop_signal = process_frame(img, model, classNames, desired_width, desired_height)
    
    if stop_signal:
        print("Misi selesai: Kondisi 'stop' tercapai.")
        break
    
    # Menampilkan data dari Arduino di frame (contoh)
    # if ser.in_waiting > 0:
    #     data = ser.readline().decode().rstrip()
    #     print("Data dari Arduino:", data)
    
    #     if data.startswith("D:"):
    #         kedalaman = data.split(":")[1]
    #     elif data.startswith("K_D:"):
    #         ultra_depan = data.split(":")[1]
    #     elif data.startswith("K_B:"):
    #         ultra_bawah = data.split(":")[1]
    #     elif data.startswith("X:"):
    #         x_axis_S = data.split(":")[1]
    #     elif data.startswith("Y:"):
    #         y_axis_S = data.split(":")[1]
    #     elif data.startswith("Z:"):
    #         z_axis_S = data.split(":")[1]
    
    # ser.write(arah.encode())
    
    cv2.putText(img, f"Arah Gerak: {arah}", (470, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
    
    image_center_x = int(img.shape[1] / 2)
    image_center_y = int(img.shape[0] / 2)
    cv2.line(img, (image_center_x - 30, image_center_y), (image_center_x + 30, image_center_y), (0, 255, 127), 2)
    cv2.line(img, (image_center_x, image_center_y - 30), (image_center_x, image_center_y + 30), (0, 255, 127), 2)
    
    fps_frame_counter += 1
    if time.time() - fps_start_time >= 1:
        fps = fps_frame_counter
        fps_frame_counter = 0
        fps_start_time = time.time()
    
    cv2.putText(img, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.imshow("img", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
