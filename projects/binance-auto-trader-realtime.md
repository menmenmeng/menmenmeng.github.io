---
layout: page
title: "실시간 트레이더"
description: |
  2022\.11 ~ 2023\.02  
  가상화폐 자동 트레이딩 프로젝트  
  Binance의 비트코인 선물 종목의 매매전략을 테스트하고, 전략에 맞추어 자동으로 트레이딩하는 봇을 만드는 개인 프로젝트입니다.
  가상화폐 거래소의 1분봉 데이터를 받고, 적절한 거래 전략을 거쳐 매매 여부를 결정한 뒤, 지정한 수량을 지정한 가격에 매매하는 트레이딩 봇을 작성하였습니다.
hide_description: false
sitemap: false
---

0. Table of Contents
{:toc}


## Background

2022년 8월부터 약 2달의 시간 동안 비트코인 선물거래 데이터를 활용하여 전략을 백테스팅하는 백테스터 라이브러리를 작성하였습니다. 이는 제가 실행할 매매 전략을 실험함과 동시에, 향후 작성할 트레이딩 봇의 코딩 베이스로 활용하기 위함이었습니다. 그러나 백테스터 작성 후 몇 주의 휴식을 거치고 실시간 트레이더 작성을 계획하면서, 두 가지 이유로, 제가 작성한 백테스터 라이브러리를 실시간 트레이더 작성에 활용하기 어려울 것임을 깨달았습니다. 

1. websocket 통신에 대한 고려 부족
> 실시간 트레이더는 코인 시장의 데이터를 받을 때 REST API가 아닌 websocket을 활용합니다. 백테스터를 작성할 당시에는 websocket에 대한 이해가 부족했기에 이에 대한 고려를 거의 하지 않았고, 그렇게 작성한 백테스터는 실시간 트레이더를 작성하려는 시점에서는 websocket 관련 기능을 추가하기에는 어려운 구조가 되어 있었습니다. 특히, 매매 조건을 확인하는 모듈에서 websocket 관련 기능을 추가하기에 매우 어려운 구조였습니다.

2. 코드의 일관성 및 가독성 부족
> 이전에 작성한 백테스터는 비슷한 기능의 함수인데도 다르게 코딩되어 있는 등 일관성이 부족하거나 하드 코딩된 부분이 많았고, 주석이 많이 달려 있지 않았습니다. 백테스터를 작성할 당시에는 작동 방식을 기억했지만 시간이 지난 후 다시 확인해 보았을 땐 작동 방식을 이해할 수 없어 수정이 어려웠습니다.

이러한 이유로 저는 이전에 작성했던 백테스터를 활용하지 않고, 위의 단점들이 개선되도록 새로운 실시간 트레이더를 작성하였습니다.


## Process

백테스터를 작성하는 동안 프로젝트의 최종 목표까지의 길을 작은 목표들로 쪼개었습니다. 그 목표들은 조금 더 간소화되어, 다음과 같이 진행될 예정입니다.

> - Binance API를 활용하여 기본적 매매를 수행한다.
> - 기본적인 매매 전략을 실험한다(백테스터 라이브러리는 다시 작성하지 않음).
> - REST API 및 websocket을 활용한 실시간 트레이더를 구성한다.
> - 고도화된 매매 전략을 과거 코인 가격 데이터를 활용하여 분석한다.
> - (Optional) 고도화된 매매 전략을 발견했다면, 실시간 트레이더에 적용한다.
> - Graphic UI를 도입하여 배포한다.

### Backtesting

[BackTester](/projects/binance-auto-trader-backtester/){:.heading}

### Trading Process

실시간 트레이더는 다음과 같은 과정을 거치면서 작동됩니다.

 1) 실시간 데이터를 받는 중,  
 2) 원하는 조건에 도달했을 경우  
 3) 실시간 통신을 끊지 않으면서 가상화폐 거래  
 4) 1~3의 반복  

1번의 과정을 위해 websocket 통신이 필요하며,  
2, 3번의 과정을 위해 websocket 통신 중에 수행될 callback 함수가 구성되어야 합니다.


### Real-Time Trader

2023년 2월 기준, 위 프로세스를 거쳐 작동하는 실시간 트레이더를 구성하였습니다. 실시간 트레이더는 binance API 통신을 지원하는 공식 라이브러리인 binance futures connector와 커스텀 모듈 5개(prelim, collector, conditional, decision, callback)를 활용하고 있으며, 아래와 같은 구조로 이루어져 있습니다.

![binance-rt-trader-process](/assets/img/projects/binance-rt-trader-process.jpg){:.lead loadings="lazy"}

callback 모듈은 실시간 데이터를 받는 중, 실시간 통신을 끊지 않으면서 매매 조건 확인 및 매매를 할 수 있도록 하는 callback 함수를 구현한 모듈입니다. collector, conditional, decision 등 3개의 모듈을 활용하여 구성되어 있으며, trader가 websocket을 통해 "Account Update", "Trade Update", "RealTime Price Data" 중 하나의 데이터를 받으면 callback 함수가 실행되어 아래의 3개 프로세스 중 하나를 실행합니다.

![binance-rt-trader-callback-process](/assets/img/projects/binance-rt-trader-callback-process.jpg){:.lead loadings="lazy"}

아래는 작성한 5개의 커스텀 모듈에 대한 설명입니다.

#### Prelim

실시간 트레이더의 동작 전 필요한 동작들을 구현해 놓은 모듈입니다. 현재의 Account Information, 과거 주가 데이터 수집, websocket stream을 열기 위한 ListenKey 생성 및 websocket stream의 url을 생성하는 함수 등을 구현하였습니다.

[codes](https://github.com/menmenmeng/TIL/blob/main/AutoTrader/BinanceTrader/rt_trader_v0.2/trade_rules/prelim.py){:.heading}
{:.read-more}

#### Collector

websocket stream에서 json 형태의 실시간 데이터가 들어오면 이를 pandas의 DataFrame 형태로 바꾸어서 저장해 주는 모듈입니다. MarkPriceCollector, RealTimeKlineCollector, KlineCollector, OrderUpdateCollector, AccountUpdateCollector 클래스가 구현되어 있습니다.

<br>

* __구현 클래스들__

  - Collector  
    아래 클래스들이 상속하는 부모 클래스

  - MarkPriceCollector  
    markPrice stream에서 데이터가 들어오면 이를 dataframe으로 저장합니다.

  - RealTimeKlineCollector  
    kline stream에서 데이터가 들어오면, 데이터를 받을 때마다 realtime Kline dataframe으로 저장합니다.

  - KlineCollector  
    kline stream에서 데이터가 들어오면, 최신 데이터를 업데이트하다가 사전에 지정된 시간 단위(ex. 1분)를 지날 때마다 overall Kline DataFrame에 저장합니다.

  - OrderUpdateCollector  
    websocket 통신 동안 거래가 성사될 때마다 들어오는 거래 데이터를 DataFrame에 저장합니다.

  - AccountUpdateCollector  
    websocket 통신 동안 거래가 성사될 때마다 들어오는 Account 변화 정보를 현재의 Account status에 업데이트합니다.


위에서 Collector 클래스를 제외한 나머지 클래스는 모두 Collector 클래스를 상속받아서 만들어지는 클래스입니다. Collector 클래스에는 대부분의 실시간 데이터 stream에서 공통으로 필요한 데이터 처리 함수들을 구현하였고, 또한 자식 클래스에서 꼭 구현해야 할 함수를 NotImplementedError를 활용하여 표시하였습니다.

<br>

* __Collector 클래스의 메소드들__

  - getEventType(message)  
    json 형태의 message를 받으면, 이 message가 어떤 stream에서 왔는지에 대한 정보를 추출합니다.

  - getRowDictFromMessage(message)  
    json 형태의 message를 dictionary 형태로 바꾸는 메소드로, 자식 클래스 내에서 꼭 구현되어야 할 메소드이기에 부모 클래스인 Collector에 NotImplementedError를 활용하여 구현해 놓았습니다. 어떤 데이터의 stream이냐에 따라 json의 컬럼명이 다르기 때문에, 이 작업은 각 데이터 스트림 Collector에 구현되는 것이 적절하다고 생각됩니다.

  - getDataFrame(message)
    json 형태의 message를 기존의 데이터를 가지고 있는 DataFrame에 업데이트하는 메소드입니다.

<br>

자식 클래스인, 각 데이터 스트림의 Collector에는 getRowDictFromMessage 메소드가 구현되었습니다.

> 예시 : RealTimeKlineCollector에서의 getRowDictFromMessage 메소드

~~~python
def getRowDictFromMessage(self, message):
    streamKey, eventType = self.getEventType(message)
    data = message['data']
    kline = data['k']

    row_dict = dict(
        stream = streamKey,
        eventType = eventType,

        eventTime = int(data['E']),
        startTime = int(kline['t']),
        closeTime = int(kline['T']),
        interval = str(kline['i']),
        open = float(kline['o']),
        high = float(kline['h']),
        low = float(kline['l']),
        close = float(kline['c']),
        volume = float(kline['v'])
    )


    self.closeTime = int(kline['t'])
    self.open = float(kline['o'])
    self.close = float(kline['c'])
    self.high = float(kline['h'])
    self.low = float(kline['l'])
    self.volume = float(kline['v'])

    print(row_dict.values())
    return row_dict
~~~


[codes](https://github.com/menmenmeng/TIL/blob/main/AutoTrader/BinanceTrader/rt_trader_v0.2/trade_rules/collector.py){:.heading}
{:.read-more}

#### Conditional

[codes](https://github.com/menmenmeng/TIL/blob/main/AutoTrader/BinanceTrader/rt_trader_v0.2/trade_rules/conditional.py){:.heading}
{:.read-more}

#### Decision

[codes](https://github.com/menmenmeng/TIL/blob/main/AutoTrader/BinanceTrader/rt_trader_v0.2/trade_rules/decision.py){:.heading}
{:.read-more}

#### Callback

[codes](https://github.com/menmenmeng/TIL/blob/main/AutoTrader/BinanceTrader/rt_trader_v0.2/trade_rules/callback.py){:.heading}
{:.read-more}



### Data Analysis & Strategy (To do)

가장 기본적이라고 할 수 있는 이동평균 돌파 전략, 그리고 볼린저 밴드를 활용한 전략을 사용하여 백테스팅 중입니다. parameter를 여러 쌍 정해 두고 RandomSearch를 이용하여 가장 좋은 결과를 내는 파라미터를 찾고 있습니다. 위 전략을 사용해 실시간 트레이더를 작성해본 후, 마지막으로 데이터 분석 기법을 통한 전략 구성을 고민하려 합니다.

전략에 따라 수익이 나는 달이 확연히 차이나는 경우가 있어, 향후에는 각 월별 데이터에 어떤 다른 점이 있는지를 탐색하고자 합니다.


## Meaning

파이썬은 객체지향 언어라는 특성이 있지만, 이를 제대로 활용해본 적은 없었습니다. 이 프로젝트를 통해 파이썬의 class를 이용한 프로그래밍에 조금씩 익숙해져 가고 있는 것 같습니다. 지금까지 파이썬 개발 자체에는 크게 관심을 두지 않았어서 부족한 부분이 많습니다. condition을 저장하는 모듈(ConditionGenerator)이 특히, 난잡하고 투박하다는 생각이 들어 이 부분을 들어내고 새롭게 개발할까 고민 중입니다.




## Skills

Python

Go back to [Myeong Hyeon Son](/about/){:.heading.flip-title}
{:.read-more}