---
title: Calibre, 변환 후 Original_Epub 삭제
date: '"2025-06-26 07:34:39 +0900"'
categories:
  - Clippings
tags:
  - clippings
  - calibre
  - calibre-web
  - 변환후
  - original_epub
  - 삭제
image: /assets/img/222136.png
hide_image: false
pin: false
---

## 1. Calibre Metadata.db

Epub을 다운로드할 때 지정된 폴더에 저장하면 자동으로 Calibre에 등록된다. 환경설정에서 특정 폴더를 지정하고 모니터링할 확장자를 정하면 된다. 이때 다른 형식으로도 변환이 가능하다. PDF를 Epub으로 변환을 해 주는 기능은 효율이 좋다. 다만 pdf의 품질이 낮아 텍스트 인식이 어렵다면 이미지 형태로 변환된다.

이렇게 등록된 Epub을 다른 라이브러리와 통일성 있게 정리하기 위해서 서점 플러그인[^1]으로 데이터를 가져오고 내 취향에 맞게 편집을 한다. 수정할 부분은 제목, 작가, 태그 그리고 책 설명이 대부분이다. 가끔 커버 이미지가 없거나 해상도가 너무 낮을 때는 바꾸기도 한다.[^2]

편집이 완료되면 Calibre-web에서도 그대로 적용된다. 뷰어로 사용하는 iPad에서 Calibre-web에 접속하여 도서를 다운로드하면 AppleBooks(도서 앱)[^3]으로 독서를 할 수 있다. 이때, 커버이미지를 변경한 도서는 반영이 안 된다. Calibre와 Calibre-web에서는 편집한 내용이 보이지만 추출한 파일에는 적용이 안되어 배출하게 된다. 이는 원본을 손상하지 않으려는 Calibre의 규칙인 듯하다. 완벽하게 추출하기 위해서는 변환이라는 단계를 거쳐야 한다. 

Calibre에서 책을 선택하고 "책 변환하기"를 누르면 많은 옵션이 있다. 상단 좌, 우측에 입력형식과 출력형식을 확인하고 변환을 하면 된다.  변환이 완료되면 두 개의 파일이 생기는데 변환된 파일은 확장자가 `.epub`이 되고, 원본 파일은 `.original_epub`으로 바뀐다. Calibre를 자주 사용하다 보면 사용하지 않는 `.original_epub`을 보관하기에는 부담이 많이 되는 것은 사실이다. 그래서 이 필요 없는 원본 파일을 이제 삭제하려 한다.

[^1]: 서점 플러그인 : 네이버 책(Naver Book) API를 등록한 플러그인으로 국내,외 도서 대부분의 메타데이터를 가져올 수 있다. 플러그인은 소스를 검색해서 직접 제작해야 한다. 

[^2]: YES24 플러그인 : 국내,외 커버 이미지를 가져 올 수 있다. 플러그인은 소스를 가져와 등록하면 되고, API는 필요 없다. 

[^3]: AppleBooks : Apple에서 제공하는 기본 도서앱으로 Mac, iPad, iPhone에서 사용할 수 있다. iCloud를 통해 모든 기기에서 공유가 가능하다. 필자의 주관으로는 현존 최고의 도서앱이라 평한다.

---

## 2. 생성된 `original_epub` 삭제

`.original_epub`은 Calibre 라이브러리로 지정한 폴더, 즉 `metadata.db` 가 저장된 폴더에 저장된다. 한글을 영어로 타이핑 한 폴더에 저장이 되기 때문에 특정 파일만 골라 지우기는 쉽지 않다. 또한, 수동으로 삭제하면 Calibre는 지워진 줄 모르기 때문에 리스트에 그래도 남아있게 된다.  Calibre가 인식한 상태로 `.original_epub` 파일을 제거 하려면 Calibre의 CLI 명령어인 `calibredb.exe` 를 사용하면 쉽다.  Calibre는 자체 DB를 관리하기 위해 `calibredb`라는 CLI 도구를 제공한다.  이걸 통해 **등록된 책의 특정 포맷**만 제거할 수 있다.

아래의 스크립트를 복사하여 텍스트파일에 넣고 .ps1으로 저장한다. 그리고 PowerShell에서 저장한 파일을 실행하면 된다. 
```
$libraryPath = "E:\Calibre-Library"
$calibredb = "C:\Program Files\Calibre2\calibredb.exe"
  
$bookList = & "$calibredb" list --library-path "$libraryPath" --for-machine | ConvertFrom-Json
  
foreach ($book in $bookList) {
    $id = $book.id
    Write-Host "Removing original_epub from book ID: $id"
    & "$calibredb" remove_format "$id" "original_epub" --library-path "$libraryPath"
}
  
Write-Host "original_epub 삭제 완료"
```

**이 명령을 실행할 때는 반드시 Calibre가 종료된 상태여야 한다.**

---
## 3. original_epub 파일 생성 방지

**`original_epub`을 생성하지 않도록 설정할 수 있다.**
Calibre는 상당히 사용자 친화적이지 않은 구조를 가지고 있다.  단순한 설정 한 개를 찾기 위해 설정의 모든 곳을 다 뒤져봐야 알 수 있다. 혹은 이런 설정이 있는지도 모를 정도다. 하지만 이런 설정이 있을까 싶은 설정은 대부분 있다. 

**환경설정(Preferences)** 의 하단에 위치한 **Tweaks** 으로 이동한다. 검색창에 **save original format**을 입력하면 *Save original file when converting/polishing from same format to same format* 이라는 항목을 찾을 수 있다.

설정값을 False로 바꾸고 저장 후 Calibre를 재시작하면 `original_epub`을 생성하지 않게 된다.
```
save_original_format_when_polishing = False
save_original_format_when_converting = False
```

---

