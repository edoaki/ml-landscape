"""Reproduce the original eight-second teaching score; no learned model used."""
import math
import struct
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'assets'
RATE = 16000
NOTES = [60, 64, 67, 64, 62, 65, 69, 67, 64, 67, 72, 71, 69, 67, 64, 60]

def build():
    stems = [[], []]
    for i in range(RATE * 8):
        t = i / RATE
        beat = min(int(t * 2), 15)
        u = t % .5
        freq = 440 * 2 ** ((NOTES[beat] - 69) / 12)
        env = min(u / .015, 1) * max(0, 1 - u / .48)
        stems[0].append(.27 * env * (math.sin(2*math.pi*freq*t) + .25*math.sin(4*math.pi*freq*t)))
        bass = 130.8128 if t < 4 else 97.9989
        pulse = math.exp(-u * 12)
        stems[1].append(.22 * pulse * math.sin(2*math.pi*bass*t) + .1 * math.exp(-u*35)*math.sin(2*math.pi*55*t))
    for name, values in [('melody', stems[0]), ('backing', stems[1]), ('mix', [a+b for a,b in zip(*stems)])]:
        with wave.open(str(ROOT / f'audio-score-{name}.wav'), 'wb') as f:
            f.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
            f.writeframes(struct.pack('<'+'h'*len(values), *(round(v*32767) for v in values)))
    # Note chart: explicitly a score, not a model-estimated spectrogram.
    b='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 230" role="img" aria-label="8秒の旋律と伴奏の楽譜を横長の棒で表示">'
    b+='<rect width="760" height="230" fill="#fcfcf8"/>'
    for x in range(9):
        b+=f'<path d="M{95+x*78} 30v150" stroke="#dfe5da"/><text x="{95+x*78}" y="210" text-anchor="middle" font-size="13">{x}秒</text>'
    b+='<text x="12" y="70" font-size="15">旋律</text><text x="12" y="163" font-size="15">伴奏</text>'
    for i,n in enumerate(NOTES):
        b+=f'<rect x="{95+i*39}" y="{110-(n-60)*5}" width="35" height="8" rx="3" fill="#4d7897"/>'
        b+=f'<rect x="{95+i*39}" y="{150 if i<8 else 164}" width="28" height="8" rx="3" fill="#ba7147"/>'
    b+='<text x="380" y="24" text-anchor="middle" font-size="14">横：時間 ／ 棒の高さ：音の高さ</text></svg>'
    (ROOT/'audio-score.svg').write_text(b)

if __name__ == '__main__':
    build()
