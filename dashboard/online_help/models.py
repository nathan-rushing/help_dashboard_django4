from django.db import models

class Document(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.document.name} - {self.name}"


class Subsection(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="subsections")
    name = models.CharField(max_length=255)

    # Shared attributes
    COLOR_CHOICES = [
        ("green", "Green"),
        ("yellow", "Yellow"),
        ("grey", "Grey"),
        ("white", "White"),
        ("orange", "Orange"),
    ]
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default="white")
    completion = models.CharField(max_length=20, default="0%")
    comments = models.TextField(blank=True, null=True)   # ✅ move here

    def __str__(self):
        return f"{self.section.name} - {self.name}"

class Writer(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class SME(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE, related_name="tasks")
    writers = models.ManyToManyField(Writer, blank=True, related_name="tasks")  # ✅ Changed here
    sme = models.ForeignKey("SME", on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")

    def __str__(self):
        writers_list = ", ".join([writer.name for writer in self.writers.all()])
        return f"Task: {self.subsection.name} ({writers_list if writers_list else 'Unassigned'})"

class Version(models.Model):
    number = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number