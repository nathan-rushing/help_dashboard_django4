from django.contrib import admin
from .models import Document, Section, Subsection, Writer, Task


# Register your models here.

admin.site.register(Document)
admin.site.register(Section)
admin.site.register(Subsection)
admin.site.register(Writer)
admin.site.register(Task)
