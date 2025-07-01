import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Function to insert data
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

# GUI window setup
root = tk.Tk()
root.title("Student Entry Form")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Labels and Entries
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

# Submit button
tk.Button(root, text="Add Student", command=insert_data, bg="#4CAF50", fg="white").grid(row=5, column=1, pady=20)

root.mainloop()
