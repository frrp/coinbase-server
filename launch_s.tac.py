# Run me with "twistd -ny launcher_s.tac.py -l -"

# Run listening
from twisted.internet import defer
on_startup = defer.Deferred()

import config
from bitcoin_rpc import BitcoinRPC
bitcoin_rpc = BitcoinRPC(config.BITCOIN_TRUSTED_HOST,
                         config.BITCOIN_TRUSTED_PORT,
                         config.BITCOIN_TRUSTED_USER,
                         config.BITCOIN_TRUSTED_PASSWORD)

# initialize the current prevhash (updated in BitcoindUpdater)
current_prevhash = None

# TODO: Start the VC twisted server here
import server
server.setup(on_startup)
#################

# TODO: communication with bitcoind
from bitcoind_updater import BitcoindUpdater
BitcoindUpdater(bitcoin_rpc, current_prevhash)
#################

# TODO: communication with VC database
from db_updater import DBUpdater
DBUpdater()
