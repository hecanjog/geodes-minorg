from pippi import dsp
from pippi import tune
from pippic.settings import config

from hcj import keys

shortname   = 'bo'
name        = 'boing'

def easeOutQuad(t, b, c, d):
    t /= d
    return -c * t*(t-2) + b

def easeOutQuart(t, b, c, d):
    t /= d
    t -= 1
    return -c * (t*t*t*t - 1) + b

def play(voice_id):
    bpm = config('bpm')
    root = config('key')
    quality = getattr(tune, config('quality')) 
    ratios = getattr(tune, config('tune')) 

    bendfactor = 0.05
#    bendfactor = 0 

    bdiv = 4
    bdiv *= dsp.randchoose([16, 24, 32]) 
    loctave = 1
    hoctave = 4

    si = 32 * dsp.randint(1, 2)
    beat = dsp.bpm2frames(bpm) / bdiv

    y = [ easeOutQuad(float(i), 0, 1, si) for i in range(si) ]
    z = [ easeOutQuad(float(i), 0, 1, si) for i in reversed(range(si)) ]

    freqs = tune.fromdegrees([1,2,3,4,5,6,7,8], root=root, octave=dsp.randint(loctave, hoctave), ratios=ratios, scale=quality)
    freqs = freqs[:dsp.randint(1, len(freqs))]
    if dsp.rand() > 0.5:
        freqs = [ f for f in reversed(freqs) ]
    freqs = dsp.rotate(freqs, dsp.randint(0, len(freqs)))

    y = y + z

    y = [ dsp.mstf(v * beat) + dsp.mstf(2) for v in y ]

    x = range(len(y))

    def make(length, freq):
        freq *= dsp.rand(1 - (bendfactor / 2.0), 1 + (bendfactor / 2.0))
        out = keys.chippy(length=int(length*dsp.rand(0.01, 0.4)), freq=freq, amp=0.7)
        out = dsp.env(out, 'phasor')
        out = dsp.pad(out, 0, length - dsp.flen(out))
        return out

    out = [ make(v, freqs[i % len(freqs)]) for i,v in enumerate(y) ]
    out = ''.join(out)

    out = dsp.pan(out, dsp.rand(0,1))

    return out
