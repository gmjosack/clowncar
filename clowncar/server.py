import time

from . import exc


_DEFAULT_DOWN_RETRY = 30


class Server(object):
    def __init__(self, hostname, port, dead_retry=_DEFAULT_DOWN_RETRY):
        self.hostname = hostname
        self.port = int(port)
        self.dead_retry = dead_retry
        self.dead_until = None

    @property
    def dead(self):
        if self.dead_until and self.dead_until > time.time():
            return True
        self.dead_until = None
        return False

    def as_tuple(self):
        return (self.hostname, self.port)

    def mark_dead(self, retry=None):
        retry = self.dead_retry if retry is None else retry
        self.dead_until = time.time() + retry

    def __hash__(self):
        return hash(self.as_tuple())

    def __lt__(self, other): return self.as_tuple() <  other
    def __le__(self, other): return self.as_tuple() <= other
    def __eq__(self, other): return self.as_tuple() == other
    def __ne__(self, other): return self.as_tuple() != other
    def __gt__(self, other): return self.as_tuple() >  other
    def __ge__(self, other): return self.as_tuple() >= other

    def __repr__(self):
        return "Server({}, {}, {})".format(self.hostname, self.port, self.dead_retry)
