# resume_app/views.py

import os
import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse
from django.conf import settings
from .pdf_utils import generate_resume_pdf

def resume_form(request):
    """
    The initial form to collect resume data.
    """
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
            "template_type": selected_template,
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "summary": request.POST.get("summary"),
            "skills": request.POST.get("skills").split(","),
            "projects": projects,
            "activities": activities,
            "awards": request.POST.get("awards").split(","),
        }

        # Store the data in session
        request.session["resume_data"] = data

        # Go to "Generating Resume" page
        return redirect("generating_resume")

    return render(request, "resumeapp/resume_form.html")

def generating_resume(request):
    """
    Page that shows a spinner/progress bar.
    It will fetch /start-generation/ via JS.
    """
    return render(request, "resumeapp/generating_resume.html")


# views.py

def start_generation(request):
    if request.method == "POST":
        data = request.session.get("resume_data")
        if not data:
            return JsonResponse({"error": "No resume data in session"}, status=400)

        template_type = data.pop("template_type", "traditional")
        pdf_file = generate_resume_pdf(data, template_type=template_type)

        import os, uuid
        from django.conf import settings

        filename = f"resume_{uuid.uuid4().hex}.pdf"
        full_path = os.path.join(settings.MEDIA_ROOT, filename)

        with open(full_path, "wb") as f:
            f.write(pdf_file.read())

        pdf_file.seek(0)
        return JsonResponse({"filename": filename})

    return JsonResponse({"error": "Method not allowed"}, status=405)



def download_finished(request, filename):
    """
    Once resume generation is done, user arrives here
    to see the download link + 'Transform to Portfolio' button.
    """
    return render(request, "resumeapp/download_finished.html", {"filename": filename})


def portfolio_view(request):
    """
    Shows a single-page HTML portfolio from the same session data.
    """
    data = request.session.get("resume_data")
    if not data:
        return render(request, "resumeapp/error.html", {"message": "No data available."})

    return render(request, "resumeapp/portfolio.html", {"data": data})
