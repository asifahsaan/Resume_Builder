from django.shortcuts import render
from django.http import FileResponse
from fpdf import FPDF, XPos, YPos
from io import BytesIO

class ResumePDF(FPDF):
    def __init__(self, company_name, slogan, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company_name = company_name
        self.slogan = slogan

        # Keep existing margins & auto page break
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(left=25, top=25, right=25)

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


def generate_resume_pdf(data, template_type="traditional"):
    """
    Generates a PDF resume using different fonts/colors
    and now includes basic background shapes
    based on the chosen template_type.
    """
    company_name = "Deltatechstore LLC"
    slogan = "Innovating Your Career Journey"

    # STYLE SETTINGS (Fonts & Accent Colors)
    STYLES = {
        "traditional": {
            "header_font_family": "Times",
            "header_font_size": 14,
            "body_font_family": "Times",
            "body_font_size": 12,
            "accent_color": (0, 0, 0)  # black
        },
        "modern": {
            "header_font_family": "Arial",
            "header_font_size": 14,
            "body_font_family": "Arial",
            "body_font_size": 12,
            "accent_color": (44, 62, 80)  # dark grey/blue
        },
        "creative": {
            "header_font_family": "Helvetica",
            "header_font_size": 14,
            "body_font_family": "Helvetica",
            "body_font_size": 12,
            "accent_color": (255, 99, 71)  # tomato color
        },
        "executive": {
            "header_font_family": "Arial",
            "header_font_size": 14,
            "body_font_family": "Arial",
            "body_font_size": 12,
            "accent_color": (52, 73, 94)  # subtle navy
        }
    }

    # Fallback to 'traditional' if unknown
    style = STYLES.get(template_type, STYLES["traditional"])

    pdf = ResumePDF(company_name, slogan)
    pdf.alias_nb_pages()
    pdf.resume_title = f"{data['name']}'s Resume"
    pdf.add_page()

    #
    # 1. DRAW BACKGROUND / SIDEBAR BASED ON TEMPLATE
    #
    if template_type == "traditional":
        # Light grey full-page background
        pdf.set_fill_color(230, 230, 230)  # R, G, B
        pdf.rect(0, 0, pdf.w, pdf.h, style="F")

    elif template_type == "modern":
        # Dark left sidebar
        pdf.set_fill_color(44, 62, 80)  # dark grey/blue
        pdf.rect(0, 0, 60, pdf.h, "F")  # 60mm wide sidebar

        # Optionally place some label in the sidebar (white text)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(style["header_font_family"], "B", 16)
        pdf.set_xy(10, 30)  # position inside the sidebar
        pdf.cell(40, 10, "Modern Template", ln=1)

        # Reset color back to black
        pdf.set_text_color(0, 0, 0)

    elif template_type == "creative":
        # Bold top bar
        pdf.set_fill_color(145, 40, 7)  # tomato
        pdf.rect(0, 0, pdf.w, 30, "F")

        # White text on top bar
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(style["header_font_family"], "B", 18)
        pdf.set_xy(10, 10)
        pdf.cell(0, 10, "Creative Template", ln=1)

        # Reset color
        pdf.set_text_color(0, 0, 0)

    elif template_type == "executive":
        # Subtle navy vertical bar on the left
        pdf.set_fill_color(52, 73, 94)  # subtle navy
        pdf.rect(0, 0, 8, pdf.h, "F")

        # We can add a small label
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(style["header_font_family"], "B", 16)
        pdf.set_xy(10, 20)
        pdf.cell(60, 10, "Executive Template", ln=1)
        pdf.set_text_color(0, 0, 0)

    #
    # 2. SETUP COLORS FOR HEADERS & BODY
    #
    HEADER_COLOR = style["accent_color"]
    BODY_COLOR = (0, 0, 0)  # black text for main

    #
    # Helper functions
    #
    def section_header(title):
        """Add section header with space check."""
        if pdf.get_y() > 260:  # near bottom
            pdf.add_page()
            # Re-draw background if needed on new page
            draw_background_on_new_page()

        pdf.set_font(style["header_font_family"], "B", style["header_font_size"])
        pdf.set_text_color(*HEADER_COLOR)
        pdf.cell(0, 6, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1)
        pdf.set_text_color(*BODY_COLOR)

    def ensure_space_for_content(min_lines=5):
        """Ensure space for a minimum number of lines."""
        line_height = 5
        remaining_space = 297 - pdf.get_y() - 10  # A4: 297mm
        required_space = min_lines * line_height
        if remaining_space < required_space:
            pdf.add_page()
            draw_background_on_new_page()

    def draw_background_on_new_page():
        """
        If text flows onto a new page, re-draw
        the background shape for that template,
        if desired.
        """
        if template_type == "traditional":
            pdf.set_fill_color(230, 230, 230)
            pdf.rect(0, 0, pdf.w, pdf.h, style="F")

        elif template_type == "modern":
            pdf.set_fill_color(44, 62, 80)
            pdf.rect(0, 0, 60, pdf.h, "F")
            # You can re-draw sidebar label if you want

        elif template_type == "creative":
            pdf.set_fill_color(145, 40, 7)
            pdf.rect(0, 0, pdf.w, 30, "F")
            # Re-draw top label if needed

        elif template_type == "executive":
            pdf.set_fill_color(52, 73, 94)
            pdf.rect(0, 0, 8, pdf.h, "F")
            # Re-draw side label if needed

    #
    # 3. PERSONAL DETAILS
    #
    pdf.set_font(style["body_font_family"], "B", 24)
    pdf.set_text_color(*BODY_COLOR)
    pdf.cell(0, 8, data["name"], align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font(style["body_font_family"], "", style["body_font_size"])
    pdf.cell(0, 8, f"{data['email']} | {data['phone']}", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)

    #
    # 4. SUMMARY
    #
    section_header("Summary")
    pdf.set_font(style["body_font_family"], "", style["body_font_size"])
    ensure_space_for_content(min_lines=4)
    pdf.multi_cell(0, 5, data["summary"])
    pdf.ln(6)

    #
    # 5. SKILLS
    #
    section_header("Skills")
    ensure_space_for_content(min_lines=4)
    pdf.set_font(style["body_font_family"], "", style["body_font_size"])
    pdf.multi_cell(0, 6, f"- {', '.join(data['skills'])}")
    pdf.ln(6)

    #
    # 6. PROJECTS
    #
    section_header("Projects")
    for project in data["projects"]:
        ensure_space_for_content(min_lines=6)
        pdf.set_font(style["body_font_family"], "B", 11)
        pdf.cell(0, 5, project["title"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font(style["body_font_family"], "", 11)
        pdf.multi_cell(0, 5, project["description"])
        pdf.ln(6)

    #
    # 7. CLUBS & EXTRACURRICULAR ACTIVITIES
    #
    section_header("Clubs & Extracurricular Activities")
    for activity in data["activities"]:
        ensure_space_for_content(min_lines=6)
        pdf.set_font(style["body_font_family"], "B", 11)
        pdf.cell(0, 5, activity["name"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font(style["body_font_family"], "I", 11)
        pdf.cell(0, 5, f"Role: {activity['role']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font(style["body_font_family"], "", 11)
        pdf.multi_cell(0, 5, activity["description"])
        pdf.ln(4)  # Space between items

    #
    # 8. AWARDS
    #
    section_header("Awards & Achievements")
    ensure_space_for_content(min_lines=4)
    pdf.set_font(style["body_font_family"], "", 11)
    for award in data["awards"]:
        pdf.cell(0, 5, f"- {award}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)

    #
    # SAVE PDF
    #
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output


def resume_form(request):
    if request.method == "POST":
        selected_template = request.POST.get("selected_template", "traditional")

        projects = [
            {"title": t, "description": d}
            for t, d in zip(
                request.POST.getlist("project_title"),
                request.POST.getlist("project_description")
            )
        ]
        activities = [
            {"name": n, "role": r, "description": d}
            for n, r, d in zip(
                request.POST.getlist("activity_name"),
                request.POST.getlist("activity_role"),
                request.POST.getlist("activity_description")
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

        pdf = generate_resume_pdf(data, template_type=selected_template)
        return FileResponse(pdf, as_attachment=True, filename="resume.pdf")

    return render(request, "resumeapp/resume_form.html")
