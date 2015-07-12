import pymongo
import tornado.escape
import tornado.ioloop
import tornado.web

from bson.json_util import dumps
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
        try:
            data = tornado.escape.json_decode(self.request.body)
        except:
            data = {}
        title = data.get("Title")
        if title:
            task = {
                "Title": title,
                "Done": False,
            }
            self.db.task.insert(task)
        self.write("Hello, world")


routers = [
    (r"/task/", TaskHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
]

application = tornado.web.Application(routers, debug=True)

if __name__ == "__main__":
    print "Runserver..."
    parse_command_line()
    application.connection = pymongo.MongoClient()
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()
