import pymongo
import tornado.escape
import tornado.ioloop
import tornado.web

from bson.json_util import dumps
from bson import ObjectId

from tornado.options import define, parse_command_line

define("debug", default=True, help="run in debug mode", type=bool)
define("port", default=8000, help="run on the given port", type=int)


class TaskHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.connection['todo']

    def get(self):
        tasks = self.db.task.find()
        self.write(dumps({"Tasks": tasks}))

    def post(self):
        title = self.get_argument("Title")
        if title:
            task = {
                "Title": title,
                "Done": False,
            }
            self.db.task.insert(task)
        self.write("Hello, world")

    def put(self, task_id):
        try:
            data = tornado.escape.json_decode(self.request.body)
        except:
            data = {}
        task_id = ObjectId(task_id)
        self.db.task.update({"_id": task_id}, {"$set": {
            "Done": data.get("Done"),
        }})


routers = [
    (r"/task/", TaskHandler),
    (r"/task/(?P<task_id>.+)/", TaskHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
]

application = tornado.web.Application(routers, debug=True)

if __name__ == "__main__":
    print "Runserver..."
    parse_command_line()
    application.connection = pymongo.MongoClient()
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()
