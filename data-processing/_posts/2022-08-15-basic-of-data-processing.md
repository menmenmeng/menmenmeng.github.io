---
layout: post
title: "[Data Processing] Basic of Data Processing"
description: >
  Basic data processing methods of numpy and pandas library.
sitemap: false
---

numpy, pandas를 탐험하며 어떤 메소드들을 자주 사용하는지 확인.
{:.lead}

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