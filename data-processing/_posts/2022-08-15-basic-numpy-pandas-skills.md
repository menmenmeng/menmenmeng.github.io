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


## 


## ndarray의 shape 변경

ndarray.reshape(d0, d1, d2, ...)에 대해서는 확실히 기억해 놓아야 한다. ndarray의 shape를 (d0, d1, d2, ...)의 형태로 바꾸어 주는 메소드이다. 데이터 값 누락 없이 차원을 변경하고자 할 때 꼭 필요하며 자주 쓰인다. 여기서 d0, d1, d2 등의 값에 -1을 넣으면 나머지 정해진 차원을 가지고 알아서 계산해서 차원을 만들어 준다. 이를 이용한 특이한 사용 용례만 따로 소개한다.
~~~python
a = np.array(15).reshape(3, 5)

a.reshape(-1)       # (15,)의 shape를 만들어 준다.
a.reshape(-1, 1)    # (15, 1)
a.reshape(-1, 1, 1) # (15, 1, 1) # 이거까지는 잘 안 썼던 듯
~~~
~~~python
''' 결과값
[ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14]
[[ 0]
 [ 1]
 [ 2]
 [ 3]
 [ 4]
 [ 5]
 [ 6]
 [ 7]
 [ 8]
 [ 9]
 [10]
 [11]
 [12]
 [13]
 [14]]
'''
~~~
~~~python
a.T                 # Transpose된 array를 반환한다.
~~~

## 소수 제거 연산(반올림, 내림, 올림)
내림, 올림, 반올림, 그리고 그저 소수부분 제거만 하는 연산을 제공해준다. 주의할 점은 np.round(반올림)은 소수점 이하 몇 번째 자리에서 반올림할 것인지에 대한 parameter를 accept하지만, 내림, 올림, 소수부분 제거 연산은 받지 않는다. 원한다면 custom method를 만들어야 한다.
~~~python
np.floor([1.53, 1.48, -1.53, -1.48])        # 내림
np.ceil([1.53, 1.48, -1.53, -1.48])         # 올림
np.round([1.53, 1.48, -1.53, -1.48], 1)     # 반올림 with 1 decimal
np.round([1.53, 1.48, -1.53, -1.48], 0)     # 반올림 with 0 decimal(정수로 반올림)
np.trunc([1.53, 1.48, -1.53, -1.48])        # 소수부 제거
~~~
~~~python
'''결과값
[ 1.  1. -2. -2.]
[ 2.  2. -1. -1.]
[ 1.5  1.5 -1.5 -1.5]
[ 2.  1. -2. -1.]
[ 1.  1. -1. -1.]
'''
~~~
