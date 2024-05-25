import cv2

# Function to display a frame and allow for coordinate adjustments
def display_frame_with_blur_region(input_video, x, y, w, h):
    cap = cv2.VideoCapture(input_video)
    ret, frame = cap.read()
    if not ret:
        print("Failed to read video")
        return

    # Draw rectangle on the frame
    frame_with_rectangle = frame.copy()
    cv2.rectangle(frame_with_rectangle, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("Frame with Blur Region", frame_with_rectangle)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cap.release()

# Example usage
input_video_path = 'Untitles video(5).mp4'
x, y, w, h = 50, 50, 100, 50  # Adjust these values as needed
display_frame_with_blur_region(input_video_path, x, y, w, h)
