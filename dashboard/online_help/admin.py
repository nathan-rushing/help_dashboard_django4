from django.contrib import admin
from .models import Document, Section, Subsection, Writer, Task, Version, SME


# Register your models here.

admin.site.register(Document)
admin.site.register(Section)
admin.site.register(Subsection)
admin.site.register(Writer)
admin.site.register(Task)
admin.site.register(Version)
admin.site.register(SME)
