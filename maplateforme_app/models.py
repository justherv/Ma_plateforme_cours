#from gdstorage.storage import GoogleDriveStorage, GoogleDrivePermissionType, GoogleDrivePermissionRole, GoogleDriveFilePermission

'''permission =  GoogleDriveFilePermission(
   GoogleDrivePermissionRole.READER,
   GoogleDrivePermissionType.USER,
   "justherven@gmail.com"
)
# Define Google Drive Storage
gd_storage = GoogleDriveStorage(permissions=(permission, ))'''

#gd_storage = GoogleDriveStorage()

import os

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User, Group
from datetime import  datetime, date
from django.db.models.fields import DurationField
#from .mychoices import *
from model_utils import Choices
# Create your models here.
from django.core.files.storage import FileSystemStorage
#import django_tables2 as tables


from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField

from maplateforme_app.storage import OverwriteStorage

from io import BytesIO

import decimal
from decimal import Decimal


class Filiere(models.Model):
    """
    Class to determine the scope of a question.
    """
    libelle_filiere=models.CharField(max_length=200)
    #correspondance=models.ManyToManyField(Niveau, through= 'Caracterisation')

    class Meta:
        verbose_name_plural="Filière"

    def __str__(self):
        """
        function that returns the name of the scope of a question.
        :return: scope of a question (domain)
        """
        return self.libelle_filiere



class Cours(models.Model):
    """
    Class for level difficulty
    """
    libelle_cours=models.CharField(max_length=100, default='', blank=True, null=True, verbose_name="Libellé du cours")

    class Meta:
        verbose_name_plural="Cours"

    def __str__(self):
        """
        function that returns names of different levels.
        :return: label of the parameter
        """
        return self.libelle_cours


class Travail_pratique(models.Model):
    """
    Class for level difficulty
    """
    libelle_tp=models.CharField(max_length=100, default='', blank=True, null=True, verbose_name="Libellé du TP")

    class Meta:
        verbose_name_plural="Travail Pratique"

    def __str__(self):
        """
        function that returns names of different levels.
        :return: label of the parameter
        """
        return self.libelle_tp



'''def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)'''


def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)


class Etudiant(models.Model):
    """
    Class that identifies a question
    """

    matricule_etudiant=models.CharField(max_length=20, default='', verbose_name="Matricule", blank=True)
    nom_etudiant= models.CharField(max_length=100, default='',  verbose_name="Nom(s)")
    prenom_etudiant = models.CharField(max_length=100, default='', blank=True, verbose_name="Prénom(s)")
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, verbose_name="Filière", default='', null=True,
                                blank=True)
    examencours = models.ManyToManyField(Cours, through='Examen_cours')
    examentp = models.ManyToManyField(Travail_pratique, through='Examen_tp')

    photo_etudiant = models.FileField(null=True, blank=True, default='', verbose_name="Photo étudiant", storage=OverwriteStorage())

    export_to_CSV = models.BooleanField(default=False, verbose_name="Cochez pour exporter (Excel)")
    export_to_TXT = models.BooleanField(default=False, verbose_name="Cochez pour exporter")

    class Meta:
        verbose_name_plural="Etudiants"

    def __str__(self):
        """
        function that returns a student code
        :return: student code
        """
        mat= self.matricule_etudiant + "   "
        matnom= mat + self.nom_etudiant
        #matnom2= matnom + " "
        #identite_etudiant= matnom2 + self.prenom_etudiant

        return matnom


class Examen_cours(models.Model):
    monetudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, verbose_name="Matricule et Nom(s)", blank=True, max_length=100, default='')
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    note_cc = models.DecimalField(decimal_places=2, max_digits=5, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True)
    note_tpe = models.DecimalField(decimal_places=2, max_digits=5, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True)
    note_synthese = models.DecimalField(decimal_places=2, max_digits=5, validators=[MinValueValidator(Decimal('0.01'))],
                                   blank=True, null=True)
    export_to_EXCEL = models.BooleanField(default=False, verbose_name="Cochez pour exporter (Excel)")

    class Meta:
        verbose_name_plural="Examen des Cours"

    def __str__(self):
        """
        function for course exam
        :return: student
        """

        return self.monetudiant


class Examen_tp(models.Model):
    monetudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, verbose_name="Matricule et Nom(s)", blank=True, max_length=100, default='')
    tp = models.ForeignKey(Travail_pratique, on_delete=models.CASCADE)
    note_tp = models.DecimalField(decimal_places=2, max_digits=5, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True)
    export_to_EXCEL = models.BooleanField(default=False, verbose_name="Cochez pour exporter (Excel)")


    class Meta:
        verbose_name_plural="Examen des TPs"

    def __str__(self):
        """
        function for TP exam
        :return: student
        """
        return self.monetudiant




class Support_cours(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, verbose_name="Libellé du cours", default='', null=True,
                                blank=True)
    libelle_support_cours= models.CharField(max_length=100, default='', blank=True, null=True, verbose_name="Libellé du support de cours")
    fichier_support_cours = models.FileField(blank=True, default='', verbose_name="Fichier du support de cours", storage=OverwriteStorage())

    class Meta:
        verbose_name_plural="Supports des Cours"

    def __str__(self):
        """
        function for TP exam
        :return: student
        """
        return self.libelle_support_cours

    def fichier_support_cours_filename(self):
        """
        function that returns names of different levels.
        :return: image name
        """
        return os.path.basename(self.fichier_support_cours.name)


class Support_tp(models.Model):
    tp = models.ForeignKey(Travail_pratique, on_delete=models.CASCADE, verbose_name="Libellé du TP", default='', null=True,
                              blank=True)
    libelle_support_tp= models.CharField(max_length=100, default='', blank=True, null=True, verbose_name="Libellé du support de TP")
    fichier_support_tp = models.FileField(blank=True, default='', verbose_name="Fichier du support de cours", storage=OverwriteStorage())

    class Meta:
        verbose_name_plural="Supports des TPs"

    def __str__(self):
        """
        function for TP exam
        :return: student
        """
        return self.libelle_support_tp