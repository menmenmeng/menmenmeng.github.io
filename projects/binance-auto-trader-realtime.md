---
layout: page
title: "가상화폐 자동 트레이딩 머신 - 실시간 트레이더"
description: |
  2022\.11 ~ 2023\.02 
  Binance의 비트코인 선물 종목의 매매전략을 테스트하고, 전략에 맞추어 자동으로 트레이딩하는 봇을 만드는 개인 프로젝트입니다.
  가상화폐 거래소의 1분봉 데이터를 받고, 적절한 거래 전략을 거쳐 매매 여부를 결정한 뒤, 지정한 수량을 지정한 가격에 매매하는 트레이딩 봇을 작성하였습니다.
hide_description: false
sitemap: false
---

0. Table of Contents
{:toc}


## Background

2022년 8월부터 약 2달의 시간 동안 비트코인 선물거래 데이터를 활용하여 전략을 백테스팅하는 라이브러리를 작성하였습니다. 이후에는 프로젝트의 본질적인 목적인, "지정한 조건에 따라 자동적으로 거래하는 트레이딩 봇"을 작성하였습니다.

이전에 작성했던 백테스팅 라이브러리는 활용하지 않고, 처음부터 작성하였습니다.


## Process

프로젝트의 최종 목표까지 도달하기 전, 작은 목표들을 쪼개자면 다음과 같습니다.
> - 백테스터 라이브러리 작성
> - 기본적 전략을 활용한 실시간 트레이더 작성
> - 비트코인 선물 가격 데이터를 활용한 데이터 분석을 통해, 변동성/가격 변동 등 예측
> - Rule-based가 아닌, 예측 알고리즘을 바탕으로 한 실시간 트레이더 작성



![binance-backtest-process](/assets/img/projects/binance-backtest-process.jpg){:.lead loadings="lazy"}

### API Communication

API 통신은 바이낸스에서 공식적으로 제공하는 binance futures connector 라이브러리를 사용하고 있습니다. 실제 트레이딩과는 큰 관계가 없지만 기능 구현을 위해 꼭 필요한 복잡한 작업들(ex. get, put에 들어갈 parameter를 받을 때, 필수가 아닌 파라미터를 빼고 함수를 실행시켜도 동작하게 하는 등)을 잘 구현해 놓았기에 활용하였습니다.


### Backtesting

백테스팅을 위해 세 가지 모듈을 구성하였습니다.

> 1. BackDataLoader : 과거의 가상화폐 가격 및 거래량 데이터 로딩 모듈
> 
> 2. ConditionGenerator : 가상화폐 매매 전략 구현 모듈
> 
> 3. BackTester : 구성된 과거 데이터 및 매매 전략을 이용하여 전략을 테스트하는 모듈


####  BackDataLoader

BackDataLoader는 과거의 가상화폐 가격 데이터를 원하는 기간 동안, 원하는 interval에 맞게 가져와주는 모듈입니다. 

기본적으로 제공하는 Binance의 API에는 max로 가져올 수 있는 row의 개수가 1500개로 정해져 있으며 이 개수를 초과한 데이터 요청은 받지 않습니다. BackDataLoader는 가져오고 싶은 데이터의 start Time과 end Time, 그리고 interval을 입력받으면 그에 따른 row의 개수를 체크하고 1500개가 넘는다면 여러 번의 데이터 요청을 통해 데이터를 가져오고 이를 하나의 DataFrame으로 묶어서 리턴합니다.

[codes](https://github.com/menmenmeng/TIL/blob/main/AutoTrader/BinanceTrader/backTester/BackDataLoader.py){:.heading}
{:.read-more}


####  ConditionGenerator

ConditionGenerator는 벡테스팅에 활용할 전략을 구성할 때, 특별한 코딩 없이 _포지션 구성 조건을 추가_ 하는 두 가지 메소드로 long 포지션, short 포지션, 그리고 포지션을 청산하는 조건을 만들도록 한 모듈입니다.

- add_andCondition()

  tmp_conditions라는 인스턴스 변수에 AND로 묶이는 condition을 추가해 주는 메소드. 추가된 조건들은 아래의 add_condition() 메소드를 통해 최종적으로 포지션 구성 조건으로 저장됨.

- add_condition()

  위의 add_andCondition() 메소드를 통해 AND로 묶이는 condition들이 tmp_conditions에 담기면, 이를 실제 condition을 나타내는 인스턴스 변수(long_conditions, short_conditions, clear_conditions)에 담는 역할을 함. 이번에 담기는 조건들은 OR로 묶이게 됨.


~~~python
# Example 1
cc = ConditionGenerator(3, 0)

cc.add_andCondition('MA1', 'MA2', '<', 3)                           # and-condition 1 (AC1)
cc.add_andCondition('MA1', 'MA2', '>', 2, func1=lambda x:x*0.9999)  # and-condition 2 (AC2)
cc.add_andCondition('MA1', 'MA2', '>', 1, func1=lambda x:x*0.9998)  # and-condition 3 (AC3)
cc.add_andCondition('MA1', 'MA2', '>', 0, func1=lambda x:x*0.9997)  # and-condition 4 (AC4)

cc.add_condition('long') # or-condition 1
~~~

> long_conditions : (AC1 and AC2 and AC3 and AC4)

~~~python
# Example 2
cc.add_andCondition('MA1', 'MA2', '<', 3)                           # and-condition 1 (AC1)
cc.add_andCondition('MA1', 'MA2', '>', 2, func1=lambda x:x*0.9999)  # and-condition 2 (AC2)
cc.add_andCondition('MA1', 'MA2', '>', 1, func1=lambda x:x*0.9998)  # and-condition 3 (AC3)
cc.add_andCondition('MA1', 'MA2', '>', 0, func1=lambda x:x*0.9997)  # and-condition 4 (AC4)
cc.add_andCondition('_short_amount', 0, '>', 0)                     # and-condition 5 (AC5)
cc.add_Condition('clear') # or-condition 1

cc.add_andCondition('MA1', 'MA2', '>', 3)                           # and-condition 6 (AC6)
cc.add_andCondition('MA1', 'MA2', '<', 2, func1=lambda x:x*1.0001)  # and-condition 7 (AC7)
cc.add_andCondition('MA1', 'MA2', '<', 1, func1=lambda x:x*1.0002)  # and-condition 8 (AC8)
cc.add_andCondition('MA1', 'MA2', '<', 0, func1=lambda x:x*1.0003)  # and-condition 9 (AC9)
cc.add_andCondition('_long_amount', 0, '>', 0)                      # and-condition 10 (AC10)
cc.add_Condition('clear') # or-condition 2
~~~

> clear_conditions : (AC1 and AC2 and AC3 and AC4 and AC5) OR (AC6 and AC7 and AC8 and AC9 and AC10)


위처럼 만든 조건은 현재는 T/F 조건으로서의 역할을 하지 못하는 pseudo-condition들이며, 이는 BackTester 모듈에서 실제 T/F조건으로 변환되어 사용됩니다.

[codes](https://github.com/menmenmeng/TIL/blob/main/AutoTrader/BinanceTrader/conditionGenerator/ConditionGenerator.py){:.heading}
{:.read-more}


####  BackTester

ConditionGenerator에서 만들어진 조건들을 가지고 실제 백테스팅을 해주는 모듈입니다. ConditionGenerator를 통해 만든 pseudo-condition들을 실제 T/F 조건으로 변환하는 메소드, 그리고 과거 데이터를 입력받아 최종 수익률을 return하는 메소드가 주요 메소드입니다.

- _make_real_condition()

  ConditionGenerator에 저장된 AND로 묶이는 조건들 각각의 실제 True/False 여부를 확인하고 리턴.

- _make_conditions()

  ConditionGenerator에 저장된 OR로 묶이는 조건들 각각의 실제 True/False 여부를 확인하고 리턴.
  메소드 내부에서 _make_real_condition()을 불러와서 AND 조건들의 T/F를 리턴받고, 이를 다시 OR로 묶은 컨디션의 T/F를 리턴.

- backtest_tmp()

  과거 데이터를 처음부터 끝까지 탐색해 가며 조건을 확인하고, 조건에 따라 long, short포지션을 취하거나 포지션을 청산(clear)하며 최종적인 수익률을 리턴함. set_long(), set_short(), set_clear()라는 매매 메소드, 그리고 _make_conditions()라는 T/F 확인 함수로 이루어져 있음


[codes](https://github.com/menmenmeng/TIL/blob/main/AutoTrader/BinanceTrader/backTester/BackTester.py){:.heading}
{:.read-more}


### Real-Time Trading (To do)

진행 예정

### Data Analysis & Strategy (To do)

가장 기본적이라고 할 수 있는 이동평균 돌파 전략, 그리고 볼린저 밴드를 활용한 전략을 사용하여 백테스팅 중입니다. parameter를 여러 쌍 정해 두고 RandomSearch를 이용하여 가장 좋은 결과를 내는 파라미터를 찾고 있습니다. 위 전략을 사용해 실시간 트레이더를 작성해본 후, 마지막으로 데이터 분석 기법을 통한 전략 구성을 고민하려 합니다.

전략에 따라 수익이 나는 달이 확연히 차이나는 경우가 있어, 향후에는 각 월별 데이터에 어떤 다른 점이 있는지를 탐색하고자 합니다.


## Meaning

파이썬은 객체지향 언어라는 특성이 있지만, 이를 제대로 활용해본 적은 없었습니다. 이 프로젝트를 통해 파이썬의 class를 이용한 프로그래밍에 조금씩 익숙해져 가고 있는 것 같습니다. 지금까지 파이썬 개발 자체에는 크게 관심을 두지 않았어서 부족한 부분이 많습니다. condition을 저장하는 모듈(ConditionGenerator)이 특히, 난잡하고 투박하다는 생각이 들어 이 부분을 들어내고 새롭게 개발할까 고민 중입니다.




## Skills

Python

Go back to [Myeong Hyeon Son](/about/){:.heading.flip-title}
{:.read-more}