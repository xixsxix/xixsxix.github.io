---
title: "NAS 모니터링시스템 #3 inotify-tools"
date: '"2025-04-04 15:28:41 +0900"'
categories:
  - Linux
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
  - entware
  - inotify
pin: false
comments: "true"
image: /assets/img/linux-title02.webp
---
이전 글에서 Entware 설치를 완료하여 Synology NAS에서 **opkg** 패키지 매니저를 사용할 수 있게 되었다. 이번 글에서는 실시간 폴더 감시를 위한 도구인 **inotify-tools**를 설치하는 과정을 정리한다.

⚠️ **주의:** 아래 모든 명령은 관리자 권한(root)에서 실행해야 한다. 일반 사용자로 접속한 경우 `sudo -i` 명령으로 root 세션으로 전환하자.

<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-1/" target="_blank"># NAS 모니터링시스템 #1 Script</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-2/" target="_blank"># NAS 모니터링시스템 #2 Entware</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-3/" target="_blank"># NAS 모니터링시스템 #3 inotify-tools</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-4/" target="_blank"># NAS 모니터링시스템 #4 inotifywait</a>

---
## NAS 자동화 3편: inotify-tools 설치

---

### inotify-tools 란?

`inotify-tools`는 리눅스의 inotify(이벤트 기반 파일 시스템 감시 기능)를 CLI에서 사용할 수 있게 해주는 유틸리티다. 대표적으로 `inotifywait`, `inotifywatch` 명령어를 제공하며, **파일이나 디렉토리에서 발생하는 이벤트(생성, 수정, 삭제 등)를 실시간으로 감지**할 수 있다. NAS 자동화에 있어 핵심 역할을 한다.

#### 1. ssh 로그인
```
ssh 사용자명@NAS_IP주소 -p 포트번호
```

#### 2. 관리자 권한으로 전환
```
sudo -i
```
아래 모든 명령은 관리자 권한(root)에서 실행해야 한다. 일반 사용자로 접속한 경우 sudo -i 명령으로 root 세션으로 전환하고 진행하자.

#### 3. opkg 업데이트
```
opkg update
```
지난 문서에서 Entware를 설치했다면 위 명령어는 오류없이 진행 될 것이다.

#### 4. inotify-tools 설치
이제 inotifywait 명령어가 포함된 inotify-tools 패키지를 설치한다.
```
opkg install inotify-tools
```
설치가 완료되면 `/opt/bin` 경로에 `inotifywait`, `inotifywatch` 등의 도구가 설치된다.

#### 5. 설치 확인
```
which inotifywait
```

정상적으로 설치되었다면 아래와 같이 출력된다.
```
# 예시
/opt/bin/inotifywait
```

또는 버전 확인
```
inotifywait --version
```

#### 6. 간단 테스트
다운로드 폴더를 대상으로 테스트를 해보자.
```
inotifywait -m /volume1/Downloads
```

이 상태에서 해당 폴더에 파일을 추가하면 다음과 같은 출력이 나타난다.
```
/volume1/Downloads/ CREATE myfile.mp4
```

---

이제 NAS에서 **폴더 변화 이벤트를 감지할 수 있는 환경**이 갖춰졌다. 다음은 `inotifywait`를 활용한 자동 정리 스크립트 구현을 다루어 보자.

<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-1/" target="_blank"># NAS 모니터링시스템 #1 Script</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-2/" target="_blank"># NAS 모니터링시스템 #2 Entware</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-3/" target="_blank"># NAS 모니터링시스템 #3 inotify-tools</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-4/" target="_blank"># NAS 모니터링시스템 #4 inotifywait</a>