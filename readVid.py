import cv2

def extract_frames(video_path, output_folder):
    # Buka video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Video tidak dapat dibuka")
        return

    # Baca video frame per frame
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Simpan frame
        frame_count += 1
        frame_name = f"frame_{frame_count}.jpg"
        output_path = f"{output_folder}/{frame_name}"
        cv2.imwrite(output_path, frame)
        print(f"Frame {frame_count} disimpan: {output_path}")

    # Tutup video
    cap.release()

if __name__ == "__main__":
    video_path = "video/kolam1.mp4"  # Ganti dengan path video Anda
    output_folder = "frames2"  # Folder untuk menyimpan frame
    extract_frames(video_path, output_folder)
