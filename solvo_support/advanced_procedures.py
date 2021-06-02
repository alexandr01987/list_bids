# -*- coding: utf-8 -*-
from .models import RequestBugSolvo


def mark_defects():
    """
    сделать отметку о найденных багах в заявках
    :return:
    """
    try:
        requests_bugs = RequestBugSolvo.objects.all()
        for rb in requests_bugs:
            req = rb.request
            if not req.is_defect_registered:
                req.is_defect_registered = True
                req.save()
    except Exception as e:
        print(e)
        pass

