import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
from scipy import integrate

# evaluation VDE
def cyclePower_evaluator(CD, cycle):
    F = CD[0:3]
    M = CD[3]
    df = pd.DataFrame()
    df['FCD'] = F[0] + F[1] * cycle.Data['speed'] + F[2] * cycle.Data['speed'] * cycle.Data['speed']
    df['PCD'] = df['FCD'] * cycle.Data['speed'] / 3.6
    df['Fi'] = M * cycle.Data['acc']
    df['Pi'] = df['Fi'] * cycle.Data['speed'] / 3.6
    df['d'] = np.trapz(cycle.Data['speed'] / 3.6, cycle.Data['time'].values)

    VDP = df['PCD'] + df['Pi']
    df['VDPp'] = VDP
    df['VDPn'] = VDP
    df['VDPp'][VDP < 0] = 0
    df['VDPn'][VDP > 0] = 0
    df['VDEp'] = integrate.cumtrapz(df['VDPp'], cycle.Data['time'].values, initial = 0) #integral of derivative
    df['VDEn'] = integrate.cumtrapz(df['VDPn'], cycle.Data['time'].values, initial=0)  # integral of derivative
    df['time'] = cycle.Data['time']
    VDE = np.trapz(df['VDPp'], cycle.Data['time'].values)  # definizione classica

    VDE_mch_rw = np.trapz(df['VDPn'], cycle.Data['time'].values)  # meccanica alle ruote in rigenerazione
    return (VDE, VDE_mch_rw), df

def VDE_variation(cycles, CD, n, varID, fig = None):
    import plotly.graph_objects as go
    F = CD[0:3]
    M = CD[3]
    CDvar = CD[0:4]
    n_trac = n[0]
    n_rege = n[1]

    if fig is None:
        fig = make_subplots(rows=4, cols=3)

    color = [
        '#1f77b4',  # muted blue
        '#ff7f0e',  # safety orange
        '#2ca02c',  # cooked asparagus green
        '#d62728',  # brick red
        '#9467bd',  # muted purple
        '#8c564b',  # chestnut brown
        '#e377c2',  # raspberry yogurt pink
        '#7f7f7f',  # middle gray
        '#bcbd22',  # curry yellow-green
        '#17becf'  # blue-teal
    ]

    for k, cycle in enumerate(cycles):
        VDEp = []
        VDEn = []
        variation_space = np.linspace(-20, 20, 100)
        VDE, df = cyclePower_evaluator(CD, cycle)
        for var in variation_space:
            var = CD[varID] * (1 + var / 100)
            CDvar[varID] = var
            VDE_var, df = cyclePower_evaluator(CDvar, cycle)
            VDEp.append(VDE_var[0])
            VDEn.append(VDE_var[1])

        cycles[k].VDE = VDE
        VDEp = np.array(VDEp)
        VDEn = np.array(VDEn)
        DeltaVDEp = (VDEp - VDE[0]) / VDE[0] * 100
        DeltaVDEn = (VDEn - VDE[1]) / VDE[1] * 100
        DeltaVDEsBase = VDE[0] / n_trac + VDE[1] * n_rege
        DeltaVDEs = (((VDEp / n_trac + VDEn * n_rege) - DeltaVDEsBase) / DeltaVDEsBase) * 100
        legend = not (varID>0)
        fig.add_trace(go.Scatter(x=variation_space, y=DeltaVDEp,
                                 mode='lines', name=cycle.name, legendgroup=cycle.name + '_group',
                                 marker_color=color[k], showlegend=legend),
                                 row=varID+1, col=1)
        fig.add_trace(go.Scatter(x=variation_space, y=DeltaVDEn,
                                 mode='lines', name=cycle.name, legendgroup=cycle.name + '_group',
                                 marker_color=color[k], showlegend=False),
                                 row=varID+1, col=2)
        fig.add_trace(go.Scatter(x=variation_space, y=DeltaVDEs,
                                 mode='lines', name=cycle.name, legendgroup=cycle.name + '_group',
                                 marker_color=color[k], showlegend=False),
                                 row=varID+1, col=3)
    return fig