---
layout: post
title : "Python - with 구문에 대해."
description: >
    with 구문에 대한 간단한 정리
sitemap: false
---

with 구문에 대한 간단한 정리
{:.lead}

0. Table of Contents
{:toc} 

## with 구문을 언제 사용하는가?

자원을 획득하고, 사용하고, 반납해야 하는 일련의 과정을 하나의 구문 안에서 할 수 있게 해준다.

with 다음에 들어오는 건 특정 class의 객체로, with구문 뒤에 객체가 쓰여지면 객체가 만들어짐 -> 객체 내의 메소드를 사용함 -> 객체가 삭제됨의 세 과정을 거친다.


### text file을 열고 닫는 경우

~~~python
with open(filepath) as f:
  f.write("new textfile is made.")
~~~

open(file, ...) 함수는 python 공식 문서를 보면, "파일 객체를 반환하는 함수"라고 되어 있다. 즉 with 다음에 함수처럼 보이는 게 왔지만, 사실은 파일 객체(자원)을 할당받아 사용하고 닫아주겠다는 뜻


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

Hello() 클래스의 객체 h를 선언하고, h의 메소드들을 사용한 뒤 객체를 닫는다.


### with 구문을 사용하기 위해 필요한 것.

class를 선언할 때, \__enter__ 메소드와 \__exit__ 메소드가 있어야 한다.
~~~python
with [object] as obj:
~~~
라는 코드에서, 가장 처음에 \__enter__메소드를 실행하고, with구문이 전부 끝나면 \__exit__메소드를 실행한다.

파일 객체를 만드는 클래스의 경우, __enter__메소드에서 파일을 open하여 객체로 저장하며, __exit__메소드에서 파일을 close한다.

예시)
~~~python
class File(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
    def __enter__(self):
        return self.file_obj
    def __exit__(self, type, value, trace_back):
        self.file_obj.close()
~~~




참고 - https://ddanggle.gitbooks.io/interpy-kr/content/ch24-context-manager.html