from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog
import os


# ---------------- KEY HANDLING ----------------
if os.path.exists("mykey.key"):
    with open("mykey.key", "rb") as mykey:
        key = mykey.read()
else:
    key = Fernet.generate_key()
    with open("mykey.key", "wb") as mykey:
        mykey.write(key)

    # Make the key file hidden
    try:
        if os.name == "nt":  # Windows
            os.system("attrib +h mykey.key")
        else:  # Linux / macOS
            os.rename("mykey.key", ".mykey.key")
    except Exception as e:
        print(f"Could not hide key file: {e}")

cipher = Fernet(key)
print("Key loaded successfully")


# ---------------- FILE PICKER ----------------
root = tk.Tk()
root.withdraw()


file_path = filedialog.askopenfilename(
    title="Select your file",
    filetypes=(("All files", "*.*"),
    )
)
root.destroy()

if not file_path:
    print("No file wa selected...")
    
else:
    # ---------------- USER INPUT ----------------
    print("1 - Encrypt\n2 - Decrypt")
    operation = input("Select operation: ")


    # ---------------- ENCRYPT ----------------
    if operation == "1":
        if file_path:
            try:
                with open(file_path, "rb") as f:
                    content = f.read()

                encrypted = cipher.encrypt(content)

                filename = os.path.basename(file_path)

                with open(f"{filename}.enc", "wb") as f:
                    f.write(encrypted)

                print("File encrypted successfully!")

            except Exception as e:
                print(f"Error: {e}")

        else:
            print("No file selected!")



    # ---------------- DECRYPT ----------------
    elif operation == "2":
        if file_path:
            try:
                with open(file_path, "rb") as f:
                    content = f.read()

                decrypted = cipher.decrypt(content)

                filename = os.path.basename(file_path)

                # remove .enc if present
                if filename.endswith(".enc"):
                    filename = filename.replace(".enc", "")

                with open(f"decrypted_{filename}", "wb") as f:
                    f.write(decrypted)

                print("File decrypted successfully!")

            except Exception as e:
                print(f"Error: {e}")

        else:
            print("No file selected!")

    else:
        print("Invalid option")