---
layout: post
title : "Kakaotalk Clone Coding - CSS"
description: >
    카카오톡 클론코딩 통해 공부한 내용들 정리
sitemap: false
---

HTML, CSS의 기초를 카카오톡 클론코딩을 통해 공부
{:.lead}

0. Table of Contents
{:toc} 

## HTML and CSS

CSS를 어떻게 추가하는가?
1. HTML파일에 HTML과 CSS를 둘 다 넣어준다.
2. 더 전문적이고 추천되는 방법 : CSS와 HTML을 분리시켜라.

지금 할 건 일단 1번임.
실제 웹사이트를 만들 땐 분리할거임.

CSS가 HTML과 같이 있다면 어떻게 써야할까. style이라는 태그를 사용할 거다. 이거는 무조건 ! head안에 있어야 한다. body가 오기 전에..

또 다른 방법은 css 파일을 만드는 것이다.
HTML에는 link태그를 이용해서 styles.css를 가져올 수 있다.

(link를 언제 사용했었나요? HTML에서, 탭 앞에 붙어 있는 icon을 정의해 줄 때 사용했었다. <link rel="shortcut-icon">요렇게 사용했었다.
여기서 rel은 relationship을 뜻함. 어떤

styles.css는 rel="stylesheet"이다.
css를 link에 넣었다면 self close하면 됨.

link는 self closing tag인가?


css를 어느 곳에서든 쓸 수 있다.

css를 작성하는 이론. HTML의 style 태그 안에 사용하는 방법.

웹페이지를 만들 땐 link를 이용해서 분리된 파일들을 연결하기만 하면 된다.

1. open style tag -> css코드를 작성
2. .css 파일을 만들어서, link, rel="stylesheet" 임을 명시해주기.

--> css코드를 어떻게 작성할까용?

## css 코드 작성방법

간단하게 생겼다. 3가지 규칙을 기억하라.

1. css가 하는 일은 point, to an HTML tag.
이 태그는 초록색이다 ~ 같은 식으로. 이걸 가르치는 일을 하는 것 자체를 selector라고 한다.

selector --> 중괄호로, 뭘 말할건지를 묶어준다.

blueTitle(selector) __가리키는 대상__, {
  makecolorblue
  24pxfontsize

  등등...

  이 안에 들어가는 건 __속성(property)__ 
}

HTML의 태그를 가져와서(selector), 내가 원하는 디자인(property)을 적용한다.

property를 외우는 건 말이 안된다. 하지마라!

css는.
속성의 이름을 적고, 콜론을 적고, 값을 쓴다. 그 다음, 세미콜론으로 닫아준다. 이게 css의 문법이다!

css property에는 띄어쓰기가 없다. 밑줄, 슬래시도 없다. 무조건 하이픈으로만.

각 property마다 가질 수 있는 값들이 다를 것이다.

px, em, point, percentage 등 값들의 단위들이 있는데, 그 중 px를 사용할 거다.


css의 모든 속성은 모든 값을 가질 수 있다. 다만 적용되지 않을 거다.. 


## CSS

Cascading은 뭔가요? cascading ... 하방으로 내려가서. 순서대로 진행되는 것.

Cascading style sheet : 위에 있는 코드부터 차례대로 읽는다는 거다. 브라우저는 이렇게 읽는다.

link를 통해 가져오는 것 : external css
HTML에 직접 쓰는 것 : internal css

두 css가 같은 대상을 가리키게 된다면 어떻게 되는가? --> 아래에 있는 게 적용된다는거야. 맨 마지막에 있는 코드가 가장 마지막에 적용, 따라서 external css에는 기본값을 적어주고, internal에 내가 따로 수정하고 싶은 걸 수정하면 된다는거다.

만약 external css를 아래로 옮긴다면, inline css보다 external css가 나중에 실행되므로 external css가 덮어씌우게 된다.

__css는 위에서부터 아래로 가면서 적용된다.__


### Blocks, inlines

모든 속성을 기억할 필요는 없습니다. 어떤 속성이 있는지만 대략 알면 됩니다. 구글링해서 사용하면 됩니다, 나머지는.

text의 모든 속성을 알아볼거고. 지금은 box에 대해 알아보겠습니다.

매우 중요!!!

모든 사이트들에서, 그걸 이루는 모든 요소가 다 box이다. box로 디자인을 하는 것.

important things.. in css

css의 tag가 같은 tag들이 HTML에 많다면, 그 모두에 적용된다. css가. 

++ box는 그 옆에 아무것도 오게 하지 않는다.
box를 만들면 어떤 박스든. div, header, main, section ... footer, article.... 박스 옆에 또 다른 박스가 오지 않는다.

3개의 span. span은 옆에 다른 요소들이 올 수 있다.

**
box는 옆에 다른 요소가 못 온다.
span은 옆에 다른 요소가 올 수 있다.

link는? (a) link도 span 옆에 나올 수 있다. 

span, link는 box가 아닌 것들이다.
paragraph는? paragraph는 옆에 아무것도 올 수 없다.
img는? img도 옆에 올 수 있어요!!!!

2개의 kind. 옆에 아무것도 올 수 없는 box같은 것들과, span등 옆에 올 수 있는 것들.

옆에 다른 요소가 못 오는걸 block
올 수 있는 걸 inline이라고 한다.

block, inline. inline: able to be in the same line.

==> block, inline.외워 외워. 그래야 디자인에 유용하다.

작은 글, 링크, 그림 등등이 모두 .
inline에 해당하는 건 많이 없다.
code도 inline이다.

기억해야 할 것 : 대부분의 box는 block이다. header도. 거의 대부분.
block이 아닌 종류를 기억하는 게 쉽다.
span, a, img. 이게 block이 아닌 대표적인 것.


### block

inline엔 없기도 함.

block의 옆에는 아무것도 올 수 없음, span에는 올수 있음. block을 inline으로 바꾸는 게 가능한가? 또는 반대?

--> 가능으 ㄴ하긴합니다.  css에서 display property를 . inline 또는 block이라고..  바꿔주면. 된답니다. 브라우저는 기본적으로  block을 block으로, inline을 inline으로 보는 기본값이 있고. 이걸 css에서 강제로 바꿔줄 수 있는 것.


block은 높이, 너비를 가질 수 있다.
inline은 그럴 수 없다. inline은 box가 아니다.

box는 특징이 세 가지 있다.

**중요.**
margin, padding, border.

### margin
margin : box 경계의 바깥에 있는 공간.

margin에 값을 두개 주면, 첫 번째는 위아래 / 두 번째는 좌우

4개 주면, top right bottom left. 를 뜻합니다.

### padding
box의 경계로부터 안쪽에 있는 공간.

**같은 태그에 서로 다른 css를 적용하는 법 : id를 사용하면 됩니다..


### class에 다뤄보자.

hello중 일부에는 A속성, 일부에는 B속성을 추가하고 싶어요.

id는 꼭 하나tag당 하나만 있을 수 있다고 했다.
id는 모두 달라야 하기 때문에 ... 

id가 다르지만 다른 것들에게 같은 속성을 넣고 싶다면, 

#id1, #id2, #id3 {
  요런식으로 속성
}

추가해주면 된다.

요소를 골라주면서도, 겹칠 수 있으면 좋겠다. --> 이게 class.

이때는 #을 쓰는대신, .을 사용한다.

.tomato {
  property
}

면, class="tomato"인 HTML 태그를 가져온다는 거.

class는 공유할 수 있다. 한 번에 여러 개의 class를 가질 수도 있어. class를 여러 개 가질 땐, class의 value에 띄어쓰기를 통해 나눠주면서 가면 됨.


## layout.

