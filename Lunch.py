import streamlit as st
import pdfplumber

# Path to the PDF file
PDF_FILE_PATH = "Lunch - Sheet1.pdf"

# Read PDF file and extract text
def read_pdf_file(pdf_file_path):
    try:
        with pdfplumber.open(pdf_file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Failed to read PDF file: {e}")

# Process student information
def process_student_information(text):
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
    return student_data

# Function to handle student submission
def student_submit(student_data, student_id, student_name):
    lunch_type = student_data.get((student_name, student_id), None)  # Reversed order for name and ID
    if lunch_type:
        info_text = f"Student ID: {student_id}\nStudent Name: {student_name}\nLunch Type: {lunch_type}"
        st.success(info_text)
    else:
        st.warning("Student information not found.")

# Page configuration
st.set_page_config(page_title="Student Lunch Type Lookup", page_icon=":fork_and_knife:")

# Title
st.title("Student Lunch Type Lookup")

# Read PDF file and extract text
text = read_pdf_file(PDF_FILE_PATH)

# Process student information
student_data = process_student_information(text)

# Set background color and padding
st.markdown(
    """
    <style>
        .stApp {
            background-color: #000000;
            padding: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Student ID entry
student_id = st.text_input("Student ID")

# Student Name entry
student_name = st.text_input("Name")

# Button for student to submit
if st.button("Submit"):
    student_submit(student_data, student_id, student_name)
