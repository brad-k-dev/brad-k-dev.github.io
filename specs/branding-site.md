# 브랜딩 허브 페이지 (GitHub Pages)

## 목표
`https://brad-k-dev.github.io/`를 출시한 모든 앱을 소개하는 브랜드 허브로 만들고,
검색엔진·AI가 읽을 수 있는 기반을 갖춘다. 경로: 웹 검색 → 허브/앱 페이지 → App Store.

## 결정
- 호스팅은 GitHub Pages 유지. Vercel Hobby는 약관 4조가 "personal or non-commercial use"로
  한정(2026-10-19 개정본, 2026-11-23 확인)이라 광고 수익 앱 홍보에 쓰지 않는다.
- 브랜드 이름은 Offtask Lab(오프태스크 랩). "딴짓"은 타인 등록 상표(09류 등, KIPRIS 2026-11-23 확인)라 이름에 쓰지 않고 슬로건 문구로만 쓴다.
- 홈은 한국어(`/`)와 영어(`/en/`) 두 페이지. 문의 메일은 offtasklab@gmail.com.
- 정적 HTML 유지. 앱 목록 하나(`build.py`, 표준 라이브러리만)에서 홈 두 개·사이트맵·llms.txt를 만들고 결과물을 커밋한다.
- 앱별 상세는 새로 만들지 않고 기존 앱별 페이지(`/mochi-bakery/` 등)를 그대로 쓴다. 중복 페이지를 만들지 않기 위해서다.

## 범위
1. 홈(`index.html`): 출시된 앱 전부를 카드로 소개(아이콘, 한 줄 설명, App Store 버튼, 소개 페이지 링크).
   지금은 쏙! 냥이 1개만 있음.
2. 홈 메타: description, OG, canonical, JSON-LD(`Organization` + 앱 목록).
3. 루트 파일: `robots.txt`, `sitemap.xml`(홈 + 앱별 페이지 URL), `llms.txt`.
4. 앱별 페이지(각 저장소, 저장소마다 PR): 빠진 description·OG, canonical,
   `MobileApplication` JSON-LD, 스마트 앱 배너(`apple-itunes-app`), 허브로 돌아가는 링크.
5. `app-ads.txt`는 건드리지 않는다.

## 범위 밖 (다음 단계)
- 의도 랜딩·블로그(구름줍줍 구름 도감 등)
- Google Search Console·네이버 서치어드바이저 등록(본인 계정 필요)
- App Store 내부 검색 최적화(ASO), 자기 도메인, 디자인 전면 개편

## 수용 기준 (JS 없이 curl로 확인)
- 홈 HTML에 출시된 앱 전부의 이름과 App Store 링크가 있다.
- `/robots.txt`, `/sitemap.xml`, `/llms.txt`가 200이고 사이트맵의 모든 URL이 200이다.
- 홈과 모든 앱 페이지에 title, description, canonical, og:title, og:image, JSON-LD가 각 1개 이상 있다.
- JSON-LD가 JSON으로 파싱되고, 내용이 화면에 보이는 문구와 일치한다.
- 모든 앱 페이지에 해당 앱 ID의 스마트 앱 배너가 있다.
- `/app-ads.txt`가 바이트 단위로 변하지 않았다.
- 위 항목을 한 번에 확인하는 `check.sh` 하나를 남긴다.

## 진행 순서
1. 이 저장소(홈, 루트 파일, check.sh) — PR 1개
2. 앱별 저장소 6개(범위 4번) — 저장소마다 PR, `APPS=1 ./check.sh`로 확인
