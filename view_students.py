import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="student",
    port=3307
)

cursor = db.cursor()

# SQL query to select all records
query = "SELECT * FROM student_data"

try:
    cursor.execute(query)
    records = cursor.fetchall()

    if records:
        print("\n📋 Student Records:")
        print("-" * 75)
        print("{:<5} {:<20} {:<25} {:<15} {:<10}".format("ID", "Name", "Email", "Course", "Gender"))
        print("-" * 75)

        for row in records:
            id = row[0] if row[0] is not None else "-"
            name = row[1] if row[1] is not None else "-"
            email = row[2] if row[2] is not None else "-"
            course = row[3] if row[3] is not None else "-"
            gender = row[4] if row[4] is not None else "-"

            print("{:<5} {:<20} {:<25} {:<15} {:<10}".format(id, name, email, course, gender))

        print("-" * 75)
    else:
        print("⚠️ No student records found.")

except Exception as e:
    print("❌ Error:", e)

cursor.close()
db.close()
