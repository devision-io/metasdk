import json
import os
from aiohttp import web
from aiohttp.web_request import Request

from metasdk import MetaApp

META = MetaApp(include_worker=False)
log = META.log

is_prod = os.environ.get("PRODUCTION", False)

"""
curl -X POST -d 'pb=1&asdasd' 'http://0.0.0.0:9977/collect?gp=1'
"""
q = META.MessageQueueService


async def collect(request: Request):
    q_data_ = str(request.query_string)
    if request.body_exists:
        post_data = str(await request.text())
        if post_data:
            if q_data_:
                q_data_ += "&"
            q_data_ += post_data

    q.send_message("collect", q_data_.encode(), serializer="bytes")

    return web.Response()


app = web.Application()

app.router.add_get("/collect", collect)
app.router.add_post("/collect", collect)

host = "0.0.0.0"
if is_prod:
    port = 80
else:
    port = 9977

if __name__ == "__main__":
    web.run_app(app, host=host, port=port, access_log=False)
