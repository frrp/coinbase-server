## virgin coin app server
## ----------------------
"""
Checks addresses from V.C. db, and when they are paid, takes both addresses and values from the db (to amount less than
one block), the remaining coins will be send to the default pool address.
Provides (pushes through twisted remote) the addresses and values to V.C. clients (stratums) - they maintain a persistent connection.
In sync with bitcoind - when new block is found, checks who found it and decides accordingly.
"""

reward = 25 # or get it from the btc network
all_values = 1+2

## list of 2 lists for addresses and amounts of virgin coins to send:
virgin_addresses = [[address1, address2, config_location.CENTRAL_WALLET],
                    [1, 2, reward-all_values]]
# check that # of addresses = # of values
####


from new_coinbaser import NewCoinbaser

def setup(setup_event=None):
    pass


# TODO: management of the vc db
## return values and addresses
def get_values():
    return virgin_addresses[1]

def get_addresses():
    return virgin_addresses[0]


## TODO: coinbase creation

def create_coinbase():
    addresses = get_addresses
    # coinbaser = SimpleCoinbaser(bitcoin_rpc, config.CENTRAL_WALLET)
    coinbaser = NewCoinbaser(bitcoin_rpc, addresses)
    (yield coinbaser.on_load)


## TODO: twisted server
from twisted.spread import pb
from twisted.application.internet import TCPServer
from twisted.application.service import Application

class VirginCoinServer(pb.Root):

    addresses = ('ad1', 2, 'ad2', 3)

    def __init__(self):
        # Fire callback when server is ready
        self.on_load = defer.Deferred()
        for method in self._remote_methods:
            method = str(method).strip()
            VirginCoinServer.__dict__['remote_' + method] = VirginCoinServer.__dict__[method]

        self._reconnect_state = {'status': 'none'}
        self._shutdown_in_progress = False

    _remote_methods = ('set_coinbase', 'set_some')

    #@staticmethod
    def set_some(self, slave):
        print "received a slave called", slave
        slave.callRemote("print", 22)
        slave.callRemote("set_addresses", self.addresses)

    def set_coinbase(self):
        pass

serverfactory = pb.PBServerFactory(VirginCoinServer())
application = Application("virgin")
VServerService = TCPServer(3305, serverfactory)
VServerService.setServiceParent(application)
