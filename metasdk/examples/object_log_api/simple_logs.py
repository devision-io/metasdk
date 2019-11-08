from metasdk import MetaApp

META = MetaApp(meta_url="http://localhost:8080")

META.ObjectLogService.log({
    "userId": 10191,
    "entityId": 2671,
    "objectId": 53,
    "code": "SET",
    "form": "my_form", # optional
    "value": {  # optional
        "foo": "bar",
        "subFoo": {
            "foo2": [1, 2, 3]
        }
    }
})

# А тут кроме лога запустится обработчик Шины событий, так как он есть именно на эту связку entity + code
# META.ObjectLogService.log({
#     "userId": 10191,
#     "entityId": 2830,
#     "objectId": "7fb540bf-3cb3-4fa8-b11e-9a5a593d500b",
#     "code": "SET",
#     # "form": None,
#     "form": "test",
#     "value": {
#         "a": 1
#     }
# })
