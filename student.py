import sqlite3

# --- MISSING UTILITY FUNCTIONS ADDED HERE ---

def get_connection():
    """Creates and returns a connection to the SQLite database."""
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    """Creates the students table if it doesn't exist yet."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                roll_no TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                course TEXT NOT NULL
            )
        """)


def print_students(students):
    """Prints all students with uniform column spacing."""
    rows = []

    for student in students:
        rows.append({
            "roll_no": str(student["roll_no"]),
            "name": str(student["name"]),
            "age": "" if student["age"] is None else str(student["age"]),
            "course": str(student["course"]),
        })

    headers = {
        "roll_no": "Roll No",
        "name": "Name",
        "age": "Age",
        "course": "Course",
    }

    roll_width = max(len(headers["roll_no"]), max(len(row["roll_no"]) for row in rows))
    name_width = max(len(headers["name"]), max(len(row["name"]) for row in rows))
    age_width = max(len(headers["age"]), max(len(row["age"]) for row in rows))
    course_width = max(len(headers["course"]), max(len(row["course"]) for row in rows))

    print(
        f"{headers['roll_no']:<{roll_width}}    "
        f"{headers['name']:<{name_width}}    "
        f"{headers['age']:<{age_width}}    "
        f"{headers['course']:<{course_width}}"
    )

    total_width = roll_width + name_width + age_width + course_width + 12
    print("-" * total_width)

    for row in rows:
        print(
            f"{row['roll_no']:<{roll_width}}    "
            f"{row['name']:<{name_width}}    "
            f"{row['age']:<{age_width}}    "
            f"{row['course']:<{course_width}}"
        )


# --- FIXED YOUR FUNCTIONS BELOW ---

def add_student():
    roll_no = input("Enter Roll No: ").strip()
    name = input("Enter Name: ").strip()
    age_text = input("Enter Age: ").strip()
    course = input("Enter Course: ").strip()

    age = int(age_text) if age_text.isdigit() else None

    student = {
        "roll_no": roll_no,
        "name": name,
        "age": age,
        "course": course,
    }

    if not student["roll_no"] or not student["name"] or not student["course"]:
        print("Roll No, Name, and Course cannot be empty.")
        return

    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO students (roll_no, name, age, course)
                VALUES (:roll_no, :name, :age, :course)
                """,
                student,
            )
        print("Student added and saved in backend.")
    except sqlite3.IntegrityError:
        print("A student with this Roll No already exists.")


def search_student():
    search_text = input("Enter Roll No or Name to search: ").strip()

    with get_connection() as connection:
        students = connection.execute(
            """
            SELECT roll_no, name, age, course
            FROM students
            WHERE roll_no = ? OR name LIKE ?
            ORDER BY roll_no
            """,
            (search_text, f"%{search_text}%"),
        ).fetchall()

    if not students:
        print("Student not found.")
        return

    print_students(students)


def update_student():
    roll_no = input("Enter Roll No to update: ").strip()

    with get_connection() as connection:
        old_student = connection.execute(
            "SELECT roll_no, name, age, course FROM students WHERE roll_no = ?",
            (roll_no,),
        ).fetchone()

    if old_student is None:
        print("Student not found.")
        return

    print("Press Enter to keep the old value.")
    new_name = input(f"Enter new Name ({old_student['name']}): ").strip()
    new_age_text = input(f"Enter new Age ({old_student['age']}): ").strip()
    new_course = input(f"Enter new Course ({old_student['course']}): ").strip()

    student = {
        "roll_no": roll_no,
        "name": new_name or old_student["name"],
        "age": int(new_age_text) if new_age_text.isdigit() else old_student["age"],
        "course": new_course or old_student["course"],
    }

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE students
            SET name = :name, age = :age, course = :course
            WHERE roll_no = :roll_no
            """,
            student,
        )

    print("Student updated in backend.")


def delete_student():
    roll_no = input("Enter Roll No to delete: ").strip()

    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM students WHERE roll_no = ?",
            (roll_no,),
        )

    if cursor.rowcount == 0:
        print("Student not found.")
    else:
        print("Student deleted from backend.")


def view_students():
    with get_connection() as connection:
        students = connection.execute(
            "SELECT roll_no, name, age, course FROM students ORDER BY roll_no"
        ).fetchall()

    if not students:
        print("No student records saved yet.")
        return

    print("\nAll Students")
    print_students(students)


def main():
    create_table()

    while True:
        print("\nStudent Management System")
        print("Backend: SQLite database")
        print("1. Add Student")
        print("2. Search Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. View All Students")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            search_student()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            view_students()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()