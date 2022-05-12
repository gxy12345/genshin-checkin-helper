"""
@Project   : genshinhelper
@Author    : y1ndan
@Blog      : https://www.yindan.me
@GitHub    : https://github.com/y1ndan
"""

from .core import Client, get_headers
from .utils import request, log, nested_lookup, extract_subset_of_dict, config, _

_LANG_DICT = {
    'zh': 'zh-cn',
    'en': 'en-us'
}


class Genshin(Client):
    def __init__(self, cookie: str = None):
        super().__init__(cookie)
        self.headers = get_headers(oversea=True)
        self.api = 'https://hk4e-api-os.mihoyo.com'
        self.act_id = 'e202102251931481'
        self.game_biz = 'hk4e_global'
        self.required_keys.update({
            'total_sign_day', 'today', 'is_sign', 'first_bind',
            'current_primogems', 'current_mora'
        })

        self.lang = _LANG_DICT.get(config.LANGUAGE, '')
        self.roles_info_url = 'https://api-os-takumi.mihoyo.com/binding/api/getUserGameRolesByCookie?game_biz={}'
        self.sign_info_url = f'{self.api}/event/sol/info?lang={self.lang}&act_id={self.act_id}'
        self.rewards_info_url = f'{self.api}/event/sol/home?lang={self.lang}&act_id={self.act_id}'
        self.sign_url = f'{self.api}/event/sol/sign?lang={self.lang}'

        self._travelers_dairy = None
        self.travelers_dairy_url = f'{self.api}/event/ysledgeros/month_info?lang={self.lang}&' + 'uid={}&region={}&month={}'
        self.daily_note_url = 'https://bbs-api-os.mihoyo.com/game_record/app/genshin/api/dailyNote'

    @property
    def sign_info(self):
        if not self._sign_info:
            log.info(_('Preparing to get check-in information ...'))
            url = self.sign_info_url
            response = request('get', url, headers=self.headers, cookies=self.cookie).json()
            log.debug(response)
            data = nested_lookup(response, 'data', fetch_first=True)
            if data:
                del data['region']
            self._sign_info.append(extract_subset_of_dict(data, self.required_keys))
        return self._sign_info

    @property
    def travelers_dairy(self):
        roles_info = self.roles_info
        self._travelers_dairy = [
            self.get_travelers_dairy(i['game_uid'], i['region'])
            for i in roles_info
        ]
        return self._travelers_dairy

    def get_travelers_dairy(self, uid: str, region: str, month: int = 0):
        log.info(_("Preparing to get traveler's dairy ..."))
        url = self.travelers_dairy_url.format(uid, region, month)
        response = request('get', url, headers=self.headers, cookies=self.cookie).json()
        log.debug(response)
        return nested_lookup(response, 'data', fetch_first=True)

    @property
    def month_dairy(self):
        raw_month_data = nested_lookup(self.travelers_dairy, 'month_data')
        return [
            extract_subset_of_dict(i, self.required_keys)
            for i in raw_month_data
        ]

    def get_daily_note(self, uid: str, region: str):
        log.info(_('Preparing to get Genshin daily note ...'))
        url = self.daily_note_url
        payload = {
            'role_id': uid,
            'server': region
        }
        from genshinhelper.utils import cookie_to_dict
        # cookie_str = "cookie_token=7wePs9s50rizPytKb4QzvlzJoO8DU6AUx17zsxq2; account_id=156448589"
        # self.cookie = cookie_to_dict(cookie_str)
        # response = request('get', url, headers=get_headers(oversea=True, with_ds=True, ds_type='3', params=payload), params=payload, cookies=self.cookie)
        response = request('get', url, headers=get_headers(oversea=True, with_ds=True, ds_type='3', params=payload), params=payload, cookies=self.cookie)
        log.debug(response.status_code)
        log.debug(response.content)
        if response.status_code == 403:
            return None
        response_json = response.json()
        if response_json['data'] is None:
            return None
        data = nested_lookup(response_json, 'data', fetch_first=True)
        return data if data else response_json



# if __name__ == '__main__':
#     log.info(_('Preparing to get Genshin daily note ...'))
#     url = 'https://bbs-api-os.mihoyo.com/game_record/app/genshin/api/dailyNote'
#     payload = {
#         'role_id': 834047734,
#         'server': 'os_asia'
#     }
#     from genshinhelper.utils import cookie_to_dict
#
#     cookie_str = "cookie_token=7wePs9s50rizPytKb4QzvlzJoO8DU6AUx17zsxq2; account_id=156448589"
#     cookie = cookie_to_dict(cookie_str)
#     response = request('get', url, headers=get_headers(with_ds=True, new_ds=True, params=payload), params=payload,
#                        cookies=cookie).json()
#     data = nested_lookup(response, 'data', fetch_first=True)
#     if data:
#         print(data)
#     else:
#         print(response)
