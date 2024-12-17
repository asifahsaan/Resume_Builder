from fpdf import FPDF
import re
import sys
from fpdf import FPDF, XPos, YPos

class ResumePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_left_margin(20)
        self.set_right_margin(20)
        self.set_top_margin(15)
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("Times", "B", 16)
        self.cell(0, 10, self.resume_title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(5)  # Extra line spacing after title

    def footer(self):
        self.set_y(-15)
        self.set_font("Times", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")


def prompt_based_input():
    """ Collect user input interactively """
    print("\n--- Step-by-Step Resume Builder ---")
    data = {}
    data["name"] = input("Full Name: ")
    data["email"] = input("Email: ")
    data["phone"] = input("Phone Number: ")
    data["university"] = input("University Name: ")
    data["degree"] = input("Degree & Year (e.g., B.Sc. CS, 2nd Year): ")
    data["grad_year"] = input("Expected Graduation Year: ")
    data["summary"] = input("Career Objective / Summary: ")

    # Skills
    data["skills"] = []
    print("\nEnter your skills one by one. Type 'done' to finish:")
    while True:
        skill = input("Skill: ")
        if skill.lower() == "done":
            break
        data["skills"].append(skill)

    # Projects
    data["projects"] = []
    print("\nEnter your projects. Type 'done' as the title to finish:")
    while True:
        title = input("Project Title: ")
        if title.lower() == "done":
            break
        description = input("Project Description: ")
        data["projects"].append({"title": title, "description": description})

    # Clubs & Activities
    data["clubs_activities"] = []
    print("\nEnter your extracurricular activities. Type 'done' to finish:")
    while True:
        activity_name = input("Activity Name: ")
        if activity_name.lower() == "done":
            break
        role = input("Role: ")
        description = input("Activity Description: ")
        data["clubs_activities"].append({"activity_name": activity_name, "role": role, "description": description})

    # Awards
    data["awards"] = []
    print("\nEnter your awards one by one. Type 'done' to finish:")
    while True:
        award = input("Award: ")
        if award.lower() == "done":
            break
        data["awards"].append(award)

    return data

def paragraph_based_input():
    """ Collect resume details from a paragraph with improved parsing """
    print("\n--- Paste your resume details in a single paragraph ---")
    paragraph = input("Enter your resume details:\n")

    # Initialize data dictionary
    data = {
        "name": "",
        "email": "",
        "phone": "",
        "university": "",
        "degree": "",
        "grad_year": "",
        "summary": "",
        "skills": [],
        "projects": [],
        "clubs_activities": [],
        "awards": []
    }

    # Extract Name (assuming it's the first line or starts the paragraph)
    name_match = re.match(r"^(.*?)\,", paragraph)
    if name_match:
        data["name"] = name_match.group(1).strip()

    # Extract University, Degree, and Graduation Year
    edu_match = re.search(r"(\w+ University).*?\((.*?)\)", paragraph)
    if edu_match:
        data["university"] = edu_match.group(1)
        data["grad_year"] = edu_match.group(2)

    # Extract Summary
    summary_match = re.search(r"Highlight (.*? real-world scenarios)\.", paragraph)
    if summary_match:
        data["summary"] = summary_match.group(1)

    # Extract Skills
    skills_match = re.search(r"key skills such as (.*?)\.", paragraph)
    if skills_match:
        data["skills"] = [skill.strip() for skill in skills_match.group(1).split(",")]

    # Extract Projects
    project_matches = re.findall(r"like (.*? \((.*?)\))", paragraph)
    for match in project_matches:
        title = match[0].split("(")[0].strip()
        description = f"Technologies: {match[1]}"
        data["projects"].append({"title": title, "description": description})

    # Extract Clubs/Activities
    club_match = re.search(r"membership in the (.*?) \(.*?\) and (.*? Robotics Team)", paragraph)
    if club_match:
        data["clubs_activities"].append({
            "activity_name": club_match.group(1),
            "role": "Member",
            "description": "Participated in coding challenges and hackathons."
        })
        data["clubs_activities"].append({
            "activity_name": club_match.group(2),
            "role": "Volunteer",
            "description": "Contributed to Robotics Team activities."
        })

    # Extract Awards
    awards_match = re.findall(r"like (.*?) and (.*?)\.", paragraph)
    if awards_match:
        data["awards"] = [award.strip() for award in awards_match[0]]

    return data


def create_resume():
    print("\nChoose input method:")
    print("1: Step-by-Step Prompt Input")
    print("2: Paragraph-Based Input")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        user_data = prompt_based_input()
    elif choice == "2":
        user_data = paragraph_based_input()
    else:
        print("Invalid choice. Exiting.")
        sys.exit()

    filename = input("Enter output PDF filename (e.g., 'resume.pdf'): ")
    if not filename.endswith(".pdf"):
        filename += ".pdf"

    create_student_resume_pdf(user_data, filename)
    print(f"\nResume saved as {filename}")

def create_student_resume_pdf(user_data, output_filename):
    """ Generate the PDF resume """
    pdf = ResumePDF()
    pdf.resume_title = f"{user_data.get('name', 'Name')}'s Resume"
    pdf.alias_nb_pages()
    pdf.add_page()

    def section_header(title):
        pdf.set_font("Times", "B", 12)
        pdf.cell(0, 6, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

    # Add Personal Details
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 10, user_data.get("name", ""), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("Times", "", 12)
    email_phone = f"{user_data.get('email', '')} | {user_data.get('phone', '')}"
    pdf.cell(0, 10, email_phone, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(8)  # Add spacing before next section

    # Objective
    section_header("Objective / Summary")
    pdf.set_font("Times", "", 11)
    pdf.multi_cell(0, 6, user_data.get("summary", ""))
    pdf.ln(8)

    # Education
    section_header("Education")
    pdf.set_font("Times", "", 11)
    pdf.multi_cell(0, 6, f"({user_data.get('grad_year')})\n{user_data.get('university')}")
    pdf.ln(8)

    # Skills
    section_header("Skills")
    pdf.set_font("Times", "", 11)
    pdf.multi_cell(0, 6, ", ".join(user_data.get("skills", [])))
    pdf.ln(8)

    # Projects
    section_header("Projects")
    for proj in user_data.get("projects", []):
        pdf.set_font("Times", "B", 11)
        pdf.cell(0, 6, proj.get("title"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Times", "", 11)
        pdf.multi_cell(0, 6, proj.get("description"))
        pdf.ln(2)
    pdf.ln(8)

    # Clubs & Extracurricular Activities
    section_header("Clubs & Extracurricular Activities")
    for club in user_data.get("clubs_activities", []):
        pdf.set_font("Times", "B", 11)
        pdf.cell(0, 6, club.get('activity_name', ""), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Times", "I", 11)
        role = club.get("role", "")
        pdf.cell(0, 6, f"Role: {role}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Times", "", 11)
        pdf.multi_cell(0, 6, club.get("description"))
        pdf.ln(2)
    pdf.ln(8)

    # Awards
    section_header("Awards & Achievements")
    for award in set(user_data.get("awards", [])):
        pdf.set_font("Times", "", 11)
        pdf.cell(0, 6, f"- {award}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)

    pdf.output(output_filename)
if __name__ == "__main__":
    create_resume()