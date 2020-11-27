# Введение


## Install

Для metasdk и для локальной меты

### Установите токен разработчика

Получите файл токен разработчика
Установите developer_settings.json в домашнюю директорию в папку .rwmeta
Например:
 - MacOS: `/Users/arturgspb/.rwmeta/developer_settings.json`
 - Windows: `C:\Users\userXXXXXX\.rwmeta\developer_settings.json`
 - Linux: `~/.rwmeta/developer_settings.json`
 
### Установите metasdk 

Для разработки скриптов на python. Для локальной меты это не надо.

Поддерживается Python 3.6+

```shell script
pip3 install metasdk --upgrade --no-cache
```

## Full Examples

[Полный список примеров](https://github.com/devision-io/metasdk/tree/master/metasdk/examples/)

## Usage

```python
import logging
from metasdk import MetaApp

# Инициализация приложения
# конфигурирует логгер и пр.
META = MetaApp()

# Проверьте работоспособность установки
r = META.db("meta").one("SELECT NOW() as now")
print(r)

# работает стандартный логгер
logging.info('Hello, from Meta App Script!')
# Можно получить экземпляр логгера с улучшеным интерфейсом для более удобного прикладывания контекста
log = META.log
log.warning('Do warning log', {"count": 1, "mycontextParam": [1, 3, 4]})
```
