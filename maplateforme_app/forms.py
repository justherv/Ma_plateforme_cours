
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.db import models
from crispy_forms.layout import Div, Field, Row, Submit, Button, Column
from model_utils import Choices

from .models import Etudiant, Travail_pratique, Examen_cours, Examen_tp, Filiere, Cours, Support_cours, Support_tp

from .mychoices import *

class EtudiantForm(forms.ModelForm):
    """
    Class form for a new question
    """

    class Meta:
        model = Etudiant
        #param= forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=Parametres)

        fields= ['filiere', 'matricule_etudiant', 'nom_etudiant', 'prenom_etudiant','photo_etudiant'
                 ]

    def clean_matricule_etudiant(self):  # Validates the Computer Name Field<br>
        matricule_etudiant = self.cleaned_data.get('matricule_etudiant')
        if (matricule_etudiant == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')

        for instance in Etudiant.objects.all():
            if instance.matricule_etudiant == matricule_etudiant:
                raise forms.ValidationError(matricule_etudiant+ ' est déjà ajouté')
        return matricule_etudiant


class EtudiantFormedit(forms.ModelForm):
    """
    Class form for updating question
    """

    class Meta:
        model = Etudiant
        fields = ['filiere','matricule_etudiant', 'nom_etudiant', 'prenom_etudiant','photo_etudiant'
                 ]

    def clean_matricule_etudiant(self):  # Validates the Computer Name Field<br>
        matricule_etudiant = self.cleaned_data.get('matricule_etudiant')
        if (matricule_etudiant == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')
        return matricule_etudiant


class EtudiantSearchForm(forms.ModelForm):
    """
    Class form for searching student
    """

    def __init__(self, *args, **kwargs):
        '''IMPORTANCE_CHOICES = Choices(
            ('', '',''),
            (0, 'low', 0),
            (1, 'normal', 1),
            (2, 'normal', 2),
            (3, 'high', 3),
            (4, 'high', 4),
            (5, 'high', 5)
        )'''

        #niveau = kwargs.pop('niveau', '')
        super(EtudiantSearchForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Etudiant
        fields = ['filiere','matricule_etudiant', 'export_to_CSV']



#---------------Filiere----------------------
class FiliereForm(forms.ModelForm):
    """
    Class form for a new application domain
    """
    class Meta:
        model = Filiere
        fields = ['libelle_filiere']

    def clean_libelle_filiere(self):  # Validates the Computer Name Field<br>
        filiere = self.cleaned_data.get('libelle_filiere')
        if (filiere == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')

        for instance in Filiere.objects.all():
            if instance.libelle_filiere== filiere:
                raise forms.ValidationError(filiere + ' est déjà ajouté')
        return filiere

class FiliereFormedit(forms.ModelForm):
    """
    Class form for updating an application domain
    """
    class Meta:
        model = Filiere
        fields = ['libelle_filiere']

    def clean_libelle_filiere(self):  # Validates the Computer Name Field<br>
        filiere = self.cleaned_data.get('libelle_filiere')
        if (filiere == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')
        return filiere

class FiliereSearchForm(forms.ModelForm):
    """
    Class form for searching an application domain
    """
    class Meta:
        model = Filiere
        fields = ['libelle_filiere']



#---------------Cours----------------------
class CoursForm(forms.ModelForm):
    """
    Class form for a new course
    """
    class Meta:
        model = Cours
        fields = ['libelle_cours']

    def clean_libelle_cours(self):  # Validates the Computer Name Field<br>
        cours = self.cleaned_data.get('libelle_cours')
        if (cours == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')

        for instance in Cours.objects.all():
            if instance.libelle_cours== cours:
                raise forms.ValidationError(cours + ' est déjà ajouté')
        return cours

class CoursFormedit(forms.ModelForm):
    """
    Class form for updating a course
    """
    class Meta:
        model = Cours
        fields = ['libelle_cours']

    def clean_libelle_cours(self):  # Validates the Computer Name Field<br>
        cours = self.cleaned_data.get('libelle_cours')
        if (cours == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')
        return cours

class CoursSearchForm(forms.ModelForm):
    """
    Class form for searching course
    """
    class Meta:
        model = Cours
        fields = ['libelle_cours']


#---------------TP----------------------
class Travail_pratiqueForm(forms.ModelForm):
    """
    Class form for a new TP
    """
    class Meta:
        model = Travail_pratique
        fields = ['libelle_tp']

    def clean_libelle_tp(self):  # Validates the Computer Name Field<br>
        tp = self.cleaned_data.get('libelle_tp')
        if (tp == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')

        for instance in Travail_pratique.objects.all():
            if instance.libelle_tp== tp:
                raise forms.ValidationError(tp + ' est déjà ajouté')
        return tp

class Travail_pratiqueFormedit(forms.ModelForm):
    """
    Class form for updating a TP
    """
    class Meta:
        model = Travail_pratique
        fields = ['libelle_tp']

    def clean_libelle_tp(self):  # Validates the Computer Name Field<br>
        tp = self.cleaned_data.get('libelle_tp')
        if (tp == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')
        return tp

class Travail_pratiqueSearchForm(forms.ModelForm):
    """
    Class form for searching TP
    """
    class Meta:
        model = Travail_pratique
        fields = ['libelle_tp']


#---------------Examen des cours------------------------
class Examen_coursForm(forms.ModelForm):
    """
    Class form for exam
    """
    #delivery_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    class Meta:
        model = Examen_cours
        fields = ['monetudiant','cours', 'note_cc', 'note_tpe', 'note_synthese']

    def clean_monetudiant(self):  # Validates the Computer Name Field<br>
        monetudiant = self.cleaned_data.get('monetudiant')
        if (monetudiant == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')

        for instance in Examen_cours.objects.all():
            if instance.monetudiant== monetudiant:
                raise forms.ValidationError(monetudiant + ' est déjà ajouté')
        return monetudiant

class Examen_coursFormedit(forms.ModelForm):
    """
    Class form for updating exam
    """
    class Meta:
        model = Examen_cours
        fields = ['monetudiant','cours', 'note_cc', 'note_tpe', 'note_synthese']

    def clean_monetudiant(self):  # Validates the Computer Name Field<br>
        monetudiant = self.cleaned_data.get('monetudiant')
        if (monetudiant == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')
        return monetudiant

#class Examen_coursSearchForm(forms.ModelForm):
class Examen_coursSearchForm(EtudiantSearchForm):
    """
    Class form for searching exam
    """
    def __init__(self, *args, **kwargs):
        '''IMPORTANCE_CHOICES = Choices(
            ('', '',''),
            (0, 'low', 0),
            (1, 'normal', 1),
            (2, 'normal', 2),
            (3, 'high', 3),
            (4, 'high', 4),
            (5, 'high', 5)
        )'''

        #niveau = kwargs.pop('niveau', '')
        #super(Examen_coursSearchForm, self).__init__(*args, **kwargs)
        super(EtudiantSearchForm, self).__init__(*args, **kwargs)


    class Meta:
        model= Etudiant
        fields =['matricule_etudiant', 'export_to_CSV']
        '''model = Examen_cours
        fields = ['monetudiant', 'export_to_EXCEL']'''


#---------------Examen des TPs------------------------
class Examen_tpForm(forms.ModelForm):
    """
    Class form for TP exam
    """
    #delivery_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    class Meta:
        model = Examen_tp
        fields = ['monetudiant','tp', 'note_tp']

    def clean_monetudiant(self):  # Validates the Computer Name Field<br>
        monetudiant = self.cleaned_data.get('monetudiant')
        if (monetudiant == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')

        for instance in Examen_tp.objects.all():
            if instance.monetudiant== monetudiant:
                raise forms.ValidationError(monetudiant + ' est déjà ajouté')
        return monetudiant

class Examen_tpFormedit(forms.ModelForm):
    """
    Class form for updating TP exam
    """
    class Meta:
        model = Examen_tp
        fields = ['monetudiant','tp', 'note_tp']

    def clean_etudiant(self):  # Validates the Computer Name Field<br>
        monetudiant = self.cleaned_data.get('monetudiant')
        if (monetudiant == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')
        return monetudiant

class Examen_tpSearchForm(EtudiantSearchForm):
    """
    Class form for searching TP exam
    """

    def __init__(self, *args, **kwargs):

        super(EtudiantSearchForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Etudiant
        fields = ['matricule_etudiant', 'export_to_CSV']






#---------------Supports des cours------------------------
class Support_coursForm(forms.ModelForm):
    """
    Class form for exam
    """
    #delivery_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    class Meta:
        model = Support_cours
        fields = ['cours', 'libelle_support_cours', 'fichier_support_cours']

    def clean_libelle_support_cours(self):  # Validates the Computer Name Field<br>
        libelle_support_cours = self.cleaned_data.get('libelle_support_cours')
        if (libelle_support_cours == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')

        for instance in Support_cours.objects.all():
            if instance.libelle_support_cours== libelle_support_cours:
                raise forms.ValidationError(libelle_support_cours + ' est déjà ajouté')
        return libelle_support_cours

class Support_coursFormedit(forms.ModelForm):
    """
    Class form for updating exam
    """
    class Meta:
        model = Support_cours
        fields = ['cours', 'libelle_support_cours', 'fichier_support_cours']

    def clean_libelle_support_cours(self):  # Validates the Computer Name Field<br>
        libelle_support_cours = self.cleaned_data.get('libelle_support_cours')
        if (libelle_support_cours == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')
        return libelle_support_cours

class Support_coursSearchForm(forms.ModelForm):
    """
    Class form for searching exam
    """
    def __init__(self, *args, **kwargs):
        '''IMPORTANCE_CHOICES = Choices(
            ('', '',''),
            (0, 'low', 0),
            (1, 'normal', 1),
            (2, 'normal', 2),
            (3, 'high', 3),
            (4, 'high', 4),
            (5, 'high', 5)
        )'''

        #niveau = kwargs.pop('niveau', '')
        super(Support_coursSearchForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Support_cours
        fields = ['libelle_support_cours']



#---------------Supports des TPs------------------------
class Support_tpForm(forms.ModelForm):
    """
    Class form for exam
    """
    #delivery_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    class Meta:
        model = Support_tp
        fields = ['tp', 'libelle_support_tp', 'fichier_support_tp']

    def clean_libelle_support_tp(self):  # Validates the Computer Name Field<br>
        libelle_support_tp = self.cleaned_data.get('libelle_support_tp')
        if (libelle_support_tp == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')

        for instance in Support_tp.objects.all():
            if instance.libelle_support_tp== libelle_support_tp:
                raise forms.ValidationError(libelle_support_tp + ' est déjà ajouté')
        return libelle_support_tp


class Support_tpFormedit(forms.ModelForm):
    """
    Class form for updating exam
    """
    class Meta:
        model = Support_tp
        fields = ['tp', 'libelle_support_tp', 'fichier_support_tp']

    def clean_libelle_support_tp(self):  # Validates the Computer Name Field<br>
        libelle_support_tp = self.cleaned_data.get('libelle_support_tp')
        if (libelle_support_tp == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')
        return libelle_support_tp

class Support_tpSearchForm(forms.ModelForm):
    """
    Class form for searching exam
    """
    def __init__(self, *args, **kwargs):
        '''IMPORTANCE_CHOICES = Choices(
            ('', '',''),
            (0, 'low', 0),
            (1, 'normal', 1),
            (2, 'normal', 2),
            (3, 'high', 3),
            (4, 'high', 4),
            (5, 'high', 5)
        )'''

        #niveau = kwargs.pop('niveau', '')
        super(Support_tpSearchForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Support_tp
        fields = ['libelle_support_tp']



#------------------------------
'''class VisuQuestionForm(forms.ModelForm):
    """
    Class form for a new application domain
    """
    class Meta:
        model = VisuQuestion
        fields = ['question', 'domaine', 'type', 'choixpossible', 'choixautorise', 'operation', 'imagequestion']
        #readonly=('operation', 'stylequestion', 'typeautorise', 'choixpossible', 'choixautorise',)
        forms.CharField(disabled=True)


    def clean_libelle_operation(self):  # Validates the Computer Name Field<br>
        operation = self.cleaned_data.get('libelle_operation')
        if (operation == ""):
            raise forms.ValidationError('Cet élément ne peut être vide')

        for instance in Operation.objects.all():
            if instance.libelle_operation== operation:
                raise forms.ValidationError(operation + ' est déjà ajouté')
        return operation

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['operation'].queryset = Operation.objects.none()

        #self.fields['libelle_parametrage'].queryset = Parametrage_Machine.objects.none()

        if 'question' in self.data:
            try:
                maquestion = int(self.data.get('question'))
                self.fields['operation'].queryset = Operation.objects.filter(question=maquestion).order_by(
                    'question')
                #self.fields['libelle_parametrage'].queryset = Parametrage_Machine.objects.filter(question=maquestion).order_by('question')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            #print("ok1")
            self.fields['operation'].queryset = self.instance.question.operation_set.order_by('libelle_operation')
            #self.fields['libelle_parametrage'].queryset = self.instance.question.parametrage_machine_set.order_by('libelle_parametrage')



class VisuQuestionSearchForm(forms.ModelForm):
    """
    Class form for searching an application domain
    """
    class Meta:
        model = VisuQuestion
        fields = ['question']
'''


'''class ExamSearchForm(forms.ModelForm):
    """
    Class form for searching question
    """
    
    def __init__(self, *args, **kwargs):
        
        super(ExamSearchForm, self).__init__(*args, **kwargs)
        self.fields['niveau'] = forms.ModelChoiceField(queryset=Niveau.objects.all(), required=False, label='Niveau')
        self.fields['type'] = forms.ChoiceField(choices=CARACTYPE_CHOICES, label='Type', initial='', required=False)
        self.fields['diff'] = forms.ChoiceField(choices=DIFF_CHOICES, label='Difficulté', initial='', required=False)
        self.fields['import'] = forms.ChoiceField(choices=IMPORT_CHOICES, label='Importance', initial='', required=False)
        self.fields['duree'] = forms.TimeField(initial='00:00:00', required=False, label='Durée', help_text='Fomat Heure:Minute:Seconde(HH:MM:SS)')
        self.fields['epsi'] = forms.TimeField(initial='00:00:00', required=False, label='Epsilon', help_text='Marge d\'erreur au format Heure:Minute:Seconde(HH:MM:SS)')
        self.fields['export_to_TXT']=forms.BooleanField(required= False, initial=False, label="Cochez pour exporter")
        

    class Meta:
        model = Question
        fields = ['domaine','code_question']
'''


#---------------Caractérisation de questions------------------------
'''class SessionsForm(forms.ModelForm):
    """
    Class form for characterising questions
    """
    class Meta:
        model = Sessions
        fields = ['date_session', 'questions', 'user']

    def clean_date_session(self):  # Validates the Computer Name Field<br>
        date_session = self.cleaned_data.get('date_session')
        return date_session


class SessionsFormedit(forms.ModelForm):
    """
    Class form for updating an application domain
    """
    class Meta:
        model = Sessions
        fields = ['date_session', 'questions', 'user']

    def clean_date_session(self):  # Validates the Computer Name Field<br>
        date_session = self.cleaned_data.get('date_session')
        return date_session

class SessionsSearchForm(forms.ModelForm):
    """
    Class form for searching question Sessions
    """
    class Meta:
        model = Sessions
        fields = ['date_session']
'''


