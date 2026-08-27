#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check.py — سنجش یک صفحهٔ زندهٔ qpedia.ir در برابر چک‌لیست بخش ۷
================================================================
اجرا:
    python3 check.py <slug>                # حدس خودکار نوع
    python3 check.py bra-ket-notation
    python3 check.py --all                 # همهٔ صفحات از آینه

⚠ آنچه این ابزار نمی‌سنجد (بخش ۱۲.۲ دستورالعمل):
    · Core Web Vitals (LCP/INP/CLS)  → pagespeed.web.dev
    · رندر موبایل                     → مرورگر
    · درستی محتوای علمی               → انسان متخصص
"""
import sys, re, json, os, urllib.request, urllib.error

SITE = "https://qpedia.ir"
UA = {"User-Agent": "qpedia-agent-check/1.0"}
PATHS = ["glossary/{}", "{}", "scientists/{}"]

BANNED = ["قانون جذب", "انرژی مثبت", "کائنات", "شعور آب", "طب کوانتومی"]
ABSOLUTE = ["ثابت شده", "همیشه", "به طور قطع", "بی‌شک", "قطعاً",
            "هیچ‌کس نمی‌داند", "همهٔ دانشمندان"]
YMYL = ["درمان", "بیماری", "دارو", "سلامت", "پزشک", "تشخیص"]


def grab(url):
    try:
        with urllib.request.urlopen(
                urllib.request.Request(url, headers=UA), timeout=40) as r:
            return r.read().decode("utf-8", "ignore"), r.status
    except urllib.error.HTTPError as e:
        return "", e.code
    except Exception:
        return "", 0


def find_page(slug):
    for p in PATHS:
        url = f"{SITE}/{p.format(slug)}/"
        h, code = grab(url)
        if code == 200 and len(h) > 5000:
            return url, h
    return None, ""


def check(slug):
    url, h = find_page(slug)
    if not h:
        print(f"❌ صفحه یافت نشد: {slug}")
        return None

    ok, bad, warn, manual = [], [], [], []

    def g(pat):
        m = re.search(pat, h, re.I | re.S)
        return m.group(1).strip() if m else None

    # ── الف) سلامت فنی ──
    (ok if url.startswith("https://") else bad).append("HTTPS و URL خوانا")

    t = g(r"<title[^>]*>(.*?)</title>")
    (ok if t and len(t) < 120 else bad).append(f"title یکتا ({len(t) if t else 0} نویسه)")

    d = g(r'name=["\']description["\'][^>]*content=["\'](.*?)["\']')
    if d and 70 <= len(d) <= 170:
        ok.append(f"meta description ({len(d)} نویسه)")
    elif d:
        warn.append(f"meta description طولش {len(d)} — بازهٔ ۷۰–۱۷۰")
    else:
        bad.append("meta description ندارد")

    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    (ok if len(h1) == 1 else bad).append(f"h1 یکتا (تعداد={len(h1)})")

    hs = [int(m) for m in re.findall(r"<h([2-4])[^>]*>", h)]
    (ok if hs else warn).append(f"سلسله‌مراتب عناوین ({len(hs)} تیتر)")

    imgs = re.findall(r"<img[^>]*>", h)
    noalt = [i for i in imgs if 'alt=' not in i]
    (ok if not noalt else warn).append(f"alt تصاویر ({len(noalt)} بدون alt از {len(imgs)})")

    (ok if 'name="viewport"' in h else bad).append("viewport موبایل")
    (ok if g(r'rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']') else bad).append("canonical")

    ld = re.findall(r'application/ld\+json[^>]*>(.*?)</script>', h, re.S)
    types = set(re.findall(r'"@type"\s*:\s*"([^"]+)"', " ".join(ld)))
    if types & {"Article", "DefinedTerm", "ScholarlyArticle", "Person"}:
        ok.append(f"Schema: {'، '.join(sorted(types))}")
    else:
        bad.append(f"Schema ناکافی (فقط {'، '.join(sorted(types)) or 'هیچ'})")

    # نقشهٔ سایت
    _, sc = grab(f"{SITE}/sitemap.xml")
    _, sc2 = grab(f"{SITE}/wp-sitemap.xml")
    (ok if 200 in (sc, sc2) else bad).append("نقشهٔ سایت XML")

    # ── ب) کیفیت محتوا ──
    art = re.search(r"<article.*?</article>", h, re.S)
    body = art.group(0) if art else h
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body))
    wc = len(text.split())
    if wc >= 600:
        ok.append(f"عمق محتوا ({wc} کلمه)")
    elif wc >= 300:
        warn.append(f"محتوای متوسط ({wc} کلمه)")
    else:
        bad.append(f"محتوای نازک ({wc} کلمه)")

    (ok if g(r'article:published_time["\'][^>]*content=["\'](.*?)["\']')
     else warn).append("تاریخ انتشار")

    has_author = bool(g(r'name=["\']author["\'][^>]*content=["\'](.*?)["\']')) \
                 or "qp-ab-nm" in h or '"author"' in " ".join(ld)
    (ok if has_author else bad).append("نویسندهٔ مشخص")

    inl = len(set(re.findall(r'href="https://qpedia\.ir(/[^"#?]*)"', h)))
    (ok if inl >= 3 else warn).append(f"لینک داخلی ({inl})")

    # ── ج) محتوای کم‌ارزش و ریسک ──
    hits = [b for b in BANNED if b in text]
    if hits:
        warn.append(f"اصطلاح شبه‌علمی: {'، '.join(hits)} — اگر «نقد شبه‌علم» است مجاز")
    else:
        ok.append("بدون اصطلاح شبه‌علمی")

    abs_hit = [a for a in ABSOLUTE if a in text]
    (ok if not abs_hit else warn).append(
        f"زبان محتاطانه" + (f" — یافت شد: {'، '.join(abs_hit)}" if abs_hit else ""))

    nq = body.count('class="qp-quote"')
    (ok if nq == 0 else warn).append(f"نقل‌قول مستقیم ({nq}) — قانون: صفر")

    if [y for y in YMYL if y in text]:
        manual.append("محتوای نزدیک به YMYL — نیازمند بازبینی متخصص و هشدار")

    # سال بدون منبع در متن
    years = sorted(set(re.findall(r"[۰-۹]{4}", text)))
    if years:
        manual.append(f"راستی‌آزمایی سال‌ها: {'، '.join(years[:12])}")

    manual += ["Core Web Vitals → pagespeed.web.dev",
               "رندر موبایل → مرورگر",
               "درستی علمی محتوا → متخصص انسانی"]

    # ── گزارش ──
    print(f"\n{'═'*62}")
    print(f"  {url}")
    print(f"{'═'*62}")
    for x in ok:
        print(f"  ✅ {x}")
    for x in warn:
        print(f"  ⚠  {x}")
    for x in bad:
        print(f"  ❌ {x}")
    print(f"\n  ── نیازمند اقدام انسانی ──")
    for x in manual:
        print(f"  👤 {x}")

    verdict = "مسدود برای انتشار" if bad else ("قابل انتشار با هشدار" if warn else "تأیید")
    print(f"\n  {'─'*58}")
    print(f"  ✅ {len(ok)} قبول · ⚠ {len(warn)} هشدار · ❌ {len(bad)} مردود")
    print(f"  حکم: {verdict}")
    return {"slug": slug, "ok": len(ok), "warn": len(warn),
            "bad": len(bad), "verdict": verdict}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--all":
        p = "/home/user/qpedia-mirror/data/quantum_term.json"
        if not os.path.exists(p):
            sys.exit("اول sync.py را اجرا کنید.")
        rows = [check(x["slug"]) for x in json.load(open(p, encoding="utf-8"))[:5]]
        print(f"\n{'═'*62}\nجمع: {len([r for r in rows if r and r['bad']])} صفحه مسدود")
    else:
        check(sys.argv[1])


if __name__ == "__main__":
    main()
