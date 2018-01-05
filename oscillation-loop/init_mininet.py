import os
from contextlib import contextmanager

from mininet.cli import CLI
from mininet.log import info, setLogLevel
from mininet.net import Mininet
from mininet.node import Node
from mininet.topo import Topo


class Router(Node):
    """A Node with IP forwarding enabled and the BIRD routing daemon running"""

    @contextmanager
    def in_router_dir(self):
        working_dir = os.getcwd()
        self.cmd('cd %s' % self.name)
        yield
        self.cmd('cd %s' % working_dir)

    def config(self, **params):
        super(Router, self).config(**params)

        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

        # Startup BIRD
        with self.in_router_dir():
            self.cmd('bird -l')

    def terminate(self):
        # Disable forwarding
        self.cmd('sysctl net.ipv4.ip_forward=0')

        # Shutdown BIRD
        with self.in_router_dir():
            self.cmd('birdc -l down')

        super(Router, self).terminate()


class DisabledRouter(Node):
    """A Node with IP forwarding enabled and the BIRD routing daemon running"""

    @contextmanager
    def in_router_dir(self):
        working_dir = os.getcwd()
        self.cmd('cd %s' % self.name)
        yield
        self.cmd('cd %s' % working_dir)

    def config(self, **params):
        super(DisabledRouter, self).config(**params)

        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')

        super(DisabledRouter, self).terminate()


def prefix(address, length):
    return "%s/%s" % (address, str(length))


class Topology(Topo):
    def build(self, *args, **params):
        r1_eth1 = '10.1.1.1'
        r4_eth1 = '10.1.1.2'
        r1_eth2 = '10.1.2.1'
        r2_eth1 = '10.1.2.2'
        r2_eth2 = '10.1.3.1'
        r3_eth1 = '10.1.3.2'
        r3_eth2 = '10.1.4.1'
        r1_eth3 = '10.1.4.2'

        r1 = self.addNode('r1', cls=Router, ip=prefix(r1_eth1, 24))
        r2 = self.addNode('r2', cls=Router, ip=prefix(r2_eth1, 24))
        r3 = self.addNode('r3', cls=Router, ip=prefix(r3_eth1, 24))
        r4 = self.addNode('r4', cls=Router, ip=prefix(r4_eth1, 24))

        self.addLink(r1, r4,
                     intfName1='r1-eth1', params1={'ip': prefix(r1_eth1, 24)},
                     intfName2='r4-eth1', params2={'ip': prefix(r4_eth1, 24)})

        self.addLink(r1, r2,
                     intfName1='r1-eth2', params1={'ip': prefix(r1_eth2, 24)},
                     intfName2='r2-eth1', params2={'ip': prefix(r2_eth1, 24)})

        self.addLink(r2, r3,
                     intfName1='r2-eth2', params1={'ip': prefix(r2_eth2, 24)},
                     intfName2='r3-eth1', params2={'ip': prefix(r3_eth1, 24)})

        self.addLink(r3, r1,
                     intfName1='r3-eth2', params1={'ip': prefix(r3_eth2, 24)},
                     intfName2='r1-eth3', params2={'ip': prefix(r1_eth3, 24)})


def run():
    """Test linux router"""
    topology = Topology()
    net = Mininet(topo=topology, controller=None)
    net.start()

    for node, type in net.items():
        if isinstance(type, Router):
            info('*** Routing Table on Router %s:\n' % node)
            info(net[node].cmd('route'))

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
