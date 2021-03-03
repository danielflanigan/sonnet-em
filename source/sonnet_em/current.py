from __future__ import absolute_import, division, print_function

import numpy as np
import pandas as pd


def one_line(filename):
    meta = dict()
    with open(filename) as f:
        # VER : 2,,U:/Commun/Projet CQPS TiN/Calculs/Sonnet/cross-correlation_experiment/...
        meta['file version'], _, meta['original filename'] = f.readline().strip().split(',')
        # sonnet,17.54, Exported Data from:,cpw_section_all_sc_slotline
        _, meta['EM version'], _, meta['exported data from'] = f.readline().strip().split(',')
        # Parameters:,Lk_pH_per_square=1000.0 trace=5.0 gap=5.0 ground=300.0
        line2 = f.readline().strip().split(',')
        assert line2[0] == 'Parameters:'
        kv_pairs = [token.split('=') for token in line2[1]]
        meta['parameters'] = dict([(kv[0], float(kv[1])) for kv in kv_pairs])
        # Frequency:,1e+09
        line3 = f.readline().strip().split(',')
        assert line3[0] == 'Frequency:'
        meta['frequency'] = float(line3[1])
        # Drive:,Port 1,V,1,P,0,Port 2,V,0,P,0,
        line4 = f.readline().strip().split(',')
        assert line4[0] == 'Drive:'
        meta['drive'] = line4[1:]
        # theLevel:, 0, 0
        line5 = f.readline().strip().split(',')
        assert line5[0] == 'theLevel:'
        meta['level'] = line5[1:]
        # Export Positions in:,UM,1e-06
        line6 = f.readline().strip().split(',')
        assert line6[0] == 'Export Positions in:'
        meta['units'] = dict(symbol=line6[1], value=float(line6[2]))
        # Export Steps:,0.125,UM, by,0.125,UM,Area,0.015625,MKS Area,1.5625e-14,m^2
        line7 = f.readline().strip().split(',')
        # JX Magnitude,Complex Form,Amps/Meter
        line8 = f.readline().strip().split(',')
        meta['physical quantity'], meta['form'], meta['current units'] = line8
        # X Directed
        line9 = f.readline().strip().split(',')
        # Y Position
        line10 = f.readline().strip()
        meta['coordinate'] = line10.split(' ')[0].lower()
        # X Position ->,100.000000
        line11 = f.readline().strip().split(',')
        meta[line11[0]] = float(line11[1])
    if 'complex' in meta['form'].lower():
        df = pd.read_csv(filename, header=11, names=[meta['coordinate'], meta['physical quantity']],
                         converters={1: lambda s: sum([complex(n) for n in s.strip().split(' ')])}
                         ).iloc[::-1]  # Reverse to start with the lowest y-values
    return df, meta
