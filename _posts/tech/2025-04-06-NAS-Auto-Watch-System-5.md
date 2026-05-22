---
title: "NAS 모니터링시스템 #5 inotifywait. 후유증"
date: '"2025-04-06 17:47:44 +0900"'
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
  - inotify
  - inotifywait
  - inotify-tools
pin: false
comments: "true"
image: /assets/img/linux-title02.webp
---

## inotifywait. 후유증

**ChatGPT**와 **VS Code**의 **GitHub Copilot**과 함께 진행한 Script를 결국 어느 정도의 선에서 마무리 했다. "완전한 것은 없다"고 스스로 다짐하며 마무리 했다. 이것이 Script의 한계라기 보다는 inotify-tools의 한계라고 생각하는 것이 옳다고 판단한다. 어쩌면 더 깊이 파고 들면 가능할 지도 모르지만 나의 한계일 수도 있을 것이다. 

상황은 이렇다. 외부에서 또는 로컬에서 감시 대상인 폴더에, 하위 폴더가 연달아 있는 폴더와 파일을 넣는다. **inotify**가 감지하고 깊숙한 폴더에 있는 파일을 지정한 폴더로 이동, 필요없는 파일은 삭제한다. 그리고 남은 폴더들을 저 안쪽부터 삭제해야 한다. 내가 원하는 것은 폴더 안으로 단계의 폴더가 있더라도 한 번의 명령으로 삭제가 되기를 원했던 것이다.

여기서 문제가 발행한다.
depth와 mindepth 를 써서 명확한 명령을 내려도 한번에 삭제가 되지는 않았다. 그리고 생각했다. 필요한 파일을 이미 이동시켰다면 굳이 안쪽부터 차례대로 삭제할 필요가 있을까? 그리고 과감히 결단했다. 
```
find "$base_dir" -type d -empty -exec rm -rf {} \;
```
그래! -empty 넣었잖아. 괜찮아.

이렇게 모든 작업을 마무리 했다.

```
#!/bin/bash
# -------------------- 설정 부분 --------------------
# 로그 파일 경로 설정
LOG_DIR="/volume1/tasks/logs"
LOG_FILE="$LOG_DIR/file_organizer_$(date +%Y-%m-%d).log"
  
# 로그 디렉토리가 존재하지 않으면 생성
mkdir -p "$LOG_DIR"
  
# 로그 출력 함수
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# 감지할 디렉토리
WATCH_DIRS=("/volume1/downloads" "/volume1/temp")
MOVIE_DIR="/volume1/movies"
CACHE_DIR="/volume1/tasks/cache"
EPUB_DIR="/volume1/ebook/epub"
PDF_DIR="/volume1/ebooks/pdf"
AXI_DIR="/volume1/axi"
MUSIC_DIR="/volume1/music"

# 파일 크기 변화 감지 후 일정 시간 동안 대기하여 완전히 다운로드된 파일을 처리
check_file_stable() {
    local file=$1
    local timeout=10  # 대기 시간 (초)
    local initial_size=$(stat -c %s "$file")
    local current_size=$initial_size
  
    for ((i=0; i<$timeout; i++)); do
        sleep 1
        current_size=$(stat -c %s "$file")
        if [ "$initial_size" -eq "$current_size" ]; then
            return 0  # 파일 크기가 변화가 없으면 처리
        fi
    done
    return 1  # 일정 시간 내에 파일 크기가 안정되지 않으면 처리하지 않음
}

# 대상 디렉토리 존재 여부 확인 및 생성
check_directory() {
    local dir=$1
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        log_message "Created missing directory: $dir"
    fi
}

# 파일이 이미 존재하면 이름 뒤에 숫자를 붙여서 저장하는 함수
move_with_unique_name() {
    local source_file=$1
    local target_dir=$2
    local target_file="$target_dir/$(basename "$source_file")"
    local counter=1

    # 파일이 존재하는 동안 숫자를 추가하여 새로운 파일 이름 생성
    while [ -e "$target_file" ]; do
        target_file="${target_dir}/$(basename "$source_file" .${source_file##*.})($counter).${source_file##*.}"
        counter=$((counter + 1))
    done

    # 파일을 이동
    mv "$source_file" "$target_file"
    log_message "Moved file: $source_file to $target_file"
}

# -------------------- inotifywait 감시 실행 --------------------
monitor_directories() {
    inotifywait -m -r -e create -e moved_to --format '%w%f' "${WATCH_DIRS[@]}" | while read FILE; do
        if [ -f "$FILE" ]; then
            # 파일 안정성 확인
            if check_file_stable "$FILE"; then
                EXT="${FILE##*.}"
                EXT_LOWER=$(echo "$EXT" | tr '[:upper:]' '[:lower:]')

                case "$EXT_LOWER" in
                    epub)
                        check_directory "$EPUB_DIR"
                        move_with_unique_name "$FILE" "$EPUB_DIR"
                        log_message "Moved EPUB file: $FILE to $EPUB_DIR"
                        ;;
                    pdf)
                        check_directory "$PDF_DIR"
                        move_with_unique_name "$FILE" "$PDF_DIR"
                        log_message "Moved PDF file: $FILE to $PDF_DIR"
                        ;;
                    mp4|mkv)
                        if [[ "$(basename "$FILE")" == hhd800.com@* ]]; then
                            move_with_unique_name "$FILE" "$AXI_DIR"
                            log_message "Moved special video file: $FILE to $AXI_DIR"
                        else
                            check_file_stable "$FILE" && move_with_unique_name "$FILE" "$MOVIE_DIR"
                            log_message "Moved video file: $FILE to $MOVIE_DIR"
                        fi
                        ;;
                    jpg|jpeg|png|gif|bmp|webp)
                        move_with_unique_name "$FILE" "$CACHE_DIR"
                        log_message "Moved image file: $FILE to $CACHE_DIR"
                        ;;
                    smi|srt)
                        move_with_unique_name "$FILE" "$MOVIE_DIR"
                        log_message "Moved subtitle file: $FILE to $MOVIE_DIR"
                        ;;
                    mp3)
                        DATE_DIR=$(date +%Y%m%d)
                        TARGET_DIR="$MUSIC_DIR/$DATE_DIR"
                        check_directory "$TARGET_DIR"
                        move_with_unique_name "$FILE" "$TARGET_DIR"
                        log_message "Moved MP3 file: $FILE to $TARGET_DIR"
                        ;;
                    *)
                        # 지정되지 않은 파일은 CACHE_DIR로 이동
                        move_with_unique_name "$FILE" "$CACHE_DIR"
                        log_message "Moved unknown file: $FILE to $CACHE_DIR"
                        ;;
                esac
            else
                log_message "Skipped unstable file: $FILE"
            fi
        fi
    done
}
  
# -------------------- downloads 폴더 처리 --------------------
process_downloads_directory() {
    local base_dir="/volume1/downloads"
  
    # base_dir 내 모든 파일 처리
    find "$base_dir" -mindepth 1 -maxdepth 1 -type f | while read FILE; do
        EXT="${FILE##*.}"
        EXT_LOWER=$(echo "$EXT" | tr '[:upper:]' '[:lower:]')
  
        case "$EXT_LOWER" in
            pdf)
                check_directory "$PDF_DIR"
                move_with_unique_name "$FILE" "$PDF_DIR"
                log_message "Moved PDF file: $FILE to $PDF_DIR"
                ;;
            mp4|mkv)
                check_file_stable "$FILE" && move_with_unique_name "$FILE" "$MOVIE_DIR"
                log_message "Moved video file: $FILE to $MOVIE_DIR"
                ;;
            *)
                move_with_unique_name "$FILE" "$CACHE_DIR"
                log_message "Moved unknown file: $FILE to $CACHE_DIR"
                ;;
        esac
    done
}
  
# -------------------- temp 폴더 처리 --------------------
process_temp_directory() {
    local base_dir="/volume1/temp"
  
    # .torrent 파일 무시하고 EPUB 파일 이동
    find "$base_dir" -type f ! -iname "*.torrent" -iname "*.epub" | while read FILE; do
        if check_file_stable "$FILE"; then
            check_directory "$EPUB_DIR"
            move_with_unique_name "$FILE" "$EPUB_DIR"
            log_message "Moved EPUB file: $FILE to $EPUB_DIR"
        else
            log_message "Skipped unstable file: $FILE"
        fi
    done
}
  
# -------------------- temp 폴더 내 모든 파일 및 폴더 삭제 --------------------
find "$base_dir" -type d -empty -exec rm -rf {} \;
  
# -------------------- 스크립트 실행 --------------------
process_downloads_directory
process_temp_directory
  
# inotifywait 감시 실행
monitor_directories
```

---

이제 **Synology DSM**에 들어가 작업 스케줄러에 등록하면 된다. 생성을 누르고 일반에서 작업에 이름을 적고, 사용자는 root. 이벤트는 부트업. 작업설정에서 사용자 정의 스크립트에 bash 명령으로 경로와 함께 적는다.
```
#!/bin/bash
# 부팅 후 inotify 실행
bash /volume1/tasks/scripts/file_organizer.sh
```

이렇게 하면 나스가 실행될 때 자동으로 **inotify**를 실행하게 된다.

---

문제는 여기서 발생했다. **Synology DSM**에 접속하자 화면이 뭔가 이상했다. 패키지 센터에 들어가 보니 이런 오류가 발생했다. 
![image](assets/linux/synology001.png)

이건 무슨 개소리냔 말이다. **ChatGPT**에 이미지를 올리고 물어도 헛소리만 해댄다. 웹 검색에 능통한 **Perplexity**에게 물었다. 그리고 새로운 사실을 깨달았다.

<div class="alert alert-info" style="background-color: #0b1c2a; color: #ffffff; padding: 10px; border-radius: 15px; border: none; white-space: pre-line;">Synology NAS에서 inotify를 구성할 때 DSM에서 오류가 발생할 가능성이 있습니다. 이는 inotify의 기본 리소스 제한 때문이며, 이를 해결하기 위해 설정을 조정해야 합니다.

<b>오류 원인</b>
1. inotify 리소스 제한: Synology NAS에서 inotify는 파일 시스템 이벤트를 감시하는 데 사용되며, 기본적으로 설정된 감시 제한이 있습니다. 이 제한은 많은 디렉토리나 파일을 감시해야 할 경우 초과될 수 있습니다.
    
2. DSM의 기본 설정: Synology DSM 운영체제는 기본적으로 inotify 관련 설정을 제한적으로 제공하며, SSH를 통해 수동으로 조정해야 하는 경우가 많습니다.
</div>

**NAS**는 기본적으로 **저사양 환경**에서 동작하는데 **inotify** 같은 실시간 감시 도구를 장시간 사용하는 것은 시스템 안정성에 큰 영향을 끼친다는 이유 때문이다. 

- **리소스 과다 사용**: 파일 이벤트를 실시간으로 감시하면서, 파일 시스템에 대한 지속적인 모니터링을 하기 때문에 메모리와 CPU 리소스를 과도하게 소모할 수 있어 이를 Synology NAS에서 제한할 수 있다.
    
- **고정된 파일 핸들링 수 제한**: 운영체제에서 설정된 최대 감시 항목 수를 넘어서면 더 이상 이벤트를 감지할 수 없게 되어버려서 Synology는 이러한 제한을 두고 있기 때문에, 설정된 값 이상의 감시를 시도할 경우 시스템이 오류를 발생시킬 수 있다.
    
- **정책적인 제한**: Synology가 안정성을 위해서 일부 고급 기능(특히 **리소스를 많이 쓰는 기능**)을 제한하거나, 비효율적인 작업을 차단하는 경우가 있어서 **inotify** 사용을 아예 막거나, 일정 수 이상의 감시를 허용하지 않을 수 있다.

일단 해결책은 있다. SSH에 관리자 권한으로 들어가 inotify 제한 값을 변경해 주면 된다.
`/etc/sysctl.conf` 에 들어가 아래와 같이 문구를 추가해 주면 된다.
```
fs.inotify.max_user_watches = 1048576
```
그리고 변경사항을 적용해 준다.
```
sysctl -p
```

그리고 다시 DSM 작업 스케줄러에 등록해서 부팅시 실행될 수 있도록 트리거를 추가해 준다.
```
#!/bin/bash
# 부팅 후 inotify 제한 설정
echo 1048576 > /proc/sys/fs/inotify/max_user_watches
```
Synology DSM에 들어가 보니 모든 것이 정상으로 돌아왔다. 
나는 이렇게 Synology NAS 자동화 시스템을 만들었다. **MAC**의 경우에는 **Hazel** 이라는 오래된 프로그램이 존재한다. 이 앱은 로컬 뿐만 아니라 연결된 서버의 폴더와 파일들을 모니터링 하고 관리한다. MAC 유저들에게는 필수 프로그램 중에 하나다. 윈도우 환경에서는 **File Juggler** 라는 프로그램이 비교될 수 있긴 한데 정말, 졸라 비싸다. 결재창 열었다가 순간 닫았다. 한달 무료로 사용해 보니 **Hazel**에 비교할 수준은 아니다. 

이제 나는 고민한다. 
**inotifywait**를 계속 쓸 것인지 아니면, 예전처럼 **Clon**으로 돌아가 매 분마다 Script를 실행할 것인지 말이다. 편리성에 현혹되어 시작하였지만 소모되는 리소스 보다 필요성이 있는지에 대한 고민이다. 내 NAS의 램은 고작 2기가란 말이다. 