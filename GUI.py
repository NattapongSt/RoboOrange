import tkinter as tk
from tkinter import messagebox
from mainClass import *

# ฟังก์ชันสำหรับปุ่มส่งค่า
def send_weight():
    weight = weight_entry.get()
    if weight:  # ตรวจสอบว่ามีการกรอกน้ำหนัก
        sys = OrangeSys()
        #messagebox.showinfo("Weight Input", f"Weight entered: {weight} kg")
        sys.run(float(weight)*1000)
    else:
        messagebox.showwarning("Input Error", "Please enter a weight.")

# ฟังก์ชันสำหรับปุ่มเริ่มระบบ
def start_system():
    weight_label.pack(pady=(20, 5))  # แสดง Label น้ำหนัก
    weight_entry.pack(pady=5)  # แสดงช่องกรอกน้ำหนัก
    send_button.pack(pady=(5, 20))  # แสดงปุ่มส่งน้ำหนัก
    #messagebox.showinfo("System", "System Started!")

# ฟังก์ชันสำหรับปุ่มหยุดระบบ
def stop_system():
    weight_entry.pack_forget()  # ซ่อนช่องกรอกน้ำหนัก
    weight_entry.delete(0, tk.END)  # ลบค่าที่กรอกไว้
    weight_label.pack_forget()  # ซ่อน Label น้ำหนัก
    send_button.pack_forget()  # ซ่อนปุ่มส่งน้ำหนัก
    messagebox.showinfo("System", "System Stopped!")

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("RoboOrange")
root.geometry("400x300")
root.configure(bg="#e8f5e9")  # เปลี่ยนสีพื้นหลังให้ดูสดใส

# สร้าง Frame สำหรับปุ่ม Start และ Stop
button_frame = tk.Frame(root, bg="#e8f5e9")
button_frame.pack(pady=20)

# สร้างปุ่มสำหรับเริ่มระบบ
start_button = tk.Button(button_frame, text="Start System", command=start_system, 
                         bg="#4CAF50", fg="white", font=("Segoe UI", 12, "bold"),
                         relief="flat", bd=0, highlightthickness=0)
start_button.pack(side=tk.LEFT, padx=20)

# สร้างปุ่มสำหรับหยุดระบบ
stop_button = tk.Button(button_frame, text="Stop System", command=stop_system, 
                        bg="#f44336", fg="white", font=("Segoe UI", 12, "bold"),
                        relief="flat", bd=0, highlightthickness=0)
stop_button.pack(side=tk.LEFT, padx=20)

# สร้าง Label สำหรับน้ำหนัก
weight_label = tk.Label(root, text="Enter Weight (kg):", font=("Segoe UI", 14), bg="#e8f5e9")

# สร้าง Entry สำหรับกรอกน้ำหนัก (ซ่อนตั้งแต่แรก)
weight_entry = tk.Entry(root, font=("Segoe UI", 14), width=20, borderwidth=0,
                         highlightbackground="#2196F3", highlightcolor="#2196F3",
                         highlightthickness=2)

# สร้างปุ่มสำหรับส่งน้ำหนัก
send_button = tk.Button(root, text="Send Weight", command=send_weight, 
                        bg="#2196F3", fg="white", font=("Segoe UI", 12, "bold"),
                        relief="flat", bd=0, highlightthickness=0)

# ทำให้ปุ่มและ Entry มีขอบมน
for widget in [start_button, stop_button, send_button, weight_entry]:
    widget.config(highlightthickness=2, relief="flat")

# เริ่มการทำงานของ GUI
root.mainloop()
