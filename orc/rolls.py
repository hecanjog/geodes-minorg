from pippi import dsp
from pippi import tune

from pippic.settings import get_param as P
from pippic.settings import config as C

shortname   = 'ro'
name        = 'rolls'

def play(voice_id):
    bpm = C('bpm')
    beat = dsp.bpm2frames(bpm)
    volume = P(voice_id, 'volume', default=1.0)

    crinkle = dsp.read('sounds/s/crinkle.wav').data
    glass1 = dsp.read('sounds/s/glass1.wav').data
    glass2 = dsp.read('sounds/s/glass2.wav').data
    toys = dsp.read('sounds/s/rolling.wav').data

    c = dsp.vsplit(crinkle, dsp.mstf(10), dsp.stf(3))
    c = dsp.randshuffle(c)
    c = c[:40]
    c = [ dsp.pan(cc, dsp.rand()) for cc in c ]
    c = [ dsp.env(cc, 'sine') for cc in c ]
    c = [ dsp.transpose(cc, dsp.rand(0.25, 0.5)) for cc in c ]

    t = dsp.vsplit(toys, dsp.mstf(10), dsp.stf(1))
    t = dsp.randshuffle(t)
    t = t[:40]
    t = [ dsp.amp(tt, dsp.rand(0.1, 0.75)) for tt in t ]
    t = [ dsp.pan(tt, dsp.rand(0, 1)) for tt in t ]
    t = [ dsp.env(tt, 'sine') for tt in t ]
    t = [ dsp.transpose(tt, 0.5) for tt in t ]

    g = dsp.vsplit(glass2, dsp.mstf(1), dsp.mstf(100))
    g = dsp.randshuffle(g)
    g = g[:40]
    g = [ dsp.amp(gg, dsp.rand(0.65, 0.85)) for gg in g ]
    g = [ dsp.transpose(gg, dsp.rand(0.5, 1.75)) for gg in g ]
    g = [ gg * dsp.randint(1, 8) for gg in g ]

    things = [c,t,g]

    out = [ dsp.mix([ dsp.randchoose(dsp.randchoose(things)) for l in range(dsp.randint(2, 4)) ]) for i in range(4) ]
    out = ''.join(out)

    dsp.log('voice %s length: %.2f' % (voice_id, dsp.fts(dsp.flen(out))))

    return out
