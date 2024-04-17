from ultralytics import YOLO
import cv2
import numpy as np
import time
import math
import serial

# Inisialisasi koneksi serial dengan Arduino
#ser = serial.Serial("COM5", 9600)  # Ganti '/dev/ttyUSB0' dengan port serial yang sesuai
#time.sleep(2)  # Tunggu sebentar agar koneksi serial stabil

# baca gambar
cap = cv2.VideoCapture("video/vid7.mp4")

# mengubah spesifik ukuran
# lebar
cap.set(3, 640)
# tinggi
cap.set(4, 480)
# kecerahan
# cap.set(10, 100)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 100)

# model
model = YOLO("best.pt")

# object classes
classNames = ["baskom", "ember"]

# Variabel untuk menghitung FPS
fps_start_time = time.time()
fps_frame_counter = 0
fps = 0

# deklarasi variabel untuk data dari sensor yang terhubung dengan arduino
depth = ""
distance = ""

# deklarasi variabel arah gerak
arah = ""

# deklarasi variabel warna
warna = ""
    
# video adalah sekumpulan gambar, sehingga dibutuhkan perulangan
while True:    
    # mengcapture image
    success, img = cap.read()
    
    results = model(img, stream=True, conf=0.85)
    
    # titik tengah x dan y
    image_center_x = int(img.shape[1] / 2)
    image_center_y = int(img.shape[0] / 2)
    
    # menentukan hsv minimum
    r_lower = np.array([163, 201, 136]) # lower red
    o_lower = np.array([2,132,164]) # lower orange
    g_lower = np.array([45, 80, 25]) # lower green

    # menentukan hsv maksimum
    r_upper = np.array([179, 255, 255]) # higher red
    o_upper = np.array([14,210,255]) # higher orange
    g_upper = np.array([90,255,255]) # higher green
    
    # ubah bgr menjadi hsv
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
    # masking
    r_mask = cv2.inRange(imgHSV,r_lower,r_upper) # red
    o_mask = cv2.inRange(imgHSV,o_lower,o_upper) # orange
    g_mask = cv2.inRange(imgHSV,g_lower,g_upper) # green
        
    # Penghalusan gambar dengan operasi morfologi
    kernel = np.ones((5, 5), np.uint8)
    r_mask = cv2.erode(r_mask, kernel, iterations=1) 
    r_mask = cv2.dilate(r_mask, kernel, iterations=1)   
    o_mask = cv2.erode(o_mask, kernel, iterations=1)
    o_mask = cv2.dilate(o_mask, kernel, iterations=1)
    g_mask = cv2.erode(g_mask, kernel, iterations=1)
    g_mask = cv2.dilate(g_mask, kernel, iterations=1)
    
    # Temukan kontur pada gambar hasil masking
    contours_r, _ = cv2.findContours(r_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_o, _ = cv2.findContours(o_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_g, _ = cv2.findContours(g_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # menyatukan dua gambar
    # imgResult = cv2.bitwise_and(img, img, mask=mask)

    # Jika ditemukan setidaknya satu kontur untuk warna merah
    for contour in contours_r:
        # hitung luas contour
        area = cv2.contourArea(contour)
        
        #isi warna
        warna = "merah"
        
        # Gambar persegi panjang berwarna putih jika luas kontur cukup besar
        if area > 1000:
            
            # coordinates
            for r in results:
                boxes = r.boxes

                for box in boxes:
                    # bounding box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                    # put box in cam
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                    # confidence
                    confidence = math.ceil((box.conf[0]*100))/100
                    print("Confidence --->",confidence)

                    # class name
                    cls = int(box.cls[0])
                    print("Class name -->", classNames[cls])
                    
                    # object details
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 2

                    cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
            
            '''
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 2)

            # Hitung momen spasial untuk mendapatkan centroid
            M = cv2.moments(contour)
            
            # Koordinat x dan y dari centroid
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0  # Atur ke nilai default jika momen spasial bernilai nol
            
            # Gambar titik centroid pada gambar hasil
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1) 
            
            # arah gerak
            if (cx > image_center_x+30 and image_center_y-30 > cy):
                print("kanan atas")
                arah = 'kanan_atas'
            elif (cx < image_center_x-30 and image_center_y-30 > cy):
                print("kiri atas")
                arah = 'kiri_atas'
            elif (cx > image_center_x+30 and image_center_y+30 < cy):
                print("kanan bawah")
                arah = 'kanan_bawah'
            elif (cx < image_center_x-30 and image_center_y+30 < cy):
                print("kiri bawah")
                arah = 'kiri_bawah' 
            elif (image_center_y-30 > cy):
                print("atas")
                arah = 'atas' 
            elif (image_center_y+30 < cy):
                print("bawah")
                arah = 'bawah'
            elif (cx > image_center_x+30):
                print("kanan")
                arah = 'kanan'  
            elif (cx < image_center_x-30):
                print("kiri")
                arah = 'kiri'                    
            else:
                print("maju")
                arah ='maju'

            # tulisan merah pada persegi panjang
            cv2.putText(img, "Merah", (x + 10 , y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
            
            # kirim data ke arduino
            #ser.write('r'.encode())
            '''
            
    # Jika ditemukan setidaknya satu kontur untuk warna orange
    for contour in contours_o:
        # hitung luas contour
        area = cv2.contourArea(contour)
        
        # isi warna
        warna = "orange"
        
        # Pengaproksimasi bentuk kontur
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        num_vertices = len(approx)
        
        # Perbandingan luas dan perimeter
        area_perimeter_ratio = area / perimeter
        
        # Gambar persegi panjang berwarna putih jika luas kontur cukup besar
        if area > 1000:
            # Jika objek memiliki 4 sudut dan perbandingan area perimeter tertentu, itu adalah persegi panjang
            if num_vertices == 4 and area_perimeter_ratio > 10: # Sesuaikan nilai threshold sesuai kebutuhan
                # Lakukan sesuatu untuk persegi panjang
                x, y, w, h = cv2.boundingRect(contour)
                
                # Hitung momen spasial untuk mendapatkan centroid
                M = cv2.moments(contour)
                
                # Koordinat x dan y dari centroid
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                else:
                    cx, cy = 0, 0  # Atur ke nilai default jika momen spasial bernilai nol
                    
                # Gambar titik centroid pada gambar hasil
                cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1) 
                # print cx,cy
                # print("titik tengah objek ", cx,cy)
                
                # arah gerak
                if (cx > image_center_x+30 and image_center_y-30 > cy):
                    print("kanan atas")
                    arah = 'kanan_atas'
                elif (cx < image_center_x-30 and image_center_y-30 > cy):
                    print("kiri atas")
                    arah = 'kiri_atas'
                elif (cx > image_center_x+30 and image_center_y+30 < cy):
                    print("kanan bawah")
                    arah = 'kanan_bawah'
                elif (cx < image_center_x-30 and image_center_y+30 < cy):
                    print("kiri bawah")
                    arah = 'kiri_bawah' 
                elif (image_center_y-30 > cy):
                    print("atas")
                    arah = 'atas' 
                elif (image_center_y+30 < cy):
                    print("bawah")
                    arah = 'bawah'
                elif (cx > image_center_x+30):
                    print("kanan")
                    arah = 'kanan'  
                elif (cx < image_center_x-30):
                    print("kiri")
                    arah = 'kiri'                    
                else:
                    print("maju")
                    arah ='maju'

                # kirim data ke arduino
                #ser.write('o'.encode())
                    
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 2)
                # tulisan orange pp pada persegi panjang
                cv2.putText(img, "orange pp", (x + 10 , y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 69, 255), 2, cv2.LINE_AA)
            else:
                # Lakukan sesuatu untuk objek lainnya (misalnya, silinder)
                # Misalnya, Anda dapat menambahkan kode di sini untuk tindakan yang sesuai dengan jenis objek lainnya
                pass
        
    # Menampilkan data kedalaman dan jarak dari Arduino di frame
    #if ser.in_waiting > 0:
        #data = ser.readline().decode().rstrip()
        #print("Data dari Arduino:", data)  # Tambahkan ini
        #if data.startswith("D:"):
            #depth = data.split(":")[1]  # Ambil nilai kedalaman air dari data
        #elif data.startswith("K:"):
            #distance = data.split(":")[1]  # Ambil nilai jarak dari data

    # ada countour atau tidak
    if not contours_g and not contours_o and not contours_r:
        warna = ""
        
    # ada warna atau tidak
    if warna == "":
        print("tidak ada warna")    
    else:
        print(warna)

    # Tampilkan kedalaman air dan jarak di frame
    cv2.putText(img, f"Kedalaman Air: {depth} cm | Jarak: {distance} cm", (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

    # tampilkan crosshair
    cv2.line(img, (image_center_x - 30, image_center_y), (image_center_x + 30, image_center_y), (0,255,127), 2)
    cv2.line(img, (image_center_x, image_center_y - 30), (image_center_x, image_center_y + 30), (0,255,127), 2)
    # print("titik tengah x,y ", image_center_x, image_center_y)
    
    # text arah gerak
    cv2.putText(img, f"Arah Gerak: {arah}", (400, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

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
    # cv2.imshow("window", imgResult)
    
    # menampilkan gambar atau video
    cv2.imshow("img", img)
        
    # pencet q untuk berhenti dari loop
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
    
cap.release
cv2.destroyAllWindows()
