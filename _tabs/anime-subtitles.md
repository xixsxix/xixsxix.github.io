---
layout: page
title: Anime Subs
icon: fas fa-closed-captioning
order: 4
permalink: /anime-subtitles/
---

# 애니 자막 상태

애니 자막 상태판은 Synology NAS에서 관리합니다.

NAS에서는 Anissia API를 기반으로 자막 등록 상태를 갱신하고, 필요한 경우 직접 갱신 버튼으로 최신 상태를 확인할 수 있습니다.

[자막 상태판 열기](https://xixsxix.i234.me/anime-subtitles/){:target="_blank" rel="noopener noreferrer" .btn .btn-primary}

## 운영 방식

* 상태판 위치: `https://xixsxix.i234.me/anime-subtitles/`
* 데이터 갱신: Synology NAS의 Python 스크립트
* 수동 갱신: NAS 상태판의 `지금 갱신` 버튼
* 자동 갱신: DSM 작업 스케줄러
* GitHub Pages는 안내 페이지 역할만 담당
