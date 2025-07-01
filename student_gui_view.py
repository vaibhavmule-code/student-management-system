import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def fetch_records():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="student",
            port=3307
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM student_data")
        records = cursor.fetchall()
        db.close()
        return records
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to fetch data.\n{e}")
        return []

def show_students():
    records = fetch_records()

    if not records:
        return

    view_window = tk.Toplevel()
    view_window.title("Student Records")
    view_window.geometry("700x300")
    
    columns = ("ID", "Name", "Email", "Course", "Gender")
    tree = ttk.Treeview(view_window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.W, width=120)

    for row in records:
        tree.insert("", tk.END, values=row)

    tree.pack(expand=True, fill="both")

# Create main window with just one button
root = tk.Tk()
root.title("View Students GUI")
root.geometry("300x150")

tk.Button(root, text="View Students", command=show_students, bg="#2196F3", fg="white", padx=20, pady=10).pack(pady=40)

root.mainloop()
