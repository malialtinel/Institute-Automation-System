from django import forms

from .models import *


class QuotaChangeForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = {
            'quota',
        }

class AddNewSection(forms.ModelForm):

	class Meta:

		model = Section
		fields = '__all__'

class Grade2Student(forms.ModelForm):

	class Meta:

		model = CompletedCourse
		fields = ['grade', 'act_course']


class OpenNewSection(forms.ModelForm):

	class Meta:

		model = Section

		exclude  = ['special_quota', 'students', 'year']

class ScheduleApproveOrReject(forms.ModelForm):

	class Meta:

		model = TakenCourse

		fields = '__all__'

	