from pippi import dsp
from pippi import tune
from pippic.settings import config
from pippic.settings import get_param as P

shortname   = 'vi'
name        = 'vibes'

def play(voice_id):
    bpm = config('bpm')
    beat = dsp.bpm2frames(bpm)

    root = config('key')
    quality = getattr(tune, config('quality')) 
    ratios = getattr(tune, config('tune')) 

    bar = beat * dsp.randchoose([8, 16, 32])

    groot = tune.ntf('c') 

    scale = tune.fromdegrees([1,3,5,8], root=root, octave=2, ratios=ratios)

    v = dsp.read('sounds/vibesc1.wav').data

    out = ''

    lens = [ bar / 5, bar / 8, bar / 12 ]
#    lens = [ bar / 6, bar / 8, bar / 16 ]

    maxbend = 2
    maxbend = 0.02

    layers = []

    for nlen in lens:
        layer = ''

        nlen /= 2

        note = dsp.transpose(v, (dsp.randchoose(scale) * 2**dsp.randint(0, 2)) / groot)
        note = dsp.fill(note, nlen)
        note = dsp.env(note, 'phasor')
        note = dsp.amp(note, 0.125)

        nbeats = bar / nlen
        for b in range(nbeats):
            b = dsp.pan(note, dsp.rand())
            b = dsp.drift(b, dsp.rand(0, dsp.rand(0.01, maxbend)))

            if dsp.flen(b) < nlen:
                b = dsp.pad(b, 0, nlen - dsp.flen(b))

#            if dsp.rand() > 0.5:
#                b = dsp.vsplit(b, dsp.flen(b) / 3, dsp.flen(b) / 2)
#                b = dsp.randshuffle(b)
#                b = [ dsp.amp(bb, dsp.rand(0.5, 2)) for bb in b ]
#                b = ''.join(b)

            layer += b

#        layer = dsp.fill(layer, bar)

        layers += [ layer ]

    out = dsp.mix(layers)
    out = dsp.fill(out, bar)

    return out
