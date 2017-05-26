import web
import fetch
import threading

urls = (
    '/','index'
)

class index:
    def GET(self):
    	thread = threading.Thread(target=fetch.fetch,args=(web.input().id,))
    	thread.start()
        return "start fetch"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()