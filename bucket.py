import tkinter as tk
from tkinter import font, messagebox
import subprocess
import os
import boto3

main_script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(main_script_dir)

root = tk.Tk()

root.title("Bucket Level Operation")
root.geometry("600x600")
root.resizable(False, False)

session = boto3.Session(
    aws_access_key_id='Access Key',
    aws_secret_access_key='Secret Key',
    region_name='ca-central-1'
)

s3 = session.client('s3')

# List S3 buckets
response = s3.list_buckets()

def back():
    subprocess.Popen(["python","main.py"])
    root.destroy()

def refresh_listbox():
    # Clear the current content of the Listbox
    listbox.delete(0, tk.END)

    # Insert updated data into the Listbox
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        listbox.insert(tk.END, bucket['Name'])

def create():
    bucket_name = bucket_name_textbox.get()

    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'ca-central-1'}
        )
        bucket_name_textbox.delete(0, tk.END)
        refresh_listbox()
        success_message = f"'{bucket_name}' created successfully."
        messagebox.showinfo("Success",success_message)

    except Exception as e:
        error_message = f"Error: {str(e)}"
        messagebox.showerror("Error", error_message)

def delete():
    selected_bucket = listbox.get(tk.ACTIVE)

    if not selected_bucket:
        messagebox.showerror("Error","No bucket selected for deletion.")
        return
    
    try:
        s3.delete_bucket(Bucket=selected_bucket)
        messagebox.showinfo("Success", f"'{selected_bucket}' deleted.")
        refresh_listbox()
    except Exception as e:
        error_message = f"Error: {str(e)}"
        messagebox.showerror("Error", error_message)

backButton = tk.Button(root, text="Back to Main", bg="blue", fg="yellow", width=30, height=2, command=back)
backButton.place(x=200, y=550)

listbox = tk.Listbox(root, width=90, height=26)
listbox.place(x=25, y=115)
for bucket in response['Buckets']:
    listbox.insert(tk.END, bucket['Name'])

bucket_label_font = font.Font(size=12, weight="bold")
bucket_label = tk.Label(root, text="Bucket Name", font=bucket_label_font)
bucket_label.place(x=25, y=10)

bucket_name_textbox = tk.Entry(root, width=40)
bucket_name_textbox.place(x=140, y=10)

createButton = tk.Button(root, text="Create", bg="blue", fg="yellow", width=10, command=create)
createButton.place(x=500, y=10)

deleteButton = tk.Button(root, text="Delete", bg="blue", fg="yellow", width=10, command=delete)
deleteButton.place(x=500, y=75)

root.mainloop()