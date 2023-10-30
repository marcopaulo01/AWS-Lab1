import tkinter as tk
import subprocess
import os

main_script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(main_script_dir)

root = tk.Tk()
root.title("Lab 1")
root.geometry("600x200")
root.resizable(False,False)
root.configure(bg='white')

def exit_program():
    root.destroy()

def open_bucket():
    subprocess.Popen(["python", "bucket.py"])
    root.destroy()

def open_object():
    subprocess.Popen(["python", "object.py"])
    root.destroy()

exitButton = tk.Button(root, text="Exit", width=20, height=3, bg="blue", fg="yellow", command=exit_program)
exitButton.place(x=425, y=75)

bucketButton = tk.Button(root, text="Bucket", width=20, height=3, bg="blue", fg="yellow", command=open_bucket)
bucketButton.place(x=25, y=75)

objectButton = tk.Button(root, text="Ojbect", width=20, height=3, bg="blue", fg="yellow", command=open_object)
objectButton.place(x=225, y=75)

root.mainloop()