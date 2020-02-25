from FinistHelper import playoff
from FinistHelper.UserInputHandler import UserInputHandler


def create_playoff(session, stage_list, number_of_winners):
    bid_list = []
    for stage in stage_list:
        winners_list = session.get(
            'https://ru-dev-robo.starline.ru/api/v1/data/events/programs/stages/' + stage + '/challonge/').json()[
                           'table_score'][0:number_of_winners]
        for winner in winners_list:
            person = {}
            person['id'] = winner['id']
            person['group'] = stage
            person['rank'] = winner['p']
            bid_list.append(person)
    print(bid_list)
    playoff.form_new_groups(bid_list)


inputHandler = UserInputHandler()
inputHandler.work_properly()

# EVENT_ID = '240'
# create_playoff(session, ['3183', '3184'], 2)  # TODO количество участников должно быть степенью двойки
