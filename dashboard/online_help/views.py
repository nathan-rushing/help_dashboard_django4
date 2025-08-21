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

from django.shortcuts import render, get_object_or_404, redirect
from .models import Document
from .forms import DocumentForm

from django.shortcuts import render, get_object_or_404
from .models import Subsection

from django.shortcuts import render, get_object_or_404, redirect
from .models import Section, Subsection
from .forms import SubsectionForm

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Document, Section
from .forms import SectionForm

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
    form = DocumentForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("online_help:document_list_edit")

    return render(request, "online_help/document_list_edit.html", {
        "documents": documents,
        "form": form
    })


def document_rename(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == "POST":
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            return redirect("online_help:document_list_edit")
    else:
        form = DocumentForm(instance=document)
    return render(request, "online_help/document_rename.html", {"form": form, "document": document})


def document_remove(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == "POST":
        document.delete()
        return redirect("online_help:document_list_edit")
    return render(request, "online_help/document_confirm_delete.html", {"document": document})


def document_sections(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    sections = document.sections.all()  # uses related_name="sections"
    return render(request, 
                  "online_help/document_sections.html", 
                  {"document": document, 
                   "sections": sections})

def document_sections_edit(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    sections = document.sections.all()  

    if request.method == "POST":
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.document = document
            section.save()
            return redirect("online_help:document_sections_edit", document_id=document.id)
    else:
        form = SectionForm()

    return render(request, 
                  "online_help/document_sections_edit.html", 
                  {"document": document, 
                   "sections": sections,
                   "form": form})


def section_rename(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if request.method == "POST":
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect("online_help:document_sections_edit", document_id=section.document.id)
    else:
        form = SectionForm(instance=section)

    return render(request, "online_help/section_rename.html", {"form": form, "section": section})


def section_delete(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    document_id = section.document.id
    section.delete()
    return redirect("online_help:document_sections_edit", document_id=document_id)

def section_subsections(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    subsections = section.subsections.all()  # uses related_name="subsections"
    return render(request, 
                  "online_help/section_subsections.html", 
                  {"section": section, 
                   "subsections": subsections})



from django.shortcuts import render, get_object_or_404, redirect
from .models import Section, Subsection
from .forms import SubsectionForm

def section_subsections_edit(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    subsections = section.subsections.all()

    # Add subsection
    if request.method == "POST" and "add_subsection" in request.POST:
        form = SubsectionForm(request.POST)
        if form.is_valid():
            subsection = form.save(commit=False)
            subsection.section = section
            subsection.save()
            return redirect("online_help:section_subsections_edit", section_id=section.id)
    else:
        form = SubsectionForm()

    # Delete subsection
    if request.method == "POST" and "delete_subsection" in request.POST:
        subsection_id = request.POST.get("subsection_id")
        subsection = get_object_or_404(Subsection, id=subsection_id, section=section)
        subsection.delete()
        return redirect("online_help:section_subsections_edit", section_id=section.id)

    return render(
        request,
        "online_help/section_subsections_edit.html",
        {"section": section, "subsections": subsections, "form": form},
    )


def subsection_rename(request, subsection_id):
    subsection = get_object_or_404(Subsection, id=subsection_id)
    section = subsection.section

    if request.method == "POST":
        form = SubsectionForm(request.POST, instance=subsection)
        if form.is_valid():
            form.save()
            return redirect("online_help:section_subsections_edit", section_id=section.id)
    else:
        form = SubsectionForm(instance=subsection)

    return render(
        request,
        "online_help/subsection_rename.html",
        {"section": section, "subsection": subsection, "form": form},
    )

from django.shortcuts import get_object_or_404, render, redirect
from .models import Subsection, Task, SME

from django.shortcuts import get_object_or_404, redirect, render
from .models import Subsection, Task, Writer
from .forms import TaskForm, WriterAssignForm  # Assuming you already have a form for Writer assignment
from django.db.models import Q


# views.py
def subsection_details(request, subsection_id):
    subsection = get_object_or_404(Subsection, id=subsection_id)
    tasks = Task.objects.filter(subsection=subsection)
    sme_list = SME.objects.filter(tasks__subsection=subsection)  # ✅ fixed here

    # Handle writer add
    if request.method == "POST" and "writer_form" in request.POST:
        form = WriterAssignForm(request.POST)
        if form.is_valid():
            writer = form.cleaned_data['writer']
            Task.objects.create(subsection=subsection, writer=writer)
            return redirect("online_help:subsection_details", subsection_id=subsection.id)
    else:
        form = WriterAssignForm()

    # Handle writer removal
    remove_writer_id = request.GET.get("remove_writer")
    if remove_writer_id:
        Task.objects.filter(subsection=subsection, writer_id=remove_writer_id).delete()
        return redirect("online_help:subsection_details", subsection_id=subsection.id)

    return render(request, "online_help/subsection_details.html", {
        "subsection": subsection,
        "tasks": tasks,
        "sme_list": sme_list,
        "form": form,
    })


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


from django.shortcuts import render, redirect, get_object_or_404
from .models import Subsection, SME
from django.views.decorators.http import require_POST

# online_help/views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Subsection, SME, Task

@require_POST
def edit_sme(request, sme_id):
    """
    Rename an existing SME (global), then redirect back to the page the user came from.
    """
    sme = get_object_or_404(SME, pk=sme_id)
    new_name = (request.POST.get("name") or "").strip()
    if not new_name:
        messages.error(request, "SME name cannot be empty.")
        return redirect(request.META.get("HTTP_REFERER", "online_help:document_list"))

    # If another SME already has this name, re-link tasks and delete the old one (merge).
    existing = SME.objects.filter(name=new_name).exclude(pk=sme.pk).first()
    if existing:
        Task.objects.filter(sme=sme).update(sme=existing)
        sme.delete()
        messages.success(request, f"SME renamed and merged into '{existing.name}'.")
    else:
        sme.name = new_name
        sme.save()
        messages.success(request, "SME updated successfully.")

    return redirect(request.META.get("HTTP_REFERER", "online_help:document_list"))


@require_POST
def add_sme(request, subsection_id):
    """
    Create (or get) an SME by name and assign it to tasks under the given subsection.
    Here we assign it only to tasks that currently have no SME.
    """
    subsection = get_object_or_404(Subsection, pk=subsection_id)
    name = (request.POST.get("name") or "").strip()

    if not name:
        messages.error(request, "Please provide a name for the SME.")
        return redirect("online_help:subsection_details", subsection_id=subsection.id)

    sme, _ = SME.objects.get_or_create(name=name)

    # Assign this SME to all tasks in the subsection that don't have an SME yet.
    Task.objects.filter(subsection=subsection, sme__isnull=True).update(sme=sme)

    messages.success(request, f"SME '{sme.name}' assigned to this subsection’s tasks.")
    return redirect("online_help:subsection_details", subsection_id=subsection.id)
