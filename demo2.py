import cv2
import pytesseract
from PIL import Image
import datetime
import time
import numpy as np

# Set path for Tesseract executable (CHANGE THIS TO YOUR TESSERACT PATH)
pytesseract.pytesseract.tesseract_cmd = r'E:\Program Files\tesseract.exe'

# Open the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Webcam is running. Place a book or paper under the webcam and position it correctly.")

# Flags and configurations
capture_ready = False
capture_start_time = None
capture_delay = 5 
book_positioned = False
user_continued = True 

# Function to detect if book is properly positioned (using edge detection)
def is_book_properly_positioned(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return len(contours) > 5  # Adjust this threshold as needed

# Function to extract text
def extract_text(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    custom_config = r'--oem 3 --psm 6'  # Improved configuration
    text = pytesseract.image_to_string(Image.fromarray(thresh), config=custom_config)
    return text.strip()

# Function to check if text is meaningful
def is_meaningful_text(text):
    """Checks if extracted text is likely meaningful."""
    min_length = 20  # Increased for less false positives
    words = text.split()
    if len(words) < 3:  # At least 3 words
        return False
    if len(text) < min_length:
        return False
    return True

while True:
    try:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame from webcam.")
            break

        cv2.imshow("Webcam Feed", frame)

        if not book_positioned:
            if is_book_properly_positioned(frame):
                print("Book is positioned correctly.")
                book_positioned = True
                capture_ready = True
                capture_start_time = time.time()

        elif book_positioned and capture_ready and (time.time() - capture_start_time >= capture_delay):
            text = extract_text(frame)
            if text and is_meaningful_text(text):
                print("Capturing frame and extracting text...")
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                frame_filename = f"captured_frame_{timestamp}.png"
                cv2.imwrite(frame_filename, frame)
                print(f"Frame captured and saved as {frame_filename}")

                # Print the extracted text HERE, immediately after capture
                print("Extracted Text:", text)

                capture_ready = False
                user_continued = False

                print("Please remove the current book.")
                while not user_continued:
                    ret, frame = cap.read()
                    cv2.imshow("Webcam Feed", frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        import sys
                        sys.exit()
                    elif not is_book_properly_positioned(frame):
                        user_continued = True
                        break

                if user_continued:
                    print("New book detected. Resuming capture...")
                    capture_ready = True
                    capture_start_time = time.time()
                    book_positioned = False # Reset the book_positioned flag
            else:
                print("No meaningful text detected. Please position the book correctly/improve lighting.")
                capture_start_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        print(f"Error: {e}")
        break

cap.release()
cv2.destroyAllWindows()