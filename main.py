from tkinter import *
from tkinter import messagebox
import sqlite3
from dpi import set_dpi

root = Tk()
root.title("ASWL traceability record")
root.geometry("700x300")
root.resizable(False, False)
root.iconbitmap('SoftLan.ico')

set_dpi()

# Create a database
conn = sqlite3.connect('ASWL.db')

# Create a cursor
c = conn.cursor()

# Create table
# c.execute(""" CREATE TABLE traceability (
#                     topscreen_id text,
#                     eol_id text
#                     )""")

# commit changes
conn.commit()

# Close connection
conn.close()


def save_condition():
    x = "11111111111111111111111"
    e1 = e1_label1.get()
    e2 = e2_label2.get()

    if (e1 != "" and e2 != "") and (len(e1) == len(x) and len(e2) == len(x)):
        submit()
    elif (e1 == "" or e2 == "") or (e1 == "" and e2 == "") or (e1 != "" and e2 == "") or (e1 == "" and e2 != ""):
        messagebox.showinfo("Atentie!", "Toate campurile trebuie completate!")
    else:
        messagebox.showinfo("Atentie!", "Scaneaza un cod valid de 23 de caractere!")



def submit():
    # Create a database / connect
    conn = sqlite3.connect('ASWL.db')

    # Create a cursor
    c = conn.cursor()

    # Insert in DB

    c.execute("INSERT INTO  traceability VALUES (:topscreen_id, :eol_id)",
              {
                  'topscreen_id': e1_label1.get(),
                  'eol_id': e2_label2.get()
              })

    # commit changes
    conn.commit()

    # Close connection
    conn.close()

    e1_label1.delete(0, 'end')
    e2_label2.delete(0, 'end')


def export():
    with open("ASWL.csv", "w") as aswl:
        aswl.write("    Topscreen ID     " + " | " "         EOL ID        \n")

    conn = sqlite3.connect('ASWL.db')

    # Create a cursor
    c = conn.cursor()

    # Create query
    c.execute("SELECT * FROM traceability")
    records = c.fetchall()

    for record in records:
        exp_first = record[0]
        exp_second = record[1]

        with open("ASWL.csv", "a") as aswl:
            aswl.writelines(exp_first + " | " + f"{exp_second}\n")
    messagebox.showinfo("Atentie!", "Fisier exportat!")
    exit()

    # commit changes
    conn.commit()

    # Close connection
    conn.close()


def check():
    top = Toplevel()
    top.geometry("750x200")
    top.title("ASWL Traceability Checking")
    top.iconbitmap('SoftLan.ico')

    def dbSearch():

        Label(top)
        e4 = Label(top, text="        Id-ul scanat nu exista.             ", font=("Arial", 15))
        e4.grid(row=1, column=3, columnspan=2, sticky="W")

        current = e3_label4.get()

        # Create a database
        conn = sqlite3.connect('ASWL.db')

        # Create a cursor
        c = conn.cursor()

        # Create query
        c.execute("SELECT * FROM traceability")
        records = c.fetchall()
        for record in records:
            rec_prim = record[0]
            rec_sec = record[1]
            if current == rec_prim:
                e4.config(text=f"{rec_sec}")

        # commit changes
        conn.commit()

        # Close connection
        conn.close()

        frame4 = LabelFrame(top, padx=30)
        frame4.grid(row=1, column=2, padx=30)

    myLabel4 = Label(top, text="Scanati topscreen-ul", font=("Arial", 15), pady=5, padx=10)
    myLabel5 = Label(top, text="             ", font=("Arial", 15), pady=10, padx=10)

    e3_label4 = Entry(top, width=25, borderwidth=5)
    e3_label4.grid(row=1, column=1)

    frame3 = LabelFrame(top).grid(row=0, columnspan=5, padx=10, pady=20)

    search_button = Button(top, text="Search", font=("Arial", 10, "bold"), command=dbSearch).grid(row=3, column=1,
                                                                                                  ipadx=15, ipady=7)
    quit_button = Button(top, text="Exit", font=("Arial", 10,), command=top.destroy).grid(row=3, column=0, ipadx=15,
                                                                                          ipady=7)

    myLabel4.grid(row=1, column=0)
    myLabel5.grid(row=2, column=0)


# Create labels on main window

myLabel1 = Label(root, text="Scanati topscreen-ul", font=("Arial", 15), pady=5, padx=10)
myLabel2 = Label(root, text="Scanati eticheta EOLT", font=("Arial", 15), pady=25, padx=10)
myLabel3 = Label(root, text="             ", font=("Arial", 15), pady=10, padx=10)
myLabel6 = Label(root, text="polycontact", font=("Arial", 18, 'bold'), fg="#0261A5")

# Create entry on main window

e1_label1 = Entry(root, width=28, borderwidth=5)
e1_label1.grid(row=1, column=1)
e2_label2 = Entry(root, width=28, borderwidth=5)
e2_label2.grid(row=2, column=1)

# Create button on main window

save_button = Button(root, text="Save", font=("Arial", 10, "bold"), command=save_condition).grid(row=4, column=1,
                                                                                                 ipadx=15,
                                                                                                 ipady=7)
quit_button = Button(root, text="Exit program", font=("Arial", 10,), command=root.quit).grid(row=4, column=0, ipadx=10,
                                                                                             pady=7)

# Create frame on main window

frame1 = LabelFrame(root, text="Frame", padx=10, pady=20).grid(row=3, columnspan=5, padx=10, pady=20)
frame2 = LabelFrame(root, text="Frame", padx=10, pady=30).grid(row=0, column=2, padx=10, pady=30)

get_button = Button(root, text="Traceability check", font=("Arial", 10), command=check).grid(row=4, column=2, ipadx=17,
                                                                                             ipady=7)
report_button = Button(root, text="Export csv", font=("Arial", 10), command=export).grid(row=4, column=4, ipadx=15,
                                                                                         ipady=4)

myLabel1.grid(row=1, column=0)
myLabel2.grid(row=2, column=0)
myLabel3.grid(row=3, column=0)
myLabel6.grid(row=0, column=4)

root.mainloop()

# Poly Color = #0261A5
