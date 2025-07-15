---
title: Linux, 영화, 드라마, 예능 분류 스크립트 분석
date: 2025-04-15T20:06:05
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
  - 영상자동분류
pin: false
comments: "true"
image: /assets/img/linux-title03.webp
---

## 1. 감시 폴더의 파일 분류

이 글은 이전 포스트 <a href="https://xixsxix.github.io/posts/Ubuntu-in-Nas/" target="_blank"># Synology NAS, Ubuntu 설치와 백업</a> 에서 설명한 내 나스에서 잘 돌아가고 있는 파일 분류 스크립트에 대한 분석이다. 간단한 내용인데 이것 저것 포함하다 보니 무척 길어졌다. 이 스크립트는 정리가 필요한 지정 폴더의 정의 설정과 공통 함수, Downloads 폴더에 저장되는 파일 처리, 비디오와 파일 분류, 이동 후 남은 파일과 폴더 청소, 그리고 마지막으로 실행 순서를 정리했다. 그리고 각 부분에 로그를 넣었는데 처리 결과만 기록하게 해 두었다. 

---

## 2. 폴더 위치와 그 정의

스크립트의 첫 부분은 감시 폴더를 지정한다. 이 스크립트가 항상 지켜보아야 할 곳은 `/volume1/downloads` 폴더이다. 이 폴더에 저장되는 모든 파일은 이 스크립트에 의해 삭제되거나 이동한다. copy는 있을 수 없다. copy 명령을 하면 스크립트에 의해 무한으로 파일이 복사될 것이다. 우선 `/volume1/downloads`를 WATCH_DIR로 명명하고 `WATCH_DIR="/volume1/Downloads"` 이라고 지정한다. 

그 다음은 이동되는 파일이 저장되는 폴더들을 지정해야 한다. 나는 epub과 pdf를 Ebook 안의 Epub과 Pdf 폴더에 저장할 것이다. 음악은 Music, 이미지는 photo로 저장한다. 그리고 mp4, mkv는 지난 번 포스트 <a href="https://xixsxix.github.io/posts/classify-and-move-video-file/" target="_blank"># 영화, 드라마, 예능 자동 분류</a>에서 설명한 대로 릴 그룹이 지정한 파일 이름을 분석하여 드라마와 다큐 그리고 예능으로 구분할 것이다. 드라마, 예능, 다큐에도 속하지 않는 영상은 모두 영화이므로 Movies 폴더에 저장하도록 만들었다. 

설정은 이렇다.
```
WATCH_DIR="/volume1/Downloads" # 감시 폴더

MOVIE_DIR="/volume1/Movies"    # 영화
TVENT_DIR="/volume1/TVent"     # 예능
TVDOCU_DIR="/volume1/TVdocu"   # 다큐
TVDRAMA_DIR="/volume1/TVdrama" # 드라마

AXI_DIR="/volume1/Axi"         # 개인

EPUB_DIR="/volume1/Ebook/Epub" # Epub
PDF_DIR="/volume1/Ebook/Pdf"   # pdf
MUSIC_DIR="/volume1/Music"     # 음악
PHOTO_DIR="/volume1/photo"     # 사진
```

필요한 폴더에 대해 그 제목을 지정하면 함수에서 제목을 별명으로 사용한다. 직접 경로를 입력해도 상관없지만 후에 수정이 있을 경우에 무수히 많은 함수를 전부 고치지 않고 이 설정만 변경하면 되기 때문에 미리 지정해서 사용하는 것이 좋다.

---
## 3. 로그의 시작

백그라운드에서 진행되는 스크립트의 진행 과정을 볼 수가 없어 로그의 기록에 의존해야 한다. 로그는 없어도 되지만 초반에는 오류를 확인해야 하기 때문에 필요할 것이다. 스크립트가 완성이 되면 파일 이동의 위치 정도만 있어도 된다.

```
LOG_DIR="/volume1/Tasks/Logs"
# 로그가 저장될 폴더의 별명과 저장 경로를 지정한다.

LOG_FILE="$LOG_DIR/file_organizer_Downloads_$(date +%Y_%m_%d).log"
# 경로에 저장되는 로그 파일의 이름을 지정한다. 지정된 이름 뒤에 _2025_04_15.log가 붙으며 하루에
한개의 파일이 생성된다.

mkdir -p "$LOG_DIR"
# 만일 폴더가 없다면 만든다.

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}
# 로그를 기록한다. date 명령으로 [YYYY-MM-DD HH:MM:SS] 형식으로 기록될 것이고 $1 함수에 전달된
인수를 받아 발생하는 함수의 결과를 기록한다.
예시 : [2025-04-15 14:32:10] 파일이 이동되었습니다.
```

---

## 4. 공통 함수

조건이 많으면 각 부분에 들어가는 공통적인 함수가 존재한다. 그 함수를 개별로 넣는 것 보다 함수의 이름을 정하고 각 함수에서 그 이름을 호출하는 것이 수정과 관리 차원에서 편리하다.

### 4.1 check_directory

이 함수는 입력받은 디렉토리가 존재하는지 확인하고, 존재하지 않으면 생성하는 함수이다.
```
# ---------- 공통 함수 ----------
check_directory() {
    local dir=$1
    [ ! -d "$dir" ] && mkdir -p "$dir"
}
```

1. 함수의 이름을 **`check_directory`** 로 정했다.
2. **`local dir=$1`**은 이 함수 내에서만 유효한 변수로 선언한다. 
3. **`$1`** : 함수의 첫번째 인수를 `dir` 변수에 할당한다.즉 `check_directory()` 함수가 호출될 때 전달된 디렉토리 경로가 `dir` 변수에 저장된다.
4. **`[ ! -d "$dir" ]`** : `-d`는 주어진 경로가 디렉토리인지 확인하는 조건이다. `!`는 부정을 의미하므로 디렉토리가 존재하지 않으면 참이 된다. 즉 `$dir`에 해당하는 경로가 디렉토리가 아니거나 존재하지 않을 경우 이 조건은 참이 된다.
5. **`&& mkdir -p "$dir"`** : && 구문은 앞의 조건이 참일 경우에 뒤의 명령을 실행한다.
6. **`mkdir -p "$dir"`** : 디렉토리를 생성하는 명령이다. `-p`는 상위 디렉토리가 없으면 함께 생성하는 옵션이다.

---

### 4.2 check_file_stable

다운로드 되는 파일이 완전히 저장되기 이전에 스크립트가 이동시키는 것을 방지하기 위해서 설정한다. 파일의 크기가 작은 경우는 상관 없을 수 있지만 영상처럼 큰 파일은 저장되기 까지 시간이 걸리므로 함수를 넣어 오류를 방지해야 한다. 

이 함수는 주어진 파일의 크기를 10초 동안 1초 간격으로 확인하면서, 파일 크기가 변하지 않으면 파일이 "불안정"하다고 판단하고 로그를 기록한다. 파일 크기가 일정 시간 동안 변하지 않으면 1을 반환하고, 변하면 안정적인 파일로 판단하여 0을 반환한다.

```
# ---------- 공통 함수 ----------
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
    log "파일 불안정: $file"
    return 1
}
```

1. **`check_file_stable()`**: 함수의 정의이다.
2. **`local file=$1`**: 첫 번째 인수를 `file` 변수에 할당한다.
3. **`local timeout=10`**: 파일 크기를 확인할 최대 반복 횟수를 설정한다. 10초 동안 파일 크기가 변하지 않으면 불안정하다고 판단하고, 함수를 종료한다.
4. **`local initial_size=$(stat -c %s "$file")`**: `stat`명령을 사용하여 크기를 바이트 단위로 확인한다. `-c %s` 옵션은 파일의 크기만 출력하는 옵션이다.
5. **`local current_size=$initial_size`**: `current_size` 변수에 `initial_size` 값을 초기화한다. 이 변수는 파일 크기가 변할 때마다 확인할 값이다.
6. `for ((i=0; i<$timeout; i++)); do` : `for` 루프는 최대 `timeout` 횟수만큼 반복한다. 기본값은 10이므로 10번 반복하며, 1초 간격으로 파일의 크기를 확인한다.
7. `sleep 1`: 1초 동안 기다린다. 파일 크기를 확인하는 간격을 1초로 설정한다.
8. `current_size=$(stat -c %s "$file")`: 매번 루프가 실행될 때마다 파일 크기를 다시 확인한다.
9. `[ "$initial_size" -eq "$current_size" ]`: `initial_size`와 `current_size`가 같으면, 즉 파일 크기가 변하지 않으면 조건이 참이 된다. 
10. `&& return 0` : 조건이 참일 경우 함수가 0을 반환하고 종료한다. 파일이 안정적이라고 판단한 것이다.
11. `done`: 앞 쪽의 `for` 루프의 끝을 나타낸다.
12. `log "파일 불안정: $file"`: 파일 크기가 일정 시간 동안 변하지 않으면, `log()` 함수로 "파일 불안정"이라는 메시지를 로그 파일에 기록한다. `$file`은 해당 파일 경로.
13. `return 1`: 파일 크기가 10초 동안 변하지 않으면, 1을 반환하여 함수가 실패했음을 나타낸다. 1은 실패를 의미한다.

---

### 4.3 move_with_unique_name

스크립트가 파일을 지정한 폴더로 이동시키는데 그 폴더에 같은 이름이 있을 경우, 이동에 실패하거나 기존에 있던 파일을 덮어 씌우는 사건이 발생할 수 있다. 이동 명령이므로 지정한 폴더에 있던 파일은 삭제되고 만다. 

이 함수는 파일을 이동시키는 역할을 담당하고 있다. 대상 디렉토리에 같은 이름의 파일이 존재하면, 파일 이름에 번호를 추가하여 생성하고 이동시킨다.

```
# ---------- 공통 함수 ----------
move_with_unique_name() {
    local source_file="$1"
    local target_dir="$2"
    local original_name="$(basename "$source_file")"
    local base_name="$(echo "$original_name" | tr -d '[:space:]')"
    local name="${base_name%.*}"
    local ext="${base_name##*.}"
    local target_file="$target_dir/$base_name"
    local counter=1
  
    while [ -e "$target_file" ]; do
        target_file="$target_dir/${name}($counter).$ext"
        counter=$((counter + 1))
    done
  
    if mv "$source_file" "$target_file" 2>>"$LOG_FILE"; then
        log "이동됨: $source_file → $target_file"
    else
        log "[ERROR] 이동 실패: $source_file → $target_file"
    fi
}
```

1. **`move_with_unique_name()`**: 
	- 함수의 정의이다.
2. **`local source_file="$1"`**: 
	- 첫 번째 인수로 이동할 파일의 경로를 담는다.
3. **`local target_dir="$2"`**:  
	- 두 번째 인수로 파일을 이동시킬 대상 디렉토리 경로이다.
4. **`local original_name="$(basename "$source_file")"`**: 
	- `basename "$source_file"`는 파일 경로에서 파일 이름만 추출하고, `original_name`변수에 저장한다.
5. **`local base_name="$(echo "$original_name" | tr -d '[:space:]')"`**:
	- 파일 이름에 공백을 모두 제거한다. 이 값을 `base_name` 변수에 저장한다.
6. **`local name="${base_name%.*}"`**: 
	- 파일 확장자를 제외한 파일 이름을 추출하고 그 값을 `name`에 저장한다.
7. **`local ext="${base_name##*.}"`**: 
	- 파일 확장자를 추출하고 그 값을 'ext'에 저장한다.
8. **`local target_file="$target_dir/$base_name"`**: 
	- 대상 디렉토리와 원본 파일을 결합하여 생성된 전체 파일 경로를 `target_file`에 저장한다.
9. **`local counter=1`**: 
	- `counter`는 파일 이름에 번호를 붙여서 중복 파일을 피할 때 사용하는 변수로 처음에는 1로 설정된다.
10. **`while [ -e "$target_file" ]; do`**: 
	- 대상 파일이 이미 존재하는지 확인하는 조건이다.
11. **`target_file="$target_dir/${name}($counter).$ext"`**: 
	- `target_file`을 `name` 뒤에 `($counter)`를 추가한 형식으로 변경한다. 
12. **`counter=$((counter + 1))`**: 
	- `counter` 값을 1 증가시킨다.
13. **`done`**: 
	- `while` 루프가 끝나는 부분이다. 파일 이름이 유니크할 때까지 루프가 계속 반복된다.
14. **`if mv "$source_file" "$target_file" 2>>"$LOG_FILE"; then`**: 
	- `mv "$source_file" "$target_file"`는 실제로 파일을 이동하는 명령이다. 
	- `2>>"$LOG_FILE"`는 오류 메시지를 `$LOG_FILE`에 기록한다.
15. **`log "이동됨: $source_file → $target_file"`**:
	- 파일 이동이 성공하면, 이동된 파일 경로를 로그에 기록한다.
16. **`else`**:
	- 파일 이동이 실패하면, `else` 블록이 실행된다.
17. **`log "[ERROR] 이동 실패: $source_file → $target_file"`**:
	- 파일 이동이 실패한 경우 오류 메시지를 로그에 기록한다.
18. **`fi`**:
	- `if` 조건문이 끝나는 부분이다.

---

### 4.4 delete_small_files

토렌트에서 파일을 다운 받다 보면 사이트를 홍보하는 파일들이 들어 있는 경우가 많다. 이런 파일중에 `.url`이나 `.txt` 파일들도 있지만 `.mp4, mkv` 등의 비디오 파일이 있어 수동으로 구분하여 삭제하여야 한다. 하지만 이러한 영상은 크기가 작기 때문에 미리 지정하여 그 이하의 파일은 삭제하도록 했다.

```
# ---------- 공통 함수 ----------
delete_small_files() {
    local base_dir=$1
    find "$base_dir" -type f \( -iname "*.mkv" -o -iname "*.mp4" \) -size -10M | while read FILE; do
        rm -f "$FILE"
        log "작은 파일 삭제됨: $FILE"
    done
}
```

1. **`delete_small_files()`**:
	- 함수 이름을 정의한다.
2. **`local base_dir=$1`**:
	- `base_dir=$1`: 첫 번째 인수를 `base_dir` 변수에 할당한다.
3. **`find "$base_dir" -type f \( -iname "*.mkv" -o -iname "*.mp4" \) -size -10M`**:
	- `find`: 파일이나 디렉토리를 검색하는 명령어
	- `"$base_dir"`: 검색할 기본 디렉토리. 이 디렉토리 내에서 파일을 검색한다.
	- `-type f`: 파일만 검색한다.
	- `\( -iname "*.mkv" -o -iname "*.mp4" \)`: `.mkv` 또는 `.mp4` 확장자를 가진 파일만 찾는다. `-iname` 옵션은 대소문자를 구분하지 않기 때문에 `.MKV`나 `.MP4`도 포함된다.
	- `-size -10M`: 크기가 10MB보다 작은 파일을 찾는다. `-10M`은 "10MB 미만"을 의미.
4. **`| while read FILE; do`**:
	- `find` 명령의 결과를 `while` 루프에 전달한다. 
	- `while read FILE; do`: `find` 명령으로 반환된 파일 경로들을 하나씩 읽어서 `FILE` 변수에 저장하고, 루프 내에서 처리한다.
5. **`rm -f "$FILE"`**:
	- `rm` 은 파일을 삭제하는 명령어이고 `-f` 는 "강제 삭제"를 의미한다. 읽기 전용 파일도 삭제한다.
6. 이후 `log` 를 작성하고 `done`으로 함수를 마친다.

---

### 4.5 move_files

이 함수는 지정된 확장자를 가진 파일들을 특정 디렉토리로 이동하는 역할을 담당한다. 공통 함수에서 설정한 함수들을 여기에서 호출하여 파일이 안정적인지 확인하고, 중복된 파일의 이름을 유니크한 이름이 생성되게 하여 이동시킨다.

```
# ---------- 공통 함수 ----------
move_files() {
    local base_dir=$1
    local target_dir=$2
    shift 2
    for ext in "$@"; do
        find "$base_dir" -type f -iname "*.$ext" | while read FILE; do
            if check_file_stable "$FILE"; then
               check_directory "$target_dir"
               move_with_unique_name "$FILE" "$target_dir"
            fi
        done
    done
}
```

1. **`move_files()`**:
	- 함수의 이름을 정의한다.
2. **`local base_dir=$1`**:
	- 첫 번째 인수를 `base_dir` 변수에 할당한다.
3. **`local target_dir=$2`**: 
	- 두 번째 인수로 파일을 이동할 대상 디렉토리이다.
4. **`shift 2`**:
	- 첫 번째와 두 번째 인수(`$1`과 `$2`)를 "왼쪽으로" 밀어서 제거한다. 그래서 `$@`에는 이제 확장자 목록만 남게 된다.
	- 예를 들어, `move_files /path/to/source /path/to/target mp4 mkv avi`라고 호출되면, `base_dir`과 `target_dir`은 각각 `/path/to/source`와 `/path/to/target`으로 설정되고, `$@`는 `mp4 mkv avi`와 같이 확장자 목록을 가진다.
5. **`for ext in "$@"; do`**:
	- `"$@"`에 포함된 확장자 목록을 반복문으로 처리한다. 폴더에 들어 있는 파일들의 확장자를 기준으로 파일을 검색하고, 지정된 확장자와 일치하는 파일들을 처리한다.
6. **`find "$base_dir" -type f -iname "*.$ext"`**:
	- 지정한 디렉토리에서 파일만 검색하고 확장자가 `$ext`인 파일을 찾는다. 
	- 확장자를 검색하는 옵션은 여러가지가 있는데 `-iname`은 대소문자를 구분하지 않기 때문에 많이 사용한다.
7. **`| while read FILE; do`**:
	- `find` 명령어의 결과를 `while` 루프를 통해 처리한다. `FILE` 변수에 각 파일의 경로가 저장된다.
8. 위 공통 함수에서 설정한 함수들을 호출한다. 
	- **`if check_file_stable "$FILE"; then`**:
	- **`check_directory "$target_dir"`**:
	- **`move_with_unique_name "$FILE" "$target_dir"`**:
9. **`done, done`** :
	- 두 개의 루프를 끝내며 함수를 마친다.

---

## 5. process_AXI_files

특정 디렉토리에 조건이 맞는 파일들을 찾아 안정성을 확인한 후, 지정된 디렉토리로 이동시키는 역할을 담당한다. 이 함수는 파일의 이름에 특정한 문자를 포함한 `.mp4` 파일을 찾아 그 이름을 삭제한 후 이동시킨다. 이 함수는 비디오를 파일 이름으로 구분하여 분류하기 전에 가장 먼저 실행되어야 한다. 고유한 이름이 주어졌기 때문에 특정하기 쉽고, 먼저 분류되지 않는다면 영화 폴더로 이동하기 때문이다.

```
process_AXI_files() {
    local base_dir="/volume1/Downloads"
    local AXI_DIR="/volume1/Axi"
    check_directory "$base_dir"
  
    find "$base_dir" -type f | grep -i "special_text@" | grep -i ".mp4$" | while read -r FILE; do
        local filename="$(basename "$FILE")"
        local clean_filename="${filename//special_text@/}"
  
        if check_file_stable "$FILE"; then
           check_directory "$AXI_DIR"
           if mv "$FILE" "$AXI_DIR/$clean_filename"; then
                log "[AXI] 이동됨: \"$filename\" → \"$AXI_DIR/$clean_filename\""
            else
                log "[AXI] ERROR: 이동 실패 - \"$filename\""
            fi
        else
            log "[AXI] ERROR: 파일 불안정 - \"$filename\""
        fi
    done
}
```

1. **`process_AXI_files()`**:
	- 함수 이름을 정의한다.
2. **`local base_dir="/volume1/Downloads"`**:
	- `base_dir`는 `"/volume1/Downloads"`라고 정의하여 검색할 파일들이 위치한 기본 디렉토리라고 정의한다.
3. **`local AXI_DIR="/volume1/Axi"`**:
	- `AXI_DIR`는 파일을 이동할 대상 디렉토리다. 이 경우, `"/volume1/Axi"` 디렉토리로 파일을 이동한다.
4. **`check_directory "$base_dir"`**:
	- 공통 함수에서 설정한 `check_directory`를 호출하여 `$base_dir`이 있는지 확인하고 없으면 해당 디렉토리를 생성한다.
5. **`find "$base_dir" -type f | grep -i "special_text@" | grep -i ".mp4$"`**:
	- 실질적인 명령어로서 `$base_dir`에서 모든 파일을 찾고 `"special_text@"` 문자열이 포함되고 `".mp4"`를 가진 확장자를 골라 낸다. `-i` 옵션은 대소문자를 구분하지 않는다.
6. **`while read -r FILE; do`**:
	- `find`와 `grep` 명령어의 출력 결과로 반환된 파일 경로들을 하나씩 처리하는 루프가 시작된다. 각 파일 경로는 `FILE` 변수에 저장된다.
7. **`local filename="$(basename "$FILE")"`**:
	- 파일 경로에서 파일 이름만 추출하여 `filename` 변수에 저장한다. `basename` 명령어는 파일 경로에서 파일 이름만 반환한다.
8. **`local clean_filename="${filename//special_text@/}"`**:
	- `"special_text@"` 문자열을 제거하여 `clean_filename`을 생성한다. 예를 들어, `"special_text@video.mp4"`는 `"video.mp4"`로 변경된다.
9. **`if check_file_stable "$FILE"; then`**:
	- 파일이 안정적인지 확인하는 공통 함수
10. **`check_directory "$AXI_DIR"`**:
	- `$AXI_DIR` 디렉토리가 존재하는지 확인하는 공통 함수
11. **`if mv "$FILE" "$AXI_DIR/$clean_filename"; then`**:
	- 파일을 `$AXI_DIR` 디렉토리로 이동한다. 파일이름은 `clean_filename`이 된다.
	- 만약 이동이 성공하면, `then` 블록에 들어가고, 실패하면 `else` 블록이 실행된다.
그 이후는 로그 기록 설정이다.

---

## 6. process_Downloads_directory

이제 `Downlaods` 디렉토리에 저장된 파일 중에 단순한 파일을 이동시킨다. 위에서 설명한 공통 함수에서 크기가 작은 파일을 삭제하고, `move_files` 함수를 호출하여 지정된 확장자를 가진 파일을 각각의 디렉토리로 이동한다. 그리고 이동이 끝나면 마지막 줄에 있는 `process_downloads_video_files`의 함수를 호출하고 종료한다.

```
process_Downloads_directory() {
    local base_dir="/volume1/Downloads"
    check_directory "$base_dir"
  
    # 작은 파일 삭제
    delete_small_files "$base_dir"
    
    # 파일 이동 및 분류 작업
    move_files "$base_dir" "$EPUB_DIR" "epub"
    move_files "$base_dir" "$PDF_DIR" "pdf"
    move_files "$base_dir" "$MUSIC_DIR" "mp3,flac,wav"
    move_files "$base_dir" "$PHOTO_DIR" "jpg,jpeg,png,gif"

	# 비디오 파일 처리 함수 호출
    process_downloads_video_files "$base_dir"
}
```

---

## 7. process_downloads_video_files

이 함수는 주어진 디렉토리에서 비디오 파일과 자막 파일을 검색하고, 파일이 안정적인지 확인한 후, 안정적이면 `classify_and_move_video_files` 함수를 호출하여 파일을 분류하고 이동시킨다. 

```
process_downloads_video_files() {
    local base_dir=$1
    find "$base_dir" -type f \( -iname "*.mp4" -o -iname "*.mkv" -o -iname "*.srt" -o -iname "*.smi" -o -iname "*.ass" \) | while read FILE; do
        if check_file_stable "$FILE"; then
            classify_and_move_video_files "$FILE"
        fi
    done
}
```

1. **`find "$base_dir" -type f \( -iname "*.mp4" -o -iname "*.mkv" -o -iname "*.srt" -o -iname "*.smi" -o -iname "*.ass" \)`**:
	- `"$base_dir"`에서 대소문자 구분없이 `.mp4, .mkv, .srt, .smi, .ass` 확장자를 가진 파일을 찾는다. 
2. **`| while read FILE; do`**:
	- `find`명령의 출력 결과를 `while` 루프를 통해 한줄씩 처리한다. 각 파일의 경로가 `FILE`에 저장되며 루프가 시작된다.
3. **`if check_file_stable "$FILE"; then`**:
	- 공통 함수에서 설정한 함수가 호출되어 파일의 안정성을 검토한다.  
4. **`classify_and_move_video_files "$FILE"`**:
	- 파일이 안정적이면 이 함수가 호출된다.

---

## 8. classify_and_move_video_files

이 함수가 이 스크립트의 가장 핵심인 부분이다. 주어진 비디오 파일을 분류하고 적절한 디렉토리로 이동시키는 작업을 수행한다. 함수의 주요 작업은 릴 그룹이 만든 비디오 파일의 이름 내에서 비디오 파일이 속할 카테고리를 결정한 후, 해당 디렉토리로 이동시키는 것이다. 여러 조건을 통해 분류하고 디렉토리를 생성하고 이동시킨다. 비디오 파일의 자세한 분류는 지난 포스트 <a href="https://xixsxix.github.io/posts/classify-and-move-video-file/" target="_blank"># 영화, 드라마, 예능 자동 분류</a>에 기록되어 있다.

```
# -------------------- 파일 분류 및 이동 --------------------
classify_and_move_video_files() {
    local file="$1"
    local filename="$(basename "$file")"
    local TVent_KEYWORDS=("때리는" "개그콘서트" "동물농장" "사장님")
    local TVdocu_KEYWORDS=("이슈Pick" "세계사" "쓸데없는" "영화가")
    local is_TVent=false
    local is_TVdocu=false

    for keyword in "${TVent_KEYWORDS[@]}"; do
        [[ "$filename" == *"$keyword"* ]] && is_TVent=true && break
    done
  
    for keyword in "${TVdocu_KEYWORDS[@]}"; do
        [[ "$filename" == *"$keyword"* ]] && is_TVdocu=true && break
    done
  
    local target_base=""
  
    if $is_TVdocu; then
        target_base="$TVDOCU_DIR"
    elif [[ "$filename" =~ ([Ss][0-9]{2})?[Ee][0-9]{2} ]]; then
        if $is_TVent; then
            target_base="$TVENT_DIR"
        else
            target_base="$TVDRAMA_DIR"
        fi
    elif [[ "$filename" =~ ([12][0-9]{3}(0[1-9]|1[0-2])[0-3][0-9]) || "$filename" =~ ([12][0-9]{3})\.(0[1-9]|1[0-2])\.(0[1-9]|[12][0-9]|3[01]) ]]; then
        if $is_TVent; then
            target_base="$TVENT_DIR"
        else
            target_base="$TVDRAMA_DIR"
        fi
    else
        target_base="$MOVIE_DIR"
    fi
  
    if [[ "$target_base" == "$MOVIE_DIR" ]]; then
        subfolder="$target_base"
    else
        # 폴더 이름에서 점을 공백으로 바꿔줌
        series_name=$(echo "$filename" | \
            sed -E 's/[ _.-]?[Ss]?[0-9]{0,2}[Ee][0-9]{2}.*//' | \
            sed 's/\.[^.]*$//' | tr '.' ' ' | sed 's/ *$//' | \
            awk '{ for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2)); print }')
        subfolder="$target_base/$series_name"
    fi
  
    # 폴더 생성
    check_directory "$subfolder"
    # 파일 이동
    move_with_unique_name "$file" "$subfolder"
}
```

### 8.1 `file`:  입력 파라미터
함수가 처리할 **파일 경로**. 이 파일은 비디오 파일(예: `.mp4`, `.mkv`, 자막 파일 등)로, 이후에 분류되어 적절한 디렉토리로 이동된다.

### 8.2 `filename="$(basename "$file")"`
파일 경로에서 파일 이름만 추출하여 `filename` 변수에 저장한다.

### 8.3 `TVent_KEYWORDS`와 `TVdocu_KEYWORDS`
각각 예능과 다큐 카테고리에 해당하는 키워드 목록을 포함하고 있다. 비디오 이름에 있는 정보로는 예능과 다큐를 구분할 수 없기 때문에 키워드를 미리 입력해야 한다. 이 키워드를 기준으로 두 분류를 구분한다.

### 8.4 예능 및 다큐 체크
1. `for keyword in "${TVent_KEYWORDS[@]}"`: `TVent_KEYWORDS` 배열에 있는 키워드를 하나씩 확인하면서, 파일 이름에 해당 키워드가 포함되어 있으면 `is_TVent=true`로 설정한다. 

2. `for keyword in "${TVdocu_KEYWORDS[@]}"`: `TVdocu_KEYWORDS` 배열에 있는 키워드를 하나씩 확인하면서, 파일 이름에 해당 키워드가 포함되어 있으면 `is_TVdocu=true`로 설정합니다.
3. `[[ "$filename" == *"$keyword"* ]] && is_TVdocu=true && break`: 파일 이름에 키워드가 포함되어 있으면 각각 `is_TVent=true`, `TVdocu=true`로 설정된다. 키워드가 포함이 되어 있으면 `&& break` 루프는 종료된다. 키워드를 다 찾았기 때문에 불필요한 반복을 방지하는 역할을 한다.

### 8.5 `local target_base=""`
빈 문자열로 `target_base` 변수를 초기화 한다는 뜻이다.

### 8.6 `target_base` 결정
1. 파일이 **다큐**인 경우 (`is_TVdocu`가 `true`):
	- `target_base="$TVDOCU_DIR"`: 다큐 파일은 `TVDOCU_DIR` 디렉토리로 이동한다.

2. 파일이 **예능** 또는 **드라마**인 경우:
	- `[[ "$filename" =~ ([Ss][0-9]{2})?[Ee][0-9]{2} ]]`: 파일 이름에 **시즌/에피소드 번호**가 포함되어 있으면 해당 파일을 예능 또는 드라마로 분류한다.
	- 예를 들어, `S01E01` 형식의 문자열을 포함하면 예능(`TVENT_DIR`) 또는 드라마(`TVDRAMA_DIR`)로 분류한다.
3. **영화**:
	- 만약 파일이 드라마나 예능으로 분류되지 않으면, 영화 파일로 간주하여 `MOVIE_DIR`로 이동한다.

### 8.7 `series_name` 추출
1. **시리즈 이름을 추출**하여 폴더 이름을 만든다. 파일 이름에서 시즌, 에피소드 번호를 제외하고, 나머지 부분을 시리즈 이름으로 사용한다.
2. `sed`, `tr`, `awk` 등을 사용하여 파일 이름에서 불필요한 문자들을 제거하고, 첫 글자를 대문자로 바꾸어 **공백을 포함한 시리즈 이름**을 추출한다.
3. `series_name`은 `filename`에서 시즌과 에피소드 번호를 제거한 뒤, **폴더 이름을 적절히 변환**하여 생성한다.

### 8.8 디렉토리 생성
- `check_directory "$subfolder"`: 생성된 `subfolder` 경로가 존재하는지 확인하고, 없다면 새로 생성한다. 이 폴더는 비디오 파일이 이동될 목적지 폴더이다.

### 8.9 파일 이동
- `move_with_unique_name "$file" "$subfolder"`: 공통 함수 `move_with_unique_name` 을 호출하여, 파일을 지정된 폴더로 이동시킨다. 만약 같은 이름의 파일이 이미 있으면 번호를 붙여서 유니크한 파일 이름을 생성하고 이동합니다.


---
## 9. 정리 함수

Downlaods 폴더에 저장된 파일 중에 원하는 파일을 선택해서 지정한 폴더로 이동시켰다. 이제 Downloads 폴더에는 필요 없는 파일과 폴더가 남아 있다. 대부분 NAS의 DSM이 자동 생성하는 숨김 처리한 폴더나 파일이 대부분이고, macOS가 켜져 있다면 `.DS_Store` 파일이 존재할 것이다. 숨겨진 파일이 존재하면 폴더가 삭제되지 않는다. 그래서 폴더를 강제로 삭제하고 Downloads 폴더를 빈 폴더로 만들어 둔다.

```
cleanup_Downloads_directory() {
    local base_dir="/volume1/Downloads"
  
        find "$base_dir" -type d -name '@eaDir' -exec rm -rf {} +
        find "$base_dir" -type f \( -name '.DS_Store' -o -name 'Thumbs.db' -o -name '.AppleDouble' -o -name '._*' \) -delete
        find "$base_dir" -mindepth 1 -type d -exec rmdir --ignore-fail-on-non-empty {} \;
}
```

1. **`cleanup_Downloads_directory`**
	- 이 함수의 이름을 정의한다.

2. **`local base_dir="/volume1/Downloads"`**
	- 청소를 시작할 기준 디렉토리를 정한다.

3. **`find "$base_dir" -type d -name '@eaDir' -exec rm -rf {} +`**
	- `base_dir` 내에서 이름이 `@eaDir` 인 디렉토리를 찾아 강제로 삭제한다. `@eaDir`은 Synology NAS에서 생성되는 메타데이터 디렉토리이다.

4. **`find "$base_dir" -type f \( -name '.DS_Store' -o -name 'Thumbs.db' -o -name '.AppleDouble' -o -name '._*' \) -delete`**
	- 이름이 `.DS_Store, Thumbs.db, .AppleDouble, ._*`인 파일을 찾아 `-delete` 삭제한다. `._*`은 macOS에서 다른 시스템과 파일을 공유할 때 생성되는 임시 파일이다.

5. **`find "$base_dir" -mindepth 1 -type d -exec rmdir --ignore-fail-on-non-empty {} \;`**
	- `-mindepth 1` 자신을 제외하고 `-type d` 하위 디렉토리만 검색해서 `--ignore-fail-on-non-empty` 비어 있지 않은 디렉토리만 `rmdir` 삭제한다.

이 함수에서 걸러지지 않은 파일은 `chche` 폴더로 이동해서 7일이 지난 후 삭제 하는 함수도 있었다. 하지만 내 다운로드 습관상 그런 파일이 남지 않아 불필요하고, cache 폴더를 정리해야 하는 번거로움이 있어 지웠다. 

---

## 10. 실행 순서 및 호출

이제 모든 함수를 만들었으니 실행을 시켜야 한다. 위에 나열된 함수는 실행 순서가 아니다. 필요한 함수를 정리한 것 일 뿐. 실행을 하는 명령어는 이제 부터다. 각 함수의 이름을 정의한 것을 보면 알겠지만 `process_`로 시작하는 함수가 실행 함수들이다. 이제 여기서 `process_` 함수를 순서대로 호출하면 실행이 되고, 실행되는 함수 속에서 공통 함수를 호출하여 완성하게 된다.  

```
check_directory "/volume1/Downloads"
process_AXI_files
process_Downloads_directory
cleanup_Downloads_directory
log "스크립트 종료 시각: $(date)"
```

1. **`check_directory "/volume1/Downloads"`**
	- 공통함수 **`check_directory`** 를 불러 **`"/volume1/Downloads"`** 의 상태를 확인한다.
2. **`process_AXI_files`** 와 **`process_Downloads_directory`**
	-  두 **`precess_`** 함수를 불러 실행 시킨다. 실행 순서는 위에 설명했듯이 필요에 의해 순서를 정한다. 
3. **`cleanup_Downloads_directory`**
	- 실행이 종료된 후 불필요한 폴더와 파일을 청소한다.
4. **`log "스크립트 종료 시각: $(date)"`**
	- 마지막에 스크립트의 종료시각을 로그 기록에 남긴다. 진행할 폴더와 파일이 없으면 로그 기록에는 이 종료시각만 남게 된다.

---

이렇게 **`/volume1/Downlaods`** 폴더에 대한 자동 분류 스크립트를 소개했다. 이 스크립트는 **NAS**에 **Docker**로 **Ubuntu**까지 설치하게 만들었지만 충분히 만족하고 있다. 이 외에도 몇개의 스크립트가 함께 실행중이다. **macOS** 를 사용하다 **Windows** 로 넘어 오면서의 답답함을 스크립트로 그나마 풀 수 있어서 다행이다. 로컬PC에서도 스크립트를 만들고 **작업스케줄러**에 등록하면 NAS처럼 사용할 수 있다. 다만 로컬PC는 24시간이 아니기에. 그리고 **AutoHotket**까지 사용한다면 환상의 PC를 만들게 될 것이다. 