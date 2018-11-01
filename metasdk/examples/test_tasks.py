import time

from metasdk import MetaApp

META = MetaApp()
log = META.log

# Установка таской для отладки кода
META.worker.debug_tasks = [{
    "data": {
        "username": "Artur"
    }
}]


@META.worker.single_task
def main(task):
    log.info('Hello task')
    time.sleep(10)

    data = task['data']
    username_ = data.get('username', '%USERNAME%')
    log.info('Hello task', {'welcome': 'Hello, ' + username_, 't': task})
    time.sleep(10)
