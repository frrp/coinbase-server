from unittest import TestCase, main
from server import VirginServer


class TestVirginServer(TestCase):
    def test_set_some(self):
        VS = VirginServer
        self.assert_(VS)

    def test_set_coinbase(self):
        self.fail()


if __name__ == '__main__':

    main()
