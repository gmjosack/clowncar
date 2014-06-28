from hashlib import md5
import time
from socket import gethostname

from . import exc

class Backends(object):
    def __init__(self, servers, partition_key):
        self._marked_bad = {}
        self._get_servers = self._normalize_servers(servers)
        self._get_partition_key = self._normalize_partition_key(partition_key)

    @property
    def servers(self):
        all_servers = self._get_servers()
        bad_servers = set()
        now = time.time()
        for server, timeout in self._marked_bad.items():
            if timeout < now:
                del self._marked_bad[server]
                continue
            bad_servers.add(server)

        return sorted(all_servers - bad_servers)

    @property
    def partition_key(self):
        return self._get_partition_key()

    @property
    def server(self):
        servers = self.servers
        if not servers:
            raise exc.NoAvailableBackends("No available backend server instances.")

        key = self._get_partition_key()
        # TODO(gary) cache the digest but need to worry about
        #            randomized keys, possibly lru.
        index = int(md5(key).hexdigest(), 16) % len(servers)
        return servers[index]

    def mark_bad(self, server, timeout):
        self._marked_bad[server] = timeout + time.time()

    def _normalize_servers(self, servers):
        if callable(servers):
            return servers
        elif isinstance(servers, basestring) and servers.count(":") == 1:
            server, port = servers.split(":")
            return lambda: set([(server, int(port))])
        elif isinstance(servers, (list, set, tuple)):
            new_servers = set()
            for server in servers:
                if isinstance(server, basestring) and server.count(":") == 1:
                    server, port = server.split(":")
                    port = int(port)
                    new_servers.add((server, port))
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
