import json
import random
import time

import requests
from checkin import Checkin
from result import Result


class Dounai(Checkin):
    def __init__(self, email, psw='1'):
        super().__init__("Dounai")
        self.email = email
        self.psw = psw

    def checkin(self) -> Result:
        dounai_headers = {
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'}

        login_data = {'email': self.email, 'passwd': self.psw}
        dounai_session = requests.Session()
        login_result = dounai_session.post('https://dounai.pro/auth/login',
                                                        headers=dounai_headers,
                                                        data=login_data)
        login_result = json.loads(login_result.text.encode())
        if 'error_code' in login_result:
            return Result.fail(login_result['msg'])
        time.sleep(random.randint(1, 3))
        dounai_headers.update({'Origin': 'https://dounai.pro', 
                               'Accept': 'application/json, text/javascript, */*; q=0.01',
                               'accept-encoding': 'gzip, deflate, br, zstd',
                               'accept-language': 'zh-CN,zh;q=0.9',
                               'pragma': 'no-cache',
                               "priority": 'u=1, i',
                               'Referer': 'https://dounai.pro/user/panel',
                               'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
                               'sec-ch-ua-mobile': '?0',
                               'sec-ch-ua-platform': '"Windows"',
                               'sec-fetch-dest': 'empty',
                               'sec-fetch-mode': 'cors',
                               'sec-fetch-site': 'same-origin',
                               'X-Requested-With': 'XMLHttpRequest',
                                  })
        dounai_checkin_page = dounai_session.post('https://dounai.pro/user/checkin',
                                                        headers=dounai_headers)
        dounai_checkin_json = json.loads(dounai_checkin_page.text.encode())
        checkin_result = dounai_checkin_json['msg']
        return Result.success(checkin_result)
