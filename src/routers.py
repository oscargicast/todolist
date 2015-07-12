from handlers import MainHandler, TaskHandler

urlpatterns = [
    (r"/", MainHandler),
    (r"/task/", TaskHandler),
    (r"/task/(?P<task_id>.+)/", TaskHandler),
]
