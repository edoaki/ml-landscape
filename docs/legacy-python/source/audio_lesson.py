"""Audio tasks explained through playable input/output examples."""
from common import *

def player(file, label):
    return f'<audio controls preload="none" aria-label="{label}" src="assets/{file}">音声を再生できません。<a href="assets/{file}">音声ファイルを開く</a></audio>'

def sample(title, description, file):
    return '<div class="audio-sample"><h3>'+title+'</h3>'+ (p(description) if description else '') +player(file,title)+'</div>'

def body():
    out=sec('tasks','音から何を取り出し、何を作るか',p('音声・音楽の研究には、言葉の認識、音の生成、音源の分離などがあります。')+table(['タスク','入力 → 出力','身近な用途'],[
        ('<a href="#asr">音声認識（ASR）</a>','話し声 → 文字列','会議の文字起こし・字幕'),
        ('<a href="#tts">音声合成（TTS）</a>','文章 → 話し声','案内の読み上げ'),
        ('<a href="#music">音楽生成</a>','曲の説明・旋律 → 音楽','映像に合うBGM'),
        ('<a href="#listen">音源分離</a>','混ざった音 → 音源ごとの波形','歌声と伴奏を取り出す')]))
    out+=sec('asr','音声認識：話し声を文字にする',p('音声認識（ASR）は、話された言葉を文字にします。会議の文字起こしや字幕に使われます。')+'<div class="compare">'+sample('入力：短い案内','','audio-tts-normal.wav')+'<div class="audio-sample"><h3>対応する文章（例）</h3><p class="audio-transcript">明日の会議は、午後三時からです。</p></div></div>'+p('Whisperなどが代表例です。雑音の中でも正確に聞き取ることや、多言語への対応が研究されています。')+p(ref('https://openai.com/index/whisper/','Whisperの研究紹介・公開例')))
    out+=sec('tts','音声合成：文章から自然な話し声を作る',
        p('音声合成（TTS）は、文章から話し声を作ります。発音だけでなく、抑揚や間の取り方も自然にすることが研究されています。Tacotron 2の合成音声と、同じ文章を人が読んだ録音の例です。')
        +p('入力：George Washington was the first President of the United States.<br>（ジョージ・ワシントンはアメリカ合衆国の初代大統領でした。）')
        +'<div class="compare">'+sample('合成音声：Tacotron 2','','audio-tacotron2-generated.wav')+sample('人の音声：録音','','audio-tacotron2-human.wav')+'</div>'
        +p('出典：'+ref('https://google.github.io/tacotron/publications/tacotron2/','Tacotron 2 著者公開サンプル')))
    out+=sec('music','音楽生成：曲の説明から、音楽を作る',p('音楽生成は、楽器や雰囲気の説明から曲を作ります。以下はMusicGenの生成例です。')+'<div class="compare">'+sample('① ダンス系の曲','指示（要約）：南国風の打楽器と、覚えやすい旋律を持つ明るいダンスポップ。','audio-musicgen-dance.mp3')+sample('② オーケストラの曲','指示（要約）：力強い打楽器、金管と弦楽器を使った、英雄的な戦いを思わせる壮大な曲。','audio-musicgen-orchestra.mp3')+'</div>'+p('指示に合う曲を作ることや、長い曲の展開を自然につなぐことが研究されています。')+p('出典：'+ref('https://ai.honu.io/papers/musicgen/','MusicGen著者試聴ページ')))
    out+=sec('listen','音源分離：混ざった曲から、一つの音を取り出す',p('音源分離は、混ざった音から歌声や楽器を取り出します。下のデモは、曲全体・旋律・伴奏の対応を示しています。')+img('audio-score.svg','8秒の旋律と伴奏。旋律は上下し、伴奏は低い位置で反復する。','旋律と伴奏の音の配置。')+'<div class="audio-switch" data-audio-switch><p><strong>聞き比べ：</strong>再生中に切り替えると、同じ位置から別の音を聞けます。</p><div class="audio-options" role="group" aria-label="聞く音を選ぶ"><button type="button" data-track="mix" aria-pressed="true">曲全体</button><button type="button" data-track="melody" aria-pressed="false">旋律だけ</button><button type="button" data-track="backing" aria-pressed="false">伴奏だけ</button></div>'+player('audio-score-mix.wav','切り替え試聴：曲全体')+'<p class="audio-status" role="status">曲全体：旋律と伴奏が重なっています。</p></div><noscript><p>旋律と伴奏を個別に聞けます。</p>'+player('audio-score-melody.wav','旋律だけ')+player('audio-score-backing.wav','伴奏だけ')+'</noscript>'+p('分離の目標を聞くデモ：混合前の旋律・伴奏を切り替えています。')+p('Demucsなどは、重なった歌声や楽器を推定して分けます。他の音の混入や、取り出した音の欠けを減らすことが研究されています。')+p(ref('https://ai.honu.io/papers/demucs/','Demucsの実際の分離結果を聞く（著者公開デモ）')))
    out+=sec('representation','波形とスペクトログラム：音をどう数値にするか',
        p('音声認識や音源分離のモデルは、音を数値として扱います。その代表的な表し方が波形とスペクトログラムです。下の図は、同じ8秒の曲をそれぞれの形式で表したものです。')
        +player('audio-score-mix.wav','波形・スペクトログラムと対応する8秒の曲')
        +sub('波形',
            p('音を時間ごとの振幅で表したものです。音が強く出るタイミングや、振動の様子が分かります。')
            +img('audio-waveform.png','上は8秒の混合曲の波形。下は1.02秒から1.06秒の振動を拡大。横軸は時間、縦軸は振幅。','上：曲全体の波形。下：40ミリ秒の拡大。'))
        +sub('スペクトログラム',
            p('音を短く区切って周波数成分を調べ、強さを色で表します。横は時間、縦は周波数で、明るいほどその成分が強いことを示します。')
            +img('audio-spectrogram.png','同じ8秒の曲のスペクトログラム。下部に低い伴奏、中央に上下する旋律、その上に倍音が見える。','同じ曲から計算。低い位置に伴奏、中央に上下する旋律、その上に倍音が見える。')
            +p('波形では重なって見える音も、周波数ごとに分けると高さや音色の特徴を捉えやすくなります。そのため、音声認識や音源分離などのモデルへの入力に使われます。')))
    out+=refs([('短時間フーリエ変換とスペクトログラム（SciPy公式資料）','https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.ShortTimeFFT.html'),('Tacotron 2 原論文','https://arxiv.org/abs/1712.05884'),('Whisper 原論文','https://arxiv.org/abs/2212.04356'),('MusicGen 原論文','https://arxiv.org/abs/2306.05284'),('Demucs 著者実装','https://github.com/facebookresearch/demucs')])
    return out+'<script src="assets/audio.js" defer></script>'
