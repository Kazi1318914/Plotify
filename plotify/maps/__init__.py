"""
plotify.maps
============

Geographic / spatial plots: ChoroplethMap, BubbleMap, HexbinMap,
Cartogram, ConnectionMap.
"""

from plotify.maps.bubble_map import BubbleMap
from plotify.maps.cartogram import Cartogram
from plotify.maps.choropleth_map import ChoroplethMap
from plotify.maps.connection_map import ConnectionMap
from plotify.maps.hexbin_map import HexbinMap

__all__ = [
    "BubbleMap",
    "Cartogram",
    "ChoroplethMap",
    "ConnectionMap",
    "HexbinMap",
]
