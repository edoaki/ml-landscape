"""Plot the bundled score's PCM waveform and measured short-time spectrum.

Run with the project's Python (NumPy + Matplotlib). Not required for HTML builds.
"""
from pathlib import Path
import wave
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[1] / 'assets'

def build():
    available = {f.name for f in font_manager.fontManager.ttflist}
    fonts = [n for n in ['Hiragino Sans', 'Noto Sans CJK JP', 'DejaVu Sans'] if n in available]
    plt.rcParams.update({'font.family': fonts,
                         'font.size': 12, 'axes.spines.top': False, 'axes.spines.right': False,
                         'figure.facecolor': '#fcfcf8', 'axes.facecolor': '#fcfcf8',
                         'text.color': '#243b30', 'axes.labelcolor': '#243b30',
                         'svg.fonttype': 'path'})
    with wave.open(str(ROOT / 'audio-score-mix.wav')) as f:
        rate = f.getframerate()
        signal = np.frombuffer(f.readframes(f.getnframes()), dtype='<i2') / 32768.
    times = np.arange(len(signal))/rate
    fig, axes = plt.subplots(2, 1, figsize=(10, 5.8), layout='constrained')
    axes[0].plot(times, signal, lw=.55, color='#4d7897', rasterized=True)
    axes[0].set(xlim=(0,8), ylim=(-.65,.65), ylabel='振幅', xlabel='時間（秒）',
                title='① 波形：8秒の曲を、時間ごとの振幅で表す')
    mask = (times >= 1.02) & (times <= 1.06)
    axes[1].plot(times[mask], signal[mask], color='#4d7897', lw=1.4)
    axes[1].scatter(times[mask][::8], signal[mask][::8], s=10, color='#4d7897')
    axes[1].set(xlim=(1.02,1.06), ylim=(-.65,.65), ylabel='振幅', xlabel='時間（秒）',
                title='一部を拡大：1.02〜1.06秒（40ミリ秒）')
    for ax in axes:
        ax.axhline(0, color='#657568', lw=.5)
        ax.grid(alpha=.18)
    fig.savefig(ROOT/'audio-waveform.png', dpi=180)
    plt.close(fig)

    # Hann window: 1024 samples (64 ms), hop: 128 samples (8 ms).
    size, hop = 1024, 128
    frames = np.lib.stride_tricks.sliding_window_view(signal, size)[::hop]
    power = abs(np.fft.rfft(frames * np.hanning(size), axis=1))**2
    db = 10*np.log10(np.maximum(power / power.max(), 1e-6))
    frequency = np.fft.rfftfreq(size, 1/rate)
    centers = (np.arange(len(frames))*hop + size/2)/rate
    fig, ax = plt.subplots(figsize=(10, 4.5), layout='constrained')
    mesh = ax.pcolormesh(centers, frequency, db.T, shading='auto', cmap='magma', vmin=-60, vmax=0, rasterized=True)
    ax.set(xlim=(0,8), ylim=(0,1200), xlabel='時間（秒）', ylabel='周波数（Hz）',
           title='② スペクトログラム：同じ8秒の曲を、周波数成分の強さで表す')
    ax.set_yticks([0,200,400,600,800,1000,1200])
    bar = fig.colorbar(mesh, ax=ax, pad=.025, ticks=[-60,-40,-20,0])
    bar.set_label('相対的な強さ（dB）  暗い：弱い ／ 明るい：強い')
    fig.savefig(ROOT/'audio-spectrogram.png', dpi=180)
    plt.close(fig)

if __name__ == '__main__':
    build()
