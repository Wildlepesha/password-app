from tkinter import *
from tkinter import ttk
import sqlite3 as sql
import pyperclip
import webbrowser as wb
from tkinter import messagebox

root = Tk()
root.title("Passwords App")
root.geometry("1000x600")
root.resizable(False, False)
changed = 0
del_one_info = ''


# data = [
#     ["Yandex1", "login", "password", "ya.ru"],
#     ["Yandex2", "login", "password", "ya.ru"],
#     ["Yandex3", "login", "password", "ya.ru"],
#     ["Yandex4", "login", "password", "ya.ru"],
#     ["Yandex5", "login", "password", "ya.ru"],
#     ["Yandex6", "login", "password", "ya.ru"],
#     ["Yandex7", "login", "password", "ya.ru"],
#     ["Yandex8", "login", "password", "ya.ru"],
#     ["Yandex9", "login", "password", "ya.ru"],
#     ["Yandex10", "login", "password", "ya.ru"],
#     ["Yandex1", "login", "password", "ya.ru"],
#     ["Yandex12", "login", "password", "ya.ru"],
#     ["Yandex13", "login", "password", "ya.ru"],
#     ["Yandex14", "login", "password", "ya.ru"],
#     ["Yandex15", "login", "password", "ya.ru"],
#     ["Yandex16", "login", "password", "ya.ru"],
#     ["Yandex17", "login", "password", "ya.ru"],
#     ["Yandex18", "login", "password", "ya.ru"],
#     ["Yandex19", "login", "password", "ya.ru"],
#     ["Yandex20", "login", "password", "ya.ru"],
# ]


# database stuff
conn = sql.connect('passwords.db')
c = conn.cursor()
c.execute("""CREATE TABLE if not exists users (
name text,
login text,
password text,
link text 
)""")

# dd simple data to table

# for record in data:
#    c.execute("""INSERT INTO users VALUES (:name, :login, :password, :link)""",
#              {
#                 'name': record[0],
#                  "login": record[1],
#                  "password": record[2],
#                  "link": record[3],
#              }
#              )
#
#
# conn.commit()
# conn.close()


def query_database():
    conn = sql.connect('passwords.db')
    c = conn.cursor()

    c.execute("""SELECT rowid, * FROM users""")
    records = c.fetchall()
    global count
    count = 0

    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[0], record[1], record[2], record[3], record[4]),
                           tags='evenrow')
        else:
            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[0], record[1], record[2], record[3], record[4]),
                           tags='oddrow')
        count += 1

    conn.commit()
    conn.close()


# style
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3")

style.map("Treeview", background=[('selected', "#347083")])

# Treeview frame
tree_frame = Frame(root)
tree_frame.pack(pady=10)
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()

# Configure scrollbar
tree_scroll.config(command=my_tree.yview)

# Format columns
my_tree['columns'] = ("ID", "Name", "Login", "Password", "Link")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=CENTER, width=30)
my_tree.column("Name", anchor=W, width=240)
my_tree.column("Login", anchor=CENTER, width=240)
my_tree.column("Password", anchor=CENTER, width=240)
my_tree.column("Link", anchor=CENTER, width=240)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Login", text="Login", anchor=CENTER)
my_tree.heading("Password", text="Password", anchor=CENTER)
my_tree.heading("Link", text="Link", anchor=CENTER)

my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")


# Record boxes
data_frame = LabelFrame(root, text="Record")
data_frame.pack(fill="x", expand="yes", padx=20)

name_label = Label(data_frame, text="Name")
name_label.grid(row=0, column=0, padx=10, pady=10)
name_entry = Entry(data_frame)
name_entry.grid(row=0, column=1, padx=10, pady=10)

login_label = Label(data_frame, text="Login")
login_label.grid(row=0, column=2, padx=10, pady=10)
login_entry = Entry(data_frame, width=25)
login_entry.grid(row=0, column=3, padx=10, pady=10)

password_label = Label(data_frame, text="Password")
password_label.grid(row=0, column=4, padx=10, pady=10)
password_entry = Entry(data_frame, width=25)
password_entry.grid(row=0, column=5, padx=10, pady=10)

link_label = Label(data_frame, text="Link")
link_label.grid(row=0, column=6, padx=10, pady=10)
link_entry = Entry(data_frame, width=25)
link_entry.grid(row=0, column=7, padx=10, pady=10)


def update_treeview():
    my_tree.delete(*my_tree.get_children())
    query_database()


def add():
    conn = sql.connect('passwords.db')
    c = conn.cursor()
    c.execute("""INSERT INTO users VALUES (:name, :login, :password, :link)""",
              {
                  "name": name_entry.get(),
                  "login": login_entry.get(),
                  "password": password_entry.get(),
                  "link": link_entry.get()
              }
              )
    conn.commit()
    conn.close()

    name_entry.delete(0, END)
    login_entry.delete(0, END)
    password_entry.delete(0, END)
    link_entry.delete(0, END)

    # update the treeview
    update_treeview()


def update():
    selected = my_tree.focus()
    values_json = my_tree.item(selected)
    id_item = values_json["values"][0]

    # update the database
    conn = sql.connect('passwords.db')
    c = conn.cursor()

    c.execute("""UPDATE users SET
    name = :name,
    login = :login,
    password = :password,
    link = :link

    WHERE oid = :oid""",
             {
                 'name': name_entry.get(),
                 'login': login_entry.get(),
                 'password': password_entry.get(),
                 'link': link_entry.get(),
                 'oid': id_item,
             }

             )

    conn.commit()
    conn.close()
    my_tree.item(selected, text='', values=(id_item, name_entry.get(), login_entry.get(),
                                            password_entry.get(), link_entry.get()))

    name_entry.delete(0, END)
    login_entry.delete(0, END)
    password_entry.delete(0, END)
    link_entry.delete(0, END)


def remove_one():
    global del_one_info
    selected = my_tree.focus()
    values_json = my_tree.item(selected)
    id_item = values_json["values"][0]

    conn = sql.connect('passwords.db')
    c = conn.cursor()
    c.execute("DELETE from users WHERE rowid="+str(id_item))
    conn.commit()
    conn.close()
    update_treeview()
    if changed == 0:
        del_one_info = messagebox.showinfo("Deleted", "Your record has been deleted")
    else:
        del_one_info = messagebox.showinfo("Удалено", "Запись была удалена")
    clear_entries()


def remove_many():
    if changed == 0:
        response = messagebox.askyesno("Delete chosen", "This wil delete chosen fields, confirm your intention")
    else:
        response = messagebox.askyesno("Удалить выбранное", "Это удалит выбранные поля, подтвердите свой выбор")
    if response == 1:
        x = my_tree.selection()

        # Create list of ID's
        ids_to_delete = []
        for record in x:
            ids_to_delete.append(my_tree.item(record, 'values')[0])

        conn = sql.connect('passwords.db')
        c = conn.cursor()

        c.executemany("DELETE FROM users WHERE rowid = ?", [(i,) for i in ids_to_delete])

        conn.commit()
        conn.close()

        update_treeview()
        clear_entries()


def remove_all():
    if changed == 0:
        response = messagebox.askyesno("Delete all", "This wil delete everything, confirm your intention")
    else:
        response = messagebox.askyesno("Удалить все", "Это удалит все поля, подтвердите свой выбор")
    if response == 1:
        conn = sql.connect('passwords.db')
        c = conn.cursor()
        c.execute("DROP TABLE users")
        conn.commit()
        c.execute("""CREATE TABLE users (
            name text,
            login text,
            password text,
            link text 
            )""")
        conn.commit()
        conn.close()
        update_treeview()
        clear_entries()


def up():
    rows = my_tree.selection()
    for row in rows:
        my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)


def down():
    rows = my_tree.selection()
    for row in reversed(rows):
        my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)


def clear_entries():
    name_entry.delete(0, END)
    login_entry.delete(0, END)
    password_entry.delete(0, END)
    link_entry.delete(0, END)
    root.focus_set()


def select_record(e):
    name_entry.delete(0, END)
    login_entry.delete(0, END)
    password_entry.delete(0, END)
    link_entry.delete(0, END)
    # Grab record Number
    selected = my_tree.focus()
    values = my_tree.item(selected, "values")

    # output to entry boxes
    name_entry.insert(0, values[1])
    login_entry.insert(0, values[2])
    password_entry.insert(0, values[3])
    link_entry.insert(0, values[4])


def copy_login():
    selected = my_tree.focus()
    values_json = my_tree.item(selected)
    login_item = values_json["values"][2]
    pyperclip.copy(login_item)
    messagebox.showinfo("Copied", "Login copied!")


def copy_password():
    selected = my_tree.focus()
    values_json = my_tree.item(selected)
    password_item = values_json["values"][3]
    pyperclip.copy(password_item)
    messagebox.showinfo("Copied", "Password copied!")


def open_link():
    selected = my_tree.focus()
    values_json = my_tree.item(selected)
    link_item = values_json["values"][4]
    wb.register("Yandex", None,
                wb.BackgroundBrowser(r"C:\Users\PC\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"))
    wb.get(using="Yandex").open(link_item)
    messagebox.showinfo("Opened", "Browser opened")


def lang_change_ru():
    global changed, del_one_info
    if changed == 0:
        my_tree.heading("Name", text="Название")
        my_tree.heading("Login", text="Логин")
        my_tree.heading("Password", text="Пароль")
        my_tree.heading("Link", text="Ссылка")

        data_frame.configure(text='Запись')

        name_label.configure(text='Название')
        password_label.configure(text='Логин')
        login_label.configure(text='Пароль')
        link_label.configure(text='Ссылка')

        button_frame.configure(text='Действия')
        danger_frame.configure(text='Удаление')

        update_button.configure(text='Обновить')
        add_button.configure(text='Добавить')
        remove_one_button.configure(text='Удалить одну запись', width=20)
        remove_many_button.configure(text='Удалить несколько записей', width=25)
        remove_all_button.configure(text='Удалить все записи', width=20)
        move_up_button.configure(text='Поднять запись', width=15)
        move_down_button.configure(text='Опустить запись')
        clear_button.configure(text='Отчистить поля', width=15)
        lang_button.configure(text='EN')
        copy_login_button.configure(text='Копировать')
        copy_password_button.configure(text='Копировать')
        open_site_button.configure(text='Открыть')

        changed += 1
    elif changed >= 1:
        my_tree.heading("Name", text="Name")
        my_tree.heading("Login", text="Login")
        my_tree.heading("Password", text="Password")
        my_tree.heading("Link", text="Link")

        data_frame.configure(text='Record')

        name_label.configure(text='Name')
        password_label.configure(text='login')
        login_label.configure(text='Password')
        link_label.configure(text='Link')

        button_frame.configure(text='Commands')
        danger_frame.configure(text='Deletion')

        update_button.configure(text='Update record')
        add_button.configure(text='Add record')
        remove_one_button.configure(text='Remove one record')
        remove_many_button.configure(text='Remove many records')
        remove_all_button.configure(text='Remove all records')
        move_up_button.configure(text='Move up record')
        move_down_button.configure(text='Move down record')
        clear_button.configure(text='Clear')
        lang_button.configure(text='RU')
        copy_login_button.configure(text='Copy')
        copy_password_button.configure(text='Copy')
        open_site_button.configure(text='Open')

        changed = 0




button_frame = LabelFrame(root, text="Commands")
button_frame.pack(fill="x", expand="yes", padx=20)

update_button = Button(button_frame, text='Update record', command=update, width=12)
update_button.grid(row=0, column=1, padx=10, pady=10)

add_button = Button(button_frame, text='Add record', width=10, command=add)
add_button.grid(row=0, column=0, padx=10, pady=10)

# deletion frame
danger_frame = LabelFrame(root, text="Deletion")
danger_frame.pack(fill="x", expand="yes", padx=20)

remove_all_button = Button(danger_frame, text='Remove all records', command=remove_all, width=20)
remove_all_button.grid(row=0, column=2, padx=10, pady=10)

remove_one_button = Button(danger_frame, text='Remove one record', command=remove_one, width=20)
remove_one_button.grid(row=0, column=0, padx=10, pady=10)

remove_many_button = Button(danger_frame, text='Remove many records', command=remove_many, width=25)
remove_many_button.grid(row=0, column=1, padx=10, pady=10)
# ----

move_up_button = Button(button_frame, text='Move up record', command=up, width=15)
move_up_button.grid(row=0, column=2, padx=10, pady=10)

move_down_button = Button(button_frame, text='Move down record', command=down, width=15)
move_down_button.grid(row=0, column=3, padx=10, pady=10)

clear_button = Button(button_frame, text='Clear', command=clear_entries, width=15)
clear_button.grid(row=0, column=4, padx=10, pady=10)

lang_button = Button(button_frame, text='RU', command=lang_change_ru, width=5)
lang_button.grid(row=0, column=5, padx=10, pady=10)

copy_login_button = Button(data_frame, text='Copy', width=15, command=copy_login)
copy_login_button.grid(row=2, column=3, padx=10, pady=10)

copy_password_button = Button(data_frame, text='Copy', width=15, command=copy_password)
copy_password_button.grid(row=2, column=5, padx=10, pady=10)

open_site_button = Button(data_frame, text='Open', width=15, command=open_link)
open_site_button.grid(row=2, column=7, padx=10, pady=10)

# Bind the treeview
my_tree.bind("<ButtonRelease-1>", select_record)

query_database()

root.mainloop()