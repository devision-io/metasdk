from metasdk import MetaApp
from metasdk.event_bus import Event

META = MetaApp()
log = META.log


@META.event_bus.listener(entity_id="2830", code=["ADD", "SET"], form_pattern=["*"], dispatcher_pattern=["meta.garpun_feeds"])
def on_upsert_ex_access(event: Event):
    print(u"on_upsert_ex_access = %s" % str(event))
    print(u"event.value = %s" % str(event.value))
    print(u"event.object_id = %s" % str(event.object_id))


META.worker.debug_tasks = [{
    "data": {
        "event": {
            "dispatcher": "meta.garpun_feeds",
            "userId": 10191,
            "entityId": 2830,
            "objectId": "7fb540bf-3cb3-4fa8-b11e-9a5a593d500b",
            "code": "SET",
            # "form": None,
            "form": "test",
            "value": {
                "a": 1
            }
        }
    }
}]


@META.worker.single_task
def main(task):
    META.event_bus.accept(task)


