---
layout: post
title: "Attention의 Q, K, V"
description: >
  Attention 공부 중 Q, K, V에 대한 고찰
sitemap: false
hide_last_modified: true
---

0. Table of Contents
{:toc}


# 개요

NLP분야에서 자주 나오는 문제 중 하나를 푸는 방법으로, BERT를 활용한 문장 분류, 개체명 인식 등이 있음. 그래서 BERT와 self-attention에 대해서 공부하고 있는데, attention의 Q, K, V 중 Key와 Value값이 다를 수도 있다는 말이 이해가 가지 않아서 서치 + 생각해보았다.

결론적으로, Key와 Value값은 다를 수 있다. attention 메커니즘을 트랜스포머에만 적용하려고 생각하니 이런 헷갈리는 상황이 발생한 것 같은데, 다른 예시를 생각해보면 Key와 Value값은 다를 수도 있어 보인다(정말 딱 맞는 예시는 아니지만). 조금 더 일반화한다면 Key와 Value가 다를 수 있다는 말의 의미를 이해할 수 있을 것 같다.


# 배경 지식


## Attention 개요

<p align="center">
  <img width="500" src="/assets/img/myown/qkv.jpg">
</p>

Attention 메커니즘의 개요
{:.figcaption}

Query, Key, Value를 활용해서 하나의 지표를 제공해 주는 메커니즘이다. 가장 처음에는 RNN 기반의 번역 모델에서 활용되었다. 원 문장의 토큰을 차례대로 RNN 셀에 넣으면서 컨텍스트 벡터를 만드는데, 이 컨텍스트 벡터가 이전의 단어들에 대한 정보를 조금 잊어먹은 상태로 나오게 되어 버린다. 긴 문장일 수록 이런 경향이 심하고, 그래서 번역 문장에서 토큰을 생성할 때마다 attention 메커니즘을 활용해서 원 문장의 단어 중 가장 유의한 단어를 찾아 정보를 더한다.

![encoder-decoder](/assets/img/myown/encoder-decoder.png){:.lead loadings="lazy"}

RNN 기반 encoder-decoder 구조
{:.figcaption}


## Attention 과정

디코더의 각 셀에서 번역 단어를 계산할 때, 그 셀의 은닉 상태와 모든 인코더 셀과의 관계를 계산하여 지표를 내놓고, 이걸 은닉 상태와 결합해서 output을 내놓는다. 주로 dot-product attention이 사용된다. attention 과정은 다음과 같이 요약할 수 있다.

![encoder-decoder-attention-added](/assets/img/myown/encoder-decoder-attention-added.png){:.lead loadings="lazy"}

RNN 기반 encoder-decoder 구조에서 attention의 사용 개요
{:.figcaption}

1. "디코더 셀의 은닉 벡터(Query)"와 "모든 인코더 셀의 은닉 벡터들(Key)"간의 내적 계산
2. 내적값에 대한 softmax 분포 계산
3. softmax 분포를 가중치로 한 "모든 인코더 셀의 은닉 벡터들(Value)"의 "가중합 벡터(Attention Value)" 계산
4. "디코더 셀의 은닉 벡터"와 "가중합 벡터(Attention Value)"를 concat하고 FCN에 input하여, 나오는 output을 단어 벡터로 활용


## Attention과 Self-attention

Attention 메커니즘은 이후에 독립적으로 사용되어 언어 모델을 구성하게 되는데 그게 transformer이고, 이 transformer의 encoder 구조를 쌓아서 만든 게 BERT다. transformer는 self-attention이라는 메커니즘으로 attention 메커니즘을 개조해서 활용한다.

| METHOD | Attention                          | Self-attention |
|:------:|:----------------------------------:|:-----------------:|
| Query  | t 시점의 _디코더_ 셀의 은닉 상태 벡터     | t 시점의 _인코더_ 셀의 은닉 상태 벡터 |
| Key    | 모든 시점의 인코더 셀의 은닉 상태 벡터들 | 모든 시점의 인코더 셀의 은닉 상태 벡터들  |
| Value  | 모든 시점의 인코더 셀의 은닉 상태 벡터들 | 모든 시점의 인코더 셀의 은닉 상태 벡터들  |

Attention과 self-attention의 차이
{:.figcaption}


# 본문

Attention과 self-attention의 차이는 query를 디코더 셀의 것을 쓰느냐, 인코더 셀의 것을 쓰느냐의 차이다. 깊이 들어가면 조금 더 복잡하긴 하지만 이번에 다룰 내용은 그게 아니기도 하고, attention과 관련해서는 [딥 러닝을 이용한 자연어 처리 입문](https://wikidocs.net/31379) 이라는 페이지에서 훨씬 더 자세하게 정리되어 있음.(감사합니다!)

그런데, 여기까지 이해하고 궁금한 게 생겼다. Key랑 Value는 Attention이든, self-attention이든 인코더 셀의 은닉 상태를 활용하니까, 항상 같은 값이다. 그럼 왜 굳이 Attention에서 K랑 V를 구분해 놓은 걸까? Attention의 적용 예시를 찾아봐도 RNN이나 트랜스포머 외의 사용처는 찾지 못했고, RNN 기반 언어 모델과 트랜스포머에서는 모두 Key와 Value를 같은 값을 쓴다.

궁금증에 대한 나의 답은, attention을 좀더 일반화하면 보인다는 거다.

언어 모델에서 attention의 사용 목적은 다음과 같다. (내적을 표준화하면 코사인 유사도이므로, 비슷한 맥락으로 이해함.)

1. 특정 시점의 디코더 셀의 토큰 벡터를 단어 벡터로 변환할 것이다.
2. 변환할 때, 디코더 셀 토큰 벡터와 모든 인코더 셀의 토큰 벡터와의 내적(유사도)을 계산하고, 가장 내적값이 큰 인코더 셀 토큰을 더 많이 반영해서 단어 벡터 변환에 활용할 것이다.

가장 문맥적으로 비슷한 단어를 많이 반영해서 번역하기 위해, attention을 사용하는 것이다. 위의 목적을 아래처럼 바꾸어 보았다.

1. 특정 시점의 디코더 셀의 토큰 벡터를 단어 벡터로 변환할 것이다.
2. 변환할 때, 디코더 셀 단어 길이와 __가장 비슷한 단어 길이__ 를 가진 인코더 셀 단어를 더 많이 반영해서 단어 벡터 변환에 활용할 것이다.

위의 attention은 가장 단어 길이가 비슷한 단어를 더 많이 반영한 번역 모델을 만들겠다는 것이다. 물론 아무도 언어 모델을 이런 식으로 만들지는 않겠지만, 가정한 것이다. 이런 경우, <배경 지식> 파트에서 설명한 attention은 다음과 같이 바뀔 것이다.

1. "디코더 셀의 __단어 길이__(Query)"와 "모든 인코더 셀의 __단어 길이__(Key)"간의 차이 계산
2. 차이값에 대한 softmax 분포 계산
3. softmax 분포를 가중치로 한 "모든 인코더 셀의 은닉 벡터들(Value)"의 "가중합 벡터(Attention Value)" 계산
4. "디코더 셀의 은닉 벡터"와 "가중합 벡터(Attention Value)"를 concat하고 FCN에 input하여, 나오는 output을 단어 벡터로 활용

Query와 Key에 들어갈 내용이 바뀌었고, Q, K, V가 모두 다른 값이 되었다. 즉, attention을 쓰는 사람이 어떻게 쓰느냐에 따라 Q, K, V는 매우 유동적으로 바뀔 수 있다는 것이다.


# 결론

Attention의 Q, K, V에 대해 더 자세히 이해하려고 공부한 거였지만 결론적으로 더 중요한 걸 깨달았다. 방법론을 완전히 이해해야 유동적인 사용이 가능하다. wikidocs에 나와 있는 내용 정도에서 끝내고 넘어갔다면 attention을 다른 곳에 활용할 생각은 절대 못 했을 것이다.


# 출처 및 참고 자료

[attention\, self attention 관련 지식 및 이미지](https://wikidocs.net/31379) : 딥러닝을 이용한 자연어 처리 입문