"""
highorder function example : sound encoding and play
"""

from wave import open
from struct import Struct
from math import floor

frame_rate = 11025

def encode(x):
    """
    Encode float x between -1 and 1 as two bytes.
    """
    i = int(16384 * x)
    return Struct('h').pack(i)

def play(sampler, name='song.wav', seconds=2):
    """
    Write the output of a sampler function as a wav file.
    """
    out = open(name, 'wb')
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(frame_rate)
    t = 0
    while t < seconds * frame_rate:
        sample = sampler(t)
        out.writeframes(encode(sample))
        t += 1
    out.close()

def tri(frequency, amplitude=0.3):
    """
    A continuous triangle wave.
    """
    period = frame_rate // frequency
    def sampler(t):
        saw_wave = t / period - floor(t / period + 0.5)
        tri_wave = 2 * abs(2 * saw_wave) - 1
        return amplitude * tri_wave
    return sampler

#1. 두가지 이상의 코드를 같이 연주하고 싶다
def both(f,g):
    return lambda t: f(t) + g(t)

#2. 전체 시간을 나누어 각각의 코드를 연주하고 싶다 : 노트의 구현
def note(f, start, end, fade=0.01):
    def sampler(t):
        seconds = t / frame_rate
        if seconds < start or seconds > end:
            return 0
        elif seconds < start + fade: # start 시작지점 0.01초 지났을때
            return (seconds - start) / fade * f(t)
        elif seconds > end - fade: # end 종료지점 0.01초 남았을때
            return (end - seconds) / fade * f(t)
        else:
            return f(t)
    return sampler

#3. mario theme 만들기
def mario(c, e, g, low_g):
    z = 0
    song = note(e, z, z + 1 / 8)
    z += 1 / 8
    song = both(song, note(e, z, z + 1 / 8))
    z += 1 / 4
    song = both(song, note(e, z, z + 1 / 8))
    z += 1 / 4
    song = both(song, note(c, z, z + 1 / 8))
    z += 1 / 8
    song = both(song, note(e, z, z + 1 / 8))
    z += 1 / 4
    song = both(song, note(g, z, z + 1 / 4))
    z += 1 / 2
    song = both(song, note(low_g, z, z + 1 / 4))
    z += 1 / 2
    return song

def mario_at(octave):
    c, e = tri(octave * c_freq), tri(octave * e_freq)
    g, low_g = tri(octave * g_freq), tri(octave * g_freq / 2)
    return mario(c, e, g, low_g)


if __name__ == "__main__":
    c_freq = 261.63 # C code
    e_freq = 329.63 # E code
    g_freq = 392.00 # G code

    c, e = tri(c_freq), tri(e_freq) # C와 E 코드를 트라이앵글 웨이브로

    # Step 1: 두가지 이상의 코드를 동시에 연주하기
    play(both(c, e), name="both_song.wav")
    # play(tri(c_freq) + tri(e_freq)) # 그냥 더하기가 될리가 없다. 함수 tri에서 + 가 정의되지 않았기 때문에

    # Step 2: Note 구현하기 - C코드, E코드 순서대로 연주하기
    play(both(note(c, 0, 1/4), note(e, 1/2, 1)), name="note_song.wav")

    # Step 3: Mario Intro Theme 만들기 - Octave 구현 + 연속적인 song 만들기
    g, low_g = tri(g_freq), tri(g_freq / 2)
    play(mario_at(1), name="mario_original.wav")
    play(mario_at(1/2), name="mario_half_down.wav")
    play(both(mario_at(1), mario_at(1 / 2)), name="mario_mix.wav")
