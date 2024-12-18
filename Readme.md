# Book Text Capture with Webcam

This Python script uses OpenCV and Tesseract OCR to capture text from books or documents placed under a webcam. It automatically detects when a book is positioned, captures an image, extracts the text, and then waits for the user to place a new book.

## Features

*   Automatic book position detection.
*   Timed capture to allow for stabilization.
*   Meaningful text detection to avoid capturing empty frames.
*   Timestamped image saving.
*   Clear console output of extracted text.
*   User-friendly workflow with prompts.

## Installation

1.  **Python:** Ensure you have Python 3 installed. Download it from [python.org](https://www.python.org/).

2.  **Required Libraries:** Install the necessary Python packages using pip:

    ```bash
    pip install opencv-python pytesseract Pillow numpy
    ```

3.  **Tesseract OCR:**

    *   Download and install Tesseract OCR from a suitable source for your operating system. You can find installers and other resources by searching for "Tesseract OCR download."
    *   **Crucially:** After installing Tesseract, you *must* set the path to the Tesseract executable in the Python script. Locate `pytesseract.pytesseract.tesseract_cmd = r'E:\Program Files\tesseract.exe'` and replace `r'E:\Program Files\tesseract.exe'` with the actual path to your `tesseract.exe` file. For example:

        *   **Windows:** `r'E:\Program Files\tesseract.exe'`
        *   **macOS (using Homebrew):** Usually `/opt/homebrew/bin/tesseract` or `/usr/local/bin/tesseract`
        *   **Linux:** Usually `/usr/bin/tesseract`

    *   You might need to install language data files for Tesseract if you're working with languages other than English. These can be downloaded from the Tesseract website.

## Usage

1.  **Run the script:** Open a terminal or command prompt, navigate to the script's directory, and run:

    ```bash
    python book_text_capture.py
    ```

2.  **Position the book:** Place a book or document under your webcam. The script will display the webcam feed and indicate when the book is positioned correctly ("Book is positioned correctly.").

3.  **Automatic capture:** After a short delay (5 seconds by default, adjustable in the code), the script will:

    *   Capture an image.
    *   Extract the text using Tesseract.
    *   Print the extracted text to the console.
    *   Save the image with a timestamped filename (e.g., `captured_frame_20241027_103000.png`).
    *   Prompt you to remove the book ("Please remove the current book.").

4.  **New book:** Remove the current book. The script will wait for you to place a new book. As soon as a new book is detected, the process repeats.

5.  **Quit:** Press the 'q' key on your keyboard to exit the script.

## Code Structure

The script is organized as follows:

*   **Imports:** Imports necessary libraries.
*   **Tesseract Path Setting:** Sets the path to the Tesseract executable.
*   **Webcam Initialization:** Opens the webcam.
*   **Flags and Configurations:** Initializes variables and flags.
*   **`is_book_properly_positioned(frame)`:** Detects if a book is present using edge detection.
*   **`extract_text(frame)`:** Extracts text from the image using Tesseract.
*   **`is_meaningful_text(text)`:** Checks if the extracted text is likely meaningful (prevents capturing blank images).
*   **Main Loop:**
    *   Reads frames from the webcam.
    *   Handles book positioning detection.
    *   Triggers capture after a delay.
    *   Extracts and prints text.
    *   Handles user interaction (waiting for book removal).
    *   Resumes capture when a new book is detected.
    *   Handles quitting.

## Customization

*   **`capture_delay`:** Adjust the delay (in seconds) between book positioning and capture.
*   **`is_book_properly_positioned()` threshold:** Modify the contour threshold to fine-tune book detection.
*   **`is_meaningful_text()` criteria:** Change the minimum length or word count to adjust what is considered "meaningful" text.

## Example Output (Console)