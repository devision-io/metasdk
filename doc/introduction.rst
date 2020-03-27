=====================
Введение
=====================


Install
=======

```
pip3 install metasdk --upgrade --no-cache
```

Python 3

Получите файл токен разработчика
Установите developer_settings.json в домашнюю директорию в папку .rwmeta
Например:
 - MacOS: `/Users/arturgspb/.rwmeta/developer_settings.json`
 - Windows: `C:\\Users\\userXXXXXX\\.rwmeta\\developer_settings.json`
 - Linux: `~/.rwmeta/developer_settings.json`

Full Examples
=============

`Полный список примеров
<https://github.com/devision-io/metasdk/tree/master/metasdk/examples/>`_

Usage
=====
.. code-block:: python

    import logging
    import starter_api
    from metasdk import MetaApp

    # Инициализация приложения
    # конфигурирует логгер и пр.
    META = MetaApp()

    # работает стандартный логгер
    logging.info('Hello, from Meta App Script!')
    # Можно получить экземпляр логгера с улучшеным интерфейсом для более удобного прикладывания контекста
    log = META.log
    log.warning('Do warning log', {"count": 1, "mycontextParam": [1, 3, 4]})

    # Поставновка задач в Запускатор
    starter_api.build_submit('YOUR_SERVICE')
    # или
    META.starter.build_submit('YOUR_SERVICE')
