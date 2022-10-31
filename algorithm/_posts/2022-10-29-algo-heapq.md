---
layout: post
title: "[Python] heapq"
description: >
  heapq 사용법에 대해.
sitemap: false
hide_last_modified: true
---

파이썬에서 우선순위 큐를 구현해 놓은 라이브러리. 사용 방법에 대해 정리함
{:.lead}

0. Table of Contents
{:toc}


## 개요

이진 트리(binary tree) 기반의 최소 힙(min heap) 자료구조 제공.

## 사용법

주의 : heap이라는 자료구조가 따로 있는 것이 아님! 우선순위 힙의 삽입/삭제 방식대로 list에 삽입/삭제를 하는 것일 뿐이다.

주로 사용하는 메소드 3개
- heapq.heappush
- heapq.heappop
- heapq.heapify


### heapq.heappush

list에 우선순위 큐 방식대로 요소를 삽입함

~~~python
import heapq

heap = [] # 빈 리스트 --> heap 자료구조처럼 사용할 놈임.

heapq.heappush(heap, 4) # heap으로 사용될 리스트에 4를 삽입
heapq.heappush(heap, 1) # 1 삽입
heapq.heappush(heap, 7) # 7 삽입
heapq.heappush(heap, 3) # 3 삽입

print(heap)
~~~
~~~python
# result
[1, 3, 7, 4]
~~~

### heapq.heappop

list에 우선순위 큐 방식대로 요소를 제거

~~~python
import heapq

heap = [1, 3, 7, 4] # 위에서 만든 heap

heapq.heappop(heap) # heap으로 사용되는 list에서 가장 우선순위가 높은(key값이 작은) 값을 제거함.
# list.pop처럼 작동됨. heap안에서는 요소가 제거되며, 제거되는 요소를 return함
~~~

~~~python
# result
1
~~~

### heapq.heapify

heap과 관련없는 list를 heap 구조를 가지도록 바꿔 줌. heappush를 여러 번 해서 heap으로 만드는 것보다 더 효율성 좋다.

heappush 여러 번 --> O(nlog(n))

heapify --> O(n) # 맨 마지막 노드들을 heapify안해도 정렬할 수 있는 방법이 있음.. 자세한 건 heapify를 검색해보기.

~~~python
import heapq

heap = [4, 1, 7, 3, 8, 5]
heapq.heapify(heap) # list.sort()처럼 지금 존재하는 리스트를 정렬하는 작업을 수행. 새로운 리스트를 return하지 않는다. 주의하길.
print(heap)
~~~

~~~python
# result
[1, 3, 5, 4, 8, 7]
~~~


### (번외) Max heap을 만드는 방법

파이썬은 최소 힙, 즉 최솟값을 가지는 요소가 가장 우선순위가 높은 힙만 만들 줄 안다.
최대 힙을 만들기 위해서는 편법을 사용해야 함.

heapq는, 2개 이상의 요소가 묶여서 tuple로 들어갈 경우, 들어가는 tuple의 가장 첫 번째 요소를 기준으로 min heap을 만든다. 그러므로 max heap을 만드려면, 가지고 있는 요소들을 num이라고 하면

(-num, num) <-- 이런 형태를 가진 리스트로 만들어준 다음에 heapify를 해주고, heapify를 할 때 [1]의 인덱스로 인덱싱해주면 된다.

~~~python
import heapq

nums = [4, 1, 7, 3, 8, 5]
heap = [(-num, num) for num in nums]

heapq.heapify(heap)
print(heap)
~~~

~~~python
# result
[(-8, 8), (-4, 4), (-7, 7), (-3, 3), (-1, 1), (-5, 5)]
~~~





## 개념

### 우선순위 큐

우선순위 개념을 Queue에 도입한 자료구조. 스택, 큐, 우선순위 큐의 "요소가 삭제될 때"의 작동방식을 비교함으로써 정의할 수 있다.

|**자료구조**|**삭제되는 요소**|
|:-------:|:-------:|
|**스택(Stack)**|가장 최근에 들어온 데이터|
|**큐(Queue)**|가장 먼저 들어온 데이터|
|**우선순위 큐(Priority Queue)**|가장 우선순위가 높은 데이터|

각 자료구조의 정의
{:.figure}

우선순위 큐는 배열, 연결 리스트, 힙으로 구현 가능한데 힙으로 구현하는 것이 가장 효율적이라고 한다.

### 이진 트리

각각의 노드가 최대 2개의 자식 노드를 가지는 트리 자료 구조.

### 힙

우선순위 큐를 위해 만들어진, 완전 이진 트리의 형태를 가진 자료구조. 여러 개의 값들 중에서 최댓값/최솟값을 빠르게 찾아내도록 만들어진 구조이다.
힙은 일종의 반정렬 상태(느슨한 정렬 상태)를 유지한다.
- 큰 값이 상위 레벨에, 작은 값이 하위 레벨이 있다. 즉, 부모 노드가 항상 자식 노드보다 더 크다.(부모-자식 간 연결된 노드에만 해당)
- 자식 노드 간에는 상/하위 관계가 없다.
- 힙 트리는 중복된 값을 허용한다.

### 힙의 종류

1. 최대 힙
 - 부모 노드의 키 값이 자식 노드의 키 값보다 크거나 같은 완전 이진 트리
2. 최소 힙
 - 부모 노드의 키 값이 자식 노드의 키 값보다 작거나 같은 완전 이진 트리.


### 힙의 구현

배열을 이용해서 힙을 구현하는 경우가 보통. 구현을 쉽게 하기 위해, 첫 번째 인덱스인 0은 사용되지 않는다고 한다.

힙에서의 부모 노드와 자식 노드와의 관계
- 왼쪽 자식의 인덱스 = (부모 인덱스) * 2
- 오른쪽 자식 인덱스 = (부모 인덱스) * 2 + 1
- 부모 인덱스 = (자식 인덱스)//2


#### 삽입

가장 마지막 인덱스에 요소를 집어넣고, 그 요소를 기준으로 위 방향 heapify를 진행함(부모-자식 간 크기 비교 후 교환)

#### 삭제

가장 첫 인덱스의 요소를 삭제하고, 가장 마지막 인덱스의 요소를 가장 첫 인덱스에 대입. 이후 가장 첫 인덱스의 요소를 기준으로 아래 방향 heapify를 진행함

#### 힙 구성

1. 비어 있는 힙에 요소를 차례대로 insert연산을 수행함. 계산복잡도 - O(nlog(n))

2. O(n)의 방법 --> 다시 확인...

