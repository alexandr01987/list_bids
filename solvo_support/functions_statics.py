# -*- coding: utf-8 -*-
import json


def get_default_id(type_id, name_status, default_status_id=0):
    """
    Получить статус по умолчанию для объекта по типу id
    :param type_id:
    :param name_status:
    :param default_status_id:
    :return:
    """
    with open(r'solvo_support/fixtures/db_data.json', 'r') as f:
        jf = json.load(f)
        for row in jf:
            if 'status_key' in row['fields'].keys():
                if row['fields']['status_key'] == name_status and row['fields']['type_id'] == type_id:
                    default_status_id = row['pk']
                    break
    return default_status_id
