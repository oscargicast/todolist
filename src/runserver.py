import tornado.ioloop
import tornado.web
import pymongo

from bson.json_util import dumps


class TaskHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.connection['todo']

    def get(self):
        tasks = self.db.task.find()
        self.write(dumps({"Tasks": tasks}))


routers = [
    (r"/task/", TaskHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
]

application = tornado.web.Application(routers, debug=True)

if __name__ == "__main__":
    print "Runserver..."
    application.connection = pymongo.MongoClient()
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()
