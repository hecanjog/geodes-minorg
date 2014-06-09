from pippi import dsp
from pippi import tune
from pippic.settings import config

from hcj import drums

shortname   = 'sn'
name        = 'snort'

def play(voice_id):
    bpm = config('bpm')

    root = config('key')
    quality = getattr(tune, config('quality')) 
    ratios = getattr(tune, config('tune')) 

    beat = dsp.bpm2frames(bpm)

    length = dsp.randint(dsp.stf(1), dsp.stf(3))

    wav = dsp.breakpoint([0] + [ dsp.rand(-1,1) for w in range(10) ] + [0], 512)
    win = dsp.wavetable('sine', 512)
    mod = dsp.wavetable('vary', 512)

    root = dsp.randchoose(tune.fromdegrees([1,3,5,8], octave=0, root='a'))

    pw = dsp.rand(0.1, 1)

    amp = dsp.rand(0.5, 1.2)

    mFreq = 0.01 / dsp.fts(length)

    out = dsp.pulsar(root, length, pw, wav, win, mod, 0.05, mFreq, amp)

#    out = dsp.env(out, 'vary')

    out = dsp.vsplit(out, dsp.mstf(1), dsp.mstf(500))
    out = dsp.randshuffle(out)
    out = [ dsp.pad(o, 0, dsp.randint(0, 4410)) for o in out ]
    out = [ dsp.pan(o, dsp.rand()) for o in out ]
    out = [ dsp.alias(o) for o in out ]
    out = [ o * dsp.randint(1, 30) for o in out ]
    out = [ dsp.env(o, 'random') for o in out ]
    out = [ dsp.amp(o, dsp.rand(0.9, 1.5)) for o in out ]

    out = ''.join(out)

    return out
