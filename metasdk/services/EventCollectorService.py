class EventCollectorService:

    def __init__(self, app):
        """
        :type app: metasdk.MetaApp
        """
        self.__app = app

        self.__tid = 'pylib-' + app.get_lib_version()
        self.__user_agent = app.user_agent
        self.__q = self.__app.MessageQueueService.get_producer()
        self.a = ""

    def track(self, category, action, label, value: int = None, user_id: int = None):
        data = {
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

        self.__q.send('me_event2', data)
