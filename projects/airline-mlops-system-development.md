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

A항공사는 기존에 수기로 운영 중인 라운지별 이용객 수 예측 모델을 MLOps 환경에 마이그레이션하는 것을 원했으며, 이에 따라 신규로 MLOps 시스템을 구축하고자 하였습니다. 해당 사업에서 저는 ML모델을 최소한의 사람의 손을 거치며 자동 운영 가능한 MLOps 아키텍쳐를 구상하였고, 해당 아키텍쳐를 구성하는 파이프라인 중 학습 관련 파이프라인을 AWS 네이티브 서비스와 Python을 활용하여 개발하였습니다.

MLOps 시스템을 구성하는 파이프라인은 추론, 학습, 모니터링 파이프라인으로 구성되며 Sagemaker Pipeline을 활용하여 구축하였습니다. 파이프라인 내 Sagemaker Step에서 실행되는 소스코드는 Python으로 개발하였으며, Preprocess, Train, Postprocess, Monitoring의 4개 커스텀 클래스로 구성하였습니다.

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

각 파이프라인에 대한 개괄적 설명은 아래와 같습니다.

1. 추론 파이프라인 : MR, PR, FR 라운지 3개 모델의 추론 결과를 매일 S3에 적재합니다. 
  - 모든 라운지가 같은 시각에 추론 데이터가 필요하므로, 3개 모델의 추론 파이프라인을 통합하여 하나의 파이프라인으로 구성하였습니다. 

2. 모니터링 파이프라인 : MR, PR, FR 라운지 3개 모델의 일주일치 추론 결과를 바탕으로 성능을 확인합니다. 
  - 같은 시점에 3개 모델의 모니터링 결과를 확인하므로, 3개 모델의 모니터링 파이프라인을 통합하여 하나의 파이프라인으로 구성하였습니다.
  
3. 학습 파이프라인 : 각 라운지별 이용객 수 예측 모델을 학습하고, 모델 아티팩트를 S3 및 Sagemaker의 Model Registry에 저장합니다. 
  - Sagemaker AutoML을 이용하여 구성하였습니다. 라운지별 모델 학습은 각 모델의 모니터링 결과에 따라 다른 시점에 일어날 수 있으므로, 각 라운지별로 학습 파이프라인을 구성하였습니다.


### 파이프라인 상세

Sagemaker Pipeline의 작동 방식은 일반적으로 아래와 같습니다.

![image](/assets/img/myown/sagemaker-pipeline.png){:.lead loadings="lazy"}

Sagemaker Pipeline은 Sagemaker Step을 통해 파이프라인을 정의하는 pipeline.py와, 파이프라인의 각 Step마다 켜지는 Sagemaker Instance 안에서 실행되는 스크립트들을 정의함으로써 구성됩니다. 각 Step은 아래의 과정을 거치며 input data 및 스크립트를 전달받고, output을 생성합니다.

> 1. 인스턴스 생성 후, 인스턴스 내로 사용자 지정 script와 input data를 전달(해당 파일의 위치로 s3 경로 또는 github, bitbucket 등의 코드 리포지토리를 참조 가능)
> 2. 인스턴스 내에서 사용자 지정 script 실행
> 3. 인스턴스 내의 저장 공간에 script 실행 결과를 저장
> 4. 인스턴스 내의 저장 공간을 S3에 복사한 후 인스턴스 종료

Sagemaker AutoML Step을 활용하는 경우에는 방식이 조금 달라지는데, 이 방식의 경우 Sagemaker에 AutoML 학습/추론 작업을 생성해달라는 API를 요청하는 방식으로 작동합니다. 따라서 학습/추론 시 추가적인 스크립트를 작성하지 않습니다. AutoML Train/Inference Step을 지정하면, Sagemaker가 학습 작업, 추론 작업을 자동으로 수행합니다.

위의 구성 방법에 따라 추론, 학습 및 모니터링 파이프라인을 구성하였습니다.

#### 추론 파이프라인

preprocessing step, fr inference step, mr inference step, pr inference step, postprocessing step의 5개 step으로 구성되어 있습니다.

> 1. preprocessing step : 각 모델에 input으로 들어갈 데이터를 만들기 위해 raw data를 전처리하는 작업입니다. 
>   - 스크립트 내에서 Preprocess 클래스를 활용하며, 시간대 변환, NA값 치환, 피쳐 생성 등의 작업을 수행합니다.
> 2. fr/mr/pr inference step : 각 라운지의 최신 모델을 받아와서 추론 결과를 내는 작업입니다. 
>   - 모델은 AutoML을 활용하므로 스크립트를 활용하지 않습니다.
> 3. postprocessing step : 각 모델의 추론 결과 output을 하나로 모아, 라운지 운영 팀에서 원하는 형태로 변환하는 작업입니다. 
>   - 스크립트 내에서 Postprocess 클래스를 활용합니다.

#### 모니터링 파이프라인

monitoring step의 1개 step으로 구성되어 있습니다.

> 1. monitoring step : 각 모델의 일주일 간 추론 결과를 통해 성능 지표를 내고, 성능이 기준치 이하로 떨어질 경우 학습 파이프라인을 트리거하는 작업입니다. 
>   - 스크립트 내에서 Monitoring 클래스를 활용하며, 해당 클래스가 수행하는 작업은 아래와 같습니다.
>   - 월요일부터 일요일까지의 추론 결과 데이터와 실제 라운지 이용객 수 데이터를 읽어옵니다.
>   - Rsquare 및 MAE를 계산하고, 성능 지표가 기준치보다 낮다면 학습 파이프라인을 트리거합니다. 

이와 같은 방법으로 생성된 학습 모델은 "PendingManualApproval" 상태로 저장되며, 담당자가 직접 승인해야 추론 모델로서 동작합니다.

#### 학습 파이프라인

preprocessing step, training step으로 구성되어 있습니다. 추론 및 모니터링 파이프라인과 다소 다른 부분이 있습니다.

> 1. preprocessing step : 각 모델에 input으로 들어갈 데이터를 만들기 위해 raw data를 전처리하는 작업으로, 추론 파이프라인 내 작업과 거의 동일합니다.
> 2. training step : AutoML 모델 학습, 검증, 모델 레지스트리 등록 등의 로직을 수행합니다.

학습 파이프라인의 training step의 경우, Sagemaker AutoML Ver.2 사용을 위해,

- 인스턴스 생성 > 사용자 스크립트 내에서 sagemaker job API 호출(인스턴스 생성) > 학습 수행 > 인스턴스 종료(1) > 인스턴스 종료(2)

의 과정을 수행하며, 이중으로 인스턴스를 온/오프합니다.

아래는 학습 파이프라인의 상세 구조입니다.

![image](/assets/img/myown/sagemaker-training-pipeline.png)


#### 참고 : 학습 파이프라인 내 이중 구조

학습 파이프라인의 이중 구조는 적절하지 않은 아키텍쳐이지만, 그와 같은 방식으로 수행해야 하는 이유가 존재했습니다.

1. 고객은 Sagemaker에서 제공하는 AutoML 기능 중, 최근 릴리즈된 AutoML Ver.2를 활용하고 싶어했습니다. AutoML Ver.2는 AutoML Ver.1과 비교하여 비정형 데이터를 다룰 수 있다는 장점이 있습니다.
2. 문제는 해당 기능은 아직 Sagemaker API Connector, 즉 Sagemaker Step으로는 구현되어 있지 않았고, boto3를 통해서만 호출 가능했습니다. Sagemaker Pipeline 구성은 무조건 Sagemaker Step을 통해 구성되어야 하기 때문에, 저는 Step에서 생성하는 인스턴스 안에서 다시 boto3로 AutoML Ver.2 API를 요청하도록 파이프라인을 개발하였습니다.


## Meaning

Ops와 관련된 첫 프로젝트였으며, 그렇기에 아쉬움이 많이 남아 있습니다. 특히, 앞으로 신규 생성될 ML모델이 쉽게 마이그레이션될 수 있는 MLOps 시스템은 만들지 못했다는 생각이 듭니다. MLOps 시스템에 올리려는 모델(라운지 이용객 수 예측 모델)이 일반적인 모델과 다른 특징을 가지고 있었기 때문에(3개의 모델이 필요함, csv 파일을 사용함 등) 파이프라인 내 대부분이 해당 모델을 가정하여 만들어지게 되었습니다. 향후 운영 인력이 다른 과제로 신규 모델을 생성하고 이를 MLOps 시스템에 올리려면, 개발된 MLOps 소스코드 중 많은 부분을 바꿔야 할 것 같습니다.

Sagemaker Pipeline을 굳이 사용할 필요가 있는가에 대한 고민도 있었습니다. Sagemaker Pipeline은 무조건 Sagemaker Step을 잇는 것으로만 구성할 수 있기 때문에, 이번의 AutoML Ver2처럼 Sagemaker API Connector로 구현되지 않은 작업에 대해서는 인스턴스를 이중으로 띄우는 등 자원 낭비가 발생하게 될 가능성이 높습니다. 또한 Sagemaker Pipeline이 범용적인 툴이 아니었기에 개발 중 이슈가 발생했을 경우 직접 github 소스코드를 뜯어보며 해결했고, 향후 운영 인력이 Sagemaker Pipeline 이슈 해결에 어려움을 겪을 수도 있다는 생각이 들었습니다.



## Skills

Python, AWS(Sagemaker, S3)

Go back to [Myeong Hyeon Son](/about/#projects){:.heading.flip-title}
{:.read-more}