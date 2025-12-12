"""
Password & QR Code Generator

This script generates secure passwords, optionally creates a QR code for the last generated password,
and allows copying it to the clipboard. Designed for learning purposes and basic security utilities.
"""


import secrets
import string
import sys

# Optional modules
try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

try:
    import pyperclip
    CLIP_AVAILABLE = True
except Exception:
    CLIP_AVAILABLE = False


# Required Character Generator
def required_characters(use_letters, use_digits, use_symbols):
    """Returns at least one character from each selected type."""
    chars = []

    if use_letters:
        chars.append(secrets.choice(string.ascii_letters))
    if use_digits:
        chars.append(secrets.choice(string.digits))
    if use_symbols:
        chars.append(secrets.choice(string.punctuation))

    return chars


# Password Generator
def generate_password(length=12, mode="strong"):
    """Generates a secure password with given length and mode."""
    if length <= 0:
        raise ValueError("Password length must be a positive number.")

    mode = mode.lower()

    use_letters = use_digits = use_symbols = False

    if mode in ("strong", "mixed"):
        use_letters = use_digits = use_symbols = True
    elif mode == "letters":
        use_letters = True
    elif mode == "digits":
        use_digits = True
    else:
        use_letters = use_digits = use_symbols = True  

    # Build character pool
    pool = ""
    if use_letters:
        pool += string.ascii_letters
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += string.punctuation

    if not pool:
        raise ValueError("Character pool is empty. Select at least one type.")

    required = required_characters(use_letters, use_digits, use_symbols)

    if len(required) > length:
        required = required[:length]

    remaining = length - len(required)
    password_parts = list(required)

    for _ in range(remaining):
        password_parts.append(secrets.choice(pool))

    secrets.SystemRandom().shuffle(password_parts)

    return "".join(password_parts)


# QR Code Creator
def create_qr_and_save(text, filepath="qrcode.png", box_size=10, border=4):
    """Creates a QR code from text and saves it as PNG."""
    if not QR_AVAILABLE:
        raise RuntimeError("QR library not installed. Install with: pip install qrcode[pil]")

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border
    )

    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)
    return filepath


def main_menu():
    print("-" * 40)
    print("   Password + QR Generator — Menu")
    print("-" * 40)
    print("1) Generate password")
    print("2) Generate example strong password (quick)")
    print("3) Save last password as QR code (PNG)")
    print("4) Copy last password to clipboard")
    print("5) Exit")
    print()

    if not QR_AVAILABLE:
        print("[Note] QR library is not installed. QR saving is disabled.")
    if not CLIP_AVAILABLE:
        print("[Note] pyperclip not installed. Clipboard copy disabled.")
    print()


# Program Loop
def main_loop():
    last_password = None

    while True:
        main_menu()
        choice = input("Your choice (1–5): ").strip()

        # 1) Generate Password
        if choice == "1":
            try:
                length = int(input("Password length (e.g., 12): ").strip())
            except ValueError:
                print("Please enter a valid integer.")
                continue

            print("Modes: strong / letters / digits / mixed")
            mode = input("Mode (default: strong): ").strip() or "strong"

            try:
                last_password = generate_password(length, mode)
            except Exception as e:
                print("Error:", e)
                continue

            print("\nGenerated Password:\n", last_password, "\n")

        # 2) Quick Example Strong Password
        elif choice == "2":
            last_password = generate_password(16, "strong")
            print("\nExample Strong Password (16 chars):\n", last_password, "\n")

        # 3) Save QR Code
        elif choice == "3":
            if not QR_AVAILABLE:
                print("QR saving is unavailable. Install qrcode module.")
                continue

            if not last_password:
                print("Generate a password first (option 1 or 2).")
                continue

            filename = input("Save file name (default: qrcode.png): ").strip() or "qrcode.png"
            try:
                path = create_qr_and_save(last_password, filepath=filename)
                print(f"QR code saved as '{path}'.")
            except Exception as e:
                print("QR creation error:", e)

        # 4) Copy To Clipboard
        elif choice == "4":
            if not CLIP_AVAILABLE:
                print("Clipboard copy unavailable. Install pyperclip.")
                continue

            if not last_password:
                print("Generate a password first.")
                continue

            try:
                pyperclip.copy(last_password)
                print("Password copied to clipboard.")
            except Exception as e:
                print("Clipboard error:", e)

        # 5) Exit
        elif choice == "5":      
            print("Exiting. Stay safe!")
            break

        else:
            print("Invalid choice. Please try again.")


# Entry Point
if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Goodbye!")
        sys.exit(0)

