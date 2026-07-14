from django.db import migrations


def create_categories(apps, schema_editor):
    Category = apps.get_model("core", "Category")

    categories = [
        "Programming",
        "Artificial Intelligence",
        "Web Development",
        "Mobile Development",
        "Data Science",
        "Cybersecurity",
        "Business",
        "Marketing",
        "Design",
        "Personal Development",
        "Finance",
        "Health & Wellness",
    ]

    for name in categories:
        Category.objects.get_or_create(name=name)
    
class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_seminar_category_alter_seminar_participants_and_more'),
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]