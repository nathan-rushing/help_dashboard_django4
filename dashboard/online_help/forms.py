# forms.py
from django import forms
from .models import Document, Section, Subsection

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

from django import forms
from .models import Writer

class TaskForm(forms.Form):
    writer = forms.ModelChoiceField(queryset=Writer.objects.all(), required=True)


# forms.py
from django import forms
from .models import Writer, Task

class WriterAssignForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['writer']

    writer = forms.ModelChoiceField(
        queryset=Writer.objects.all(),
        required=True,
        label="Select Writer"
    )
