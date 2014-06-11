from pippi import dsp
from pippi import tune
from pippic.settings import config
from pippic.settings import get_param as P
import json

from hcj import drums

shortname   = 'cl'
name        = 'clap'

c1 = dsp.read('sounds/clap1.wav').data
c2 = dsp.read('sounds/clap2.wav').data
tape1 = dsp.read('sounds/tape1.wav').data

def play(voice_id):
    bpm = config('bpm')
    beat = dsp.bpm2frames(bpm)
    dsl = P(voice_id, 'drum', '["c","k","h"]')
    dsp.log(dsl)
    dsl = json.loads(dsl)

    def hat(beat):
        length = beat * 4
        nbeats = 16
        blen = length / nbeats

        out = ''

        for b in range(nbeats):
            h = dsp.transpose(tape1, 9)
            h = dsp.fill(h, dsp.mstf(dsp.rand(1, 20)))
            h = dsp.env(h, 'phasor')
            h = dsp.amp(h, dsp.rand(0, 0.8))
            h = dsp.pad(h, 0, blen - dsp.flen(h))

            out += h

        out *= 8

        return out

    def kick(beat):
        out = drums.sinekick(length=beat, amp=dsp.rand(0.8, 1))
        out = dsp.pad(out, 0, beat * dsp.randint(1, 2))
        out *= 2
        return out

    def clap1(beat):
        c = dsp.read('sounds/mikeclap.wav').data
        c = dsp.transpose(c, dsp.rand(1, 2.5))
        c = dsp.fill(c, dsp.mstf(dsp.rand(10, 100)))
        c = dsp.env(c, 'phasor')
        c = dsp.amp(c, dsp.rand(1, 3))
        c = dsp.pad(c, 0, beat - dsp.flen(c))

        blen = beat / dsp.randchoose([1,2])
        c = dsp.pad(c, blen, 0)

        c *= 4

        return c

    def clap2(beat):
        nlens = [
            beat * 2,
            beat,
            beat / 2,
        ]

        # length of pattern (in beats)
        nbeats = dsp.randint(10, 15)

        # beat lengths (from a set of bpm-derived note lengths defined in the nlens list)
        blens = [ dsp.randchoose(nlens) for b in range(nbeats) ]

        out = ''
     
        # synthesize the tones
        for i in range(nbeats):
            beat = dsp.transpose(dsp.randchoose([c1,c2]), dsp.rand(0.25, 40.0))
            beat = dsp.pad(beat, 0, blens[i] - dsp.flen(beat))
            beat = dsp.amp(beat, dsp.rand(1, 4))

            # add it to the output
            out += beat

        return out

    all = []

    if 'c' in dsl:
        clapper = dsp.randchoose([clap1,clap2])
        all += [ clapper(beat) ]

    if 'k' in dsl:
        all += [ kick(beat) ]

    if 'h' in dsl:
        all += [ hat(beat) ]

    out = dsp.mix(all)

#    out = dsp.vsplit(out, dsp.mstf(dsp.rand(8, 140)), dsp.mstf(500))
#    out = dsp.randshuffle(out)
#    out = ''.join(out)

    out = dsp.vsplit(out, 10, 1000)
    out = [ dsp.amp(o, dsp.rand(0, 4)) for o in out ]
    out = [ dsp.env(o, 'random') for o in out ]
    out = [ dsp.transpose(o, dsp.rand(0.25, 1)) for o in out ]
    out = dsp.randshuffle(out)
    out = ''.join(out)

    out = dsp.pine(out, int(dsp.flen(out) * dsp.rand(1.5, 4)), dsp.rand(10, 2000), dsp.randint(0, 2), dsp.rand(1, 3), dsp.randint(0, 2), dsp.rand(1, 3)) 
    out = dsp.amp(out, 0.65)

    glass = dsp.read('sounds/s/glass2.wav').data

    glass = dsp.vsplit(glass, dsp.mstf(1), dsp.mstf(100))
    glass = dsp.randshuffle(glass)
#    glass = [ dsp.pad(g, 0, dsp.randint(10, 1000)) for g in glass ]
#    glass = [ dsp.transpose(g, dsp.rand(0.5, 1.5)) * dsp.randint(1, 3) for g in glass ]
    glass = ''.join(glass)

    glass = dsp.fill(glass, dsp.flen(out))

    out = dsp.mix([ out, glass ])

    return out
