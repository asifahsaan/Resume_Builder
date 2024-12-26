# resume_app/pdf_utils.py

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
    and includes basic background shapes
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
        pdf.set_fill_color(230, 230, 230)  # Light grey
        pdf.rect(0, 0, pdf.w, pdf.h, "F")

    elif template_type == "modern":
        # Dark left sidebar
        pdf.set_fill_color(44, 62, 80)
        pdf.rect(0, 0, 60, pdf.h, "F")

        # Sidebar label example
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(style["header_font_family"], "B", 16)
        pdf.set_xy(10, 30)
        pdf.cell(40, 10, "Modern Template", ln=1)
        pdf.set_text_color(0, 0, 0)

    elif template_type == "creative":
        # Bold top bar
        pdf.set_fill_color(255, 99, 71)  # tomato
        pdf.rect(0, 0, pdf.w, 30, "F")
        # Label
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(style["header_font_family"], "B", 18)
        pdf.set_xy(10, 10)
        pdf.cell(0, 10, "Creative Template", ln=1)
        pdf.set_text_color(0, 0, 0)

    elif template_type == "executive":
        # Subtle navy vertical bar on the left
        pdf.set_fill_color(52, 73, 94)
        pdf.rect(0, 0, 8, pdf.h, "F")
        # Label
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(style["header_font_family"], "B", 16)
        pdf.set_xy(10, 20)
        pdf.cell(60, 10, "Executive Template", ln=1)
        pdf.set_text_color(0, 0, 0)

    #
    # Now define accent color / body color
    #
    HEADER_COLOR = style["accent_color"]
    BODY_COLOR = (0, 0, 0)

    def draw_background_on_new_page():
        """ Re-draw the background if a new page is added. """
        if template_type == "traditional":
            pdf.set_fill_color(230, 230, 230)
            pdf.rect(0, 0, pdf.w, pdf.h, "F")

        elif template_type == "modern":
            pdf.set_fill_color(44, 62, 80)
            pdf.rect(0, 0, 60, pdf.h, "F")
            # Could re-add label if you want

        elif template_type == "creative":
            pdf.set_fill_color(255, 99, 71)
            pdf.rect(0, 0, pdf.w, 30, "F")
            # Could re-add label

        elif template_type == "executive":
            pdf.set_fill_color(52, 73, 94)
            pdf.rect(0, 0, 8, pdf.h, "F")
            # Could re-add label

    def ensure_space_for_content(min_lines=5):
        """Ensure there's enough space left for at least min_lines lines."""
        line_height = 5
        remaining_space = 297 - pdf.get_y() - 10  # A4 is 297mm tall
        required_space = min_lines * line_height
        if remaining_space < required_space:
            pdf.add_page()
            draw_background_on_new_page()

    def section_header(title):
        if pdf.get_y() > 260:
            pdf.add_page()
            draw_background_on_new_page()

        pdf.set_font(style["header_font_family"], "B", style["header_font_size"])
        pdf.set_text_color(*HEADER_COLOR)
        pdf.cell(0, 6, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1)
        pdf.set_text_color(*BODY_COLOR)

    #
    # PERSONAL DETAILS
    #
    pdf.set_font(style["body_font_family"], "B", 24)
    pdf.set_text_color(*BODY_COLOR)
    pdf.cell(0, 8, data["name"], align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font(style["body_font_family"], "", style["body_font_size"])
    pdf.cell(0, 8, f"{data['email']} | {data['phone']}", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)

    #
    # SUMMARY
    #
    section_header("Summary")
    pdf.set_font(style["body_font_family"], "", style["body_font_size"])
    ensure_space_for_content(min_lines=4)
    pdf.multi_cell(0, 5, data["summary"])
    pdf.ln(6)

    #
    # SKILLS
    #
    section_header("Skills")
    ensure_space_for_content(min_lines=4)
    pdf.set_font(style["body_font_family"], "", style["body_font_size"])
    pdf.multi_cell(0, 6, "- " + ", ".join(data["skills"]))
    pdf.ln(6)

    #
    # PROJECTS
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
    # CLUBS & EXTRACURRICULAR ACTIVITIES
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
        pdf.ln(4)

    #
    # AWARDS
    #
    section_header("Awards & Achievements")
    ensure_space_for_content(min_lines=4)
    pdf.set_font(style["body_font_family"], "", 11)
    for award in data["awards"]:
        pdf.cell(0, 5, f"- {award}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)

    #
    # RETURN THE PDF
    #
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output
