from django.db import migrations

def agregar_equipamiento(apps, schema_editor):
    # Obtener los modelos
    Weapon = apps.get_model('equipment', 'Weapon')

    # Lista de armas predefinidas
    armas = [
        {"name": "Espada de Acero", "tipo": "weapon", "potencia": 40, "alcance": 1},
        {"name": "Arco Largo", "tipo": "weapon", "potencia": 35, "alcance": 10},
        {"name": "Lanza de Plata", "tipo": "weapon", "potencia": 45, "alcance": 3},
    ]

    # Insertar armas
    for arma in armas:
        Weapon.objects.create(**arma)

class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0003_remove_equipment_imagen'),  # Reemplázalo con la última migración existente
    ]

    operations = [
        migrations.RunPython(agregar_equipamiento),
    ]
