import csv
import os
import threading



"""
Author: Loggan April
"""


FILE_NAME = "module_assessment_grades 1 (2).csv"

# ensures that the csv file exists otherwise creates the file with the respective headings
def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME,"w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Student_No",
                "Name",
                "Surname",
                "Module",
                "Quiz(10%)",
                "Project(20%)",
                "Final_Exam(50%)",
                "Practical(20%)",
                "Overall Grade"
            ])

# retrieves user information and then stores it in the csv file
def save_student(student):
    with open(FILE_NAME,"a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                student["student_No"],
                student["name"],
                student["surname"],
                student["module"],
                student["Quiz(10%)"],
                student["Project(20%)"],
                student["Final_Exam(50%)"],
                student["Practical(20%)"],
                student["Overall_Grade"]
            ])

# reads the csv file and loads all students into a list
def load_students():
    # holds all the student information retireved from the csv file
    students = []
    try:
        # opens and reads the file
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)
            #reads the file row by row
            for row in reader:
                # adds each row of information to the student list
                students.append(row)
    #throws an error if the file is not found
    except FileNotFoundError:
        return []
    
    return students

def load_students_async(callback):
    # Load students in a background thread
    def run():
        students = load_students()
        callback(students)
    thread = threading.Thread(target=run, daemon=True)
    thread.start()

def search_student(student_no):
    with open(FILE_NAME, "r",newline="") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if row[0] == student_no:
                return row

    return None

def delete_student(student_no):
    # Remove from CSV
    rows = []

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows.append(header)

        for row in reader:
            if row[0] != student_no:
                rows.append(row)

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def update_student(student_no, updated_row):
    rows = []

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows.append(header)

        for row in reader:
            if row[0] == student_no:
                rows.append(updated_row)
            else:
                rows.append(row)
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)


