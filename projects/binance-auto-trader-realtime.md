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

callback 모듈은 실시간 통신을 끊지 않으면서, message가 들어올 때마다 현 상태를 확인하고 매매 조건 확인 및 매매를 할 수 있도록 하는 callback 함수를 구현한 모듈입니다. collector, conditional, decision 등 3개의 모듈을 활용하여 구성되어 있으며, trader가 websocket을 통해 "Account Update", "Trade Update", "RealTime Price Data" 중 하나의 데이터를 받으면 callback 함수가 실행되어 아래의 3개 프로세스 중 하나를 실행합니다.

![binance-rt-trader-callback-process](/assets/img/projects/binance-rt-trader-callback-process.jpg){:.lead loadings="lazy"}

아래는 작성한 5개의 커스텀 모듈에 대한 설명입니다.

#### prelim

실시간 트레이더의 동작 전 필요한 동작들을 구현해 놓은 모듈입니다. 현재의 Account Information, 과거 주가 데이터 수집, websocket stream을 열기 위한 ListenKey 생성 및 websocket stream의 url을 생성하는 함수 등을 구현하였습니다.

[codes](https://github.com/menmenmeng/TIL/blob/main/AutoTrader/BinanceTrader/rt_trader_v0.2/trade_rules/prelim.py){:.heading}
{:.read-more}

#### collector

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

(예시 : RealTimeKlineCollector에서의 getRowDictFromMessage 메소드)

~~~python
def getRowDictFromMessage(self, message):
    streamKey, eventType = self.getEventType(message)
    data = message['data']

    # json 메시지
    kline = data['k']

    # json 메시지를 dictionary형태로 변환
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

    # 인스턴스 변수를 업데이트
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


#### conditional

Conditional은 Collector가 받아온 데이터를 T/F 값을 가지는 bool 형태로 변환하는 모듈입니다. 데이터프레임의 값을 보고 Volatility의 값이 이전보다 증가했다거나, 현재 주가가 이동평균을 돌파했다거나 등 매매 조건 판단의 재료가 되는 bool 데이터를 Decision 모듈로 전달합니다.

현재는 기초적인 볼린저 밴드 전략을 활용하고 있기 때문에 BBConditional, RVConditional의 두 개 클래스만 구현되어 있습니다. 각 클래스는 Bollinger Band와 Realized Volatility와 관련된 bool 데이터를 만듭니다.

매매 전략이 다양한 만큼 하드코딩이 필요한 부분이 많습니다. 아래는 BBConditional에서 각 밴드선을 돌파하는지 여부를 bool 데이터로 만드는 코드입니다. 

~~~python
# 5분 전까지의 종가 데이터가 upperBand의 위/아래에 있는지 여부
PASTcloses_gt_upperInter_5t = self.closes[-5:] > self.upperInter[-5:]
PASTcloses_gt_upperBand_5t = self.closes[-5:] > self.upperBand[-5:]

# 5분 전까지의 종가 데이터가 lowerBand의 위/아래에 있는지 여부
PASTcloses_lt_lowerInter_5t = self.closes[-5:] < self.lowerInter[-5:]
PASTcloses_lt_lowerBand_5t = self.closes[-5:] < self.lowerBand[-5:]

# 현재(실시간) 종가 데이터가 upperBand의 위/아래에 있는지 여부
CURRclose_gt_upperInter = self.rt_close > float(self.upperInter[-1:])
CURRclose_gt_upperBand = self.rt_close > float(self.upperBand[-1:])

# 현재(실시간) 종가 데이터가 lowerBand의 위/아래에 있는지 여부
CURRclose_lt_lowerInter = self.rt_close < float(self.lowerInter[-1:])
CURRclose_lt_lowerBand = self.rt_close < float(self.lowerBand[-1:])
~~~

위와 같은 데이터들이 Decision 모듈로 전달됩니다.


[codes](https://github.com/menmenmeng/TIL/blob/main/AutoTrader/BinanceTrader/rt_trader_v0.2/trade_rules/conditional.py){:.heading}
{:.read-more}

#### decision

Conditional에서 만들어진 bool 데이터를 바탕으로 현재 상태가 매매 조건에 부합하는지 여부를 확인합니다. 매매 조건에 부합한다면 거래 요청을 REST API를 통해 전달합니다.

- trade(currentPrice, **conditions)  

  현재 주가 및 BBConditional, RVConditional에서 만들어진 bool 데이터를 인자로 받아서 매매 조건 부합 여부를 확인합니다.

  매매 조건은 현재 상태가 롱 포지션인지, 숏 포지션인지, 또는 포지션이 없는지에 따라 나뉩니다.

  1. 포지션이 없을 경우  
    기초적인 볼린저 밴드 전략에 따라 롱/숏 포지션을 취합니다.

  2. 롱 포지션일 경우  
    주가가 0.16%(상수) 상승 시 이득을 취하며 포지션을 청산하고,  
    주가가 0.11%(상수) 하락 시 손해를 보고 포지션을 청산합니다.

  3. 숏 포지션일 경우  
    위와 반대로,  
    주가가 0.16%(상수) 하락 시 이득을 취하며 포지션을 청산하고,  
    주가가 0.11%(상수) 상승 시 손해를 보고 포지션을 청산합니다.


- trade_limit(side, price, amount)  
  trade 메소드에서 포지션을 취하거나 청산할 때 이 메소드가 사용됩니다. long/short 포지션 및 가격과 양을 정하여 REST API를 통해 거래 요청을 전달합니다.


[codes](https://github.com/menmenmeng/TIL/blob/main/AutoTrader/BinanceTrader/rt_trader_v0.2/trade_rules/decision.py){:.heading}
{:.read-more}


#### callback

callback은 websocket을 통해 message가 들어올 때마다 수행되는 함수입니다. 받은 데이터가 어떤 데이터 스트림에서 온 것인지 파악하고, 그에 맞는 기능을 수행합니다. 아래 그림은 위에서 보여 주었던, Callback 클래스의 callback 함수가 수행하는 기능에 대한 프로세스입니다.

![binance-rt-trader-callback-process](/assets/img/projects/binance-rt-trader-callback-process.jpg){:.lead loadings="lazy"}


#### rt_trader

rt_trader에서는 트레이딩을 시작하는 작업 및 KeyboardInterrupt를 통해 트레이딩을 끝내는 작업이 구현되어 있습니다. API Key와 Secret Key를 받아 stream을 열고, 작성한 callback 함수가 여기에서 기능을 수행하도록 합니다.


[codes](https://github.com/menmenmeng/TIL/blob/main/AutoTrader/BinanceTrader/rt_trader_v0.2/trade_rules/callback.py){:.heading}
{:.read-more}


### Data Analysis & Strategy (To do)

현재까지는 복잡한 지표를 따로 활용하지 않고 기초적인 지표인 볼린저 밴드만을 활용하고 있습니다. 자주 활용되는 기술 지표 기반의 여러 전략도 구현해볼 생각은 있지만, 우선은 머신러닝/딥러닝을 활용하여 상승/하락 패턴을 찾는 작업을 해보고 싶습니다. 루나 코인 사태의 기간을 제외한 과거 데이터를 API를 통해 다운로드하였고, 분야에 맞는 여러 가지 방법론을 찾아보고 아웃풋을 얻어보려 합니다.


## Meaning

위에서 말했듯, 이전의 BackTester에 있는 문제들을 개선하기 위해 여러 노력을 기울였습니다. 결과적으로 많은 부분에서 개선되었고 특히 데이터를 수집하고 처리하는 collector 모듈에서 클래스 상속을 통해 반복 작업을 줄일 수 있었습니다.

다만 기술 지표를 활용한 전략 구현(conditional, decision 모듈)에 있어서는 아직 확실하게 구조화, 모듈화가 되지 못했습니다. 활용하는 전략마다 지표가 다르기 때문에 하드코딩되는 부분이 필연적으로 존재하여 이 부분을 최대한 줄이려고 합니다.


## Skills

Python

Go back to [Myeong Hyeon Son](/about/){:.heading.flip-title}
{:.read-more}