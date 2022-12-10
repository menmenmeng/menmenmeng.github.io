---
layout: post
title : "Kakaotalk Clone Coding - HTML"
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
  - ordered list, uordered list.

- a
  - anchor를 뜻합니다.
  - 다른 웹사이트로 이동하는 방법.
  - h1은 태그 하나로 충분했죠? link(a)는 다른 추가적인 게 필요하다. 바로 우리가 "어디로 가야 하는지!"
  - tag에 추가하는 부가적인 정보를 attributes라고 한다. attributes.!!!
  - a 태그에는 다른 부가적인 정보가 필요한데, 그게 href라는 attribute이다. hyperinc reference.

니꼬, attribute는 아무 태그에나 추가해도 되는거야? 그래 물론이지~ 라고 하시는데?

h1 태그에 pineapple이라는 태그를 넣어도 된다. 그렇지만! 브라우저가 단지 저게 어떤 의미인지 이해해지 못할 뿐이다.

이해하지 못하는 attribute를 쓰면, 브라우저가 이해 못하므로 그냥 무시해버린다.!!!! 중요.

만약 href를 h1태그에 넣으면 어케돼요? 그러나, 클릭은 되지 않는다. 왜?? h1에는 href에는 없는 attribute니까요.

구문을 작성할 때 조심해야 한다. ahref는 잘못된 거고, a href라고 해야 해용. attribute간에는 항상 띄어쓰기를 해주어야 한다. tag이름, attribute간에는. 항상.


a 태그에는 target이라는 attribute있다. 자세한 건 home.html을 살펴보자..
많은 태그들은 많은 attribute들이 있다. 이거는 가르쳐줄 수 없는 거고 작은 것에서부터.

img태그에 대해. img태그는 진짜 중요한 attribute가 있다. 일단 img는 닫아주는 태그가 없다. 이렇게 작성 안한대!!

self_closing tag이기 때문이다. img 사이에는 content가 없다. img는 그냥 img일 뿐이거든!!! content 즉 text가 없기 때문이야.

img는 태그가 아니다. 그냥 img는 img일 뿐이다



### HTML의 문서구조를 작성하는 방법.

태그 : <\!DOCTYPE html> --> 이건 mandatory하다. 
그다음에 <\html><\/html> 를 연다.

이 안에 head, body라는 두 파트에 대한 구조를 설명하는 코드를 짠다.
head - invisible setting
body - contents


head안에.
- title : 탭의 이름

브라우저 상에서 보여야 할 것은 전부, body안에 있어야 한다. 즉 contents는 전부 body에 있어야 함.


넷플릭스를 구글에 쳐 보면, head의 title, meta(content)가 드러난다. 구글이 그 사이트를 크롤링해서 원하는 태그의 것을 가져오는 것.

meta 태그 : Extra data. title, base, link, style 등 사용해서 못하는걸 표현한다.

meta는 두 개의 content, name. 두 개의 attr를 가지고 있다.
__meta charset="utf-8" 이거 되게 중요하다. 코드에 대한 인코딩을 어떻게 할지를 알려준다는 거. 이거는 잊지 말아야 한다__

메타는 항상 self closing 태그이다.

html에도 lang이라는 attr를 통해 "kr"--> html이 구글, Bing 등에서 어떤 언어로 검색되는 게 더 좋은지를 알려주는 거다.

meta description 은 구글이 찾는 메타기 때문에 매우 중요하다.
name=description얘기임.

link rel="shortcut icon" : 탭에서 아이콘을 보여주는 역할.

사이트의 부가적인 정보는 모두 head에 넣는다. 정보를 찾는 역할. 웹사이트의 메타정보!




### form 태그

form 엄청쿨하대. 뭔데이게

1. form의 양식을 만들어줘야 한다.
 - input 태그가 가장 중요하다.
 - mdn에서 input 태그에 들어갈 수 있는 attr를 전부 확인 가능하다.
 - type attr : 어떤 유형의 input을 사용할 것인가? 
 - placeholder attr : 무슨 이름의 input인가. 빈칸일 때 나타나는 문자열



HTML element references 에서 찾을 수 있나 봄.



### 의미가 있는 태그 없는 태그가 있다.

의미가 없는 태그부터.
div : box. 박스하나라고 보면 된다.
일자로 배치해도 상관없지만, 위아래로 두고 싶을 때도 있다. 이럴 경우, 태그를 div 안에다 넣는다. 박스 안에다 넣겠다는거다!!

**box는 양옆에 위치할 수 없다. 무조건 위 아래로만 가능.
--> 의미가 없다는 거다. 

이런 의미없는 태그들이 많지만, 다 읽으면 대강 파악할 수 있다. 의미를

코드 자체로 의미가 부여되어있다.

header 태그 : head랑 다르다. header는 body아넹 있습니다. div를 대체할 수 있고, 완전 똑같은 기능을 한다. -->그러나 이걸 쓰는 이유는, 코드를 봤을 때 website의 header임을 바로 알게 될 수 있기 때문..

website는 id와 함께, div를 엄청많이 썼다. 지금은 header라는 것만 쓰면, header임을 알 수 있다.

main : <div id="main"> 도 괜찮지만, main을 사용하는 게 더 좋다고.

footer도 마찬가지. header랑 비슷함..

paragraph : <p>

div, header, main, footer : 모두 똑같은 기능을 하지만, website를 이해하기 더 쉽게 만들기 위해 이걸 만드는 거다.
==> semantic HTML이다. 이게

span도 비슷한 느낌으로, short text를 위해 존재한다.
p는 paragraph를 위해 존재.
이 둘은 아무런 의미는 없고, 기능상에도 다르지 않다.
그러나 우리는 적절한 상황에 적절한 semantic을 가져오는 것들을 사용해서 만든다는 거다.

website를 더 쉽게 이해하기 위해, --> semantic HTML을 사용하는 것이다.

div, span에는 의미가 없지만. header, main, address는 다 의미가 있는 것 . semantic..


**class name 라는 attribute도 중요하다. css에서 사용할 것.


