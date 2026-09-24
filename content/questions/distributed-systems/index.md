---
id: distributed-systems
title: 分散学習・推論実行
summary: データを分けるか、モデルを分けるか。複数GPUへの仕事の分担と、通信・待ち時間の関係を図で見る。
url: questions/distributed-systems.html
status: ready
scope: 大きな学習・推論をどう実行するか。計算の分担、通信、メモリ、遅延・処理量
prerequisites:
- fundamentals
related: []
origins:
- efficiency.html#systems
styles:
- content/questions/distributed-systems/components/tables.css
english_title: Distributed Training and Inference
---

## 複数GPUで、仕事とメモリを分担する {#distributed-example}

**分散学習**は、一つのモデルの学習を複数の計算装置で分担する方法です。計算を速くする、または一台のメモリに収まらないモデルを動かすために使います。ここでは、製品写真から傷を判定するモデルをGPU（大量の数値計算を並行して行う装置）で学ぶ例を考えます。

## データ並列：同じモデルで、別々の写真を学ぶ {#data-parallel-example}

{{component:data-parallel}}

**勾配**は、予測の誤差を減らすために重みをどちらへ動かすかの手がかりです。各GPUが別の写真から求めた勾配を平均し、同じ規則で更新することで、全GPUが同じモデルを保ちます。これが同期データ並列です。[公式解説](source:exp-ddp)

## モデル並列：モデルの計算を分ける {#model-parallel-example}

{{component:model-parallel}}

データ並列では各GPUにモデル全体を置きます。一台に収まらない場合は、層や層内の計算を分けます。パイプライン並列は複数の入力を重ねて処理し、テンソル並列は一つの層を複数GPUで計算します。[パイプライン並列](source:pipeline)・[テンソル並列](source:inference)

**メモリには重み以外も必要です。** 学習では勾配、更新用の記録、計算途中の出力も保存します。FSDPなどは重み・勾配・更新用の記録を分割保存し、必要な重みを計算時に集めます。保存量を減らす代わりに通信が増えます。[FSDPの解説](source:fsdp)

## 台数を増やしても、そのまま速くはならない {#systems}

{{component:communication}}

勾配や中間出力の通信、遅いGPUを待つ時間が加わります。速くするには、計算中に通信を進める、仕事の偏りを減らす、といった工夫も必要です。比較ではモデルと一回の更新に使う写真数をそろえます。

## 推論：多数の依頼を同時に処理する {#latency-throughput}

{{component:inference}}

推論は、学習済みの重みで新しい入力に答える処理です。写真をまとめて計算すると処理量が増える場合がありますが、写真が集まるのを待つと一件の遅延は増えます。**一件を早く返すことと、多数に答えることは別の目標**です。

文章生成では、最初のトークン（単語やその一部）が出るまでと、その後の生成間隔も分けて測ります。過去の計算結果を保存する**KVキャッシュ**は再計算を減らしますが、文章が長いほど、同時に扱う依頼が多いほどメモリを使います。
