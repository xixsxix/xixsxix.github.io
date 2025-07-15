---
title: "NAS 모니터링시스템 #4 inotifywait"
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
  - inotifywait
pin: false
comments: "true"
image: /assets/img/linux-title02.webp
---
이전 편에서 `inotify-tools`를 설치하고 기본적인 테스트까지 마쳤다. 이번 글에서는 내가 실제로 Synology NAS에 적용한 실시간 감시 시스템을 중심으로 `inotifywait`를 활용한 자동화 환경 구축 과정을 공유하고자 한다.

⚠️ **주의:** 아래 모든 명령은 관리자 권한(root)에서 실행해야 한다. 일반 사용자로 접속한 경우 `sudo -i` 명령으로 root 세션으로 전환하자.

<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-1/" target="_blank"># NAS 모니터링시스템 #1 Script</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-2/" target="_blank"># NAS 모니터링시스템 #2 Entware</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-3/" target="_blank"># NAS 모니터링시스템 #3 inotify-tools</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-4/" target="_blank"># NAS 모니터링시스템 #4 inotifywait</a>

---
## NAS 자동화 4편: # inotifywait 실전 활용

---

### inotifywait 란?

`inotifywait`는 지정한 디렉토리에서 **파일 생성, 이동, 수정 등의 이벤트를 실시간으로 감지**해주는 명령어다. 자동화 스크립트와 함께 사용하면 NAS가 스스로 작업을 처리하도록 만들 수 있다.

---
### 1. 내가 설정한 감시 구조

NAS를 사용할 때 도큐멘트들은 작업 진행하면서 파일을 저장하기 때문에 감시 시스템을 구성할 필요가 거의 없다. 감시 시스템은 갑자기 많이 파일이 다운로드 되거나 많은 파일을 이동시켜 NAS가 빨리 정리하게 만드는 시스템이다. 그래서 나는 아래와 같이 정의했다.

- **Downloads** : 자동으로 받은 파일이 저장되는 경로
- **Temp** : 로컬 PC에서 수동으로 NAS로 업로드하는 공간

그래서 `/volume1/Downloads` 와 `/volume1/Temp` 두 디렉토리를 동시에 감시하도록 구성했다. 
이곳에 특정 확장자 파일이 생성되면 `auto_cleanup.sh` 스크립트를 실행하여 정리 작업을 수행하도록 했다.

---
### 2. 실제 사용 중인 `auto_watch.sh`

이 스크립트를 완성하기 위해서 
```
#!/bin/bash
############################################################
# ▶ 실행 (백그라운드):
#    nohup /volume1/homes/JHs/auto_watch.sh > /dev/null 2>&1 &
#
# ▶ 실행 중인지 확인:
#    ps | grep auto_watch
#
# ▶ 실행 중지:
#    killall auto_watch.sh
#
# ▶ 로그 확인:
#    tail -f /volume1/homes/JHs/Logs/watcher.log
#
# ▶ 로그 위치:
#    /volume1/homes/JHs/Logs/watcher.log
#
# ▶ 연결된 정리 스크립트:
#    /volume1/homes/JHs/auto_cleanup.sh
############################################################
# 감시 대상 디렉토리
WATCH_DIRS=("/volume1/Downloads" "/volume1/Temp")

# 감시 확장자
TARGET_EXT="mp4|mkv|avi|srt|smi|epub|opf"  # 추가 확장자 적용

# cleanup 스크립트 경로
CLEANUP_SCRIPT="/volume1/homes/JHs/auto_cleanup.sh"

# 감시 로그
LOG_WATCH="/volume1/homes/JHs/Logs/watcher.log"

mkdir -p "$(dirname "$LOG_WATCH")"

# inotifywait 설치 확인
if ! command -v inotifywait &> /dev/null; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Error: inotifywait is not installed. Please install it and try again." >> "$LOG_WATCH"
    exit 1
fi

# 시작 시 전체 정리 1회 실행
echo "$(date '+%Y-%m-%d %H:%M:%S') - Initial cleanup started." >> "$LOG_WATCH"
if ! sh "$CLEANUP_SCRIPT"; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Error: Initial cleanup failed." >> "$LOG_WATCH"
fi

# 감시 시작 로그
echo "$(date '+%Y-%m-%d %H:%M:%S') - Watching started for: ${WATCH_DIRS[*]}" >> "$LOG_WATCH"

# 실시간 감시 시작 (하위 디렉토리까지 감지하도록 -r 옵션 추가)
inotifywait -mr -e create -e moved_to --format "%w%f" "${WATCH_DIRS[@]}" | while read NEWFILE; do
  echo "$(date '+%Y-%m-%d %H:%M:%S') - File detected: \"$NEWFILE\"" >> "$LOG_WATCH"
  sleep 2

  # 디버깅 로그 추가
  echo "$(date '+%Y-%m-%d %H:%M:%S') - Debug: Checking file path: \"$NEWFILE\"" >> "$LOG_WATCH"

  # 확장자 추출
  EXT="${NEWFILE##*.}"
  EXT="${EXT,,}"  # 소문자로 변환
  if echo "$EXT" | grep -Eiq "^($TARGET_EXT)$"; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Matched: \"$NEWFILE\" → Running cleanup" >> "$LOG_WATCH"
    if ! sh "$CLEANUP_SCRIPT"; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Error: Cleanup script failed for \"$NEWFILE\"" >> "$LOG_WATCH"
    fi
  else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Skipped: \"$NEWFILE\" (Extension not matched)" >> "$LOG_WATCH"
  fi
done
```

⚠️ 이 스크립트는 관리자 권한(root)으로 실행해야 한다.

---

### 3. 백그라운드 실행
```
nohup /volume1/homes/JHs/auto_watch.sh > /dev/null 2>&1 &
```

실행 확인:
```
ps | grep auto_watch
```

중지:
```
killall auto_watch.sh
```

또는 로그 파일을 실시간 확인:
```
tail -f /volume1/homes/JHs/Logs/watcher.log
```
*자주 사용하지만 잊을 수 있어서 스크립트에 주석으로 넣어놨다.*

---

### 4. 연동되는 cleanup 스크립트

이제 `inotifywait`가 백그라운드에서 실행이 되었다. 감지된 파일이 있을 때 로그를 남기고 `auto_cleanup.sh`가 실행이 된다. 참고로 `auto_cleanup.sh`는 이전에 다루었던 <a href="https://xixsxix.github.io/posts/Nas-Auto-Script/" target="_blank">Synology Nas Auto Script</a>에서 정리했다. 이로서 확장자에 따라 파일을 이동시키거나 불필요한 파일을 삭제하고 로그를 남기도록 구성했다. 

이제 NAS는 지정한 폴더에 파일이 생성되면 **즉시 반응하고 필요한 작업을 자동으로 처리**할 수 있도록 만들어 졌다. 단순한 스케줄러 실행보다 훨씬 더 효율적이며, 즉각적인 처리가 가능하다는 점에서 만족도가 매우 높다. 

지금까지의 작업은 파일의 확장자로 구분하여 작업하도록 만들었다. 하지만 파일의 이름으로 분석한다면 이름 안의 단어로 영화와 드라마로 구분할 수도 있다. 영화는 영화 폴더에 넣고 드라마는 파일 이름에 있는 제목에 따라 폴더를 만들어 이동시키는 작업도 가능하다. 하지만 너무 세분하면 내가 더 피곤해 질 것 같아 고민중이다.

다음에 기회가 되면 제작해 보리라 다짐해 본다.


<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-1/" target="_blank"># NAS 모니터링시스템 #1 Script</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-2/" target="_blank"># NAS 모니터링시스템 #2 Entware</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-3/" target="_blank"># NAS 모니터링시스템 #3 inotify-tools</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-4/" target="_blank"># NAS 모니터링시스템 #4 inotifywait</a>