from .backends.jsonrpc import JSONRPCDaemon


class Daemon(object):
    """Beldex daemon.

    Provides interface to a daemon instance.

    :param backend: a daemon backend
    :param \\**kwargs: arguments to initialize a :class:`JSONRPCDaemon <beldex.backends.jsonrpc.JSONRPCDaemon>`
                        instance if no backend is given
    """

    def __init__(self, backend=None, **kwargs):
        if backend and len(kwargs):
            raise ValueError("backend already given, other arguments are extraneous")

        self._backend = backend if backend else JSONRPCDaemon(**kwargs)

    def info(self):
        """
        Returns basic information about the daemon.

        :rtype: dict
        """
        return self._backend.info()

    @property
    def net(self):
        return self._backend.net()

    def height(self):
        """
        Return daemon's chain height.

        :rtype: int
        """
        return self._backend.info()["height"]

    def send_transaction(self, tx, relay=True):
        """
        Sends a transaction generated by a :class:`Wallet <beldex.wallet.Wallet>`.

        :param tx: :class:`Transaction <beldex.transaction.Transaction>`
        :param relay: whether to relay the transaction to peers. If `False`, the daemon will have
                to mine the transaction itself in order to have it included in the blockchain.
        """
        return self._backend.send_transaction(tx.blob, relay=relay)

    def mempool(self):
        """
        Returns current mempool contents.

        :rtype: list of :class:`Transaction <beldex.transaction.Transaction>`
        """
        return self._backend.mempool()

    def headers(self, start_height, end_height=None):
        """
        Returns block headers for given height range.
        If no :param end_height: is given, it's assumed to be equal to :param start_height:

        :rtype: list of dict
        """
        return self._backend.headers(start_height, end_height)

    def block(self, bhash=None, height=None):
        """
        Returns a block of specified height or hash.

        :param str bhash: block hash, or
        :param int height: block height

        :rtype: :class:`Block <beldex.block.Block>`
        """
        if height is None and bhash is None:
            raise ValueError("Height or hash must be specified")
        return self._backend.block(bhash=bhash, height=height)

    def transactions(self, hashes):
        """
        Returns transactions matching given hashes. Accepts single hash or a sequence.

        :param hashes: str or list of str
        """
        if isinstance(hashes, str):
            hashes = [hashes]
        return self._backend.transactions(hashes)
