---
title: NAS-Auto-Watch-System-6
date: '"2025-04-08 13:55:15 +0900"'
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
  - initify
  - inotifywait
  - inotify-tools
pin: false
comments: "true"
image: /assets/img/linux-title02.webp
---

이전 글에 이어 한참을 고민하다 Synology NAS, DSM에 있는 **Task Scheduler**를 사용하기로 했다. 며칠을 사용해 보니 내가 원하지 않는 상황이 생겼다. 그래서 다시 스크립트를 수정하고 원래 방식대로 돌아갔다. 다만 **ChatGPT**의 도움으로 많이 개선한 스크립트를 만들었다.

**inotify**는 실시간 감시 프로그램이기 때문에 부족한 부분이 발생한다. 완벽한 스크립트를 구성해서 실행시키면 분명 좋은 결과가 발생할 수 있겠지만, 나는 아직 많이 모자르다. **inotify**는 감시하는 폴더에 이벤트가 발생할 경우에 작동한다. 그 이벤트 발생 이전에 저장된 파일이나 폴더는 감시대상이 아니다. 이 부분을 해결하기 위해서는 이벤트 발생시, 이전 생성된 파일이나 폴더가 있는지 검토하게 만들어야 한다. 

만들면 되지.
그런데 **Task Scheduler**에 등록해서 사용하는 법과 비교했을 때 무엇이 더 좋은가 에 대한 궁금증이다. 이벤트가 발생했을 때 이벤트 상황을 처리하고 이전 추가로 발생한 작업들을 재 처리하는 스크립트와 매 분마다 실행하여 감시 폴더에 있는 모든 파일과 폴더를 대상으로 작업을 하는 스크립트.

여기서 나는 선택했다. 저사양에서 돌아가는 Synology NAS의 리소스를 무시해가면 사용하는 것 보다, 정상적으로 **Task Scheduler**에 등록해서 관리하는 것이 모든 면에서 편리하다는 것을. 그리고 다시 스크립트를 조절해서 최종을 만들었다. 

```
#!/bin/bash

# -------------------- 설정 --------------------
LOG_DIR="/volume1/Tasks/Logs"
LOG_FILE="$LOG_DIR/file_organizer_$(date +%Y-%m-%d).log"
 
WATCH_DIRS=("/volume1/Downloads" "/volume1/Temp")
MOVIE_DIR="/volume1/Movies"
CACHE_DIR="/volume1/Tasks/Cache"
EPUB_DIR="/volume1/Ebook/Epub"
PDF_DIR="/volume1/Ebook/Pdf"
AXI_DIR="/volume1/Axi"
MUSIC_DIR="/volume1/Music"
PHOTO_DIR="/volume1/photo"
  
# -------------------- 공통 함수 --------------------
mkdir -p "$LOG_DIR"
  
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}
  
check_directory() {
    local dir=$1
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir" || { log_message "Failed to create directory: $dir"; exit 1; }
        log_message "Created missing directory: $dir"
    fi
}
  
check_file_stable() {
    local file=$1
    local timeout=10
    local initial_size=$(stat -c %s "$file")
    local current_size=$initial_size
    for ((i=0; i<$timeout; i++)); do
        sleep 1
        current_size=$(stat -c %s "$file")
        [ "$initial_size" -eq "$current_size" ] && return 0
    done
    return 1
}
  
move_with_unique_name() {
    local source_file=$1
    local target_dir=$2
    local base_name="$(basename "$source_file")"
    local name="${base_name%.*}"
    local ext="${base_name##*.}"
    local target_file="$target_dir/$base_name"
    local counter=1
  
    while [ -e "$target_file" ]; do
        target_file="$target_dir/${name}($counter).$ext"
        counter=$((counter + 1))
    done
  
    mv "$source_file" "$target_file" || { log_message "Failed to move file: $source_file"; exit 1; }
    log_message "Moved file: $source_file to $target_file"
}
  
# -------------------- Downloads 처리 --------------------
process_Downloads_directory() {
    local base_dir="/volume1/Downloads"
    check_directory "$base_dir"
    Downloads_move_epub_files "$base_dir"
    Downloads_move_pdf_files "$base_dir"
    Downloads_move_srt_and_smi_files "$base_dir"
    Downloads_move_png_and_jpg_files "$base_dir"
}
  
Downloads_move_epub_files() {
    local base_dir=$1
    find "$base_dir" -type f -iname "*.epub" | while read FILE; do
        if check_file_stable "$FILE"; then
            check_directory "$EPUB_DIR"
            move_with_unique_name "$FILE" "$EPUB_DIR"
        else
            log_message "Skipped unstable EPUB file: $FILE"
        fi
    done
}
  
Downloads_move_pdf_files() {
    local base_dir=$1
    find "$base_dir" -type f -iname "*.pdf" | while read FILE; do
        if check_file_stable "$FILE"; then
            check_directory "$PDF_DIR"
            move_with_unique_name "$FILE" "$PDF_DIR"
        else
            log_message "Skipped unstable PDF file: $FILE"
        fi
    done
}
  
Downloads_move_srt_and_smi_files() {
    local base_dir=$1
    find "$base_dir" -type f \( -iname "*.smi" -o -iname "*.srt" \) | while read FILE; do
        if check_file_stable "$FILE"; then
            check_directory "$MOVIE_DIR"
            move_with_unique_name "$FILE" "$MOVIE_DIR"
        else
            log_message "Skipped unstable SRT/SMI file: $FILE"
        fi
    done
}
  
Downloads_move_png_and_jpg_files() {
    local base_dir=$1
    find "$base_dir" -type f \( -iname "*.jpg" -o -iname "*.png" \) | while read FILE; do
        if check_file_stable "$FILE"; then
            check_directory "$PHOTO_DIR"
            move_with_unique_name "$FILE" "$PHOTO_DIR"
        else
            log_message "Skipped unstable PNG/JPG file: $FILE"
        fi
    done
}
  
# -------------------- Temp 처리 --------------------
process_Temp_directory() {
    local base_dir="/volume1/Temp"
    check_directory "$base_dir"
    Temp_move_epub_files "$base_dir"
    Temp_move_pdf_files "$base_dir"
    Temp_move_srt_and_smi_files "$base_dir"
    Temp_delete_opf_and_jpg_files "$base_dir"
}
  
Temp_move_epub_files() {
    local base_dir=$1
    find "$base_dir" -type f -iname "*.epub" | while read FILE; do
        if check_file_stable "$FILE"; then
            check_directory "$EPUB_DIR"
            move_with_unique_name "$FILE" "$EPUB_DIR"
        else
            log_message "Skipped unstable EPUB file: $FILE"
        fi
    done
}
  
Temp_move_pdf_files() {
    local base_dir=$1
    find "$base_dir" -type f -iname "*.pdf" | while read FILE; do
        if check_file_stable "$FILE"; then
            check_directory "$PDF_DIR"
            move_with_unique_name "$FILE" "$PDF_DIR"
        else
            log_message "Skipped unstable PDF file: $FILE"
        fi
    done
}
  
Temp_move_srt_and_smi_files() {
    local base_dir=$1
    find "$base_dir" -type f \( -iname "*.smi" -o -iname "*.srt" \) | while read FILE; do
        if check_file_stable "$FILE"; then
            check_directory "$MOVIE_DIR"
            move_with_unique_name "$FILE" "$MOVIE_DIR"
        else
            log_message "Skipped unstable SRT/SMI file: $FILE"
        fi
    done
}
  
Temp_delete_opf_and_jpg_files() {
    local base_dir=$1
    find "$base_dir" -type f \( -iname "*.opf" -o -iname "*.jpg" \) | while read FILE; do
        rm -f "$FILE" && log_message "Deleted file: $FILE"
    done
}
  
# -------------------- 정리 함수 --------------------
cleanup_Downloads_directory() {
    local base_dir="/volume1/Downloads"
    find "$base_dir" -mindepth 1 -type d -empty -delete
    log_message "Deleted empty subdirectories in $base_dir"
}
  
cleanup_Temp_directory() {
    local base_dir="/volume1/Temp"
    find "$base_dir" -mindepth 1 -type d -empty -delete
    log_message "Deleted empty subdirectories in $base_dir"
}
  
cleanup_old_cache_files() {
    local cache_dir="/volume1/Tasks/Cache"
    find "$cache_dir" -type f -mtime +7 -exec rm -f {} \;
    log_message "Deleted files older than 7 days in $cache_dir"
}
  
cleanup_syno_cache_files() {
    local cache_dir="/volume1/Tasks/Cache"
    find "$cache_dir" -name '*@SynoEAStream' -delete
    log_message "Deleted Synology cache stream files in $cache_dir"
}
  
cleanup_old_logs() {
    find "$LOG_DIR" -type f -name "file_organizer_*.log" -mtime +30 -exec rm -f {} \;
    log_message "Deleted logs older than 30 days"
}
 
# -------------------- 실행 --------------------
log_message "Starting file organizer script..."
  
check_directory "/volume1/Downloads"
check_directory "/volume1/Temp"
  
cleanup_old_logs
process_Downloads_directory
process_Temp_directory
cleanup_Temp_directory
cleanup_Downloads_directory
cleanup_old_cache_files
cleanup_syno_cache_files
  
log_message "File organizer script completed."
```

이제는 다운되는 영상 파일을 자동으로 구분하여 아래 폴더에 각각 저장하는 스크립트를 만들어 보려 한다.

/volume1/Movies/
/volume1/TVShows/
/volume1/Documentaries/

누구와? **ChatGPT**와...