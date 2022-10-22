---
layout: page
title: "가상화폐 자동 트레이딩 머신"
description: |
  2022\.08 ~  
  Binance의 비트코인 선물 종목의 매매전략을 테스트하고, 전략에 맞추어 자동으로 트레이딩하는 봇을 만드는 개인 프로젝트입니다.
hide_description: false
sitemap: false
---

0. Table of Contents
{:toc}


## Background

기업의 가치를 보고 투자할 수 있는 주식과는 다르게, 가상화폐에는 특수한 것을 제외하고는 실제 가치라고 부를 만한 것이 없습니다. 그렇기에 제게 가상화폐 투자는 투자라기보단 투기의 이미지가 강해서 굳이 흥미를 가지지 않았습니다. 그러나 매체에서 보이던 "가상화폐 자동 트레이딩으로 선거자금을 벌었다"는 정치인, 그리고 주변인들의 가상화폐 자동 트레이딩 실 사례들을 듣고 가상화폐의 가치가 아니라 가상화폐 매매자들의 움직임만으로 상승/하락을 예측할 수도 있지 않을까, 하는 궁금증이 생겼습니다.

데이터 분석을 활용한 가상화폐 매매 전략 도출이 가능할지 확인해 보고 싶어 프로젝트를 시작했으며, 현재는 API 통신의 기본적 지식 공부 및 파이썬 프로그래밍 실력 향상(+ 잘 되면 작은 용돈 벌이까지) 등도 겸하기 위해 작은 라이브러리처럼 매매 프로그램을 만들어가고 있습니다.


## Process

2022년 10월 기준 Binance API를 활용하여 과거 데이터를 로드하고 가상화폐를 매매해 보았으며, 과거 데이터를 로딩하고 백테스팅하는 모듈을 프로그래밍하였습니다. 데이터 분석을 활용한 매매 전략을 도출하는 데에는 좀 더 시간이 걸릴 것 같습니다. 현재는 손해도 이익도 크지 않을 안전한 전략을 바탕으로 백테스팅 모듈 및 웹소켓을 이용한 실시간 트레이딩 봇을 먼저 개발하고, 그 이후 데이터 분석을 통한 매매 전략을 도출해보려 합니다.


### API Communication

API 통신은 바이낸스에서 공식적으로 제공하는 binance futures connector 라이브러리를 사용하고 있습니다. 처음에는 바이낸스에서 제공하는 라이브러리 없이 파이썬의 requests 모듈만 활용하여 매매하려 하였으나, 실제 트레이딩과는 큰 관계가 없지만 기능 구현을 위해 꼭 필요한 복잡한 작업들(ex. get, put에 들어갈 parameter를 받을 때, 필수가 아닌 파라미터를 빼고 함수를 실행시켜도 동작하게 하는 등)을 잘 구현해 놓았기에 활용하였습니다.


### Backtesting Modules

백테스팅을 위해 세 가지 모듈을 구성하였습니다.

> 1. BackDataLoader
> 2. ConditionGenerator
> 3. BackTester

####  BackDataLoader

BackDataLoader는 과거의 가상화폐 가격 데이터를 원하는 기간 동안, 원하는 interval에 맞게 가져와주는 모듈입니다. 

기본적으로 제공하는 Binance의 API에는 max로 가져올 수 있는 row의 개수가 1500개로 정해져 있으며 이 개수를 초과한 데이터 요청은 받지 않습니다. BackDataLoader는 가져오고 싶은 데이터의 start Time과 end Time, 그리고 interval을 입력받으면 그에 따른 row의 개수를 체크하고 1500개가 넘는다면 여러 번의 데이터 요청을 통해 데이터를 가져오고 이를 하나의 DataFrame으로 묶어서 리턴합니다.

[BackDataLoader 코드](https://github.com/menmenmeng/TIL/blob/main/AutoTrader/BinanceTrader/backTester/BackDataLoader.py)


####  ConditionGenerator

ConditionGenerator는 벡테스팅에 활용할 전략을 구성할 때, 특별한 코딩 없이 _포지션 구성 조건을 추가_ 하는 두 가지 메소드로 long 포지션, short 포지션, 그리고 포지션을 청산하는 조건을 만들도록 한 모듈입니다.

- add_andCondition()

  tmp_conditions라는 인스턴스 변수에 AND로 묶이는 condition을 추가해 주는 메소드입니다. 추가된 조건들은 아래의 add_condition() 메소드를 통해 최종적으로 포지션 구성 조건으로 저장됩니다.

- add_condition()

  위의 add_andCondition() 메소드를 통해 AND로 묶이는 condition들이 tmp_conditions에 담기면, 이를 실제 condition을 나타내는 인스턴스 변수(long_conditions, short_conditions, clear_conditions)에 담는 역할을 합니다. 이번에 담기는 조건들은 OR로 묶이게 됩니다.


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


위처럼 만든 조건은 현재는 코드로서의 역할을 하지 못하는 pseudo-condition들이며, 이는 BackTester 모듈에서 실제 T/F조건으로 변환되어 사용됩니다.

[ConditionGenerator 코드](https://github.com/menmenmeng/TIL/blob/main/AutoTrader/BinanceTrader/conditionGenerator/ConditionGenerator.py)


####  BackTester

ConditionGenerator에서 만들어진 조건들을 가지고 실제 백테스팅을 해주는 모듈입니다.




[BackTester 코드](https://github.com/menmenmeng/TIL/blob/main/AutoTrader/BinanceTrader/backTester/BackTester.py)



## Meaning


## Skills


Go back to [Myeong Hyeon Son](/about/){:.heading.flip-title}
{:.read-more}