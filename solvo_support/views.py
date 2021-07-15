# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.response import Response
from datetime import datetime
from .models import RequestSolvo, ErrorSolvo, RevisionSolvo, EmailSolvo, BugSolvo, RequestBugSolvo, Status
from .forms import FormError, FormRevision, FormBug, FormCommentOnRequest
import solvo_support.advanced_procedures as adv_proc
from .serializers import RequestSolvoSerializer

# Create your views here.

classes_for_list_dict = {
    'error': {'class_name': ErrorSolvo, 'form_name': FormError, 'ru_name': 'ошибки'},
    'revision': {'class_name': RevisionSolvo, 'form_name': FormRevision, 'ru_name': 'доработки'},
}


def get_revision_or_error_by_solvo_number(solvo_request_id):
    """
    получить доработку или ошибку по за id заявки

    :param solvo_request_id:  номер заявки Солво
    :return:
    """
    try:
        full_info_request = classes_for_list_dict['revision']['class_name'].objects.get(solvo_number=solvo_request_id)
    except ObjectDoesNotExist:
        try:
            full_info_request = classes_for_list_dict['error']['class_name'].objects.get(solvo_number=solvo_request_id)
        except ObjectDoesNotExist:
            raise Http404
    return full_info_request


def index(request):
    """
    главная страница приложения

    :param request:
    :return:
    """
    now = datetime.now()
    if 6 <= now.hour < 13:
        hello_word = 'Доброго утра'
    elif 13 <= now.hour < 17:
        hello_word = 'Доброго дня'
    elif 17 <= now.hour < 24:
        hello_word = 'Доброго вечера'
    else:
        hello_word = 'Доброй ночи'
    # if
    context = {'hello_word': hello_word}
    return render(request, 'solvo_support/index.html', context)


def find_requests_by_text(request):
    """
    поиск заявок по текстовому запросу

    :param request:
    :return:
    """
    import re
    list_found_requests = []
    set_found_nums = set()
    all_emails = EmailSolvo.objects.all()
    context = dict()
    if request.method == 'POST':
        search_text = request.POST.get('search_box', None)
        find_re = re.compile(search_text.lower())
        if find_re is not None:
            for email in all_emails:
                if find_re.search(email.body_email.lower()) and email.request_solvo.solvo_number not in set_found_nums:
                    found_request = get_revision_or_error_by_solvo_number(email.request_solvo.solvo_number)
                    list_found_requests.append(found_request)
                    set_found_nums.add(email.request_solvo.solvo_number)
        context['solvo_requests_list'] = list_found_requests
        context['type_requests'] = 'found_by_emails'
        context['key_word'] = search_text
        context['h1_body_header'] = f'Поиск в письмах по тексту "{search_text}"'
    return render(request, 'solvo_support/search_in_emails.html', context)


@permission_required('solvo_support.view_requestsolvo')
def list_requests(request, status_requests, type_requests):
    """
    список заявок Солво

    :param request:
    :param status_requests:
    :param type_requests:
    :return:
    """
    # классы для получения заявок
    solvo_requests_list = []  # список для возврата
    if status_requests == 'everyone':
        if type_requests != 'all' and type_requests in classes_for_list_dict.keys():
            solvo_requests_list = get_list_or_404(classes_for_list_dict[type_requests]['class_name'])
            h1_body_header = classes_for_list_dict[type_requests]['ru_name']
        else:
            for request_info in classes_for_list_dict.values():
                db_requests = list(request_info['class_name'].objects.all())
                solvo_requests_list.extend(db_requests)
            h1_body_header = 'Все заявки'
    elif status_requests == 'actual':
        if type_requests != 'all' and type_requests in classes_for_list_dict.keys():
            solvo_requests_list = get_list_or_404(classes_for_list_dict[type_requests]['class_name'].actual_requests)
            h1_body_header = f"Актуальные {classes_for_list_dict[type_requests]['ru_name']}"
        else:
            for request_info in classes_for_list_dict.values():
                db_requests = list(request_info['class_name'].actual_requests.all())
                solvo_requests_list.extend(db_requests)
            h1_body_header = 'Все актуальные заявки'
    else:
        raise Http404

    context = {'solvo_requests_list': solvo_requests_list,
               'status_requests': status_requests,
               'type_requests': type_requests,
               'h1_body_header': h1_body_header.capitalize(),
               }
    return render(request, 'solvo_support/list_requests.html', context)


@permission_required('solvo_support.view_requestsolvo')
def request_details(request, type_request, solvo_number):
    """
    детали заявки

    :param request:
    :param type_request:
    :param solvo_number:
    :return:
    """
    if type_request in classes_for_list_dict.keys():
        solvo_request = get_object_or_404(classes_for_list_dict[type_request]['class_name'],
                                          solvo_number=solvo_number
                                          )
        bugs_by_request = [req_bug.bug for req_bug in RequestBugSolvo.objects.filter(request=solvo_request)]
    else:
        raise Http404

    if request.method == 'POST':
        form = classes_for_list_dict[type_request]['form_name'](request.POST)
        if form.is_valid():
            solvo_request = classes_for_list_dict[type_request]['class_name'].objects.get(solvo_num_request=solvo_number)
            solvo_request.status = Status.objects.get(pk=request.POST['status'])
            solvo_request.save()
    else:
        form = classes_for_list_dict[type_request]['form_name'](instance=solvo_request)

    context = {'solvo_request': solvo_request,
               'type_request': type_request,
               'form': form,
               'bugs_by_request': bugs_by_request
               }

    return render(request, 'solvo_support/request_details.html', context)


@permission_required('solvo_support.change_requestsolvo')
def change_request(request, type_request, solvo_request_number):
    """
    изменить заявку Солво

    :param request:
    :param type_request:
    :param solvo_request_number:
    :return:
    """
    request_solvo = get_object_or_404(classes_for_list_dict[type_request]['class_name'],
                                      solvo_number=solvo_request_number)
    if request.method == 'POST':
        form = classes_for_list_dict[type_request]['form_name'](
            data=request.POST,
            instance=request_solvo
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request_solvo.get_absolute_url())
    else:

        form = classes_for_list_dict[type_request]['form_name'](instance=request_solvo)

    context = {'form': form, 'request_solvo': request_solvo}

    return render(request, 'solvo_support/change_request.html', context)


@permission_required('solvo_support.view_emailsolvo')
def list_emails(request, solvo_number_request=None):
    """
    список писем по заявке или все письма

    :param request:
    :param solvo_number_request:
    :return:
    """
    request_solvo = None
    if solvo_number_request is not None:
        request_solvo = get_object_or_404(RequestSolvo, solvo_number=solvo_number_request)
        emails_solvo = get_list_or_404(EmailSolvo, request_solvo=request_solvo)
    else:
        emails_solvo = EmailSolvo.objects.all()
    context = {'emails_solvo': emails_solvo,
               'solvo_number_request': solvo_number_request,
               'request_solvo': request_solvo
               }
    return render(request, 'solvo_support/list_emails.html', context)


@permission_required('solvo_support.view_emailsolvo')
def email_details(request, id_email):
    """
    детали электронного письма

    :param request:
    :param id_email:
    :return:
    """
    email_solvo = EmailSolvo.objects.get(pk=id_email)
    solvo_request = get_revision_or_error_by_solvo_number(email_solvo.request_solvo.solvo_number)
    context = {'email_solvo': email_solvo, 'link_to_request': solvo_request.get_absolute_url}
    return render(request, 'solvo_support/email_details.html', context)


@permission_required('solvo_support.add_commentrequestsolvo')
def add_comment(request, solvo_request_number):
    """
    добавить комментарий к заявке

    :param request:
    :param solvo_request_number:
    :return:
    """
    pass
    if request.method == 'POST':
        form_comment = FormCommentOnRequest(request.POST)
        if form_comment.is_valid():
            form_comment.save()
    else:
        form_comment = FormCommentOnRequest(instance=solvo_request_number)


@permission_required('solvo_support.view_bugsolvo')
def list_bugs(request, request_number):
    """
    получить список дефектов (если есть номер то по заявке)

    :param request:
    :param request_number:  номер заявки в Солво
    :return:
    """
    context = dict()
    if request_number == 'all':
        bugs = BugSolvo.objects.all()
    elif request_number.isdigit():
        request_solvo = get_object_or_404(RequestSolvo, solvo_number=request_number)
        bugs_by_request = get_list_or_404(RequestBugSolvo, request=request_solvo)
        bugs = [bug_req.bug for bug_req in bugs_by_request]
        context['request_solvo'] = request_number
    else:
        raise Http404

    context['bugs'] = bugs
    print(context)
    return render(request, 'solvo_support/list_bugs.html', context)


@permission_required('solvo_support.view_bugsolvo')
def bug_details(request, bug_number):
    """
    получить детали дефекта

    :param request:
    :param bug_number:
    :return:
    """
    bug = get_object_or_404(BugSolvo, solvo_number=bug_number)
    if request.method == 'POST':
        form = FormBug(data=request.POST, instance=bug)
        if form.is_valid():
            form.save()
    else:
        form = FormBug(instance=bug)
    list_request_by_bug = RequestBugSolvo.objects.filter(bug=bug)
    list_rev_err = [get_revision_or_error_by_solvo_number(rb.request.solvo_number) for rb in list_request_by_bug]
    context = {'bug': bug,
               'list_request_by_bug': list_rev_err,
               'form': form,
               }
    # print(list_rev_err)
    return render(request, 'solvo_support/bug_details.html', context)


def call_procedures(request, name_of_procedure=None):
    """
    выполнение процедур

    :param request:
    :param name_of_procedure:
    :return:
    """
    from django.shortcuts import reverse
    dict_procedures = {
        'mark_defects': adv_proc.mark_defects
    }

    context = {'procedures': dict_procedures}

    if name_of_procedure is None:
        return render(request, 'solvo_support/call_procedures.html', context)

    else:
        if name_of_procedure in dict_procedures.keys():
            dict_procedures[name_of_procedure]()
            return HttpResponse(f'Процедура {name_of_procedure} выполнена')
        else:
            return HttpResponse(f'ошибка')


class SolvoRequestSet(viewsets.ModelViewSet):
    queryset = RequestSolvo.objects.all().order_by('-solvo_number')
    serializer_class = RequestSolvoSerializer
    lookup_field = 'solvo_number'
