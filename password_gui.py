"""
Password & QR Code Generator

This script generates secure passwords, optionally creates a QR code for the last generated password,
and allows copying it to the clipboard. Designed for learning purposes and basic security utilities.
"""


import secrets
import string
import sys
import tkinter as tk

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
#if __name__ == "__main__":
    #try:
        #main_loop()
    #except KeyboardInterrupt:
        #print("\nInterrupted by user. Goodbye!")
        #sys.exit(0)

def start_gui():
    root = tk.Tk() #Ana Pencere (Main Window) oluşturulur
    root.title("Password & QR Generator")  #Pencerenin başlığı (title) oluşturulur.
    root.configure(bg="#121212")
    #root.geometry("600x500") #pencerenin boyutu (size) oluşturulur.
    root.state("zoomed")
    #root.mainloop() #pencerenin sürekli açık kalmasını sağlar. 
    
    def on_generate_click():
        try:
            length = int(entry_length.get())
            mode = var_mode.get()
            password = generate_password(length, mode) #orijinal fonksiyonu çağırır.

            entry_result.delete(0, tk.END) #Önce eskileri siler.
            entry_result.insert(0, password) #Yenisini yazar. 
        except ValueError:
            status_label.config(text="Please enter a valid number.", fg="red")
    
    def on_copy_click():
        password = entry_result.get()
        if not password:
            status_label.config(text="First create a password!", fg="red")
            return
        if CLIP_AVAILABLE :
            pyperclip.copy(password)
            status_label.config(text="Copied the password to the clipboard.", fg="#05a124")
        else:
            status_label.config(text="ERROR: 'pyperclip' module is not installed.", fg="red")
    
    def on_qr_click():
        password = entry_result.get()
        filename = entry_qr_name.get().strip()
        if not password:
            status_label.config(text="First create a password for the QR Code!", fg="red")
            return
        if not filename:
            filename = "qrcode.png"
        if not filename.endswith(".png"):
            filename += ".png"
        if QR_AVAILABLE:
            try:
                path = create_qr_and_save(password, filepath=filename)
                status_label.config(text=f"QR Code Saved!: {path}", fg="#00FF00")
            except Exception as e:
                status_label.config(text=f"ERROR: {e}", fg="red")
        else:
                status_label.config(text="ERROR: 'qrcode' module is not installed!", fg="red")


    title_label = tk.Label(root, text = "Password Generator", font=("Arial", 24, "bold"), bg="#121212", fg="white")
    title_label.pack(pady=30) #pady=30: Üstten ve alttan 30 piksel boşluk bırak

    frame_settings = tk.Frame(root, bg="#121212") #Ayarları bir arada tutmak için görünmez bir kutu
    frame_settings.pack(pady=10)

    length_label = tk.Label(frame_settings, text = "Password Length:", font=("Arial", 15), bg="#121212", fg="white")
    length_label.pack(side=tk.LEFT, padx=10)     #Ekrana yerleştir
    entry_length = tk.Entry(frame_settings, font=("Arial", 15), width=5, justify="center")
    entry_length.insert(0, "12")  #Kutunun içine varsayılan olarak "12" yaz
    entry_length.pack(side=tk.LEFT, padx=10)

    mode_label = tk.Label(frame_settings, text = "Select Mode:",font=("Arial", 15), bg="#121212", fg="white")
    mode_label.pack(side=tk.LEFT, padx=10)
    modes = ["strong", "letters", "digits", "mixed"]
    #Seçilen değeri tutacak özel bir Tkinter değişkeni;
    var_mode = tk.StringVar(root)
    var_mode.set("strong")  #Varsayılan olarak "strong" seçili gelsin.
    mode_menu = tk.OptionMenu(frame_settings, var_mode, *modes)
    mode_menu.config(font=("Arial", 12))
    mode_menu.pack(side=tk.LEFT, padx=10)

    button_generate = tk.Button(root, text = "Generate Password", command =on_generate_click, bg = '#333333', fg = '#f54242', font=("Arial", 14, "bold"), activebackground="white")
    button_generate.pack(pady=20, ipadx=10, ipady=5)

    entry_result = tk.Entry(root, font = ("Courier", 18), width=30, justify="center", bg="#2D2D2D", fg="white")
    entry_result.pack(pady=10)

    frame_actions = tk.Frame(root, bg="#121212")
    frame_actions.pack(pady=20)

    button_copy = tk.Button(frame_actions, text="Copy", command=on_copy_click, bg="#444", fg="white", font=("Arial", 12))
    button_copy.pack(side=tk.LEFT, padx=20)

    button_qr = tk.Button(frame_actions,text="Save QR Code", command=on_qr_click, bg="#444", fg="white", font=("Arial", 12))
    button_qr.pack(side=tk.LEFT, padx=20)

    label_qr = tk.Label(root, text="QR Dosya Adi:", bg="#121212", fg="gray")
    label_qr.pack(pady=(10, 0))
    entry_qr_name = tk.Entry(root, bg="#2D2D2D", fg="white", justify="center")
    entry_qr_name.insert(0, "qrcode.png")
    entry_qr_name.pack(pady=5)

    status_label = tk.Label(root, text="Ready", font=("Arial", 12), bg="#121212", fg="gray")
    status_label.pack(side=tk.BOTTOM, pady=30)
    

    root.mainloop()

if __name__ == "__main__":
    start_gui()


