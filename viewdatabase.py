import sqlite3
from prettytable import PrettyTable

# Connect to the database
def connect_db():
    try:
        conn = sqlite3.connect('C:\StudentManagement\instance\database.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Function to view teachers
def view_teachers():
    conn = connect_db()
    if conn is None:
        return
    
    cursor = conn.cursor()
    
    try:
        # Fetch all teachers (table name is lowercase 'teacher')
        cursor.execute("SELECT * FROM teacher")
        teachers = cursor.fetchall()
        
        # Create a table for display
        teacher_table = PrettyTable()
        teacher_table.field_names = ["ID", "Teacher ID", "Name", "Gender", "Mobile", "Email", "Password", "Subjects"]
        
        for teacher in teachers:
            teacher_table.add_row(teacher)
        
        print("\n=== Teachers ===")
        print(teacher_table if teachers else "No teachers found.")
    except sqlite3.OperationalError as e:
        print(f"Error: {e} (Table 'teacher' may not exist yet)")
    
    conn.close()

# Function to view students
def view_students():
    conn = connect_db()
    if conn is None:
        return
    
    cursor = conn.cursor()
    
    try:
        # Fetch all students (table name is lowercase 'student')
        cursor.execute("SELECT * FROM student")
        students = cursor.fetchall()
        
        # Create a table for display
        student_table = PrettyTable()
        student_table.field_names = ["ID", "Student ID", "Name", "Age", "Gender", "Course", "Scores", "Attendance", "Password", "Email/Mobile"]
        
        for student in students:
            student_table.add_row(student)
        
        print("\n=== Students ===")
        print(student_table if students else "No students found.")
    except sqlite3.OperationalError as e:
        print(f"Error: {e} (Table 'student' may not exist yet)")
    
    conn.close()

# Main function to run the script
def main():
    print("Viewing Database Contents...")
    view_teachers()
    view_students()

if __name__ == "__main__":
    main()