from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def ensure_person_user_column(apps, schema_editor):
    table_name = "parties_person"
    with schema_editor.connection.cursor() as cursor:
        existing_tables = set(schema_editor.connection.introspection.table_names(cursor))
        if table_name not in existing_tables:
            return
        columns = {
            column.name
            for column in schema_editor.connection.introspection.get_table_description(cursor, table_name)
        }
    if "user_id" in columns:
        return

    Person = apps.get_model("parties", "Person")
    field = models.OneToOneField(
        blank=True,
        null=True,
        on_delete=django.db.models.deletion.CASCADE,
        to=settings.AUTH_USER_MODEL,
    )
    field.set_attributes_from_name("user")
    field.model = Person
    schema_editor.add_field(Person, field)


class Migration(migrations.Migration):
    dependencies = [
        ("parties", "0004_alter_studentevaluation_subject"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[migrations.RunPython(ensure_person_user_column, migrations.RunPython.noop)],
            state_operations=[
                migrations.AddField(
                    model_name="person",
                    name="user",
                    field=models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
