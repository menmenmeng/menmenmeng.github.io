---
layout: post
title: "[Data] Basic numpy, pandas skills"
description: >
  Basic data processing methods and attributes of numpy and pandas library.
sitemap: false
---

numpy와 pandas에서 기본적으로 사용되는 method와 attributes
{:.lead}
정해진 주제는 없고 전반적으로 자주 쓰이는 numpy와 pandas의 메소드 및 속성을 정리했다(사실 내가 자꾸 까먹어서 기록해 두려고 함).

쓸만한 메소드나 속성을 발견할 때마다 추가될 예정

0. Table of Contents
{:toc}

## numpy

자주 사용하며 꼭 필요한 것들만 모았다.
{:.lead}

### ndarray의 속성값들

데이터가 어떤 모양인지를 개괄적으로 파악하기 위해 사용하기 좋은 것들
~~~python
a = np.array(15).reshape(3, 5)

a.shape     # (3, 5)
a.ndim      # 2
a.dtype     # int64 # ndarray의 모든 요소는 공통된 dtype을 가지도록 되어 있다.
a.itemsize  # 8 # 각 요소가 얼마의 메모리를 차지하고 있는지를 바이트로 표시. int64이므로 64비트(==8바이트)
a.size      # 15 # 몇 개 들어 있나.
type(a)     # <class 'numpy.ndarray'>
~~~


### ndarray의 생성

데이터(리스트)를 직접적으로 넣어주어 ndarray를 만들 수도 있지만, shape를 지정하고 임의의 값을 채워넣어 ndarray를 생성할 수도 있다. 아래의 코드 블럭은 ndim과 shape를 지정하여 그 모양의 ndarray를 만드는 방법이다. 어떤 값들로 채워지는지에 따라 메소드가 구분되어 있다.
~~~python
np.empty((d0, d1, ...))     # 초기화되지 않은 값으로 채우기. (!= random)
np.zeros((d0, d1, ...))     # 값을 0으로 채우기
np.ones((d0, d1, ...))      # 값을 1로 채우기
~~~

아래는 등간격의 데이터를 ndarray로 생성하고 싶을 때 사용하는 메소드이다. 그래프의 x축에 해당되는 데이터를 만들 때 주로 사용했었고, 실제로 데이터 분석을 위해서는 잘 사용하지 않는 것 같다.
~~~python
np.arange(10, 30, 5)    # params : first, last, period. [first, last) 안에서 5의 간격으로 올라감
np.linspace(0, 4, 5)    # params : first, last, size. [first, last] 안에서 5개의 숫자를 만들어냄
~~~

특정 ndarray와 같은 shape를 가진 임의의 ndarray를 생성하고 싶다면, 다음과 같은 메소드를 사용할 수 있다.
~~~python
a = np.array(15).reshape(3, 5)
np.zeros_like(a)    # a의 shape와 동일한 shape를 가지며 값이 0으로 초기화된 ndarray 반환
np.ones_like(a)     # a의 shape와 동일한 shape를 가지며 값이 1로 초기화된 ndarray 반환
~~~




### ndarray의 여러 연산 메소드들

일반적인 연산, 예를 들어 특정 숫자 더하기나 빼기, 또는 log를 취하거나 제곱을 하거나 루트를 취하는 등... 대부분의 연산은 element wise(element by element)로 이루어진다. 숫자의 각각의 요소에 연산이 이루어진다.
범용 연산 관련, 어떤 연산들이 있는지는 [available-ufunc][available-ufunc-numpy] 에서 확인.

집계함수(sum, min, max 등)는 위와는 다르다. 통계를 낸다는 관점에서 사용되는 연산이다. 여기서 집계함수가 받는 parameter중 **axis**는 매우 매우 중요하니 잘 이해해야 한다.

주로 사용하는 2차원 array에 대해, axis=0, axis=1은 다음과 같이 정해진다.


![Image](/assets/img/myown/numpy_axis_0.jpg){:.lead loading="lazy"}
axis 번호의 기준
{:.figure}

np.sum을 예시로 들면, axis에 따른 함수의 결과값은 다음과 같이 나타난다.
![Image](/assets/img/myown/numpy_axis_2.jpg)
{:.lead width="400" loading="lazy"}


numpy의 집계함수 안에 들어가는 axis파라미터는 아래와 같이 생각하면 조금 이해가 쉽다.

> np.aggr(axis=n) : axis=n의 index를 변형시키는 연산.
> 즉 axis=n을 제외한 다른 axis에는 아무런 변화를 주지 않는 연산.


자주 사용하는 집계함수는 다음과 같다.
- np.sum()
- np.min()
- np.max()
- np.argmin() # min값의 요소 index를 반환
- np.argmax() # max값의 요소 index를 반환
- np.cumsum() # 모든 요소의 누적합


### ndarray의 shape 변경

ndarray.reshape(d0, d1, d2, ...)에 대해서는 확실히 기억해 놓아야 한다. ndarray의 shape를 (d0, d1, d2, ...)의 형태로 바꾸어 주는 메소드이다. ndarray의 차원을 변경하고자 할 때 꼭 필요하며 자주 쓰인다. 여기서 d0, d1, d2 등의 값에 -1을 넣으면 나머지의 지정된 차원을 가지고 알아서 계산해서 차원을 만들어 준다. 이를 이용한 특이한 사용 용례만 따로 소개한다.
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

ndarray.T:

아래는 transpose된 ndarray를 반환하는 방법이다.
~~~python
a.T                 # Transpose된 array를 반환한다.
~~~

### 소수 제거 연산(반올림, 내림, 올림)

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

그 외 resize(), ravel()과 같은 함수도 있지만 대부분 reshape 선에서 정리됨.


### 데이터 쌓기(concatenate)

np.vstack(), np.hstack()을 통해 두 개 데이터를 concat할 수 있다.
- np.vstack() : axis=0기준으로 쌓음. vertical stack, 즉 위 아래로 합친다. -> axis=0
- np.hstack() : axis=1기준으로 쌓음. horizontal stack.

두 메소드 모두 numpy array로 이루어진 튜플 형태, 즉 (arr1, arr2, ..., arr_n)의 input을 받아서 array를 방향에 맞게 합쳐 준다. vsplit(), hsplit() 메소드(이름에서 드러나듯이 stack 함수의 역연산)도 있지만 이 메소드들은 slicing으로 충분히 커버가 가능하니 굳이 알아둘 필요는 없을 듯.


### 그 외
브로드캐스팅, 인덱싱, boolean mask를 이용한 인덱싱은 계속해서 리마인드



## pandas

index, column으로 이루어진, 비정형 데이터를 python상에서 저장하고 다루기에 가장 편리한 라이브러리
{:.lead}




[available-ufunc-numpy]:https://numpy.org/doc/stable/reference/ufuncs.html