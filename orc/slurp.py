from pippi import dsp
from pippic.settings import config
from pippic.settings import get_param as P
import json

shortname       = 'sl'
name            = 'slurp'
loop            = True

def play(voice_id):
    volume = P(voice_id, 'volume', 100.0)
    volume = volume / 100.0 # TODO: move into param filter
    volume = volume * 0.65
    length = P(voice_id, 'length', 40)
    env    = False
    wii    = False
#    wii    = True

    speed  = False
    
    numcycles = dsp.randint(1, 200)

    # Make breakpoint env with 2-10 vals between 0.1 and 1.0
    curve_a = dsp.breakpoint([1.0] + [dsp.rand(0.1, 1.0) for r in range(dsp.randint(2, 10))] + [0], numcycles)

    # Make wavetable with single cycle from given wave types
    curve_types = ['vary', 'phasor', 'sine', 'cos', 'impulse']
    curve_b = dsp.wavetable(dsp.randchoose(curve_types), numcycles)

    # Make pan curve - always cosine
    pan = dsp.breakpoint([ dsp.rand() for i in range(dsp.randint(5, 50)) ], numcycles)
    amps = dsp.breakpoint([ dsp.rand(0.1, 0.75) for i in range(dsp.randint(5, 30)) ], numcycles)

    # Multiply breakpoint curve with simple wavetable
    wtable = [ curve_a[i] * curve_b[i] for i in range(numcycles) ]

    # Scale to max frequency
    wtable = [ (f * 20000) + length for f in wtable ]

    # Possible osc wavetypes
    wtypes = ['sine2pi']
#    wtypes = ['tri', 'sine2pi', 'impulse']
#    wtypes = ['impulse', 'tri', 'cos', 'sine2pi', 'vary']

    if wii is True:
        out = [ dsp.pan(dsp.cycle(wtable[i], dsp.randchoose(wtypes)), pan[i]) for i in range(numcycles) ]
    else:
        wtype = dsp.randchoose(wtypes)
        out = [ dsp.pan(dsp.cycle(wtable[i], wtype), pan[i]) for i in range(numcycles) ]

    out = [ dsp.amp(oo, amps[i]) for i, oo in enumerate(out) ]

    out = dsp.amp(''.join(out), volume)

    if speed != False and speed > 0.0:
        out = dsp.transpose(out, speed)

    if env != False:
        out = dsp.env(out, env)

    return out

