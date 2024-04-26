from ultralytics import YOLO
import cv2
import math 
import numpy as np
import time
import serial

# Inisialisasi koneksi serial dengan Arduino
# ser = serial.Serial("COM5", 9600)  # Ganti '/dev/ttyUSB0' dengan port serial yang sesuai
# time.sleep(2)  # Tunggu sebentar agar koneksi serial stabil

# baca gambar
cap = cv2.VideoCapture("video/renang.mp4")

# Mengubah dimensi video
desired_width = 640
desired_height = 480

# Mengambil dimensi video asli
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Menentukan rasio perubahan
width_ratio = desired_width / original_width
height_ratio = desired_height / original_height

# model
model = YOLO('forReal2_openvino_model/', task='detect')

# object classes
classNames = ["bucket", "gate", "obstacle"]

# Variabel untuk menghitung FPS
fps_start_time = time.time()
fps_frame_counter = 0
fps = 0

# # deklarasi variabel untuk data dari sensor yang terhubung dengan arduino
# depth = ""
distance = ""

# # deklarasi variabel arah gerak
arah = ""

# ukuran
# size = (original_width, original_height)

# # out
# out = cv2.VideoWriter('output.avi', -1, 20.0, size)
    
# video adalah sekumpulan gambar, sehingga dibutuhkan perulangan
while True:    
    success, img = cap.read()
    
    # Resize gambar
    img = cv2.resize(img, (desired_width, desired_height))
    
    # titik tengah x dan y
    image_center_x = int(img.shape[1] / 2)
    image_center_y = int(img.shape[0] / 2)
    
    results = model(img, conf=0.85, imgsz=640)

    # coordinates
    for r in results:
        boxes = r.boxes

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

            # if(classNames[cls] == "bucket"):
            #     print("bucket")
            # elif(classNames[cls] == "gate"):
            #     print("gate")
            # elif(classNames[cls] == "obstacle"):
            #     print("obstacle")
            # else:
            #     print("tidak ada class")
            
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
            
            if (image_center_y-30 > center_y):
                arah = 'atas' 
            elif (image_center_y+30 < center_y):
                arah = 'bawah'
            elif (center_x > image_center_x+30):
                 arah = 'kanan'  
            elif (center_x < image_center_x-30):
                arah = 'kiri'                    
            else:
                arah ='maju'
      
        
    # Menampilkan data kedalaman dan jarak dari Arduino di frame
    # if ser.in_waiting > 0:
    #     data = ser.readline().decode().rstrip()
    #     distance = data
    #     print("Data dari Arduino:", data)  # Tambahkan ini
        #if data.startswith("D:"):
            #depth = data.split(":")[1]  # Ambil nilai kedalaman air dari data
        #elif data.startswith("K:"):
            #distance = data.split(":")[1]  # Ambil nilai jarak dari data

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
    
cap.release()
# out.release()
cv2.destroyAllWindows()