from pippi import dsp
from pippi import tune
from pippic.settings import config

from hcj import keys

shortname   = 'we'
name        = 'weeds'
device      = 'default'

def play(voice_id):
    reload(keys)

    bpm = config('bpm')
    root = config('key')
    quality = getattr(tune, config('quality')) 
    ratios = getattr(tune, config('tune')) 

    scale = [1,6,8,9]

    if dsp.rand() > 0.5:
        scale = reversed(scale)

    freqs = tune.fromdegrees(scale, root=root, octave=dsp.randint(0, 2), ratios=ratios, scale=quality)

    freqs = dsp.rotate(freqs, dsp.randint(0, len(freqs)))

    out = ''

    length = int(dsp.bpm2frames(bpm) * dsp.randchoose([0.25, 0.5, 1]) * 0.5) 
    length = dsp.bpm2frames(bpm) * 4
    length = dsp.stf(dsp.rand(0.05, 0.5))
    for n in range(dsp.randint(1, 3)):
        amp = dsp.rand(0.5, 1)
        freq = dsp.randchoose(freqs)
        freq = freqs[n%len(freqs)]
        b = keys.chippy(length=length, freq=freq, amp=amp)

        b = dsp.split(b, 100)

        oenvs = dsp.breakpoint([0,0,0,0] + [ dsp.rand() for i in range(len(b) / 10) ], len(b))
        opans = dsp.breakpoint([dsp.rand(0.4, 0.6)] + [ dsp.rand() for i in range(len(b) / 100) ] + [0.5], len(b))
        b = [ dsp.amp(b[i], oenvs[i]) for i in range(len(b)) ]
        b = [ dsp.pan(b[i], opans[i]) for i in range(len(b)) ]

        b = ''.join(b)
        #b = dsp.env(b, 'phasor')
        b = dsp.env(b, 'sine')

        out += b

    return out
