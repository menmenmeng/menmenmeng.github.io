---
layout: post
title : "Python - with 구문에 대해."
description: >
    with 구문에 대한 간단한 정리
sitemap: false
---

0. Table of Contents
{:toc} 

## 개요

자원을 획득하고, 사용하고, 반납해야 하는 일련의 과정을 하나의 구문 안에서 할 수 있게 해주는 게 with 구문이다. 사실 `with open(txtfile) ...`과 같은 구문을 통해서 얕게는 알고 있었지만, 실시간 트레이더를 만들기 위해 binance futures connector의 코드를 뜯어보는 과정에서 with 구문을 이해하지 못하고 있었다는 사실에 충격을 먹고 알아보았다.


## 본문

with 다음에 나오는 건 특정 class의 객체로, with 구문 뒤에 객체가 쓰여지면 다음과 같은 과정을 거친다.

1. 객체가 생성됨
2. 객체 내의 메소드를 사용함
3. 객체가 삭제됨

객체 생성, 실행, 삭제가 원큐에 이뤄지는 아주 효율적인 방법이라고 할 수 있다. 아래는 with 구문의 사용 예시에 대해 정리한 것이다.


### text file을 열고 닫는 경우

~~~python
with open(filepath) as f:
  f.write("new textfile is made.")
~~~

`open(file, ...)` 함수는 python 공식 문서를 보면, __"파일 객체를 반환하는 함수"__ 라고 되어 있다. 즉 with 다음에 함수처럼 보이는 게 왔지만, 사실은 이 함수 자체가 파일 객체로서 작동하게 되는 것이고 위에서 말한 것과 마찬가지로 객체를 할당받아 사용하고 닫아주겠다는 뜻이란 걸 알 수 있다.


### custom class 예시

~~~python
class Hello:
    def __enter__(self):
        # 자원을 가져오거나 만든다.(file, class-object..)
        print('enter...')
        return self # 반환값이 있어야 VARIABLE를 블록 내에서 사용할 수 있다
        
    def sayHello(self, name):
        # 자원을 사용한다. ex) 인사한다
        print('hello ' + name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 마지막 처리를 한다(자원반납 등)
        print('exit...')


with Hello() as h:
    h.sayHello('obama')
    h.sayHello('trump')
~~~

`Hello`라는 클래스를 만들고, with구문에서 `Hello` 클래스의 객체를 `h`라는 이름으로 선언하여 `h`의 메소드를 사용한 뒤 객체를 닫는 코드이다.


### with 구문을 사용하기 위해 필요한 것.

class를 선언할 때 with 구문이 작동되는 형태로 만드려면 `__enter__` 메소드와 `__exit__` 메소드를 class의 코드에 포함시켜야 한다.

~~~python
with [object] as obj:
~~~

위의 코드는 사실, with 구문의 시작에 `object`객체의 `__enter__`메소드를 실행하고, with 구문의 끝에 `__exit__`메소드를 실행하는 과정이 숨겨져 있다. 일례로 파일 객체를 만드는 클래스의 경우, `__enter__` 메소드에서 파일을 open하고 이를 객체로 저장하며, `__exit__` 메소드에서 파일을 닫는다.

~~~python
class File(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
    def __enter__(self):
        return self.file_obj
    def __exit__(self, type, value, trace_back):
        self.file_obj.close()
~~~

File 클래스의 `__enter__`, `__exit__` 메소드에 대해.
{:.figcaption}


## 출처 및 참고 자료

[Context Manager](https://ddanggle.gitbooks.io/interpy-kr/content/ch24-context-manager.html)