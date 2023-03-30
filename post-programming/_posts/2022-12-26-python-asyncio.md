---
layout: post
title: "Python - 비동기 함수 라이브러리 asyncio"
description: >
  websocket을 열 수 있는 파이썬 라이브러리 asyncio에 대해 (아주 살짝) 공부해 봄
sitemap: false
hide_last_modified: true
---


0. Table of Contents
{:toc}

## 개요

binance API를 활용한 실시간 트레이더를 만들 때, binance에서 공식적으로 제공하고 있는 binance futures connector 등, binance 트레이딩에 최적화된 라이브러리가 아니라 혼자 힘으로 모든 걸 만들어 보고 싶어서 공부했던 것.

결론적으로 말하자면 혼자서 모든 걸 다 만드는 건 말도 안 되는 일이었다. 깊이 공부하진 않았고, 적당한 개념만 공부하고 넘어갔다.

## 배경 지식

- 

## 본문

- 메인루틴, 서브루틴, 코루틴

함께 실행되는 함수들 간의 관계를 나타내는 용어들. 서브루틴은 메인이 되는 함수 내에서 호출되는 또 다른 함수를 말한다. 파이썬 프로그래밍 할 때 매우 매우매우 자주 보는 형태이고, 서브루틴은 메인루틴에 종속된 관계다. 메인루틴이 본인의 일을 진행하다가 서브루틴을 호출하고, 호출된 서브루틴은 본인의 역할을 다하고 나서 다시 메인루틴에 주도권을 넘겨준다. 서브루틴이 메인루틴을 호출하지는 않는다.

![subroutine](/assets/img/myown/subroutine.png)

반면 코루틴은 메인루틴과 동등한 관계에서 실행된다. 메인루틴 안에 서브루틴을 포함시키는 방식이 아니라, 한 스레드에서 메인루틴과 코루틴이 함께 작동한다. 실시간 트레이딩 또한 이런 방식으로 진행되어야 한다. 왜냐하면, 데이터를 받아 오는 함수와 매매를 실행하는 함수가 어느 하나에 종속되지 않고, 지속적으로 주도권을 서로에게 넘겨주며 작동해야 하기 때문이다.

![coroutine](/assets/img/myown/coroutine.png)


- asyncio 기반의 코루틴

파이썬으로 코루틴을 만드는 방법에는 두 가지 방법이 있다. 1) 제너레이터 기반의 코루틴, 2) asyncio 기반의 코루틴이다. 제너레이터는 yield 구문을 활용해서, 메인 루틴을 돌리다가 다른 루틴을 돌리는 제동 장치를 만들 수 있다.

asyncio는 비동기 프로그래밍을 위한 파이썬 라이브러리이며, 이 라이브러리를 활용해서 코루틴을 만들 수 있다. 


- asyncio 기반 코루틴 생성 방법

코루틴 객체는 `async def main()`을 활용해서 함수 선언하듯이 선언할 수 있다.  
짜여진 main() 함수를 `asyncio.run(main())`을 활용해서 실행하면 새로운 event loop을 만듦과 동시에, 코루틴 객체인 `main`을 실행한다.  

`await`명령을 중간에 만나면, event loop는 거기서 실행을 suspent하고 await 뒤에 나오는 객체의 값을 받을 때까지 기다린다. (`await myCoroutine()`)  
`await`뒤의 객체가 값을 리턴하면, 그 때 다시 event loop를 resume한다.  

`await` 뒤에 나올 수 있는 객체를 awaitable 객체라고 하며, 코루틴, 태스크, 퓨처가 있다.  

- 코루틴 : async def를 활용해서 만들어진 함수
- 태스크 : `asyncio.create_task(main())`과 같은 형태로 코루틴을 create_task로 감싸서 만드는 객체. 비동기 실행 가능한 객체가 된다고 함.
- 퓨처 : ---아직 잘 모르겠음.


## 결론

이 정도만 공부하고 말았다. 기본적인 asyncio의 사용법은 익혔지만, 혼자 힘으로 binance websocket stream을 여는 코드를 만들기엔 너무 깊이 있는 내용인 것 같아서 보류했다.

사실 앞으로 이걸 더 공부할지도 잘 모르겠음...


## 출처 및 참고 자료

[tistory 블로그 중](https://nowonbun.tistory.com/674)  
[코딩도장1](https://dojang.io/mod/page/view.php?id=2469)  
[코딩도장2](https://dojang.io/mod/page/view.php?id=2418)  