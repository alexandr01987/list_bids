# -*- coding: utf-8 -*-

from django import forms
from .models import ErrorSolvo, RevisionSolvo, BugSolvo, CommentRequestSolvo


class FormError(forms.ModelForm):
    class Meta:
        model = ErrorSolvo
        fields = ('solvo_number', 'subject', 'description', 'solvo_registered_date', 'comment', 'status')
        widgets = {
            'solvo_number': forms.TextInput(attrs={'rows': 1, 'cols': 30, 'readonly': 'readonly'}),
            'subject': forms.TextInput(attrs={'size': 100, 'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'rows': 12, 'cols': 150}),
            'comment': forms.Textarea(attrs={'rows': 2, 'cols': 60}),
            # 'solvo_registered_date': forms.SelectDateWidget()
        }
        labels = {
            'solvo_number': 'Номер заявки Солво',
            'subject': 'Тема',
            'description': 'Описание',
            'comment': 'Комментарий к заявке',
            'solvo_registered_date': 'Дата регистрации',
            'status': 'Статус',
        }


class FormRevision(forms.ModelForm):
    class Meta:
        model = RevisionSolvo
        fields = ('solvo_number', 'solvo_revision_number', 'subject', 'description', 'solvo_registered_date',
                  'hours_for_develop', 'deadline_date', 'is_accelerated', 'comment', 'status')
        widgets = {
            'solvo_number': forms.TextInput(attrs={'readonly': 'readonly'}),
            'solvo_revision_number': forms.TextInput(attrs={'size': 100, 'readonly': 'readonly'}),
            'subject': forms.TextInput(attrs={'size': 130}),
            'description': forms.Textarea(attrs={'rows': 6, 'cols': 150}),
            'comment': forms.Textarea(attrs={'rows': 3, 'cols': 60}),
            'hours_for_develop': forms.NumberInput(attrs={'min': 0}),
            # 'solvo_registered_date': forms.SelectDateWidget(),
            'deadline_date': forms.SelectDateWidget()
        }
        labels = {
            'solvo_number': 'Номер заявки Солво',
            'solvo_revision_number': 'Номер доработки Солво',
            'subject': 'Тема',
            'description': 'Описание',
            'comment': 'Комментарий к заявке',
            'solvo_registered_date': 'Дата регистрации',
            'status': 'Статус',
            'hours_for_develop': 'Человекочасов для выполнения',
            'deadline_date': 'Срок выполнения',
            'is_accelerated': 'Ускоренная',
        }


class FormBug(forms.ModelForm):
    """
    Форма для бага
    """
    class Meta:
        model = BugSolvo
        fields = ['date_registered', 'critical_state', 'status']
        # widgets = {
        #     'date_registered': forms.SelectDateWidget()
        # }
        labels = {
            'date_registered': 'Дата фиксации',
            'critical_state': 'Уровень критичности',
            'status': 'Статус',
        }


class FormCommentOnRequest(forms.ModelForm):
    """
    Форма для комментов
    """
    class Meta:
        model = CommentRequestSolvo
        fields = ('comment_to_request', )