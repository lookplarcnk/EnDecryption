import os
import tkinter as tk
from tkinter import filedialog
import tempfile
import shutil

# search file and directory
def encrypt_decrypt_file(file_path, key, operation):
    try:
        with open(file_path, 'rb') as fin:
            content = bytearray(fin.read())

        for index, values in enumerate(content):
            content[index] = values ^ key

        # Use a temporary file to avoid overwriting the original
        temp_file_path = tempfile.mktemp()
        with open(temp_file_path, 'wb') as fout:
            fout.write(content)

        # Move the temporary file to the original file
        shutil.move(temp_file_path, file_path)

        result_label.config(text=f'{operation} Done for {file_path}.')
    # call err
    except FileNotFoundError:
        result_label.config(text=f'Error: File not found - {file_path}')
    except ValueError:
        result_label.config(text='Error: Invalid key. Please enter a valid integer key.')
    except Exception as e:
        result_label.config(text=f'Error caught: {type(e).__name__} - {e}')

def browse_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)
    operation_var.set("Single File")

def browse_directory():
    directory_path = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, directory_path)
    operation_var.set("All Files")

def process_encryption_decryption():
    selected_operation = operation_var.get()
    key = int(key_entry.get())

    if selected_operation == "Single File":
        file_path = file_entry.get()
        encrypt_decrypt_file(file_path, key, 'Encryption/Decryption')
    elif selected_operation == "All Files":
        directory = directory_entry.get()

        if not os.path.isdir(directory):
            result_label.config(text=f'Error: {directory} is not a valid directory.')
            return

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                encrypt_decrypt_file(file_path, key, 'Encryption/Decryption')

# GUI setup
root = tk.Tk()
root.title("File Encryption and Decryption")
root.geometry('600x400')
root.config(bg='#E0F0FF')

# Operation Selection
operation_var = tk.StringVar()
operation_var.set("Single File")

operation_label = tk.Label(root, text="Select Operation:")
operation_label.pack(pady=5)
operation_label.config(bg='#FFFFFF') 

single_file_radio = tk.Radiobutton(root, text="Single File", variable=operation_var, value="Single File")
single_file_radio.pack(pady=5)
single_file_radio.config(bg='#FFFFFF') 

all_files_radio = tk.Radiobutton(root, text="All Files", variable=operation_var, value="All Files")
all_files_radio.pack(pady=5)
all_files_radio.config(bg='#FFFFFF')

# File/Directory Path Entry
file_label = tk.Label(root, text="File/Directory Path:")
file_label.pack(pady=5)
file_label.config(bg='#FFFFFF')  

file_entry = tk.Entry(root, width=50)
file_entry.pack()

browse_button = tk.Button(root, text="Browse", command=lambda: browse_file() if operation_var.get() == "Single File" else browse_directory())
browse_button.pack(pady=5)

# Directory Entry
directory_label = tk.Label(root, text="Directory Path (for All Files):")
directory_label.pack(pady=5)
directory_label.config(bg='#FFFFFF')  

directory_entry = tk.Entry(root, width=50)
directory_entry.pack()

# Encryption Key Entry
key_label = tk.Label(root, text="Encryption/Decryption Key:")
key_label.pack(pady=5)
key_label.config(bg='#FFFFFF')  

key_entry = tk.Entry(root)
key_entry.pack()

# Button for Encryption/Decryption
process_button = tk.Button(root, text="Encrypt/Decrypt", command=process_encryption_decryption)
process_button.pack(pady=5)

# Result Label
result_label = tk.Label(root, text="Made by RMUTL Student")
result_label.pack(pady=5)
result_label.config(bg='#FFFFFF')

root.mainloop()
