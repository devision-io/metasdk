import json
from urllib.parse import urlencode
from datetime import datetime


class EventCollectorService:

    def __init__(self, app):
        """
        :type app: metasdk.MetaApp
        """
        self.__app = app

        self.__tid = 'pylib-' + app.get_lib_version()
        self.__user_agent = app.user_agent
        self._q = self.__app.MessageQueueService
        self.a = ""

    def track(self, category, action, label, value: int = None, user_id: int = None):
        now = datetime.now()
        event_time = str(now.strftime("%Y-%m-%d %H:%M:%S"))

        # self._q.send_message('me_event2', {
        #     "t": event_time,
        #     "ua": self.__user_agent,
        # })

        data = {
            "t": event_time,
            "ua": self.__user_agent,
            "tid": self.__tid,
            "c": category,
            "a": action,
            "l": label,
        }
        if value is not None:
            data['v'] = value
        if user_id is not None:
            data['u'] = user_id

        # print(json.dumps(data))
        # exit(1)
        self._q.send_message('me_event2', b'{"t": "2020-02-29 11:31:34", "ua": "local_debug_serivce | b0", "tid": "pylib-20.0225.0", "c": "account", "a": "create", "l": "success", "v": 0}', serializer="bytes")
        # self._q.send_message('me_event2', data)
