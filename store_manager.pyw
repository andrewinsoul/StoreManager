import datetime
import os
import sqlite3
import time
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk

from PIL import Image, ImageTk
from sys import exit

import approximator as apprx
import money_validator as mv
import quantity_converter as qc

"""This simple app helps in maintaining day-to-day transaction in your company"""
initializer = sqlite3.connect('store.db')
cursor = initializer.cursor()

sql_code = \
    '''
    CREATE TABLE IF NOT EXISTS products
    (
    id_number INTEGER PRIMARY KEY,
    Name_Of_Product VARCHAR(80),
    Quantity_Of_Product VARCHAR(20),
    Price_Of_Product VARCHAR(20)
    );
    '''
cursor.execute(sql_code)

# sql_code = \
# '''
# CREATE TABLE IF NOT EXISTS sales
# (
# sn INTEGER PRIMARY KEY,
# Date_Of_Sales DATE,
# Name_Of_Product VARCHAR(80),
# Quantity_Sold_Out VARCHAR(20),
# Price_Realized VARCHAR(25)
# );
# '''
# cursor.execute(sql_code)

# sql_code = \
# '''
# CREATE TABLE IF NOT EXISTS expenses
# (
# sn INTEGER PRIMARY KEY,
# Date DATE,
# Purpose_Of_Expenses VARCHAR(350),
# Amount_Spent VARCHAR(25)
# );
# '''
# cursor.execute(sql_code)
#
sql_code = \
    '''
    CREATE TABLE IF NOT EXISTS company_credentials
    (
    sn INTEGER PRIMARY KEY,
    name_of_company VARCHAR(100),
    password1 VARCHAR(16),
    password2 VARCHAR(16)
    );
    '''
cursor.execute(sql_code)

sql_code = \
    '''
    CREATE TABLE IF NOT EXISTS view_string_table
    (
    sn INTEGER PRIMARY KEY,
    view_string VARCHAR(300)
    );
    '''
cursor.execute(sql_code)

sql_code = \
    '''
    CREATE TABLE IF NOT EXISTS view_sales_string
    (
    id INTEGER PRIMARY KEY,
    view_stringSales VARCHAR(500)
    );
    '''
cursor.execute(sql_code)

sql_code = \
    '''
    CREATE TABLE IF NOT EXISTS view_expenses_string
    (
    id INTEGER PRIMARY KEY,
    view_stringExpenses VARCHAR(1000)
    );
    '''
cursor.execute(sql_code)

cursor.execute('SELECT exists(SELECT 1 FROM view_string_table LIMIT 1);')
result = cursor.fetchone()
if not result[0]:
    default_products = \
        (
            (1, 'Andy Body Spray', '4dzn', '3,000 per dzn'),
            (2, 'Kylie Lipstick', '2dzn', '1,500 per dzn'),
            (3, 'Imam', '1grs', '4,000 per dzn'),
            (4, 'Green Tea Powder', '4pcs', '300 per pcs'),
            (5, 'Glory Facewipes', '3dzn', '2,000 per dzn'),
            (6, 'Masacara Eyeliner', '4dzn', '1,500 per dzn'),
            (7, 'I Powder', '4dzn', '6,000 per dzn'),
            (8, 'Lash Beautyblender', '6dzn', '400 per pcs'),
            (9, 'Computer', '1grs', '200,000 per pcs'),
            (10, 'Sports Car', '8pcs', '15,000,000 per pcs'),
            (11, 'Infinix Hot4 Phone', '2dzn', '35,000 per pcs'),
            (12, 'I-Phone 7', '2dzn', '250,000 per pcs')
        )
    info = ''
    for item in default_products:
        # temp_list = [item[1], item[3], item[2]]
        info += (' ' * 4 + '{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + ('\t' * 4) + (
            ' ' * 19) + '{2:<13s}\n' + (
                     '-' * 164) + '\n'). \
            format(item[1], item[2], item[3])
    cursor.execute('INSERT INTO view_string_table VALUES(?,?)', (None, info))
    cursor.executemany('INSERT INTO products VALUES(?, ?, ?, ?)', default_products)
    initializer.commit()
# else:
#     cursor.execute('SELECT * FROM view_string_table')
#     info = cursor.fetchone()[1]

initializer.close()


# def product_checker(product):
#     connection = sqlite3.connect('store.db')
#     cursor = connection.cursor()
#     sql_code = 'SELECT Name_Of_Product FROM products WHERE Name_Of_Product = ?'
#     cursor.execute(sql_code, (product,))
#     data = cursor.fetchone()
#     if data is None:
#         connection.close()
#         return False
#     connection.close()
#     return True

# def product_add(product_name, product_qty, product_price):
#     connection = sqlite3.connect('store.db')
#     cursor = connection.cursor()
#     temp_list = [(product_name, product_qty, product_price)]
#     for item in temp_list:
#         format_str = \
#         '''
#         INSERT INTO products(id number, Name Of Product, Quantity Of Product, Price Of Product)
#         VALUES (NULL, '{name}', '{quantity}', '{price}');
#         '''
#         sql_code = format_str.format(name=item[0], quantity=item[1], price=item[2])
#         cursor.execute(sql_code)
#     connection.commit()
#     connection.close()
#     return 0

# def product_remove(product):
#     connection = sqlite3.connect('store.db')
#     with connection:
#         cursor = connection.cursor()
#         cursor.execute('SELECT name_of_product FROM products WHERE name_of_product = ?', (product,))
#         data = cursor.fetchone()
#         if data is None:
#             tkinter.messagebox.showerror('Error', str(product) + ' not found in database')
#             return 1
#         sql_command = 'DELETE FROM products WHERE name_of_product=?'
#         cursor.execute(sql_command, (product,))
#         tkinter.messagebox.showinfo('deleted', str(product) + ' successfully removed')
#     connection.close()
#     return 0

# TODO: put in database the complete string and display once called
# TODO: put back button in change password and update frame
# TODO: how do I make the app make use of internet time rather than the computer's time
# TODO:
# def kill():
#     from sys import exit
#     exit()
#     return 0


def change():
    def back2menu():
        change_window.destroy()
        app.deiconify()
        return 0

    def password_checker():
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()
        cursor.execute('SELECT password1, password2 FROM company_credentials WHERE sn=?', (1,))
        password = cursor.fetchone()[0]
        print('old password: ', password)
        if password != old_password.get():
            if old_password.get() == '':
                tkinter.messagebox.showerror('Enter password', 'entry for old password blank')
            else:
                prompt = tkinter.messagebox.askretrycancel('Wrong password', 'password incorrect, try again')
                if prompt:
                    old_password.delete(0, tk.END)
                else:
                    change_window.destroy()
                    app.deiconify()
        elif new_password1.get() != new_password2.get():
            prompt = tkinter.messagebox.askretrycancel('password mismatch', 'verification of new password '
                                                                            'failed, try again')
            if prompt:
                new_password1.delete(0, tk.END)
                new_password2.delete(0, tk.END)
            else:
                change_window.destroy()
                app.deiconify()
        else:
            if new_password1.get() == '':
                tkinter.messagebox.showerror('Enter password', 'password entry blank')
            else:
                cursor = connection.cursor()
                sql_code = \
                    '''
                    UPDATE company_credentials
                    SET password1 = ?,
                    password2 = password1
                    WHERE sn = ?
                    '''
                cursor.execute(sql_code, (new_password1.get(), 1))
                connection.commit()
                tkinter.messagebox.showinfo('success', 'password successfully changed')
                change_window.destroy()
                app.deiconify()
        connection.close()
        return 0

    app.withdraw()
    change_window = tk.Toplevel(app)
    change_window.geometry('540x260+400+200')
    change_window.configure(background='#a1dbcd')
    change_window_icon = ImageTk.PhotoImage(file=os.path.join('c:\\users\\user\\pycharmprojects\\app_store',
                                                              'store.ico'))
    change_window.tk.call('wm', 'iconphoto', change_window._w, change_window_icon)
    change_window.resizable(0, 0)
    lab2 = tk.Label(change_window, width=15, text='Enter Old password:', bg='#a1dbcd')
    old_password = tk.Entry(change_window, show="\u2022", font='helvetica 8 bold')
    lab3 = tk.Label(change_window, width=15, text='Enter New password:', bg='#a1dbcd')
    new_password1 = tk.Entry(change_window, show='\u2022')
    lab4 = tk.Label(change_window, width=15, text='Verify New password:', bg='#a1dbcd')
    new_password2 = tk.Entry(change_window, show='\u2022')
    change_btn = tk.Button(change_window, text='save', cursor='hand2',
                           bg='black', fg='white', bd=3, command=password_checker, width=8, height=1)
    bk_image = Image.open('c:\\users\\user\\pycharmprojects\\app_store\\back_button1.jpg')
    bk_photo = ImageTk.PhotoImage(bk_image)
    back_button = tk.Button(change_window, cursor="hand2", image=bk_photo, command=back2menu, bd=4)
    back_button.image = bk_photo
    lab2.grid(row=4, pady=20, padx=20, column=2)
    old_password.grid(row=4, column=3, ipadx=125)
    lab3.grid(row=5, pady=15, padx=20, column=2)
    new_password1.grid(row=5, column=3, ipadx=125)
    lab4.grid(row=6, column=2, pady=15, padx=20)
    new_password2.grid(row=6, column=3, ipadx=125)
    change_btn.grid(columnspan=6, column=1, pady=30, sticky='w', padx=10)
    back_button.grid(row=7, columnspan=7, column=2, sticky='e')

    def change_password_handler(event):
        password_checker()

    change_btn.bind('<Return>', change_password_handler)

    def back_button_handler(event):
        back2menu()

    back_button.bind('<Return>', back_button_handler)
    return 0


def view():
    app.withdraw()
    view_window = tk.Toplevel(app, bg='dark turquoise')
    view_window.resizable(0, 0)
    view_window.geometry('400x250+400+200')
    view_window_icon = ImageTk.PhotoImage(file=os.path.join('c:\\users\\user\\pycharmprojects\\app_store',
                                                            'store.ico'))
    view_window.tk.call('wm', 'iconphoto', view_window._w, view_window_icon)

    def back2Menu():
        view_window.destroy()
        app.deiconify()
        return 0



    def view_store():
        def scrollbar_handler_up(event):
            text.yview(tk.SCROLL, -50, 'units')
            return 0

        def scrollbar_handler_down(event):
            text.yview(tk.SCROLL, 50, 'units')
            return 0

        def back():
            view_store_window.destroy()
            view_window.deiconify()
            return 0

        view_store_window = tk.Toplevel(app, bg='dark turquoise')
        view_store_window.resizable(0, 0)
        view_store_window.geometry('400x250+400+200')
        view_store_window_icon = ImageTk.PhotoImage(file=os.path.join('c:\\users\\user\\pycharmprojects\\app_store',
                                                                'store.ico'))
        view_store_window.tk.call('wm', 'iconphoto', view_store_window._w, view_store_window_icon)
        frame3 = tk.Frame(view_store_window, bg='dark turquoise')
        frame3.winfo_toplevel().geometry("1005x520+90+90")
        view_window.iconify()
        heading = '{0:<36s} {1:<30s} {2:>30s}'.format('Name Of Product\t\t',
                                                'Quantity Remaining', 'Price Of Product\t\t\t')
        lab = tk.Label(frame3, text=heading, bg='dark turquoise', font='helvetica 15 bold italic')
        writer_label = tk.Label(view_store_window, text=u'\N{copyright sign}' + ' an Andy Production',
                                font='purita 9 bold italic', bg='dark turquoise')
        btn1 = tk.Button(view_store_window, bg='dark turquoise', font='purita 9 bold italic', command=back,
                         cursor='hand2', text='Back', width=7)
        lab.pack(pady=10)
        text = tk.Text(frame3, bg='dark turquoise', width=500, height=20, font='helvetica 13', cursor='arrow')
        s = ttk.Style()
        s.configure('odk.Vertical.TScrollbar', width=30)
        scroller = ttk.Scrollbar(frame3, style='odk.Vertical.TScrollbar')
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM view_string_table')
        list_of_products = cursor.fetchone()
        info = list_of_products[1]
        text.insert(tk.END, info)
        text.config(state=tk.DISABLED)
        frame3.pack()
        scroller.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(side=tk.LEFT, fill=tk.Y)
        scroller.configure(command=text.yview)
        text.configure(yscrollcommand=scroller.set)
        app.bind('<Up>', scrollbar_handler_up)
        app.bind('<Down>', scrollbar_handler_down)
        btn1.pack(pady=5)
        writer_label.pack(side='right')
        return 0

    def view_product():
        def back():
            view_product_window.destroy()
            view_window.deiconify()
            return 0

        def product_viewer():
            product = ent1.get().title()
            connection = sqlite3.connect('store.db')
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM products WHERE Name_Of_Product=?', (ent1.get().title(),))
            single_product = cursor.fetchone()
            if single_product is not None:
                view_product_window.geometry('400x200+500+200')
                text = 'Name Of Product: ' + single_product[1] + '\n' + '\n ' + \
                       'Quantity Remaining: ' + single_product[2] + '\n' + '\n ' + \
                       'Price Of Product: ' + single_product[3]
                label = tk.Label(view_product_window, pady=20, text=text, font='purita 9 bold italic',
                                 bg='dark turquoise')
                frame1.grid_forget()
                frame.grid_forget()
                btn.grid_forget()
                label.grid()
                btn2 = tk.Button(view_product_window, text='Back', font='helvetica 10 bold italic',
                                 command=back, cursor='hand2', bg='dark turquoise', width=15)
                btn2.grid(column=0, columnspan=7, sticky='e')

                def menu_handler(event):
                    back()
                btn2.bind('<Return>', menu_handler)
            else:
                tkinter.messagebox.showerror('product not found', ent1.get().title() + ' not found in database')
                ent1.delete(0, tk.END)
            return 0
        view_window.iconify()
        view_product_window = tk.Toplevel(view_window, bg='dark turquoise')
        view_product_window.geometry('500x200+400+200')
        view_product_window_icon = ImageTk.PhotoImage(file=os.path.join('c:\\users\\user\\pycharmprojects\\app_store',
                                                                  'store.ico'))
        view_product_window.tk.call('wm', 'iconphoto', view_product_window._w, view_product_window_icon)
        view_product_window.resizable(0, 0)
        frame = tk.Frame(view_product_window, bg='dark turquoise')
        frame1 = tk.Frame(view_product_window, bg='dark turquoise')
        lab = tk.Label(frame, bg='dark turquoise', text='\tEnter name of product you want to view',
                       font='helvetica 12 bold italic')
        lab2 = tk.Label(frame1, width=15, text='Name of Product: ', bg='dark turquoise', padx=5,
                        font='helvetica 10 bold')
        ent1 = tk.Entry(frame1, font='helvetica 10 bold')
        btn = tk.Button(frame1, text='view product', command=product_viewer, bg='dark turquoise', bd=4,
                        cursor='hand2', font='helvetica 10 bold')
        bk_image = Image.open('c:\\users\\user\\pycharmprojects\\app_store\\back_button1.jpg')
        bk_photo = ImageTk.PhotoImage(bk_image)
        back_button = tk.Button(frame1, cursor="hand2", image=bk_photo, command=back2Menu, bd=4)
        back_button.image = bk_photo
        frame.grid(sticky='nsew', pady=10)
        frame1.grid(sticky='nsew', pady=20)
        lab.pack()
        lab2.grid(row=3, column=0, sticky='w')
        ent1.grid(row=3, column=1, sticky='w', ipadx=100)
        btn.grid(row=6, columnspan=1, pady=35)
        back_button.grid(columnspan=3, sticky='e', row=6)

        def product_viewer_handler(event):
            product_viewer()

        btn.bind('<Return>', product_viewer_handler)
        return 0

    lab1 = tk.Label(view_window, text='Select what you wish to view: ', bg='dark turquoise',
                    font='helvetica 13 bold')
    view_var = tk.IntVar()
    view_store_btn = tk.Button(view_window, text='View Store', cursor='hand2', bd=3,
                               command=view_store, font='purita 10 bold', bg='dark turquoise', width=8)
    view_product_btn = tk.Button(view_window, text='View a Product', bd=3, cursor='hand2', font='purita 10 bold',
                                 command=view_product, bg='dark turquoise', width=16)
    btn1 = tk.Button(view_window, text='Back', command=back2Menu, pady=5,
                     cursor='hand2', height=1, width=14, font='helvetica 9 bold italic',
                     bg='dark turquoise', borderwidth=3)
    lab1.pack(pady=10)
    view_store_btn.pack(padx=35, ipadx=30, pady=15)
    view_product_btn.pack(padx=15, ipadx=60, pady=15)
    btn1.pack(ipadx=90, pady=30)

    def view_store_btn_handler(event):
        view_store()
        return 0

    view_store_btn.bind('<Return>', view_store_btn_handler)

    def view_product_btn_handler(event):
        view_product()
        return 0

    view_product_btn.bind('<Return>', view_product_btn_handler)

    def btn1_handler(event):
        back2Menu()
        return 0

    btn1.bind('<Return>', btn1_handler)
    return 0


def update():
    app.wm_withdraw()
    update_window = tk.Toplevel(app, bg='dark turquoise')
    update_window.geometry('400x150+400+200')
    update_window.resizable(0, 0)
    update_window_icon = ImageTk.PhotoImage(file=os.path.join('c:\\users\\user\\pycharmprojects\\app_store',
                                                              'store.ico'))
    update_window.tk.call('wm', 'iconphoto', update_window._w, update_window_icon)

    def Back2Menu():
        update_window.destroy()
        app.wm_deiconify()
        return 0

    def enter_update():
        connection = sqlite3.connect('store.db', isolation_level=None)
        cursor = connection.cursor()
        cursor.execute('SELECT password1 FROM company_credentials WHERE sn=?', (1,))
        password = cursor.fetchone()[0]
        connection.close()
        # with shelve.open('Store Manager Credentials') as shelf:
        #     password = shelf['password'][0]
        if trans_password_entry.get() != password:
            prompt = tkinter.messagebox.askretrycancel('error', 'password incorrect, try again: ')
            if prompt:
                trans_password_entry.delete(0, 'end')
            else:
                Back2Menu()
        else:
            trans_password_entry.grid_forget()
            trans_password_btn.grid_forget()
            trans_password_lab.grid_forget()
            back_button.grid_forget()
            update_window.geometry('500x300+400+200')
            def product_adder():
                def product_adder_imp():
                    if name_ent_add.get() == '' or qty_ent2_add.get() == '' or qty_ent3_add.get() == '' or \
                                    qty_ent4_add.get() == '' or price_ent_add.get() == '':
                        tkinter.messagebox.showerror('Error', 'some entry are not filled')
                    elif not (qty_ent3_add.get()).isdecimal() or '-' in qty_ent3_add.get():
                        tkinter.messagebox.showerror('Error', 'this entry must be a positive numerical value')
                    elif not mv.money_checker(price_ent_add.get()):
                        tkinter.messagebox.showerror('Error', 'wrong format for money entry')
                        price_ent_add.delete(0, 'end')
                    elif (qty_ent2_add.get() != 'pcs' and (
                                    qty_ent2_add.get() != 'dzn' or qty_ent2_add.get() != 'grs')) \
                            and (qty_ent2_add.get() != 'dzn' and (
                                            qty_ent2_add.get() != 'pcs' or qty_ent2_add.get() != 'grs')) \
                            and (qty_ent2_add.get() != 'grs' and (
                                            qty_ent2_add.get() != 'pcs' or qty_ent2_add.get() != 'dzn')) \
                            or ((qty_ent4_add.get() != 'pcs' and (
                                            qty_ent4_add.get() != 'dzn' or qty_ent4_add.get() != 'grs'))
                                and (qty_ent4_add.get() != 'dzn' and (
                                                qty_ent4_add.get() != 'pcs' or qty_ent4_add.get() != 'grs'))
                                and (qty_ent4_add.get() != 'grs' and (
                                                qty_ent4_add.get() != 'pcs' or qty_ent4_add.get() != 'dzn'))):
                        tkinter.messagebox.showerror('Error', 'entry must either be pcs, grs, dzn')
                        if not (qty_ent2_add.get() == 'pcs' or qty_ent2_add.get() == 'grs' or
                                        qty_ent2_add.get() == 'dzn'):
                            qty_ent2_add.delete(0, 'end')
                        else:
                            qty_ent4_add.delete(0, 'end')
                    else:
                        connection = sqlite3.connect('store.db', isolation_level=None)
                        cursor = connection.cursor()
                        cursor.execute('SELECT Name_Of_Product FROM products WHERE Name_Of_Product=?',
                                       (name_ent_add.get().title(),))
                        data = cursor.fetchone()
                        if data is None:
                            cursor.execute('SELECT * FROM view_string_table')
                            info = cursor.fetchone()[1]
                            # print(info)
                            cursor.execute('DELETE FROM view_string_table')
                            temp_list = [
                                (name_ent_add.get().title(),
                                 '{0:,}'.format(
                                     int(mv.money_formatter(price_ent_add.get()))) + ' per ' + qty_ent2_add.get(),
                                 qty_ent3_add.get() + ' ' + qty_ent4_add.get())
                            ]
                            for item in temp_list:
                                format_str = \
                                    '''
                                    INSERT INTO products(id_number, Name_Of_Product, Quantity_Of_Product, 
                                    Price_Of_Product)
                                    VALUES (NULL, '{name}', '{price}', '{quantity}'); 
                                    '''
                                sql_code = format_str.format(name=item[0], quantity=item[1], price=item[2])
                                cursor.execute(sql_code)
                                sql_code = \
                                    '''
                                    INSERT INTO view_string_table(sn, view_string)
                                    VALUES (NULL, ?)
                                    '''
                                info += (
                                    ' ' * 4 + '{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + (
                                        '\t' * 4) + (
                                        ' ' * 19) + '{2:<13s}\n' + ('-' * 164) + '\n').format(
                                    item[0], item[2], item[1])
                                cursor.execute(sql_code, (info,))
                            # connection.commit()
                            prompt = tkinter.messagebox.askyesno('confirm', name_ent_add.get().title()
                                            + ' successfully added, wish to add another product: ')
                            if prompt:
                                name_ent_add.delete(0, 'end')
                                price_ent_add.delete(0, 'end')
                                qty_ent3_add.delete(0, 'end')
                            else:
                                product_adder_window.destroy()
                                update_window.deiconify()
                                # Back2Menu()
                        else:
                            prompt = tkinter.messagebox.askyesno('confirm', name_ent_add.get().title()
                                                + ' already in database\nwish to update it\'s stock')
                            if prompt:
                                product_adder_frame.destroy()
                                adder_btn.grid_forget()
                                product_stock_updater()
                            else:
                                product_adder_frame.destroy()
                                Back2Menu()

                        connection.close()
                    return 0
                update_window.iconify()
                product_adder_window = tk.Toplevel(app, bg='dark turquoise')
                product_adder_window.geometry('500x300+400+200')
                product_adder_window.resizable(0, 0)
                product_adder_window_icon = ImageTk.PhotoImage(
                    file=os.path.join('c:\\users\\user\\pycharmprojects\\app_store',
                                      'store.ico'))
                product_adder_window.tk.call('wm', 'iconphoto', product_adder_window._w, product_adder_window_icon)
                product_adder_frame = tk.Frame(product_adder_window, bg='dark turquoise')
                product_adder_frame.winfo_toplevel().geometry("530x200-220+220")
                product_adder_frame.grid()
                name_lab_add = tk.Label(product_adder_frame, bg='dark turquoise', font='purita 11 bold',
                                        text='Name of product: ', width=15)
                name_ent_add = tk.Entry(product_adder_frame, font='helvetica 10 bold')
                qty_lab_add = tk.Label(product_adder_frame, font='purita 11 bold', text='Price of product: ',
                                       bg='dark turquoise', width=15)
                price_ent_add = tk.Entry(product_adder_frame, font='helvetica 10 bold')
                per_lab = tk.Label(product_adder_frame, bg='dark turquoise', text='per', font='purita 11 bold')
                qty_ent2_add = tk.Spinbox(product_adder_frame, values=('pcs', 'grs', 'dzn'), wrap=True,
                                          font='helvetica 10 bold', width=5, justify='center')
                qty_lab3 = tk.Label(product_adder_frame, bg='dark turquoise', font='purita 11 bold',
                                    text='Quantity of product: ', width=15)
                qty_ent3_add = tk.Entry(product_adder_frame, font='helvetica 10 bold')
                qty_ent4_add = tk.Spinbox(product_adder_frame, values=('pcs', 'grs', 'dzn'), wrap=True,
                                          font='helvetica 10 bold', width=5, justify='center')
                name_lab_add.grid(column=0, row=0, pady=10, sticky='w')
                name_ent_add.grid(column=1, row=0, ipadx=110)
                qty_lab_add.grid(column=0, row=1, padx=5, pady=10)
                price_ent_add.grid(column=1, row=1, ipadx=10, sticky='w')
                per_lab.grid(row=1, column=1, sticky='w', padx=126)
                qty_ent2_add.grid(row=1, column=1, sticky='w', padx=154)
                qty_lab3.grid(column=0, row=2, pady=10, padx=5)
                qty_ent3_add.grid(column=1, row=2, ipadx=30, sticky='w')
                qty_ent4_add.grid(column=1, row=2)
                adder_btn = tk.Button(product_adder_window, text='Add Product', font='helvetica 10 bold italic',
                                      command=product_adder_imp, width=15, bg='dark turquoise', cursor='hand2',
                                      bd=4)
                adder_btn.grid(ipadx=7, row=4, pady=25)

                def adder_btn_handler(event):
                    product_adder_imp()
                    return 0

                adder_btn.bind('<Return>', adder_btn_handler)
                return 0

            def product_stock_updater():
                def product_stock_updater_imp():
                    if name_ent_update_stock.get() == '' or update_qty_ent2.get() == '' or update_qty_ent1.get(

                    ) == '':
                        tkinter.messagebox.showerror('Error', 'some entry are not filled')
                    elif not (update_qty_ent1.get()).isdecimal() or '-' in update_qty_ent1.get():
                        tkinter.messagebox.showerror('Error', 'Quantity of product must be a positive numerical '
                                                              'value')
                    elif (update_qty_ent2.get() != 'pcs' and (
                                    update_qty_ent2.get() != 'dzn' or update_qty_ent2.get() != 'grs')) \
                            and (update_qty_ent2.get() != 'dzn' and (update_qty_ent2.get() != 'pcs' or
                                                                             update_qty_ent2.get() != 'grs')) \
                            and (update_qty_ent2.get() != 'grs' and (update_qty_ent2.get() != 'pcs' or
                                                                             update_qty_ent2.get() != 'dzn')) \
                            or ((update_qty_ent2.get() != 'pcs' and (update_qty_ent2.get() != 'dzn' or
                                                                             update_qty_ent2.get() != 'grs'))
                                and (update_qty_ent2.get() != 'dzn' and (update_qty_ent2.get() != 'pcs' or
                                                                                 update_qty_ent2.get() != 'grs'))
                                and (update_qty_ent2.get() != 'grs' and (update_qty_ent2.get() != 'pcs' or
                                                                                 update_qty_ent2.get() !=
                                                                                 'dzn'))):
                        tkinter.messagebox.showerror('Error', 'quantity must either be pcs, grs or dzn')
                        if not (update_qty_ent2.get() == 'pcs' or update_qty_ent2.get() == 'grs' or
                                        update_qty_ent2.get() == 'dzn'):
                            update_qty_ent2.delete(0, 'end')
                        else:
                            update_qty_ent1.delete(0, 'end')
                    # elif not product_checker(name_ent_update_stock.get().title()):
                    else:
                        connection = sqlite3.connect('store.db', isolation_level=None)
                        cursor = connection.cursor()
                        cursor.execute('SELECT Name_Of_Product FROM products WHERE Name_Of_Product=?',
                                       (name_ent_update_stock.get().title(),))
                        data = cursor.fetchone()
                        if data is not None:
                            cursor.execute('SELECT Quantity_Of_Product FROM products WHERE Name_Of_Product=?',
                                           (name_ent_update_stock.get().title(),))
                            data = cursor.fetchone()
                            cursor.execute('SELECT Price_Of_Product FROM products WHERE Name_Of_Product=?',
                                           (name_ent_update_stock.get().title(),))
                            cursor.execute('SELECT Price_Of_Product FROM products WHERE Name_Of_Product=?',
                                           (name_ent_update_stock.get().title(),))
                            temp_price_of_product = cursor.fetchone()[0]
                            # print(temp_price_of_product)
                            total_qty = update_qty_ent1.get() + update_qty_ent2.get()
                            new_qty = qc.qty_converter(data[0]) + qc.qty_converter(total_qty)
                            cursor = connection.cursor()
                            cursor.execute('SELECT * FROM view_string_table')
                            info = cursor.fetchone()[1]
                            if new_qty >= 144:
                                new_qty1 = new_qty // 144
                                new_qty3 = new_qty % 144
                                if new_qty >= 12:
                                    new_qty = new_qty3 // 12
                                    new_qty2 = new_qty3 % 12
                                    temp_list = (str(new_qty1) + 'grs' + ' + ' +
                                                 str(new_qty) + 'dzn' + ' + ' + str(new_qty2) + 'pcs').split('+')
                                    if temp_list[2].replace(' ', '') == '0pcs' and temp_list[1].replace(' ',
                                                                                                        '') == \
                                            '0dzn':
                                        new_str = str(new_qty1) + ' grs'
                                    elif temp_list[2].replace(' ', '') != '0pcs' and temp_list[1].replace(' ',
                                                                                                          '') \
                                            == '0dzn':
                                        new_str = str(new_qty1) + ' grs' + '+' + temp_list[2].replace(' ', '')
                                    elif temp_list[2].replace(' ', '') == '0pcs' and temp_list[1].replace(' ',
                                                                                                          '') \
                                            != '0dzn':
                                        new_str = str(new_qty1) + 'grs' + '+' + temp_list[1].replace(' ', '')
                                    else:
                                        new_str = str(new_qty1) + 'grs' + '+' + str(new_qty) + 'dzn' + '+' + str(
                                            new_qty2) + 'pcs'
                                else:
                                    new_str = str(new_qty1) + '+' + str(new_qty)
                                # with connection:
                                sql_command = \
                                    '''
                                    UPDATE products
                                    SET Quantity_Of_Product = ?
                                    WHERE Name_Of_Product = ?
                                    '''
                                cursor.execute(sql_command, (new_str, name_ent_update_stock.get().title()))
                                # connection.commit()
                                old_string = ''
                                # old_string = ('{0:<30s}    \t\t\t\t\t                 {1:<10s}\t\t\t\t
                                #             ' \
                                #              '{2:<13s}\n'+'-'*164+'\n').\
                                #     format(name_ent_update_stock.get().title(), new_str, temp_price_of_product)
                                old_string += \
                                    (
                                        ' '*4+'{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + (
                                            '\t' * 4) + (
                                            ' ' * 19) + '{2:<13s}'). \
                                        format(name_ent_update_stock.get().title(), data[0],
                                               temp_price_of_product)
                                new_string = \
                                    (
                                        ' '*4+'{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + (
                                            '\t' * 4) + (
                                            ' ' * 19) + '{2:<13s}'). \
                                        format(name_ent_update_stock.get().title(), new_str,
                                               temp_price_of_product)
                                cursor.execute('DELETE FROM view_string_table')
                                info = info.replace(old_string, new_string)
                                sql_code = 'INSERT INTO view_string_table(sn, view_string)' \
                                           'VALUES (NULL, ?)'
                                cursor.execute(sql_code, (info,))
                                prompt = tkinter.messagebox.askyesno('Confirm',
                                                                     'stock of ' + name_ent_update_stock.get(

                                                                     ).title() + ' successfully updated, '
                                                                                 'wish to update stock of '
                                                                                 'another product?')
                                if prompt:
                                    name_ent_update_stock.delete(0, 'end')
                                    update_qty_ent1.delete(0, 'end')
                                else:
                                    product_stock_updater_window.destroy()
                                    Back2Menu()
                            elif new_qty >= 12:
                                new_qty1 = new_qty // 12
                                new_qty = new_qty % 12
                                temp_list = (str(new_qty1) + 'dzn' + ' + ' + str(new_qty) + 'pcs').split('+')
                                if temp_list[1].replace(' ', '') == '0pcs':
                                    new_str = str(new_qty1) + 'dzn'
                                else:
                                    new_str = str(new_qty1) + 'dzn' + '+' + str(new_qty) + 'pcs'
                                sql_command = \
                                    '''
                                    UPDATE products
                                    SET Quantity_Of_Product = ?
                                    WHERE Name_Of_Product = ?
                                    '''
                                cursor.execute(sql_command, (new_str, name_ent_update_stock.get().title()))
                                old_string = ''
                                old_string += \
                                    (
                                        ' '*4+'{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + (
                                            '\t' * 4) + (
                                            ' ' * 19) + '{2:<13s}'). \
                                        format(name_ent_update_stock.get().title(), data[0],
                                               temp_price_of_product)
                                new_string = \
                                    (
                                        ' '*4+'{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + (
                                            '\t' * 4) + (
                                            ' ' * 19) + '{2:<13s}'). \
                                        format(name_ent_update_stock.get().title(), new_str,
                                               temp_price_of_product)
                                cursor.execute('DELETE FROM view_string_table')
                                info = info.replace(old_string, new_string)
                                sql_code = 'INSERT INTO view_string_table(sn, view_string)' \
                                           'VALUES (NULL, ?)'
                                cursor.execute(sql_code, (info,))
                                prompt = tkinter.messagebox.askyesno('Confirm',
                                                                     'stock of ' + name_ent_update_stock.get(

                                                                     ).title() + ' successfully updated, '
                                                                                 'wish to update stock of '
                                                                                 'another '
                                                                                 'product?')
                                if prompt:
                                    name_ent_update_stock.delete(0, 'end')
                                    update_qty_ent1.delete(0, 'end')
                                else:
                                    product_stock_updater_window.destroy()
                                    Back2Menu()
                            else:
                                new_str = str(new_qty) + 'pcs'
                                sql_command = \
                                    '''
                                    UPDATE products
                                    SET Quantity_Of_Product = ?
                                    WHERE Name_Of_Product = ?
                                    '''
                                cursor.execute(sql_command, (new_str, name_ent_update_stock.get().title()))
                                old_string = \
                                    (' '*4+'{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + (
                                    '\t' * 4) + (' ' * 19) + '{2:<13s}'). \
                                        format(name_ent_update_stock.get().title(), data[0],
                                               temp_price_of_product)
                                new_string = \
                                    (' '*4+'{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + (
                                    '\t' * 4) + (' ' * 19) + '{2:<13s}'). \
                                        format(name_ent_update_stock.get().title(), new_str,
                                               temp_price_of_product)
                                cursor.execute('DELETE FROM view_string_table')
                                info = info.replace(old_string, new_string)
                                sql_code = 'INSERT INTO view_string_table(sn, view_string)' \
                                           'VALUES (NULL, ?)'
                                cursor.execute(sql_code, (info,))
                                prompt = tkinter.messagebox.askyesno('Confirm', 'stock of ' +
                                name_ent_update_stock.get().title() +' successfully changed\nwish to change '
                                'stock of another product?')
                                if prompt:
                                    name_ent_update_stock.delete(0, 'end')
                                    update_qty_ent1.delete(0, 'end')
                                else:
                                    product_stock_updater_window.destroy()
                                    update_window.deiconify()
                        else:
                            prompt = tkinter.messagebox.askyesno('Confirm', name_ent_update_stock.get().title() +
                                                                 ' not found in database, wish to add it?')
                            if prompt:
                                product_stock_updater_window.destroy()
                                product_adder()
                            else:
                                product_stock_updater_window.destroy()
                                update_window.deiconify()
                        connection.close()
                        return 0

                update_window.iconify()
                product_stock_updater_window = tk.Toplevel(update_window, bg='dark turquoise')
                product_stock_updater_window.geometry('500x300+400+200')
                product_stock_updater_window.resizable(0, 0)
                product_stock_updater_window_icon = ImageTk.PhotoImage(
                    file=os.path.join('c:\\users\\user\\pycharmprojects\\app_store',
                                      'store.ico'))
                product_stock_updater_window.tk.call('wm', 'iconphoto', product_stock_updater_window._w,
                                                     product_stock_updater_window_icon)
                product_stock_updater_frame = tk.Frame(product_stock_updater_window, bg='dark turquoise')
                product_stock_updater_frame.winfo_toplevel().geometry("530x200-220+220")
                product_stock_updater_frame.grid()
                update_lab_ent = tk.Label(product_stock_updater_frame, bg='dark turquoise', width=15,
                                          text='Name of product: ', font='purita 11 bold')
                name_ent_update_stock = tk.Entry(product_stock_updater_frame, font='helvetica 10 bold')
                update_qty_lab = tk.Label(product_stock_updater_frame, bg='dark turquoise', width=15,
                                          text='Quantity of product: ', font='purita 11 bold')
                update_qty_ent1 = tk.Entry(product_stock_updater_frame, font='helvetica 10 bold')
                update_qty_ent2 = tk.Spinbox(product_stock_updater_frame, font='helvetica 10 bold', wrap=True,
                                             values=('dzn', 'pcs', 'grs'), width=5, justify='center')
                update_stock_btn = tk.Button(product_stock_updater_frame, font='helvetica 10 bold italic',
                                             bg='dark turquoise',
                                             command=product_stock_updater_imp, bd=4, cursor='hand2',
                                             text='Update '
                                                  'stock',
                                             width=15)
                update_lab_ent.grid(row=0, column=0, pady=15, sticky='w')
                name_ent_update_stock.grid(row=0, column=1, ipadx=110, sticky='w')
                update_qty_lab.grid(row=1, column=0, pady=15, padx=10, sticky='w')
                update_qty_ent1.grid(row=1, column=1, ipadx=30, sticky='w')
                update_qty_ent2.grid(row=1, column=1)
                update_stock_btn.grid(ipadx=7, row=4, pady=25, columnspan=500)

                def update_stock_btn_handler(event):
                    product_stock_updater_imp()
                    return 0

                update_stock_btn.bind('<Return>', update_stock_btn_handler)
                return 0

            def product_deleter():
                def product_deleter_imp():
                    if name_ent1_del.get() == '' or name_ent1_del.get().isspace():
                        tkinter.messagebox.showerror('Blank Entry', 'Name of product entry blank')
                    else:
                        connection = sqlite3.connect('store.db', isolation_level=None)
                        cursor = connection.cursor()
                        cursor.execute('SELECT Name_Of_Product FROM products WHERE Name_Of_Product = ?',
                                       (name_ent1_del.get().title(),))
                        data = cursor.fetchone()
                        if data is None:
                            tkinter.messagebox.showerror('Not Found', name_ent1_del.get().title() +
                                                         ' not found in database')
                            name_ent1_del.delete(0, tk.END)
                        else:
                            cursor.execute('SELECT Quantity_Of_Product FROM products WHERE Name_Of_Product=?',
                                           (name_ent1_del.get().title(),))
                            quantity_data = cursor.fetchone()[0]
                            cursor.execute('SELECT * FROM view_string_table')
                            info = cursor.fetchone()[1]
                            cursor.execute('SELECT Price_Of_Product FROM products WHERE Name_Of_Product=?',
                                           (name_ent1_del.get().title(),))
                            temp_price_of_product = cursor.fetchone()[0]
                            sql_command = 'DELETE FROM products WHERE Name_Of_Product=?'
                            cursor.execute(sql_command, (name_ent1_del.get().title(),))
                            old_string = \
                                (
                                    ' '*4+'{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + ('\t' * 4)
                                     + (
                                        ' ' * 19) + '{2:<13s}\n' + ('-' * 164) + '\n'). \
                                    format(name_ent1_del.get().title(), quantity_data,
                                           temp_price_of_product)
                            new_string = ''
                            cursor.execute('DELETE FROM view_string_table')
                            info = info.replace(old_string, new_string)
                            # os.system('cls')
                            sql_code = 'INSERT INTO view_string_table(sn, view_string)' \
                                       'VALUES (NULL, ?)'
                            cursor.execute(sql_code, (info,))
                            # connection.commit()
                            prompt = tkinter.messagebox.askyesno('Confirm', name_ent1_del.get(
                            ).title() + ' successfully '
                                        'deleted.\nwish to delete another product?')
                            if prompt:
                                name_ent1_del.delete(0, 'end')
                            else:
                                product_deleter_window.destroy()
                                update_window.deiconify()
                        connection.close()
                    return 0

                update_window.iconify()
                product_deleter_window = tk.Toplevel(app, bg='dark turquoise')
                product_deleter_window.geometry('500x300+400+200')
                product_deleter_window.resizable(0, 0)
                product_deleter_window_icon = ImageTk.PhotoImage(
                    file=os.path.join('c:\\users\\user\\pycharmprojects\\app_store',
                                      'store.ico'))
                product_deleter_window.tk.call('wm', 'iconphoto', product_deleter_window._w, product_deleter_window_icon)
                product_deleter_frame = tk.Frame(product_deleter_window, bg='dark turquoise')
                product_deleter_frame.winfo_toplevel().geometry("450x150-220+220")
                product_deleter_frame.grid()
                name_lab_del = tk.Label(product_deleter_frame, bg='dark turquoise', width=15,
                                        text='Name of product: ',
                                        font='purita 11 bold')
                name_ent1_del = tk.Entry(product_deleter_frame, font='helvetica 10 bold')
                del_btn = tk.Button(product_deleter_frame, font='helvetica 10 bold italic', bg='dark turquoise',
                                    command=product_deleter_imp, bd=4, cursor='hand2', text='Remove product',
                                    width=15)
                name_lab_del.grid(row=0, column=0, pady=15)
                name_ent1_del.grid(row=0, column=1, ipadx=60)
                del_btn.grid(row=4, ipadx=7, pady=30, column=1, columnspan=1, sticky='w', padx=20)

                def del_btn_handler(event):
                    product_deleter_imp()

                del_btn.bind('<Return>', del_btn_handler)
                return 0

            def price_changer():
                def price_changer_imp():
                    # shelf = shelve.open('Store')
                    if (name_pc_ent2.get() != 'pcs' and (
                                    name_pc_ent2.get() != 'dzn' or name_pc_ent2.get() != 'grs')) \
                            and (name_pc_ent2.get() != 'dzn' and (
                                            name_pc_ent2.get() != 'pcs' or name_pc_ent2.get() != 'grs')) \
                            and (name_pc_ent2.get() != 'grs' and (
                                            name_pc_ent2.get() != 'pcs' or name_pc_ent2.get() != 'dzn')):
                        tkinter.messagebox.showerror('Error', 'entry must either be pcs, grs or dzn')
                        name_pc_ent2.delete(0, 'end')
                    elif not mv.money_checker(name_pc_ent3.get()):
                        tkinter.messagebox.showerror('Error', 'wrong format for money entry')
                        name_pc_ent3.delete(0, 'end')
                    else:
                        connection = sqlite3.connect('store.db', isolation_level=None)
                        cursor = connection.cursor()
                        cursor.execute('SELECT Quantity_Of_Product FROM products WHERE Name_Of_Product=?',
                                       (name_pc_ent1.get().title(),))
                        qty_data = cursor.fetchone()
                        if qty_data is None:
                            tkinter.messagebox.showerror('product not found', name_pc_ent1.get().title()
                                                         +' not found in database')
                            name_pc_ent1.delete('end')
                        else:
                            qty_data = qty_data[0]
                            cursor.execute('SELECT Price_Of_Product FROM products WHERE Name_Of_Product=?',
                                           (name_pc_ent1.get().title(),))
                            cursor.execute('SELECT Price_Of_Product FROM products WHERE Name_Of_Product=?',
                                           (name_pc_ent1.get().title(),))
                            temp_price_of_product = cursor.fetchone()[0]
                            # print(temp_price_of_product)
                            new_price = '{0:,}'.format(int(mv.money_formatter(name_pc_ent3.get()))) + ' per ' + \
                                        name_pc_ent2.get()
                            # new_qty = qc.qty_converter(data[0]) + qc.qty_converter(total_qty)
                            # cursor = connection.cursor()
                            cursor.execute('SELECT * FROM view_string_table')
                            info = cursor.fetchone()[1]
                            # new_str =
                            sql_command = \
                                '''
                                UPDATE products
                                SET Price_Of_Product = ?
                                WHERE Name_Of_Product = ?
                                '''
                            cursor.execute(sql_command, (new_price, name_pc_ent1.get().title()))
                            old_string = \
                                (' '*4+'{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + ('\t' * 4) + (
                                    ' ' * 19) + '{2:<13s}'). \
                                    format(name_pc_ent1.get().title(), qty_data, temp_price_of_product)
                            new_string = \
                                (' '*4+'{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + ('\t' * 4) + (
                                    ' ' * 19) + '{2:<13s}'). \
                                    format(name_pc_ent1.get().title(), qty_data, new_price)
                            cursor.execute('DELETE FROM view_string_table')
                            # print(old_string in info)
                            info = info.replace(old_string, new_string)
                            sql_code = 'INSERT INTO view_string_table(sn, view_string)' \
                                       'VALUES (NULL, ?)'
                            cursor.execute(sql_code, (info,))
                            connection.close()
                            prompt = tkinter.messagebox.askyesno('Confirm',
                                                                 name_pc_ent1.get().title() + '\'s price '
                                                                                              'successfully '
                                                                                              'changed\nwould you '
                                                                                              'like to change price'
                                                                                              ' of another product ')
                            if prompt:
                                name_pc_ent1.delete(0, 'end')
                                name_pc_ent3.delete(0, 'end')
                            else:
                                price_changer_window.destroy()
                                update_window.deiconify()
                    return 0

                update_window.iconify()
                price_changer_window = tk.Toplevel(app, bg='black')
                price_changer_window.geometry('500x300+400+200')
                price_changer_window.resizable(0, 0)
                price_changer_window_icon = ImageTk.PhotoImage(
                    file=os.path.join('c:\\users\\user\\pycharmprojects\\app_store',
                                      'store.ico'))
                price_changer_window.tk.call('wm', 'iconphoto', price_changer_window._w, price_changer_window_icon)
                price_changer_frame = tk.Frame(price_changer_window, bg='dark turquoise')
                price_changer_frame.winfo_toplevel().geometry("450x200-450+220")
                price_changer_frame.grid()
                name_lab_pc = tk.Label(price_changer_frame, bg='dark turquoise', width=15,
                                       text='Name of product: ',
                                       font='purita 11 bold')
                name_lab_pc1 = tk.Label(price_changer_frame, bg='dark turquoise', text='per',
                                        font='purita 11 bold')
                name_pc_ent1 = tk.Entry(price_changer_frame, font='helvetica 10 bold')
                qty_lab_pc = tk.Label(price_changer_frame, bg='dark turquoise', width=15,
                                      text='Price Of Product: ',
                                      font='purita 11 bold')
                name_pc_ent3 = tk.Entry(price_changer_frame, font='helvetica 10 bold')
                name_pc_ent2 = tk.Spinbox(price_changer_frame, font='helvetica 10 bold',
                                          values=('pcs', 'dzn', 'grs'),
                                          wrap=True, justify='center', width=5)
                pc_btn = tk.Button(price_changer_frame, font='helvetica 10 bold italic', bg='dark turquoise',
                                   command=price_changer_imp, bd=4, cursor='hand2', text='Change product price',
                                   width=15)
                name_lab_pc.grid(row=0, column=0, pady=15, sticky='w')
                name_pc_ent1.grid(row=0, column=1, ipadx=70, sticky='w')
                qty_lab_pc.grid(row=1, column=0, pady=15, sticky='w')

                name_pc_ent3.grid(row=1, column=1, ipadx=5, sticky='w')
                name_lab_pc1.grid(row=1, column=1, sticky='w', padx=155)  # per
                name_pc_ent2.grid(row=1, column=1, sticky='w', padx=190)  # dzn, pcs, grs
                pc_btn.grid(row=4, ipadx=7, pady=30, column=1, columnspan=1, sticky='w', padx=20)

                def pc_btn_handler(event):
                    price_changer_imp()

                pc_btn.bind('<Return>', pc_btn_handler)
                return 0

            trans_label = tk.Label(update_window, bg='dark turquoise', font='helvetica 12 bold italic',
                                   text='I would like to update my store by: ')
            trans_btn1 = tk.Button(update_window, bg='dark turquoise', font='helvetica 11 bold', cursor='hand2',
                                   command=product_adder, text='Adding a product')
            trans_btn2 = tk.Button(update_window, bg='dark turquoise', font='helvetica 11 bold', cursor='hand2',
                                   text='Removing a product', command=product_deleter)
            trans_btn3 = tk.Button(update_window, bg='dark turquoise', font='helvetica 11 bold', cursor='hand2',
                                   text='Changing a product\'s price', command=price_changer)
            trans_btn4 = tk.Button(update_window, bg='dark turquoise', font='helvetica 11 bold', cursor='hand2',
                                   text='Updating stock of a product', command=product_stock_updater)
            trans_back = tk.Button(update_window, bg='dark turquoise', font='helvetica 11 bold', cursor='hand2',
                                   text='Back to Menu', command=Back2Menu)
            trans_label.grid(padx=100)
            trans_btn1.grid(pady=10, ipadx=5)
            trans_btn2.grid(pady=10, ipadx=10)
            trans_btn3.grid(pady=10, ipadx=15)
            trans_btn4.grid(pady=10, ipadx=35)
            trans_back.grid(pady=15, ipadx=100)

            def trans_btn1_handler(event):
                product_adder()
                return 0

            trans_btn1.bind('<Return>', trans_btn1_handler)

            def trans_btn2_handler(event):
                product_deleter()
                return 0

            trans_btn2.bind('<Return>', trans_btn2_handler)

            def trans_btn3_handler(event):
                price_changer()
                return 0

            trans_btn3.bind('<Return>', trans_btn3_handler)

            def trans_btn4_handler(event):
                product_stock_updater()
                return 0

            trans_btn4.bind('<Return>', trans_btn4_handler)

            def trans_back_handler(event):
                Back2Menu()
                return 0

            trans_back.bind('<Return>', trans_back_handler)
        connection.close()

    def back2menu():
        update_window.destroy()
        app.deiconify()

    trans_password_lab = tk.Label(update_window, bg='dark turquoise', font='helvetica 10 bold italic',
                                  text='Enter Password: ', width=15)
    trans_password_entry = tk.Entry(update_window, show="\u2022", font='helvetica 9 bold')
    trans_password_lab.grid(row=0, pady=10, column=0)
    trans_password_btn = tk.Button(update_window, text='update store', font='purita 10 bold italic',
                                   bg='dark turquoise', cursor='hand2', command=enter_update)
    bk_image = Image.open('c:\\users\\user\\pycharmprojects\\app_store\\back_button1.jpg')
    bk_photo = ImageTk.PhotoImage(bk_image)
    back_button = tk.Button(update_window, cursor="hand2", image=bk_photo, command=back2menu, bd=4)
    back_button.image = bk_photo
    trans_password_entry.grid(row=0, column=1, ipadx=60)
    trans_password_btn.grid(padx=20, row=3, column=0, columnspan=1, pady=50, sticky='w')
    back_button.grid(row=3, columnspan=4, sticky='e')

    def trans_password_btn_handler(event):
        enter_update()
        return 0
    trans_password_btn.bind('<Return>', trans_password_btn_handler)


    def trans_back_handler(event):
        back2menu()
        return 0
    back_button.bind('<Return>', back2menu)
    return 0

def help_btn():
    app.wm_withdraw()
    help_window = tk.Toplevel(app, bg='dark turquoise')
    help_window.wm_resizable(0, 0)
    help_window.geometry('700x450+400+200')
    help_window_icon = ImageTk.PhotoImage(file=os.path.join('c:\\users\\user\\pycharmprojects\\app_store',
                                                            'store.ico'))
    help_window.tk.call('wm', 'iconphoto', help_window._w, help_window_icon)

    def back2Menu():
        help_window.destroy()
        app.deiconify()
        return 0

    def change_password_help():
        pass

    def view_store_help():
        pass

    def update_help():
        pass

    def transaction_help():
        pass

    info = '''
            The Store Manager App is a desktop app developed and written by Okoye, Andrew that manages 
            your day-to-day transactions including your sales and expenses. The software prompts you to 
            initialize your password when the software is opened for the first time. The password you 
            initialized will be same password you have to type in when you wish to update your store. Click on 
            any button below for more on that feature. 
            '''

    lab1 = tk.Message(help_window, text=info, font='helvetica 10 bold', bg='dark turquoise', justify='left',
                      width=950)
    btn1 = tk.Button(help_window, text='Changing Password', command=change_password_help, cursor='hand2',
                     font='purita 10 bold italic', bg='dark turquoise', width=16)
    btn2 = tk.Button(help_window, text='Viewing Store', command=view_store_help, cursor='hand2',
                     font='purita 10 bold italic', bg='dark turquoise', width=20)
    btn3 = tk.Button(help_window, text='Updating Store', command=update_help, cursor='hand2',
                     font='purita 10 bold italic', bg='dark turquoise', width=25)

    btn4 = tk.Button(help_window, text='Recording/Viewing Transactions', command=transaction_help, cursor='hand2',
                     font='purita 10 bold italic', bg='dark turquoise', width=30)
    btn5 = tk.Button(help_window, text='Back to Main Menu', command=back2Menu, cursor='hand2',
                     font='purita 10 bold italic', bg='dark turquoise', width=35)
    lab1.pack(pady=10, padx=5)
    btn1.pack(pady=12)
    btn2.pack(pady=12)
    btn3.pack(pady=12)
    btn4.pack(pady=12)
    btn5.pack(pady=12)


def transactions():
    app.wm_withdraw()
    transaction_window = tk.Toplevel(app, bg='dark turquoise')
    transaction_window.resizable(0, 0)
    # transaction_frame = tk.Frame(transaction_window, bg='dark turquoise')
    transaction_window.geometry('350x250+400+200')
    transaction_window_icon = ImageTk.PhotoImage(file=os.path.join('c:\\users\\user\\pycharmprojects\\app_store',
                                                                   'store.ico'))
    transaction_window.tk.call('wm', 'iconphoto', transaction_window._w, transaction_window_icon)

    def back2Menu():
        transaction_window.destroy()
        app.wm_deiconify()
        return 0

    def sales():
        def sales_recorder():
            connection = sqlite3.connect('store.db', isolation_level=None)
            # with connection:
            cursor = connection.cursor()
            cursor.execute('SELECT Name_Of_Product from products WHERE Name_Of_Product = ?',
                           (name_ent.get().title(),))
            product_name_data = cursor.fetchone()
            cursor.execute('SELECT Quantity_Of_Product from products WHERE Name_Of_Product = ?',
                           (name_ent.get().title(),))
            quantity_data = cursor.fetchone()
            cursor.execute('SELECT Price_Of_Product from products WHERE Name_Of_Product = ?',
                           (name_ent.get().title(),))
            price_data = cursor.fetchone()
            if name_ent.get().title() == '':
                tkinter.messagebox.showerror('Error', 'Entry for name of product is blank')
            elif product_name_data is None:
                tkinter.messagebox.showerror('Product not found',
                                             name_ent.get().title() + ' not found in database')
                name_ent.delete(0, tk.END)
            elif not qty_ent.get().isdecimal():
                if qty_ent.get() == '':
                    tkinter.messagebox.showerror('Error', 'Entry for quantity sold out is blank')
                else:
                    tkinter.messagebox.showerror('Invalid input', 'expected only numerical values in quantity '
                                                                  'sold out entry')
                    qty_ent.delete(0, tk.END)
            elif (qty_ent2.get() != 'pcs' and (qty_ent2.get() != 'dzn' or qty_ent2.get() != 'grs')) \
                    and (qty_ent2.get() != 'dzn' and (qty_ent2.get() != 'pcs' or qty_ent2.get() !=
                        'grs')) and (qty_ent2.get() != 'grs'
                                     and (qty_ent2.get() != 'pcs' or qty_ent2.get() != 'dzn')):
                tkinter.messagebox.showerror('Error',
                                             'pcs, grs and dzn are the only values allowed in this entry')
                qty_ent2.delete(0, 'end')
            elif qc.qty_converter(qty_ent.get() + qty_ent2.get()) > qc.qty_converter(quantity_data[0]):
                tkinter.messagebox.showerror('Error', 'Quantity sold out cannot be more than Quantity in store')
            else:
                qty_sold = qty_ent.get() + qty_ent2.get()
                price = qc.per_product(price_data[0])
                dt = datetime.datetime.now()
                sales_time = datetime.datetime(dt.year, dt.month, dt.day)
                sales_time = sales_time.strftime('%d-%b-%y')
                # insert_code = '''INSERT INTO sales VALUES(NULL,?,?,?,?)'''
                # cursor.execute(insert_code, (
                # sales_time, name_ent.get().title(), qty_sold, int(qc.qty_converter(qty_sold) * price)))
                new_qty = qc.qty_converter(quantity_data[0]) - qc.qty_converter(qty_ent.get() + qty_ent2.get())
                cursor.execute('SELECT * FROM view_string_table')
                info = cursor.fetchone()[1]
                if new_qty >= 144:
                    new_qty1 = new_qty // 144
                    new_qty3 = new_qty % 144
                    if new_qty3 >= 12:
                        new_qty = new_qty3 // 12
                        new_qty2 = new_qty % 12
                        temp_list = (str(new_qty1) + 'grs' + ' + ' + str(new_qty) + 'dzn' + ' + ' + str(
                            new_qty2) + 'pcs').split('+')
                        if temp_list[2].replace(' ', '') == '0pcs' and temp_list[1].replace(' ', '') != '0dzn':
                            new_str = str(new_qty1) + 'grs' + ' + ' + str(new_qty) + 'dzn'
                        elif temp_list[2].replace(' ', '') != '0pcs' and temp_list[1].replace(' ', '') == '0dzn':
                            new_str = str(new_qty1) + 'grs' + ' + ' + str(new_qty2) + 'pcs'
                        else:
                            new_str = str(new_qty1) + 'grs' + ' + ' + str(new_qty) + 'dzn' + ' + ' + str(
                                new_qty2) + 'pcs'
                        update_code = \
                            '''
                            UPDATE products
                            SET Quantity_Of_Product = ?
                            WHERE Name_Of_Product = ?
                            '''
                        cursor.execute(update_code, (new_str, product_name_data[0]))
                        old_string = \
                            ('{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + ('\t' * 4) + (
                                ' ' * 19) + '{2:<13s}'). \
                                format(name_ent.get().title(), quantity_data[0], price_data[0])
                        # print('old data = ', old_string)
                        new_string = \
                            ('{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + ('\t' * 4) + (
                                ' ' * 19) + '{2:<13s}'). \
                                format(name_ent.get().title(), new_str, price_data[0])
                        # print(new_string)
                        cursor.execute('DELETE FROM view_string_table')
                        # connection.commit()
                        # print(info)
                        print(old_string in info)
                        info = info.replace(old_string, new_string)
                        # os.system('cls')
                        sql_code = 'INSERT INTO view_string_table(sn, view_string)' \
                                   'VALUES (NULL, ?)'
                        cursor.execute(sql_code, (info,))
                        sql_code = 'INSERT INTO view_sales_string(id, view_stringSales)' \
                                   'VALUES (NULL, ?)'
                        cursor.execute('SELECT exists(SELECT 1 FROM view_sales_string LIMIT 1);')
                        result = cursor.fetchone()
                        if not result[0]:
                            print((price * qc.qty_converter(qty_sold)))
                            print('apprx: ', apprx.price_estimator((price * qc.qty_converter(qty_sold))))
                            info = ' ' * 3 + '{0:<6s}' + '\t'*2 + ' ' * 5 + '{1:<35s}' + '\t' * 5 + ' ' * 9 + \
                                   '{2:<9s}' + ' ' + '\t' * 2 \
                                   + '\t' + '{3:,}' + '\n'. \
                                       format(sales_time, name_ent.get().title(), qty_sold,
                                              apprx.price_estimator(int(price * qc.qty_converter(qty_sold)))) + \
                                                '_' * 97 + '\n'
                        else:
                            cursor.execute('SELECT * FROM view_sales_string')
                            info = cursor.fetchone()[1]
                            info += ' ' * 3 + '{0:<6s}' + '\t*2' + ' ' * 5 + '{1:<35s}' + '\t' * 5 + ' ' * 9 + \
                                    '{2:<9s}' + ' ' + '\t' * 2 \
                                    + '\t' + '{3:,}' + '\n'. \
                                        format(sales_time, name_ent.get().title(), qty_sold,
                                               apprx.price_estimator(int(price * qc.qty_converter(qty_sold)))) + \
                                    '_' * 97 + '\n'
                        cursor.execute(sql_code, (info,))

                    else:
                        temp_list = (str(new_qty1) + 'grs' + ' + ' + str(new_qty) + 'pcs').split('+')
                        if temp_list[1].replace(' ', '') == '0pcs':
                            new_str = str(new_qty1) + 'grs'
                        else:
                            new_str = str(new_qty1) + 'grs' + ' + ' + str(new_qty) + 'pcs'
                        update_code = \
                            '''
                            UPDATE products
                            SET Quantity_Of_Product = ?
                            WHERE Name_Of_Product = ?
                            '''
                        cursor.execute(update_code, (new_str, product_name_data[0]))
                        old_string = \
                            ('{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + ('\t' * 4) + (
                                ' ' * 19) + '{2:<13s}'). \
                                format(name_ent.get().title(), quantity_data[0], price_data[0])
                        # print('old data = ', old_string)
                        new_string = \
                            ('{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + ('\t' * 4) + (
                                ' ' * 19) + '{2:<13s}'). \
                                format(name_ent.get().title(), new_str, price_data[0])
                        # print(new_string
                        cursor.execute('DELETE FROM view_string_table')
                        # connection.commit()
                        # print(info)
                        print(old_string in info)
                        info = info.replace(old_string, new_string)
                        # os.system('cls')
                        sql_code = 'INSERT INTO view_string_table(sn, view_string)' \
                                   'VALUES (NULL, ?)'
                        cursor.execute(sql_code, (info,))
                        sql_code = 'INSERT INTO view_sales_string(id, view_stringSales)' \
                                   'VALUES (NULL, ?)'
                        cursor.execute('SELECT exists(SELECT 1 FROM view_sales_string LIMIT 1);')
                        result = cursor.fetchone()
                        if not result[0]:
                            info = ' ' * 3 + '{0:<6s}' + '\t*2' + ' ' * 5 + '{1:<35s}' + '\t' * 5 + ' ' * 9 + \
                                   '{2:<9s}' + ' ' + '\t' * 2 \
                                   + '\t' + '{3:,}' + '\n'. \
                                       format(sales_time, name_ent.get().title(), qty_sold,
                                              apprx.price_estimator(price * qc.qty_converter(qty_sold))) \
                                                + '_' * 97 + '\n'
                        else:
                            cursor.execute('SELECT * FROM view_sales_string')
                            info = cursor.fetchone()[1]
                            info += ' ' * 3 + '{0:<6s}' + '\t*2' + ' ' * 5 + '{1:<35s}' + '\t' * 5 + ' ' * 9 + \
                                    '{2:<9s}' + ' ' + '\t' * 2 \
                                    + '\t' + '{3:,}' + '\n'. \
                                        format(sales_time, name_ent.get().title(), qty_sold,
                                               apprx.price_estimator(price * qc.qty_converter(qty_sold))) + \
                                                '_' * 97 + '\n'
                        cursor.execute(sql_code, (info,))
                elif new_qty >= 12:
                    new_qty1 = new_qty // 12
                    new_qty = new_qty % 12
                    temp_list = (str(new_qty1) + 'dzn' + ' + ' + str(new_qty) + 'pcs').split('+')
                    if temp_list[1].replace(' ', '') == '0pcs':
                        new_str = str(new_qty1) + 'dzn'
                    else:
                        new_str = str(new_qty1) + 'dzn' + '+' + str(new_qty) + 'pcs'
                    update_code = \
                        '''
                        UPDATE products
                        SET Quantity_Of_Product = ?
                        WHERE Name_Of_Product = ?
                        '''
                    cursor.execute(update_code, (new_str, product_name_data[0]))
                    old_string = \
                        ('{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + ('\t' * 4) + (
                            ' ' * 19) + '{2:<13s}'). \
                            format(name_ent.get().title(), quantity_data[0], price_data[0])
                    # print('old data = ', old_string)
                    new_string = \
                        ('{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + ('\t' * 4) + (
                            ' ' * 19) + '{2:<13s}'). \
                            format(name_ent.get().title(), new_str, price_data[0])
                    # print(new_string)
                    cursor.execute('DELETE FROM view_string_table')
                    # connection.commit()
                    # print(info)
                    print(old_string in info)
                    info = info.replace(old_string, new_string)
                    # os.system('cls')
                    sql_code = 'INSERT INTO view_string_table(sn, view_string)' \
                               'VALUES (NULL, ?)'
                    cursor.execute(sql_code, (info,))
                    sql_code = 'INSERT INTO view_sales_string(id, view_stringSales)' \
                               'VALUES (NULL, ?)'
                    cursor.execute('SELECT exists(SELECT 1 FROM view_sales_string LIMIT 1);')
                    result = cursor.fetchone()
                    if not result[0]:
                        print(price, qty_sold, qc.qty_converter(qty_sold))
                        info = (' '*3 + '{0:<6s}' + '\t'*2 + ' '*5 + '{1:<35s}' + '\t'*5 + ' '*9 +
                               '{2:<9s}' + ' ' + '\t'*3 + '{3:}' + '\n').\
                                   format(sales_time, name_ent.get().title(), qty_sold,
                                          apprx.price_estimator(price * qc.qty_converter(qty_sold))) + \
                               '_' * 97 + '\n'
                    else:
                        cursor.execute('SELECT * FROM view_sales_string')
                        info = cursor.fetchone()[1]
                        cursor.execute('DELETE FROM view_sales_string')
                        info += (' '*3 + '{0:<6s}' + '\t'*2 + ' '*5 + '{1:<35s}' + '\t'*5 + ' '*9 +
                                 '{2:<9s}' + ' ' + '\t'*3 + ' '*5 + '{3:,}' + '\n'). \
                                    format(sales_time, name_ent.get().title(), qty_sold,
                                           apprx.price_estimator(price * qc.qty_converter(qty_sold))) + \
                                              '_' * 97 + '\n'
                    cursor.execute(sql_code, (info,))
                else:
                    temp_list = (str(new_qty) + 'pcs').split('+')
                    if temp_list[0].replace(' ', '') == '0pcs':
                        new_str = str(0)
                    else:
                        new_str = str(new_qty) + 'pcs'
                    update_code = \
                        '''
                        UPDATE products
                        SET Quantity_Of_Product = ?
                        WHERE Name_Of_Product = ?
                        '''
                    cursor.execute(update_code, (new_str, product_name_data[0]))
                    old_string = \
                        ('{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + ('\t' * 4) + (
                            ' ' * 19) + '{2:<13s}'). \
                            format(name_ent.get().title(), quantity_data[0], price_data[0])
                    # print('old data = ', old_string)
                    new_string = \
                        ('{0:<30s}' + (' ' * 4) + ('\t' * 5) + (' ' * 17) + '{1:<10s}' + ('\t' * 4) + (
                            ' ' * 19) + '{2:<13s}'). \
                            format(name_ent.get().title(), new_str, price_data[0])
                    # print(new_string)
                    cursor.execute('DELETE FROM view_string_table')
                    # connection.commit()
                    # print(info)
                    print(old_string in info)
                    info = info.replace(old_string, new_string)
                    # os.system('cls')
                    sql_code = 'INSERT INTO view_string_table(sn, view_string)' \
                               'VALUES (NULL, ?)'
                    cursor.execute(sql_code, (info,))
                    sql_code = 'INSERT INTO view_sales_string(id, view_stringSales)' \
                               'VALUES (NULL, ?)'
                    cursor.execute('SELECT exists(SELECT 1 FROM view_sales_string LIMIT 1);')
                    result = cursor.fetchone()
                    if not result[0]:
                        info = ' ' * 3 + '{0:<6s}' + '\t*2' + ' ' * 5 + '{1:<35s}' + '\t' * 5 + ' ' * 9 + '{2:<9s}' + ' ' + '\t' * 2 \
                               + '\t' + '{3:,}' + '\n'. \
                                   format(sales_time, name_ent.get().title(), qty_sold,
                                          apprx.price_estimator(price * qc.qty_converter(qty_sold))) + \
                               '_' * 97 + '\n'
                    else:
                        cursor.execute('SELECT * FROM view_sales_string')
                        info = cursor.fetchone()[1]
                        info += ' ' * 3 + '{0:<6s}' + '\t*2' + ' ' * 5 + '{1:<35s}' + '\t' * 5 + ' ' * 9 + '{2:<9s}' + ' ' + '\t' * 2 \
                                + '\t' + '{3:,}' + '\n'. \
                                    format(sales_time, name_ent.get().title(), qty_sold,
                                           apprx.price_estimator(price * qc.qty_converter(qty_sold))) \
                                                + '_' * 97 + '\n'
                    cursor.execute(sql_code, (info,))
                prompt = tkinter.messagebox.askyesno('Confirm', 'Sales successfully recorded'
                                                                '\nWould you like to record another sales: ')
                if prompt:
                    name_ent.delete(0, 'end')
                    qty_ent.delete(0, tk.END)
                else:
                    transaction_window.destroy()
                    app.deiconify()
                # connection.close()
                return 0

        t_lab.grid_forget()
        btn2.grid_forget()
        btn3.grid_forget()
        btn4.grid_forget()
        btn5.grid_forget()
        btn6.grid_forget()
        sales_frame = tk.Frame(transaction_window, bg='dark turquoise')
        sales_frame.winfo_toplevel().geometry("500x200-220+220")
        sales_frame.grid()
        name_lab = tk.Label(sales_frame, bg='dark turquoise', font='helvetica 10 bold',
                            text='{0:<20s}'.format('Name of Sold Product: '))
        name_ent = tk.Entry(sales_frame, font='helvetica 8 bold')
        name_lab.grid(row=0, column=0, pady=10, padx=8)
        name_ent.grid(row=0, column=1, ipadx=90)
        qty_lab = tk.Label(sales_frame, bg='dark turquoise', font='helvetica 10 bold',
                           text='{0:<13s}'.format('Quantity Sold Out: '))
        qty_ent = tk.Entry(sales_frame, font='helvetica 8 bold')
        qty_ent2 = tk.Spinbox(sales_frame, font='helvetica 8 bold', values=('pcs', 'grs', 'dzn'), wrap=True,
                              width=5)
        qty_lab.grid(row=1, column=0, pady=10)
        qty_ent.grid(row=1, column=1, ipadx=3, sticky='w')
        qty_ent2.grid(row=1, column=1, ipadx=2, padx=60)
        btn_exp = tk.Button(sales_frame, bg='sky blue', cursor='hand2', command=sales_recorder, bd=4,
                            font='helvetica 10 bold', text='Record')
        btn_exp.grid(pady=25, columnspan=500)

        def btn_exp_handler(event):
            sales_recorder()
            return 0

        btn_exp.bind('<Return>', btn_exp_handler)
        return 0

    def expenses():
        def scroller_up_handler(event):
            purpose_ent.yview(tk.SCROLL, -2, 'units')
            return 0

        def scroller_down_handler(event):
            purpose_ent.yview(tk.SCROLL, 2, 'units')
            return 0

        def expenses_recorder():
            key_time = datetime.datetime.now()
            date = datetime.datetime(key_time.year, key_time.month, key_time.day, key_time.hour,
                                     key_time.minute, key_time.second)
            exp_date = date.strftime('%d - %m - %y')
            connection = sqlite3.connect('store.db', isolation_level=None)
            cursor = connection.cursor()
            if purpose_ent.get('1.0').isspace():
                tkinter.messagebox.showerror('Error',
                                             'purpose of expenses is blank, please fill appropriately.')
            elif not mv.money_checker(amount_ent.get()):
                tkinter.messagebox.showerror('Error', 'Invalid input format for monetary value.')
                amount_ent.delete(0, 'end')
            else:
                # cursor.execute('SELECT exists(SELECT 1 FROM expenses LIMIT 1);')
                # result = cursor.fetchone()
                # insert_code = '''INSERT INTO expenses VALUES(NULL,?,?,?)'''
                # cursor.execute(insert_code, (exp_date, purpose_ent.get('1.0', '1.end'), amount_ent.get()))
                insert_code = '''INSERT INTO view_expenses_string VALUES(NULL,?)'''
                cursor.execute('SELECT exists(SELECT 1 FROM view_expenses_string LIMIT 1);')
                result = cursor.fetchone()
                if not result[0]:
                    # info = (' '*2)+'{0:<6s}'+' '+'\t'*3+' '*11+'{1:<35s}'+'\t*6'+' '*6+'{2:,}\n'. \
                    #                    format(exp_date, mv.wrapper(purpose_ent.get('1.0', '1.end')),
                    #                           int(mv.money_formatter(amount_ent.get()))) + '_' * 97 + '\n'
                    info = ((' ' * 2) + '{0:<6s}' + ' ' + '\t' * 3 + ' ' * 11 + '{1:<35s}' + '\t' * 6 + ' ' * 6
                            + '{2:,}\n').format(exp_date, mv.wrapper(purpose_ent.get('1.0', '1.end')),
                                                apprx.price_estimator(
                                                    int(mv.money_formatter(amount_ent.get())))) + '_' * \
                                                                                                  97 + '\n'
                else:
                    cursor.execute('SELECT * FROM view_expenses_string')
                    info = cursor.fetchone()[1]
                    cursor.execute('DELETE FROM view_expenses_string')
                    print(info)
                    info += ((' ' * 2) + '{0:<6s}' + ' ' + '\t' * 3 + ' ' * 11 + '{1:<35s}' + '\t' * 6 + ' ' * 6
                             + '{2:,}\n').format(exp_date, mv.wrapper(purpose_ent.get('1.0', '1.end')),
                                                 apprx.price_estimator(int(mv.money_formatter(amount_ent.get(

                                                 ))))) + '_' * 97 + '\n'
                cursor.execute(insert_code, (info,))
                prompt = tkinter.messagebox.askyesno('Confirm', 'Expenses successfully recorded'
                                                                '\nWould you like to record another expenses? ')
                if prompt:
                    purpose_ent.delete('1.0', '1.end')
                    amount_ent.delete(0, tk.END)
                else:
                    transaction_window.destroy()
                    app.deiconify()
            connection.close()
            return 0

        t_lab.grid_forget()
        btn2.grid_forget()
        btn3.grid_forget()
        btn4.grid_forget()
        btn5.grid_forget()
        btn6.grid_forget()
        expenses_frame = tk.Frame(transaction_window, bg='dark turquoise')
        expenses_frame.winfo_toplevel().geometry("500x300+300+220")
        expenses_frame.grid()
        purpose_lab = tk.Label(expenses_frame, bg='dark turquoise', font='helvetica 10 bold',
                               text='{0:<6s}'.format('Purpose of spending: '), width=19)
        purpose_ent = tk.Text(expenses_frame, font='helvetica 8 bold', width=50, height=6, spacing1=3, spacing2=3,
                              spacing3=3, wrap='word')
        purpose_lab.grid(row=1, column=0)
        purpose_ent.grid(row=1, column=1, padx=17, pady=15, sticky='w')
        amount_lab = tk.Label(expenses_frame, bg='dark turquoise', font='helvetica 10 bold',
                              text='{0:<13s}'.format('Amount Spent: '), width=15)
        amount_ent = tk.Entry(expenses_frame, font='helvetica 8 bold')
        amount_lab.grid(row=2, column=0, pady=10)
        amount_ent.grid(row=2, column=1, ipadx=3, sticky='w', padx=10)
        scroll_style = ttk.Style()
        scroll_style.configure('odk.Vertical.TScrollbar', troughcolor='light green', bg='navy', width=8)
        scroller = ttk.Scrollbar(expenses_frame, style='odk.Vertical.TScrollbar')
        scroller.grid(sticky=tk.E, column=1, row=1, ipady=36)
        scroller.configure(command=purpose_ent.yview)
        purpose_ent.configure(yscrollcommand=scroller.set)
        app.bind('<Up>', scroller_up_handler)
        app.bind('<Down>', scroller_down_handler)
        btn_exp = tk.Button(expenses_frame, bg='sky blue', cursor='hand2', command=expenses_recorder, bd=4,
                            font='helvetica 10 bold', text='Record')
        writer_label = tk.Label(expenses_frame, text=u'\N{copyright sign}' + ' an Andy Production',
                                font='purita 9 bold italic', bg='dark turquoise')
        btn_exp.grid(pady=55, columnspan=500)
        writer_label.grid(row=3, column=1, sticky='e')

        def btn_exp_handler(event):
            expenses_recorder()
            return 0

        btn_exp.bind('<Return>', btn_exp_handler)
        return 0

    def sales_viewer():
        def scroller_up_handler(event):
            text.yview(tk.SCROLL, -2, 'units')
            return 0

        def scroller_down_handler(event):
            text.yview(tk.SCROLL, 2, 'units')
            return 0

        def sales_viewer_btn_handler(event):
            back2Menu()
            return 0

        sales_viewer_frame = tk.Frame(transaction_window, bg='dark turquoise')
        sales_viewer_frame.winfo_toplevel().geometry("900x530+90+90")
        t_lab.grid_forget()
        btn2.grid_forget()
        btn3.grid_forget()
        btn4.grid_forget()
        btn5.grid_forget()
        btn6.grid_forget()
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()
        cursor.execute('SELECT exists(SELECT 1 FROM view_sales_string LIMIT 1);')
        result = cursor.fetchone()
        if not result[0]:
            sales_lab = tk.Label(transaction_window, text='No sales transaction have been made',
                                 bg='dark turquoise',
                                 font='helvetica 12 bold italic')
            sales_btn = tk.Button(transaction_window, text='Back to Main Menu', command=back2Menu,
                                  bg='dark turquoise', cursor='hand2', font='purita 10 bold italic')

            def sales_btn_handler(event):
                back2Menu()

            sales_btn.bind('<Return>', sales_btn_handler)
            sales_lab.pack(pady=90)
            sales_btn.pack()
        else:
            title = '{0:4s} {1:25s} {2:6s} {3:<47s}'.format('\tDate', '\t\tName Of Product',
                                                            '     \t\t\tQuantity Sold', '\t\tRealized price')
            sales_label = tk.Label(transaction_window, text=title, bg='dark turquoise',
                                   font='helvetica 12 bold italic')
            sales_label.pack()
            s = ttk.Style()
            s.configure('odk.Vertical.TScrollbar')
            scroller = ttk.Scrollbar(sales_viewer_frame, style='odk.Vertical.TScrollbar')
            text = tk.Text(sales_viewer_frame, width=500, height=24, bg='dark turquoise', font='helvetica 12')
            sales_viewer_btn = tk.Button(transaction_window, bg='dark turquoise', text='Back to Main Menu',
                                         bd=4, command=back2Menu, cursor='hand2', font='helvetica 10 bold italic')
            writer_label = tk.Label(transaction_window, text=u'\N{copyright sign}' + ' an Andy Production',
                                    font='purita 9 bold italic', bg='dark turquoise')
            cursor.execute('SELECT * FROM view_sales_string')
            sales_record = cursor.fetchone()[1]
            text.insert(tk.END, sales_record)
            text.config(state=tk.DISABLED)
            sales_viewer_frame.pack()
            scroller.pack(side=tk.RIGHT, fill=tk.Y)
            text.pack(side=tk.LEFT, fill=tk.Y)
            sales_viewer_btn.pack(pady=10)
            writer_label.pack(side='right')
            scroller.configure(command=text.yview)
            text.configure(yscrollcommand=scroller.set)
            app.bind('<Up>', scroller_up_handler)
            app.bind('<Down>', scroller_down_handler)
            sales_viewer_btn.bind('<Return>', sales_viewer_btn_handler)
        connection.close()
        return 0
        # shelf = shelve.open('Store')
        # if 'recorded sales' not in shelf:
        #     sales_lab = tk.Label(transaction_window, text='No sales transaction have been made',
        # bg='dark turquoise',
        #                          font='helvetica 12 bold italic')
        #     sales_btn = tk.Button(transaction_window, text='Back to Main Menu', command=back2Menu,
        #                           bg='dark turquoise', cursor='hand2', font='purita 10 bold italic')
        #     def sales_btn_handler(event):
        #         back2Menu()
        #     sales_btn.bind('<Return>', sales_btn_handler)
        #     sales_lab.pack(pady=90)
        #     sales_btn.pack()
        # else:
        #     title = '{0:4s} {1:25s} {2:6s} {3:<47s}'.format('\tDate', '\t\tName Of Product',
        # '     \t\t\tQuantity Sold',
        #                                                        '\t\tRealized price')
        #     sales_label = tk.Label(transaction_window, text=title, bg='dark turquoise', font='helvetica 12
        # bold italic')
        #     sales_label.pack()
        #     s = ttk.Style()
        #     s.configure('odk.Vertical.TScrollbar')
        #     scroller = ttk.Scrollbar(sales_viewer_frame, style='odk.Vertical.TScrollbar')
        #     text = tk.Text(sales_viewer_frame, width=500, height=24, bg='dark turquoise', font='helvetica 12')
        #     sales_viewer_btn = tk.Button(transaction_window, bg='dark turquoise', text='Back to Main Menu',
        #                                  bd=4, command=back2Menu, cursor='hand2', font='helvetica 10 bold
        # italic')
        #     writer_label = tk.Label(transaction_window, text=u'\N{copyright sign}' + ' an Andy Production',
        #                             font='purita 9 bold italic', bg='dark turquoise')
        #     sales_record = ''
        #     for index in shelf['recorded sales']:
        #         sales_record += '  {0:<6s} \t\t     {1:<35s}\t\t\t\t\t         {2:<9s} \t\t           \t
        #  {3:,}\n'.\
        #                             format(index[0], index[1], index[2], index[3])+'_'*97+'\n'
        #     text.insert(tk.END, sales_record)
        #     text.config(state=tk.DISABLED)
        #     sales_viewer_frame.pack()
        #     scroller.pack(side=tk.RIGHT, fill=tk.Y)
        #     text.pack(side=tk.LEFT, fill=tk.Y)
        #     sales_viewer_btn.pack(pady=10)
        #     writer_label.pack(side='right')
        #     scroller.configure(command=text.yview)
        #     text.configure(yscrollcommand=scroller.set)
        #     app.bind('<Up>', scroller_up_handler)
        #     app.bind('<Down>', scroller_down_handler)
        #     sales_viewer_btn.bind('<Return>', sales_viewer_btn_handler)
        # shelf.close()
        # return 0

    def expenses_viewer():
        def scroller_up_handler(event):
            exp_text.yview(tk.SCROLL, -2, 'units')
            return 0

        def scroller_down_handler(event):
            exp_text.yview(tk.SCROLL, 2, 'units')
            return 0

        def back2Menu_btn_handler(event):
            back2Menu()
            return 0

        expenses_viewer_frame = tk.Frame(transaction_window, bg='dark turquoise')
        expenses_viewer_frame.winfo_toplevel().geometry("900x540+90+90")
        t_lab.grid_forget()
        btn2.grid_forget()
        btn3.grid_forget()
        btn4.grid_forget()
        btn5.grid_forget()
        btn6.grid_forget()
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()
        cursor.execute('SELECT exists(SELECT 1 FROM view_expenses_string);')
        result = cursor.fetchone()
        if not result[0]:
            expenses_lab = tk.Label(transaction_window, text='No expenses transaction have been made',
                                    bg='dark turquoise', font='helvetica 12 bold italic')
            expenses_btn = tk.Button(transaction_window, text='Back to Main Menu', command=back2Menu,
                                     font='purita 10 bold italic', bg='dark turquoise', cursor='hand2')
            expenses_lab.pack(pady=90)
            expenses_btn.pack()
        else:
            cursor.execute('SELECT * FROM view_expenses_string')
            expenses_data = cursor.fetchone()[1]
            title = '{0:<40s} {1:<25s} {2:<47s}'.format('Date', '\t\tPurpose Of Spending', '     \t\t\tAmount '
                                                                                           'Spent')
            expenses_label = tk.Label(expenses_viewer_frame, text=title, bg='dark turquoise',
                                      font='helvetica 12 bold italic')
            expenses_label.pack()
            s = ttk.Style()
            s.configure('odk.Vertical.TScrollbar')
            exp_text = tk.Text(expenses_viewer_frame, width=97, height=24, bg='dark turquoise',
                               font='helvetica 12')
            exp_text.pack()
            # expenses_record = ''
            scroller = ttk.Scrollbar(expenses_viewer_frame, style='odk.Vertical.TScrollbar')
            back2Menu_btn = tk.Button(transaction_window, text='Back to Main Menu', bg='dark turquoise',
                                      font='helvetica 10 bold italic', command=back2Menu, cursor='hand2')
            writer_label = tk.Label(transaction_window, text=u'\N{copyright sign}' + ' an Andy Production',
                                    font='purita 9 bold italic', bg='dark turquoise')
            exp_text.insert(tk.END, expenses_data)
            exp_text.config(state=tk.DISABLED)
            expenses_viewer_frame.pack()
            scroller.configure(command=exp_text.yview)
            exp_text.configure(yscrollcommand=scroller.set)
            scroller.pack(side=tk.RIGHT, fill=tk.Y)
            exp_text.pack(side=tk.LEFT, fill=tk.Y)
            back2Menu_btn.pack(pady=15)
            writer_label.pack(side='right')
            app.bind('<Up>', scroller_up_handler)
            app.bind('<Down>', scroller_down_handler)
            back2Menu_btn.bind('<Return>', back2Menu_btn_handler)
        connection.close()
        return 0
        # shelf = shelve.open('Store')
        # if 'recorded expenses' not in shelf:
        #     expenses_lab = tk.Label(transaction_window, text='No expenses transaction have been made',
        #                             bg='dark turquoise', font='helvetica 12 bold italic')
        #     expenses_btn = tk.Button(transaction_window, text='Back to Main Menu', command=back2Menu,
        #                              font='purita 10 bold italic', bg='dark turquoise', cursor='hand2')
        #     expenses_lab.pack(pady=90)
        #     expenses_btn.pack()
        # else:
        #     title = '{0:<40s} {1:<25s} {2:<47s}'.format('Date', '\t\tPurpose Of Spending', '     \t\t\tAmount '
        #                                                                                          'Spent')
        #     expenses_label = tk.Label(expenses_viewer_frame, text=title, bg='dark turquoise', font='helvetica
        #  12 bold italic')
        #     expenses_label.pack()
        #     s = ttk.Style()
        #     s.configure('odk.Vertical.TScrollbar')
        #
        #     exp_text = tk.Text(expenses_viewer_frame, width=97, height=24, bg='dark turquoise',
        # font='helvetica 12')
        #     expenses_record = ''
        #     exp_text.pack()
        #     expenses_record = ''
        #     scroller = ttk.Scrollbar(expenses_viewer_frame, style='odk.Vertical.TScrollbar')
        #     back2Menu_btn = tk.Button(transaction_window, text='Back to Main Menu', bg='dark turquoise',
        #                               font='helvetica 10 bold italic', command=back2Menu, cursor='hand2')
        #     writer_label = tk.Label(transaction_window, text=u'\N{copyright sign}' + ' an Andy Production',
        #                             font='purita 9 bold italic', bg='dark turquoise')
        #     for expenses in shelf['recorded expenses']:
        #         expenses_record += '  {0:<6s} \t\t\t           {1:<35s}\t\t\t\t\t\t      {2:,}\n'. \
        #         format(expenses[0], mv.wrapper(expenses[1]), int(mv.money_formatter(expenses[2]))) + '_' * 97\
        #                            + '\n'
        #     exp_text.insert(tk.END, expenses_record)
        #     exp_text.config(state=tk.DISABLED)
        #     expenses_viewer_frame.pack()
        #     scroller.configure(command=exp_text.yview)
        #     exp_text.configure(yscrollcommand=scroller.set)
        #     scroller.pack(side=tk.RIGHT, fill=tk.Y)
        #     exp_text.pack(side=tk.LEFT, fill=tk.Y)
        #     back2Menu_btn.pack(pady=15)
        #     writer_label.pack(side='right')
        #     app.bind('<Up>', scroller_up_handler)
        #     app.bind('<Down>', scroller_down_handler)
        #     back2Menu_btn.bind('<Return>', back2Menu_btn_handler)
        # shelf.close()
        # return 0

    t_lab = tk.Label(transaction_window, bg='dark turquoise', font='helvetica 12 bold italic',
                     text='Select a mode of transaction: ')
    btn2 = tk.Button(transaction_window, text='Record Expenses', bg='sky blue', font='helvetica 10 bold',
                     command=expenses, cursor='hand2')
    btn3 = tk.Button(transaction_window, text='Record Sales/Income', bg='sky blue', font='helvetica 10 bold',
                     command=sales, cursor='hand2')
    btn4 = tk.Button(transaction_window, text='view sales', bg='sky blue', font='helvetica 10 bold',
                     cursor='hand2', command=sales_viewer)
    btn5 = tk.Button(transaction_window, text='view expenses\t\t', bg='sky blue', font='helvetica 10 bold',
                     cursor='hand2', command=expenses_viewer)
    btn6 = tk.Button(transaction_window, text='Back', bg='sky blue', font='helvetica 10 bold',
                     cursor='hand2', command=back2Menu)
    t_lab.grid(row=0, column=1, pady=5, columnspan=6)
    btn2.grid(row=2, column=1, sticky=tk.E, padx=10, pady=25)
    btn5.grid(row=3, column=1, pady=15, padx=10, sticky=tk.E)
    btn3.grid(row=2, column=2, sticky=tk.W, padx=40)
    btn4.grid(row=3, column=2, sticky=tk.W, padx=40)
    btn6.grid(row=4, column=1, columnspan=5, pady=40, ipadx=103)

    def btn2_handler(event):
        expenses()
        return 0

    btn2.bind('<Return>', btn2_handler)

    def btn3_handler(event):
        sales()
        return 0

    btn3.bind('<Return>', btn3_handler)

    def sales_viewer_handler(event):
        sales_viewer()
        return 0

    btn4.bind('<Return>', sales_viewer_handler)

    def expenses_viewer_handler(event):
        expenses_viewer()
        return 0

    btn5.bind('<Return>', expenses_viewer_handler)

    def Back2Menu_handler(event):
        back2Menu()
        return 0

    btn6.bind('<Return>', Back2Menu_handler)
    return 0


def frame2():
    app.configure(background='lightgrey')
    connection = sqlite3.connect('store.db')
    cursor = connection.cursor()
    cursor.execute('SELECT name_of_company FROM company_credentials WHERE sn=?', (1,))
    Name_of_company = cursor.fetchone()[0]
    f2.winfo_toplevel().geometry("1000x700-190+10")
    f2.grid()
    title = tk.Label(f2, text='\t\tWelcome to the Store Manager App\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t',
                     font='Helvetica 20 bold italic', fg='firebrick', bg='navy')
    company = tk.Label(f2, text='\n\nName of Company:  '
                                + str(Name_of_company), font='Calibri 13 italic', fg='white', bg='navy')
    instruction = tk.Label(app, text='\n\nclick on any image below to use any feature', background='lightgrey',
                           font='helvetica 14 bold')
    title.pack(pady=5)
    company.pack(padx=20, side=tk.LEFT)
    instruction.grid(row=4, sticky='w', padx=262)
    image = Image.open('c:\\users\\user\\pycharmprojects\\app_store\\change_password_icon1.gif')
    photo = ImageTk.PhotoImage(image)
    btn2 = tk.Button(app, text="Link", cursor="hand2", image=photo, command=change, background='orange', bd=3)
    btn2.image = photo
    btn2.grid(pady=65, columnspan=1, sticky='w', padx=65)
    image1 = Image.open('c:\\users\\user\\pycharmprojects\\app_store\\view_icon.jpg')
    photo1 = ImageTk.PhotoImage(image1)
    btn3 = tk.Button(app, height=150, text='Link', cursor="hand2", image=photo1, command=view,
                     background='orange',
                     bd=3)
    btn3.image = photo1
    btn3.grid(row=5, sticky='w', padx=400)
    image2 = Image.open('c:\\users\\user\\pycharmprojects\\app_store\\update_store_icon.jpg')
    photo2 = ImageTk.PhotoImage(image2)
    btn4 = tk.Button(app, text='Link', highlightthickness=0, cursor='hand2', image=photo2, command=update,
                     background='orange', bd=3)
    btn4.image = photo2
    btn4.grid(row=5, sticky='w', padx=750)
    image3 = Image.open('c:\\users\\user\\pycharmprojects\\app_store\\e-transaction.jpg')
    photo3 = ImageTk.PhotoImage(image3)
    btn5 = tk.Button(app, text='Link', cursor='hand2', image=photo3, command=transactions, background='orange',
                     bd=3)
    btn5.image = photo3
    btn5.grid(row=6, columnspan=1, sticky='w', padx=65)
    image4 = Image.open('c:\\users\\user\\pycharmprojects\\app_store\\help_icon.jpg')
    photo4 = ImageTk.PhotoImage(image4)
    btn6 = tk.Button(app, text='Link', cursor='hand2', image=photo4, command=help_btn, bg='orange', bd=3)
    btn6.image = photo4
    btn6.grid(row=6, sticky='w', padx=750)
    return 0


def collector():
    """This function collects the name of the company as well as the initialized password"""
    connection = sqlite3.connect('store.db')
    cursor = connection.cursor()
    if password.get() != password1.get():
        prompt = tkinter.messagebox.askretrycancel('password not identical', 'password mismatch')
        if prompt:
            password.delete(0, tk.END)
            password1.delete(0, tk.END)
        else:
            exit()
    else:
        if password.get() == '':
            tkinter.messagebox.showinfo('Blank Password', 'please enter password before submitting')
        elif name.get() == '':
            tkinter.messagebox.showinfo('Name of Company blank', 'Enter the name of your company')
        else:
            insert_command = \
                '''
                INSERT INTO company_credentials(
                sn, name_of_company, password1, password2)
                VALUES(NULL, ?,?,?);
                '''
            cursor.execute(insert_command, (name.get(), password1.get(), password.get()))
            connection.commit()
            tkinter.messagebox.showinfo('success', 'password successfully initialized')
            f1.winfo_toplevel().geometry('439x230')
            MAX = 1500
            s = ttk.Style()
            s.theme_use('clam')
            s.configure('red.Horizontal.TProgressbar', foreground='red', background='navy')
            progress_var = tk.DoubleVar()
            w0 = tk.Label(f1, text="saving your company's credentials", bg='#a1dbcd', fg='black', pady=20,
                          font='helvetica 12 bold')
            w3 = tk.Label(f1, text='please ensure the time and date setting of your computer is always\ncurrent',
                          bg='#a1dbcd', fg='black', font='purita 9 bold italic')
            w1 = ttk.Progressbar(f1, style='red.Horizontal.TProgressbar', variable=progress_var,
                                 orient='horizontal', length=399, mode='determinate', maximum=MAX)
            name.grid_forget()
            password.grid_forget()
            lab.grid_forget()
            lab2.grid_forget()
            lab3.grid_forget()
            password1.grid_forget()
            btn1.grid_forget()
            w1.pack(ipady=20, pady=15, padx=10)
            w0.pack(padx=60)
            w3.pack(side='bottom', padx=15)
            for i in range(MAX):
                progress_var.set(i)
                time.sleep(0.01)
                f1.update()
            f1.grid_forget()
            f2.grid(row=0, column=0, sticky='nswe')
            frame2()
    # connection.close()
    app.configure(background='lightgrey')
    return 0


app = tk.Tk()
app.resizable(0, 0)
app.configure(background='#a1dbcd')
imgicon = ImageTk.PhotoImage(file=os.path.join('c:\\users\\user\\pycharmprojects\\app_store', 'store.ico'))
app.tk.call('wm', 'iconphoto', app._w, imgicon)
app.title('Store Manager')
f1 = tk.Frame(app, bg='#a1dbcd')
f2 = tk.Frame(app, bg='navy')
change_frame = tk.Frame(app, bg='#a1dbcd')
f2.winfo_toplevel().geometry('')
connection = sqlite3.connect('store.db')
cursor = connection.cursor()
cursor.execute('SELECT * FROM company_credentials;')
data = cursor.fetchall()
if not data:
    f1.grid(row=0, column=0, sticky='nsew')
    f1.winfo_toplevel().geometry('450x200+400+200')
    lab = tk.Label(f1, width=15, text="Name of Company: ", bg='#a1dbcd', font='helvetica 10 bold')
    name = tk.Entry(f1, font='calibri 10 bold')
    lab.grid(row=2, column=1, padx=1, pady=10)
    name.grid(row=2, column=3, padx=1, pady=10, ipadx=80)
    lab2 = tk.Label(f1, width=15, text="Initialize password:", bg='#a1dbcd', font='helvetica 10 bold')
    password = tk.Entry(f1, show="\u2022", font='calibri 10 bold')
    lab2.grid(row=4, column=1, pady=10, padx=2)
    password.grid(pady=10, row=4, column=3, padx=9, ipadx=80)
    lab3 = tk.Label(f1, text="Confirm password: ", width=15, bg='#a1dbcd', font='helvetica 10 bold')
    password1 = tk.Entry(f1, show="\u2022", font='calibri 10 bold')
    lab3.grid(row=6, column=1, pady=10)
    password1.grid(row=6, column=3, ipadx=80)
    btn1 = tk.Button(f1, text='Submit', cursor='hand2', bg='#a1dbcd', fg='black', height=1, command=collector,
                     font='helvetica 12 bold italic')
    btn1.grid(row=10, pady=26, column=1, columnspan=4)


    def btn1_handler(event):
        collector()


    btn1.bind('<Return>', btn1_handler)
else:
    frame2()
    # Everythong we'll be adding to make this app more functional and beautiful will
    # be done so under the function frame2 and we'll now call that function here. That
    # is the logic I'm going to employ
# this_year = time.time()
# new_year =
connection.close()
app.mainloop()
