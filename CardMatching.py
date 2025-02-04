from robot import Robot

rbt = Robot()

run = True
while run:
    print("1. CAPTURE IMAGE")
    print("2. COMPARE IMAGE")
    print("3. EXIT\n")
    print("4. COMPARE TEXT\n")

    choice = input("ENTER CHOICE: ").strip(" ").lower()
    if (choice == "1") | (choice == "capture image"):
        rbt.capture_image()

    elif (choice == "2") | (choice == "compare"):
        rbt.compare_cards()

    elif (choice == "3") | (choice == "exit"):
        rbt.destroy()
        run = False

    elif (choice == "4") | (choice == "exit"):
        rbt.destroy()
        run = False

    else:
        print("===== CHOOSE AGAIN =====\n\n")

