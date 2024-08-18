---
layout: about
image: /assets/img/myown/og-image.jpg
description: >
  Porfolio of Myeong hyeon Son.
hide_description: true
redirect_from:
  - /projects/
  - /download/
---

# Myeong Hyeon Son

<!--author-->

0. Table of Contents
{:toc}

## About Me

데이터 분석가이자 MLOps 엔지니어로서 성장하고자 하는 손명현입니다. 데이터를 통한 고찰뿐 아니라, 데이터를 바탕으로 한 제품의 안정적 배포까지 데이터의 흐름과 관련된 모든 것에 관심을 가지고 있습니다. 회사에서 데이터와 관련된 다양한 프로젝트를 해보며 경험을 쌓아가고 있습니다.

## Profile

__Name__
{:.lead}
손명현 (Myeonghyeon Son), 1995년 4월 9일생


__Education__
{:.lead}
Yonsei University - Industrial Engineering

- Bachelor of Science
- 2014.03 ~ 2022.08
- Cumulative GPA 3.73/4.3


__Contact__
{:.lead}
- (+82)010-8776-9308
- franksmh0409@gmail.com

<br>
<br>
<br>
<br>
<br>

## Skills

__Python__
{:.lead}
- \<공학정보처리\>, \<정보프로그래밍\> 수업 및 \<데이터마이닝 이론 및 응용\> 수업으로 파이썬 및 머신러닝 활용을 공부하였습니다.
- \<스타트업 투자 유치 요인 분석\>, \<코로나 팬데믹 이후 품목별 소비 예측\>, \<가상화폐 자동 트레이딩 머신\> 프로젝트에서 파이썬을 활용하였습니다.
- LG CNS 내 프로젝트(항공사 MLOps 구축, 항공사 CDP 구축)에서 파이썬을 활용하였습니다.

__SQL(MySQL)__
{:.lead}
- <산업정보관리론> 수업으로 DB의 이론적 지식 및 SQL을 학습하였습니다.
- LG CNS 인턴십에서 Insight 도출을 위해 활용하였습니다.
- 항공사 CDP 구축 프로젝트에서 SQL을 활용하여 데이터 변환 로직을 작성하였습니다.

__AWS(S3, Athena, Glue, Sagemaker, MWAA)__
{:.lead}
- 항공사 MLOps 구축 프로젝트에서 Sagemaker Pipeline, Sagemaker AutoML을 활용하여 MLOps 파이프라인을 구축하였습니다.
- 항공사 CDP 구축 프로젝트에서 S3, Athena를 활용하여 EDA 수행 및 최종 테이블을 설계하였습니다.
- 항공사 CDP 구축 프로젝트에서 Glue, Sagemaker, MWAA(Airflow)를 활용하여 배치 추론 파이프라인을 구축하였습니다.

<!-- __GCP(BigQuery, Looker Studio)__
{:.lead}
- 앱 푸시 시스템 고도화 프로젝트(타겟팅 시스템 구축)에서 BigQuery를 활용하여 ETL 파이프라인을 구축하였으며 Looker Studio를 활용하여 대시보드를 구축하였습니다. -->

__tableau__
{:.lead}
- LG CNS 인턴십에서 데이터 탐색 작업 후 도출한 Insight를 프레젠테이션하기 위해 활용하였습니다.

<br>
<br>
<br>
<br>
<br>
<br>


## Projects

시간 역순으로 기록하였습니다.

__[사내] 앱 푸시 시스템 고도화 (Ongoing)__
{:.lead}

_2024\.05 ~ 2024\.07_
{:.faded}

- __수행 업무__<br>
  Java Devon 프레임워크(CNS 자체 프레임워크) 기반의 앱 푸시 광고 시스템에서 타겟 마케팅 시스템을 위한 DW 및 ETL 파이프라인 구축<br>
  Java 환경의 웹 배치 서버에서 GCP BigQuery로의 데이터 이관 및 집계 파이프라인 구성

- __활용 Skill__<br>
  Java, SQL, GCP(BigQuery)


Continue reading [detail](projects/app-push-targeting-system-development.md)
{:.read-more}



__[사내] 항공사 내 추론지수 개발 및 배치 추론 파이프라인 구축__
{:.lead}

_2023\.11 ~ 2024\.03_
{:.faded}

- __수행 업무__<br>
  항공사 CDP에서 ML기반의 지수를 개발하고, 개발한 지수의 배치 추론 파이프라인을 AWS 환경에서 구축<br>
  프레스티지/퍼스트 클래스 구매 가능성을 지수화하는 High-Class 선호지수를 개발하였고, 해당 지수를 포함하여 5개 지수의 주기적 배치 파이프라인을 MWAA를 활용하여 구성

- __활용 Skill__<br>
  Python, SQL, AWS(Sagemaker, S3, Athena, MWAA, Glue)


Continue reading [detail](projects/airline-feature-development.md)
{:.read-more}



__[사내] 항공사 내 MLOps 시스템 구축__
{:.lead}

_2023\.07 ~ 2023\.10_
{:.faded}

- __수행 업무__<br>
  항공사 MLOps 환경을 구축하고, 기존에 수기로 운영 중이던 ML모델을 해당 환경에 마이그레이션<br>
  AWS 환경에서 Sagemaker, Lambda, EventBridge를 활용하여 학습-추론-모니터링 파이프라인을 구축하고, 라운지 이용객 수 예측 모델을 해당 시스템 위에 이식하였음

- __활용 Skill__<br>
  Python, AWS(Sagemaker, S3)


Continue reading [detail](projects/airline-mlops-system-development.md)
{:.read-more}



__[사내] 평생교육 플랫폼 학습 컨텐츠 분류 및 추천 방안 설계__
{:.lead}

_2022\.11 ~ 2023\.01_
{:.faded}

- __수행 업무__<br>
  평생교육 플랫폼 통합 프로젝트에서 데이터 분석 과제에 대한 컨설팅 수행<br>
  학습 컨텐츠 카테고리의 자동 분류, 학습자 맞춤형 컨텐츠 추천의 주제로 분석과제 도출 및 수행 방안을 설계하였음

- __활용 Skill__<br>
  PowerPoint


Continue reading [detail](projects/lifelong-edu-platform.md){:.heading}
{:.read-more}



__[개인] 가상화폐 자동 트레이딩 머신__
{:.lead}

_2022\.08 ~ 2023\.02_
{:.faded}

- __수행 업무__<br>
  Binance의 API를 활용하여 비트코인 선물 자동 트레이딩 시스템을 구축<br>
  선물 가격 데이터의 로드, 매매 전략에 따른 매매 수행을 라이브러리 형태로 구현<br>
  백테스터 &rarr; 실시간 트레이더 2단계의 과정을 통해 구현하였음

- __활용 Skill__<br>
  Python


_Skills : Python_
{:.faded}


_백테스터 (2022\.08 ~ 2022\.10)_{:.faded} Continue reading [detail](projects/binance-auto-trader-backtester.md){:.heading}
{:.read-more}  
_실시간 트레이더 (2022\.11 ~ 2023\.02)_{:.faded} Continue reading [detail](projects/binance-auto-trader-realtime.md){:.heading}
{:.read-more}  



__[사내] TV 시청 로그 데이터를 활용한 INSIGHT 발굴__
{:.lead}

_2022\.06 ~ 2022\.07_
{:.faded}

- __수행 업무__<br>
  LG CNS 인턴십 동안 LG U+, LG스포츠, LG사내복지몰 등 LG계열사의 데이터 풀에서 데이터를 탐색하고 Insight를 발굴<br>
  LG U+ 의 TV 시청로그를 통해 유의미한 지표를 생성하고, Insight를 프레젠테이션함

- __활용 Skill__<br>
  SQL, tableau


Continue reading [detail](projects/uptv-log.md){:.heading}
{:.read-more}



__[개인] 코로나 팬데믹 이후 품목별 소비 예측__
{:.lead}

_2021\.09 ~ 2021\.11_
{:.faded}

- __수행 업무__<br>
  공공 데이터포털의 카드 소비 데이터를 활용하여 소비 패턴 변화를 관찰하고 프레젠테이션<br>
  RandomForest기법을 활용하여 시계열 분석 모델링을 수행

- __활용 Skill__<br>
  Python


Continue reading [detail](projects/forecast-after-covid.md){:.heading}
{:.read-more}



__[학부] 스타트업 투자 유치 요인 분석__
{:.lead}

_2019\.03 ~ 2019\.07_
{:.faded}

- __수행 업무__<br>
  스타트업 채용정보 사이트를 스크래핑하여 각 스타트업의 관련 정보를 수집하고, 군집화, MBR, 로지스틱 회귀를 적용하여 스타트업이 일정 금액 이상의 투자금을 유치할 확률이 얼마나 되는지를 예측하는 프로젝트 수행

- __활용 Skill__<br>
  Python, SAS


Continue reading [detail](projects/startup-investment.md){:.heading}
{:.read-more}



## Websites

[__블로그__ : https://menmenmeng.github.io/about/](https://menmenmeng.github.io/about/)

[__깃허브__ : https://github.com/menmenmeng](https://github.com/menmenmeng)


<!-- [__Blog__](https://menmenmeng.github.io)
{:.lead}
데이터 분석 관련된 지식들과 취미생활을 공유하기 위해 만든 블로그 페이지입니다.
이거 hydejack 예시 파일들 아직 남아있음, 이거 지워주기. -->