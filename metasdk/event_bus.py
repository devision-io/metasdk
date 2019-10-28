from typing import List, Callable

from metasdk.__state import get_current_app


class Listen(object):
    """
    Декоратор для оборачивания запускаемых методов.
    С него же снимается инфа о том, какие подписки существуют.
    """

    def __init__(self, entity_id: str, code: List[str], form_pattern: List[str] = None, receive_value: bool = False):
        """
        Регистрация метода в шине
        :param entity_id: ID сущности META
        :param code: Коды ObjectLogService META - ADD, SET, REMOVE
        :param form_pattern: Формы, на которые долэен реагировать хендлер, может быть пустым. Если пустой - значит form в event-е может быть заполненным или незаполненным,
                                а если * - то форма долэна быть заполнена, но заполнена любым значением
        :param receive_value: нужно ли добавлять value в событие
        """
        self.entity_id = entity_id
        self.code = code
        self.form_pattern = form_pattern
        self.receive_value = receive_value

    def __call__(self, original_func):
        get_current_app().event_bus.add_listener(self, original_func)

        def wrappee(*args, **kwargs):
            return original_func(*args, **kwargs)

        return wrappee


class Listener(object):
    """
    Хранилище функции и настройки
    """

    def __init__(self, listen: Listen, handler_func: Callable):
        self.listen = listen
        self.handler_func = handler_func


class Event(object):
    """
    Объект события с его контентом.
    На основе данных таска запускатора
    """

    def __init__(self, task):
        self.__task = task

        edata = task['data']['event']
        self.user_id = int(edata['userId'])
        self.entity_id = str(edata['entityId'])
        self.object_id = str(edata['objectId'])
        self.code = str(edata['code'])
        self.form = str(edata['form']) if edata['form'] else None
        self.value = edata.get('value')


class EventBus(object):
    """
    Сама Шина. Она же хранит всю карту слушателей
    """
    listener = Listen

    def __init__(self, app) -> None:
        """
        :type app: metasdk.MetaApp
        """
        self.__app = app
        self.__listeners_map = {}

    def add_listener(self, listen, handler_func):
        entity_id = listen.entity_id
        self.__listeners_map.setdefault(entity_id, [])
        listener = Listener(listen, handler_func)
        self.__listeners_map[entity_id].append(listener)

    def get_listeners(self):
        for listeners in self.__listeners_map.values():
            for listener in listeners:
                yield listener

    def accept(self, task):
        event = Event(task)
        # listener: type Listener
        for listener in self.__listeners_map.get(event.entity_id, []):
            if event.code not in listener.listen.code:
                continue

            if not self.__contains_in_form_patterns(event.form, listener.listen.form_pattern):
                continue

            listener.handler_func(event)

    def __contains_in_form_patterns(self, form, form_patterns):
        if not form_patterns:
            return True

        if not form:
            # если нет формы, то паттерны обязаны содержать хотябы ожин, целиком состоящий из *
            # это будет означать, что любые form годятся для хендлера
            return '*' in form_patterns

        for form_pattern in form_patterns:
            if form_pattern.startswith("*"):
                # есть подобие регулярки. Например qwe*
                if form.endswith(form_pattern[1:]):
                    return True
            elif form_pattern.endswith("*"):
                # есть подобие регулярки
                if form.startswith(form_pattern[:-1]):
                    return True
            else:
                # регулярки нет, можно проверять точным вхождением
                if form == form_pattern:
                    return True
        return False
