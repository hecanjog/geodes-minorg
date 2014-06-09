""" Requires sox and text2wave (via festival)
"""

from pippi import dsp
from pippi import tune
import subprocess
import os

shortname = 'si'
name = 'sing'

def sox(cmd, sound):
    path = os.getcwd()
    filename_in = '/proc-in'
    filename_out = '/proc-out.wav'

    dsp.write(sound, filename_in)

    cmd = cmd % (path + filename_in + '.wav', path + filename_out)
    subprocess.call(cmd, shell=True)

    sound = dsp.read(path + filename_out).data

    return sound

def text2wave(lyrics):
    path = os.getcwd() + '/bag.wav'
    cmd = "echo '%s' | /usr/bin/text2wave -o %s" % (lyrics, path)

    ret = subprocess.call(cmd, shell=True)

    words = dsp.read('bag.wav').data

    return words

def singit(lyrics, mult):
    words = text2wave(lyrics)

    pitches = [ dsp.randint(1, 9) for i in range(dsp.randint(2, 4)) ]
    pitches = tune.fromdegrees(pitches, octave=dsp.randint(1, 4), root='c')

    return words

    sings = [ dsp.pine(words, dsp.flen(words) * mult, pitch) for pitch in pitches ]
    sings = dsp.mix(sings)

#    sings = sox("sox %s %s tempo 1.0", sings)

    return sings

def play(voice_id):
    lyric = 'om is the bow, the arrow is the soul'

    out = singit(lyric, dsp.randint(5, 10))

    return out

