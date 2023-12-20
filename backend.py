import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from tkcalendar import DateEntry

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="cocoa_more"
)

mycursor = mydb.cursor()
# ReservationSystemGUI()
class RestaurantSystem:
    def __init__(gui, root):
        gui.root = root
        gui.reservations = []
        gui.menu = []
        gui.sales = []
        gui.create_widgets()
   
    def create_widgets(gui):
        tab_control = ttk.Notebook(gui.root)

        tab1 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='ยกเลิกการจอง')

        tree_columns = ("Customer Name","โต๊ะที่","เวลาเข้าร้าน", "Status","Datetime")
        global tree
        tree = ttk.Treeview(tab1, columns=tree_columns, show="headings")
        for col in tree_columns:
            tree.heading(col, text=col)
        tree.pack(pady=10)
        query = "SELECT `order_id`,`customer_name`, `phone_number`, `datetime`, `table_number`, `sum_all_food`, `sum_all`, `Status` ,datetime_stamp FROM `order_menu` WHERE 1  AND Status = 'จอง' "
        mycursor.execute(query)
        reservation_data = mycursor.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for reservation in reservation_data:
            order_id        = reservation[0]
            customer_name   = reservation[1]
            phone_number    = reservation[2]
            datetime        = reservation[3]
            table_number    = reservation[4]
            sum_all_food    = reservation[5]
            sum_all         = reservation[6]
            status          = reservation[7]
            datetime_stamp  = reservation[8]
            sale_status = 'Completed' if status == 'Completed' else 'Not Completed'
            tree.insert("", "end", values=(customer_name, table_number, datetime,status,datetime_stamp))
        cancel_button = tk.Button(tab1, text="ยกเลิกการจอง", command=gui.cancel_reservation)
        cancel_button.pack()

        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab2, text='เมนูอาหาร')

        menu_columns = ("User_name", "Table", "Food_Name", "Price", "Quantity", "date")
        global menu_tree
        menu_tree = ttk.Treeview(tab2, columns=menu_columns, show="headings")
        for col in menu_columns:
            menu_tree.heading(col, text=col)
        menu_tree.pack(pady=10)
        gui.selected_item = menu_tree.selection()
        for item in gui.selected_item:
            menu_tree = tree.item(item, "values")[0]
        # print(menu_tree)
        query = "SELECT OM.`customer_name` , OM.`table_number` , OMD.food_name , OMD.price , OMD.queantity , OM.datetime FROM `order_menu` AS OM LEFT JOIN `order_menu_detail` AS OMD ON OMD.table_number = OM.table_number WHERE 1=1 AND Status = 'จอง' "
        mycursor.execute(query)
        reservation_data = mycursor.fetchall()
        for i in menu_tree.get_children():
            menu_tree.delete(i)
        for reservation in reservation_data:
            detail_customer_name   = reservation[0]
            detail_table_number    = reservation[1]
            detail_food_name       = reservation[2]
            detail_price           = reservation[3]
            detail_queantity       = reservation[4]
            detail_datetime        = reservation[5]
            
            sale_status = 'Completed' if status == 'Completed' else 'Not Completed'
            menu_tree.insert("", "end", values=(detail_customer_name, detail_table_number, detail_food_name,detail_price,detail_queantity,detail_datetime))

        edit_button = tk.Button(tab2, text="แก้ไขข้อมูล", command=gui.edit_order)
        edit_button.pack()
        add_button = tk.Button(tab2, text="เพิ่มรายการอาหาร", command=gui.save_order)
        add_button.pack()

        gui.customer_name_menu2 = tk.StringVar()
        gui.table_number_menu2  = tk.StringVar()
        gui.food_name_menu2     = tk.StringVar()
        gui.price_menu2         = tk.StringVar()
        gui.queantity           = tk.StringVar()

       
        gui.label_customer = tk.Label(tab2, text="Customer Name:")
        gui.label_customer.pack()
        gui.customer_name = tk.Entry(tab2,textvariable=gui.customer_name_menu2)
        gui.customer_name.pack()
        gui.label_table = tk.Label(tab2, text="โต๊ะที:")
        gui.label_table.pack()
        gui.table_numner = tk.Entry(tab2,textvariable=gui.table_number_menu2)
        gui.table_numner.pack()
        gui.label_food = tk.Label(tab2, text="อาหารที่สั่ง:")
        gui.label_food.pack()
        gui.food_name = tk.Entry(tab2,state='disabled' , textvariable=gui.food_name_menu2)
        gui.food_name.pack()
        gui.label_price = tk.Label(tab2, text="ราคา: ")
        gui.label_price.pack()
        gui.input_price = tk.Entry(tab2 , textvariable=gui.price_menu2)
        gui.input_price.pack()
        gui.label_queantity= tk.Label(tab2, text="จำนวน:")
        gui.label_queantity.pack()
        gui.input_queantity = tk.Entry(tab2 , textvariable=gui.queantity)
        gui.input_queantity.pack()
        gui.update_button = tk.Button(tab2, text="บันทึกการแก้ไข", command=gui.edit_order)
        gui.update_button.pack()


        # label_price = tk.Label(tab2, text="วัน//เวลา")
        # label_price.pack()
        # gui.entry_quantity = tk.Entry(tab2)
        # gui.entry_quantity.pack()
        tab_control.pack(expand=1, fill="both")
        tab3 = ttk.Frame(tab_control)
        tab_control.add(tab3, text='ระบบคิดบิล')
        cal = DateEntry(tab3, width=12, background="darkblue", foreground="white", borderwidth=2)
        cal.pack(padx=10, pady=10)
        label_category = tk.Label(tab3, text="ถึง")
        label_category.pack()
        cal = DateEntry(tab3, width=12, background="darkblue", foreground="white", borderwidth=2)
        cal.pack(padx=10, pady=10)

        bill_system = BillSystem(tab3)
        bill_system.create_widgets()

        tab_control.pack(expand=1, fill="both")
    def edit_order(gui):
        selected_item = menu_tree.selection()
       
        for item in selected_item:
            customer_name = menu_tree.item(item, "values")[0] #Customer_name
            sql_order = "SELECT OM.`customer_name` , OM.`table_number` , OMD.food_name , OMD.price , OMD.queantity , OM.datetime FROM `order_menu` AS OM LEFT JOIN `order_menu_detail` AS OMD ON OMD.table_number = OM.table_number WHERE 1=1 AND Status = 'จอง' AND OM.`customer_name` = %s "
            edit_order = (customer_name,)
            mycursor.execute(sql_order,edit_order)
            reservation_data = mycursor.fetchall()
            for i in menu_tree.get_children():
                menu_tree.delete(i)
            for reservation in reservation_data:
                customer_name   = reservation[0]
                table_number    = reservation[1]
                food_name       = reservation[2]
                price           = reservation[3]
                queantity       = reservation[4]
                # sale_status = 'Completed' if status == 'Completed' else 'Not Completed'
            gui.customer_name_menu2.set(customer_name)
            gui.table_number_menu2.set(table_number)
            gui.food_name_menu2.set(food_name)
            gui.price_menu2.set(price)
            gui.queantity.set(queantity)
    def save_order(gui):
                
        gui.label_customer.pack_forget()
        gui.label_table.pack_forget()
        gui.label_food.pack_forget()
        gui.label_price.pack_forget()
        gui.label_queantity.pack_forget()
        gui.update_button.pack_forget()
        gui.customer_name.pack_forget()
        gui.table_numner.pack_forget()
        gui.food_name.pack_forget()
        gui.input_price.pack_forget()
        gui.input_queantity.pack_forget()


    def cancel_reservation(gui):
        selected_item = tree.selection()
        for item in selected_item:
            customer_name = tree.item(item, "values")[0]
            update_status = "UPDATE order_menu SET Status = 'ยกเลิกจอง' WHERE 1 AND customer_name = %s"
            data_update = (customer_name,)
            mycursor.execute(update_status,data_update)
            mydb.commit()
            print(mycursor.rowcount, "record update.")
            gui.load_reservations()
    def load_reservations(gui):
        query = "SELECT `order_id`,`customer_name`, `phone_number`, `datetime`, `table_number`, `sum_all_food`, `sum_all`, `Status` ,datetime_stamp FROM `order_menu` WHERE 1  AND Status = 'จอง' "
        mycursor.execute(query)
        reservation_data = mycursor.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for reservation in reservation_data:
            order_id        = reservation[0]
            customer_name   = reservation[1]
            phone_number    = reservation[2]
            datetime        = reservation[3]
            table_number    = reservation[4]
            sum_all_food    = reservation[5]
            sum_all         = reservation[6]
            status          = reservation[7]
            datetime_stamp  = reservation[8]
            # sale_status = 'Completed' if status == 'Completed' else 'Not Completed'
            tree.insert("", "end", values=(customer_name, table_number, datetime,status,datetime_stamp))

class BillSystem:
    def __init__(gui, root):
        gui.root = root
        gui.selected_date = None

        # Add Calendar

    def create_widgets(gui):
        # # Combobox สำหรับวัน
        # gui.day_label = tk.Label(gui.root, text="วัน:")
        # gui.day_label.pack(side=tk.LEFT, padx=10, pady=10)
        # gui.days = [str(i) for i in range(1, 32)]
        # gui.day_var = tk.StringVar(value="1")
        # gui.day_combobox = ttk.Combobox(gui.root, textvariable=gui.day_var, values=gui.days)
        # gui.day_combobox.pack(side=tk.LEFT, padx=10, pady=10)



        # # Combobox สำหรับเดือน
        # gui.month_label = tk.Label(gui.root, text="เดือน:")
        # gui.month_label.pack(side=tk.LEFT, padx=10, pady=10)
        # gui.months = [
        #     "มกราคม", "กุมภาพันธ์", "มีนาคม",
        #     "เมษายน", "พฤษภาคม", "มิถุนายน",
        #     "กรกฎาคม", "สิงหาคม", "กันยายน",
        #     "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
        # ]
        # gui.month_var = tk.StringVar(value=gui.months[0])
        # gui.month_combobox = ttk.Combobox(gui.root, textvariable=gui.month_var, values=gui.months)
        # gui.month_combobox.pack(side=tk.LEFT, padx=10, pady=10)

        # # Combobox สำหรับปี
        # gui.year_label = tk.Label(gui.root, text="ปี:")
        # gui.year_label.pack(side=tk.LEFT, padx=10, pady=10)
        # gui.years = [str(i) for i in range(2022, 2030)]  # ปีตั้งแต่ 2022 - 2029
        # gui.year_var = tk.StringVar(value="2022")
        # gui.year_combobox = ttk.Combobox(gui.root, textvariable=gui.year_var, values=gui.years)
        # gui.year_combobox.pack(side=tk.LEFT, padx=10, pady=10)

        # # ปุ่มเลือกวันที่
        # gui.date_button = tk.Button(gui.root, text="เลือกวันที่", command=gui.select_date)
        # gui.date_button.pack(side=tk.TOP, padx=10, pady=10)

        # ปุ่มสรุปยอดขาย
        gui.summary_button = tk.Button(gui.root, text="สรุปยอดขายทั้งหมด", command=gui.summarize_sales)
        gui.summary_button.pack(side=tk.TOP, padx=10, pady=10)

        # ส่วนของตารางรายการขาย
        gui.tree = ttk.Treeview(gui.root, columns=("โต๊ะ","รายการ","จำนวน", "ยอดขายสุทธิ"))
        gui.tree.heading("#0", text="วันที่")
        gui.tree.heading("โต๊ะ", text="โต๊ะ")
        gui.tree.heading("รายการ", text="รายการ")
        gui.tree.heading("จำนวน", text="จำนวน")
        gui.tree.heading("ยอดขายสุทธิ", text="ยอดขายสุทธิ")
        gui.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # cal = Calendar(root, selectmode = 'day',
        #        year = 2020, month = 5,
        #        day = 22)
 
        # cal.pack(pady = 20)

    def select_date(gui):
        selected_day = gui.day_var.get()
        selected_month = gui.month_var.get()
        selected_year = gui.year_var.get()

        if selected_day and selected_month and selected_year:
            selected_date = f"{selected_day} {selected_month} {selected_year}"
            gui.selected_date = datetime.strptime(selected_date, "%d %B %Y").strftime("%d/%m/%Y")
            gui.date_button.config(text=f"วันที่: {gui.selected_date}")
        else:
            messagebox.showinfo("คำเตือน", "กรุณาเลือกวันที่ก่อนทำการสรุปยอดขาย")

    def summarize_sales(gui):
        if gui.selected_date:
            # สร้างข้อมูลสำหรับตารางรายการขาย
            sales_data = [
                {"วันที่": gui.selected_date, "รายการ": "สินค้า A", "ยอดขายสุทธิ": 1000},
                {"วันที่": gui.selected_date, "รายการ": "สินค้า B", "ยอดขายสุทธิ": 1500},
                # สามารถเพิ่มข้อมูลเพิ่มเติมได้ตามต้องการ
            ]

            # ลบข้อมูลเก่าในตาราง
            for item in gui.tree.get_children():
                gui.tree.delete(item)

            # นำข้อมูลใหม่เข้าตาราง
            for data in sales_data:
                gui.tree.insert("", tk.END, values=(data["วันที่"],data["โต๊ะ"], data["รายการ"], data["จำนวน"],data["ยอดขายสุทธิ"]))
        else:
            messagebox.showinfo("คำเตือน", "กรุณาเลือกวันที่ก่อนทำการสรุปยอดขาย")

        


if __name__ == "__main__":
    root = tk.Tk()
    root.title("ระบบหลังร้าน")
    system = RestaurantSystem(root)
    root.mainloop()
