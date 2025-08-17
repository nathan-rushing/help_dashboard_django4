from django.shortcuts import render

# Create your views here.
from collections import defaultdict, Counter
import json
import math
import pandas as pd

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.db.models import Prefetch, F, Value, CharField
from django.db.models.functions import Coalesce
from .models import Task, Subsection, Section, Document, Writer, SME


from .models import (
    Document, Section, Subsection, Writer, Task
)
# from .forms import (

# )

def home_test(request):
    # Fetch all tasks with related data
    tasks = Task.objects.select_related("subsection__section__document", "writer").all()
    return render(request, 
                  "online_help/home_test.html", 
                  {"tasks": tasks})

def tasks_test(request):
    tasks = Task.objects.select_related("subsection__section__document", "writer").all()
    return render(request, 
                  "online_help/tasks_test.html", 
                  {"tasks": tasks})

def document_list(request):
    documents = Document.objects.all()
    return render(request, 
                  "online_help/document_list.html", 
                  {"documents": documents})

def document_list_edit(request):
    documents = Document.objects.all()
    return render(request, 
                  "online_help/document_list_edit.html", 
                  {"documents": documents})

def document_sections(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    sections = document.sections.all()  # uses related_name="sections"
    return render(request, 
                  "online_help/document_sections.html", 
                  {"document": document, 
                   "sections": sections})

def document_sections_edit(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    sections = document.sections.all()  # uses related_name="sections"
    return render(request, 
                  "online_help/document_sections_edit.html", 
                  {"document": document, 
                   "sections": sections})


def section_subsections(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    subsections = section.subsections.all()  # uses related_name="subsections"
    return render(request, 
                  "online_help/section_subsections.html", 
                  {"section": section, 
                   "subsections": subsections})

def section_subsections_edit(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    subsections = section.subsections.all()  # uses related_name="subsections"
    return render(request, 
                  "online_help/section_subsections_edit.html", 
                  {"section": section, 
                   "subsections": subsections})


from django.shortcuts import render, get_object_or_404
from .models import Subsection

def subsection_details(request, subsection_id):
    subsection = get_object_or_404(Subsection, id=subsection_id)

    # Grab tasks and prefetch related writer/SME to avoid N+1 queries
    tasks = subsection.tasks.select_related("writer", "sme").all()

    # Collect unique SME **names** (FK-safe filtering)
    sme_list = (
        tasks.filter(sme__isnull=False)
             .values_list("sme__name", flat=True)
             .distinct()
             .order_by("sme__name")
    )

    return render(
        request,
        "online_help/subsection_details.html",
        {
            "subsection": subsection,
            "tasks": tasks,
            "sme_list": sme_list,  # <-- pass names
        },
    )
