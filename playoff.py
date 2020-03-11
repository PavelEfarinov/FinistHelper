def form_new_groups(winners):
    print(winners)


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
    form_new_groups(bid_list)
