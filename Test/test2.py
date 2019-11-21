from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

authorizer = DummyAuthorizer()
authorizer.add_user("user", "12345", "/home/pi", perm="elradfmw")
authorizer.add_anonymous("/home/pi/", perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("192.168.50.34", 1026), handler)
server.serve_forever()

