import cv2
import pytesseract


class OCRCamera:

    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" #Windows
    # pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract" #M2 Mac
    # "/usr/bin/tesseract" #Raspbery Pi
    def __init__(self, tesseract_path="/opt/homebrew/bin/tesseract"):
        """
        Initialize the OCRCamera class with the specified Tesseract path.
        :param tesseract_path: Path to the Tesseract executable.
        """
        self.tesseract_path = tesseract_path
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path

    def capture_image(self, image_path="captured_image.jpg"):
        """
        Capture an image from the camera and save it to the specified path.
        :param image_path: Path where the captured image will be saved.
        """
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Error: Could not open the camera.")

        print("Capturing image... Press 'Space' to capture.")

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            cv2.imshow("Press 'Space' to Capture, 'Esc' to Exit", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == 32:  # Spacebar
                cv2.imwrite(image_path, frame)
                print(f"Image saved as {image_path}")
                break
            elif key == 27:  # Escape key
                cap.release()
                cv2.destroyAllWindows()
                exit()

        cap.release()
        cv2.destroyAllWindows()
        return image_path

    def extract_text(self, image_path):
        """
        Extract text from the given image using Tesseract OCR.
        :param image_path: Path to the image file.
        :return: Extracted text.
        """
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Error: Unable to load the image {image_path}")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        extracted_text = pytesseract.image_to_string(gray)
        return extracted_text

    def detect_text_boxes(self, image_path):
        """
        Detect text in an image and draw bounding boxes around words.
        :param image_path: Path to the image file.
        """
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Error: Unable to load the image {image_path}")

        h, w, _ = image.shape
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        detection_boxes = pytesseract.image_to_boxes(gray)
        for box in detection_boxes.splitlines():
            b = box.split()
            x, y, w_, h_ = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            y = h - y  # Convert Y-coordinates
            h_ = h - h_
            cv2.rectangle(image, (x, h_), (w_, y), (0, 255, 0), 2)

        cv2.imshow("Text Detection", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    ocr = OCRCamera()
    img_path = ocr.capture_image()
    text = ocr.extract_text(img_path)
    print("\nExtracted Text:")
    print(text)
    ocr.detect_text_boxes(img_path)