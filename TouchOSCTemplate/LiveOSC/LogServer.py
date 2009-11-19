import SocketServer
import time

class LoggerRequestHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        print self.client_address, 'connected!'

    def handle(self):
        while 1:
            time.sleep(0.01)
            data = self.request.recv(1024)
            if len(data.strip()) > 0 :
                print data.strip()

    def finish(self):
        print self.client_address, 'disconnected!'

if __name__=='__main__':
    server = SocketServer.ThreadingTCPServer(('localhost', 4444), LoggerRequestHandler)
    server.serve_forever()

