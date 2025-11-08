# -*- coding: utf-8 -*-

def classFactory(iface):
    from .road_network_plugin import RoadNetworkPlugin
    return RoadNetworkPlugin(iface)