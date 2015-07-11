import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("Hello")


application = tornado.web.Application([
    (r"/hello", MainHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
], debug=True)

if __name__ == "__main__":
    print "Runserver..."
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()
