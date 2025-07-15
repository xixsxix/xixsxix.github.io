---
title: Synology NAS, Ubuntu 설치와 백업
date: '"2025-04-14 21:52:10 +0900"'
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
image: /assets/img/ChatGPTImage_07_52_39.png
---
## 1. Synology NAS 함수 오류, 실패의 원인은?

**Synology NAS**에 여러 폴더를 관리하고 자동화하기 위해 스크립트를 작성하기 시작했다. 특히 Torrent에서 받은 여러 파일을 자동으로 구분하여 각 폴더에 저장하는 자동 분류 스크립트에 대한  <a href="https://xixsxix.github.io/posts/classify-and-move-video-file/" target="_blank"># 영화,드라마,예능 자동분류</a>  포스트를 공개하기도 했었다. 하지만 스크립트에서 계속 오류가 났다. 로그에 실패 원인을 기록하게 해 두었지만 로그에도 기록되지도 않았다. 단순히 함수 오류라고 생각하고 수정을 거듭했지만 쉽지 않았다. 

많은 고민을 하던 중 뜻 밖의 원인을 알게 되었다. **Synology NAS**는 일반적인 설치형 리눅스 배포판과는 다르게 설계되어 있다고 한다. **Synology NAS**는 네트워크 저장소 기능이 중심이기 때문에 배포판 리눅스에 비해 자유롭게 커스터마이징할 수 없도록 제한이 되어 있다고도 한다. 사용자가 리눅스를 직접 다루는게 목적이 아닌 웹 UI를 통해 모든 걸 설정하게 설계되어 있기 때문이다. 

**Synology NAS**는 사용자 및 그룹 관리를 **DSM(DiskStation Manager)** 라는 자체 운영 체제를 통하여 직관적이고 단순하게 설정을 할 수 있다. 하지만 터미널에서 root 권한은 전체 시스템의 설정을 변경하는데 제약이 있다. 반면 **리눅스 배포판**은 세밀한 권한 설정을 통해 다양한 방법으로 시스템을 제어할 수 있다. 패키지 시스템과 경로 체계도 리눅스 배포판은 많이 다른다. Synology NAS는 DSM 자체적으로 `/usr/syno/bin`, `/opt`,  `/var/packages` 등의 특수 구조를 사용하고 있다. 일반적인 `which`, `stat`, `vi` 등이 예상한 경로에 없기 때문에 처음 명령을 입력하면 오류가 나 당황하게 된다.

---

## 2. **Ubuntu**(**Ubuntu**) 설치

스크립트를 나스에서 사용하지 못한다면 **설치형 배포판 리눅스**를 직접 설치하는 수 밖에 없다. 그래서 Synology NAS에 **Ubuntu**를 설치하기로 했다. 하지만 DSM 자체를 일반 리눅스로 바꾸는 것은 불가능에 가깝고, Synology에서도 이를 공식적으로 허용하지 않는다고 한다. 그렇다면 **Docker**에 리눅스 컨테이너를 설치하는 것이 최선이라고 생각했다. **Docker**는 Synology가 지원하고 있기 때문이다. 

Synology DSM에 들어가 **Docker**를 설치한다. DSM이 버전업하면서 **Container Manager** 로 변경되었다. 설치가 다 되면 이제 경로를 결정해야 한다. `/volume1` 안에 여러 폴더를 마운트할 수 있지만, 폴더를 만들 때 마다 마운트 하는 것이 번거롭다면 `/volume1` 하나만 마운트하는 것이 편리하다. 
NAS에 터미널로 접속한 후 아래와 같이 진행한다.

```
docker run -it \
  --name file_organizer_**Ubuntu** \
  --network host \
  -v /volume1:/volume1 \
  **Ubuntu** /bin/bash
```

여기서 **--name**에 **file_organizer_Ubuntu**는 콘테이너의 이름이므로 다르게 지정해도 된다.

이렇게 하면 **Ubuntu**를 다운받아 설치를 하고 마운트까지 한다. 이제 터미널의 프롬프트가 바뀌면서  bash 쉘로 진입해 있을 것이다. 이제 필요한 패키지를 설치하기 위해서 다음 명령을 실행한다.

```
apt update && apt install -y bash coreutils findutils sed grep procps iputils-ping **cron** tzdata vim less curl net-tools
```

만약 여기서 관련파일을 다운받지 못하고 0%에서 진행이 안된다면 방화벽 때문일 가능성이 크다. Docker 컨테이너가 인터넷에 연결되지 못해 일어나는 상황이다. 당장  DSM에 들어가 방화벽을 잠시 꺼두자.
설치가 시작되면 한참 걸린다. 필요 프로그램을 다운받고 설치가 진행된다. 설치 도중에 국가와 지역 설정을 하게 된다. 이 설정으로 시간을 바꿀 수 있다.  설치가 다 되면 이제 독립적인 **Ubuntu** 시스템을 갖추게 된다.

---

## 3. Script와  cron

이제 그동안 만들어 둔 스크립트를 **cron**에 등록하고 실행한다. 처음은 모든 폴더를 하나의 스크립트로 만들어 운영하려고 했었다. 하지만 감시 폴더별로 구분해서 스크립트를 만드는 것이 효율적이라고 생각했고, 로그 역시 구분하는 것이 관리 차원에서 편리할 것이라고 판단했다. 그래서 두개의 스크립트를 등록한다.

```
crontab -e
```

**cron**을 등록하는 편집기에 들어가게 된다. 이곳에 실행 시간과 스크립트 경로를 입력하고 로그를 등록한다.

```
* * * * * bash /volume1/Tasks/file_organizer_Temp.sh >> /volume1/Tasks/Logs/**cron**_stdout.log 2>&1
* * * * * bash /volume1/Tasks/file_organizer_Downloads.sh >> /volume1/Tasks/Logs/**cron**_stdout.log 2>&1
```

실행 간격은 1분이다. bash 명령으로 경로에 있는 스크립트를 실행하고 로그를 생성한다.

```
*  *  *  *  *   <실행할 명령>
│  │  │  │  │
│  │  │  │  └─ 요일 (0-7) (0 또는 7 = 일요일)
│  │  │  └──── 월 (1-12)
│  │  └─────── 일 (1-31)
│  └────────── 시 (0-23)
└───────────── 분 (0-59)
```

저장하고 나와서 **cron**을 실행한다.
```
service cron start
또는
cron
```

그리고 확인.
```
ps aux | grep cron
```

이제 중요한 점은 스크립트를 실행하기 위해서는 항상 Docker의 컨테이너가 실행되어 있어야 한다는 것이다. 하지만 기본적으로 Docker 컨테이너는 내부에서 뭔가 계속 동작하지 않으면 자동으로 종료된다. 그래서 계속 켜두기 위해서 컨테이너를 백그라운드에서 항상 살아 있게 만들어야 한다. 

```
docker update --restart unless-stopped file_organizer_Ubuntu
```

이 명령을 하기 위해서는 먼저 **Ubuntu**에서 `exit` 로 나가서 NAS 터미널로 이동해야 한다. 도커 컨테이너 내부에서 도커 명령을 실행하지 못하기 때문이다. 이렇게 컨테이너가 자동으로 시작하는 명령도 있지만 Synology DSM의 **Container Manager** 에 들어가 컨테이너에서 **자동 재시작 활성화**에 체크해도 된다. 하지만 두개 다 할 필요는 없다.

그동안 Synology NAS에서 돌아가지 않았던 스크립트가 이제 제대로 운영된다. 한번에 잘 실행되고 특정한 폴더 내의 파일들이 지정된 폴더를 만들어 정리되는 모습을 보니 우울한 마음이 한결 편해졌다. 

---

## 4. Backup !important

이제  NAS를 사용하다가 무언가의 이유로 도커 패키지를 제거하면 그 안에 설치해 둔 **Ubuntu** 컨테이너, 내부 설정, 크론, 로그까지 전부 사라지게 된다. 왜냐하면 도커의 컨테이너는 휘발성이기 때문이다. 항상 조심해야 한다. 이미 스크립트와 로그는 컨테이너 안이 아니라 호스트에 있기 때문에 컨테이너가 없어진다 하더라도 삭제되지는 않을 것이다. 하지만 도커에 설치한 각 패키지와 설정들은 삭제될 것이다. 

이제부터 백업을 진행해 보자.
### 4.1 `docker run` 명령어를 `.sh`에 저장
이 명령어는 나중에 컨테이너를 다시 생성할 수 있는 핵심이다.

```
#!/bin/bash
docker run -it \
  --name file_organizer_Ubuntu \
  --restart=always \
  --network host \
  -v /volume1:/volume1 \
  -v /etc/localtime:/etc/localtime:ro \
  Ubuntu /bin/bash
```

위 내용을 `/volume1/Tasks/docker_run_Ubuntu.sh` 에 저장해 둔다.

### 4.2 **cron**tab, 스크립트 파일 외부 저장

#### 4.2.1 스크립트 (`.sh`) 위치 확인
```
/volume1/Tasks/file_organizer_Temp.sh  
/volume1/Tasks/file_organizer_Downloads.sh
```
이건 내가 사용하고 있는 스크립트인데 이미 호스트에 저장해 두었으니 아직은 안전하다 할 수 있다. 하지만 혹시 모르니 로컬에 저장하거나 크라우드 저장소에 넣어 두는 것도 좋다.

#### 4.2.2 **cron**tab 백업 (컨테이너 내부)

컨테이너에 들어가서, 즉 **Ubuntu** 내부에 들어가서 아래 명령을 실행한다. 그러면 `/volume1/Tasks/`에 `Ubuntu_crontab.bak` 파일이 생기게 된다. 
```
crontab -l > /volume1/Tasks/Ubuntu_crontab.bak
```

이것을 나중에 이렇게 복원할 수 있다.
```
crontab /volume1/Tasks/Ubuntu_crontab.bak
```


### 4.3 컨테이너 상태 전체 저장 (비추천)

```
docker commit file_organizer_Ubuntu file_Ubuntu_backup
docker save -o /volume1/Tasks/file_Ubuntu_backup.tar file_Ubuntu_backup
```

이렇게 하면 `.tar` 파일 하나로 완전히 복제할 수 있다. 대신 용량이 크고, 나중에 `docker load`로 복원해야 한다. 이건 특별할 상황에서 만 추천한다. 위의 스크립트 기반 복원이 더 간편하다.

---

이 정도의 설정으로 완벽하게 백업을 해 두었다. 이 기록을 따라 하다 보면 분명히 오류가 발생할 것이다. 그 이유는 많은 시행착오 중에 성공한 부분을 다뤘기 때문이다. 하지만 그 시행착오도 경험의 일부이기 때문에 소중하다. 다음에는 실행 중인 완성된 스크립트를 다뤄 보기로 하겠다.

