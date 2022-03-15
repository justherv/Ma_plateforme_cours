from .models import Etudiant
import django_filters

class EtudiantFilter(django_filters.FilterSet):

    class Meta:
        model = Etudiant
        fields = ['matricule_etudiant', ]