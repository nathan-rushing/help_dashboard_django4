import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from online_help.models import Document, Section, Subsection, Writer, Task, SME


class Command(BaseCommand):
    help = "Import tasks from the Excel file into the database"

    def handle(self, *args, **kwargs):
        excel_path = os.path.join(
            settings.BASE_DIR,  # help_dashboard_django4/
            "online_help", "management", "dataset",
            "Radiant_2025.1_help_assignments_v3_cleaned.xlsx"
        )
        df = pd.read_excel(excel_path, sheet_name="2025.1")

        imported_count = 0

        for _, row in df.iterrows():
            doc_name = str(row.get("Documentation")).strip()
            sec_name = str(row.get("Section")).strip()
            sub_name = str(row.get("Sub-sections")).strip()
            writer_name = str(row.get("Writer")).strip()
            comments = row.get("Comments")
            sme_name = str(row.get("Subject Matter Expert/Engineering")).strip() if pd.notna(row.get("Subject Matter Expert/Engineering")) else None
            sme = None
            if sme_name:
                sme, _ = SME.objects.get_or_create(name=sme_name)

            color = str(row.get("color")).lower().strip() if row.get("color") else "white"

            if not doc_name or not sec_name or not sub_name:
                continue

            document, _ = Document.objects.get_or_create(name=doc_name)
            section, _ = Section.objects.get_or_create(document=document, name=sec_name)
            subsection, _ = Subsection.objects.get_or_create(section=section, name=sub_name)

            writer = None
            if writer_name and writer_name.lower() != "no writer":
                writer, _ = Writer.objects.get_or_create(name=writer_name)

            task, created = Task.objects.get_or_create(
                subsection=subsection,
                writer=writer,
                sme=sme,   # ✅ now foreign key
                defaults={
                    "comments": comments if pd.notna(comments) else "",
                    "color": color,
                },
            )

            if created:
                imported_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Excel data imported successfully from {excel_path}! Imported {imported_count} new tasks."
        ))
