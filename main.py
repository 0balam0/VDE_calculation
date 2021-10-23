from mss_uff_reader import Cycle
from VDE_calulation import cyclePower_evaluator
from VDE_calulation import VDE_variation
import numpy as np
import pandas as pd

import os
# plot library
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# report generator
import dash
from dash import dcc
from dash import html

# color = [
#     '#1f77b4',  # muted blue
#     '#ff7f0e',  # safety orange
#     '#2ca02c',  # cooked asparagus green
#     '#d62728',  # brick red
#     '#9467bd',  # muted purple
#     '#8c564b',  # chestnut brown
#     '#e377c2',  # raspberry yogurt pink
#     '#7f7f7f',  # middle gray
#     '#bcbd22',  # curry yellow-green
#     '#17becf'   # blue-teal
#     ]

# lettura file mms
cycleFolder = '.\\cycle\\uff\\'
cycles = []
for k, file in enumerate(os.listdir('.\\cycle\\uff\\')):#C:\Users\matteo.demarco\Desktop\pythonPoject\VDE_evaluator\cycle\uff\Custom_MCT_UHU R_USA - BEVER_Template (TEST).mss
    cycles.append(Cycle())
    cycles[k].File['name'] = file#r'Custom_MCT_UHU R_USA - BEVER_Template (TEST).mss'
    cycles[k].File['dir'] = cycleFolder
    cycles[k].ReadGofastFile()
    cycles[k].AccEvaluation()


# Caratteristiche veicolo
CD = [112, 0.255, 0.0254, 2500]
n_trac = 0.6
n_rege = 0.6

# VDE evaluation
for cycle in cycles:
    VDE, df = cyclePower_evaluator(CD, cycle)
    cycle.VDE = {'VDE': VDE, 'df': df}
    print(f"{cycle.File['name']}:\t{cycle.VDE['VDE']}")

cycles[1].VDE['df'].to_csv('.\\prova.csv')
# # VDE sensitivity
# fig = make_subplots(rows=4, cols=3)
# VDE_variation(cycles, CD, [n_trac, n_rege], 0, fig)
# VDE_variation(cycles, CD, [n_trac, n_rege], 1, fig)
# VDE_variation(cycles, CD, [n_trac, n_rege], 2, fig)
# VDE_variation(cycles, CD, [n_trac, n_rege], 3, fig)
#
# fig.show()

# Cycle plot
















# i = 0
# print(cycles[i].name)
# VDE, df = cyclePower_evaluator(CD, cycles[i])
# print(VDE)