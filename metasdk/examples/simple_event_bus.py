from metasdk import MetaApp
from metasdk.event_bus import Event

META = MetaApp()
log = META.log


@META.event_bus.listener(entity_id="2830", code=["ADD", "SET"], form_patterns=["*"])
def on_upsert_ex_access(event: Event):
    print(u"on_upsert_ex_access = %s" % str(event))
    print(u"event.value = %s" % str(event.value))
    print(u"event.object_id = %s" % str(event.object_id))


META.worker.debug_tasks = [{
    "data": {
        "event": {
            "user_id": 10191,
            "entity_id": 2830,
            "object_id": "42",
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


