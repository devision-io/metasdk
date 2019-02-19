"""

Супер мелкие функции, которые нужны от 3 использований

"""
import json
from itertools import islice
import jwt


def chunks(iterable, count_items_in_chunk):
    """
    разбить iterable на куски по count_items_in_chunk элементов

    :param iterable:
    :param count_items_in_chunk:
    :return:
    """
    iterator = iter(iterable)
    for first in iterator:  # stops when iterator is depleted
        def chunk():  # construct generator for next chunk
            yield first  # yield element from for loop
            for more in islice(iterator, count_items_in_chunk - 1):
                yield more  # yield more elements from the iterator

        yield chunk()  # in outer generator, yield next chunk


def pretty_json(obj):
    """
    Представить объект в вище json красиво отформатированной строки
    :param obj:
    :return:
    """
    return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)


def decode_jwt(input_text, secure_key):
    """
    Раскодирование строки на основе ключа
    :param input_text: исходная строка
    :param secure_key: секретный ключ
    :return:
    """
    if input_text is None:
        return None

    encoded = (input_text.split(":")[1]).encode('utf-8')
    decoded = jwt.decode(encoded, secure_key)
    return decoded['sub']
