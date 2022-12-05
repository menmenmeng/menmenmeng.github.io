---
layout: post
title : "Kakaotalk Clone Coding"
description: >
    카카오톡 클론코딩 통해 공부한 내용들 정리
sitemap: false
---

HTML, CSS의 기초를 카카오톡 클론코딩을 통해 공부
{:.lead}

0. Table of Contents
{:toc}  

HTML, CSS에 대해 배움.

## 웹사이트는 어떻게 만들어지나?

굉장히 역동적으로, interactive하게 만들어질 수도 있지만. 반면 심플하게, title, text, image만으로 이루어지는 경우도 많다.

interactive? YouTube, Netflix같은 것들이 그 예시. 반면 Times같은 뉴스페이퍼의 경우는 simple하게 만들어져 있음. title, text, image..

View -> Developer -> View source.

Netflix, YouTube, Times .. just text !  넷플릭스나 유튜브는 조금 더 어려운 Text지만 결국엔 다 text일 뿐이다.

브라우저가 코드를 받고, 코드를 구현해 준다.

무슨 텍스트를, 어디다 넣어야 하는지. 그걸 우리가 공부해야할 것.

어떤 종류의 텍스트인가? 

## 웹사이트는 3종류의 텍스트로 이루어져 있다.

최대 3종류, 최소 2종류라고 한다. 텍스트가 아니라! 이제부터 언어라고 한다.

HTML, CSS, Javascript 이렇게 3개 언어만이 웹사이트를 만든다. 우리가 해야 할 건 이 세 개의 언어를 공부하는 것 뿐.

HTML만드는 건 쉬워. CSS는 연습해야 하고, javascript는 공부해야 하고... 가장 중요한 건 HTML, CSS를 잘 다루게 되는 것이다.

## HTML부터 배워보자!

Hypertext Markup Language. : content. title, image, text, link, .... click, ... title, ... image description, .... sidebar, date, ...

이 모든 것들이 content다.

__HTML은 브라우저에게 웹사이트의 content가 어떻게 구성되어 있는지 설명할 때 사용한다.__

title이 뭐고, sidebar, navigation, header, .... 모든 것들. HTML만이 할 수 있다. 브라우저에게, content가 어떻게 구성되어 있는지를 설명하는 것.

## CSS

Cascading Style Sheets. CSS는 HTML과 같이 써야 한다. with HTML! CSS를 따로 사용하거나, HTML만 따로 사용하지 않는다.

CSS는 뭘까? 브라우저에게 웹사이트가 어떻게 보여야 하는지 가르쳐 준다. 즉 디자인 !!

HTML = contents.

CSS = how the content look like.


이 컨텐츠는 4개의 컬럼을 차지해야 한다... 이런 걸 알려줌. 이게 디자인이다. visual things, 색상, 사이즈 같은 것들.


## Javascript

웹사이트를 똑똑하게 만들어준다. interactivity. 이게 웹사이트의 뇌이다.

모든 웹사이트에서 뇌가 필요한 것은 아니다. animation은 배울 것. 모바일에서 볼 수 있게도 만들 것. 그렇지만 javascript는 아니다. interactivity, 뇌. 이게 javascript

이번에는 그냥! HTML, CSS만 공부할 것.



## HTML

브라우저는 컨텐츠를 표시한다는 것을 보여주려 한다.

코드를 규칙대로 작성해야. 브라우저 내에 잘 보인다.

contents에 태그를 단다. 이게 곧!!!! HTML의 문법이다.
like...

<\food>김치<\/food> 라고 하면, HTML은 "김치"에 달린 태그 food를 보고 '아, "김치"는 음식이구나... 한다는 거죠..


무슨 태그를, 어디에 넣어야 하는지를 배운다면 웹사이트를 배울 수 있다.

__tag는 전부 기억할 필요가 없다. tag가 엄청 많으니까.. 대신 어떻게 작동하는지를 알면 된다.__


### 자주 사용하는 tag들.
[home.html](C:\TIL\Web\kokoa-clone\home.html)

- h1, h2, h3, h4, h5, h6
  - header. 제목을 나타낸다.
  - h7부턴 존재하지 않음. h1~h6, 6 depth가 디폴트로 쓸 수 있는 최대치
- ol, ul