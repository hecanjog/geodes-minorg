from pippi import dsp
from pippi import tune
from pippic import rt
from pippic.settings import config
from pippic.settings import get_param as P

shortname   = 'gu'
name        = 'guitar'

def play(voice_id):
    bpm = config('bpm')
    key = config('key')
    quality = getattr(tune, config('quality')) 
    ratios = getattr(tune, config('tune')) 

    beat = dsp.bpm2frames(bpm)
    beat = beat / 4

    glitch = False
    alias = False
    nbeats = P(voice_id, 'multiple', dsp.randchoose([8, 16]))

    gs = ['gC1', 'gC2']
    g = dsp.randchoose(gs)
    n = dsp.read('sounds/%s.wav' % g).data

#    speeds = [1, 1.25, 1.5, 1.666, 2, 4]
    speeds = [1, 1.25, 1.5, 2, 3, 4, 6, 8, 16]

    root = tune.ntf('c')
    target = tune.ntf(key)

    n = dsp.transpose(n, target / root)
    n = dsp.fill(n, dsp.stf(20))
    n = dsp.transpose(n, dsp.randchoose(speeds))
    n = dsp.split(n, beat)
    n = dsp.randshuffle(n)
    n = n[:nbeats + 1]

    if alias:
        n = [ dsp.alias(nn) for nn in n ]

    n = [ dsp.amp(nn, dsp.rand(0.1, 0.75)) for nn in n ]
    n = [ dsp.pan(nn, dsp.rand()) for nn in n ]

    n = ''.join(n)

    out = n

    if glitch:
        out = dsp.vsplit(out, dsp.mstf(dsp.rand(80, 140)), dsp.mstf(500))
        out = dsp.randshuffle(out)
        out = ''.join(out)

    return out
