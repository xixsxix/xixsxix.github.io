---
title: "NAS 모니터링시스템 #2 Entware"
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
pin: false
comments: "true"
image: /assets/img/linux-title02.webp
---

이번 포스트에서는 지난 번 작성했던 **NAS 자동 스크립트**를 실행하기 위한 **모니터링 시스템**을 만든 방법에 대해 정리해 본다. 지난 포스트에서는 다운로드 된 파일을 자동으로 지정된 폴더에 이동시키고 불필요한 파일은 삭제하는 스크립트 작성기 였다. 

<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-1/" target="_blank"># NAS 모니터링시스템 #1 Script</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-2/" target="_blank"># NAS 모니터링시스템 #2 Entware</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-3/" target="_blank"># NAS 모니터링시스템 #3 inotify-tools</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-4/" target="_blank"># NAS 모니터링시스템 #4 inotifywait</a>

**ChatGPT**는 대화할 때 처음부터 제안하지 않는다. 묻는 말에 방법을 제시하지만 더 좋은 방법이 있다고 먼저 말하지 않는다. 그래서 대화 중에 더 좋은 방법이 있는지 물어야 한다. 그래야 알려준다. 나는 **ChatGPT와 많은 시행착오를 겪었다.** 

이 문서는 그 시행착오 로그를 보고 정리 한 문서이다. 

---
## NAS 자동화 2편: Entware 설치

---

### 모니터링 기반 자동 실행 시스템에는 어떤 방식이 있을까?

![image](/assets/linux/161139.png)

여기서 나는 **inotify** 를 선택했다. 특정 폴더에 변화가 생기면 즉시 반응하는 시스템. 내가 원하던 방식이다. 하지만 별도 패키지가 필요하다. 기본적으로 시놀로지에서는 설치가 안 되어 있어서 설치를 해야 한다.

```
opkg install inotify-tools
```

**powershell**로 접속해서 위 명령어를 입력하면 된다. 하지만 **opkg**가 설치되어 있지 않을 것이다. 시놀로지에는 기본적으로 **opkg**가 없기 때문에 **Entware**를 설치해야 한다. 

---
### Entware란?

Entware는 시놀로지에서 사용할 수 있는 **경량 리눅스 패키지 관리자(opkg)** 이다. 설치하면 inotify-tools, htop, mc, rsync, screen 등 여러 CLI 도구를 사용할 수 있게 된다. 
 
#### 1. ssh 로그인
```
ssh 사용자명@NAS_IP주소 -p 포트번호
```

#### 2. 관리자 권한으로 전환
```
sudo -i
```
#### 3. NAS 모델명을 확인해 보자.
```
uname -m
```

시놀로지는 대부분 인텔 기반이기 때문에 **x86_64** 일 것이다.

#### 4. Entware 설치 스크립트 다운로드
```
cd /tmp
wget https://bin.entware.net/aarch64-k3.10/installer/generic.sh -O entware_install.sh
chmod +x entware_install.sh
./entware_install.sh
```
설치 URL은 NAS CPU 아키텍처에 따라 다를 수 있다. 위 코드는 Synology DS218+ (aarch64)기준이며, 모델에 따라 달라지니 꼭 확인해야 한다.

혹시 퍼미션 때문에 ./entware_install.sh 에서 오류가 난다면 강제 설치도 가능하다.
```
bash entware_install.sh
```

**CPU 아키텍처 & 커널 버전용 패키지 경로**

| 경로            | 설명                                              |
| ------------- | ----------------------------------------------- |
| x64-k3.2      | Synology DS218+ 같은 **Intel x64 커널 3.2 기반 NAS**용 |
| aarch64-k3.10 | ARM 64bit 기반 NAS (예: DS220j)                    |
| armv7sf-k3.2  | 32비트 ARM NAS                                    |


#### 5. 설치 완료 후 초기화
```
echo 'export PATH=/opt/bin:/opt/sbin:$PATH' >> ~/.profile
. ~/.profile
```

설치가 완료되면 /opt/bin에 opkg 명령어가 생성된다.  환경변수를 등록하지 않으면 command not found가 발생할 수 있으므로 ~/.profile에 추가해준다.

또는 NAS를 재부팅 하면 자동 적용된다고 하는데 나는 오랜만에 부팅도 해 주었다.

#### 6. 설치 확인
```
opkg --version
```

정상 출력 예시:
```
opkg version 38eccbb1fd694d4798ac1baf88f9ba83d1eac616 (2024-10-16)
```

#### 7. opkg 초기 업데이트
```
opkg update
```

이제부터 **opkg install inotify-tools** 같은 명령으로 패키지를 설치할 수 있게 되었다.

#### 8. 주의사항
Entware는 Synology NAS DSM 패키지 센터와 별개로 동작하기 때문에 시스템 파일을 변경하거나 /opt를 삭제하면 기능이 깨질 수 있다. Synology DSM 업데이트 시 Entware 디렉토리(/opt)가 초기화될 수 있으므로 확인해야 한다.

---

다음은 inotify-tools 설치에 대해서 정리해 보자.

<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-1/" target="_blank"># NAS 모니터링시스템 #1 Script</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-2/" target="_blank"># NAS 모니터링시스템 #2 Entware</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-3/" target="_blank"># NAS 모니터링시스템 #3 inotify-tools</a>
<a href="https://xixsxix.github.io/posts/NAS-Auto-Watch-System-4/" target="_blank"># NAS 모니터링시스템 #4 inotifywait</a>