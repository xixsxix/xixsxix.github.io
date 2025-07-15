---
title: AutoHotkey Shortcut System
date: '"2025-04-09 15:00:51 +0900"'
categories:
  - AutoHotkey
tags:
  - nas
  - 나스
  - script
  - 스크립트
  - 자동화
  - 리눅스
  - linux
  - 서버관리
  - 서버
  - synology
  - autohotkey
  - shortcut
pin: false
comments: "true"
image: /assets/img/linux-title03.webp
---
## AutoHotkey

요즘은 오토핫키(AutoHotkey)를 모르는 유저는 거의 없지 않을까? 출시된지 벌써 20년이 넘었으니 참 오랫동안 사랑받는 프로그램이다. 한동안 맥을 주로 사용하느라 오토핫키를 잊고 있었는데 이제 윈도우를 이용하게 되어 조금씩 만지고 있다. 프로그램을 설치하려고 사이트에 들어가니 v2.0과 v1.1이 있길래 무심코 2.0을 다운받았다. 그리고 **ChatGPT**와 코드 제작을 시작했다. 

이전에 가지고 있던 .ahk에서 오류가 발생하기 시작했다. 오류를 잡기 위해서는 v2.0에 맞는 함수로 변경을 해야 한다. 벌써 머리가 아파온다. 그러나 나에게는 **ChatGPT**가 있지 않는가. 그런데 이녀석도 버벅거린다. 1.1로 제안하고 오류나면 미안하단다. 미쳐버리겠다. 

**ChatGPT**는 내가 생각하는 것 처럼 움직이지 않는다. 똑똑하고 아는 건 많은데, 질문을 잘 해야 정답을 찾을 수 있다. 그리고 이전에 질문했던 모든 것을 기억하고 있다. 그래서 처음부터 다시 시작하고 싶어도 예전에 질문하고 답했던 결과를 합쳐서 계속 시도한다. 이럴때는 새 창으로 바꾸어 질문해야 오류를 피할 수 있다.

---

## 정의

이제 정의를 해야 한다. 평소에 잘 사용하는 프로그램을 한번의 단축키로 일괄 실행할 것이다. 그 이전에 일단 한 개의 코드를 성공해야 한다. 그래야 다음 프로그램을 시작할 수 있기 때문이다. 처음부터 복잡하게 시작하면 어디가 잘못되었는지 도무지 찾을 수가 없다.

1. 크롬을 실행한다.
2. 이미 크롬이 실행되어 있으면 새탭을 연다. `^t`
3. 주소창을 선택한다.  `^l`
4. 주소를 입력하고 `{Enter}`를 누른다.

이렇게 하면 원하는 주소로 들어간다. 이렇게 단순한 건 한번에 성공할 줄 알았다. 좌절이다.
크롬 인식을 못한다. 

---

AHK가 크롬을 인식하는 방법은 4가지가 있다. 
1. **ahk_class Chrome_WidgetWin_1** : 열려있는 크롬의 첫번째 창
2. **ahk_exe chrome.exe** : 실제 크롬의 실행파일
3. **ahk_pid** : 고유의 PID, 실행할 때 마다 바뀐다.
4. **ahk_id** : 고유의 ID, 실행할 때 마다 바뀐다.

3,  4 번의 방법은 불편하다. PID를 자동을 찾을 수 있는 함수는 분명 존재한다. 그러나 그렇게 까지 해서 찾을 필요는 없다. 간단한 1, 2번이 있으니까. 1번은 열려있는 창이 여러개 일 경우 첫번째 창을 선택한다.
```
WinActivate, ahk_class Chrome_WidgetWin_1
WinWaitActive, ahk_class Chrome_WidgetWin_1
```

 2번도 마찬가지다. 
```
WinActivate, Google Chrome
WinWaitActive, Google Chrome
```

그리고 주소창에 "https://www.chatgpt.com" 를 입력하고 엔터를 치면 그 주소로 이동하게 한다. 아 그런데 문제가 생겼다. 주소창에 한글로 입력이 되는 것이다. **ㅗㅅ센://ㅈㅈㅈ.촘ㅅ헷.채ㅡ/** 으로 말이다. 여기에 코드를 하나 더 입력해야 한다. 무조건 영문으로 입력하도록 말이다.
```
SetInputLanguage("A0000409")  ; 영어 (미국) IME로 고정

SetInputLanguage(LangID) {
    WinGet, hwnd, ID, A
    PostMessage, 0x50, 0, %LangID%, , ahk_id %hwnd%
}
```

일이 점점 커지고 있다. 문제는 저렇게 해도 상황이 바뀌지 않는다는 것이다. 다른 생각을 해야 한다. 한글때문에 직접 입력이 되지 않는다면 주소를 클립보드에 복사해서 붙혀넣는 방식으로 바꾸기로 했다. 
```
Clipboard := "https://chatgpt.com/"
ClipWait(1) ; 클립보드가 1초 이내에 업데이트될 때까지 대기
Send("^v")  ; 클립보드에 저장된 URL 붙여넣기
        Sleep(100)  ; 잠시 대기
        Send("{Enter}")  ; Enter 키
```

21세기에 클립보드 복사 붙혀넣기 하는데 1초 이상을 기다려야 한다는 걸 이해할 수 없었다. 이런 방식은 아닌 것 같다는 생각에 다른 방식을 찾기 시작했다. 그래서 결국 새로운 방법을 찾았다. Shortcut 파일을 만들어 실행 시키는 방법이다. 

---

먼저 가고자 하는 사이트의 주소를 .url 형식의 파일로 생성한다. 주소창을 선택하고 폴더에 드래그만 하면 생성된다. 그리고 코드를 만든다.
```
^Numpad1::Run("D:\ShortCuts\ChatGPT.url")
```

단 한 줄이 저 긴 코드를 대신했다. 이 얼마나 간단한가. 이렇게 작성한 코드를 정리해서 .ahk 로 저장하고 관리자권한으로 실행한다.

---
## 완성

이것은 지금 간단히 만든 내 **Shortcut-System**이다.
```
#Requires AutoHotkey v2

^Numpad1::Run("C:\Users\xixsxix\AppData\Local\Programs\Obsidian\Obsidian.exe")
^Numpad2::Run("C:\Users\xixsxix\AppData\Local\Programs\Microsoft VS Code\Code.exe")
^Numpad3::Run('cmd.exe /k "cd /d d:\xixsxix.github.io && bundle exec jekyll serve"')
^Numpad4::Run("D:\ShortCuts\ChatGPT.url")
^Numpad5::Run("D:\ShortCuts\Perplexity.url")
^Numpad7::Run("D:\Scripts\MoveMP3.bat")
^Numpad8::Run("D:\Scripts\MovePNG.bat")
^Numpad9::Run("D:\Scripts\MoveMP4.bat")
```

.url 파일을 따로 관리해야 하는 다소 불편함이 있지만 한줄 짜리를 몇십줄 코드로 대신하는 것 보다는 간단하다. 이런 식으로 앞에 **^**(Ctrl), **!**(Alt), **+**(Shift) 등을 이용해서 활용하면 왠만한 프로그램은 다 등록할 수 있다. 

