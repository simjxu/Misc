import datetime

account_motes = {
    'sj_office': [
        '30000c2a690be1bc'
    ],
    'svp': [
        '30000c2a690be059',
        '30000c2a690be04a',
        '30000c2a690be1c9',
        '30000c2a690be1c2',
        '30000c2a690be1b7',
        '30000c2a690be1c6',
        '30000c2a690be1c1',
        '30000c2a690be008',
        '30000c2a690be04b',
        '30000c2a690be063',
        '30000c2a690be011',
        '30000c2a690be1ed',
        '30000c2a690be1ba',
        '30000c2a690be1e4',
        '30000c2a690be1d0',
        '30000c2a690be1e2'
    ],
    'stanford': [
        '30000c2a690be05b',
        '30000c2a690be04e',
        '30000c2a690be1bf',
        '30000c2a690be1b5',
        '30000c2a690be01b',
        '30000c2a690be00f',
        '30000c2a690be050',
        '30000c2a690be1b4',
        '30000c2a690be01d',
        '30000c2a690be053'
    ]
}

start_dates = {
    'svp': datetime.datetime.strptime('2016-7-30', '%Y-%m-%d'),
    'stanford': datetime.datetime.strptime('2016-7-1', '%Y-%m-%d')
}

result_base_url = 'results/'
chart_base_url = 'results/charts/'
battery_logs_base_url = 'data/'
battery_logs_download_base_url = 'https://petasense.blob.core.windows.net/battery-test-logs/'


class Context(object):
    def __init__(self, account):
        self.account = account
        self.start_date = start_dates[account]
        self.device_id_list = account_motes[account]

    def set_account(self, account):
        self.account = account

global context
context = Context('svp')