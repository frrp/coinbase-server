#TODO: server keeps connection to bitcoind, deserializes coinbase, checks cb address...
# inspired by BlockUpdater

import StringIO
import config
import binascii
from twisted.internet import reactor, defer
#import util
#from poolsrv.posix_time import posix_time
import halfnode
import poolsrv.logger
log = poolsrv.logger.get_logger()

global current_prevhash

class BitcoindUpdater(object):
    # detecting a new block on the network.

    def __init__(self, bitcoin_rpc, current_prevhash):
        # Fire callback when server is ready
        # self.on_load = defer.Deferred()

        self.bitcoin_rpc = bitcoin_rpc
        self.clock = None
        self.schedule()
        self.current_prevhash = current_prevhash

    def schedule(self):
        when = self._get_next_time()
        self.clock = reactor.callLater(when, self.run) #@UndefinedVariable

    def _get_next_time(self):
        when = config.PREVHASH_REFRESH_INTERVAL
        return when

    @defer.inlineCallbacks
    def run(self):
        try:
            # we could ask the stratums to give us the template, but it's an overkill
            if self.current_prevhash == None: # we run this for the first time
                self.current_prevhash = yield self.bitcoin_rpc.get_best_block_hash() # this always holds: BITCOIN_VERSION_0_9_PLUS
            else:
                prevhash = yield self.bitcoin_rpc.get_best_block_hash()
                if prevhash and prevhash != self.current_prevhash:
                    log.info("New block! Prevhash: %s" % prevhash)
                    # deserialize the coinbase tx
                    # check coinbase address(es), if they are same as the current VC addresses, set new ones to client
                    block = yield self.bitcoin_rpc.getblock(prevhash, 'true')
                    t = halfnode.CTransaction()
                    transactions = block['tx'] # txids

                    cb = yield self.bitcoin_rpc.gettxout(transactions[i]) # the first transaction is coinbase
                    # if cb['coinbase'] == 'true': # what if the first tx is not coinbase ??
                    addrs = cb['addresses']
                    # t.deserialize(StringIO.StringIO(binascii.unhexlify()))
                    if addrs[0] in current_vc_addresses: # first output address is among our current addresses, other should be too
                        pass # set new current addresses to the client

                    self.current_prevhash = prevhash

        except Exception:
            log.exception("UpdateWatchdog.run failed")
        finally:
            self.schedule()