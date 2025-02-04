from robot import Robot
from TextMatching import OCRCamera


def compare_text():
    ocr = OCRCamera()
    print("Capture first image for text comparison...")
    img_path1 = ocr.capture_image()
    text1 = ocr.extract_text(img_path1)
    print(f"Extracted Text 1:\n{text1}\n")

    print("Capture second image for text comparison...")
    img_path2 = ocr.capture_image()
    text2 = ocr.extract_text(img_path2)
    print(f"Extracted Text 2:\n{text2}\n")

    if text1.strip() == text2.strip():
        print("✅ The texts are identical!")
    else:
        print("❌ The texts are different!")


rbt = Robot()

run = True
while run:
    print("1. CAPTURE IMAGE")
    print("2. COMPARE IMAGE")
    print("3. COMPARE TEXT")
    print("4. EXIT\n")

    choice = input("ENTER CHOICE: ").strip().lower()

    if choice in ["1", "capture image"]:
        rbt.capture_image()
    elif choice in ["2", "compare image"]:
        rbt.compare_cards()
    elif choice in ["3", "compare text"]:
        compare_text()
    elif choice in ["4", "exit"]:
        rbt.destroy()
        run = False
    else:
        print("===== CHOOSE AGAIN =====\n\n")
