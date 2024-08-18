---
layout: page
title: "앱 푸시 시스템 고도화 (Ongoing)"
description: |
  2024\.05 ~ 2024\.07  
  LG CNS에서 운영하는 앱 푸시 시스템에 타겟팅 시스템을 추가하여 고도화하였습니다.
hide_description: false
sitemap: false
---

0. Table of Contents
{:toc}


## Overview

LG CNS 내부 사업인 "앱 푸시 광고 시스템"에서 조건에 맞는 ADID를 타겟팅하여 광고를 푸시하는 타겟 마케팅 시스템을 구축하는 중입니다. 기존 시스템은 Java 및 Spring 기반의 LG CNS 자체 프레임워크인 Devon을 바탕으로 구축되어 있습니다. DE파트 리딩을 맡아, 운영에 용이하도록 해당 프레임워크를 기반으로 인프라, 테이블 및 ETL 프로세스를 설계/구축하고 있습니다. 

GCP BigQuery 내에 대용량 로그 테이블 및 ADID를 집계 기준으로 하는 Feature 테이블을 생성하는 ETL 파이프라인을 구축하고, 앱 푸시 발송 시 해당 테이블을 참조하도록 기존 시스템의 웹 및 배치 소스를 신규 개발/수정 중에 있습니다.



## Process




## Meaning




## Skills

Java, SQL, GCP(BigQuery, Looker Studio)

Go back to [Myeong Hyeon Son](/about/#projects){:.heading.flip-title}
{:.read-more}