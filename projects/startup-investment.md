---
layout: page
title: "스타트업 투자 유치 요인 분석"
description: |
  2019\.03 ~ 2019\.07  
  스타트업 리크루팅 사이트의 데이터를 바탕으로 투자 유치 요인을 분석한 팀 프로젝트입니다.
hide_description: false
sitemap: false
---

0. Table of Contents
{:toc}

## Background

학부 수업인 \<데이터마이닝이론및응용\> 수업에서 머신러닝 관련 구체적 이론을 접한 뒤, 이를 활용하는 차원에서 진행했던 팀 프로젝트입니다. 2018년 기준, 벤처 투자의 규모는 34,259억원으로 최대치를 기록하였습니다. 그러나, 여전히 많은 스타트업이 자금 유치에 어려움을 겪고 있습니다.

스타트업의 투자 유치에 관련된 선행 연구는 존재하나, 정성적 연구이거나 설문을 통한 연구, 또는 기업의 수치적인 부분에 대한 통찰이 많았습니다. 이에 저희 팀은 스타트업의 정보에서 대표자, 기업에 대한 새로운 변수를 데이터적인 관점에서 알아보고 투자사들이 스타트업을 평가함에 있어서 새로운 지표가 될 수 있는 요인을 발굴하고자 하였습니다.


## Process

### Data Processing

스타트업 위주의 리크루팅 사이트인 [로켓펀치](https://www.rocketpunch.com/companies)에는 대표자의 학력, 기업 소재지, 대표자 간 네트워크와 기술 스택 등 다양한 스타트업 관련 정보가 있습니다. 이 사이트에서 로켓펀치에 등록된 지 3년 이상이 된 스타트업 200여개를 파이썬을 이용해 웹스크래핑하여 데이터를 수집하였습니다.

X변수로 대표자의 출신 학부, 대표자의 최종 학력, 대표자의 인맥 지표, 기업의 매력 지표, 산업 분야, 기술 분야, 기업의 소재지 등 7개를 먼저 사용하였고, Y변수는 3년 이내에 받은 투자 액수의 합계로 설정하였습니다. 대표자의 인맥 지표는 로켓펀치에 연결된 다른 대표자의 수로 설정하였으며, 기업의 매력 지표는 팔로우 수를 조회수로 나눈 값을 사용하였습니다. 

|**변수**|**세부 설명**|
|:-------|:-------|
|**X1**|대표자의 출신 학부 : 범주형|
|**X2**|대표자의 최종 학력 : 범주형|
|**X3**|대표자의 인맥 : 수치형(명)|
|**X4**|기업의 매력도 : 수치형|
|**X5**|산업 분야 : 범주형(교육, 금융, 패션 등 8가지)|
|**X6**|기술 분야 : 범주형(웹서비스, 모바일 등 6가지)|
|**X7**|기업 소재지 : 범주형|

위 변수 중 X1, X2, X3, X4, X7을 수치형 변수로 변환하여 FA 및 Clustering을 통해 기업을 5개의 클러스터로 나누었으며, 분류 결과를 X변수에 추가하여 Y변수를 예측하기 위한 분석 데이터로 활용하였습니다.

<!-- ![startup-FA image](/assets/img/projects/startup-FA.jpg){width="100" height="200" loading="lazy"} -->
<!-- <p align="center">
  <img width="350" src="/assets/img/projects/startup-FA.jpg">
</p> -->
최종적으로 만들어진 분석용 데이터의 X, Y변수는 다음과 같습니다.

|**변수**|**세부 설명**|
|:-------|:-------|
|**X1**|대표자의 출신 학부 : 범주형|
|**X2**|대표자의 최종 학력 : 범주형|
|**X3**|대표자의 인맥 : 수치형(명)|
|**X4**|기업의 매력도 : 수치형|
|**X5**|산업 분야 : 범주형(교육, 금융, 패션 등 8가지)|
|**X6**|기술 분야 : 범주형(웹서비스, 모바일 등 6가지)|
|**X6`**|자본 집약 산업 여부 : 범주형(웹서비스-모바일-e commerce-플랫폼, IoT-AI-기타 의 2가지)|
|**X7**|기업 소재지 : 범주형|
|**X8**|클러스터 결과 : 범주형|
|**Y**|3년 이내 투자 유치액 : 수치형(천만원)|

X6` "자본 집약 산업 여부" 변수는 기술분야에 따라 투자금의 range가 달라질 가능성을 고려하기 위해 X6에서 파생하였습니다.
{:.figure}


### Modeling

기술분야에 따라 투자금의 range가 달라질 것을 고려하여 X6` 변수를 기준으로 스타트업의 산업군을 두 가지 범주로 분류하였습니다. 각 범주에 각각 MBR Regression, MBR Classification, 그리고 Logistic Regression을 수행하였습니다. 분석 프로세스를 다음과 같이 간략하게 그림으로 나타낼 수 있습니다.

![startup-process-all](/assets/img/projects/startup-process-all.jpg){:.lead loading="lazy"}

Y변수(투자 유치액)의 경우 수치형 변수이기 때문에, Classification을 수행할 때 적절한 값을 기준으로 투자 유치 성공 여부를 나누어야 했습니다. X6`을 기준으로 나뉜 각 그룹에 대해, 하위 40%의 투자금액(4억원, 6.5억원)을 기준으로 Y변수를 1과 0으로 나누고 Classification을 진행하였습니다. MBR Regression 및 MBR Classification에서 각각 어떤 k값을 가지는 것이 가장 좋은 예측 결과를 가져오는지 평가하였고, Logistic Regression을 통해 얻어낸 회귀식의 계수를 이용하여 Odds ratio 분석을 수행하였습니다. 

MBR에서는 Regression의 경우 k=21, Classification의 경우 k=11일 경우 가장 예측 확률이 높다는 결론을 얻었습니다. Classification의 경우, 하위 40% 이상의 투자금액을 받는 기업은 80~90% 정도의 정확도로 예측했지만 하위 40% 미만의 투자금액을 받는 기업은 40~50%의 정확도로 예측하였습니다.

Odds ratio 분석을 통해 투자 유치 확률이 대표자의 인맥 지표가 한 단위 오를 때마다 1.6%, 기업의 매력도 지표가 한 단위 오를 때마다 18% 오른다는 결론을 얻어냈습니다. 그러나 그 외, 학력이 비공개에서 공개로 바뀌면 투자 유치 성공 확률이 0%에 가까워진다거나, 인프라가 부족한 대표자가 사교적 성격인 대표자보다 매우 높은 확률로 투자 유치에 성공하는 결과를 가져오는 등 받아들이기 어려운 결과도 도출되었습니다.


## Meaning

데이터 분석에 대한 이론적 기초를 갓 배운 상태로 수행했던 프로젝트이기 때문에, 배운 점도 많았지만 아쉬운 점도 많은 프로젝트였습니다. 가장 아쉬운 점은 역시 데이터가 부족했다는 점이었습니다. 분석에 사용할 변수의 개수도, 데이터 자체의 개수도 적었기에 무리한 가정으로 분석을 진행한 부분이 많았습니다. 순서형 변수가 될 만한 가능성이 있는 범주형 변수들을 모두 수치형으로 변환하여 Clustering에 사용하거나, 투자 유치 성공 여부를 나누는 기준이 모호했다는 점, 그리고 투자 유치에 실패한 기업들의 데이터를 입수하는 데에 어려움이 있었다는 점 등이 아쉬운 점입니다. 그러나 스타트업의 투자 유치 여부를 판단하는 데에 기업의 수치적, 재정적 요소뿐 아니라 스타트업 대표의 인맥, 또는 스타트업 자체의 매력도 또한 어느 정도의 영향을 미칠 수 있음을 볼 수 있었던 프로젝트였으며, 개인적으로도 실제적인 데이터 분석을 경험할 수 있었던 의미 있는 프로젝트였습니다.



## Skills

Python(beautifulsoup, selenium), SAS


Go back to [Myeong Hyeon Son](/about/){:.heading.flip-title}
{:.read-more}