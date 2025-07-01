import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Insert student
def insert_data():
    name = entry_name.get()
    email = entry_email.get()
    course = entry_course.get()
    gender = gender_var.get()

    if not name or not email or not course or not gender:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="student",
            port=3307
        )
        cursor = db.cursor()
        query = "INSERT INTO student_data (name, email, course, gender) VALUES (%s, %s, %s, %s)"
        values = (name, email, course, gender)
        cursor.execute(query, values)
        db.commit()
        messagebox.showinfo("Success", "Student record inserted successfully!")
        entry_name.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_course.delete(0, tk.END)
        gender_var.set(None)
        cursor.close()
        db.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to insert data.\n{e}")

# View records
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

# Update/Delete window
def update_delete_window():
    win = tk.Toplevel()
    win.title("Update/Delete Student")
    win.geometry("400x350")

    tk.Label(win, text="Student ID").pack(pady=5)
    id_entry = tk.Entry(win)
    id_entry.pack()

    tk.Label(win, text="Name").pack(pady=5)
    name_entry = tk.Entry(win)
    name_entry.pack()

    tk.Label(win, text="Email").pack(pady=5)
    email_entry = tk.Entry(win)
    email_entry.pack()

    tk.Label(win, text="Course").pack(pady=5)
    course_entry = tk.Entry(win)
    course_entry.pack()

    tk.Label(win, text="Gender").pack(pady=5)
    gender_var = tk.StringVar()
    tk.Radiobutton(win, text="Male", variable=gender_var, value="Male").pack()
    tk.Radiobutton(win, text="Female", variable=gender_var, value="Female").pack()

    def update_student():
        if not id_entry.get().strip():
            messagebox.showwarning("Missing ID", "Please enter Student ID to update.")
            return

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="student",
                port=3307
            )
            cursor = db.cursor()
            cursor.execute("SELECT * FROM student_data WHERE id = %s", (id_entry.get(),))
            if cursor.fetchone() is None:
                messagebox.showerror("Not Found", "No student found with that ID.")
                db.close()
                return

            query = """UPDATE student_data 
                       SET name=%s, email=%s, course=%s, gender=%s 
                       WHERE id=%s"""
            values = (
                name_entry.get(),
                email_entry.get(),
                course_entry.get(),
                gender_var.get(),
                id_entry.get()
            )
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Success", "Record Updated!")
            db.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_student():
        if not id_entry.get().strip():
            messagebox.showwarning("Missing ID", "Please enter Student ID to delete.")
            return

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="student",
                port=3307
            )
            cursor = db.cursor()
            cursor.execute("SELECT * FROM student_data WHERE id = %s", (id_entry.get(),))
            if cursor.fetchone() is None:
                messagebox.showerror("Not Found", "No student found with that ID.")
                db.close()
                return

            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?")
            if confirm:
                cursor.execute("DELETE FROM student_data WHERE id = %s", (id_entry.get(),))
                db.commit()
                messagebox.showinfo("Deleted", "Student record deleted.")
            db.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Update", command=update_student, bg="orange", fg="white", width=15).pack(pady=10)
    tk.Button(win, text="Delete", command=delete_student, bg="red", fg="white", width=15).pack()

# GUI setup
root = tk.Tk()
root.title("Student Management System")
root.geometry("400x420")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_name = tk.Entry(root, width=30)
entry_name.grid(row=0, column=1, padx=10)

tk.Label(root, text="Email").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_email = tk.Entry(root, width=30)
entry_email.grid(row=1, column=1, padx=10)

tk.Label(root, text="Course").grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_course = tk.Entry(root, width=30)
entry_course.grid(row=2, column=1, padx=10)

tk.Label(root, text="Gender").grid(row=3, column=0, padx=10, pady=10, sticky="w")
gender_var = tk.StringVar()
tk.Radiobutton(root, text="Male", variable=gender_var, value="Male").grid(row=3, column=1, sticky="w")
tk.Radiobutton(root, text="Female", variable=gender_var, value="Female").grid(row=4, column=1, sticky="w")

tk.Button(root, text="Add Student", command=insert_data, bg="#4CAF50", fg="white", width=20).grid(row=5, column=1, pady=10)
tk.Button(root, text="View Students", command=show_students, bg="#2196F3", fg="white", width=20).grid(row=6, column=1)
tk.Button(root, text="Update/Delete", command=update_delete_window, bg="#9C27B0", fg="white", width=20).grid(row=7, column=1, pady=10)

root.mainloop()
