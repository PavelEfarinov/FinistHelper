import requests

from FinistHelper.RequestHandler import RequestHandler


class UserInputHandler(object):
    def __init__(self):
        self.requestHandler = RequestHandler
        self.EVENT_ID = 0

    def work_properly(self):
        print('Введите EVENT_ID для мероприятие, с которым хотите работать')
        self.EVENT_ID = input()
        with requests.Session() as session:
            self.requestHandler = RequestHandler(self.EVENT_ID, session, False)
            print('Выберите необходимое действие\n'
                  'ПУНКТЫ 1,2 НЕ РАБОТАЮТ ДЛЯ ПАРНЫХ ВИДОВ\n',
                  '1. Выгрузить все прошедшие попытки в файл\n',
                  '2. Загрузить все попытки из файла\n',
                  '3. Создать группы с парной круговой системой\n',
                  '4. Закрыть программу')
            user_answer = int(input())
            if user_answer == 1:
                print('Введите stage ID (ex. 1234):')
                stage_id = int(input())
                print('Введите имя файла (ex. SUMO_attempts.json):')
                filename = input()
                self.requestHandler.get_server_attempts(stage_id, filename)
            elif user_answer == 2:
                print('Введите stage ID (ex. 1234):')
                stage_id = int(input())
                print('Введите имя файла (ex. SUMO_attempts.json):')
                filename = input()
                self.requestHandler.post_local_json(stage_id, filename)
            elif user_answer == 3:
                print('Введите program ID (ex. 1234):')
                program_id = int(input())
                print('Введите количество групп:')
                group_number = input()
                self.requestHandler.create_groups(group_number, program_id)
