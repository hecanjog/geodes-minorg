from pippi import dsp
from pippi import tune
import math
from pippic.settings import config
from pippic.settings import get_param as P
import json

shortname   = 'dr'
name        = 'drone'
loop        = True

def play(voice_id):
    bpm = config('bpm')
    beat = dsp.bpm2frames(bpm)
    dsl = P(voice_id, 'drum', 'h.c')

    length = int(P(voice_id, 'length', dsp.stf(dsp.rand(5, 12))))
    volume = P(voice_id, 'volume', 80.0) 
    volume = volume / 100.0 # TODO move into param filter

    octave = P(voice_id, 'octave', 3)
    notes = P(voice_id, 'note', '["%s"]' % config('key'))
    notes = json.loads(notes)
    
    hertz = P(voice_id, 'hertz', False)
    alias = P(voice_id, 'alias', False)
    bend = P(voice_id, 'bend', False)
    env = P(voice_id, 'envelope', 'gauss')
    harmonics = P(voice_id, 'harmonic', '[1,2,3,4]')
    harmonics = json.loads(harmonics)
    reps      = P(voice_id, 'repeats', 1)
    waveform = P(voice_id, 'waveform', 'tri')

    quality = getattr(tune, config('quality')) 
    ratios = getattr(tune, config('tune')) 

    glitch = False
    root = 27.5
    pinecone = False
    bbend = False
    wild = False

    if bbend == True:
        bend = True

    tune.a0 = float(root)

    # These are amplitude envelopes for each partial,
    # randomly selected for each. Not to be confused with 
    # the master 'env' param which is the amplit
    wtypes = ['sine', 'phasor', 'line', 'saw']    
    layers = []

    if hertz is not False:
        notes = hertz

    for note in notes:
        tones = []
        for i in range(dsp.randint(2,4)):
            if hertz is not False:
                freq = float(note)

                if octave > 1:
                    freq *= octave
            else:
                freq = tune.ntf(note, octave)

            snds = [ dsp.tone(length, freq * h, waveform, 0.05) for h in harmonics ]
            snds = [ dsp.env(s, dsp.randchoose(wtypes), highval=dsp.rand(0.3, 0.6)) for s in snds ]
            snds = [ dsp.pan(s, dsp.rand()) for s in snds ]

            if bend is not False:
                def bendit(out=''):
                    if bbend == True:
                        bendtable = dsp.randchoose(['impulse', 'sine', 'line', 'phasor', 'cos', 'impulse'])
                        lowbend = dsp.rand(0.8, 0.99)
                        highbend = dsp.rand(1.0, 1.25)
                    else:
                        bendtable = 'sine'
                        lowbend = 0.99
#                        lowbend = 0.75
                        highbend = 1.01
#                        highbend = 1.5

                    out = dsp.split(out, 441)

                    freqs = dsp.wavetable(bendtable, len(out))

                    freqs = [ math.fabs(f) * (highbend - lowbend) + lowbend for f in freqs ]

                    out = [ dsp.transpose(out[i], freqs[i]) for i in range(len(out)) ]
                    return ''.join(out)

                snds = [ bendit(snd) for snd in snds ]

            tones += [ dsp.mix(snds) ]

        layer = dsp.mix(tones)

        if wild != False:
            layer = dsp.vsplit(layer, 41, 4410)
            layer = [ dsp.amp(dsp.amp(l, dsp.rand(10, 20)), 0.5) for l in layer ]
            layer = ''.join(layer)
        
        if pinecone != False:
            layer = dsp.pine(layer, length, freq, 4)

        layer = dsp.env(layer, env)

        layers += [ layer ]

    out = dsp.mix(layers) * reps

    return dsp.amp(out, volume)


