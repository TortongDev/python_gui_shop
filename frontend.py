import tkinter as tk
from tkinter import messagebox
import mysql.connector
import random
import tkinter as tk
from PIL import Image, ImageTk

# MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="cocoa_more"
)

mycursor = mydb.cursor()

# Reservation System
class ReservationSystemGUI:
    def __init__(gui, root):
        gui.root = root
        gui.root.title("ระบบจอง")
        image_path = "./logo-anamai.png"
        img = Image.open(image_path)
        width = 300
        height = 100
        img = img.resize((width, height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        image_label = tk.Label(gui.root, image=photo)
        image_label.pack()

        gui.menu_items = {
            "-": 0,
            "Iceberg Banoffee": 50.0,
            "Iceberg Black Magic": 40.0,
            "Iceberg CCM Combo": 60.0,
            "Iceberg Cocoa Cheesecake": 60.0,
            "Iceberg Blueberry Cheesecake": 60.0,
            "Iceberg Cocoa Twist": 60.0,
            "Iceberg Greentea Twist": 60.0,
            "Iceberg Snow White": 60.0,
            "IIceberg Thai-Thai": 60.0,
        }

        gui.selected_menu_items = {}
        gui.data_item_detail = {}
        gui.data_item_detail_push = []
        gui.name_var = tk.StringVar()
        gui.phone_var = tk.StringVar()
        gui.num_people_var = tk.IntVar()
        gui.reservation_time_var = tk.StringVar()
        gui.menu_var = tk.StringVar()
        gui.menu_var.set(list(gui.menu_items.keys())[0])
        gui.quantity_var = tk.IntVar(value=1)
        gui.table_number_var = tk.StringVar()
        gui.total_sales_var = tk.DoubleVar(value=0.0)
        gui.total_revenue_var = tk.DoubleVar(value=0.0)
        gui.create_customer_info_frame()
        gui.create_menu_frame()

    # function สร้างแบบฟอร์มบันทึกส่วนบน
    def create_customer_info_frame(gui):
        frame = tk.Frame(gui.root)
        frame.pack(padx=400, pady=30)
        tk.Label(frame, text="ชื่อ(ที่ใช้จอง):").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=gui.name_var).grid(row=0, column=1)
        tk.Label(frame, text="เบอร์โทรติดต่อ:").grid(row=1, column=0, sticky="w")
        tk.Entry(frame, textvariable=gui.phone_var).grid(row=1, column=1)
        tk.Label(frame, text="ระบุเวลาที่จะเข้าร้าน:").grid(row=2, column=0, sticky="w")
        tk.Entry(frame, textvariable=gui.reservation_time_var).grid(row=2, column=1)
        tk.Label(frame, text="จำนวนคนในกลุ่ม:").grid(row=3, column=0, sticky="w")
        tk.Entry(frame, textvariable=gui.num_people_var, validate="key",
                 validatecommand=(frame.register(gui.validate_num_people), '%P')).grid(row=3, column=1)
        tk.Label(frame, text="โต๊ะที่:").grid(row=4, column=0, sticky="w")
        tk.Entry(frame, textvariable=gui.table_number_var).grid(row=4, column=1)
        tk.Label(frame, text="เมนูอาหาร").grid(row=5, column=0, sticky="w")
        tk.OptionMenu(frame, gui.menu_var, *gui.menu_items.keys()).grid(row=5, column=1)
        tk.Label(frame, text="จำนวนที่สั่ง").grid(row=6, column=0, sticky="w")
        tk.Entry(frame, textvariable=gui.quantity_var).grid(row=6, column=1)
        tk.Label(frame, text="ยอดรวมจากการขายอาหาร:").grid(row=8, column=0, sticky="w")
        tk.Label(frame, textvariable=gui.total_sales_var).grid(row=8, column=1)
        tk.Label(frame, text="ยอดรวมจากค่าจองโต๊ะ: 50 บาท").grid(row=9, column=0, sticky="w")
        tk.Label(frame, text="สรุปยอดทั้งหมด:").grid(row=10, column=0, sticky="w")
        tk.Label(frame, textvariable=gui.total_revenue_var).grid(row=10, column=1)
    def validate_num_people(gui, value):
        return value.isdigit()
    
    # function ล้างค่าออกจาก กล่องข้อความ 
    def clear_all_fields(gui):
        gui.name_var.set("")
        gui.phone_var.set("")
        gui.num_people_var.set(0)
        gui.reservation_time_var.set("")
        gui.menu_var.set("")
        gui.quantity_var.set(1)

    # function ปุ่ม เมนู จัดการส่วนล่าง   
    def create_menu_frame(gui):
        frame = tk.Frame(gui.root)
        frame.pack(padx=10, pady=10)
        tk.Label(frame, text="เมนูที่สั่ง").grid(row=0, column=0, columnspan=2, pady=10)
        gui.menu_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=50)
        gui.menu_listbox.grid(row=1, column=0, columnspan=5, pady=5)
        gui.update_menu_listbox()
        tk.Button(frame, text="เพิ่มเมนู", command=gui.add_menu).grid(row=2, column=0, pady=5)
        tk.Button(frame, text="Clear เมนูอาหาร", command=gui.remove_menu).grid(row=2, column=1, pady=5)
        tk.Label(frame, text="จำนวนที่สั่ง").grid(row=3, column=0, pady=5)
        gui.quantity_label = tk.Label(frame, text="1")
        gui.quantity_label.grid(row=3, column=1, pady=5)
        tk.Button(frame, text="ยืนยันการจอง", command=gui.submit_customer_info).grid(row=5, column=0, columnspan=2, pady=10)

    # function เมื่อคลิกปุ่ม 'ยืนยันการจอง'
    def submit_customer_info(gui):
        # table order id
        insert_order ="INSERT INTO `order_menu`(`phone_number`, `datetime`, `table_number`, `sum_all_food`, `sum_all`) VALUES (%s,%s,%s,%s,%s)"
        val_order = (gui.phone_var.get(),gui.reservation_time_var.get(), gui.table_number_var.get(),gui.total_sales_var.get(),gui.total_revenue_var.get())
        mycursor.execute(insert_order,val_order)
        mydb.commit()

        for item_insert in gui.data_item_detail_push:
            gui.item_name = item_insert['name']
            gui.item_menu = item_insert['menu']
            gui.item_quantity = item_insert['quantity']
            # table order detail
            insert_order_detail ="INSERT INTO `order_menu_detail`( `food_name`, `table_number`, `queantity`, `price`) VALUES (%s,%s,%s,%s)"
            val_order_detail = ( gui.item_name, gui.table_number_var.get() ,gui.item_quantity , gui.item_menu)
            mycursor.execute(insert_order_detail,val_order_detail)
            mydb.commit()
            
            # messagebox.showinfo("บันทึกข้อมูลลูกค้าเสร็จสิ้น",
            #                     f"ชื่อ: {gui.name_var.get()}\nเบอร์โทร: {gui.phone_var.get()}\n"
            #                     f"จำนวนคน: {gui.num_people_var.get()}\nเวลา: {gui.reservation_time_var.get()}\n"
            #                     f"โต๊ะที่: {gui.table_number_var.get()}")
            
        # gui.clear_all_fields()

    # function เมื่อคลิก 'เพิ่มเมนู'
    def add_menu(gui):
        selected_menu = gui.menu_var.get()
        if selected_menu != "-":
            if selected_menu in gui.selected_menu_items:
                gui.selected_menu_items[selected_menu]["quantity"] += 1
            else:
                gui.selected_menu_items[selected_menu] = {"quantity": 1, "price": gui.menu_items[selected_menu]}
            found = False
            for item in gui.data_item_detail_push:
                if item["name"] == selected_menu:
                    item["quantity"] += 1
                    found = True
                    break

            if not found:
                gui.data_item_detail_push.append({"name": selected_menu, "menu": gui.menu_items[selected_menu], "quantity": 1})

            gui.update_menu_listbox()
            gui.update_total_price()

    # function เมื่อคลิก 'Clear เมนูอาหาร'
    def remove_menu(gui):
        gui.menu_listbox.delete(0, tk.END)
        selected_menu = gui.menu_var.get()
        if selected_menu != "-" and selected_menu in gui.selected_menu_items:
            if gui.selected_menu_items[selected_menu]["quantity"] > 1:
                gui.selected_menu_items[selected_menu]["quantity"] -= 1
            else:
                del gui.selected_menu_items[selected_menu]
            
            gui.data_item_detail_push = []
            gui.update_menu_listbox()
            gui.update_total_price()

    # function update ค่าใน Listbox ตอนกดเพิ่มเมนู เมนูจะเพิ่มเรื่อยๆ
    def update_menu_listbox(gui):
        gui.menu_listbox.delete(0, tk.END)
        for menu_item, details in gui.selected_menu_items.items():
            gui.menu_listbox.insert(tk.END, f"{menu_item} x{details['quantity']}")

   # function update คำนวนจำนวน ราคาของเมนู
    def update_total_price(gui):
        total_price = sum(details["quantity"] * details["price"] for details in gui.selected_menu_items.values())
        gui.total_sales_var.set(total_price)
        gui.total_revenue_var.set(total_price + 50)
        gui.quantity_label.config(text=str(gui.selected_menu_items[gui.menu_var.get()]["quantity"]))

if __name__ == "__main__":
    root = tk.Tk()
    reservation_app = ReservationSystemGUI(root)
    root.mainloop()