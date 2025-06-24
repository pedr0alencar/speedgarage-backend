from django.db import migrations
import json
from pathlib import Path
from django.utils import timezone


FIXTURE_PATH = Path(__file__).resolve().parent.parent / "fixtures" / "seed_iconic_unique.json"

def load_iconic(apps, schema_editor):
    Carro   = apps.get_model("reviews", "Carro")
    Critica = apps.get_model("reviews", "Critica")
    User    = apps.get_model("auth", "User")

    # garante usuário pk=1 (gearhead). Crie normalmente via createsuperuser se já não existir.
    if not User.objects.filter(pk=1).exists():
        User.objects.create_superuser(pk=1, username="gearhead", email="gearhead@example.com", password="123456")

    data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    carros_cache = {}

    for obj in data:
        if obj["model"] == "reviews.carro":
            fields = obj["fields"]
            carro, _ = Carro.objects.get_or_create(
                marca=fields["marca"],
                modelo=fields["modelo"],
                ano=fields["ano"],
                defaults={}
            )
            carros_cache[obj["pk"]] = carro

    for obj in data:
        if obj["model"] == "reviews.critica":
            fields = obj["fields"]
            Critica.objects.get_or_create(
                pk=obj["pk"],
                defaults={
                    "usuario_id": fields["usuario"],
                    "carro":      carros_cache[fields["carro"]],
                    "avaliacao":  fields["avaliacao"],
                    "texto":      fields["texto"],
                    "criado_em":  timezone.datetime.fromisoformat(fields["criado_em"].replace("Z", "+00:00")),
                }
            )

def unload_iconic(apps, schema_editor):
    # Reverso opcional – apaga críticas e carros criados
    Carro   = apps.get_model("reviews", "Carro")
    Critica = apps.get_model("reviews", "Critica")
    Critica.objects.all().delete()
    Carro.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ("reviews", "0002_auto"),      # coloque aqui a última migração existente
    ]

    operations = [
        migrations.RunPython(load_iconic, reverse_code=unload_iconic),
    ]
