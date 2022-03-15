from functools import reduce
from itertools import chain

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django_tables2 import RequestConfig
from django.contrib.auth.models import User, Group

import django.forms as forms
from .models import Etudiant, Cours, Examen_cours, Examen_tp, Filiere, Travail_pratique, Support_cours, Support_tp
from .forms import EtudiantForm, EtudiantSearchForm, EtudiantFormedit, Examen_coursForm, Examen_coursSearchForm,\
    Examen_coursFormedit, Examen_tpForm, Examen_tpSearchForm, Examen_tpFormedit, FiliereForm, FiliereSearchForm,\
    FiliereFormedit, CoursForm, CoursFormedit, CoursSearchForm, Travail_pratiqueForm, Travail_pratiqueFormedit,\
    Travail_pratiqueSearchForm, Support_coursForm, Support_coursFormedit, Support_coursSearchForm, \
    Support_tpForm, Support_tpFormedit, Support_tpSearchForm

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

from django.core.files import File

from io import BytesIO

import urllib

import zipfile
from django.core.files.uploadedfile import SimpleUploadedFile
from urllib.request import urlretrieve
from zipfile import ZipFile

from os.path import basename

import pathlib

import re
from pygcode import Line

import csv
import ast
import os
import json

import operator

from django.views.generic import ListView, CreateView, UpdateView

from django.db.models import Q

from .tables import EtudiantTable

from .filters import EtudiantFilter

from django.core.files.storage import FileSystemStorage

from datetime import  datetime, date, time, timedelta

from itertools import combinations

import json

import xlwt

#import  timedelta

# from .models import Member


# Create your views here.
def home(request):
    """
    function corresponding to the view of home page of student
    :param request:
    :type request:
    :return:home view
    :rtype:
    """
    #title = "Page dédiée aux étudiants d' MIP3 (ENSAI) "
    title= ""
    context = {
        'title': title,
    }
    return render(request, 'maplateforme_app/home.html', context)




def etudiant_list(request):
    """
    function that gives view on the list of questions
    :param request:
    :type request:
    :return:view on the list of questions
    :rtype:
    """
    #choix=[]
    #epsilon=50.0
    title = 'Liste des étudiants'
    etudiants = Etudiant.objects.all().order_by('nom_etudiant')
    etu_filiere=etudiants
    instance = etudiants
    form = EtudiantSearchForm(request.POST or None)


    #table= QuestionTable(Question.objects.all())
    context = {
        'title': title,
        'etudiants': etudiants,
        'form': form,
        #'table' : table,
    }

    if request.method == 'POST':
        print('post Ok')
        list_selected= request.POST.getlist('etudiants_choisis')
        print("Ma liste selectionnée = ",list_selected)

        fil= 0          #filière vide
        #niv = 0  # niveau vide->niv=0, niveau choisi->niv=1
        if form['filiere'].value():
            etudiants= Etudiant.objects.all().order_by('nom_etudiant').filter(
            filiere=form['filiere'].value())
            etu_filiere=etudiants
            fil=1     #filière sélectionné
            #print(questions)


        if form['matricule_etudiant'].value():
            if fil==0:
                etudiants = Etudiant.objects.all().order_by('nom_etudiant').filter(
                    matricule_etudiant__icontains=form['matricule_etudiant'].value())
            else:
                etudiants = etu_filiere.all().order_by('nom_etudiant').filter(
                    matricule_etudiant__icontains=form['matricule_etudiant'].value())

        context = {
            'title': title,
            'etudiants': etudiants,
            'form': form,
        }

        #if not form['export_to_TXT'].value():

        if form['export_to_CSV'].value():
            if len(list_selected) > 0:
                print('mes etudiants sont: ', etudiants)
                print("##########")
                print('ma selection est: ', list_selected)

                clauses = (Q(matricule_etudiant__icontains=p) for p in list_selected)
                query = reduce(operator.or_, clauses)
                etudiants = Etudiant.objects.order_by('nom_etudiant').filter(query)

                print("#########ok##")
                print('mes nouveaux étudiants sont: ', etudiants)

                context = {
                    'title': title,
                    'etudiants': etudiants,
                    'form': form,
                    # 'table': table,
                }

            #fichier = HttpResponse(content_type='text/csv')
            fichier = HttpResponse(content_type='application/ms-excel')
            '''writer=csv.writer(fichier)
            writer.writerow(['Matricule', 'Nom', 'Prénom'])'''

            #examen_cours=Examen_cours.objects.all().order_by('etudiant')

            #------------------ajout etudiant--------------------------
            '''for row in etudiants.values_list('matricule_etudiant', 'nom_etudiant', 'prenom_etudiant'):
                print('ma ligne est:', row)
                writer.writerow(row)'''
            #fichier['Content-Disposition'] = 'attachment; filename="liste_etudiants.csv"'

            fichier['Content-Disposition'] = 'attachment; filename="liste_etudiants.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Les étudiants')
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = ['MATRICULE', 'NOM', 'PRENOM']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            #font_style.font.bold = False

            rows = etudiants.values_list('matricule_etudiant', 'nom_etudiant', 'prenom_etudiant').order_by('nom_etudiant')

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, str(row[col_num]), font_style)
            wb.save(fichier)



            return fichier


    return render(request, "maplateforme_app/etudiant_list.html", context)


def etudiant_new(request):
    """
    function view for adding new question
    :param request:
    :type request:
    :return:view on the new question
    :rtype:
    """
    title = "Enregistrement d'un étudiant"

    form = EtudiantForm(request.POST or None)
        #form = EtudiantForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        # form.save_m2m()
        messages.success(request, 'Enregistrement effectué avec succès')
        return redirect('etudiant_list')

    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'maplateforme_app/etudiant_edit.html', context)


# ------------------------------------
def etudiant_edit(request, id=None):
    """
    function view for updating a given question
    :param request:
    :type request:
    :param id:code question of the question to edit
    :type id:
    :return:view on the updated question
    :rtype:
    """
    title = "Modification d'un étudiant"
    instance = get_object_or_404(Etudiant, id=id)
    if request.method == 'POST':
        form = EtudiantFormedit(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()

            messages.success(request, 'Modification effectuée avec succès')
            return redirect('etudiant_list')
    else:
        form = EtudiantFormedit(instance=instance)
        context = {
            'title': title,
            'instance': instance,
            'form': form,
        }
        return render(request, 'maplateforme_app/etudiant_edit.html', context)




def etudiant_delete(request, id=None):
    """
    function view for deleting a given student
    :param request:
    :type request:
    :param id:matricule of the student to delete
    :type id:
    :return:list view of sudents without the deleted student
    :rtype:
    """
    instance = get_object_or_404(Etudiant, id=id)
    instance.delete()
    return redirect("etudiant_list")


# ---------------Reponse-----------------------+-
'''class reponse_list(ListView):
    model = Reponse
    context_object_name = 'reponses'
    '''


# ---------------Filières-----------------------+-

def filiere_list(request):
    """
    function that gives view on the list of specialities
    :param request:
    :return: list view on speciality
    """
    title = "Liste des filières"
    filieres = Filiere.objects.all().order_by('libelle_filiere')
    form = FiliereSearchForm(request.POST or None)
    context = {
        'title': title,
        'filieres': filieres,
        'form': form,
    }
    if request.method == 'POST':
        filieres = Filiere.objects.all().order_by('libelle_filiere').filter(
            libelle_filiere=form['libelle_filiere'].value())
        context = {
            'title': title,
            'filieres': filieres,
            'form': form,
        }
    return render(request, "maplateforme_app/filiere_list.html", context)


def filiere_new(request):
    """
    function view to add a new scope of speciality
    :param request:
    :return: view on new scope of speciality
    """
    title = "Enregistrement d'une filière"
    form = FiliereForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Enregistrement effectué avec succès')
        return redirect('filiere_list')
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'maplateforme_app/filiere_edit.html', context)


def filiere_edit(request, id=None):
    """
    function view to update a scope of speciality
    :param request:
    :param id: name of the speciality to update
    :return: view on the updated speciality
    """
    title = "Modification d'une filière"
    instance = get_object_or_404(Filiere, id=id)
    form = FiliereFormedit(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Modification effectuée avec succès')
        return redirect('filiere_list')
    context = {
        'title': title,
        'instance': instance,
        'form': form,
    }
    return render(request, 'maplateforme_app/filiere_edit.html', context)


def filiere_delete(request, id=None):
    """
    function view for deleting speciality
    :param request:
    :param id: name of speciality to delete
    :return: view on speciality without the deleted speciality
    """
    instance = get_object_or_404(Filiere, id=id)
    instance.delete()
    return redirect("filiere_list")



# ---------------Cours-----------------------+-

def cours_list(request):
    """
    function that gives view on the list of courses
    :param request:
    :return: list view on course
    """
    title = "Liste des cours"
    cours = Cours.objects.all().order_by('libelle_cours')
    form = CoursSearchForm(request.POST or None)
    context = {
        'title': title,
        'cours': cours,
        'form': form,
    }
    if request.method == 'POST':
        cours = Cours.objects.all().order_by('libelle_cours').filter(
            libelle_cours=form['libelle_cours'].value())
        context = {
            'title': title,
            'cours': cours,
            'form': form,
        }
    return render(request, "maplateforme_app/cours_list.html", context)


def cours_new(request):
    """
    function view to add a new scope of course
    :param request:
    :return: view on new scope of course
    """
    title = "Enregistrement d'un cours"
    form = CoursForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Enregistrement effectué avec succès')
        return redirect('cours_list')
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'maplateforme_app/cours_edit.html', context)


def cours_edit(request, id=None):
    """
    function view to update a scope of course
    :param request:
    :param id: name of the course to update
    :return: view on the updated course
    """
    title = "Modification d'un cours"
    instance = get_object_or_404(Cours, id=id)
    form = CoursFormedit(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Modification effectuée avec succès')
        return redirect('cours_list')
    context = {
        'title': title,
        'instance': instance,
        'form': form,
    }
    return render(request, 'maplateforme_app/cours_edit.html', context)


def cours_delete(request, id=None):
    """
    function view for deleting course
    :param request:
    :param id: name of the course to delete
    :return: view on course without the deleted course
    """
    instance = get_object_or_404(Cours, id=id)
    instance.delete()
    return redirect("cours_list")


# ---------------TPs-----------------------+-

def tp_list(request):
    """
    function that gives view on the list of TPs
    :param request:
    :return: list view on TP
    """
    title = "Liste des TPs"
    tps = Travail_pratique.objects.all().order_by('libelle_tp')
    form = Travail_pratiqueSearchForm(request.POST or None)
    context = {
        'title': title,
        'tps': tps,
        'form': form,
    }
    if request.method == 'POST':
        tps = Travail_pratique.objects.all().order_by('libelle_tp').filter(
            libelle_tp=form['libelle_tp'].value())
        context = {
            'title': title,
            'tps': tps,
            'form': form,
        }
    return render(request, "maplateforme_app/tp_list.html", context)


def tp_new(request):
    """
    function view to add a new scope of TP
    :param request:
    :return: view on new scope of TP
    """
    title = "Enregistrement d'un TP"
    form = Travail_pratiqueForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Enregistrement effectué avec succès')
        return redirect('tp_list')
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'maplateforme_app/tp_edit.html', context)


def tp_edit(request, id=None):
    """
    function view to update a scope of TP
    :param request:
    :param id: name of the TP to update
    :return: view on the updated TP
    """
    title = "Modification d'un TP"
    instance = get_object_or_404(Travail_pratique, id=id)
    form = Travail_pratiqueFormedit(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Modification effectuée avec succès')
        return redirect('tp_list')
    context = {
        'title': title,
        'instance': instance,
        'form': form,
    }
    return render(request, 'maplateforme_app/tp_edit.html', context)


def tp_delete(request, id=None):
    """
    function view for deleting TP
    :param request:
    :param id: name of the TP to delete
    :return: view on course without the deleted TP
    """
    instance = get_object_or_404(Travail_pratique, id=id)
    instance.delete()
    return redirect("tp_list")

# ---------------Examen des cours------------------------
def examencours_list(request):
    """
    function view for listing question characteristics
    :param request:
    :return: list view on question characteristics
    """
    title = "Notes d'Informatique 3"
    examencours = Examen_cours.objects.order_by('monetudiant__nom_etudiant')
    form = Examen_coursSearchForm(request.POST or None)

    context = {
        'title': title,
        'examencours': examencours,
        'form': form,
    }

    if request.method == 'POST':

        list_selected= request.POST.getlist('notesetudiants_choisis')
        print("Ma liste selectionnée = ",list_selected)

        if form['matricule_etudiant'].value() :
            #print('matricule_edtudiant = ', form['matricule_etudiant'].value())
            examencours = Examen_cours.objects.order_by('monetudiant__nom_etudiant').filter(
                monetudiant__matricule_etudiant__icontains=form['matricule_etudiant'].value())
        context = {
            'title': title,
            'examencours': examencours,
            'form': form,
        }

        #CSV here is Excel
        if form['export_to_CSV'].value():
            print('OK')
            if len(list_selected) > 0:
                clauses = (Q(monetudiant__matricule_etudiant__icontains=p) for p in list_selected)
                query = reduce(operator.or_, clauses)
                examencours = Examen_cours.objects.order_by('monetudiant__nom_etudiant').filter(query)

                context = {
                    'title': title,
                    'examencours': examencours,
                    'form': form,
                    # 'table': table,
                }

            #fichier = HttpResponse(content_type='text/csv')
            fichier = HttpResponse(content_type='application/ms-excel')

            fichier['Content-Disposition'] = 'attachment; filename="liste_notes_info3.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet("Les notes d'Info 3")
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = ['MATRICULE', 'NOM(S)', 'PRENOM(S)', 'CC/20', 'TPE/20']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            #font_style.font.bold = False

            rows = examencours.values_list('monetudiant__matricule_etudiant', 'monetudiant__nom_etudiant', 'monetudiant__prenom_etudiant'  , 'note_cc', 'note_tpe').order_by('monetudiant__nom_etudiant')
            print('rows= ', rows)

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, str(row[col_num]), font_style)
            wb.save(fichier)

            return fichier


    return render(request, "maplateforme_app/examencours_list.html", context)



def examencours_new(request):
    """
    function view to characterize a question
    :param request:
    :return: view on question with its characteristics
    """
    title = "Enregistrement des notes des étudiants"
    form = Examen_coursForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Enregistrement effectué avec succès')
        return redirect('examencours_list')
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'maplateforme_app/examencours_edit.html', context)


def examencours_edit(request, id=None):
    """
    function view for updating characteristics of a question
    :param request:
    :param id: code question of the question whose characteristics has to be updated
    :return: view on the questions with their characteristics
    """
    title = "Modification des notes d'un étudiant"
    instance = get_object_or_404(Examen_cours, id=id)
    form = Examen_coursFormedit(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()
        messages.success(request, 'Modification effectuée avec succès')
        return redirect('examencours_list')
    context = {
        'title': title,
        'instance': instance,
        'form': form,
    }
    return render(request, 'maplateforme_app/examencours_edit.html', context)


def examencours_delete(request, id=None):
    """
    function view for deleting characteristics of a question
    :param request:
    :param id: code question of the question whose characteristics has to be deleted
    :return: view on characteristics without the deleted characteristics
    """
    instance = get_object_or_404(Examen_cours, id=id)
    instance.delete()
    return redirect("examencours_list")



# ---------------Examen des TPs------------------------
def examentp_list(request):
    """
    function view for listing question characteristics
    :param request:
    :return: list view on question characteristics
    """
    title = 'Notes du TP'
    examentps = Examen_tp.objects.all().order_by('monetudiant__nom_etudiant')
    form = Examen_tpSearchForm(request.POST or None)
    context = {
        'title': title,
        'examentps': examentps,
        'form': form,
    }
    if request.method == 'POST':


        list_selected = request.POST.getlist('notestps_choisis')
        print("Ma liste selectionnée = ", list_selected)

        if form['matricule_etudiant'].value():
            examentps = Examen_cours.objects.all().order_by('monetudiant__nom_etudiant').filter(
                monetudiant__matricule_etudiant__icontains=form['matricule_etudiant'].value())
        context = {
            'title': title,
            'examentps': examentps,
            'form': form,
        }

        # if not form['export_to_TXT'].value():
        #CSV here is Excel

        if form['export_to_CSV'].value():
            print('OK')
            if len(list_selected) > 0:
                print('mes examens cours sont: ', examentps.values_list('monetudiant__matricule_etudiant'))
                print("##########")
                print('ma selection est: ', list_selected)

                clauses = (Q(monetudiant__matricule_etudiant__icontains=p) for p in list_selected)
                query = reduce(operator.or_, clauses)
                examentps = Examen_tp.objects.order_by('monetudiant__nom_etudiant').filter(query)

                print("#########ok##")
                # print('mes nouvelles notes des étudiants sont: ', examencours.va)

                context = {
                    'title': title,
                    'examentps': examentps,
                    'form': form,
                    # 'table': table,
                }

            # fichier = HttpResponse(content_type='text/csv')
            fichier = HttpResponse(content_type='application/ms-excel')

            fichier['Content-Disposition'] = 'attachment; filename="liste_notes_tpinfo3.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet("Les notes de TP d'Info 3")
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = ['MATRICULE', 'NOM(S)', 'PRENOM(S)', 'TP/20']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # font_style.font.bold = False

            rows = examentps.values_list('monetudiant__matricule_etudiant', 'monetudiant__nom_etudiant',
                                           'monetudiant__prenom_etudiant', 'note_tp').order_by(
                'monetudiant__nom_etudiant')
            print('rows= ', rows)

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, str(row[col_num]), font_style)
            wb.save(fichier)

            return fichier



    return render(request, "maplateforme_app/examentp_list.html", context)


def examentp_new(request):
    """
    function view to characterize a TP
    :param request:
    :return: view on question with its characteristics
    """
    title = "Enregistrement des notes de TP des étudiants"
    form = Examen_tpForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Enregistrement effectué avec succès')
        return redirect('examentp_list')
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'maplateforme_app/examentp_edit.html', context)


def examentp_edit(request, id=None):
    """
    function view for updating characteristics of a TP
    :param request:
    :param id: code question of the question whose characteristics has to be updated
    :return: view on the questions with their characteristics
    """
    title = "Modification des notes du TP d'un étudiant"
    instance = get_object_or_404(Examen_tp, id=id)
    form = Examen_tpFormedit(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()
        messages.success(request, 'Modification effectuée avec succès')
        return redirect('examentp_list')
    context = {
        'title': title,
        'instance': instance,
        'form': form,
    }
    return render(request, 'maplateforme_app/examentp_edit.html', context)


def examentp_delete(request, id=None):
    """
    function view for deleting characteristics of a question
    :param request:
    :param id: code question of the question whose characteristics has to be deleted
    :return: view on characteristics without the deleted characteristics
    """
    instance = get_object_or_404(Examen_tp, id=id)
    instance.delete()
    return redirect("examentp_list")





# ---------------Support de Cours-----------------------+-

def supportcours_list(request):
    """
    function that gives view on the list of courses
    :param request:
    :return: list view on course
    """
    title = "Supports des cours"
    supportcours = Support_cours.objects.all().order_by('libelle_support_cours')
    form = Support_coursSearchForm(request.POST or None)
    context = {
        'title': title,
        'supportcours': supportcours,
        'form': form,
    }
    if request.method == 'POST':
        supportcours = Support_cours.objects.all().order_by('libelle_support_cours').filter(
            libelle_support_cours=form['libelle_cours'].value())
        context = {
            'title': title,
            'supportcours': supportcours,
            'form': form,
        }
    return render(request, "maplateforme_app/supportcours_list.html", context)


def supportcours_new(request):
    """
    function view to add a new scope of course
    :param request:
    :return: view on new scope of course
    """
    title = "Enregistrement d'un support de cours"
    if request.method == 'POST':
        form = Support_coursForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enregistrement effectué avec succès')
            return redirect('supportcours_list')
    else:
        form = Support_coursForm()
        context = {
            'title': title,
            'form': form,
        }
        return render(request, 'maplateforme_app/supportcours_edit.html', context)


def supportcours_edit(request, id=None):
    """
    function view to update a scope of course
    :param request:
    :param id: name of the course to update
    :return: view on the updated course
    """
    title = "Modification d'un support de cours"
    instance = get_object_or_404(Support_cours, id=id)
    if request.method == 'POST':
        form = Support_coursFormedit(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, 'Modification effectuée avec succès')
            return redirect('supportcours_list')
    else:
        form = Support_coursFormedit(instance=instance)
        context = {
            'title': title,
            'instance': instance,
            'form': form,
        }
        return render(request, 'maplateforme_app/supportcours_edit.html', context)


def supportcours_delete(request, id=None):
    """
    function view for deleting course
    :param request:
    :param id: name of the course to delete
    :return: view on course without the deleted course
    """
    instance = get_object_or_404(Support_cours, id=id)
    instance.delete()
    return redirect("supportcours_list")




# ---------------Support de TPs-----------------------+-

def supportp_list(request):
    """
    function that gives view on the list of courses
    :param request:
    :return: list view on course
    """
    title = "Supports des TPs"
    supportp = Support_tp.objects.all().order_by('libelle_support_tp')
    form = Support_tpSearchForm(request.POST or None)
    context = {
        'title': title,
        'supportp': supportp,
        'form': form,
    }
    if request.method == 'POST':
        supportp = Support_tp.objects.all().order_by('libelle_support_tp').filter(
            libelle_support_tp=form['libelle_tp'].value())
        context = {
            'title': title,
            'supportp': supportp,
            'form': form,
        }
    return render(request, "maplateforme_app/supportp_list.html", context)


def supportp_new(request):
    """
    function view to add a new scope of course
    :param request:
    :return: view on new scope of course
    """
    title = "Enregistrement d'un support de TP"
    if request.method == 'POST':
        form = Support_tpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enregistrement effectué avec succès')
            return redirect('supportp_list')
    else:
        form = Support_tpForm()
        context = {
            'title': title,
            'form': form,
        }
        return render(request, 'maplateforme_app/supportp_edit.html', context)


def supportp_edit(request, id=None):
    """
    function view to update a scope of course
    :param request:
    :param id: name of the course to update
    :return: view on the updated course
    """
    title = "Modification d'un support de TP"
    instance = get_object_or_404(Support_tp, id=id)
    if request.method == 'POST':
        form = Support_tpFormedit(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, 'Modification effectuée avec succès')
            return redirect('supportp_list')
    else:
        form = Support_tpFormedit(instance=instance)
        context = {
            'title': title,
            'instance': instance,
            'form': form,
        }
        return render(request, 'maplateforme_app/supportp_edit.html', context)


def supportp_delete(request, id=None):
    """
    function view for deleting course
    :param request:
    :param id: name of the course to delete
    :return: view on course without the deleted course
    """
    instance = get_object_or_404(Support_tp, id=id)
    instance.delete()
    return redirect("supportp_list")


#-----------------------VisuQuestion-------------------------------
'''def visuquestion2(request):
    """
    function that gives view on the list of questions
    :param request:
    :return: view on the list of questions
    """
    title = "Visualisation d'une Question"
    questions = Question.objects.all().order_by('question')
    form = VisuQuestionForm(request.POST or None)

    context = {
        'title': title,

        'form': form,
    }
  

    if form['question'].value() in questions:
        #fichier = HttpResponse(content_type='text/plain')
        reponses = Reponse.objects.all().order_by('question')
        operations = Operation.objects.all().order_by('question')
        # parametrages = Parametrage_Machine.objects.all().order_by('libelle_parametrage')
        instance = questions
        instance2 = reponses
        quest = form['question'].value()
        # instance3= parametrages
        # instance4= operations
        # lis=[]
        # ------------------chargement des val de question--------------------------
        for row in instance:
            if quest == row.code_question:
                form['stylequestion'] = row.style_question
                form['typeautorise'] = row.type_autorise
                form['choixpossible'] = row.choix_possible


    return render(request, "ingenumapp/rechercher.html", context)'''


'''def rechercher(request):
    if request.method== 'POST':
        srch= request.POST['srh']

        if srch:
            match= Question.objects.filter(code_question__icontains=srch)
            if match:
                #reponse_query=Reponse.objects.filter(question__code_question__icontains=srch)
                #question_id = request.GET.get(match)
                #print("MATCH = ")
                #print(match)
                question_id= match.first()
                reponse_query = set(
                    Operation.objects.filter(question=question_id).order_by('libelle_operation'))
                    caracterisation_query = set(
                    Caracterisation.objects.filter(question=question_id).order_by('question'))
                #results= chain(match, reponse_query)
                #if reponse_query:
               # print(reponse_query)

                #print('MATCH')
                return  render(request, 'ingenumapp/rechercher.html', {'sr': match, 'rep': reponse_query, 'caract': caracterisation_query})
            else:
                print('NO MATCH')
                messages.error(request, 'question inexistante')
        else:
            return HttpResponseRedirect('/rechercher')

    return  render(request, 'ingenumapp/rechercher.html')'''


#----------------------------vue de l'impetrant ------------------------------
'''def impetrant(request):
    title = 'Ma Session de questions'
    mes_sessions = Sessions.objects.all().order_by('date_session').filter(user= request.user).distinct()
    #instance=questions
    #form = QuestionSearchForm(request.POST or None)
    context = {
        'title': title,
        'mes_sessions': mes_sessions,
        # 'table' : table,
    }

    return  render(request, 'ingenumapp/impetrant.html', context)'''


#--------------------
'''def media(request):
    """
    function that gives view on the list of questions
    :param request:
    :return: view on the list of questions
    """
    #choix=[]
    title = 'Liste des fichiers'
    questions = Question.objects.all().order_by('code_question')
    mon_fichier = open('contenu_questions.txt', 'w+')
    #file_contents = f.read()
    #print(file_contents)
    #f.close()

    questions_session = BytesIO()
    zip_questions = zipfile.ZipFile(questions_session, 'w')
    #current_directory = str(pathlib.Path().absolute())
    #zip_questions = zipfile.ZipFile('mes_questions.zip', 'w')


    quest_domaine=questions
    instance = questions
    form = QuestionSearchForm(request.POST or None)
    #table= QuestionTable(Question.objects.all())
    context = {
        'title': title,
        'questions': questions,
        'form': form,
        #'table' : table,
    }



    if request.method == 'POST':
        list_candidat = request.POST.getlist('questions_candidat')
        # print(quest_selected)
        # if form.Meta.model.code_question=="":
        # print("choix")

        dom = 0  # domaine vide
        niv = 0  # niveau vide->niv=0, niveau choisi->niv=1
        if form['domaine'].value():
            questions = Question.objects.all().order_by('code_question').filter(
                domaine=form['domaine'].value())
            quest_domaine = questions
            dom = 1  # domaine sélectionné
            print(questions)

        if form['code_question'].value():
            if dom == 0:
                questions = Question.objects.all().order_by('code_question').filter(
                    code_question__icontains=form['code_question'].value())
            else:
                questions = quest_domaine.all().order_by('code_question').filter(
                    code_question__icontains=form['code_question'].value())



        context = {
            'title': title,
            'questions': questions,
            'form': form,
            # 'table': table,
        }

        # if not form['export_to_TXT'].value():

        if form['export_to_TXT'].value():
            if len(list_candidat) > 0:
                print(questions)
                print("##########")
                print(list_candidat)

                clauses = (Q(code_question__icontains=p) for p in list_candidat)
                query = reduce(operator.or_, clauses)
                questions = Question.objects.filter(query)

                print("#########ok##")
                print(questions)

                context = {
                    'title': title,
                    'questions': questions,
                    'form': form,
                    # 'table': table,
                }

            #fichier = HttpResponse(content_type='text/plain')

            reponses = Reponse.objects.all().order_by('question')
            operations = Operation.objects.all().order_by('question')
            caracterisations = Caracterisation.objects.all().order_by('niveau')


            # ------------------ajout question--------------------------
            print('row1= ', questions)
            for row in questions:

                #fichier.write("******************************************************** \n")
                #fichier.write(str(row.code_question) +"\n")
                #print('row= ', questions)
                mon_fichier.write(str(row.code_question) +"\n")

                if str(row.domaine) != "None":
                    mon_fichier.write(str(row.domaine) + " ")

                mes_param = [str(elem) for elem in list(row.parametres_question.all().order_by('param'))]
                if len(mes_param) > 0:
                    for para in mes_param:
                        mon_fichier.write(para + " ")
                #fichier.write("\n")


                mes_types = [str(elem) for elem in list(row.type_question.all())]
                if len(mes_types) > 0:
                    for typequest in mes_types:
                        mon_fichier.write(typequest + " ")

                if str(row.etat_question) != "None":
                    mon_fichier.write(str(row.etat_question) + " ")

                # --------------------------Ajout du Niveau, du Type_caractérisation, de la Difficulté et de l'Importance d'une Caractérisation--------------------
                trouve=True
                for row4 in caracterisations:
                    mes_quescaract = [str(elem) for elem in list(row4.question.all())]
                    #print(mes_quescaract)
                    #print("\n")
                    if row.code_question in mes_quescaract :
                        #if (str(row4.niveau) != "None") or (str(row4.type_caracterisation) != "None") or (str(row4.difficulte) != "None") or (str(row4.duree) != "None"):
                            if trouve==True:
                                mon_fichier.write("\n")

                            if (str(row4.niveau) != "None"):
                                mon_fichier.write(str(row4.niveau) + " ")

                            if (str(row4.type_caracterisation) != "None"):
                                mon_fichier.write(str(row4.type_caracterisation) + " ")

                            if str(row4.difficulte) != "None":
                                mon_fichier.write(str(row4.difficulte) + " ")

                            if str(row4.importance) != "None":
                                mon_fichier.write(str(row4.importance) + " ")

                            if str(row4.duree) != "None":
                                mon_fichier.write(str(row4.duree) + " ")

                            trouve=False




                # --------------------------ajout_reponse--------------------
                for row2 in reponses:
                    if str(row2.question) == str(row.code_question):
                        mes_spec = [str(spec) for spec in list(row2.specification.all())]

                        if (str(row2.parametre) != "None") or (len(mes_spec)>0) :
                            mon_fichier.write("\n")

                            if str(row2.parametre) != "None":
                                mon_fichier.write(" " + str(row2.parametre))

                            #mes_spec = [str(spec) for spec in list(row2.specification.all())]
                            if len(mes_spec) > 0:
                                mon_fichier.write(" (")
                                for i, specif in enumerate(mes_spec):
                                    mon_fichier.write(specif)
                                    if i < len(mes_spec) - 1:
                                        mon_fichier.write(";")
                                mon_fichier.write(")")
                        # -------------------ajout operation----------------------------------------
                        #fichier.write("\n")
                        mes_op = [str(op) for op in list(row2.operation.all())]
                        #print(mes_op)
                        if len(mes_op) > 0:
                            for operation in mes_op:
                                mon_fichier.write("\n")
                                mon_fichier.write(operation)


                # -----------Contexte 1,2,3,4--------------------------------
                if (bool(row.contexte1) == True) or (bool(row.contexte3) == True) or (
                        bool(row.contexte4) == True):
                    mon_fichier.write("\n")

                    if bool(row.contexte1) == True:
                        nom_fstl = row.contexte1.path
                        zip_questions.write(nom_fstl, basename(nom_fstl))
                        mon_fichier.write(str(row.contexte1.name) + " ")

                    if bool(row.contexte3) == True:
                        nom_fct3 = row.contexte3.path
                        zip_questions.write(nom_fct3, basename(nom_fct3))
                        mon_fichier.write(str(row.contexte3.name) + " ")

                    if bool(row.contexte4) == True:
                        nom_fct4 = row.contexte4.path
                        zip_questions.write(nom_fct4, basename(nom_fct4))
                        mon_fichier.write(str(row.contexte4.name) + " ")



                    # -----------Question sous forme image---------------
                if bool(row.image_question) == True:
                    mon_fichier.write("\n")
                    nom_image = row.image_question.path
                    zip_questions.write(nom_image, basename(nom_image))
                    # fichier.write(str(row.image_question.name)+"\n")
                    mon_fichier.write(str(row.image_question.name))

                # -------------Choix possible & choix autorisé-----------------------
                if str(row.choix_possible) != "None":
                    mon_fichier.write("\n")
                    mon_fichier.write(str(row.choix_possible) + " ")
                if str(row.choix_autorise) != "None":
                    mon_fichier.write(str(row.choix_autorise))

                #fichier.write("\n")
                mon_fichier.write("\n")

                # fichier.write("\n")
            #for line in fichier.

            #fichier['Content-Disposition'] = 'attachment; filename="liste_candidat.txt"'


            mon_fichier.close()
            #nom_fichier = '/media/liste_candidat.txt'
            zip_questions.write('contenu_questions.txt')
            zip_questions.close()

            resp = HttpResponse(questions_session.getvalue(), content_type="application/x-zip-compressed")
            resp['Content-Disposition'] = 'attachment; filename=Questions_session.zip'

            return resp


            # else:
            #   id_list = request.POST.getlist('choices', default=None)
            #  print(id_list)


    return render(request, "ingenumapp/media.html", context)


def trouve_question(Tableau, maquestion):
    trouve=False
    i=0
    while (i<len(Tableau)) and trouve==False :
        if Tableau[i]==maquestion:
            trouve=True

        i+=1

    return  trouve'''


'''def trouve_Tquestion(GQ, Tableau) :
    reponse = False

    i = 0
    while (i < len(GQ)) and (reponse == False):
        nbre = 0
        j=0
        #trouve=False
        print('GQ_i= ', GQ[i])
        print('Tableau= ', Tableau)
        while(j<len(Tableau)):
            if trouve_question(GQ[i], Tableau[j]) == True:
                # print("elt present")
                nbre += 1

            j+=1
        print('nombre= ', nbre)
        if(nbre==len(GQ[i])):
            print('OUI, TABLEAU PRESENT')
            reponse=True

        i += 1


    return reponse'''







# ---------------Sessions de questions------------------------
'''def sessions_list(request):
    """
    function view for listing Sesssions of questions
    :param request:
    :return: list view on question characteristics
    """
    title = 'Liste des Sessions'
    sessions = set(Sessions.objects.all().order_by('date_session'))
    form = SessionsSearchForm(request.POST or None)
    context = {
        'title': title,
        'sessions': sessions,
        'form': form,
    }
    if request.method == 'POST':
        sessions = Sessions.objects.all().order_by('date_session').filter(
            date_session=form['date_session'].value())
        context = {
            'title': title,
            'sessions': sessions,
            'form': form,
        }
    return render(request, "ingenumapp/sessions_list.html", context)



def sessions_new(request):
    """
    function view to characterize a question
    :param request:
    :return: view on question with its characteristics
    """
    title = "Enregistrement d'une Session de questions"
    if request.method == 'POST':
        # form = QuestionForm(request.POST or None)
        form = SessionsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # form.save_m2m()
            messages.success(request, 'Enregistrement effectué avec succès')
            return redirect('sessions_list')
    else:
        form = SessionsForm()
        context = {
            'title': title,
            'form': form,
        }
        return render(request, 'ingenumapp/sessions_edit.html', context)


def sessions_edit(request, id=None):
    """
    function view to update a scope of question (application domain)
    :param request:
    :param id: name of the application domain to update
    :return: view on the updated application domain
    """
    title = "Modification d'une Session de questions"
    instance = get_object_or_404(Sessions, id=id)
    if request.method == 'POST':
        form = SessionsFormedit(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()

            messages.success(request, 'Modification effectuée avec succès')
            return redirect('sessions_list')
    else:
        form = SessionsFormedit(instance=instance)
        context = {
            'title': title,
            'instance': instance,
            'form': form,
        }
        return render(request, 'ingenumapp/sessions_edit.html', context)


def sessions_delete(request, id=None):
    """
    function view for deleting an application domain
    :param request:
    :param id: name of application domain to delete
    :return: view on application domains without the deleted application domain
    """
    instance = get_object_or_404(Sessions, id=id)
    instance.delete()
    return redirect("sessions_list")
'''


