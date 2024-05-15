---
layout: post
title: "node.js와 flask에서의 서버 바인딩"
description: >
  -
sitemap: false
hide_last_modified: true
---


0. Table of Contents
{:toc}

## 개요

docker container 안에서 node.js로 만들어진 앱을 실행한 후, 로컬 머신에서 접속하면 접속이 잘 됐다. 그런데, 같은 앱을 flask로 만들고 container를 실행하니, 로컬 머신에서 접속이 안 된다. 이유를 찾아봤더니 node.js와 flask 간에 다른 점이 조금 있었다.

## 배경 지식

바인딩이란? 클라이언트 컴퓨터가 서버 컴퓨터로 접속이 된 상태를 바인딩이라고 한다. 즉 "ip주소를 바인딩한다"라는 말은, 서버에 접속 가능한 클라이언트의 ip주소를 명시한다... 와 같은 말로 보면 되지 않을까.

## 본문

node.js에서는 소스코드 내의 `app.listen(80)` 부분에 ip주소를 명시하지 않으면 기본값으로 0.0.0.0이 설정된다. 즉 node.js에서 바인딩 주소에 대해 특별한 설정을 하지 않으면, 모든 ip주소에 대해 바인딩된다. 모든 클라이언트가 서버와 연결 가능하다는 것이다. 만약 127.0.0.1, 즉 로컬 컴퓨터(컨테이너가 인식하는)에서만 연결 가능하도록 만들고 싶으면 `app.listen(80, '127.0.0.1')` 처럼 ip주소를 명시해야 한다.

flask는 shell에서 flask 앱 실행 시 `flask run --host "x.x.x.x" --port $PORT` 와 같은 식으로, 바인딩 ip 및 port를 명시한다. 만약 option을 주지 않는다면, 즉 ip주소를 명시하지 않는다면 flask는 127.0.0.1에 대해서 바인딩된다. 즉 클라이언트가 로컬 컴퓨터가 아니면 접속할 수 없게 된다.

컨테이너는 로컬 머신에서 실행되지만, 로컬 머신과 완전히 다른 독립된 환경을 가지고 있다. 컨테이너 내에서 로컬 컴퓨터란, 컨테이너 그 자체이며 컨테이너 입장에서 컨테이너를 실행한 컴퓨터(진짜 내 눈 앞에 있는)는 외부의 클라이언트이다. 따라서 flask 앱 실행 시 `--host "0.0.0.0"` 옵션을 추가해야 한다.


## 출처 및 참고 자료

[StackOverflow](https://stackoverflow.com/questions/33953447/express-app-server-listen-all-interfaces-instead-of-localhost-only)