from user_statistics.google_api.ga_server_application import analytics_api_v3
from datetime import datetime

class GoogleAnalytics(object):
 
    @staticmethod
    def frequency():       
        frequency_items = []       
        users = analytics_api_v3.new_users()
        for user in users:
            date = datetime.strptime(user[0], '%Y%m%d')
            item = {'date': date.strftime('%Y-%m-%d'), 'count': user[1]}
            frequency_items.append(item)
        return frequency_items

        