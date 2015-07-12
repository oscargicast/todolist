from tornado.web import url
from handlers import MainHandler, TaskHandler


urlpatterns = [
    url(r"/", MainHandler, name="main"),
    url(r"/task/?", TaskHandler),
    url(r"/task/(?P<task_id>.+)/", TaskHandler),
]
