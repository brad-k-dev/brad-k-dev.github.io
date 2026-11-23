#!/usr/bin/env python3
"""앱 목록 하나로 index.html, en/index.html, sitemap.xml, llms.txt를 만든다.

새 앱 출시: APPS에 한 항목 추가, images/<slug>.jpg 저장, `python3 build.py`, 결과물 커밋.
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
BASE = "https://brad-k-dev.github.io"
BRAND = "Offtask Lab"
BRAND_KO = "오프태스크 랩"
EMAIL = "offtasklab@gmail.com"

# page: 앱별 소개 페이지 경로(각 앱 저장소가 게시). page_en이 없으면 영어 홈도 page로 링크한다.
# kr_only: 한국 App Store에만 있는 앱.
APPS = [
    dict(slug="mochi-bakery", id=6822971808, page="/mochi-bakery/", kind="game",
         ko=("모찌 베이커리: 말랑 블록 퍼즐", "모찌를 쟁반에 올려 한 줄을 채우면 뿅! 손가락 하나로 즐기는 힐링 블록 퍼즐."),
         en=("Mochi Bakery: Block Puzzle", "Drop squishy mochi onto the tray and fill a row or column to pop them. A relaxing block puzzle.")),
    dict(slug="squish-cats", id=6826563332, page="/Squish-cats/", kind="game",
         ko=("쏙! 냥이 - 귀여운 냥이 퍼즐", "톡 치면 쏙! 냥이들을 같은 색 바구니로 보내는 귀여운 퍼즐 게임."),
         en=("Squish Cats: Cute Cat Jam", "Tap a cat and it runs straight into the basket of its color. A cozy one-tap puzzle.")),
    dict(slug="gureum-jupjup", id=6826859875, page="/gureum-jupjup/", kind="app", kr_only=True,
         ko=("구름줍줍", "하늘에서 발견한 구름을 찍고, 이름 붙이고, 나만의 하늘에 모으는 앱."),
         en=("Gureum Jupjup (구름줍줍)", "Snap the clouds you find in the sky, name them, and collect them in a sky of your own.")),
    dict(slug="luma-garden", id=6826611529, page="/luma-garden/", page_en="/luma-garden/index-en.html", kind="game",
         ko=("루마 가든: 빛 퍼즐", "타일을 돌려 빛의 길을 잇고 꽃을 피우는 편안한 퍼즐 게임."),
         en=("Luma Garden", "Rotate tiles to connect paths of light and make the garden bloom. A relaxing puzzle.")),
    dict(slug="slipring", id=6823086561, page="/slipring/", kind="game",
         ko=("슬립링", "탭하면 방향이 뒤집힌다. 조여오는 호의 틈을 통과하는 원탭 아케이드."),
         en=("Slipring", "A dot runs a ring. Tap to send it the other way and be in the gap. A one-tap arcade game.")),
    dict(slug="sneaky-salaryman", id=6819158926, page="/sneaky-salaryman/", kind="game",
         ko=("칼퇴 대작전", "엄마, 부장님, CCTV, 사장님의 시선을 피해 99단계를 돌파하는 픽셀 잠입 게임."),
         en=("Sneaky Salaryman: Clock Out", "A pixel stealth game about clocking out on time without getting caught.")),
]

T = {
    "ko": dict(path="/", title=f"{BRAND} · {BRAND_KO} | 딴짓도 진지하게 만드는 앱과 게임",
               desc=f"{BRAND}({BRAND_KO})은 잠깐의 딴짓을 위한 작은 iOS 앱과 게임을 만드는 인디 스튜디오입니다. 모찌 베이커리, 쏙! 냥이, 구름줍줍 등 무료 앱을 소개합니다.",
               tagline="딴짓도 진지하게 만듭니다",
               intro=f"{BRAND}({BRAND_KO})은 잠깐의 딴짓을 위한 작은 iOS 앱과 게임을 만드는 인디 스튜디오입니다.",
               apps="만든 앱과 게임", free="무료", game="게임", app="앱", store="App Store에서 받기", more="소개",
               kr_only="", contact="문의", other="English", other_path="/en/"),
    "en": dict(path="/en/", title=f"{BRAND} | Small iOS apps and games, seriously off task",
               desc=f"{BRAND} is an indie studio from Korea making small iOS apps and games for your in-between moments: Mochi Bakery, Squish Cats, Slipring and more. All free.",
               tagline="Seriously off task.",
               intro=f"{BRAND} is an indie studio from Korea making small iOS apps and games for your in-between moments.",
               apps="Apps and games", free="Free", game="Game", app="App", store="Get it on the App Store", more="About",
               kr_only="Korean App Store only.", contact="Contact", other="한국어", other_path="/"),
}

CSS = """
:root { --bg: #fff8f1; --card: #ffffff; --ink: #4a383d; --soft: #7d676c; --pink: #d6436a; --line: #f1e2da; }
@media (prefers-color-scheme: dark) { :root { --bg: #221b1d; --card: #2d2427; --ink: #f4e9ec; --soft: #bfaab0; --pink: #ff8fa6; --line: #3d3135; } }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.7 -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Noto Sans KR", sans-serif; }
main { max-width: 760px; margin: 0 auto; padding: 40px 16px 64px; }
header { text-align: center; margin-bottom: 28px; }
h1 { font-size: 34px; margin: 0; letter-spacing: -0.5px; }
.tag { font-size: 18px; margin: 2px 0 12px; color: var(--pink); font-weight: 600; }
.intro { color: var(--soft); margin: 0 auto; max-width: 34em; }
h2 { font-size: 15px; color: var(--soft); font-weight: 600; margin: 32px 4px 0; }
.app { display: flex; gap: 16px; background: var(--card); border: 1px solid var(--line); border-radius: 20px; padding: 18px; margin: 12px 0; }
.app img { width: 76px; height: 76px; border-radius: 17px; flex: none; }
.app h3 { font-size: 19px; margin: 0; line-height: 1.35; }
.app p { margin: 4px 0 8px; color: var(--soft); }
.badge { font-size: 13px; color: var(--soft); border: 1px solid var(--line); border-radius: 99px; padding: 1px 9px; margin-right: 4px; white-space: nowrap; }
.links a { color: var(--pink); margin-right: 14px; font-size: 15px; font-weight: 600; white-space: nowrap; }
footer { text-align: center; color: var(--soft); font-size: 14px; margin-top: 40px; }
footer a { color: inherit; }
""".strip()


def store_url(app, lang):
    return f"https://apps.apple.com/{'kr/' if lang == 'ko' or app.get('kr_only') else ''}app/id{app['id']}"


def page_url(app, lang):
    return (app.get("page_en") if lang == "en" else None) or app["page"]


def json_ld(lang, t):
    return {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": f"{BASE}/#org", "name": BRAND, "alternateName": BRAND_KO,
             "url": f"{BASE}/", "email": EMAIL, "description": t["intro"]},
            {"@type": "ItemList", "name": t["apps"], "itemListElement": [
                {"@type": "ListItem", "position": i, "item": {
                    "@type": "MobileApplication", "name": app[lang][0], "description": app[lang][1],
                    "url": BASE + page_url(app, lang), "installUrl": store_url(app, lang),
                    "image": f"{BASE}/images/{app['slug']}.jpg", "operatingSystem": "iOS",
                    "applicationCategory": "GameApplication" if app["kind"] == "game" else "PhotographyApplication",
                    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW" if lang == "ko" else "USD"},
                    "publisher": {"@id": f"{BASE}/#org"}}}
                for i, app in enumerate(APPS, 1)]},
        ],
    }


def card(app, lang, t):
    name, desc = app[lang]
    note = f" {t['kr_only']}" if app.get("kr_only") and t["kr_only"] else ""
    return f"""  <article class="app">
    <img src="/images/{app['slug']}.jpg" alt="{escape(name)}" width="76" height="76" loading="lazy">
    <div>
      <h3>{escape(name)}</h3>
      <p>{escape(desc + note)}</p>
      <div class="links">
        <span class="badge">{t[app['kind']]}</span><span class="badge">{t['free']}</span>
        <a href="{store_url(app, lang)}">{t['store']}</a>
        <a href="{page_url(app, lang)}">{t['more']}</a>
      </div>
    </div>
  </article>"""


def html(lang):
    t = T[lang]
    url = BASE + t["path"]
    ld = json.dumps(json_ld(lang, t), ensure_ascii=False, indent=1).replace("</", "<\\/")
    cards = "\n".join(card(a, lang, t) for a in APPS)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(t['title'])}</title>
<meta name="description" content="{escape(t['desc'])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ko" href="{BASE}/">
<link rel="alternate" hreflang="en" href="{BASE}/en/">
<link rel="alternate" hreflang="x-default" href="{BASE}/en/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{escape(t['title'])}">
<meta property="og:description" content="{escape(t['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/images/og.png">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{ld}
</script>
<style>
{CSS}
</style>
</head>
<body>
<main>
  <header>
    <h1>{BRAND}</h1>
    <p class="tag">{t['tagline']}</p>
    <p class="intro">{escape(t['intro'])}</p>
  </header>
  <h2>{t['apps']}</h2>
{cards}
  <footer>
    <p>{t['contact']}: <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{t['other_path']}">{t['other']}</a></p>
    <p>© 2026 {BRAND}</p>
  </footer>
</main>
</body>
</html>
"""


def sitemap():
    paths = ["/", "/en/"]
    for a in APPS:
        paths += [a["page"]] + ([a["page_en"]] if a.get("page_en") else [])
    urls = "\n".join(f"  <url><loc>{BASE}{p}</loc></url>" for p in paths)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'


def llms():
    t = T["en"]
    lines = [f"# {BRAND}", "", f"> {t['intro']} Korean name: {BRAND_KO}. All apps listed here are free on the App Store.", "",
             f"- Home (Korean): {BASE}/", f"- Home (English): {BASE}/en/", f"- Contact: {EMAIL}", "", "## Apps and games", ""]
    for a in APPS:
        note = " Korean App Store only." if a.get("kr_only") else ""
        lines.append(f"- [{a['en'][0]}]({BASE}{page_url(a, 'en')}): {a['en'][1]}{note} "
                     f"Korean title: {a['ko'][0]}. iOS, free. App Store: {store_url(a, 'en')}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    (ROOT / "en").mkdir(exist_ok=True)
    (ROOT / "index.html").write_text(html("ko"), encoding="utf-8")
    (ROOT / "en" / "index.html").write_text(html("en"), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (ROOT / "llms.txt").write_text(llms(), encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    print(f"built {len(APPS)} apps")
