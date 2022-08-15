---
layout: post
title: "[Data] Basic numpy, pandas skills"
description: >
  Basic data processing methods of numpy and pandas library.
sitemap: false
---

numpy와 pandas에서 기본적으로 사용되는 method와 인스턴스 변수들
{:.lead}
정해진 주제 없이, 전반적으로 자주 쓰이는 numpy와 pandas의 메소드들을 정리했다.

0. Table of Contents
{:toc}


## ndarray의 속성값들

데이터가 어떤 모양인지를 개괄적으로 파악하기 위해 사용하기 좋은 메소드 또는 인스턴스 변수들.
~~~python
a = np.array(15).reshape(3, 5)

a.shape     # (3, 5)
a.ndim      # 2
a.dtype     # int64 # ndarray의 모든 요소는 공통된 dtype을 가지도록 되어 있다.
a.itemsize  # 8 # 각 요소가 얼마의 메모리를 차지하고 있는지를 바이트로 표시. int64이므로 64비트(==8바이트)
a.size      # 15 # 몇 개 들어 있나.
type(a)     # <class 'numpy.ndarray'>
~~~

## ndarray의 생성

데이터(리스트)를 직접적으로 넣어주어 만드는 방법도 있지만, 지정한 모양에 랜덤한 값(또는 초기화된 값)을 채워넣어 생성하는 메소드도 존재한다. 아래의 코드 블럭은 ndim과 shape를 정해두고 그 정해진 모양대로 ndarray를 만드는 방법이다.
~~~python
np.empty((d0, d1, ...))     # 초기화되지 않은 값으로 채우기. (!= random)
np.zeros((d0, d1, ...))     # 0으로 채우기
np.ones((d0, d1, ...))      # 1로 채우기
~~~

데이터를 등간격으로 생성하고 싶을 때 사용하는 메소드도 있다. 지금까지 봐왔던 사용처는 그래프 그릴 때 x축에 해당되는 index값들을 생성할 때 사용하는 것 정도..?
~~~python
np.arange(10, 30, 5)    # params : first, last, period. [first, last) 안에서 5의 간격으로 올라감
np.linspace(0, 4, 5)    # params : first, last, size. [first, last] 안에서 5개의 숫자를 만들어냄
~~~