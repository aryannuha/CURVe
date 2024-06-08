from ultralytics import YOLO
import cv2
import math 
import numpy as np
import time
import serial
from picamera2 import Picamera2
from libcamera import controls

# Inisialisasi koneksi serial dengan Arduino
# ser = serial.Serial("COM5", 9600)  # Ganti '/dev/ttyUSB0' dengan port serial yang sesuai
# time.sleep(2)  # Tunggu sebentar agar koneksi serial stabil

# baca gambar
#cap = cv2.VideoCapture("vid7.mp4")

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
picam2.start()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})


# Mengubah dimensi video
desired_width = 640
desired_height = 480

# # Mengambil dimensi video asli
# original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# # Menentukan rasio perubahan
# width_ratio = desired_width / original_width
# height_ratio = desired_height / original_height

# model
model = YOLO('ini352_2.onnx', task='detect')

# object classes
classNames = ["bucket", "gate", "obstacle"]

# Variabel untuk menghitung FPS
fps_start_time = time.time()
fps_frame_counter = 0
fps = 0

# variabel posisi awal konstan
x_axis = ""
y_axis = ""
z_axis = ""

# deklarasi variabel untuk data dari sensor yang terhubung dengan arduino
ultra_depan = ""
ultra_bawah = ""
kedalaman = ""
x_axis_S = ""
y_axis_S = ""
z_axis_S = ""

# # deklarasi variabel arah gerak
arah = ""

# ukuran
# size = (original_width, original_height)

# # out
# out = cv2.VideoWriter('output.avi', -1, 20.0, size)
    
# video adalah sekumpulan gambar, sehingga dibutuhkan perulangan
while True: 
   #success, img = cap.read()
    img = picam2.capture_array() 
    
    # Resize gambar
    img = cv2.resize(img, (desired_width, desired_height))
    
    # titik tengah x dan y
    image_center_x = int(img.shape[1] / 2)
    image_center_y = int(img.shape[0] / 2)
    
    results = model(img, conf=0.85, imgsz=352)

    # ada objek
    for r in results:
        boxes = r.boxes
        
        # tidak terdeteksi objek
        if not boxes:
            arah = "n"  

        # ada class pada model
        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            
            # Menambahkan titik tengah
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # confidence
            confidence = math.ceil((box.conf*100))/100
            print("Confidence --->", confidence)

            # class name
            cls = int(box.cls)
            print("Class name -->", classNames[cls])

            if(classNames[cls] == "bucket"):            # bucket terdeteksi
                if (image_center_y-30 > center_y):      # ke atas
                    arah = 'atas' 
                elif (image_center_y+30 < center_y):    # ke bawah
                    arah = 'bawah'
                elif (center_x > image_center_x+30):    # ke kanan
                    arah = 'kanan'  
                elif (center_x < image_center_x-30):    # ke kiri
                    arah = 'kiri'                    
                else:                                   # maju
                    arah = 'maju'
                print("bucket")
            elif(classNames[cls] == "gate"):            # gate terdeteksi
                if (image_center_y-30 > center_y):      # ke atas
                    arah = 'atas' 
                elif (image_center_y+30 < center_y):    # ke bawah
                    arah = 'bawah'
                elif (center_x > image_center_x+30):    # ke kanan
                    arah = 'kanan'  
                elif (center_x < image_center_x-30):    # ke kiri
                    arah = 'kiri'                    
                else:                                   # maju
                    arah ='maju'
                print("gate")
            elif(classNames[cls] == "obstacle"):        # obstacle terdeteksi
                arah = "kanan"
                time.sleep(2)
                arah = "maju"
                print("obstacle")
            
            # object details
            org = [x1+10, y1-10]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (0, 255, 0)
            thickness = 2
            
            # Gambar lingkaran merah di titik tengah
            cv2.circle(img, (center_x, center_y), 5, (0, 255, 0), -1)  
            
            # Menuliskan text di atas bounding box
            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
        
    # Menampilkan data kedalaman dan jarak dari Arduino di frame
    # if ser.in_waiting > 0:
    #     data = ser.readline().decode().rstrip()
    #     distance = data
    #     print("Data dari Arduino:", data)  # Tambahkan ini
        #if data.startswith("D:"):
            #depth = data.split(":")[1]  # Ambil nilai kedalaman air dari data
        #elif data.startswith("K_D:"):
            # ultra_depan = data.split(":")[1]  # Ambil nilai jarak dari data
        #elif data.startswith("K_B:"):
            # ultra_bawah = data.split(":")[1]  # Ambil nilai jarak dari data
        #elif data.startswith("X:"):
            # x_axis_S = data.split(":")[1]  # Ambil nilai jarak dari data
        #elif data.startswith("Y:"):
            # y_axis_S = data.split(":")[1]  # Ambil nilai jarak dari data
        #elif data.startswith("Z:"):
            # z_axis_S = data.split(":")[1]  # Ambil nilai jarak dari data

    # kirim data ke arduino
    # arah gerak
    # ser.write(arah.encode())
    
    # Tampilkan kedalaman air dan jarak di frame
    # cv2.putText(img, f"Ultrasonic: {distance} cm", (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
    
    # text arah gerak
    cv2.putText(img, f"Arah Gerak: {arah}", (400, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

    # tampilkan crosshair
    cv2.line(img, (image_center_x - 30, image_center_y), (image_center_x + 30, image_center_y), (0,255,127), 2)
    cv2.line(img, (image_center_x, image_center_y - 30), (image_center_x, image_center_y + 30), (0,255,127), 2)

    # Increment frame counter untuk menghitung FPS
    fps_frame_counter += 1
            
    # Cek waktu setiap detik untuk menghitung FPS
    if time.time() - fps_start_time >= 1:
        fps = fps_frame_counter
        fps_frame_counter = 0
        fps_start_time = time.time()
    
    # Menampilkan FPS di layar
    cv2.putText(img, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # menampilkan gambar atau video
    cv2.imshow("img", img)
    
    # # write
    # out.write(img)
        
    # pencet q untuk berhenti dari loop
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
    
# out.release()
cv2.destroyAllWindows()
