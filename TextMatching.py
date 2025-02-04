import cv2
import pytesseract

#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"



cap = cv2.VideoCapture(0)  # Open the default camera (0)
if not cap.isOpened():
    raise RuntimeError("Error: Could not open the camera.")

print("Capturing image... Press 'Space' to capture.")

while True:
    ret, frame = cap.read()  # Capture frame-by-frame
    if not ret:
        continue

    cv2.imshow("Press 'Space' to Capture, 'Esc' to Exit", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 32:  # Spacebar to capture image
        image_path = "captured_image.jpg"
        cv2.imwrite(image_path, frame)
        print(f"Image saved as {image_path}")
        break
    elif key == 27:  # Escape key to exit
        cap.release()
        cv2.destroyAllWindows()
        exit()

cap.release()
cv2.destroyAllWindows()

image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError(f"Error: Unable to load the image {image_path}")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding for better text visibility
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


extracted_text = pytesseract.image_to_string(gray)

print("\nExtracted Text:")
print(extracted_text)


h, w, _ = image.shape
detection_boxes = pytesseract.image_to_boxes(gray)

for box in detection_boxes.splitlines():
    b = box.split()
    x, y, w_, h_ = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    y = h - y  # Convert Y-coordinates
    h_ = h - h_
    cv2.rectangle(image, (x, h_), (w_, y), (0, 255, 0), 2)  # Draw bounding box


cv2.imshow("Text Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
