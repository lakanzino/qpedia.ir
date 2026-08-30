#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
factcheck.py — بررسی خودکار ادعاهای مقاله در برابر پایگاه‌های بیرونی
====================================================================

⚠ این ابزار «صحت مقاله» را تأیید نمی‌کند.
   فقط چند نوع ادعای *ساختارمند* را می‌سنجد:

   ۱. DOI و ارجاع مقاله   → CrossRef API
   ۲. سال تولد/مرگ دانشمند → Wikidata SPARQL
   ۳. نقل‌قول مستقیم        → باید صفر باشد (قانون ۱)
   ۴. سال بدون منبع        → قانون ۲
   ۵. الگوهای زبانی مشکوک   → قطعیت بیش از حد

   آنچه نمی‌تواند بسنجد در بخش «محدودیت‌ها» فهرست شده.

اجرا:
    python3 factcheck.py batch.json
"""
import sys, json, re, time, urllib.request, urllib.parse

UA = {"User-Agent": "qpedia-factcheck/1.0 (educational; contact via qpedia.ir)"}
TIMEOUT = 30


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)


# ─────────── ۱) DOI ───────────
def check_doi(doi):
    try:
        m = get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}")["message"]
        yr = None
        for k in ("published-print", "published-online", "issued"):
            if k in m:
                yr = m[k]["date-parts"][0][0]
                break
        return {"ok": True, "title": m.get("title", ["?"])[0],
                "year": yr,
                "authors": [a.get("family", "?") for a in m.get("author", [])],
                "journal": (m.get("container-title") or ["?"])[0]}
    except Exception as e:
        return {"ok": False, "err": f"{type(e).__name__}"}


# ─────────── ۲) دانشمندان ───────────
PEOPLE = {
    # ⚠ فقط QIDهایی که با جستجوی زندهٔ Wikidata تأیید شدند.
    #   هر نامی که تأیید نشد، عمداً حذف شده — بهتر از QID غلط.
    "پلانک": "Q9021",        # Max Planck 1858-1947
    "اینشتین": "Q937",       # Albert Einstein 1879-1955
    "بور": "Q7085",          # Niels Bohr 1885-1962
    "دوبروی": "Q83331",      # Louis de Broglie
    "فاینمن": "Q39246",      # Richard Feynman 1918-1988
    "دیراک": "Q47480",       # Paul Dirac 1902-1984
    "هایزنبرگ": "Q40904",    # Werner Heisenberg
    "شرودینگر": "Q9130",     # Erwin Schrodinger 1887-1961
    "میلیکان": "Q130975",    # Robert A. Millikan 1868-1953
    "رادرفورد": "Q9123",     # Ernest Rutherford 1871-1937
    "گاموف": "Q59478",       # George Gamow
    "بالمر": "Q122986",      # Johann Jakob Balmer 1825-1898
    # تأییدنشده و لذا حذف‌شده: یانگ (نتیجه‌ای برنگشت)،
    # تونومورا (جستجو یک پژوهشگر ادبیات برگرداند — شخص اشتباه)،
    # اساکی و ارنفست (خطای نرخ درخواست).
}


def wikidata_people(qids):
    if not qids:
        return {}
    vals = " ".join(f"wd:{q}" for q in qids)
    q = f"""SELECT ?p ?pLabel ?birth ?death WHERE {{
  VALUES ?p {{ {vals} }}
  OPTIONAL {{ ?p wdt:P569 ?birth }} OPTIONAL {{ ?p wdt:P570 ?death }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "fa,en" }} }}"""
    try:
        d = get("https://query.wikidata.org/sparql?format=json&query="
                + urllib.parse.quote(q))
        out = {}
        for b in d["results"]["bindings"]:
            qid = b["p"]["value"].rsplit("/", 1)[-1]
            out[qid] = {"name": b["pLabel"]["value"],
                        "birth": b.get("birth", {}).get("value", "")[:4],
                        "death": b.get("death", {}).get("value", "")[:4]}
        return out
    except Exception as e:
        print(f"  ⚠ Wikidata در دسترس نبود: {type(e).__name__}")
        return {}


# ─────────── ۳) الگوهای زبانی مشکوک ───────────
HEDGE_NEEDED = [
    (r"(?<!احتمالاً )ثابت شده(?! است که این)", "«ثابت شده» — در علم اثبات نداریم، تأیید تجربی داریم"),
    (r"هیچ‌کس نمی‌داند", "ادعای مطلق دربارهٔ دانش بشر"),
    (r"همهٔ دانشمندان", "ادعای اجماع کامل"),
    (r"قطعاً|بی‌شک|بدون شک", "قطعیت بیش از حد"),
    (r"برای اولین بار در تاریخ", "ادعای تقدم — نیازمند منبع"),
    (r"دقیقاً \d+ سال", "دقت کاذب عددی"),
]

FA2EN = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")


def audit(item):
    h = item.get("content_html", "")
    plain = re.sub(r"<[^>]+>", " ", h)
    src = " ".join(item.get("sources", []))
    src_lat = src.translate(FA2EN)
    R = {"errors": [], "warns": [], "info": []}

    # قانون ۱
    nq = h.count('class="qp-quote"')
    if nq:
        R["errors"].append(f"{nq} نقل‌قول مستقیم — قانون ۱ می‌گوید صفر")

    # قانون ۲
    orphan = []
    for y in sorted(set(re.findall(r"[۰-۹]{4}", plain))):
        lat = y.translate(FA2EN)
        if 1500 <= int(lat) <= 2100 and lat not in src_lat and y not in src:
            orphan.append(y)
    if orphan:
        R["warns"].append(f"سال بدون ردیابی در منابع: {'، '.join(orphan)}")

    # الگوهای زبانی
    for pat, why in HEDGE_NEEDED:
        if re.search(pat, plain):
            R["warns"].append(f"الگوی مشکوک: {why}")

    # DOI
    for doi in set(re.findall(r"10\.\d{4,9}/[^\s,;)]+", src)):
        r = check_doi(doi.rstrip(".,"))
        if r["ok"]:
            R["info"].append(f"✅ DOI {doi} → {r['authors']} · {r['journal']} · {r['year']}")
        else:
            R["errors"].append(f"❌ DOI نامعتبر یا یافت نشد: {doi} ({r['err']})")
        time.sleep(0.4)

    # دانشمندان نام‌برده
    named = [n for n in PEOPLE if n in plain]
    R["_people"] = named
    return R


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "batch.json"
    B = json.load(open(src, encoding="utf-8"))
    if isinstance(B, dict):
        B = [B]

    print(f"بررسی خودکار {len(B)} مقاله\n")
    print("⚠ این ابزار صحت علمی را تأیید نمی‌کند — فقط ادعاهای ساختارمند را می‌سنجد.\n")

    allp = set()
    reports = []
    for i, it in enumerate(B, 1):
        R = audit(it)
        allp |= {PEOPLE[n] for n in R["_people"]}
        reports.append((it, R))
        icon = "❌" if R["errors"] else ("⚠" if R["warns"] else "✅")
        print(f"{icon} [{i}] {it.get('title','')}")
        for x in R["errors"]:
            print(f"      ❌ {x}")
        for x in R["warns"]:
            print(f"      ⚠  {x}")
        for x in R["info"]:
            print(f"      {x}")
        if R["_people"]:
            print(f"      👤 {'، '.join(R['_people'])}")

    # دانشمندان
    if allp:
        print(f"\n{'─'*56}\nتاریخ تولد/مرگ از Wikidata:")
        for qid, d in wikidata_people(sorted(allp)).items():
            print(f"  {d['name']:<26} {d['birth']} – {d['death']}")

    ne = sum(len(r["errors"]) for _, r in reports)
    nw = sum(len(r["warns"]) for _, r in reports)
    print(f"\n{'─'*56}")
    print(f"  {ne} خطا · {nw} هشدار")
    print("""
⚠ آنچه این ابزار نمی‌تواند بسنجد:
  · درستی توضیح فیزیکی
  · اینکه آیا روایت تاریخی محل مناقشه است
  · نسبت دادن ایده به شخص اشتباه
  · تفسیر نادرست از داده‌ای درست
  اینها فقط با بازبینی انسانِ متخصص پیدا می‌شوند.""")


if __name__ == "__main__":
    main()
