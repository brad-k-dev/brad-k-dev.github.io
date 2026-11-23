#!/bin/bash
# 크롤러 눈(JS 없는 HTML)으로 수용 기준을 확인한다.
#   ./check.sh                      배포된 사이트 확인
#   ./check.sh http://localhost:8000  로컬 확인 (python3 -m http.server 8000)
#   APPS=1 ./check.sh               앱별 페이지(다른 저장소)의 메타까지 확인
BASE=${1:-https://brad-k-dev.github.io}
PROD=https://brad-k-dev.github.io
IDS="6822971808 6826563332 6826859875 6826611529 6823086561 6819158926"
APP_PAGES="mochi-bakery:6822971808 Squish-cats:6826563332 gureum-jupjup:6826859875 luma-garden:6826611529 slipring:6823086561 sneaky-salaryman:6819158926"
fail=0
ok() { echo "  ok   $1"; }
bad() { echo "  FAIL $1"; fail=1; }
has() { grep -qiE "$2" <<<"$1" && ok "$3" || bad "$3"; }
meta() { # $1 html, $2 label
  has "$1" '<title>[^<]+' "$2 title"
  has "$1" 'name="description" content="[^"]+' "$2 description"
  has "$1" 'rel="canonical"' "$2 canonical"
  has "$1" 'property="og:title"' "$2 og:title"
  has "$1" 'property="og:image"' "$2 og:image"
  has "$1" 'application/ld\+json' "$2 JSON-LD"
  if grep -qiE '<meta[^>]*robots[^>]*noindex' <<<"$1"; then bad "$2 noindex 없음"; else ok "$2 noindex 없음"; fi
}

for p in / /en/; do
  echo "== $BASE$p"
  h=$(curl -sL -m 20 "$BASE$p")
  meta "$h" "$p"
  [ "$(grep -oi '<h1' <<<"$h" | wc -l | tr -d ' ')" = 1 ] && ok "$p h1 1개" || bad "$p h1 1개"
  for id in $IDS; do has "$h" "apps\.apple\.com/[a-z/]*app/id$id" "$p App Store 링크 $id"; done
  python3 -c '
import json, re, sys
h = sys.stdin.read()
blocks = re.findall(r"<script type=\"application/ld\+json\">(.*?)</script>", h, re.S)
assert blocks, "JSON-LD 없음"
for b in blocks:
    for item in json.loads(b)["@graph"][1]["itemListElement"]:
        name = item["item"]["name"]
        assert name.replace("&", "&amp;") in h.split("</head>")[1], f"화면에 없는 이름: {name}"
' <<<"$h" && ok "$p JSON-LD 파싱·화면 문구 일치" || bad "$p JSON-LD 파싱·화면 문구 일치"
done

echo "== 루트 파일"
for f in robots.txt sitemap.xml llms.txt images/og.png; do
  [ "$(curl -s -o /dev/null -m 20 -w '%{http_code}' "$BASE/$f")" = 200 ] && ok "/$f 200" || bad "/$f 200"
done
[ "$(curl -s -o /dev/null -m 20 -w '%{http_code}' "$BASE/no-such-page-check")" = 404 ] && ok "없는 주소 404" || bad "없는 주소 404"
for u in $(curl -sL -m 20 "$BASE/sitemap.xml" | grep -o '<loc>[^<]*' | cut -c6-); do
  path=${u#$PROD}
  case "$path" in /|/en/) t="$BASE$path" ;; *) t="$u" ;; esac   # 앱별 페이지는 다른 저장소가 게시한다
  [ "$(curl -sL -o /dev/null -m 20 -w '%{http_code}' "$t")" = 200 ] && ok "sitemap $path 200" || bad "sitemap $path 200"
done
git -C "$(dirname "$0")" diff --quiet 219c655 -- app-ads.txt && ok "app-ads.txt 변경 없음" || bad "app-ads.txt 변경 없음"

if [ -n "$APPS" ]; then
  for e in $APP_PAGES; do
    p=${e%%:*}; id=${e##*:}
    echo "== $PROD/$p/"
    h=$(curl -sL -m 20 "$PROD/$p/")
    meta "$h" "/$p/"
    has "$h" "apple-itunes-app\" content=\"app-id=$id" "/$p/ 스마트 앱 배너"
  done
fi

[ $fail = 0 ] && echo "PASS" || echo "FAIL"
exit $fail
