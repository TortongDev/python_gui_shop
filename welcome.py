import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from tkcalendar import DateEntry

from frontend import ReservationSystemGUI 
from backend import RestaurantSystem, BillSystem 

class MainShop:
    def __init__(gui, root):
        frame = tk.Frame()
        frame.pack(padx=400, pady=30)
        image_label = tk.Label(frame, text='ระบบจองโต๊ะ' , pady=10)
        image_label.pack()
        button_program_user = tk.Button(frame, text="จองโต๊ะ (ลูกค้า)" , command=gui.program_user)
        button_program_user.pack()
        button_program_admin = tk.Button(frame, text="ระบบหลังบ้าน (พนักงาน)", command=gui.program_admin)
        button_program_admin.pack()
        root.mainloop()
 
    def program_user(gui):
        reservation_window = tk.Toplevel(root)
        reservation_window.title("ระบบจอง")
        reservation_app = ReservationSystemGUI(reservation_window)

        root.mainloop()
    def program_admin(gui):
        reservation_window = tk.Toplevel(root)
        reservation_window.title("ระบบจัดการหลังบ้าน")
        system = RestaurantSystem(reservation_window)

if __name__ == "__main__":
    root = tk.Tk()
    reservation_app = MainShop(root)
    root.mainloop()
