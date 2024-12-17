from django.shortcuts import render
from django.http import FileResponse
from fpdf import FPDF, XPos, YPos
from io import BytesIO

class ResumePDF(FPDF):
    def __init__(self, company_name, slogan, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company_name = company_name
        self.slogan = slogan

    def footer(self):
        # Move to bottom-right corner
        self.set_y(-20)
        self.set_x(-50)  # Position 50 units from the right margin

        # Set font and light color for company name and slogan
        self.set_font("Times", "I", 8)
        self.set_text_color(150, 150, 150)  # Light gray color (RGB: 150, 150, 150)

        # Print company name and slogan
        self.cell(0, 5, self.company_name, align="R", new_x=XPos.RIGHT, new_y=YPos.NEXT)
        self.cell(0, 5, self.slogan, align="R")


def generate_resume_pdf(data):
    company_name = "Deltatechstore LLC"
    slogan = "Innovating Your Career Journey"

    pdf = ResumePDF(company_name, slogan)
    pdf.alias_nb_pages()
    pdf.resume_title = f"{data['name']}'s Resume"
    pdf.add_page()

    def section_header(title):
        """Add section header with space check."""
        if pdf.get_y() > 260:  # Check if header would be too close to the page bottom
            pdf.add_page()
        pdf.set_font("Times", "B", 14)
        pdf.cell(0, 6, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        # pdf.ln(1)

    def ensure_space_for_content(min_lines=5):
        """Ensure space for a minimum number of lines."""
        line_height = 5
        remaining_space = 297 - pdf.get_y() - 10  # A4 page height minus margins
        required_space = min_lines * line_height
        if remaining_space < required_space:
            pdf.add_page()

    # Personal Details
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 8, data['name'], align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Times", "", 12)
    pdf.cell(0, 8, f"{data['email']} | {data['phone']}", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)

    # Summary
    section_header("Summary")
    pdf.set_font("Times", "", 11)
    ensure_space_for_content(min_lines=4)
    pdf.multi_cell(0, 5, data['summary'])
    pdf.ln(6)

    # Skills
    section_header("Skills")
    ensure_space_for_content(min_lines=4)
    pdf.set_font("Times", "", 11)
    pdf.multi_cell(0, 6,f'- { ", ".join(data['skills'])}')
    pdf.ln(6)

    # Projects
    section_header("Projects")
    for project in data['projects']:
        ensure_space_for_content(min_lines=6)
        pdf.set_font("Times", "B", 11)
        pdf.cell(0, 5, project['title'], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Times", "", 11)
        pdf.multi_cell(0, 5, project['description'])
        pdf.ln(6)

    # Clubs & Extracurricular Activities
    section_header("Clubs & Extracurricular Activities")
    for activity in data['activities']:
        ensure_space_for_content(min_lines=6)
        pdf.set_font("Times", "B", 11)
        pdf.cell(0, 5, activity['name'], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Times", "I", 11)
        pdf.cell(0, 5, f"Role: {activity['role']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Times", "", 11)
        pdf.multi_cell(0, 5, activity['description'])
        pdf.ln(4)  # Space between categories


    # Awards
    section_header("Awards & Achievements")
    ensure_space_for_content(min_lines=4)
    pdf.set_font("Times", "", 11)
    for award in data['awards']:
        pdf.cell(0, 5, f"- {award}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)  # Space after awards

    # Save PDF
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

def resume_form(request):
    if request.method == "POST":
        projects = [
            {"title": t, "description": d}
            for t, d in zip(request.POST.getlist("project_title"), request.POST.getlist("project_description"))
        ]
        activities = [
            {"name": n, "role": r, "description": d}
            for n, r, d in zip(
                request.POST.getlist("activity_name"),
                request.POST.getlist("activity_role"),
                request.POST.getlist("activity_description"),
            )
        ]
        data = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "summary": request.POST.get("summary"),
            "skills": request.POST.get("skills").split(","),
            "projects": projects,
            "activities": activities,
            "awards": request.POST.get("awards").split(","),
        }
        pdf = generate_resume_pdf(data)
        return FileResponse(pdf, as_attachment=True, filename="resume.pdf")
    return render(request, "resumeapp/resume_form.html")
