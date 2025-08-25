# forms.py
from django import forms
from .models import Writer, Document, Section, Subsection, Writer
# forms.py
from django import forms
from .models import Task, Writer

# forms.py
from django import forms
from .models import Writer, Task

from django import forms
from .models import Document, Section, Subsection, Writer

from django import forms
from .models import Task

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

# forms.py
from django import forms
from .models import Writer

class WriterAssignForm(forms.Form):
    writer = forms.ModelChoiceField(queryset=Writer.objects.all(), required=True)


class AssignTaskForm(forms.Form):
    document = forms.ModelChoiceField(queryset=Document.objects.all(), required=True)
    section = forms.ModelChoiceField(queryset=Section.objects.none(), required=True)
    sub_section = forms.ModelChoiceField(queryset=Subsection.objects.none(), required=True)
    writers = forms.ModelMultipleChoiceField(
        queryset=Writer.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Case 1: bound form (POST)
        if 'document' in self.data:
            try:
                document_id = int(self.data.get('document'))
                self.fields['section'].queryset = Section.objects.filter(document_id=document_id)
            except (ValueError, TypeError):
                pass
        # Case 2: initial data (GET or re-render after error)
        elif self.initial.get("document"):
            self.fields['section'].queryset = Section.objects.filter(document=self.initial["document"])

        if 'section' in self.data:
            try:
                section_id = int(self.data.get('section'))
                self.fields['sub_section'].queryset = Subsection.objects.filter(section_id=section_id)
            except (ValueError, TypeError):
                pass
        elif self.initial.get("section"):
            self.fields['sub_section'].queryset = Subsection.objects.filter(section=self.initial["section"])

class SubsectionEditForm(forms.ModelForm):
    class Meta:
        model = Subsection
        fields = ["color", "completion", "comments"]
        widgets = {
            "color": forms.Select(attrs={"class": "form-control"}),
            "completion": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 50%"}),
            "comments": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
        }

