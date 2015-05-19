## twisted virgin server

#import config
from twisted.spread import pb

#VSERVER = None
server_port = 3305

# test values ???
addresses = ('ad1', 'ad2')
values = (2, 3)
height = 50
prevhash = 'abc4'

# indicator of new VC addresses (needed??)
addresses_ready = True

class VirginServer(pb.Root):

    def __init__(self):
        # Fire callback when server is ready
        # self.on_load = defer.Deferred()
        for method in self._remote_methods:
            method = str(method).strip()
            VirginServer.__dict__['remote_' + method] = VirginServer.__dict__[method]

        self.addresses = addresses
        self.values = values
        self.height = height
        self.prevhash = prevhash

        self._reconnect_state = {'status': 'none'}
        self._shutdown_in_progress = False

    _remote_methods = ('set_registry', 'set_some')

    #@staticmethod
    def set_some(self, slave):
        print "received a slave called ", slave
        slave.callRemote("print", "Test")
        if addresses_ready:
            slave.callRemote("set_addresses", self.addresses, self.values, self.height, self.prevhash)

    def set_registry(self):
        # not needed
        pass



def setup(setup_event=None):
    from twisted.application import service
    application = service.Application("VC-server")

    if setup_event == None:
        setup_finalize(None, application)
    else:
        setup_event.addCallback(setup_finalize, application)

    return application

def setup_finalize(event, application):
    global VSERVER

    from twisted.application import internet
    #from twisted.internet import reactor
    #from mining.service import MiningServiceEventHandler
    #import socket_transport
    # Set up thread pool size for service threads
    # reactor.suggestThreadPoolSize(config.THREAD_POOL_SIZE)
    # Attach Socket Transport service to application
    '''
    VSERVER = internet.TCPServer(config.LISTEN_SOCKET_TRANSPORT,
                                socket_transport.SocketTransportFactory(debug=config.DEBUG,
                                                                        event_handler=MiningServiceEventHandler,
                                                                        tcp_proxy_protocol_enable=config.TCP_PROXY_PROTOCOL))
    VSERVER.setServiceParent(application)
    '''

    serverfactory = pb.PBServerFactory(VirginServer())
    VSERVER = internet.TCPServer(server_port, serverfactory).setServiceParent(application)

    return event

if __name__ == '__main__':
    print "This is not executable script. Try 'twistd -ny launcher.tac instead!"
