---
title: Portainer, Docker 설치
date: '"2025-06-21 01:55:02 +0900"'
categories:
  - Synology Nas
tags:
  - synology
  - nas
  - 시놀로지
  - 나스
  - portainer
  - docker
  - docker-compose
pin: false
comments: "true"
image: /assets/img/portainer-t.png
---

## 1. Portainer 

[Portainer](https://www.portainer.io/)는 Docker 환경을 시각적으로 관리할 수 있게 해주는 웹 기반 GUI (Graphical User Interface) Tool이다.  
복잡한 CLI (Command Line Interface) 없이 컨테이너, 이미지, 네트워크, 볼륨 등을 클릭 몇 번으로 조작할 수 있도록 도와준다.  Synology Nas의 DSM에서도 GUI 환경에서 Docker 설치를 제공하는 Container manager가 있지만, 컨테이너의 시작, 정지, 재시작, 로그 확인 등 간단한 기능 만 제공할 뿐이다.  설치한 docker를 시각적으로 보고 관리하기를 원한다면 [Portainer](https://www.portainer.io/)를 설치를 권장한다.

[Portainer](https://www.portainer.io/)는 우습지만 자기 자신도 Docker다.  그래서 CLI 환경이나 Nas의 Container manager를 이용해서 설치해야 한다.  설치는 유료와 무료 버전이 있지만 개인 사용자는 무료 기능 만으로 충분하다.  [Portainer](https://www.portainer.io/)를 설치해 보면 더 많은 Docker를 설치하려고 검색하고 있을지도 모른다.

---

## 2. Portainer 설치

ssh에 root로 접속하자.
```
ssh 사용자명@NAS_IP주소 -p 포트번호
sudo -i
```

폴더를 만들고 소유권과 권한을 설정한다.
```
mkdir -p /volume1/docker/portainer
chown 1026:100 /volume1/docker/portainer
chmod 775 /volume1/docker/portainer
```

만든 폴더로 이동해서 docker-compose.yml를 만든다.
```
cd /volume1/docker/portainer
nano docker-compose.yml

# nano가 없으면
vi docker-compose.yml
```

아래의 문장을 입력하고 저장한다. 
```
version: '3.3'

services:
  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    restart: always
    ports:
      - "9000:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /volume1/docker/portainer:/data
```

저장하고 나와서 `docker-compose`로 실행한다.
```
docker compose up -d
```

설치가 완료되면 브라우저로 나스 ip에 port 9000으로 접속한다.
```
NAS_IP주소:9000
```

접속하면 관리자 아이디와 비밀번호를 생성해 접속하면 된다.

---

사용법은 다음 기회에~