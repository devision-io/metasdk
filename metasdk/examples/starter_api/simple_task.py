from metasdk import MetaApp

META = MetaApp(starter_api_url="http://s2.meta.vmc.loc:28341")

task_data = META.StarterService.submit("adptools.clear_logs", {})
print(u"task_data = %s" % str(task_data))


def optional_await_task_callback(task_info, is_finish):
    print(u"task_info = %s" % str(task_info))
    print(u"is_finish = %s" % str(is_finish))


result_task_info = META.StarterService.await_task(task_data.get('taskId'), task_data.get('serviceId'), optional_await_task_callback)

print(u"result_task_info = %s" % str(result_task_info))
