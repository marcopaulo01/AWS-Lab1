import os
import subprocess
import tkinter as tk
from tkinter import font, ttk, filedialog, messagebox
import boto3

main_script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(main_script_dir)

root = tk.Tk()

root.title("Object Level Operation")
root.geometry("600x600")

session = boto3.Session(
    aws_access_key_id='Access key',
    aws_secret_access_key='Secret key',
    region_name='ca-central-1'
)

s3 = session.client('s3')

response = s3.list_buckets()
bucket_names = [bucket['Name'] for bucket in response['Buckets']]

def list_objects(event=None):
    selected_bucket = combo.get()
    if selected_bucket:
        objects = s3.list_objects_v2(Bucket=selected_bucket)
        object_name = [obj['Key'] for obj in objects.get('Contents',[])]
        #update listbox
        listbox.delete(0, tk.END)
        for obj_name in object_name:
            listbox.insert(tk.END, obj_name)

def back():
    subprocess.Popen(["python","main.py"])
    root.destroy()

def browse():
    file_path = filedialog.askopenfilename()
    if file_path:
        object_text_box.config(state='normal')
        object_text_box.delete(1.0, tk.END)
        object_text_box.insert(tk.END, file_path)
        object_text_box.config(state='disabled')

def upload():
    selected_bucket = combo.get()
    file_path = object_text_box.get("1.0", "end-1c")

    if not selected_bucket:
        messagebox.showerror("Error", "No bucket selected")
        return
    
    if not file_path:
        messagebox.showerror("Error", "No file selected")
        return
    
    try:
        s3.upload_file(file_path, selected_bucket, os.path.basename(file_path))
        messagebox.showinfo("Success", f"File uploaded to '{selected_bucket}' successfully.")
        list_objects()
        object_text_box.config(state='normal')
        object_text_box.delete(1.0, tk.END)
        object_text_box.config(state='disabled')
    except Exception as e:
        error_message = f"Error: {str(e)}"
        messagebox.showerror("Error", error_message)

backButton = tk.Button(root, text="Back to Main", bg="blue", fg="yellow", width=20, height=2, command=back)
backButton.place(x=440, y=535)

browseButton = tk.Button(root, text="Browse", bg="blue", fg="yellow",width=20, height=2, command=browse)
browseButton.place(x=440, y=70)

uploadButton = tk.Button(root, text="Upload", bg="blue", fg="yellow",width=20, height=2, command=upload)
uploadButton.place(x=440, y=125)

listbox = tk.Listbox(root,width=67, height=28)
listbox.place(x=25, y=125)

object_text_box = tk.Text(root, width=40, height=3, state="disabled")
object_text_box.place(x=105, y=70)

label_font = font.Font(size=12, weight="bold")
object_label = tk.Label(root, text="Object", font=label_font)
object_label.place(x=25, y=80)

bucket_label = tk.Label(root, text="Bucket", font=label_font)
bucket_label.place(x=25, y=40)

combo = ttk.Combobox(root, width=50)
combo['values'] = bucket_names
combo.bind("<<ComboboxSelected>>", list_objects)
combo.place(x=105, y=40)

root.mainloop()