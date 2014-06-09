from pippi import dsp
from pippi import tune
from pippic.settings import config

from hcj import keys

shortname   = 'pa'
name        = 'pattern'
device = 'default'

def play(voice_id):
    bpm = config('bpm')
    beat = dsp.bpm2frames(bpm)

    root = 'bb'
    amp = dsp.rand(0.4, 0.85)

    nlens = [
        beat * 4,
        beat * 3,
        beat * 2, 
        beat + (beat / 2),
        beat, 
        beat / 2,
        beat / 4,
    ]

    scale = [2,4,6,9]
    scale = [1,4,6,8]
#    scale = [1,3,4,5,6,8,9]
#    scale = [1,2,3,5,6,8,9]
#    scale = [1,5,8]
    freqs = tune.fromdegrees(scale, root=root, octave=dsp.randint(2,4), ratios=tune.terry)

    # length of pattern (in beats)
    elen = 0
    tlen = beat * dsp.randint(2, 8)

    # beat lengths (from a set of bpm-derived note lengths defined in the nlens list)
    blens = []
    while elen < tlen:
        l = dsp.randchoose(nlens)
        blens += [ l ]
        elen += l

    # beat pulsewidths
    bpws = [ dsp.rand(0.1, 1) for pw in range(len(blens)) ]

    out = ''

    # choose a pitch from the scale
    freq = dsp.randchoose(freqs)
 
    # synthesize the tones
    for i in range(len(blens)):
        # find the length of the pulse
        blen = int(round(blens[i] * bpws[i]))

        # find the length of the rest
        brest = blens[i] - blen

        # make a rhodes tone with a random amplitude
        #beat = keys.rhodes(length=blen, freq=freq, amp=dsp.rand(0.3, 0.5))
        beat = keys.rhodes(length=blen, freq=freq, amp=amp)

        # pan the tone to a random position
        beat = dsp.pan(beat, dsp.rand())

        # bitcrush the tone a random amount
#        beat = dsp.alias(beat)

        # pad the tone with silence
        beat = dsp.pad(beat, 0, brest)

        # add it to the output
        out += beat

    out *= dsp.randint(1, 2)

    if dsp.rand() > 0.75:
        out = dsp.split(out, dsp.bpm2frames(bpm) / dsp.randchoose([1,2,4]))
        out = dsp.randshuffle(out)
        out = ''.join(out)

    return out
