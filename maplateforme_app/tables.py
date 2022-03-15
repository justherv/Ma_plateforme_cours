import django_tables2 as tables
from .models import Etudiant

class EtudiantTable(tables.Table):
    selection=tables.CheckBoxColumn(accessor='pk')

    class Meta:
        model = Etudiant
