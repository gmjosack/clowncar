import pytest
import time

from clowncar.backends import Backends
from clowncar.exc import NoAvailableBackends


def test_backend_creation():
    """ Test Creating a backend with various arguments."""

    backend = Backends("localhost:8888", "pkey")
    assert backend.servers == [("localhost", 8888)]
    assert backend.server == ("localhost", 8888)

    backend = Backends(["localhost:8888", "localhost:8989"], "pkey")
    assert backend.servers == [("localhost", 8888), ("localhost", 8989)]

def test_markdead():
    """ Test marking the active server dead."""

    backend = Backends([
        "localhost:8881",
        "localhost:8882",
        "localhost:8883",
        "localhost:8884",
        "localhost:8885",
    ], "pkey")

    assert backend.server == ("localhost", 8884)
    backend.server.mark_dead(.2)
    assert backend.server == ("localhost", 8885)
    time.sleep(.3)
    assert backend.server == ("localhost", 8884)

def test_nobackends():
    """ Test when all backends have been marked dead."""

    backend = Backends([
        "localhost:8881",
        "localhost:8882",
    ], "pkey")

    assert backend.server == ("localhost", 8882)
    backend.server.mark_dead(.2)
    assert backend.server == ("localhost", 8881)
    backend.server.mark_dead(.2)

    with pytest.raises(NoAvailableBackends):
        backend.server

    time.sleep(.3)
    assert backend.server == ("localhost", 8882)
