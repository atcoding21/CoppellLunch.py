import tkinter as tk
from tkinter import messagebox
import PyPDF2

# Path to the PDF file
PDF_FILE_PATH = r"C:\Users\Vsing\PycharmProjects\Coppell Lunch\Lunch - Sheet1.pdf"
# Read PDF file and extract text
try:
    with open(PDF_FILE_PATH, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
except Exception as e:
    messagebox.showerror("Error", f"Failed to read PDF file: {e}")

# Process student information
def process_student_information(text):
    global student_data
    student_data = {}
    # Split text by newline and process each line
    lines = text.split("\n")
    for line in lines:
        if line.strip():
            # Extract student information from each line
            student_info = line.strip().split()  # Split by spaces
            if len(student_info) == 3:
                student_data[(student_info[0], student_info[1])] = student_info[2]
            else:  # Handle case with last name
                student_name = student_info[0] + " " + student_info[1]
                student_data[(student_name, student_info[2])] = student_info[3]

# Function to handle student submission
def student_submit():
    student_id = id_entry.get()
    student_name = name_entry.get()
    lunch_type = student_data.get((student_name, student_id), None)  # Reversed order for name and ID
    if lunch_type:
        info_text = f"Student ID: {student_id}\nStudent Name: {student_name}\nLunch Type: {lunch_type}"
        lunch_type_label.config(text=info_text, fg="#FFFFFF")  # White text
    else:
        lunch_type_label.config(text="Student information not found.", fg="#FFFFFF")  # White text

# Create the main window
root = tk.Tk()
root.title("Student Lunch Type Lookup")
root.configure(bg="#000000")  # Black background

# Set window size
window_width = 600
window_height = 400

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate x and y positions for centering the window
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2

# Set window geometry
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Process student information
process_student_information(text)

# Create a frame for the main content
content_frame = tk.Frame(root, bg="#000000")  # Black background
content_frame.pack(expand=True)

# Frame for student form
student_frame = tk.Frame(content_frame, bg="#000000")  # Black background
student_frame.pack(pady=20)

# Student ID entry
tk.Label(student_frame, text="Student ID:", bg="#000000", fg="#FFFFFF", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
id_entry = tk.Entry(student_frame, bg="#FFFFFF", font=("Arial", 14))  # White background
id_entry.grid(row=0, column=1, padx=10, pady=5)

# Student Name entry
tk.Label(student_frame, text="Name:", bg="#000000", fg="#FFFFFF", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5)
name_entry = tk.Entry(student_frame, bg="#FFFFFF", font=("Arial", 14))  # White background
name_entry.grid(row=1, column=1, padx=10, pady=5)

# Button for student to submit
submit_button = tk.Button(student_frame, text="Submit", command=student_submit, bg="#FF0000", fg="#FFFFFF", font=("Arial", 14))  # Red button
submit_button.grid(row=2, columnspan=2, pady=20)

# Label to display lunch type
lunch_type_label = tk.Label(content_frame, text="", bg="#000000", fg="#FFFFFF", font=("Arial", 16))  # Black background, white text
lunch_type_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
