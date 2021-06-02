# -*- coding: utf-8 -*-


import json
import os

list_of_json_dicts = []
json_name_file = 'db_data'
counter = 0


def count_increment():
    global counter
    counter += 1
    return counter


def generate_json_from_dict(dictionary_info, name_model, list_to_json):
    """
    Генератор json данных из словарей

    :param dictionary_info: словарь с информацией для json
    :param name_model: имя модели
    :param list_to_json: список с информацией в json
    :return:
    """
    for pk in dictionary_info.keys():
        dict_to_json = dict()
        dict_to_json["model"] = name_model
        dict_to_json["pk"] = pk
        dict_to_json["fields"] = dictionary_info[pk]
        list_to_json.append(dict_to_json)


def save_to_fixtures_json(list_json_dicts, name_file):
    """
    Сохранить фикстуры как json

    :param list_json_dicts: файл для фикстур
    :param name_file:  имя для сохранения файла
    :return:
    """
    cur_dir = os.path.dirname(os.path.abspath(__file__))

    with open(f'{os.path.join(cur_dir, name_file)}.json', 'wt', encoding='utf-8') as json_file:
        json.dump(list_json_dicts, json_file, ensure_ascii=False, indent=4)


def generate_critical(list_for_json):
    """
    герератор фикстур для кричиности дефектов

    :param list_for_json:
    :return:
    """
    model_name = 'solvo_support.bugcriticalsolvo'
    dict_critical = {
        1: {
            'key_name': 'l',
            'ru_name': "низкий",
            'days_for_fix': 60
        },
        2: {
            'key_name': 'm',
            'ru_name': "средний",
            'days_for_fix': 30
        },
        3: {
            'key_name': 'h',
            'ru_name': "высокий",
            'days_for_fix': 2
        }
    }

    generate_json_from_dict(dict_critical, model_name, list_for_json)


def generate_statuses(list_for_json):
    """
    генератор фикстур для статусов

    :param list_for_json:
    :return:
    """
    global counter
    counter = 0
    model_name = 'solvo_support.status'
    dict_statuses = {
        count_increment(): {
            'type_id': 1,
            'status_key': 'new',
            'ru_status_name': 'новая',
        },
        count_increment(): {
            'type_id': 1,
            'status_key': 'in_solvo',
            'ru_status_name': 'ожидаем ответ от Солво',
        },
        count_increment(): {
            'type_id': 1,
            'status_key': 'in_era',
            'ru_status_name': 'мы должны дать ответ',
        },
        count_increment(): {
            'type_id': 1,
            'status_key': 'solvo_wait_example',
            'ru_status_name': 'нужен пример для Солво',
        },
        count_increment(): {
            'type_id': 1,
            'status_key': 'resolved',
            'ru_status_name': 'решена',
        },
        count_increment(): {
            'type_id': 1,
            'status_key': 'closed',
            'ru_status_name': 'закрыта без решения',
        },
        count_increment(): {
            'type_id': 2,
            'status_key': 'estimating',
            'ru_status_name': 'оценивается',
        },
        count_increment(): {
            'type_id': 2,
            'status_key': 'matching',
            'ru_status_name': 'согласование',
        },
        count_increment(): {
            'type_id': 2,
            'status_key': 'developing_by_solvo',
            'ru_status_name': 'выполняется в Солво',
        },
        count_increment(): {
            'type_id': 2,
            'status_key': 'on_our_test',
            'ru_status_name': 'на нашем тесте',
        },
        count_increment(): {
            'type_id': 2,
            'status_key': 'done',
            'ru_status_name': 'выполнена',
        },
        count_increment(): {
            'type_id': 2,
            'status_key': 'not_actual',
            'ru_status_name': 'не актуальна',
        },
        count_increment(): {
            'type_id': 3,
            'status_key': 'registered',
            'ru_status_name': 'зарегистрирован',
        },
        count_increment(): {
            'type_id': 3,
            'status_key': 'fix_on_test',
            'ru_status_name': 'на нашем тесте',
        },
        count_increment(): {
            'type_id': 3,
            'status_key': 'fixed',
            'ru_status_name': 'исправлено',
        },
        count_increment(): {
            'type_id': 3,
            'status_key': 'canceled',
            'ru_status_name': 'отменён',
        },
    }

    generate_json_from_dict(dict_statuses, model_name, list_for_json)


generate_critical(list_of_json_dicts)
generate_statuses(list_of_json_dicts)
save_to_fixtures_json(list_of_json_dicts, json_name_file)
