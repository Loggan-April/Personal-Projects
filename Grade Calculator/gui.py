import tkinter as tk
import pywinstyles
from tkinter import ttk
from tkinter import messagebox
from data_module import save_student
from data_module import load_students_async
from data_module import search_student
from data_module import delete_student
from data_module import update_student
from grade_module import overall_mark



"""
Author: Loggan April
"""


root = tk.Tk()
root.title("Eduvos Student Grade Calculator")
root.geometry("700x500")
pywinstyles.apply_style(root, "dark")
pywinstyles.change_header_color(root, "#0015FF")
FILE_NAME = "module_assessment_grades 1 (2).csv"

#------------- FUNCTIONS ----------------------

# function to hide all frame to ensure none of them clash with each other
def hide_all_pages():
    home_page.pack_forget()
    second_page.pack_forget()
    third_page.pack_forget()
    fourth_page.pack_forget()

# function to close the gui
def close_app():
    root.destroy()

# fucntion to show the main page
def show_home_page():
    hide_all_pages()
    root.title("Eduvos Student Grade Calculator")
    root.geometry("700x500")
    pywinstyles.apply_style(root, "dark")
    pywinstyles.change_header_color(root, "#0015FF")
    home_page.pack(fill="both", expand=True)

# function to show the page for user to enter their details
def show_second_page():
    hide_all_pages()
    root.title("Capture Student Marks")
    root.geometry("500x500")
    second_page.pack(fill="both", expand=True)
    pywinstyles.apply_style(root, "dark")
    pywinstyles.change_header_color(root, "#C9C9C9")
    
# function to show all the users in the csv file that can be deleted
def show_third_page():
    hide_all_pages()
    root.title("View / Delete Records")
    root.geometry("1000x550")
    third_page.pack(fill="both", expand=True)
    pywinstyles.apply_style(root, "dark")
    pywinstyles.change_header_color(root, "#C30000")
    load_students_gui()

def show_fourth_page():
    hide_all_pages()
    root.title("Search & Update Marks")
    root.geometry("900x500")
    pywinstyles.apply_style(root, "dark")
    pywinstyles.change_header_color(root, "#26FF00")
    fourth_page.pack(fill="both", expand=True)
    top_frame.pack(fill="both")    
    table_frame.pack(fill="both", expand=True)
    bottom_frame.pack(fill="both")

def search_student_gui():
    student_no = searchStudent_entry.get().strip()
    student = search_student(student_no)

    if student:
        update_display.insert("", "end", values=student)
    else:
        messagebox.showinfo(
            "Not found",
            "Student not found",
        )

def save_data_gui():
    
    #overall gets the user's marks and then passes it to the overall_mark function in the grade_module file
    overall = overall_mark(
        quiz_entry.get(),
        project_entry.get(),
        exam_entry.get(),
        practical_entry.get()
    )
    
    # try statement gets all the user's information and then passes it to the save_student function in the data_module file
    try:
        student = {
            "student_No": studentNo_entry.get(),
            "name": name_entry.get(),
            "surname": surname_entry.get(),
            "module": modules.get(),
            "Quiz(10%)": quiz_entry.get(),
            "Project(20%)": project_entry.get(),
            "Final_Exam(50%)": exam_entry.get(),
            "Practical(20%)": practical_entry.get(),
            "Overall_Grade": overall
            
        }

        save_student(student)
    except ValueError:
        messagebox.showreror("Error", "Enter valid credentials")
    
    
    result_label = tk.Label(
    second_page,
    text=f"Saved. Overall Grade: {overall:.1f}",
    fg="blue",
    font=("Ariel", 9, "bold")
    )
    result_label.grid(row=9,column=1,columnspan=2)

    messagebox.showinfo("Success", f"{name_entry.get()} has successfully been added")

def load_students_gui():
    #removes everything from the table
    students_display.delete(*students_display.get_children())

    #inserts all data from the csv file into the table
    def on_loaded(rows):
        for row in rows:
            students_display.insert("", "end", values=row)
    load_students_async(on_loaded)

def delete_student_gui():
    selected_student = students_display.selection()

    # displays error if a student isn't selected
    if not selected_student:
        messagebox.showerror("Error", "Please select a student to delete", colour="red")
        return
    
    
    # Asks user to confirm their decision
    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?",
    )

    if not confirm:
        return

    # Get selected row values
    values = students_display.item(selected_student)["values"]
    student_no_to_delete = values[0]

    # Remove from Treeview
    students_display.delete(selected_student)
    delete_student(student_no_to_delete)
    messagebox.showinfo("Success", "Student has been deleted")

def update_student_gui():
    # gets the selected student to update
    selected = update_display.selection()
    if not selected:
        messagebox.showerror("Error", "Search and select a student first")
        return
    values = list(update_display.item(selected)["values"])
    student_no = values[0]
    new_mark = new_mark_entry.get()

    # If no new mark is entered then an error will popup
    if not new_mark:
        messagebox.showerror("Error", "Enter a new mark")
        return
    
    col_map = {
        "Quiz(10%)": 4,
        "Project(20%)": 5,
        "Final Exam(50%)": 6,
        "Practical(20%)": 7,
    }
    field = assessment.get()
    values[col_map[field]] = new_mark

    #Recalculate overall grade
    values[8] = overall_mark(values[4], values[5], values[6], values[7])

    # calls the function from data_module to update the list of students in the csv file
    update_student(student_no, values)

    #Refresh the display
    update_display.delete(*update_display.get_children())
    update_display.insert("", "end", values=values)

    messagebox.showinfo("Success", f"{assessment.get()} updated successfully")

#----------------- FRAMES -----------------

# All the frames that will be displayed according to their respective buttons
home_page = tk.Frame(root)
second_page = tk.Frame(root)
third_page = tk.Frame(root)
fourth_page = tk.Frame(root) 
top_frame = tk.Frame(fourth_page)
table_frame = tk.Frame(fourth_page)
bottom_frame = tk.Frame(fourth_page)

# Displays the home frame
home_page.pack(fill="both", expand=True)



#------------ HOME PAGE ------------------------

# title label for the home page
title = tk.Label(
    home_page,
    text="🎓 Eduvos Student Grade Calculator\n(2026 Final Project 2)",
    fg ="#00406C",
    font=("Ariel", 22, "bold")
)
title.pack()

# sub title for the main page
sub_title = tk.Label(
    home_page,
    text="Manage Students Marks Easily",
    fg = "#808080",
    font=("Ariel", 13)
)
sub_title.pack(pady = 30)



#button to capture new details
capture_btn = tk.Button(
    home_page,
    text ="Capture Student Marks",
    command = show_second_page,
    bg = "dark green",
    fg = "black",
    width = 25,
    height=2
)
capture_btn.pack()

#button to view/delete a specific record
View_btn = tk.Button(
    home_page,
    text ="View / Delete Records",
    command=show_third_page,
    bg = "light blue",
    fg = "black",
    width = 25,
    height=2
)
View_btn.pack(pady = 10)

#button to search/update for a specific record
Search_btn = tk.Button(
    home_page,
    text ="Search / Update Records",
    command = show_fourth_page,
    bg ="orange",
    fg = "black",
    width = 25,
    height=2,
    
)
Search_btn.pack()

# button to close the program/gui
Exit_btn = tk.Button(
    home_page,
    text ="Close Application",
    command=close_app,
    bg = "red",
    fg = "black",
    width = 25,
    height=2
    
)
Exit_btn.pack(pady = 10)


#----------------- SECOND PAGE -------------------------


# title to instruct the user to enter their student No
tk.Label(second_page, text="Studen No: ").grid(row=0,column=1,pady=20 , padx=30, sticky="w")
studentNo_entry = tk.Entry(second_page, width=26)
studentNo_entry.grid(row=0,column=2, padx=30)

# title to instruct the user to enter their Name
tk.Label(second_page, text="Name: ").grid(row=1,column=1, pady=5, padx=30, sticky="w")
name_entry = tk.Entry(second_page, width=26)
name_entry.grid(row=1,column=2, padx=30)

# title to instruct the user to enter their Surname
tk.Label(second_page, text="Surname: ").grid(row=2,column=1,pady=5 , padx=30, sticky="w")
surname_entry = tk.Entry(second_page, width=27)
surname_entry.grid(row=2,column=2, padx=30)

# title to instruct the user to select their Module
tk.Label(second_page, text="Module: ").grid(row=3,column=1,pady=5 , padx=30, sticky="w")
modules = ttk.Combobox(second_page, width=26)
modules.grid(row=3,column=2, padx=30)

# combobox to hold all the modules
modules["values"] = (
    "C++ Programming",
    "Database Systems",
    "Java Programming",
    "Python Programming",
    "Networking"
)
modules.current(0)

# title to instruct the user to enter their quiz mark
tk.Label(second_page, text="Quiz(10%): ").grid(row=4,column=1,pady=5 , padx=30, sticky="w")
quiz_entry = tk.Entry(second_page, width=26)
quiz_entry.grid(row=4,column=2, padx=30)

# title to instruct the user to enter their project mark
tk.Label(second_page, text="Project(20%): ").grid(row=5,column=1,pady=5 , padx=30, sticky="w")
project_entry = tk.Entry(second_page, width=26)
project_entry.grid(row=5,column=2, padx=30)

# title to instruct the user to enter their final exam mark
tk.Label(second_page, text="Final Exam(50%): ").grid(row=6,column=1,pady=5 , padx=30, sticky="w")
exam_entry = tk.Entry(second_page, width=26)
exam_entry.grid(row=6,column=2, padx=10)

# title to instruct the user to enter their practical mark
tk.Label(second_page, text="Practical(20%): ").grid(row=7,column=1,pady=5 , padx=30, sticky="w")
practical_entry = tk.Entry(second_page, width=26)
practical_entry.grid(row=7,column=2, padx=30)

# button to save the user's information
Save_btn = tk.Button(
    second_page,
    text ="Save",
    command=save_data_gui,
    bg = "light green",
    fg = "black",
    width = 20,
    height=0
    
)
Save_btn.grid(row=8,column=1,columnspan=2,pady = 12, padx=20)

Return_btn = tk.Button(
    second_page,
    text ="Return",
    command=show_home_page,
    bg = "light blue",
    fg = "black",
    width = 20,
    height=0
    
)
Return_btn.grid(row=10,column=1,columnspan=2,pady = 12, padx=20)


#--------------------- THIRD PAGE ------------------------
# container to adjust the height and width of the table
display_container = tk.Frame(third_page, height=300, width=200)
display_container.pack(fill="x", pady=(1,0),padx=5)
display_container.pack_propagate(False)

# table with its respective columns
students_display = ttk.Treeview(
    display_container,
    columns=(
        "Student No",
        "Name",
        "Surname",
        "Module",
        "Quiz(10%)",
        "Project(20%)",
        "Final Exam(50%)",
        "Practical(20%)",
        "Overall Grade"
    ),
    show="headings"
)
students_display.pack(fill="x",expand=True)

# headings for each column and the column heading
students_display.heading("Student No", text="Student No")
students_display.heading("Name", text="Name")
students_display.heading("Surname", text="Surname")
students_display.heading("Module", text="Module")
students_display.heading("Quiz(10%)", text="Quiz (10%)")
students_display.heading("Project(20%)", text="Project (20%)")
students_display.heading("Final Exam(50%)", text="Final Exam (50%)")
students_display.heading("Practical(20%)", text="Practical (20%)")
students_display.heading("Overall Grade", text="Overall Grade")

# adjusts the width of each column to a desired size
students_display.column("Student No", width=50)
students_display.column("Name", width=40)
students_display.column("Surname", width=40)
students_display.column("Module", width=65)
students_display.column("Quiz(10%)", width=30)
students_display.column("Project(20%)", width=40)
students_display.column("Final Exam(50%)", width=44)
students_display.column("Practical(20%)", width=50)
students_display.column("Overall Grade", width=40)

# delete button to delete a student from the table and csv file calling the delete_student_gui function
Delete_btn = tk.Button(
    third_page,
    text ="Delete",
    command = delete_student_gui, 
    bg = "light pink",
    fg = "black",
    width = 5,
    height=0
)
Delete_btn.pack(side ="right", padx=10)

Return_btn = tk.Button(
    third_page,
    text ="Return",
    command=show_home_page,
    bg = "light blue",
    fg = "black",
    width = 5,
    height=0
    
)
Return_btn.pack(side="right",padx=10)


#--------------- FOURTH PAGE --------------

# label to instruct user to search by the student no
tk.Label(top_frame, text="Search by Student No: ",font=("Arial",12)).grid(row=0,column=1,padx=11, sticky="e")
# entry field  to enter the student no
searchStudent_entry = tk.Entry(top_frame,width=25)
searchStudent_entry.grid(row=0,column=2,padx=100)

# search button to retieve all the information by student no
search_btn = tk.Button(
    top_frame,
    text= "Search",
    command = search_student_gui,
    bg = "light blue",
    fg = "black",
    width = 5,
    height = 0
    )
search_btn.grid(row=0,column=3,padx=20)

# creates a new frame 'window' to keep the table inside of
update_container = tk.Frame(table_frame, height=300, width=200)
update_container.pack(fill="x", pady=(0,0))
update_container.pack_propagate(False)  # disables the frame from being resized

# table to display all the student information
update_display = ttk.Treeview(
    update_container,
    columns=(
        "Student No",
        "Name",
        "Surname",
        "Module",
        "Quiz(10%)",
        "Project(20%)",
        "Final Exam(50%)",
        "Practical(20%)",
        "Overall Grade"
    ),
    show="headings"
)
update_display.pack(fill="x",expand=True, padx = 50)

# heading for each column
update_display.heading("Student No", text="Student No")
update_display.heading("Name", text="Name")
update_display.heading("Surname", text="Surname")
update_display.heading("Module", text="Module")
update_display.heading("Quiz(10%)", text="Quiz (10%)")
update_display.heading("Project(20%)", text="Project (20%)")
update_display.heading("Final Exam(50%)", text="Final Exam (50%)")
update_display.heading("Practical(20%)", text="Practical (20%)")
update_display.heading("Overall Grade", text="Overall Grade")

# sets the width of each column
update_display.column("Student No", width=50)
update_display.column("Name", width=40)
update_display.column("Surname", width=40)
update_display.column("Module", width=65)
update_display.column("Quiz(10%)", width=30)
update_display.column("Project(20%)", width=40)
update_display.column("Final Exam(50%)", width=44)
update_display.column("Practical(20%)", width=50)
update_display.column("Overall Grade", width=40)

# label instructs user to select an assessment to update
tk.Label(bottom_frame, text="Select Assessment: ", font=("Arial",13)).grid(row=4,column=1, sticky="w")

# combo box to hold all the assessments that can be updates
assessment = ttk.Combobox(bottom_frame)
assessment.grid(row=4,column=2, padx=100)

# the assessments inside of the combo box
assessment["values"] = (
    "Quiz(10%)",
    "Project(20%)",
    "Final Exam(50%)",
    "Practical(20%)",
)
# sets the first assessment inside the combo box to be selected when program is run 
assessment.current(0)

# lable to instruct the user to enter their new mark
tk.Label(bottom_frame, text="New Mark: ", font=("Arial",13)).grid(row=5,column=1, sticky="w")

# entry field for the user to enter their new mark
new_mark_entry = tk.Entry(bottom_frame, width=23)
new_mark_entry.grid(row=5,column=2, pady=5, padx = 100)

# update button to complete the update 
Update_btn = tk.Button(
    bottom_frame,
    text ="Update Mark",
    command=update_student_gui,
    bg = "light green",
    fg = "black",
    width = 20,
    height=0
    
)
Update_btn.grid(row=6,column=1,padx=100, pady=10)

Return_btn = tk.Button(
    bottom_frame,
    text ="Return",
    command=show_home_page,
    bg = "light blue",
    fg = "black",
    width = 20,
    height=0
    
)
Return_btn.grid(row=7,column=1,padx=100, pady=10)





# completes the gui frames, button, lables, and entry fields and displays the 
root.mainloop()