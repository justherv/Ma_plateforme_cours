from django.contrib import admin
from django.http import HttpResponse

from .models import Etudiant, Cours, Filiere, Travail_pratique, Examen_cours, Examen_tp, Support_cours, Support_tp
#from tinymce.widgets import  TinyMCE
from django.db import  models
#from.views import impetrant


# Register your models here.
'''class QuestionAdmin(admin.ModelAdmin):
    
    fieldsets = [
        ("Code/Type/Etat", {"fields":["code_question","type_question","etat_question"]}),
        ("Style/Paramètres", {"fields": ["style_question", "parametres_question"]}),
        ("Forme/Choix", {"fields": ["type_autorise", "choix_possible", "choix_autorise"]}),
        ("Fichier associé", {"fields": ["fichier_question"]}),
        ("Question en image", {"fields": ["image_question"]}),
        ("Contenu", {"fields": ["contenu_question"]}),
        ("Commentaire", {"fields": ["commentaire_question"]})
        #("Niveau de difficulté", {"fields": ["niveau"]}),
        #("Domaine", {"fields": ["domaine"]})
        # ("Réponse", {"fields": ["reponse"]})
    ]
'''






admin.site.register(Etudiant)
admin.site.register(Filiere)
admin.site.register(Cours)
admin.site.register(Travail_pratique)
admin.site.register(Examen_cours)
admin.site.register(Examen_tp)
admin.site.register(Support_cours)
admin.site.register(Support_tp)


#admin.site.register(impetrant)
