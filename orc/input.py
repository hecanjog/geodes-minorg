from pippi import dsp
from pippic import rt

shortname   = 'in'
name        = 'input'

def play(voice_id):
    out = rt.capture(dsp.mstf(2000))
    dsp.write(out, 'sounds/input')

    return ''
