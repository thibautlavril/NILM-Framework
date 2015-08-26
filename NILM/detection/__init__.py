# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 15:03:12 2015

@author: thibaut
"""

from simple_edge import simple_edge
from steady_states import steady_states


__all__ = {
        "simple_edge": {
            "model": simple_edge,
            "parameters": {
                "edge_threshold": 70}},
        "steady_states": {
            "model": steady_states,
            "parameters": {
                "edge_threshold": 70,
                "state_threshold": 15}}}
