---
layout: page
title: "항공사 MLOps 시스템 구축"
description: |
  2023\.07 ~ 2023\.10  
  항공사에서 MLOps 시스템을 구축하고, 기존에 수기로 운영 중인 ML모델을 MLOps 시스템에 마이그레이션하였습니다.
hide_description: false
sitemap: false
---

0. Table of Contents
{:toc}


## Overview

A항공사는 기존에 수기로 운영 중인 라운지별 이용객 수 예측 모델을 MLOps 환경에 마이그레이션하는 것을 원했으며, 이에 따라 신규로 MLOps 시스템을 구축하고자 하였습니다. 해당 사업에서 저는 ML모델을 최소한의 사람의 손을 거치며 자동 운영 가능한 MLOps 아키텍쳐를 구상하였고, 학습 관련 파이프라인을 AWS 네이티브 서비스와 Python을 활용하여 개발하였습니다.

MLOps 시스템을 구성하는 파이프라인은 추론, 학습, 모니터링 파이프라인으로 구성하였으며 Sagemaker Pipeline을 활용하여 구축하였습니다. 파이프라인 내 Sagemaker Step에서 실행되는 소스코드는 Python으로 개발하였으며, Preprocess, Train, Postprocess, Monitoring의 4개 커스텀 클래스로 구성하였습니다.

Sagemaker 외에 파이프라인 스케줄링을 위해 Lambda 및 EventBridge를 활용하였으며, A항공사의 CI/CD 표준인 BitBucket, Jenkins를 활용하여 CI/CD를 구축하였습니다. 또한 학습 파이프라인 트리거 알림 및 모니터링 파이프라인 결과 알림을 위해 AWS SNS를 활용하였습니다.


## Process

### 파이프라인 아키텍쳐

A항공사는 라운지별 이용객 수 예측 모델을 라운지 종류(MR, PR, FR)에 따라 3개로 나누어 운영하고 있었으며 이를 고려하여 MLOps 파이프라인을 개발하였습니다. 추론, 학습, 모니터링 파이프라인을 중심으로 한 개괄적인 아키텍쳐는 아래와 같습니다.

![image](/assets/img/myown/airline-mlops-architecture-simple.png){:.lead loadings="lazy"}

> 1. 매일 07시, S3에 csv 형태의 데이터 적재
> 2. Lambda를 활용하여 S3 발생 이벤트를 확인하고, Sagemaker와 S3의 데이터를 활용하여 추론 파이프라인 수행
> 3. 매주 일요일 20시, EventBridge를 활용하여 모니터링 파이프라인 수행
> 4. 모니터링 파이프라인 결과 모델에 성능 저하가 발생했을 경우 학습 파이프라인을 트리거하며, 동시에 모니터링 결과를 AWS SNS를 활용하여 알림
> 5. 학습 파이프라인 실행(모니터링 파이프라인 결과 성능 저하가 발생한 모델에 한하여), 학습된 모델은 Sagemaker의 Model Registry에 저장됨. "Pending" 상태로 모델이 저장되며, 해당 모델의 검증 데이터셋 성능을 사람이 확인 후 "Approved" 상태로 변경하면 다음 추론부터 해당 모델을 활용하게 됨
> 6. S3에 저장한 모델 추론 결과를 Lambda를 활용하여 export


### 파이프라인 상세

Sagemaker Pipeline의 작동 방식은 일반적으로 아래와 같습니다.

![image](/assets/img/myown/sagemaker-pipeline.png){:.lead loadings="lazy"}

Sagemaker Pipeline은 Sagemaker Step을 통해 파이프라인을 정의하는 pipeline.py와, 파이프라인의 각 Step마다 켜지는 Sagemaker Instance 안에서 실행되는 스크립트들을 정의함으로써 구성됩니다. 각 Step은 아래의 과정을 거치며 input data 및 스크립트를 전달받고, output을 생성합니다.

1. 인스턴스 생성 후, 인스턴스 내로 사용자 지정 script와 input data를 전달(해당 파일의 위치로 s3 경로 또는 github, bitbucket 등의 코드 리포지토리를 참조 가능)
2. 인스턴스 내에서 사용자 지정 script 실행
3. 인스턴스 내의 저장 공간에 script 실행 결과를 저장
4. 인스턴스 내의 저장 공간을 S3에 복사한 후 인스턴스 종료

위의 구성 방법에 따라 추론, 학습 및 모니터링 파이프라인을 구성하였습니다. 먼저, 각 파이프라인에 대한 개괄적 설명은 아래와 같습니다.

1. 추론 파이프라인 : MR, PR, FR 라운지 3개 모델의 추론 결과를 매일 S3에 적재합니다. 
  - 모든 라운지가 같은 시각에 추론 데이터가 필요하므로, 3개 모델의 추론 파이프라인을 통합하여 하나의 파이프라인으로 구성하였습니다. 

2. 모니터링 파이프라인 : MR, PR, FR 라운지 3개 모델의 일주일치 추론 결과를 바탕으로 성능을 확인합니다. 
  - 같은 시점에 3개 모델의 모니터링 결과를 확인하므로, 3개 모델의 모니터링 파이프라인을 통합하여 하나의 파이프라인으로 구성하였습니다.
  
3. 학습 파이프라인 : 각 라운지별 이용객 수 예측 모델을 학습하고, 모델 아티팩트를 S3 및 Sagemaker의 Model Registry에 저장합니다. 
  - Sagemaker AutoML을 이용하여 구성하였습니다. 라운지별 모델 학습은 각 모델의 모니터링 결과에 따라 다른 시점에 일어날 수 있으므로, 각 라운지별로 학습 파이프라인을 구성하였습니다.

각 파이프라인에 대한 구체적인 구조는 아래와 같습니다.




### 소스코드 구조

각 파이프


## Meaning




## Skills

Python, AWS(Sagemaker, S3)

Go back to [Myeong Hyeon Son](/about/#projects){:.heading.flip-title}
{:.read-more}