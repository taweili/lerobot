import cv2
import os

def list_and_capture_cameras(max_to_check=10, output_dir="outputs/camera_captures"):
    """List available cameras and capture a frame from each."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    available_cameras = []
    
    for i in range(max_to_check):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            # Capture frame
            ret, frame = cap.read()
            if ret:
                # Save frame as PNG
                filename = os.path.join(output_dir, f"camera_{i}.png")
                cv2.imwrite(filename, frame)
                print(f"Saved frame from camera {i} to {filename}")
                available_cameras.append(i)
            cap.release()
    
    return available_cameras

if __name__ == "__main__":
    print("Checking for available cameras and capturing frames...")
    cameras = list_and_capture_cameras()
    
    if cameras:
        print(f"\nFound {len(cameras)} available camera(s):")
        for cam in cameras:
            print(f"- Camera index: {cam}")
    else:
        print("No cameras found.")