from metasdk.apiclient import ApiClient

api = ApiClient.build_from_developer_settings("hello", "v1")

# Установите другой URL api если надо
# api.host = "http://localhost:8084"

resp = api.request("hello/ping", post_data={
    "ping": "Hi!!!"
})

print(u"resp = %s" % str(resp))
