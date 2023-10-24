import sqlite3
conn = sqlite3.connect(r"D:\new\sqdatapro2.db")
cursor = conn.cursor()                                       

from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import time 
from tkinter import messagebox, Listbox ,StringVar,font
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import Toplevel, Label, Entry, Button, filedialog
import tkinter.font as tkFont
import sqlite3
from tkinter import filedialog
import io
from PIL import Image, ImageTk
from io import BytesIO


cart_items = []
total_price = 0
total = 0                               
image_tk = None  
receipt_window = None  
order_items = []


#หน้าแรกของโปรแกรม
root = Tk()
root.title("น้ำผลไม้สกัดดาวรุ่ง")
root.geometry("900x600+390+120")
root.resizable(False, False)
imggg = Image.open(r"D:\\new\\eieiphoto\\main.png")
root_imggg = ImageTk.PhotoImage(imggg)
Label(root,image=root_imggg).place(x=0)   

def checkint(P):  
    if P.isdigit() or P == "":
        return True
    else:
        return False 
z=[]

def edit():
    selected_product = products_listbox.curselection()
    if selected_product:                                        
        a = selected_product[0]
        idedit = z[a]
        name = name_entry.get()
        price = price_entry.get()
        file_pic = filedialog.askopenfilename()
        if file_pic:                                     
            with open(file_pic, 'rb') as file:
                picture = file.read()      
        cursor.execute('''UPDATE store SET name =?,price =?,picture=? WHERE id =? ''',(name, price, picture, idedit))
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        conn.commit()
        show()
#เพิ่มภาพ
def add():
    name = name_entry.get()  
    price = price_entry.get()      
    

    file_ = filedialog.askopenfilename()   
        with open(file_, 'rb')as file:
            picture = file.read()
    if name and price  and picture:
        cursor.execute("INSERT INTO store (name, price,picture) VALUES (?, ?, ?)", (name, price, picture))        
        conn.commit()
        
        name_entry.delete(0, tk.END) 
        price_entry.delete(0, tk.END)
        show()
#ลบรายการที่ adminกรอก
def delete():
    selected_product = products_listbox.curselection()
    if selected_product:
        a = selected_product[0]
        product_id = z[a]        
        cursor.execute("DELETE FROM store WHERE id=?", (product_id,))
        conn.commit()
        show() 

def show():                                                   
    products_listbox.delete(0, tk.END)   
    c = conn.cursor()
    c.execute('''SELECT * FROM store''')                
    result = c.fetchall()
    i = 1
    z.clear()

    for x in result:
        products_listbox.insert(x[0]," Product No:  {}    {}    price:  {} ".format(i,x[1],x[2],x[3]))
        z.append(x[0])
        i+=1 

 #หน้าต่างเพิ่มลบสินค้า
def back():
    admin_new_waterwindow.destroy()   

    #login แอดมิน
def admin1():     
    global admin_window
    global check_login

    admin_window = Toplevel(root)
    admin_window.title("สำหรับแอดมิน")
    admin_window.geometry("500x350+390+120")  
    admin_window.resizable(False, False)
    imgg=Image.open('admin1.png')
    admin_window.imgg=ImageTk.PhotoImage(imgg)
    Label(admin_window,image=admin_window.imgg).place(x=0)


    def check_login(): 
            password = codeadmin.get()
            if password == "" :
                messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกรหัสผ่านให้ถูกต้อง")
            elif password == "999":   
                admin_window.destroy()
                add_new_water() 
    

    def add_new_water():
        global admin_window, products_listbox, name_entry, price_entry, z, admin_new_waterwindow

        admin_new_waterwindow = Toplevel(root)
        admin_new_waterwindow.title("เพิ่มรายการสินค้าใหม่")
        admin_new_waterwindow.geometry("900x600+390+120")
        admin_new_waterwindow.resizable(False, False)

        #สร้างตัวแปรเพื่อเก็บวันที่
        selected_date = tk.StringVar()

        #แสดงประวัติคำสั่งซื้อรายวัน
        def show_daily_orders():
            date = selected_date.get() 
            daily_sales = calculate_daily_sales(date)
            
            daily_sales_label.config(text=f"วันที่ {date}: {daily_sales} บาท")
            daily_sales_label.place(x=615, y=95)

        #คำนวณยอดขายรายวันโดยค้นหาข้อมูลจากฐานข้อมูล SQLite
        def calculate_daily_sales(date):

            conn = sqlite3.connect(r"D:\new\sqdatapro2.db")
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(price) FROM bill WHERE date = ?", (date,)) #วิธีกรอก 12/09/2023

            result = cursor.fetchone() 
            return result[0] if result[0] else 0

        #สร้างตัวแปรเพื่อเก็บรายเดือน
        selected_month = tk.StringVar()

        #แสดง
        def show_monthly_orders():
            month = selected_month.get()  
            monthly_sales = calculate_monthly_sales(month)
            #แสดงผลลัพธ์บน Label
            monthly_sales_label.config(text=f"เดือน {month}: {monthly_sales} บาท")
            monthly_sales_label.place(x=620, y=220)

        def calculate_monthly_sales(month):
            conn = sqlite3.connect(r"D:\new\sqdatapro2.db")
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(price) FROM bill WHERE (month) = ?", (month,))  
            result = cursor.fetchone() #fetchone คือการดึงข้อมูล
            return result[0] if result[0] else 0 #ถ้าไม่มีข้อมูลจะขึ้น 0


        img4=Image.open('admin2.png')
        admin_new_waterwindow.img4=ImageTk.PhotoImage(img4)
        Label(admin_new_waterwindow,image=admin_new_waterwindow.img4).place(x=0)


        #แสดงผลลัพธ์ของยอดขายรายวัน
        daily_sales_label = tk.Label(admin_new_waterwindow, text="", font=12)
        daily_sales_label.place(x=785, y=80)

        #สร้างเมนูเลือกวันที่ในแท็บรายวัน
        date_entry = tk.Entry(admin_new_waterwindow, textvariable=selected_date, font=18,justify="center")
        date_entry.place(x=635, y=120,width=200,height=30)
        show_daily_button = tk.Button(admin_new_waterwindow, text="แสดงประวัติรายวัน",fg="black",bg="#F7FFE3",command=show_daily_orders,font=18)
        show_daily_button.place(x=665, y=155)

        #แสดงผลลัพธ์ของยอดขายรายเดือน
        monthly_sales_label = tk.Label(admin_new_waterwindow, text="", font=12)
        monthly_sales_label.pack()

        #สร้างเมนูเลือกเดือนในแท็บรายเดือน
        month_entry = tk.Entry(admin_new_waterwindow, textvariable=selected_month, font=18,width=15,justify="center")
        month_entry.place(x=635, y=243,width=200,height=30)
        show_monthly_button = tk.Button(admin_new_waterwindow, text="แสดงประวัติรายเดือน",fg="black",bg="#F7FFE3", command=show_monthly_orders,font=18)
        show_monthly_button.place(x=660, y=280)
        

        name_entry = tk.Entry(admin_new_waterwindow, bg="#ffffff", borderwidth="1px", font=("Times", 17), fg="#000000", justify="center", relief="sunken")
        name_entry.place(x=40, y=110, width=250, height=50)

        validate_func = admin_new_waterwindow.register(checkint)
        price_entry=tk.Entry(admin_new_waterwindow,validate='key',validatecommand=(validate_func, "%P"),bg="#ffffff", borderwidth="1px", font=("Times", 17), fg="#000000", justify="center", relief="sunken")
        price_entry.place(x=40,y=210,width=250,height=50)
        

        add_button = tk.Button(admin_new_waterwindow, bg="#F7FFE3", font=("Times", 17), fg="#000000", justify="center", text="ADD",  borderwidth="3px",command=add)
        add_button.place(x=320, y=70, width=250, height=64)

        delete_button = tk.Button(admin_new_waterwindow, bg="#F7FFE3", font=("Times", 17), fg="#000000", justify="center", text="DELETE", borderwidth="3px",command=delete)
        delete_button.place(x=320, y=160, width=250, height=64)

        edit_button = tk.Button(admin_new_waterwindow, bg="#F7FFE3", font=("Times", 17), fg="#000000", justify="center", text="EDIT", borderwidth="3px",command=edit)
        edit_button.place(x=320, y=249, width=250, height=64)

                
        name_label = tk.Label(admin_new_waterwindow, bg="#000000", font=("Times", 13), fg="#ffffff", justify="center",borderwidth="1px", text="ชื่อสินค้า", relief="sunken")
        name_label.place(x=96, y=88, width=140, height=30)

        price_label = tk.Label(admin_new_waterwindow, bg="#000000", font=("Times", 13), fg="#ffffff", justify="center",borderwidth="1px", text="ราคาสินค้า", relief="sunken")
        price_label.place(x=96, y=188, width=140, height=30)


        products_listbox = tk.Listbox(admin_new_waterwindow, bg="#ffffff", borderwidth="4px", font=("Times", 14), fg="#333333", relief="sunken")
        products_listbox.place(x=30, y=350, width=840, height=220)

        end = tk.Button(admin_new_waterwindow, bg="#76b666", font=("Times", 20), justify="center", text="🔙", borderwidth="3px",command=back, highlightthickness=0, bd=0)
        end.place(x=9, y=8, width=40, height=40)
        show()
                
                
    #รหัส
    tel_var = tk.IntVar()
    tel_var.set("")
    codeadmin =tk.Entry(admin_window,textvariable=tel_var,font=("Arial", 15),width=15, justify="center") 
    codeadmin.place(x=170,y=175)
    custom_font = tkFont.Font(size=14)
    pum6 = Button(admin_window,text="ยืนยัน",fg="white",bg="#76b666",font=custom_font,width=5,height=1,command=check_login)
    pum6.place(x=225,y=230)

l = PhotoImage(file='adminpum.png')
pum5 = Button(root,image=l,command=admin1, highlightthickness=0, bd=0)
pum5.place(x=843,y=10)

# สร้างหน้าต่างเมนูสรรพคุณ
#เชื่อมปุ่มกับหน้าเมนู
def menuushow():
    global menu_window,photo
    menu_window = Toplevel(root)  
    menu_window.title("เมนู")
    menu_window.geometry("900x600+390+120")
    menu_window.resizable(False, False)

    img = Image.open(r"D:\\new\\eieiphoto\\menu.png")
    photo = ImageTk.PhotoImage(img)

    lbl = Label(menu_window, image=photo)
    lbl.pack()

    def backtoroot():
        menu_window.destroy()

    menu_window.protocol("WM_DELETE_WINDOW", backtoroot)

    back10 = tk.Button(menu_window, text="🔙", command=backtoroot,font=20,bg="#E1F4EA", highlightthickness=0, bd=0)
    back10.place(x=5, y=4)
        

custom_font = tkFont.Font(size=14)
pum1 = Button(root,text="เมนู",fg="white",bg="#76b666",font=custom_font,width=13,height=1,command=menuushow)
pum1.place(x=608,y=235)


#หน้าสั่งซื้อ
#เชื่อมปุ่มกับหน้าorder
def ordershow():
    def order_show_product():
            cursor.execute("SELECT * FROM store")
            pictures = cursor.fetchall()
            
            
            def addtocart(item):
                def add():
                    c = conn.cursor()
                    c.execute("INSERT INTO myOrder (name, price, picture) VALUES (?, ?, ?)", (item[1], item[2], item[3]))
                    conn.commit()
                    add_to_cart()
                return add

            for i, x in enumerate(pictures):    
                image = Image.open(BytesIO(x[3]))
                target_width, target_height = 87, 80  
                image = image.resize((target_width, target_height))   
                image = ImageTk.PhotoImage(image)    

                custom3_font = tkFont.Font(size=11)
                label = Button(product, image=image, text=" {}  $ {} ".format(x[1], x[2]), compound="top", command=addtocart(x), bg= "#76B666", fg="white",font=custom3_font, width=100, height=100)
                label.image = image
                label.grid(row=i // 4, column=i % 4, padx=10, pady=10)

    def on_mousewheel(event):      
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")


    order_window = Toplevel()  
    order_window.title("ordernow")
    order_window.geometry("900x600+390+120")
    order_window.configure(bg="#76B666")
    screenwidth = order_window.winfo_screenwidth()
    screenheight = order_window.winfo_screenheight()
    order_window.resizable(False, False)
    
    c = PhotoImage(file="tt.png") 
    namestore=Label(order_window,image=c)
    namestore.place(x=200,y=20,width=498,height=66)


    canvas = Canvas(order_window, bg="#F7FFE3") 
    canvas.place(x=50, y=100, width=517, height=450)
    product = Frame(canvas, bg="#F7FFE3") 
    canvas.create_window((0, 0), window=product, anchor='nw')
    order_window.bind("<MouseWheel>", on_mousewheel) 

    order_show_product()

    #แสดงสินค้าที่เพิ่มจากแอดมิน
    for item in order_items:
        item_label = Label(order_window, text=f"{item['name']} - {item['price']} บาท", font=('arial', 12), bg='#E6E6E6')
        item_label.pack()
    
        #เพิ่มเข้าตะกร้า 
    def add_to_cart():
        global total_price
        
        cart_items.clear()
        cursor.execute("SELECT * FROM myOrder")
        order = cursor.fetchall()
        #item_name,item_price=order'
        for item_name,item_price,picture in order:
    
                cart_items.append((item_name,item_price))
                
        total_price += item_price
        
        update_cart_listbox()  
        update_total_label()   
        
        
    #ลบของออกจากตะกร้าลดยอดรวมและอัปเดตการแสดงผลของรายการในตะกร้าและยอดรวมทั้งหมด
    def remove_from_cart():
        global total_price
        cursor.execute('''DELETE FROM myOrder''')
        conn.commit()
        cart_items.clear()
        total_price = 0
        
        update_cart_listbox()
        update_total_label()

    #เป็นการอัปเดตข้อมูลในตะกร้า
    def update_cart_listbox():
        cart_listbox.delete(0,END) 
        for (name, price) in (cart_items):
            item_text = f"     {name}      {price:.2f} " 
            cart_listbox.insert(tk.END, item_text)
        
    
    #ลบและคำนวณ
    def remove_selected_item():
        remove_from_cart()  
        total = sum(sinka[1] for sinka in cart_items)
        
        if total >= 200:
            discount = 10  
            total -= discount 
            

        else:
            discount = 0
            pass

    remove_button = tk.Button(order_window, text="ล้างรายการที่เลือก", command=remove_selected_item,font=26,bg="#F7FFE3")
    remove_button.pack()
    remove_button.place(x=690, y=493)
    

    # สร้างใบเสร็จ
   
    def generate_receipt(items, total, discount):
        global receipt_window  
        named_tuple = time.localtime()  
        time_string = time.strftime("%d/%m/%Y", named_tuple)

        named_tuple1 = time.localtime() 
        time_string1 = time.strftime("%m/%Y", named_tuple1)

    
        receipt_window = Toplevel(root)
        receipt_window.title("ใบเสร็จ")
        receipt_window.geometry("300x600+450+150")
        receipt_window.resizable(False, False)
    

        bill = Image.open('orderbill.png')
        root.bill = ImageTk.PhotoImage(bill)

        # สร้าง Label และเก็บ bill_now ในตัวแปร label
        label = Label(receipt_window, image=root.bill)
        label.place(x=0, y=0)  # ระบุตำแหน่ง x และ y ที่ต้องการแสดง Label

        receipt = f"รายการทั้งหมด\n\n"
        for item, price in items:
            receipt += f"{item}           {price:.2f} บาท\n"
        receipt += f"\n\n\nยอดรวม            {total_price:.2f} บาท\n"
        priceprice=total_price - discount
        receipt += f"ส่วนลด             {discount:.2f} บาท\n"
        receipt += f"ยอดสุทธิ           {priceprice:.2f} บาท\n\n"
        receipt += f"{time_string}"

        # แสดงใบเสร็จใน Label
        receipt_label = Label(receipt_window, text=receipt, font=("Arial", 12),bg="#F7FFE3")
        receipt_label.place(x=62, y=117)

        
        cursor.execute("INSERT INTO bill (order_total,date,price,month) VALUES (?, ?, ?,?)", (receipt, time_string,priceprice,time_string1))
        conn.commit()

        receipt_window.protocol("WM_DELETE_WINDOW", clearlist)
         
    
    #ชำระเงิน
    def checkout():
        total = sum(sinka[1] for sinka in cart_items)
        discount = 0
    
        if total >= 200:
            discount = 10     
            total -= discount

        global receipt_window            
        generate_receipt(cart_items, total, discount) 
        
   
    checkout_button = tk.Button(order_window, text="ชำระเงิน", command=checkout,font=24,bg="#F7FFE3")
    checkout_button.pack()
    checkout_button.place(x=748, y=545)

    def backto():   
        order_window.destroy()
        

    order_window.protocol("WM_DELETE_WINDOW", backto)
    back = tk.Button(order_window, text="🔙", command=backto,font=20,bg="#F7FFE3", highlightthickness=0, bd=0)
    back.place(x=9, y=8)

    #เคลียร์ของในlistbox
    def clearlist(): 
        global total_price
        global receipt_window  
        while len(cart_items) > 0:   
            item_name, item_price = cart_items.pop()  
            item_name = 0
            item_price = 0
            total_price = 0
            update_total_label()
            cursor.execute('''DELETE FROM myOrder ''')
            conn.commit()
            cart_listbox.delete(0,END)
            receipt_window.destroy()
        

    def update_total_label():
        total_ver.set(f"รวมทั้งหมด          {total_price:.2f} บาท")
        total_label.config(font=("Arial", 14),bg="#F7FFE3")
        total_label.place(x=635,y=435)


    #แสดงรายการในรถเข็น
    cart_listbox = Listbox(order_window, width=25, height=20,font=16,bg="#F7FFE3")
    cart_listbox.place(x=630, y=100)
    

    total_ver = StringVar()
    total_label = tk.Label(order_window, textvariable=total_ver, font=("Arial", 12))
    total_label.pack()
    total_label.place(x=600, y=450)
    
    order_window.mainloop()
    
custom1_font = tkFont.Font(size=14)
pum2 = Button(root,text="สั่งซื้อตอนนี้",fg="white",bg="red",font=custom1_font,width=13,height=1,command=ordershow)
pum2.place(x=608,y=295)


#เชื่อมปุ่มกับหน้าสมัครสมาชิก
def memberr():

    def get_name():  
        name = et1.get()   
        tel = et2.get()#ล้างข้อมูล
        et2.delete(0,END)
        

        named_tuple = time.localtime() # get struct_time
        time_string = time.strftime("%d/%m/%Y, %H:%M:%S", named_tuple)

        if len(tel) !=10 or not tel.isdigit():
            messagebox.showerror("error","กรุณากรอกหมายเลข 10 หลัก")
        else:
            
            cursor.execute("INSERT INTO shopmember (name_member, tel, date) VALUES (?, ?, ?)", (name, tel, time_string))
            conn.commit()
            
            love3.destroy()
            messagebox.showinfo("CONFIRM", "สมัครสมาชิกสำเร็จ")
            
            
    love3 = Toplevel(root)  # สร้างหน้าต่างย่อย
    love3.title("member")
    love3.geometry("900x600+390+120")
    love3.resizable(False,False)
    img=Image.open('member1.png')
    root.img=ImageTk.PhotoImage(img)
    Label(love3,image=root.img).place(x=0)
    
    name_var = tk.StringVar()  
    et1 = tk.Entry(love3, textvariable=name_var,font=("Arial", 15),width=15) #Entryboxเป็นช่องให้พิมข้อความ
    et1.place(x=380,y=250)

    tel_var = tk.IntVar()
    tel_var.set("")
    et2=tk.Entry(love3,textvariable=tel_var,font=("Arial", 15),width=15) #Entryboxเป็นช่องให้พิมข้อความ
    et2.place(x=380,y=307)
    
    
    pum3 = Button(love3,text="ยืนยัน",fg="white",bg="#76b666",font=10,width=10,height=1, command=get_name)
    pum3.place(x=398,y=410)
    
    def backbackback():
        love3.destroy()
    
    love3.protocol("WM_DELETE_WINDOW", backbackback)
    pum5555 = tk.Button(love3, text="🔙", command=backbackback,font=20, highlightthickness=0, bd=0)
    pum5555.place(x=9, y=8)

    
custom2_font = tkFont.Font(size=14)
pum3 = Button(root,text="สมัครสมาชิก",fg="white",bg="#76b666",font=custom2_font,width=13,height=1,command=memberr)
pum3.place(x=608,y=355)


#ผู้พัฒนา
def Creatorshow():
    love4_window = Toplevel(root)
    love4_window.title("ผู้พัฒนา")
    love4_window.geometry("500x350+450+150")
    love4_window.resizable(False,False)
    diphoto=Image.open('D:\\new\\eieiphoto\\di.png')
    root.diphoto=ImageTk.PhotoImage(diphoto)
    Label(love4_window,image=root.diphoto).place(x=0)

custom3_font = tkFont.Font(size=14)
pum4 = Button(root,text="ผู้พัฒนา",fg="white",bg="#76b666",font=custom3_font,width=13,height=1,command=Creatorshow)
pum4.place(x=608,y=415)

#ออกจากโปรแกรม
def exitProgram(): 
    result = messagebox.askquestion("ยืนยันการออก", "คุณต้องการที่จะออกจากโปรแกรมหรือไม่?")
    if result == "yes": 
        root.destroy()

root.protocol("WM_DELETE_WINDOW", exitProgram)  

root.mainloop()