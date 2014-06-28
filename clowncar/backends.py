from hashlib import md5
import time
from socket import gethostname

from . import exc
from .server import Server


class Backends(object):
    def __init__(self, servers, partition_key):
        self._get_servers = self._normalize_servers(servers)
        self._get_partition_key = self._normalize_partition_key(partition_key)

    @property
    def servers(self):
        servers = []
        for server in self._get_servers():
            if server.dead:
                continue
            servers.append(server)
        return servers

    @property
    def partition_key(self):
        return self._get_partition_key()

    @property
    def server(self):
        servers = self.servers
        if not servers:
            raise exc.NoAvailableBackends("No available backend server instances.")
        key = self._get_partition_key()
        index = int(md5(key).hexdigest(), 16) % len(servers)
        return servers[index]

    def _normalize_servers(self, servers):
        if callable(servers):
            return servers
        elif isinstance(servers, basestring) and servers.count(":") == 1:
            hostname, port = servers.split(":")
            return lambda: [Server(hostname, port)]
        elif isinstance(servers, (list, set, tuple)):
            new_servers = []
            for server in servers:
                if isinstance(server, basestring) and server.count(":") == 1:
                    hostname, port = server.split(":")
                    new_servers.append(Server(hostname, port))
                else:
                    raise TypeError("Invalid type to servers argument.")
            return lambda: new_servers

        raise TypeError("Invalid type to servers argument.")

    def _normalize_partition_key(self, partition_key):
        if partition_key is None:
            partition_key = gethostname()

        if callable(partition_key):
            return partition_key
        elif isinstance(partition_key, basestring):
            return lambda: partition_key

        raise TypeError("Invalid type to partition_key argument.")
