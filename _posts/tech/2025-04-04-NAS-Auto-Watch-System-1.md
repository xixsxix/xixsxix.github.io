---
title: "NAS 모니터링시스템 #1 Script"
date: '"2025-04-04 10:26:15 +0900"'
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
pin: false
comments: "true"
image: /assets/img/linux-title02.webp
---

## NAS 자동화 1편: # Script

---

Synology Nas를 사용한 지 벌써 10년이 넘었다. 회사에서 합사를 처음 진행할 때 직원이 본사에서 받아온 네모난 기계를 처음 보았다. 기계를 네트워크 케이블에 연결하니 우리만의 서버가 만들어졌다. 너무 신기했다. 그 이후 나는 작고 저렴한 개인 Nas를 구매했다. 그렇게 내 Nas생활이 시작되었다.   
  
Nas를 설치하고 내 PC생활은 달라졌다. iPhone과 iPad, 그리고 맥북은 iCloud를 통해 한 기기처럼 사용했었지만 윈도우 환경에 있는 PC는 그러하지 못했다. Nas는 수십 기가에 달하는 파일들을 통합하고 모든 기기를 일체화해 주었다. 필요한 자료가 있으면 접속해서 어디서든 편집이 가능하게 해 주었다. 용량이 적은 iCloud에 의존해야 했던 모든 것이 풍족해졌다.   
  
Nas가 무엇보다 편리한 것은 토렌트를 자동으로 받아 온다는 것이다. 지정한 영화, 드라마, 예능, 음악 등을 자동으로 Nas가 받아 두면 퇴근 후에 정리했다. 그것도 불편했다. 그래서 Nas에 있는 리눅스 환경을 이용해서 Script를 작성하기로 했다. HTML에 필요한 명령 일부만 알고 있던 나는 검색을 통해 스크립트를 완성했다. 기준은 이렇다.   
  
1. Downloads : 나스가 자동으로 받아 저장하는 곳  
2. Temp : 로컬에서 나스에 올리는 곳  
3. 다운받은 영상과 자막 등 해당 폴더로 이동  
4. 홍보성 파일 등 삭제  
5. 빈폴더 삭제  
6. 일정기간 지난 파일 삭제  
  
이렇게 작성한 스크립트를 Nas 작업스케줄러에 등록하고 1분 간격으로 실행했다.    
```
## 일정 기간이 지난 파일 삭제 
find "/volume1/TV/예능/" \
  -type f \
  -mtime +30 \
  \( -name '*.mp4' -o -name '*.mkv' -o -name '*.ts' \) \
  -exec rm {} \;

find "/volume1/TV/예능/" \
  -type d \
  -empty \
  -mtime +30 \
  -exec rm -d {} \;

find "/volume1/TV/다큐/" \
  -type f \
  -mtime +90 \
  \( -name '*.mp4' -o -name '*.mkv' -o -name '*.ts' \) \
  -exec rm {} \;

find "/volume1/TV/다큐/" \
  -type d \
  -empty \
  -mtime +90 \
  -exec rm -d {} \;

## 다운로드 영상 이동 
find "/volume1/Downloads/" \
  -type f \
  \( -name '*.mp4' -o -name '*.mkv' -o -name '*.srt' -o -name '*.smi' \) \
  -exec mv {} "/volume1/Movies" \;

find "/volume1/Temp/" \
  -type f \
  \( -name '*.srt' -o -name '*.smi' \) \
  -exec mv {} "/volume1/Movies" \;

find "/volume1/Downloads/" \
  -type f \
  \( -name '*.epub' \) \
  -exec mv {} "/volume1/Ebook/Ebook(Epub)" \;

find "/volume1/Temp/" \
  -type f \
  \( -name '*.epub' \) \
  -exec mv {} "/volume1/Ebook/Ebook(Epub)" \;

find "/volume1/Downloads/" \
  -type f \
  \( -name '*.pdf' \) \
  -exec mv {} "/volume1/Ebook/Ebook(PDF)" \;

find "/volume1/Temp/" \
  -type f \
  \( -name '*.pdf' \) \
  -exec mv {} "/volume1/Ebook/Ebook(PDF)" \;

## 필요없는 파일 삭제 
find "/volume1/Downloads/" \
  -type f \
  \( -name '*.url' -o -name '*.txt' -o -name 'www.YTS.MX.jpg' \) \
  -exec rm {} \;

find "/volume1/TV/" \
  -type f \
  \( -name '*.vsmeta' \) \
  -exec rm {} \;

find "/volume1/Temp/" \
  -type f \
  \( -name '*.jpg' -o -name '*.opf' \) \
  -exec rm {} \;

## 용량작은 파일 삭제 
find "/volume1/Downloads/" \
  -type f \
  -size -50k \
  -exec rm {} \;

## 빈폴더 삭제 
find "/volume1/Downloads/." \
  -type d \
  -empty \
  -exec rm -d {} \;

find "/volume1/Temp/." \
  -type d \
  -empty \
  -exec rm -d {} \;
```

난 이 스크립트로 상당히 오랜 기간 사용했다. 하지만 이렇게 작성한 스크립트가 잘 된 거지 검토해 줄 사람이 없었다. 내 주위엔 이 분야에 전문가가 아무도 없다. 그래서 이번에 ChatGPT에게 검토를 부탁했다.   
  
ChatGPT와 나눈 대화를 정리하면 이렇다.  
1. -exec rm {}에서 공백/특수문자 문제  
2. 빈 디렉터리 삭제: -d 옵션보다 -delete 사용 권장  
3. 중복 이동 조건  
4. 빈 폴더 삭제 시 경로 오류 가능성  
5. 로그 기록이 없음 (특히 NAS에서는 추적 필요)  
6. 그 외 개인용 작업들  
  
ChatGPT는 유료이더라도 오류가 있다. 그래서 꼼꼼히 확인해야 한다. 대화 중 다른 주제로 이야기를 나눈 경우에는 두 주제를 합치는 경우가 종종 있다. 아무튼 그렇게 여러 내용 중 최종본을 만들었다.  
  
```
## 로그 디렉토리
LOG_DIR="/volume1/homes/JHs/Logs"
mkdir -p "$LOG_DIR"

# 오늘 날짜 기준 로그 파일
LOG_DATE=$(date '+%Y-%m-%d')
LOG="$LOG_DIR/cleanup_$LOG_DATE.log"

# 로그 시작
echo "=== Cleanup started at $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG"

# ------------------------------------------------------
# 로그 정리 (압축 및 삭제)
# ------------------------------------------------------

# 7일 지난 로그 파일 압축
find "$LOG_DIR" \
  -type f \
  -name "cleanup_*.log" \
  -mtime +7 \
  ! -name "*.gz" \
  -exec gzip "{}" \; >> "$LOG" 2>&1

# 30일 지난 압축 로그 삭제
find "$LOG_DIR" \
  -type f \
  -name "*.gz" \
  -mtime +30 \
  -exec rm -v "{}" \; >> "$LOG" 2>&1

# ------------------------------------------------------
# 오래된 영상 파일 삭제 (예능: 30일, 다큐: 90일)
# ------------------------------------------------------

find "/volume1/TV/예능/" \
  -type f \
  -regex '.*\.\(mp4\|mkv\|ts\)' \
  -mtime +30 \
  -print0 | xargs -0 rm -v >> "$LOG" 2>&1

find "/volume1/TV/예능/" \
  -type d \
  -empty \
  -mtime +30 \
  -delete >> "$LOG" 2>&1

find "/volume1/TV/다큐/" \
  -type f \
  -regex '.*\.\(mp4\|mkv\|ts\)' \
  -mtime +90 \
  -print0 | xargs -0 rm -v >> "$LOG" 2>&1

find "/volume1/TV/다큐/" \
  -type d \
  -empty \
  -mtime +90 \
  -delete >> "$LOG" 2>&1

# ------------------------------------------------------
# 다운로드 폴더 정리 및 파일 이동
# ------------------------------------------------------

# 1. 개인용이라서 Void

# 2. 일반 영상 및 자막 파일은 Movies로 이동
find "/volume1/Downloads/" \
  -type f \
  -regex '.*\.\(mp4\|mkv\|srt\|smi\)' \
  -exec mv "{}" "/volume1/Movies" \; >> "$LOG" 2>&1

# 3. Temp 내 자막 파일도 Movies로 이동
find "/volume1/Temp/" \
  -type f \
  -regex '.*\.\(srt\|smi\)' \
  -exec mv "{}" "/volume1/Movies" \; >> "$LOG" 2>&1

# ------------------------------------------------------
# 개인용이라서 Void
# ------------------------------------------------------

# ------------------------------------------------------
# Ebook 파일 이동 (epub/pdf)
# ------------------------------------------------------

find "/volume1/Downloads/" \
  -type f \
  -name '*.epub' \
  -exec mv "{}" "/volume1/Ebook/Ebook(Epub)" \; >> "$LOG" 2>&1

find "/volume1/Temp/" \
  -type f \
  -name '*.epub' \
  -exec mv "{}" "/volume1/Ebook/Ebook(Epub)" \; >> "$LOG" 2>&1

find "/volume1/Downloads/" \
  -type f \
  -name '*.pdf' \
  -exec mv "{}" "/volume1/Ebook/Ebook(PDF)" \; >> "$LOG" 2>&1

find "/volume1/Temp/" \
  -type f \
  -name '*.pdf' \
  -exec mv "{}" "/volume1/Ebook/Ebook(PDF)" \; >> "$LOG" 2>&1

# ------------------------------------------------------
# 불필요 파일 삭제
# ------------------------------------------------------

find "/volume1/Downloads/" \
  -type f \
  -regex '.*\.\(url\|txt\)' \
  -exec rm -v "{}" \; >> "$LOG" 2>&1

find "/volume1/Downloads/" \
  -type f \
  -name 'www.YTS.MX.jpg' \
  -exec rm -v "{}" \; >> "$LOG" 2>&1

find "/volume1/TV/" \
  -type f \
  -name '*.vsmeta' \
  -exec rm -v "{}" \; >> "$LOG" 2>&1

find "/volume1/Temp/" \
  -type f \
  -regex '.*\.\(jpg\|opf\)' \
  -exec rm -v "{}" \; >> "$LOG" 2>&1

# ------------------------------------------------------
# 빈 폴더 정리
# ------------------------------------------------------

find "/volume1/Downloads/" \
  -type d \
  -empty \
  -delete >> "$LOG" 2>&1

find "/volume1/Temp/" \
  -type d \
  -empty \
  -delete >> "$LOG" 2>&1

# ------------------------------------------------------
# 완료 로그
# ------------------------------------------------------

echo "=== Cleanup completed at $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG"
echo "" >> "$LOG"

```
  
*로그까지 정리해서 스크립트를 완성했다. 중간에 개인용이 별도로 있는데 보안상 삭제했다.*  
  
이 버전에서 문제는 Downloads나 Temp 폴더에 들어 가는 jpg, png 같은 이미지들이 필요한 것 일 수도 있다는 것이다. 그래서 이미지 파일의 경우는 다른 폴더에 일정 기간 저장해 둔 후 삭제하는 명령을 넣었다.

그리고 이 스크립트를 "VS Code" GitHub Copilot에 다시 물었다. 그가 만들어 준 script는 이렇다. 참고로 GitHub Copilot은 VS Code 프로그램에 내장되어 있는 코딩 전문 AI다.

```
#!/bin/bash

############################################################
#
# 자동 정리 스크립트 (업데이트 버전)
#
# - 용량 작은 영상 삭제 (100MB 미만)
# - 확장자별 파일 이동
# - 이미지 파일은 별도 폴더로 7일간 보관 후 삭제
# - 불필요한 파일 삭제 (Temp는 공격적으로, Downloads는 안전하게)
# - 빈 폴더 정리
# - 로그 저장
#
############################################################

# 설정
BASE_DIR="/volume1"
DOWNLOADS_DIR="$BASE_DIR/Downloads"
TEMP_DIR="$BASE_DIR/Temp"
VOID_DIR="$BASE_DIR/VOID"
MOVIES_DIR="$BASE_DIR/Movies"
EBOOK_DIR="$BASE_DIR/Ebook"
MEDIACACHE_DIR="$BASE_DIR/homes/JHs/Mediacache/Images"
LOG_DIR="$BASE_DIR/homes/JHs/Logs"
LOG_DATE=$(date '+%Y-%m-%d')
LOG="$LOG_DIR/cleanup_$LOG_DATE.log"

mkdir -p "$LOG_DIR" "$MEDIACACHE_DIR"

echo "=== Cleanup started at $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG"

# 함수 정의
delete_small_files() {
    local path=$1
    local size=$2
    echo "Deleting small files under $size in $path..." >> "$LOG"
    find "$path" -type f -name "*.mp4" -size -"$size" -exec rm -v "{}" \; >> "$LOG" 2>&1
}

move_files() {
    local path=$1
    local pattern=$2
    local target=$3
    echo "Moving files matching pattern '$pattern' from $path to $target..." >> "$LOG"
    find "$path" -type f -regex "$pattern" -exec mv -v "{}" "$target" \; >> "$LOG" 2>&1
}

rename_files() {
    local path=$1
    echo "Renaming files in $path..." >> "$LOG"
    find "$path" -type f -name "VOID" | while read file; do
        dir=$(dirname "$file")
        base=$(basename "$file")
        clean=${base#VOID}
        if [ "$base" != "$clean" ]; then
            mv -v "$file" "$dir/$clean" >> "$LOG" 2>&1
            echo "Renamed: $base -> $clean" >> "$LOG"
        fi
    done
}

delete_unnecessary_files() {
    local path=$1
    local pattern=$2
    echo "Removing unnecessary files from $path..." >> "$LOG"
    find "$path" -type f -regex "$pattern" -print0 | xargs -0 -I {} rm -v "{}" >> "$LOG" 2>&1
}

delete_empty_folders() {
    local path=$1
    echo "Deleting empty folders in $path..." >> "$LOG"
    find "$path" -type d -empty -delete >> "$LOG" 2>&1
}

# ✅ [1] 용량 작은 .mp4 삭제 (100MB 미만)
delete_small_files "$DOWNLOADS_DIR" "100M"
delete_small_files "$TEMP_DIR" "100M"

# ✅ [2] 다운로드 영상 이동
move_files "$DOWNLOADS_DIR" '.*VOID.*\.mp4' "$VOID_DIR"
move_files "$DOWNLOADS_DIR" '.*\.(mp4|mkv|srt|smi)' "$MOVIES_DIR"
move_files "$TEMP_DIR" '.*\.(srt|smi)' "$MOVIES_DIR"

# ✅ [3] Ebook 파일 이동
move_files "$DOWNLOADS_DIR" '.*\.epub' "$EBOOK_DIR/Ebook(Epub)"
move_files "$DOWNLOADS_DIR" '.*\.pdf' "$EBOOK_DIR/Ebook(PDF)"
move_files "$TEMP_DIR" '.*\.epub' "$EBOOK_DIR/Ebook(Epub)"
move_files "$TEMP_DIR" '.*\.pdf' "$EBOOK_DIR/Ebook(PDF)"

# ✅ [4] 이미지 파일은 Mediacache로 이동 (7일 보관)
echo "Moving image files to Mediacache..." >> "$LOG"
find "$DOWNLOADS_DIR" -type f -regex '.*\.(jpg|jpeg|png)' -print0 | xargs -0 -I {} mv -v "{}" "$MEDIACACHE_DIR" >> "$LOG" 2>&1
echo "Deleting cached images older than 7 days..." >> "$LOG"
find "$MEDIACACHE_DIR" -type f -mtime +7 -print0 | xargs -0 -I {} rm -v "{}" >> "$LOG" 2>&1

# ✅ [5] VOID 접두어 제거
rename_files "$VOID_DIR"

# ✅ [6] 불필요한 파일 제거
delete_unnecessary_files "$DOWNLOADS_DIR" '.*\.(url|txt|html|nfo)'
delete_unnecessary_files "$TEMP_DIR" '.*\.(jpg|jpeg|png|opf|url|txt|html|nfo)'

# ✅ [7] 빈 폴더 삭제
delete_empty_folders "$DOWNLOADS_DIR"
delete_empty_folders "$TEMP_DIR"

echo "=== Cleanup completed at $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG"
```

이제 나스에 있는 작업 스케줄러에 등록하고 실행하면 된다. 그동안 실행 간격은 1분이었다. ChatGPT는 너무 빠르다고 한다. 안정화되면 15분 정도를 권장한다고 한다. 하지만 영상을 받고 어찌 15분이나 기다릴 수 있겠는가.

Nas를 사용하는 궁극적인 이유는 완전 자동화이다. 자동으로 다운로드 받은 파일의 이름이나 확장자에 따라 최대한 구분하여 특정한 폴더에 규칙대로 이동시키고 삭제하는 방식 말이다. Mac의 경우는 10년, 그 이전 부터 가능했다. 프로그램 하나로 모든 로컬 파일이나 연결되어 있는 서버까지 규칙에 따라 움직인다. 최근 맥에서 윈도우로 바뀐 환경으로 인해 나는 모두 바꿔야 했다.

이제 그 시스템을 ChatGPT와 함께 만들어 보려고 한다. 작업스케줄러를 이용하지 않고 특정 폴더에 지정한 파일이 저장되면 바로 움직이는 시스템을 만들어 보자.

<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-1/" target="_blank"># NAS 모니터링시스템 #1 Script</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-2/" target="_blank"># NAS 모니터링시스템 #2 Entware</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-3/" target="_blank"># NAS 모니터링시스템 #3 inotify-tools</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-4/" target="_blank"># NAS 모니터링시스템 #4 inotifywait</a>