import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="student",
    port=3307  # use 3306 if you're on default port
)

cursor = db.cursor()

# Input from user
name = input("Enter student name: ")
email = input("Enter student email: ")
course = input("Enter student course: ")
gender = input("Enter gender (Male/Female): ")

# SQL query
query = "INSERT INTO student_data (name, email, course, gender) VALUES (%s, %s, %s, %s)"
values = (name, email, course, gender)

# Execute query
try:
    cursor.execute(query, values)
    db.commit()
    print("✅ Student record inserted successfully!")
except Exception as e:
    print("❌ Error:", e)

cursor.close()
db.close()
