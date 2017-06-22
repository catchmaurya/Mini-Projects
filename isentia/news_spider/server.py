# Import your application as:
# from wsgi import application
# Example:
from functools import wraps
from wsgi import application
from cherrypy import expose, tools, response
# Import CherryPy
import cherrypy
import json

def error_page_404(status, message, traceback, version):
    return "404 Error!"

def jsonify(func):
    '''JSON decorator for CherryPy'''
    @wraps(func)
    def wrapper(*args, **kw):
        value = func(*args, **kw)
        response.headers["Content-Type"] = "application/json"
        return json.dumps(value)

    return wrapper

class News:
    def getdb(self):
        from pymongo import MongoClient
        client = MongoClient('localhost:27017')
        db = client.journal
        return db

    @expose
    def index(self):
        return "Welcome to isentia demo AWS-REST api!"

    @expose
    @tools.json_out()
    @tools.json_in()
    def getnews(self,**kwargs):
        #input_json = cherrypy.request.json
        mydict = eval(cherrypy.request.headers.get('Json'))
#        import pdb;pdb.set_trace();
        category = mydict["category"].lower()
        db = self.getdb()
        result = db.news.find({'article':category})
        outputdic = []
        count = 1
        for i in result:
            tempdic = {}
            print i
            tempdic['id']=count
            tempdic['keyword'] = i['keyword']
            tempdic['author'] = i['author']
            tempdic['headline'] = i['headline']
            tempdic['url'] = i['url']
            tempdic['date'] = i['date']
            tempdic['article'] = i['article']
            count = count + 1
            outputdic.append(tempdic)
        return {'result': outputdic}

if __name__ == '__main__':

    # Mount the application
    cherrypy.tree.graft(application, "/")

    # Unsubscribe the default server
    cherrypy.server.unsubscribe()

    # Instantiate a new server object
    server = cherrypy._cpserver.Server()

    # Configure the server object
    server.socket_host = "0.0.0.0"
    server.socket_port = 8080
    server.thread_pool = 30

    # For SSL Support
    # server.ssl_module            = 'pyopenssl'
    # server.ssl_certificate       = 'ssl/certificate.crt'
    # server.ssl_private_key       = 'ssl/private.key'
    # server.ssl_certificate_chain = 'ssl/bundle.crt'

    # Subscribe this server
    server.subscribe()

    # Example for a 2nd server (same steps as above):
    # Remember to use a different port

    # server2             = cherrypy._cpserver.Server()

    # server2.socket_host = "0.0.0.0"
    # server2.socket_port = 8081
    # server2.thread_pool = 30
    # server2.subscribe()

    # Start the server engine (Option 1 *and* 2)

    cherrypy.quickstart(News())

#    cherrypy.engine.start(News())
#    cherrypy.engine.block()
