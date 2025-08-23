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
from django.db.models import Prefetch, F, Value, CharField, Q
from django.db.models.functions import Coalesce

from .models import (
    Document, Section, Subsection, Writer, Task, SME
)
from .forms import (
    DocumentForm, SectionForm, SubsectionForm, TaskForm, WriterAssignForm
)

from collections import defaultdict

from collections import defaultdict
from django.db.models import Value
from django.db.models.functions import Coalesce

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Version
from .forms import AssignTaskForm

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

from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskEditForm
from django.shortcuts import render, get_object_or_404
from .models import Task
@require_POST
@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def update_version(request):
    new_version = request.POST.get('version')
    if new_version:
        version_obj, _ = Version.objects.get_or_create(id=1)
        version_obj.number = new_version
        version_obj.save()
        return JsonResponse({'status': 'success', 'version': new_version})
    return JsonResponse({'status': 'error', 'message': 'No version provided'}, status=400)

@require_POST
@login_required
def verify_password(request):
    password = request.POST.get('password')
    user = authenticate(username=request.user.username, password=password)
    if user:
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid password'}, status=403)

@login_required
def home_test(request):
    writers = Writer.objects.annotate(
        sort_name=Coalesce('name', Value('zzz'))
    ).order_by('sort_name')

    tasks = Task.objects.select_related('writer', 'subsection__section__document')

    writer_tasks_grouped = {}
    color_classes = [
        "color-blue", "color-green", "color-red", "color-purple",
        "color-cyan", "color-orange", "color-teal", "color-yellow"
    ]

    writer_color_classes = {}
    for i, writer in enumerate(writers):
        writer_color_classes[writer.pk] = color_classes[i % len(color_classes)]

        grouped_by_doc = defaultdict(list)
        for task in tasks:
            if task.writer_id == writer.pk:
                document = task.subsection.section.document
                grouped_by_doc[document].append(task)
        writer_tasks_grouped[writer.pk] = dict(grouped_by_doc)

    version = Version.objects.first()

    ctx = {
        'writers': writers,
        'writer_tasks_grouped': writer_tasks_grouped,
        'writer_color_classes': writer_color_classes,
        'version': version,
        'can_edit': request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff),
    }
    return render(request, 'online_help/home_test.html', ctx)

from collections import defaultdict
from django.db.models import Count
from django.shortcuts import get_object_or_404
import json

@login_required
def dash_per_user(request, writer_pk):
    writer = get_object_or_404(Writer, pk=writer_pk)

    tasks = (
        Task.objects
        .filter(writer=writer)
        .select_related('subsection__section__document')
        .order_by('subsection__section__document__name',
                  'subsection__section__name',
                  'subsection__name')
    )

    # Group tasks by Document name
    grouped = defaultdict(list)
    for tk in tasks:
        doc_name = tk.subsection.section.document.name
        grouped[doc_name].append(tk)

    # Counts by color
    color_counts_qs = tasks.values('color').annotate(count=Count('id'))
    color_counts = {row['color'] or 'No Color': row['count'] for row in color_counts_qs}

    # Counts by document (for the pie chart)
    doc_counts_qs = tasks.values('subsection__section__document__name').annotate(count=Count('id'))
    document_task_counts = {
        row['subsection__section__document__name'] or 'No Document': row['count']
        for row in doc_counts_qs
    }

    return render(request, 'online_help/dash_per_user.html', {
        'writer': writer,
        'grouped_tasks': dict(grouped),
        'color_counts': color_counts,
        'total_tasks': tasks.count(),
        'document_task_counts_json': json.dumps(document_task_counts),
    })


@login_required
def view_subsection(request, subsection_id):
    task = get_object_or_404(Task, subsection_id=subsection_id)

    context = {
        "writer": task.writer.name if task.writer else "Unassigned",
        "section": task.subsection.section.name,
        "subsection": task.subsection.name,
        "color": task.color,
        "comments": task.comments,
        "sme": task.sme.name if task.sme else "Unassigned",
        "completion": task.completion,
        "task_id": subsection_id,
    }
    return render(request, "online_help/view_subsection.html", context)

@login_required
def view_subsection_edit(request, subsection_id):
    task = get_object_or_404(Task, subsection_id=subsection_id)

    if request.method == "POST":
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("online_help:view_subsection", subsection_id=subsection_id)
    else:
        form = TaskEditForm(instance=task)

    return render(request, "online_help/view_subsection_edit.html", {
        "form": form,
        "task": task,
    })


@login_required
def tasks_test(request):
    tasks = Task.objects.select_related("subsection__section__document", "writer").all()
    grouped_tasks = defaultdict(list)
    for task in tasks:
        document = task.subsection.section.document if task.subsection and task.subsection.section else None
        grouped_tasks[document].append(task)

    return render(request, "online_help/tasks_test.html", {"grouped_tasks": dict(grouped_tasks)})



@login_required
def document_list(request):
    documents = Document.objects.all()
    return render(request, 
                  "online_help/document_list.html", 
                  {"documents": documents})

@login_required
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


@login_required
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


@login_required
def document_remove(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == "POST":
        document.delete()
        return redirect("online_help:document_list_edit")
    return render(request, "online_help/document_confirm_delete.html", {"document": document})


@login_required
def document_sections(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    sections = document.sections.all()  # uses related_name="sections"
    return render(request, 
                  "online_help/document_sections.html", 
                  {"document": document, 
                   "sections": sections})

@login_required
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


@login_required
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


@login_required
def section_delete(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    document_id = section.document.id
    section.delete()
    return redirect("online_help:document_sections_edit", document_id=document_id)

@login_required
def section_subsections(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    subsections = section.subsections.all()  # uses related_name="subsections"
    return render(request, 
                  "online_help/section_subsections.html", 
                  {"section": section, 
                   "subsections": subsections})

@login_required
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


@login_required
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


@login_required
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

    remove_task_id = request.GET.get("remove_task")
    if remove_task_id:
        Task.objects.filter(id=remove_task_id, subsection=subsection).delete()
        return redirect("online_help:subsection_details", subsection_id=subsection.id)

    return render(request, "online_help/subsection_details.html", {
        "subsection": subsection,
        "tasks": tasks,
        "sme_list": sme_list,
        "form": form,
    })



@require_POST
@login_required
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
@login_required
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


@login_required
def assign_task(request):
    if request.method == 'POST':
        form = AssignTaskForm(request.POST)

        if form.is_valid():
            document = form.cleaned_data['document']
            section = form.cleaned_data['section']
            sub_section = form.cleaned_data['sub_section']
            writer = form.cleaned_data['writer']
            sme = form.cleaned_data['sme']

            # Find task(s) for the given subsection
            task = Task.objects.filter(subsection=sub_section).first()

            if not task:
                form.add_error(None, "Task not found for the selected subsection.")
            else:
                # Assign writer and SME to the task
                task.writer = writer
                task.sme = sme
                task.save()

                return redirect('online_help:tasks_test')  # Redirect after success

        else:
            print("Form is invalid:", form.errors)

    else:
        form = AssignTaskForm()

    return render(request, 'online_help/assign_task.html', {'form': form})

# For assign_task AJAX functionality
@login_required
def load_sections(request):
    document_id = request.GET.get('document')
    sections = Section.objects.filter(document_id=document_id).values("id", "name")
    return JsonResponse(list(sections), safe=False)

@login_required
def load_subsections(request):
    section_id = request.GET.get('section')
    subsections = Subsection.objects.filter(section_id=section_id).values("id", "name")
    return JsonResponse(list(subsections), safe=False)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next') or 'online_help:home_test'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    next_url = request.GET.get('next', '')
    return render(request, 'online_help/login.html', {'next': next_url})

@login_required
def logout_view(request):
    logout(request)
    return redirect('online_help:login')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Task

from django.shortcuts import render
from .models import Task, Document

from .models import Task, Document, Writer

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Task, Document, Writer

@login_required
def view_all(request):
    document_filter = request.GET.get('document')
    color_filter = request.GET.get('color')
    writer_filter = request.GET.get('writer')

    # ✅ Initialize tasks first
    tasks = Task.objects.select_related(
        'writer', 'sme', 'subsection__section__document'
    ).all()

    # ✅ Apply filters safely
    if document_filter:
        tasks = tasks.filter(subsection__section__document__id=document_filter)

    if color_filter:
        tasks = tasks.filter(color=color_filter)

    if writer_filter == "unassigned":
        tasks = tasks.filter(writer__isnull=True)
    elif writer_filter:
        tasks = tasks.filter(writer__id=writer_filter)

    # ✅ Prepare dropdown data
    documents = Document.objects.all()
    writers = Writer.objects.all()
    colors = [choice[0] for choice in Task.COLOR_CHOICES]

    return render(request, 'online_help/view_all.html', {
        'tasks': tasks,
        'documents': documents,
        'writers': writers,
        'colors': colors,
        'selected_document': document_filter,
        'selected_color': color_filter,
        'selected_writer': writer_filter,
    })


import openpyxl
from openpyxl.styles import Font
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Document

@login_required
def export_excel(request):
    # Create a workbook and sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tasks Overview"

    # Header row
    headers = [
        "Document", "Section", "Subsection", "Task Color", "Completion",
        "Writer", "SME", "Comments"
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    # Populate rows
    for document in Document.objects.prefetch_related("sections__subsections__tasks"):
        for section in document.sections.all():
            for subsection in section.subsections.all():
                for task in subsection.tasks.all():
                    ws.append([
                        document.name,
                        section.name,
                        subsection.name,
                        task.color,
                        task.completion,
                        task.writer.name if task.writer else "",
                        task.sme.name if task.sme else "",
                        task.comments or ""
                    ])

    # Prepare response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="tasks_export.xlsx"'
    wb.save(response)
    return response
