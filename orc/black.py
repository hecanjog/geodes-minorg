from pippi import dsp
from pippi import tune
from pippic import rt
from pippic.settings import config
from pippic.settings import get_param as P

shortname   = 'bl'
name        = 'black'

def play(voice_id):
    bpm = config('bpm')
    key = config('key')
    quality = getattr(tune, config('quality')) 
    ratios = getattr(tune, config('tune')) 

    beat = dsp.bpm2frames(bpm)
    nlen = beat / dsp.randchoose([4,5,6,7,8,9,10])

    root = 340.0
    target = tune.ntf(key)

    n = dsp.read('sounds/mike.wav').data
    n = dsp.transpose(n, target / root)
    n = dsp.amp(n, 0.4)

    length = dsp.randint(16, 64) * beat
    ngrains = length / nlen

    n = dsp.transpose(n, dsp.randchoose([0.5, 1, 2, 2, 4, 4]))
    n = dsp.split(n, nlen)

    snd = dsp.randchoose(n)
    snd = dsp.env(snd, 'sine')

    grains = [ snd for i in range(ngrains) ]
    grains = [ dsp.pan(grain, dsp.rand()) for grain in grains ]

    out = ''.join(grains)
    out = dsp.env(out, 'sine')

#    out = dsp.pad(out, 0, dsp.stf(dsp.randint(0.5, 3)))

    return out
