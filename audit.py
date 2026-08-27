#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit.py — اسکن شروع جلسه (بند ۳ دستورالعمل)
=============================================
ورک‌اسپیس را اسکن می‌کند و وضعیت را گزارش می‌دهد.
⚠ هیچ چیزی حذف نمی‌کند — فقط شناسایی و پیشنهاد (بند ۱۲.۲).
"""
import os, json, subprocess, urllib.request
from datetime import datetime

ROOT = "/home/user"
SKIP = {".arena", ".cache", "__pycache__", "node_modules", ".git",
        ".venv", "dist", "build", ".npm"}

# پروژه‌های شناخته‌شدهٔ مرتبط با qpedia
KNOWN = {
    "AGENT": "دستورالعمل و ابزار سنجش",
    "estelahat": "موتور تولید محتوا (tpl.py, gen/)",
    "qpedia-audit": "افزونه‌های وردپرس و گزارش‌ها",
    "qpedia-bot": "ربات انتشار REST",
    "qpedia-offline": "خط لولهٔ آفلاین + مقالات",
    "qpedia-mirror": "آینهٔ محتوای سایت",
    "daneshmandan": "موتور تولید زندگینامهٔ دانشمندان (w1-w5.py)",
    "maghalat": "موتور تولید مقالات + گزارش‌ها",
    "repos": "مخازن گیت — شامل Qpedia-map",
    "uploads": "تصاویر و اسکرین‌شات‌های ارسالی کاربر",
}


def walk():
    """پوشه‌های سطح اول + شمارش."""
    rows = []
    for d in sorted(os.listdir(ROOT)):
        p = os.path.join(ROOT, d)
        if d.startswith(".") or not os.path.isdir(p):
            continue
        n = sz = 0
        for dp, dn, fn in os.walk(p):
            dn[:] = [x for x in dn if x not in SKIP]
            for f in fn:
                try:
                    sz += os.path.getsize(os.path.join(dp, f))
                    n += 1
                except OSError:
                    pass
        rows.append((d, n, sz))
    return rows


def loose_files():
    return [f for f in sorted(os.listdir(ROOT))
            if os.path.isfile(os.path.join(ROOT, f)) and not f.startswith(".")]


def site_status():
    out = {}
    for label, url in [("سایت", "https://qpedia.ir/"),
                       ("REST", "https://qpedia.ir/wp-json/"),
                       ("نقشهٔ سایت", "https://qpedia.ir/sitemap.xml")]:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "qpedia-audit/1.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                out[label] = r.status
        except Exception as e:
            out[label] = getattr(e, "code", "خطا")
    return out


def mirror_counts():
    d = os.path.join(ROOT, "qpedia-mirror", "data")
    if not os.path.isdir(d):
        return None, None
    c, when = {}, None
    for f in sorted(os.listdir(d)):
        if f.startswith("tax_") or not f.endswith(".json"):
            continue
        p = os.path.join(d, f)
        try:
            c[f[:-5]] = len(json.load(open(p, encoding="utf-8")))
            when = datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M")
        except Exception:
            pass
    return c, when


def pending():
    """کارهای باز شناخته‌شده."""
    items = []
    p = os.path.join(ROOT, "qpedia-offline", "batch.json")
    if os.path.exists(p):
        try:
            b = json.load(open(p, encoding="utf-8"))
            nq = sum(x["content_html"].count("qp-quote") for x in b)
            items.append(f"batch.json: {len(b)} مقالهٔ آماده، {nq} نقل‌قول "
                         f"({'✅ پاک' if nq == 0 else '⚠ باید صفر باشد'}) — منتشرنشده")
        except Exception:
            pass
    if os.path.exists(os.path.join(ROOT, "qpedia-audit/importer/qpedia-header-fix.php")):
        items.append("qpedia-header-fix.php آماده — روی سایت نصب نشده")
    return items


def main():
    print("═" * 60)
    print("  اسکن شروع جلسه —", datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("═" * 60)

    print("\n▸ پوشه‌های ورک‌اسپیس")
    tot_f = tot_s = 0
    unknown = []
    for d, n, sz in walk():
        tag = KNOWN.get(d)
        mark = "✅" if tag else "❓"
        if not tag:
            unknown.append(d)
        print(f"  {mark} {d:<18} {n:>4} فایل  {sz/1024:>8.0f} KB   {tag or 'نامشخص'}")
        tot_f += n
        tot_s += sz
    print(f"     {'جمع':<18} {tot_f:>4} فایل  {tot_s/1024:>8.0f} KB")

    lf = loose_files()
    if lf:
        print(f"\n▸ فایل‌های ریشه ({len(lf)})")
        for f in lf:
            print(f"     {f}")

    print("\n▸ وضعیت سایت زنده")
    for k, v in site_status().items():
        print(f"  {'✅' if v == 200 else '❌'} {k:<14} HTTP {v}")

    c, when = mirror_counts()
    print("\n▸ آینهٔ محتوا")
    if c:
        print(f"  آخرین همگام‌سازی: {when}")
        for k, v in c.items():
            print(f"     {k:<22} {v}")
    else:
        print("  ⚠ آینه موجود نیست — python3 qpedia-mirror/sync.py")

    pd = pending()
    if pd:
        print("\n▸ کارهای باز")
        for x in pd:
            print(f"  · {x}")

    print("\n▸ موارد نامرتبط (بند ۳)")
    if unknown:
        for u in unknown:
            print(f"  ❓ {u} — نیازمند تصمیم کاربر (حذف نمی‌کنم)")
    else:
        print("  ✅ همهٔ پوشه‌ها مرتبط با پروژه‌اند")

    print("\n" + "═" * 60)


if __name__ == "__main__":
    main()
