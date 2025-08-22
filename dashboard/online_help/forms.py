# forms.py
from django import forms
from .models import Writer, Document, Section, Subsection, Writer
# forms.py
from django import forms
from .models import Task, Writer

# forms.py
from django import forms
from .models import Writer, Task


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["name"]

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["name"]

class SubsectionForm(forms.ModelForm):
    class Meta:
        model = Subsection
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subsection name'}),
        }


class TaskForm(forms.Form):
    writer = forms.ModelChoiceField(queryset=Writer.objects.all(), required=True)

class WriterAssignForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['writer']

    writer = forms.ModelChoiceField(
        queryset=Writer.objects.all(),
        required=False,   # ✅ allow blank
        empty_label="No Writer Assigned",  # ✅ dropdown option for blank
        label="Select Writer"
    )

# class AssignTaskForm(forms.Form):
#     document = forms.ChoiceField(
#         label="Document",
#         required=True,
#         widget=forms.Select(attrs={'id': 'id_document', 'class': 'form-control'})
#     )
#     section = forms.ChoiceField(
#         label="Section",
#         required=True,
#         widget=forms.Select(attrs={'id': 'id_section', 'class': 'form-control'})
#     )
#     sub_section = forms.ChoiceField(
#         label="Subsection",
#         required=True,
#         widget=forms.Select(attrs={'id': 'id_sub_section', 'class': 'form-control'})
#     )
#     writer = forms.ModelChoiceField(
#         queryset=Writer.objects.all(),
#         label="Writer",
#         required=True,
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         documents = Document.objects.filter(id__in=Task.objects.values_list('document', flat=True).distinct())
#         self.fields['document'].choices = [('', 'Select document')] + [(doc.id, doc.title) for doc in documents]

#         self.fields['section'].choices = [('', 'Select section')]
#         self.fields['sub_section'].choices = [('', 'Select subsection')]

#         if 'document' in self.data:
#             document = self.data.get('document')
#             sections = Task.objects.filter(document=document).values_list('section', flat=True).distinct()
#             self.fields['section'].choices += [(s, s) for s in sections]

#         if 'section' in self.data:
#             section = self.data.get('section')
#             subsections = Task.objects.filter(section=section).values_list('sub_section', flat=True).distinct()
#             self.fields['sub_section'].choices += [(s, s) for s in subsections]

from django import forms
from .models import Document, Section, Subsection, Writer, SME

class AssignTaskForm(forms.Form):
    document = forms.ModelChoiceField(queryset=Document.objects.all(), required=True)
    section = forms.ModelChoiceField(queryset=Section.objects.none(), required=True)
    sub_section = forms.ModelChoiceField(queryset=Subsection.objects.none(), required=True)
    writer = forms.ModelChoiceField(queryset=Writer.objects.all(), required=True)
    sme = forms.ModelChoiceField(queryset=SME.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # dynamically load section/subsection if data already present
        if 'document' in self.data:
            try:
                document_id = int(self.data.get('document'))
                self.fields['section'].queryset = Section.objects.filter(document_id=document_id)
            except (ValueError, TypeError):
                pass

        if 'section' in self.data:
            try:
                section_id = int(self.data.get('section'))
                self.fields['sub_section'].queryset = Subsection.objects.filter(section_id=section_id)
            except (ValueError, TypeError):
                pass
