import base64
import os
from aiohttp import web
from aiohttp.web_request import Request

from metasdk import MetaApp

KAFKA_TOPIC = "collect"

META = MetaApp(include_worker=False)
log = META.log

is_prod = os.environ.get("PRODUCTION", False)

"""
curl -X POST -d 'pb=1&asdasd' 'http://0.0.0.0:9977/collect/1123?gp=1'
ab -n 10000 -c 100 -k "http://0.0.0.0:9977/collect/zxc?qwe=123"
"""
producer = META.MessageQueueService.get_producer(serializer="bytes")

PIXEL_GIF_DATA = base64.b64decode(
    b"R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")


async def write_to_kafka(request: Request):
    collector_name = request.match_info.get('collector_name')

    q_data_ = collector_name + '|' + str(request.query_string)
    if request.body_exists:
        post_data = str(await request.text())
        if post_data:
            if q_data_:
                q_data_ += "&"
            q_data_ += post_data
    producer.send(KAFKA_TOPIC, q_data_.encode())


async def collect(request: Request):
    request.loop.create_task(write_to_kafka(request))

    return web.Response(body=PIXEL_GIF_DATA, content_type='image/gif')


app = web.Application()

app.router.add_get("/collect/{collector_name}", collect)
app.router.add_post("/collect/{collector_name}", collect)

host = "0.0.0.0"
if is_prod:
    port = 80
else:
    port = 9977

if __name__ == "__main__":
    web.run_app(app, host=host, port=port, access_log=None)
