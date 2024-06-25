import cv2
import numpy as np
import time
from tensorflow.lite.python.interpreter import Interpreter
import serial

# Inisialisasi koneksi serial dengan Arduino
# ser = serial.Serial("COM5", 9600)  # Ganti dengan port serial yang sesuai
# time.sleep(2)  # Tunggu sebentar agar koneksi serial stabil

# Fungsi untuk memproses frame
def process_frame(img, interpreter, labels, min_conf):
    global arah, gate1_passed, obstacle_avoided, gate3_passed, barang_dijatuhkan

    # Get model details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    float_input = (input_details[0]['dtype'] == np.float32)
    input_mean = 127.5
    input_std = 127.5

    # Image center
    image_center_x = int(img.shape[1] / 2)
    image_center_y = int(img.shape[0] / 2)

    # Preprocess the frame
    frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame_resized_model = cv2.resize(frame_rgb, (width, height))
    input_data = np.expand_dims(frame_resized_model, axis=0)

    # Normalize pixel values if using a floating model (i.e., if model is non-quantized)
    if float_input:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[1]['index'])[0]  # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[3]['index'])[0]  # Class index of detected objects
    scores = interpreter.get_tensor(output_details[0]['index'])[0]  # Confidence of detected objects

    # If no objects detected
    if len(scores) == 0 or max(scores) < min_conf:
        arah = 'f'  # maju
        return img, False

    for i in range(len(scores)):
        if scores[i] > min_conf:
            # Get bounding box coordinates
            ymin = int(max(1, (boxes[i][0] * img.shape[0])))
            xmin = int(max(1, (boxes[i][1] * img.shape[1])))
            ymax = int(min(img.shape[0], (boxes[i][2] * img.shape[0])))
            xmax = int(min(img.shape[1], (boxes[i][3] * img.shape[1])))

            # Draw bounding box
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 255, 255), 2)

            # Calculate center of the bounding box
            center_x = int((xmin + xmax) / 2)
            center_y = int((ymin + ymax) / 2)
            cv2.circle(img, (center_x, center_y), 5, (0, 255, 0), -1)

            # Get object name and confidence
            object_name = labels[int(classes[i])]
            label = f'{object_name}: {int(scores[i] * 100)}%'
            cv2.putText(img, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Logic for controlling direction and mission state
            if object_name == "gate" and not gate1_passed:
                width_gate1 = xmax - xmin
                if center_x > image_center_x + 30:
                    arah = 'r'  # kanan
                elif center_x < image_center_x - 30:
                    arah = 'l'  # kiri
                else:
                    arah = 'f'  # maju
                if width_gate1 > 0.9 * img.shape[1]:
                    gate1_passed = True
                    print("Gate 1 telah dilewati!")

            elif object_name == "obstacle" and gate1_passed and not obstacle_avoided:
                width_obstacle = xmax - xmin
                if width_obstacle < 0.25 * img.shape[1]:
                    if center_x > image_center_x + 30:
                        arah = 'r'  # kanan
                    elif center_x < image_center_x - 30:
                        arah = 'l'  # kiri
                    else:
                        arah = 'f'  # maju
                else:
                    arah = 'r'  # kanan
                    obstacle_avoided = True
                    print("Obstacle dihindari!")

            elif object_name == "gate" and obstacle_avoided and not gate3_passed:
                width_gate3 = xmax - xmin
                if center_x > image_center_x + 30:
                    arah = 'r'  # kanan
                elif center_x < image_center_x - 30:
                    arah = 'l'  # kiri
                else:
                    arah = 'f'  # maju
                if width_gate3 > 0.9 * img.shape[1]:
                    gate3_passed = True
                    print("Gate 3 telah dilewati!")

            elif object_name == "bucket" and not barang_dijatuhkan:
                width_bucket = xmax - xmin
                if width_bucket < img.shape[1] * 0.95:
                    if center_x > image_center_x + 30:
                        arah = 'd'  # kanan
                    elif center_x < image_center_x - 30:
                        arah = 'a'  # kiri
                    else:
                        arah = 'w'  # maju
                else:
                    arah = 's'  # stop
                    barang_dijatuhkan = True
                    print("Barang berhasil dijatuhkan")
                    return img, True  # Mengembalikan True untuk menandakan penghentian

    return img, False  # Mengembalikan False untuk melanjutkan pembacaan

def tflite_detect_camera(modelpath, lblpath, min_conf):
    global arah, arah_sebelumnya, gate1_passed, obstacle_avoided, gate3_passed, barang_dijatuhkan

    # Load the label map into memory
    with open(lblpath, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # Load the TensorFlow Lite model into memory
    interpreter = Interpreter(model_path=modelpath)
    interpreter.allocate_tensors()

    # Open a connection to the camera or video file
    cap = cv2.VideoCapture("video/take4.mp4")  # Path to video file or 0 for default camera

    # Mengatur dimensi video
    desired_width = 640
    desired_height = 480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

    # Initialize frame rate calculation
    fps_start_time = time.time()
    fps_frame_counter = 0
    fps = 0

    stop_signal = False

    while True:
        if not stop_signal:
            success, img = cap.read()
            if not success:
                print("Error: Tidak dapat membaca frame video.")
                break

            img = cv2.resize(img, (desired_width, desired_height))
            img, stop_signal = process_frame(img, interpreter, labels, min_conf)

        # Mengirim data hanya saat arah berubah
        if arah != arah_sebelumnya:
            print(f"Mengirim data: {arah}")
            # ser.write(arah.encode())
            arah_sebelumnya = arah

        # Display direction
        cv2.putText(img, f"Arah Gerak: {arah}", (470, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        # Draw center lines
        image_center_x = int(img.shape[1] / 2)
        image_center_y = int(img.shape[0] / 2)
        cv2.line(img, (image_center_x - 30, image_center_y), (image_center_x + 30, image_center_y), (0, 255, 127), 2)
        cv2.line(img, (image_center_x, image_center_y - 30), (image_center_x, image_center_y + 30), (0, 255, 127), 2)

        # Calculate FPS
        fps_frame_counter += 1
        if time.time() - fps_start_time >= 1:
            fps = fps_frame_counter
            fps_frame_counter = 0
            fps_start_time = time.time()
        cv2.putText(img, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display state
        cv2.putText(img, f"Gate1: {gate1_passed}", (10, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(img, f"Obstacle: {obstacle_avoided}", (10, 410), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(img, f"Gate3: {gate3_passed}", (10, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(img, f"Barang dijatuhkan: {barang_dijatuhkan}", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Output", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    arah = 'f'  # Inisialisasi arah
    arah_sebelumnya = None
    gate1_passed = False
    obstacle_avoided = False
    gate3_passed = False
    barang_dijatuhkan = False
    model_path = "saved_model/detect.tflite"  # Path to the TFLite model file
    label_path = "saved_model/labelmap.txt"  # Path to the label file
    min_conf_threshold = 0.85  # Minimum confidence threshold
    tflite_detect_camera(model_path, label_path, min_conf_threshold)
