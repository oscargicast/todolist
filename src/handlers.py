import tornado.escape
import tornado.web

from bson.json_util import dumps
from bson import ObjectId


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")


class TaskHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.db = self.application.db['todo']
        self.task = self.db.task

    @tornado.web.addslash
    def get(self):
        tasks = self.task.find()
        self.write(dumps({"Tasks": tasks}))

    def post(self):
        title = self.get_argument("Title")
        if title:
            task = {
                "Title": title,
                "Done": False,
            }
            self.task.insert(task)

    def put(self, task_id):
        try:
            data = tornado.escape.json_decode(self.request.body)
        except:
            data = {}
        task_id = ObjectId(task_id)
        self.task.update({"_id": task_id}, {"$set": {
            "Done": data.get("Done"),
        }})

    def delete(self, task_id):
        try:
            data = tornado.escape.json_decode(self.request.body)
        except:
            data = {}
        task_id = ObjectId(task_id)
        self.task.remove({"_id": task_id})
