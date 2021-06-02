# -*- coding: utf-8 -*-
import openpyxl
import re


class ExcelFile:
    """
    Эксель файл
    """
    def __init__(self, path_file):
        self.path_file = path_file
        self.list_of_emails = []
        self.list_of_requests = []
        self.dict_of_bugs = dict()
        self.unique_dict_of_requests = dict()
        self.file_excel = openpyxl.load_workbook(self.path_file)
        self.handle_excel_file()

    def get_emails_from_excel(self):
        """
        получить письма из эксель файла

        :return:
        """
        for list_exl_name in self.file_excel.sheetnames:
            for row in self.file_excel[list_exl_name].rows:
                self.list_of_emails.append(
                    ExcelEmail(
                        subject=row[0].value,
                        date_received=row[1].value,
                        sender=row[2].value,
                        body=row[3].value,
                    )
                )

    def made_requests_from_emails(self):
        """
        получить заявки из писем
        :return:
        """
        for email in self.list_of_emails:
            request = ExcelRequest(email)
            if request.number_request is not None:
                self.list_of_requests.append(request)

    def made_unique_requests_dict(self):
        """
        получить словарь уникальных заявок
        :return:
        """
        for req in self.list_of_requests:
            print(req.number_request)
        sorted_requests = sorted(self.list_of_requests, key=lambda obj: obj.date_received)
        for request in sorted_requests:
            if request.type_request == 'revision' and request.number_request not in self.unique_dict_of_requests.keys():
                self.unique_dict_of_requests[request.number_request] = request
        for request in sorted_requests:
            if request.number_request not in self.unique_dict_of_requests.keys():
                self.unique_dict_of_requests[request.number_request] = request

    def scan_for_bugs(self):
        """
        поиск дефектов по заявке
        :return:
        """
        bug_number_pattern = r'#(\d+)'  # шаблон получения номера бага
        bug_name_pattern = rf'BUG:(.*){bug_number_pattern}'  # шаблон полуения всего имени бага
        re_bug_name = re.compile(bug_name_pattern)  # регулярное выражение для поиска дефекта

        def define_critical(body_message):
            """
            определить критичность дефекта

            :return: критичность заявки
            """
            critical_dict = {'l': r'[Нн]изкой',
                             'm': r'[Сс]редней',
                             'h': r'[Вв]ысокой',}  # словарь критичности багов
            for key, pattern in critical_dict.items():
                if re.search(pattern, body_message):
                    critical_status = key
                    break
            else:
                critical_status = 'l'
            return critical_status

        for request in sorted(self.list_of_requests, key=lambda obj: obj.date_received, reverse=True):
            try:
                test_bugs_list = re_bug_name.findall(request.body)
                if test_bugs_list:
                    critical_scan_status = define_critical(request.body)
                    for name_bug, num_bug in test_bugs_list:
                        new_bug = ExcelBug(
                            request_number=request.number_request,
                            solvo_number=num_bug,
                            name=name_bug,
                            date_registered=request.date_received,
                            critical_state=critical_scan_status
                        )
                        self.dict_of_bugs[num_bug] = new_bug
            except Exception:
                pass

    def handle_excel_file(self):
        """
        обработать эксель для создания списка писем

        :return:
        """
        self.get_emails_from_excel()
        self.made_requests_from_emails()
        self.made_unique_requests_dict()
        self.scan_for_bugs()


class ExcelEmail:
    """
    Электронное письмо из эксель
    """

    def __init__(self, sender, subject, date_received, body):
        self.sender = sender
        self.subject = subject
        self.date_received = date_received
        self.body = body or 'ошибка в обработке письма'
        self.handle_email()

    def handle_subject(self):
        """
        обработать заголовок письма
        :return:
        """
        remove_pattern = r'.*\[Support-era2\]\s*'
        self.subject = re.sub(remove_pattern, '', self.subject)

    def handle_body(self):
        """
        обработать тело письма для лучшей читаемости
        :return:
        """
        new_body = self.body  # тело письма для обработки
        list_replace_signs = [
            (r'(_x000D_)+[\n\s]*', '\n'),  # заменить переходы строк
            ('\n{3,}', '\n'),  # уменьшить кол-во пустых строк
            ('((> )|>)+', ''),  # убрать стрелки
        ]
        try:
            # цикл чтобы убрать лишнии знаки
            for sign_tuple in list_replace_signs:
                new_body = re.sub(sign_tuple[0], sign_tuple[1], new_body)
                print(new_body)
            new_body = new_body[:3000]
            self.body = new_body
            # перекодировка сообщения
            # new_body = new_body.encode('utf-8', errors='ignore')
            # self.body = new_body.decode('utf-8', errors='ignore')
        except Exception as e:
            print(e)
            pass

    def handle_email(self):
        """
        обработать письмо

        :return:
        """
        self.handle_body()
        self.handle_subject()


class ExcelRequest(ExcelEmail):
    """
    Заявка Солво
    """
    def __init__(self, email):
        super().__init__(**email.__dict__)
        self.number_request = None
        self.type_request = None
        self.number_revision = None
        self.define_request()

    def check_as_revision(self):
        """
        получить номер доработки
        :return:
        """
        num_revision_re = re.compile(r'\((ERA-2[-\w]+)\)')  # шаблона номера доработки
        try:
            if re.search(r'\(ERA-2[-\w]+\)', self.subject) and re.search('доработк[ау]', self.subject):
                self.number_revision = num_revision_re.search(self.subject).groups()[0]
                self.type_request = 'revision'
                return True
            else:
                return False
        except AttributeError:
            self.number_revision = None
            return False

    def define_request(self):
        """
        получить номер заявки и присвоить
        :return:
        """
        num_pattern_request = re.compile(r'\[#(\d+)\]')  # шаблон номера заявки
        try:
            self.number_request = num_pattern_request.search(self.subject).groups()[0]
            is_revision = self.check_as_revision()
            if not is_revision:
                self.type_request = 'error'
        except AttributeError:
            self.number_request = None
            self.type_request = 'message'

    def __str__(self):
        """
        вернуть имя заявки в зависимости от типа

        :return:
        """
        if self.type_request == 'revision':
            return_name = f'[{self.number_request}]++({self.number_revision}) -- {self.subject}'
        elif self.type_request == 'error':
            return_name = f'[{self.number_request}] -- {self.subject}'
        else:
            return_name = f'{self.subject}'
        return return_name


class ExcelBug:
    """
    Дефект из заявки экселя
    """
    def __init__(self, request_number, solvo_number, name, date_registered, critical_state):
        self.request_number = request_number
        self.solvo_number = solvo_number
        self.name = name
        self.date_registered = date_registered
        self.critical_state = critical_state
