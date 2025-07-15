---
# the default layout is 'page'
icon: fas fa-info-circle
order: 4
---

## 1. 자막, 영상, 오디오 편집
영상에서 필요한 자막을 정확하게 추출하고 클립을 만들기 위해 **100분의 1초 단위**까지 조정이 필요하다.  
이 과정에서 다음 프로그램을 사용한다.  

- **[Subtitle Edit](https://www.nikse.dk/subtitleedit/)** (Windows) / **[Aegisub](https://aegisub.org/)** (Mac)  
- **[ffmpeg](https://ffmpeg.org/)** : 블로그에 올릴 영상 및 자막 추출  
- **ChatGPT + 배치파일** : 자동화된 시간 입력 코드 작성

## 2. 자막 번역 및 자료 조사
AI 번역 도구 중에서는 **ChatGPT**가 질문을 저장하고 대화의 연속성이 뛰어나 메인으로 사용 중이다.  

- **[ChatGPT](https://chatgpt.com/)** : 번역 및 해석, 문맥 분석  
- **[Copilot](https://copilot.microsoft.com/)** : 유연한 문장 해석  
- **[Perplexity](https://www.perplexity.ai/)** : 초기 사용, 현재는 우선순위 낮음  

## 3. 사전 및 언어 학습
AI 번역 결과가 부족할 때는 직접 사전을 활용한다.  

- **[네이버 사전](https://dict.naver.com/)** : API를 활용한 검색  
- **[Language Reactor](https://www.languagereactor.com/)** (Chrome 확장) : 넷플릭스 원본 자막 확인  

## 4. 문서 작성 및 편집
모든 문서 작성과 정리는 **Obsidian**에서 시작한다.  

- **[Obsidian](https://obsidian.md/)** : 노트 및 문서 관리  
- **[Furigana Plugin](https://github.com/uonr/obsidian-furigana)** : 일본어 루비 문자 입력  
- **[Beeftext](https://beeftext.org/)** : 반복되는 단어 및 문장 단축 입력  

## 5. GitHub 블로그
Obsidian에서 작성한 문서를 바로 블로그로 커밋하기 위해 **GitHub Pages + Jekyll**을 활용한다.  

- **[GitHub](https://github.com/)** : 블로그 호스팅  
- **[Jekyll](https://jekyllrb.com/)** + **[Chirpy Theme](https://github.com/cotes2020/jekyll-theme-chirpy)** : 블로그 엔진  
- **[VS Code](https://code.visualstudio.com/)** : HTML/CSS 수정 및 커밋 관리  
