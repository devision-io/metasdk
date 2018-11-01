from metasdk import MetaApp

META = MetaApp()

UserManagementService = META.UserManagementService
resp = UserManagementService.send_recovery_notice("arturgspb", "meta")
print(u"resp = %s" % str(resp))
# resp = {'error': None, 'error_details': None, 'success_details': 'Вам отправлено уведомление о сбросе пароля на email art@realweb.ru. Следуйте инструкциям из письма.'}

resp = UserManagementService.send_recovery_notice("arturgspb2", "meta")
print(u"resp = %s" % str(resp))
# resp = {'error': 'user_not_found', 'error_details': 'Пользователь с таким логином не найден', 'success_details': None}
