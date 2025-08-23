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
    COLOR_CHOICES = [
        ("green", "Green"),
        ("yellow", "Yellow"),
        ("grey", "Grey"),
        ("white", "White"),
        ("orange", "Orange"),
    ]
    subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE, related_name="tasks")
    writer = models.ForeignKey(Writer, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    sme = models.ForeignKey("SME", on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    comments = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default="white")
    completion = models.CharField(max_length=20, default="0%")

    def __str__(self):
        return f"Task: {self.subsection.name} ({self.writer.name if self.writer else 'Unassigned'})"

class Version(models.Model):
    number = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number