---
layout: page
title: "항공사 지수 개발 및 배치 추론 파이프라인 구축"
description: |
  2023\.11 ~ 2024\.03  
  항공사에서 활용할 지수를 개발하고, 일/월 배치 추론을 수행하는 파이프라인을 구축하였습니다.
hide_description: false
sitemap: false
---

0. Table of Contents
{:toc}


## Overview

A항공사는 여러 곳의 원천 데이터를 한 데 모아서 CDP를 구축하고자 했고, 그 과정에서 로그 집계 기반 집계지수 및 머신러닝 모델 기반의 추론지수를 개발하고자 하였습니다. 해당 사업에서 저는 머신러닝 모델 기반의 추론지수 중 하나(High-Class 선호지수)를 Sagemaker Studio 환경에서 개발하였고, 모든 추론지수 개발이 완료된 후 지수들의 배치 추론 파이프라인을 Sagemaker, Glue, MWAA를 활용하여 구축하였습니다.

개발한 High-Class 선호지수는, 과거 데이터를 기반으로 향후 6개월 간 해당 고객이 프레스티지/퍼스트 클래스를 구매할지 여부를 예측하는 모델입니다. S3, Athena를 활용하여 기 구축된 Data Lake에서 EDA를 수행하였고, 성별/연령 및 마일리지 정보 등을 바탕으로 XGBoost를 활용한 예측 모델을 개발하였습니다.

추론지수 개발이 완료된 후, 5개 지수에 대해 각각의 배치 추론 파이프라인을 구성하였습니다. 스케줄러 및 파이프라인 코드는 MWAA(Airflow)를 활용하였고, MWAA가 지원하는 SagemakerOperator 및 GlueOperator를 활용하여 해당 서비스를 구동했습니다. Sagemaker Job 내에서 수행될 소스코드는 Python으로 개발하였으며, Load, Preprocess, Train, Inference, Postprocess의 5개 클래스로 구성하였습니다.


## Process




## Meaning

위에서 말했듯, 이전의 BackTester에 있는 문제들을 개선하기 위해 여러 노력을 기울였습니다. 결과적으로 많은 부분에서 개선되었고 특히 데이터를 수집하고 처리하는 collector 모듈에서 클래스 상속을 통해 반복 작업을 줄일 수 있었습니다.

처음에는 binance futures connector(binance 공식 라이브러리) 없이 requests, asyncio 등 general한 라이브러리를 활용해서 만드려고 했습니다([codes](https://github.com/menmenmeng/TIL/tree/main/AutoTrader/BinanceTrader/rt_trader_noConnector/wss_trader0)). 그러나 websocket stream을 열고 유지하는 과정이 너무 복잡하고 본인이 키우려는 스킬과는 거리가 멀다고 생각해 이후에는 binance futures connector를 활용한 모델로 수정하여 프로그램을 작성했습니다.

기술 지표를 활용한 전략 구현(conditional, decision 모듈)에 있어서는 아직 확실하게 구조화, 모듈화가 되지 못했습니다. 활용하는 전략마다 지표가 다르기 때문에 하드코딩되는 부분이 필연적으로 존재하여 이 부분을 최대한 줄이려고 합니다.


## Skills

Python

Go back to [Myeong Hyeon Son](/about/#projects){:.heading.flip-title}
{:.read-more}