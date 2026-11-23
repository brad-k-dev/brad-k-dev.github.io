# brad-k-dev.github.io

Offtask Lab(오프태스크 랩) 브랜드 홈과 AdMob 인증 파일(`app-ads.txt`). 같은 AdMob 계정을 쓰는 모든 앱이 이 파일을 함께 씁니다.

- 새 앱 출시: `build.py`의 `APPS`에 한 항목 추가, `images/<slug>.jpg` 저장, `python3 build.py`, 결과물 커밋.
- 확인: `./check.sh`(배포본) 또는 `python3 -m http.server 8791 --bind 127.0.0.1` 후 `./check.sh http://127.0.0.1:8791`.
- `index.html`, `en/index.html`, `sitemap.xml`, `llms.txt`, `robots.txt`는 `build.py`가 만든 파일이라 직접 고치지 않습니다.
