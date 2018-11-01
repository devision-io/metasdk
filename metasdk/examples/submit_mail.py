from metasdk import MetaApp

META = MetaApp()

# Рекомендуется выдумывать unique_id для КАЖДОГО письма, чтобы избежать спама при ошибках или повторных запусках ваших скриптов
gen_id = "HJljkasdlkjasd"
META.MailService.submit_mail("meta@realweb.ru", "art@realweb.ru", "TTT", "ttt pong", unique_id="my_mail_category__" + gen_id)

# Без уникализации письма. Не рекомендуется, так как если ваш ког будет багать и бесконечно добавлять письма - то, вы можете заспамить адресатов
META.MailService.submit_mail("meta@realweb.ru", "art@realweb.ru", "TTT", "ttt pong")