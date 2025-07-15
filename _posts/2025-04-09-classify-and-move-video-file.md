---
title: 영화, 드라마, 예능 자동 분류
date: '"2025-04-08 18:09:11 +0900"'
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

## 1. 기준을 정하다.

음악 파일인 **MP3**는 메타태그가 존재한다. 그 정보를 이용해 아티스트나 앨범으로 구분하거나 장르별로 나누어 저장이 가능하다. 하지만 **MP4**, **MKV** 같은 영상에는 메타태그가 없어서 그 영상을 만들어 배포하는 릴 그룹이 정한 제목에 한정되어 구분할 수 밖에 없다. 

대부분의 영상에는 **제목.시즌.에피소드.제작날자.화질.오디오.릴그룹명.확장자**로 대부분 만들어 배포된다. 이 중에서 제목,시즌,에피소드,제작날자로 구분하여 각 폴더별로 나누어 저장하려고 한다.

영화의 경우는 명확하다. 시즌과 에피소드의 구분이 없기 때문이다. 단순히 제목 뒤에 제작년도가 있거나 없을 수도 있다. 그러나 에피소드번호가 없기 때문에 영화로 명확히 구분 지을 수 있다.

예시) **영화** Mufasa.The.Lion.King.2024.2160p.4K.WEB.x265.10bit.AAC5.1-YTS.MX.mkv

---

문제는 드라마와 예능의 구분이다. 여기서 한발 더 나아가 다큐멘터리까지 구분하는 것은 거의 불가능에 가깝다. 명확한 제목을 명시하지 않고 모든 영상을 구분하려는 첫 목표가 희미해지는 순간이다. 아래 예시를 보면 난감하다. 제목 외엔 다 똑같기 때문이다. 특히 신병3은 시즌3인데 제목에 신병3이라고 명시해 놓았기 때문에 시즌으로 구분하기도 어렵다. 

예시) **드라마** 신병3.E01.250407.1080p.H264-F1RST.mp4
예시) **예   능** 골 때리는 그녀들.E165.250402.1080p.H264-F1RST.mp4

---

어쩔 수 없이 키워드를 미리 등록하는 방법으로 진행해야 한다. **ChatGPT**는 드라마는 신작이 많아 등록하기 어려우므로 반복이 많은 예능을 등록하는 것을 추천하고 있다. 그렇다면 내가 일주일 동안 즐겨보는 예능은 무엇인가? 를 따져야 한다. 그러고 보니 나는 TV를 안 본다. 내가 보고 싶은 예능은 대부분 스트리밍이 되기 때문이다. 그래서, 하지 말까?

**Cron** 등록은 하지 않더라도 만들었다.

---

## 2. 전체 구조 및 동작 요약

이 쉘 스크립트는 **NAS의 Downloads 폴더에 저장된 영상 파일(mp4, mkv)** 을 자동으로 분류해서  `/volume1/Movies`, `/volume1/TVdrama`, `/volume1/TVent`, `/volume1/TVdocu` 로 이동시키는 정리 자동화 도구이다. 

### 2.1. 파일 검사 및 준비
#### 2.1.1. **`log_message`**:로그 파일에 작업 내역 기록
```
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "/volume1/Tasks/logs/video_classifier_$(date +%Y-%m-%d).log"
}
```

#### 2.1.2. **`check_directory`**: 폴더가 없으면 생성
```
check_directory() {
    [ ! -d "$1" ] && mkdir -p "$1"
}
```

#### 2.1.3. **`move_with_unique_name`**: 이름 중복 시 `(1)`, `(2)` 붙임
```
move_with_unique_name() {
    local source_file="$1"
    local target_dir="$2"
    local base_name="$(basename "$source_file")"
    local name="${base_name%.*}"
    local ext="${base_name##*.}"
    local target_file="$target_dir/$base_name"
    local counter=1

    while [ -e "$target_file" ]; do
        target_file="$target_dir/${name}($counter).$ext"
        counter=$((counter + 1))
    done

    mv "$source_file" "$target_file"
    log_message "Moved: $source_file to $target_file"
}
```
---

###  2.2. 핵심 로직– `classify_and_move_video_file()`

이 함수가 실질적으로 파일을 분류하고 이동한다.

#### 2.2.1. 내부 동작
1. 파일명을 가져와서 변수에 저장
2. 키워드 기반 예능/다큐 판단
3. 예능 키워드 포함 여부 체크 - `is_TVent`
4. 다큐 키워드 포함 여부 체크 - `is_TVdocu`
```
classify_and_move_video_file() {
    local file="$1"
    local filename="$(basename "$file")"
    local base_name="${filename%.*}"
    local TVent_KEYWORDS=("때리는" "개그콘서트" "동물농장" "사장님")
    local TVdocu_KEYWORDS=("꼬리에" "세계속으로" "이슈 Pick" "세계사")
    local is_TVent=false
    local is_TVdocu=false

    for keyword in "${TVent_KEYWORDS[@]}"; do
        [[ "$filename" == *"$keyword"* ]] && is_TVent=true && break
    done

    for keyword in "${TVdocu_KEYWORDS[@]}"; do
        [[ "$filename" == *"$keyword"* ]] && is_TVdocu=true && break
    done

    local target_base=""
```

#### 2.2.2. 분류 조건 판단
```
if $is_TVdocu; then
    target_base="/volume1/TVdocu"
```

#### 2.2.3. 최종 경로 지정
- 영화는 그냥 /Movies에 넣고
- 예능/드라마/다큐는 제목별 하위폴더 생성
```
if [[ "$target_base" == "/volume1/Movies" ]]; then
        subfolder="$target_base"
    else
        series_name=... # 시리즈 이름 추출
        subfolder="$target_base/$series_name"
    fi
```

#### 2.2.4. 자막도 같이 이동
```
for sub_ext in srt smi ass; do
    subtitle_file="${file%.*}.$sub_ext"
    ...
done
```

---

### 2.3. 실행 파트
- Downloads 폴더에서 `.mp4`, `.mkv` 파일을 찾아
- 각각 `classify_and_move_video_file`에 전달해서 분류 실행
```
find "/volume1/Downloads" -type f \( -iname "*.mp4" -o -iname "*.mkv" \) \
    -exec bash -c 'classify_and_move_video_file "$1"' _ {} \;
```

---

## 3. 마무리 작업
이렇게 해서 Downloads 폴더의 영상 정리 자동화 스크립트를 마쳤다. 테스트 해보니 오류없이 제대로 진행되었다. 

다만 키워드로 등록한 단어가 실제 영상 제목에 반드시 존재 해야 작동한다. 만약 **"개그콘서트"** 라고 설정했는데 이름이 **"개 그 콘 서 트"** 라고 공백이 생기면 분류하지 못한다는 것이다. 그럴 경우에는 키워드에 "개그콘서트"와 "개 그 콘 서 트"를 함께 적어 넣어야 한다. 하지만 이 경우는 폴더 이름이 **"개 그 콘 서 트"** 가 되어 버린다.

그래서 공백이 없는 키워드로 설정하고 **공백 제거 코드**를 추가로 넣으면 조금 더 유연해 질 수 있다. 파일명을 가져올 때 이름부분에 공백이 있으면 제거를 한다. 그리고 타겟 폴더에 공백을 제거한 이름으로 폴더를 만들고, 그 안에 공백을 제거한 제목을 적용한 파일을 저장한다.

이렇게 코드를 마쳤다. 
```
bash /volume1/Tasks/classify.sh
```
실행했다. Downloads폴더에 잔뜩 쌓아 둔 파일이 사라지는 쾌감은 정말 짜릿하다.

아래는 완성된 전체 코드이다.
```
#!/bin/bash

# Downloads 안의 mp4, mkv 파일을 분석해서 Movies / TVdrama / TVent / TVdocu 로 구분 이동

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "/volume1/Tasks/logs/video_classifier_$(date +%Y-%m-%d).log"
}

check_directory() {
    [ ! -d "$1" ] && mkdir -p "$1"
}

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

    mv "$source_file" "$target_file"
    log_message "Moved: $source_file to $target_file"
}

classify_and_move_video_file() {
    local file="$1"
    local filename="$(basename "$file")"
    local base_name="${filename%.*}"
    local TVent_KEYWORDS=("때리는" "개그콘서트" "동물농장" "사장님")
    local TVdocu_KEYWORDS=("꼬리에" "세계속으로" "이슈Pick" "세계사")
    local is_TVent=false
    local is_TVdocu=false
    local clean_filename=$(echo "$filename" | tr -d '[:space:]')

    for keyword in "${TVent_KEYWORDS[@]}"; do
        [[ "$clean_filename" == *"$keyword"* ]] && is_TVent=true && break
    done

    for keyword in "${TVdocu_KEYWORDS[@]}"; do
        [[ "$clean_filename" == *"$keyword"* ]] && is_TVdocu=true && break
    done

    local target_base=""

    if $is_TVdocu; then
        target_base="/volume1/TVdocu"
    elif [[ "$filename" =~ ([Ss][0-9]{2})?[Ee][0-9]{2} ]]; then
        if $is_TVent; then
            target_base="/volume1/TVent"
        else
            target_base="/volume1/TVdrama"
        fi
    elif [[ "$filename" =~ ([12][0-9]{3}(0[1-9]|1[0-2])[0-3][0-9]) || "$filename" =~ ([12][0-9]{3})\.(0[1-9]|1[0-2])\.(0[1-9]|[12][0-9]|3[01]) ]]; then
        if $is_TVent; then
            target_base="/volume1/TVent"
        else
            target_base="/volume1/TVdrama"
        fi
    else
        target_base="/volume1/Movies"
    fi

    if [[ "$target_base" == "/volume1/Movies" ]]; then
        subfolder="$target_base"
    else
        series_name=$(echo "$clean_filename" | \
            sed -E 's/[ _.-]?[Ss]?[0-9]{0,2}[Ee][0-9]{2}.*//' | \
            sed 's/\.[^.]*$//' | tr '.' ' ' | sed 's/ *$//' | \
            awk '{ for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2)); print }')
        subfolder="$target_base/$series_name"
    fi

    check_directory "$subfolder"
    move_with_unique_name "$file" "$subfolder"
    log_message "Classified and moved: $file to $subfolder"

    for sub_ext in srt smi ass; do
        subtitle_file="${file%.*}.$sub_ext"
        [ -f "$subtitle_file" ] && move_with_unique_name "$subtitle_file" "$subfolder"
    done
}

# 함수 내보내기 (하위 셸에서 사용 가능하게)
export -f classify_and_move_video_file
export -f check_directory
export -f move_with_unique_name
export -f log_message

# 실행
find "/volume1/Downloads" -type f \( -iname "*.mp4" -o -iname "*.mkv" \) \
    -exec bash -c 'classify_and_move_video_file "$1"' _ {} \;
```