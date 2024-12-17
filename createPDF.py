from fpdf import FPDF

class ResumePDF(FPDF):
    def header(self):
        """
        Overriding FPDF's header method to include a header section on every page.
        """
        # Set font for the header (Times New Roman, Bold, 16pt)
        self.set_font("Times", "B", 16)
        # Create a cell for the resume title or name (left some margin on the left)
        self.cell(0, 10, self.resume_title, ln=True, align="C")
        self.ln(5)  # blank line after the header
    
    def footer(self):
        """
        Overriding FPDF's footer method to include a footer on every page.
        """
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Set font for the footer (Times New Roman, Italic, 8pt)
        self.set_font("Times", "I", 8)
        # Page number
        page_num_text = f"Page {self.page_no()}/{{nb}}"
        self.cell(0, 10, page_num_text, 0, 0, "C")

def create_student_resume_pdf(
    user_data,
    output_filename="student_resume.pdf"
):
    """
    Creates a PDF resume for a 2nd-year CS student using the FPDF library with Times New Roman font.

    user_data is expected to be a dictionary with keys:
    {
        "name": str,
        "email": str,
        "phone": str,
        "university": str,
        "degree": str,
        "grad_year": str,
        "summary": str,
        "skills": list of str,
        "projects": [
            {
                "title": str,
                "description": str
            },
            ...
        ],
        "clubs_activities": [
            {
                "activity_name": str,
                "role": str,
                "description": str
            },
            ...
        ],
        "awards": list of str
    }
    """
    # Initialize custom PDF class
    pdf = ResumePDF("P", "mm", "A4")
    pdf.resume_title = f"{user_data.get('name', 'Name')}'s Resume"
    pdf.alias_nb_pages()  # for total page count
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- HEADER: Name & Contact Info ---
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 8, user_data.get("name", "Name"), ln=True, align="C")
    
    pdf.set_font("Times", "", 12)
    contact_info = f"{user_data.get('email', 'Email')} | {user_data.get('phone', 'Phone')}"
    pdf.cell(0, 6, contact_info, ln=True, align="C")
    pdf.ln(8)

    # --- CAREER OBJECTIVE / SUMMARY ---
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 6, "Objective / Summary", ln=True)
    pdf.set_font("Times", "", 11)
    summary_text = user_data.get("summary", "A highly motivated Computer Science student...")
    pdf.multi_cell(0, 6, summary_text)
    pdf.ln(6)

    # --- EDUCATION ---
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 6, "Education", ln=True)
    pdf.set_font("Times", "", 11)
    degree_info = (f"{user_data.get('degree', 'B.Sc. in Computer Science')} "
                   f"({user_data.get('grad_year', 'Expected Graduation 20XX')})")
    pdf.cell(0, 6, degree_info, ln=True)
    pdf.cell(0, 6, user_data.get("university", "University Name"), ln=True)
    pdf.ln(6)

    # --- SKILLS ---
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 6, "Key Skills", ln=True)
    pdf.set_font("Times", "", 11)
    skills = user_data.get("skills", [])
    if skills:
        skills_str = ", ".join(skills)
        pdf.multi_cell(0, 6, skills_str)
    else:
        pdf.cell(0, 6, "No skills provided", ln=True)
    pdf.ln(6)

    # --- PROJECTS ---
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 6, "Projects", ln=True)
    projects = user_data.get("projects", [])
    if projects:
        for proj in projects:
            pdf.set_font("Times", "B", 11)
            pdf.cell(0, 6, proj.get("title", "Project Title"), ln=True)
            
            pdf.set_font("Times", "", 11)
            pdf.multi_cell(0, 6, proj.get("description", "Project description goes here."))
            pdf.ln(4)
    else:
        pdf.set_font("Times", "", 11)
        pdf.cell(0, 6, "No projects provided", ln=True)
    pdf.ln(4)

    # --- CLUBS & ACTIVITIES ---
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 6, "Clubs & Extracurricular Activities", ln=True)
    clubs = user_data.get("clubs_activities", [])
    if clubs:
        for club in clubs:
            pdf.set_font("Times", "B", 11)
            pdf.cell(0, 6, club.get("activity_name", "Activity"), ln=True)
            
            pdf.set_font("Times", "I", 11)
            role = club.get("role", "")
            pdf.cell(0, 6, f"Role: {role}", ln=True)

            pdf.set_font("Times", "", 11)
            description = club.get("description", "")
            pdf.multi_cell(0, 6, description)
            pdf.ln(4)
    else:
        pdf.set_font("Times", "", 11)
        pdf.cell(0, 6, "No clubs or activities provided", ln=True)
    pdf.ln(4)

    # --- AWARDS / ACHIEVEMENTS ---
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 6, "Awards & Achievements", ln=True)
    awards = user_data.get("awards", [])
    pdf.set_font("Times", "", 11)
    if awards:
        for award in awards:
            pdf.cell(0, 6, f"- {award}", ln=True)
    else:
        pdf.cell(0, 6, "No awards or achievements provided", ln=True)
    pdf.ln(6)

    # --- Output the PDF to a file ---
    pdf.output(output_filename)
    print(f"PDF generated: {output_filename}")


# ------------------------------------------------------------------------
# EXAMPLE USAGE
# ------------------------------------------------------------------------
if __name__ == "__main__":
    student_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1 (555) 123-4567",
        "university": "XYZ University",
        "degree": "B.Sc. Computer Science, 2nd Year",
        "grad_year": "Expected 2026",
        "summary": (
            "Enthusiastic and dedicated 2nd-year Computer Science student with a passion for "
            "software development and problem-solving. Seeking to leverage classroom knowledge "
            "in a practical environment to gain experience in coding, algorithms, and data structures."
        ),
        "skills": ["Python", "Java", "Data Structures", "Git/GitHub", "HTML/CSS", "Team Collaboration"],
        "projects": [
            {
                "title": "Student Portfolio Website",
                "description": (
                    "Developed a personal portfolio website using HTML, CSS, and a bit of JavaScript. "
                    "Showcases academic projects, coding samples, and extracurricular achievements."
                )
            },
            {
                "title": "Basic Chat Application",
                "description": (
                    "Created a command-line chat application in Python using sockets. "
                    "Learned about client-server architecture and basic networking principles."
                )
            }
        ],
        "clubs_activities": [
            {
                "activity_name": "Computer Science Club",
                "role": "Member",
                "description": (
                    "Participated in weekly coding challenges and hackathons. "
                    "Collaborated with peers to learn new programming techniques."
                )
            },
            {
                "activity_name": "Robotics Team",
                "role": "Volunteer",
                "description": (
                    "Helped design and test small-scale robots for inter-college competitions, "
                    "focusing on sensor integration and mechanical design aspects."
                )
            }
        ],
        "awards": [
            "Dean's List (2023)",
            "1st place in University Programming Contest"
        ]
    }

    create_student_resume_pdf(student_data, "john_doe_resume_times_new_roman.pdf")
