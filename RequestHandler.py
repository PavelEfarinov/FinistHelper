import copy
import json
import re

import requests


class RequestHandler(object):
    def __init__(self, event_id, session, new_cookies_required):
        self.session = session
        if new_cookies_required:
            self.get_cookie_from_server()
        self.set_local_cookie()
        self.EVENT_ID = event_id

    def get_server_attempts(self, stage, file):
        response = self.session.get(
            'https://ru-dev-robo.starline.ru/api/v1/data/referee/events/programs/stages/' + str(stage) + '/bids')
        attempts_info = response.json()
        print(attempts_info)
        with open(file, 'w') as f:
            json.dump(self.server_to_local_json(attempts_info), f)

    def server_to_local_json(self, attempts_info):
        attempts_list = []
        for i in range(len(attempts_info)):
            for j in range(len(attempts_info[i]['singleResults'])):
                result_list = attempts_info[i]['singleResults'][j]['results'][1:-1].split(',')
                client_json = client_json_template.copy()
                for k in range(len(result_list)):
                    client_json['params'][k] = float(result_list[k])
                client_json['number'] = attempts_info[i]['singleResults'][j]['number']
                client_json['disq_action'] = str(attempts_info[i]['singleResults'][j]['disqualification'])
                client_json['bid'] = attempts_info[i]['bid']['id']
                attempts_list.append(copy.deepcopy(client_json))
                print(client_json)
        return attempts_list

    def post_local_json(self, stage, file):
        with open(file) as f:
            local_json = json.load(f)
        attempts_list = []
        for i in range(len(local_json)):
            server_json = server_json_template.copy()
            server_json["number"] = local_json[i]["number"]
            if local_json[i]['disq_action'] == '1':
                server_json["disq_action"] = local_json[i]["disq_action"]
            else:
                server_json["params"] = local_json[i]["params"]
            resp = self.session.post(
                'https://ru-dev-robo.starline.ru/api/v1/data/referee/events/programs/stages/' + str(stage) + '/bids/' +
                str(local_json[i]["bid"]) + '/results', data=str(server_json).replace('\'', '\"'))
            print(str(server_json).replace('\'', '\"'), resp)
        return attempts_list

    def create_groups(self, number_of_groups, program_id):

        bid_list = self.session.get('https://ru-dev-robo.starline.ru/api/v1/data/admin/events/' + str(self.EVENT_ID) + '/bids').json()
        filtered_bid_list = []
        for bid in bid_list:
            if bid['status'] == 6:
                for stage in bid['program_stages']:
                    if stage['program']['id'] == program_id:
                        filtered_bid_list.append(copy.deepcopy(bid['id']))
                        break
        print(filtered_bid_list)
        stage_list = []
        for i in range(int(number_of_groups)):
            group_name = 'Group ' + chr(i + 65)
            current_json = {
                "RCME_ProgramStage[name]": group_name,
                "RCME_ProgramStage[type_start]": "0",
                "RCME_ProgramStage[type_transfer]": "0",
                "RCME_ProgramStage[status]": "0",
                "RCME_ProgramStage[hidden_results]": "0",
                "RCME_ProgramStage[challonge_type]": "RoundRobin",
                "RCME_ProgramStage[started_at]": "",
                "RCME_ProgramStage[match_time]": "60",
                "yt0": ""
            }
            stage_list.append(re.search('=\d+', str(
                self.session.post(
                    'https://ru-dev-robo.starline.ru/eventadmin/' + self.EVENT_ID + '/ProgramStage/create?id=' + str(
                        program_id),
                    data=current_json).url))[0][1:])
        print(stage_list)
        for i in range(int(number_of_groups)):
            bid_json = {
                "yt0": ""
            }
            new_stage_bids = filtered_bid_list[i::int(number_of_groups)]
            for bid in new_stage_bids:
                print(bid)
                bid_json['RCME_ProgramStage[' + str(bid) + ']'] = 1
            self.session.post(
                'https://ru-dev-robo.starline.ru/eventadmin/' + self.EVENT_ID + '/ProgramStage/bids?id=' +
                stage_list[i],
                data=bid_json)

    def get_cookie_from_server(self):
        self.session.get('https://ru-dev-robo.starline.ru/auth/login')
        self.session.post('https://ru-dev-robo.starline.ru/auth/login', data=login_data)
        with open('../cookies.json', 'w') as f:
            json.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)

    def set_local_cookie(self):
        with open('cookies.json') as f:
            self.session.cookies.update(json.load(f))


login_data = {
    "RCMS_LoginForm[username]": "pavelefarinov@gmail.com",
    "RCMS_LoginForm[password]": "qr2177pkb",
    "yt0": "Войти"
}
server_json_template = {
    # "params": {},
    # "disq_action": 0,
    "number": 0
}

client_json_template = {
    "params": {},
    "number": 0,
    "disq_action": "0",
    "bid": 0
}
