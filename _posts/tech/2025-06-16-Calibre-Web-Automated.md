---
title: Calibre-Web Automated 도커 설치
date: '"2025-06-16 15:47:54 +0900"'
categories:
  - Synology Nas
tags:
  - synology
  - nas
  - 시놀로지
  - 나스
  - calibre
  - calibre-web
  - calibre-web-automated
  - docker
  - container_manager
  - ebook
  - 전자책
pin: false
comments: "true"
image: /assets/img/CWA-Homepage.png
---

## 1. Calibre  
  
![Calibre](/assets/img/222136.png)  
[https://calibre-ebook.com/](https://calibre-ebook.com/)
  
**Calibre는 python을 기반으로 개발한 오픈소스 전자책(ebook) 관리 소프트웨어다.**      
대용량 전자책 라이브러리를 체계적으로 관리하는 데는 매우 강력하다.  처음 설치했을 때는 직관적이지 않은 UI와 투박한 인터페이스에 실망해 외면했었다.  그러나 기능을 하나씩 접해가며 사용해 보니, 전자책 정리와 메타데이터 관리에 있어서 만큼은 Calibre를 능가할 도구가 없다는 확신이 들었다.    
    
**Calibre의 메타데이터 관리 기능은 사실상 독보적이다.**      
단순히 책 제목만 입력해도 Amazon, Google Books 등의 데이터베이스에서 저자, 출판사, 발행일, 표지 이미지를 자동으로 불러온다. 여기에 네이버북, YES24 등 사용자 제작 플러그인을 설치하면 국내 도서의 메타데이터도 가져올 수 있다.  해외 서적뿐 아니라 한국어 전자책 정리에도 매우 강력한 도구다.    
    
**Calibre는 전자책 관리 소프트웨어이지 전자책 리더기는 아니다.**     
물론 뷰어의 기능이 있지만 UI나 사용성은 상당히 뒤처진다. 무엇보다 iPad로 전자책을 읽는 나에게 뷰어로서의 기능은 필요하지 않았다.  PC에 저장된 라이브러리를 iPad에 간편하게 옮기는 과정이 중요했다.  저자나 장르별로 구분하거나, 표지 이미지를 보고 쉽게 읽을 책을 고르고 싶었다. 그렇게 찾아낸 것이 **Calibre-Web**이다.  
  
---  
  
## 2. Calibre-Web  
  
![Calibre-Web](/assets/img/main_screen.png)  
[https://github.com/janeczku/calibre-web](https://github.com/janeczku/calibre-web)  
  
**Calibre-Web은 Calibre에서 개발한 것이 아니다.**  
Calibre-Web은 Flask 프레임워크 기반의 독립 프로젝트로 Calibre의 메타데이터와 라이브러리를 기반으로 작동하는 별도의 웹 인터페이스로 개발되었다.  전자책을 탐색, 읽기, 다운로드하기 위해 직관적이고 깔끔한 UI를 제공한다.   
사용자는 스마트폰이나 태블릿 등 다양한 기기에서 브라우저를 통해 접근하면 된다. 또한 자체 뷰어도 깔끔한 편이어서 웹에서 전자책을 열람하거나 다운로드하여 자신의 기기에서 열람하면 된다.  
    
Calibre 자체에도 콘텐츠 서버(content server)가 내장되어 있어 브라우저를 통해 전자책에 접근할 수는 있다.  하지만 PC를 계속 켜 두어야 한다는 치명적인 단점이 존재한다.     
    
Calibre-Web은 다양한 특징과 장점을 가지고 있다. 그중에 주요 장점은 **로그인과 사용자 권한 관리** 기능이다.  권한을 부여받은 가족이나 지인 또는 전자책을 공유하고 싶은 사용자들이 각자의 라이브러리를 공유할 수 있는 **업로드 기능**이 있다.  또한 자신의 서재를 만들고 공유할 수 있는 기능 또한 독특하다.  Calibre-Web은 단순한 뷰어를 넘어서, **진정한 개인 전자 도서관의 형태**로 활용할 수 있다.  일종의 독서 커뮤니티를 형성할 수 있는 매우 유용한 솔루션이 된다.    
    
Calibre-Web은 거의 완벽한 Calibre과 비교했을 때 핵심 기능 몇 가지가 부족하다. 그래서 사용자들은 Calibre와 Calibre-Web 두 서비스를 병렬로 실행하여 부족한 부분을 채워가야 하는 불완전한 솔루션이었다.  Calibre에서 도서를 등록 또는 변환하고 메타데이터를 수정한 후, Calibre-Web에서 활용하는 방식이었다.    
  
최근에 Calibre-Web의 현대적이고 가벼운 웹 UI와 Calibre의 견고하고 다양한 기능을 결합하고, 또 그 위에 다양한 추가 기능과 자동화를 더한 올인원 솔루션을 목표로 하는 프로젝트가 새롭게 공개되었다.  이 포스트에서는 이 올인원 솔루션 설치에 대해 설명해 보려 한다.  
  
---  
  
## 3. Calibre-Web Automated  
  
![Calibre-Web Automated](/assets/img/CWA-Homepage.png)  
[https://github.com/crocodilestick/Calibre-Web-Automated](https://github.com/crocodilestick/Calibre-Web-Automated)
  
공개된 지 채 1년이 되지 않았고 메이저 업데이트는 4개월 정도 된 Calibre-Web Automated(CWA)는 인기 오픈소스 도서 관리 시스템인 Calibre-Web의 기능을 확장하고 자동화 기능을 추가한 포크 프로젝트이다.  기존 Calibre-web은 사용자의 수동 개입이 필요한 부분이 많았으나 CWA는 다양한 자동화 기능을 통해 관리자의 개입을 최소화하고 도서 등록부터 정리까지의 과정을 자동 처리할 수 있도록 설계되었다.  
  
개발자 사이트에는 각 특징에 대한 자세한 설명이 되어 있다. 그중에 가장 큰 특징은 **CWA Admin Functions** 이다.  자동으로 도서를 등록해 주고 새 도서가 등록되면 정해진 형식으로 자동 변환해 준다. 비어있는 메타데이터나 커버이미지가 있다면 데이터베이스를 검색해서 추가해 준다. 새 도서를 주기적으로 인식하여 metadata.db를 갱신하고 백업도 해준다.   
  
그 외에도 많은 기능이 포함되어 있지만 이 문서에서 설명하기엔 너무 벅차다.  자세한 내용은 개발자 사이트에서 확인하기를 바란다. 다만. 개발자는 아직 활발히 개발 중이며 작업 중이고 코드 기반이 성숙해지는 동안 예상치 못한 버그가 발생할 수 있다고 조심스레 경고하고 있다.   
  
**Calibre-Web Automated(CWA)를 설치는 생각보다 간단하다.**  
다만 Nas를 운용 중이어야 하고 Calibre가 자신의 PC에 설치되어 있어야 한다. 로컬에 라이브러리 폴더가 저장되어 있다면 Nas로 옮기자.    
  
---  
  
## 4. Docker 패키지 설치  
  
Calibre-Web Automated는 python으로 개발되었으며, 직접 설치하거나 Docker를 통해 구동할 수 있다.  가장 간편한 방식은 Docker 이미지를 사용하는 것이다. 특히 Synology NAS와 같은 장비에서는 Docker 패키지를 통해 손쉽게 Calibre-Web Automated를 설치할 수 있다.  
  
Synology는 예전에 Docker라는 이름으로 패키지를 제공했지만, 최근 DSM 업데이트 이후 Container Manager로 변경되었다. 따라서 DSM 패키지 센터에서 Container Manager를 검색하여 설치하면 된다.  
  
설치가 완료되면, Docker 관련 파일을 저장할 전용 폴더를 지정해 두는 것이 좋다.  이 전용 폴더는 이미지, 컨테이너 설정, 로그 등 다양한 데이터가 생성되는 공간이다.  분산 저장 시 관리가 어려워질 수 있으므로 Docker의 전용 폴더는 필수라고 볼 수 있다.  나는 `/volume1/docker` 폴더를 만들어 사용하고 있다. 설치되는 모든 Docker 기반 애플리케이션은 이 경로에서 관리하고 있다.  
  
```  
/volume1  
   ├ docker/  
   │  └─ calibreweb-automated/  
   │        └─ config/  
   ├ Ebook/     ← Calibre 라이브러리(metadata.db 포함)  
   └ ingest/ ← 다운로드한 Ebook이 저장되고 자동 등록되는 공간  
```  
  
DSM의 제어판, 공유 폴더에서 `docker` 공유 폴더를 만든다. 볼륨의 어미 폴더는 ssh로 만들 수 없으므로 미리 만들어 둔다.  또한, 라이브러리를 저장할 `books`폴더도 만든다. 그리고 윈도우의 Calibre에서 라이브러리 폴더로 지정해 두면 아래 설치를 따라 하기 편해진다. 그리고 새 도서가 저장되고 자동 등록되는 공간인 `ingest` 폴더도 함께 만들어 두자.  
  
---  
  
## 5. Calibre-Web Automated, Docker Compose 설치  
  
 **Container Manager**에서 이미지를 다운로드하고 GUI 환경에서 설치하는 방법이 있다. 하지만 이 포스트에서는 Docker Compose를 사용하여 이미지를 다운부터 설정과 설치까지 한 번에 할 것이다. 이렇게 진행하기 위해서는 아래처럼 폴더를 생성한다.  다르게 하고 싶을 때는 반드시 모든 경로를 동일하게 설정해 주어야 한다.
   
- `/volume1/Ebook` : Calibre 라이브러리가 저장된 폴더  
- `/volume1/ingest` : 자동 작업 공간  
- `/volume1/docker/calibreweb-automated` : 이미지가 설치될 폴더  
- `/volume1/docker/calibreweb-automated/config` : 설정 저장 공간  
  
<center><i>다른 폴더명을 사용하려면 반드시 아래에도 동일하게 적용해야 한다.</i></center>  
  
필요한 폴더를 다 만들었으면 cmd나 powershell을 이용해서 ssh에 접속한다.  
  
```  
ssh 사용자명@NAS_IP주소 -p 포트번호  
```  
  
비밀번호를 입력하고 관리자로 접속한다.  
```  
sudo -i  
```  
  
Linux에서 에러는 권한 문제가 대부분이다. 혹시 모르니 먼저 권한을 지정하자.  
```  
mkdir -p /volume1/docker/calibreweb-automated/config  
chown -R 1026:100 /volume1/docker/calibreweb-automated  
chmod -R 775 /volume1/docker/calibreweb-automated  
```  
  
`docker-compose.yml` 의 이름으로 아래 코드를 작성하고 이미지가 설치될 폴더인 `/volume1/docker/calibreweb-automated`에 저장한다.  
  
```  
services:  
  calibre-web-automated:  
    image: crocodilestick/calibre-web-automated:latest  
    container_name: calibre-web-automated  
    environment:  
      - PUID=1026  
      - PGID=100  
      - TZ=Asia/Seoul  
    volumes:  
      - /volume1/docker/calibreweb-automated/config:/config  
      - /volume1/Ebook:/calibre-library  
      - /volume1/ingest:/cwa-book-ingest  
    ports:  
      - 8083:8083  
    restart: unless-stopped
```  
  
이제 `/volume1/docker/calibreweb-automated`로 이동하고 설치를 시작한다.  
```  
cd /volume1/docker/calibreweb-automated  
docker compose up -d  
```  
  
설치가 완료되고 몇 분 후에 브라우저로 접속해 보자.   
```  
http://192.168.0.100(nas ip):8083  
```  
  
초기 관리자 로그인
```
사용자이름 : admin
비밀번호 : admin123
```

설치가 완료되면 역방향 프록시를 설정하고 주소를 할당하면 외부에서도 도서를 다운로드하거나 직접 열람할 수 있는 개인 도서관이 완성된다.  

---  
  
내 NAS에 여러 번 설치 및 삭제를 반복하며 Calibre-Web Automated의 구조와 동작을 충분히 검증했다. 이 글을 참고한 다른 환경에서도 에러 없이 작동하기를 바란다. 

Calibre-Web Automated의 진짜 가치는 단순한 뷰어나 서버가 아니다.  사람과 책을 연결하는 ‘공유의 구조’에 있다.  설정에서 사용자에게 업로드를 허용하면 가족과 지인들이 직접 자신의 전자책을 올리고 함께 열람할 수 있는 작은 도서관이 완성되기 때문이다.  
  
전자책은 이제 더 이상 나만의 소유가 아니다. Calibre-Web Automated를 통해 각자의 책을 공유하고, 함께 읽고, 채워나가는 공동의 책장을 만들 수 있다.  단 하나의 주소로 당신의 책장이 세상과 연결되는 것이다.   
  
**이제 당신의 도서관을 열어보자.**  
  
---  
  
## 6. Docker Container 중지 및 삭제  
  
사용 중에 도커의 이미지를 삭제하고 싶다면 루트 권한으로 아래와 같이 입력하면 된다.   
```  
docker stop calibre-web-automated 
docker rm calibre-web-automated
```  
  
다운로드하였던 이미지까지 지우고 싶다면 아래처럼 입력하자.  
```  
docker rmi crocodilestick/calibre-web-automated:latest
```

---

현재 Calibre-Web Automated 는 로딩에 **치명적인 이슈**가 있어서 Calibre-Web를 사용하고 있다.