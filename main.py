import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    branch TEXT,
    semester INTEGER
)
""")

conn.commit()


def add_student():
    name = input("Enter student name: ")
    age = int(input("Enter age: "))
    branch = input("Enter branch: ")
    semester = int(input("Enter semester: "))

    cursor.execute(
        "INSERT INTO students (name, age, branch, semester) VALUES (?, ?, ?, ?)",
        (name, age, branch, semester)
    )

    conn.commit()
    print("Student added successfully!")


def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        print("No students found.")
        return

    print("\n===== STUDENTS =====")

    for student in students:
        print(
            f"ID: {student[0]} | "
            f"Name: {student[1]} | "
            f"Age: {student[2]} | "
            f"Branch: {student[3]} | "
            f"Semester: {student[4]}"
        )


def search_student():
    name = input("Enter student name to search: ")

    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        ("%" + name + "%",)
    )

    students = cursor.fetchall()

    if not students:
        print("No matching students found.")
        return

    print("\n===== SEARCH RESULTS =====")

    for student in students:
        print(
            f"ID: {student[0]} | "
            f"Name: {student[1]} | "
            f"Age: {student[2]} | "
            f"Branch: {student[3]} | "
            f"Semester: {student[4]}"
        )


def update_student():
    view_students()

    try:
        student_id = int(input("\nEnter student ID to update: "))

        cursor.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        )

        student = cursor.fetchone()

        if not student:
            print("Student not found.")
            return

        name = input("Enter new name: ")
        age = int(input("Enter new age: "))
        branch = input("Enter new branch: ")
        semester = int(input("Enter new semester: "))

        cursor.execute("""
            UPDATE students
            SET name = ?, age = ?, branch = ?, semester = ?
            WHERE id = ?
        """, (name, age, branch, semester, student_id))

        conn.commit()
        print("Student updated successfully!")

    except ValueError:
        print("Please enter valid values.")


def delete_student():
    view_students()

    try:
        student_id = int(input("\nEnter student ID to delete: "))

        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        if cursor.rowcount == 0:
            print("Student not found.")
        else:
            conn.commit()
            print("Student deleted successfully!")

    except ValueError:
        print("Please enter a valid ID.")
def add_marks():
    view_students()

    try:
        student_id = int(input("\nEnter student ID: "))

        cursor.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        )

        student = cursor.fetchone()

        if not student:
            print("Student not found.")
            return

        print("\nEnter marks out of 100:")

        python = float(input("Python: "))
        maths = float(input("Maths: "))
        dsa = float(input("Data Structures: "))
        dbms = float(input("DBMS: "))

        total = python + maths + dsa + dbms
        average = total / 4

        if average >= 90:
            grade = "A+"
        elif average >= 80:
            grade = "A"
        elif average >= 70:
            grade = "B"
        elif average >= 60:
            grade = "C"
        elif average >= 50:
            grade = "D"
        else:
            grade = "F"

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS marks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                python REAL,
                maths REAL,
                dsa REAL,
                dbms REAL,
                total REAL,
                average REAL,
                grade TEXT
            )
        """)

        cursor.execute("""
            INSERT INTO marks
            (student_id, python, maths, dsa, dbms, total, average, grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id,
            python,
            maths,
            dsa,
            dbms,
            total,
            average,
            grade
        ))

        conn.commit()

        print("\nMarks added successfully!")
        print(f"Total: {total:.2f}")
        print(f"Average: {average:.2f}")
        print(f"Grade: {grade}")

    except ValueError:
        print("Please enter valid marks.")
def view_results():
    view_students()

    try:
        student_id = int(input("\nEnter student ID: "))

        cursor.execute("""
            SELECT students.name, marks.python, marks.maths,
                   marks.dsa, marks.dbms, marks.total,
                   marks.average, marks.grade
            FROM students
            JOIN marks ON students.id = marks.student_id
            WHERE students.id = ?
        """, (student_id,))

        result = cursor.fetchone()

        if not result:
            print("No marks found for this student.")
            return

        print("\n===== STUDENT RESULT =====")
        print(f"Name: {result[0]}")
        print(f"Python: {result[1]:.2f}")
        print(f"Maths: {result[2]:.2f}")
        print(f"Data Structures: {result[3]:.2f}")
        print(f"DBMS: {result[4]:.2f}")
        print(f"Total: {result[5]:.2f}")
        print(f"Average: {result[6]:.2f}")
        print(f"Grade: {result[7]}")

    except ValueError:
        print("Please enter a valid ID.")
def add_attendance():
    view_students()

    try:
        student_id = int(input("\nEnter student ID: "))

        cursor.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        )

        student = cursor.fetchone()

        if not student:
            print("Student not found.")
            return

        total_classes = int(input("Enter total classes: "))
        attended_classes = int(input("Enter attended classes: "))

        if total_classes <= 0:
            print("Total classes must be greater than 0.")
            return

        if attended_classes < 0 or attended_classes > total_classes:
            print("Invalid attendance values.")
            return

        percentage = (attended_classes / total_classes) * 100

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                total_classes INTEGER,
                attended_classes INTEGER,
                percentage REAL
            )
        """)

        cursor.execute("""
            INSERT INTO attendance
            (student_id, total_classes, attended_classes, percentage)
            VALUES (?, ?, ?, ?)
        """, (
            student_id,
            total_classes,
            attended_classes,
            percentage
        ))

        conn.commit()

        print("\nAttendance added successfully!")
        print(f"Attendance: {percentage:.2f}%")

    except ValueError:
        print("Please enter valid numbers.")
def view_attendance():
    view_students()

    try:
        student_id = int(input("\nEnter student ID: "))

        cursor.execute("""
            SELECT students.name, attendance.total_classes,
                   attendance.attended_classes, attendance.percentage
            FROM students
            JOIN attendance ON students.id = attendance.student_id
            WHERE students.id = ?
            ORDER BY attendance.id DESC
            LIMIT 1
        """, (student_id,))

        result = cursor.fetchone()

        if not result:
            print("No attendance record found.")
            return

        print("\n===== ATTENDANCE =====")
        print(f"Name: {result[0]}")
        print(f"Total Classes: {result[1]}")
        print(f"Attended Classes: {result[2]}")
        print(f"Attendance: {result[3]:.2f}%")

    except ValueError:
        print("Please enter a valid ID.")

while True:
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Add Marks")
    print("7. View Student Results")
    print("8. Add Attendance")
    print("9. View Attendance")
    print("10. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        update_student()

    elif choice == "5":
        delete_student()

    elif choice == "6":
        add_marks()

    elif choice == "7":
        view_results()

    elif choice == "8":
        add_attendance()

    elif choice == "9":
        view_attendance()

    elif choice == "10":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")

conn.close()