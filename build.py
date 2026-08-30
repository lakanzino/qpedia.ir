#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — خط لولهٔ آفلاین کیوپدیا
==================================
از متادیتا + بدنه، سه خروجی می‌سازد. هیچ تماسی با سایت نمی‌گیرد.

    preview.html   پیش‌نمایش کامل با CSS واقعی سایت — در مرورگر باز کنید
    review.md      برگهٔ بازبینی: منابع، اعداد، هشدارها
    importer.php   افزونهٔ یک‌بارمصرف — نصب، وارد کردن، حذف

اجرا:
    python3 build.py batch.json
"""
import sys, os, json, re, base64
from datetime import datetime

sys.path.insert(0, "/home/user/estelahat")
sys.path.insert(0, "/home/user/estelahat/gen")
import tpl

OUT = os.path.dirname(os.path.abspath(__file__))

TERM_CATS = {
    "مفاهیم بنیادی": 75, "ریاضیات کوانتومی": 76, "آزمایش‌ها و پدیده‌ها": 77,
    "اطلاعات و تفسیرها": 78, "ذرات بنیادی": 79, "مفاهیم تکمیلی و فناوری‌ها": 80,
}
BANNED = ["قانون جذب", "انرژی مثبت", "کائنات", "شعور آب", "طب کوانتومی"]


def validate(it):
    e, w = [], []
    for f in ("title", "slug", "content_html"):
        if not it.get(f):
            e.append(f"فیلد «{f}» خالی است")
    s = it.get("slug", "")
    if s and not re.fullmatch(r"[a-z0-9\-]+", s):
        e.append(f"اسلاگ نامعتبر: «{s}»")
    c = it.get("category")
    if c and c not in TERM_CATS:
        e.append(f"دستهٔ «{c}» روی سایت نیست. مجاز: {'، '.join(TERM_CATS)}")
    body = it.get("content_html", "")
    if body and not body.lstrip().startswith('<article class="qp-card'):
        e.append("ساختار qp-card ندارد — از tpl.card() تولید نشده؟")
    if "<style" in body:
        e.append("تگ <style> در محتوا — CSS باید از افزونهٔ سایت بیاید")
    hits = [b for b in BANNED if b in body]
    if hits:
        e.append(f"اصطلاح شبه‌علمی: {'، '.join(hits)}")

    # ── قانون ۱: نقل‌قول مستقیم ممنوع مگر با تأیید صریح ──
    nq = body.count('class="qp-quote"')
    if nq and not it.get("quote_verified"):
        e.append(f"{nq} نقل‌قول مستقیم بدون پرچم quote_verified — "
                 f"قانون ۱: یا حذف کن یا در همین جلسه متن دقیقش را جستجو کن")

    # ── قانون ۲: هر سال باید در منابع ردیابی شود ──
    src = " ".join(it.get("sources", []))
    src_lat = src.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))
    plain = re.sub(r"<[^>]+>", " ", body)
    years = set(re.findall(r"[۰-۹]{4}", plain))
    orphan = []
    for y in years:
        lat = y.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))
        if not (1500 <= int(lat) <= 2100):
            continue
        if lat not in src_lat and y not in src:
            orphan.append(y)
    if orphan:
        w.append(f"سال بدون ردیابی در منابع: {'، '.join(sorted(orphan))} "
                 f"← قانون ۲")

    d = it.get("desc", "")
    if not d:
        w.append("توضیح متا ندارد")
    elif not (70 <= len(d) <= 170):
        w.append(f"متا {len(d)} نویسه (بازهٔ ۷۰–۱۷۰)")
    if len(it.get("title", "")) > 90:
        w.append("عنوان بلند")
    if body and len(body) < 1500:
        w.append(f"محتوا {len(body)} نویسه — کوتاه")
    if not it.get("sources"):
        w.append("منبع ندارد")
    return e, w


def numbers(txt):
    """هر عدد را برای راستی‌آزمایی دستی بیرون می‌کشد."""
    plain = re.sub(r"<[^>]+>", " ", txt)
    return sorted(set(re.findall(r"[۰-۹0-9]{2,}(?:[.,][۰-۹0-9]+)?", plain)))


PHP_TEMPLATE = r'''<?php
/**
 * Plugin Name: Qpedia Batch Importer (یک‌بارمصرف)
 * Description: وارد کردن __N__ کارت به‌صورت پیش‌نویس. پس از استفاده حذف کنید.
 * Version: 1.0.0
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

function qbi_payload() {
	$b64 =
__CHUNKS__
	return json_decode( base64_decode( $b64 ), true );
}

add_action( 'admin_menu', function () {
	add_management_page( 'ورود دسته‌ای کیوپدیا', 'ورود کیوپدیا',
		'edit_posts', 'qbi', 'qbi_screen' );
} );

function qbi_screen() {
	if ( ! current_user_can( 'edit_posts' ) ) { wp_die( 'دسترسی ندارید.' ); }
	$rows = qbi_payload();
	echo '<div class="wrap" dir="rtl"><h1>ورود دسته‌ای کیوپدیا</h1>';
	echo '<p>' . count( $rows ) . ' کارت آمادهٔ ورود به‌صورت <strong>پیش‌نویس</strong>.</p>';

	if ( isset( $_POST['qbi_go'] ) && check_admin_referer( 'qbi_run' ) ) {
		echo '<div class="notice notice-info"><ul>';
		$new = 0; $upd = 0;
		foreach ( $rows as $r ) {
			$ex  = get_page_by_path( $r['slug'], OBJECT, 'quantum_term' );
			$arg = array(
				'post_type'    => 'quantum_term',
				'post_title'   => $r['title'],
				'post_name'    => $r['slug'],
				'post_content' => $r['content'],
				'post_excerpt' => $r['desc'],
				'post_status'  => 'draft',
			);
			if ( $ex ) {
				$arg['ID'] = $ex->ID;
				$id = wp_update_post( $arg );
				$upd++; $v = 'به‌روزرسانی';
			} else {
				$id = wp_insert_post( $arg );
				$new++; $v = 'ایجاد';
			}

			if ( $id && ! is_wp_error( $id ) ) {
				if ( ! empty( $r['cat'] ) ) {
					wp_set_object_terms( $id, array( (int) $r['cat'] ), 'quantum_term_category' );
				}
				echo '<li>✅ ' . esc_html( $v ) . ' #' . intval( $id ) . ' — ' . esc_html( $r['title'] ) . '</li>';
			} else {
				echo '<li>❌ ناموفق — ' . esc_html( $r['title'] ) . '</li>';
			}
		}
		echo '</ul><p><strong>' . $new . ' ایجاد · ' . $upd . ' به‌روزرسانی</strong></p></div>';
		echo '<p><a class="button button-primary" href="' .
			esc_url( admin_url( 'edit.php?post_type=quantum_term&post_status=draft' ) ) .
			'">دیدن پیش‌نویس‌ها</a></p>';
		echo '<div class="notice notice-warning"><p>کار تمام شد. ' .
			'<strong>حالا این افزونه را حذف کنید.</strong></p></div>';
	} else {
		echo '<table class="widefat striped" style="max-width:820px"><thead><tr>' .
			'<th>عنوان</th><th>اسلاگ</th><th>حجم</th></tr></thead><tbody>';
		foreach ( $rows as $r ) {
			echo '<tr><td>' . esc_html( $r['title'] ) . '</td><td><code>' .
				esc_html( $r['slug'] ) . '</code></td><td>' .
				number_format_i18n( mb_strlen( $r['content'] ) ) . ' نویسه</td></tr>';
		}
		echo '</tbody></table><form method="post" style="margin-top:18px">';
		wp_nonce_field( 'qbi_run' );
		echo '<button name="qbi_go" class="button button-primary button-hero">' .
			'ورود به‌صورت پیش‌نویس</button></form>';
	}
	echo '</div>';
}
'''


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "batch.json"
    items = json.load(open(src, encoding="utf-8"))
    if isinstance(items, dict):
        items = [items]

    ok, bad, rows = [], 0, []
    print(f"پردازش {len(items)} مورد از {src}\n")
    for i, it in enumerate(items, 1):
        e, w = validate(it)
        icon = "❌" if e else ("⚠" if w else "✅")
        print(f"{icon} [{i}] {it.get('title','')[:48]}")
        for x in e:
            print(f"      ❌ {x}")
        for x in w:
            print(f"      ⚠  {x}")
        if e:
            bad += 1
        else:
            ok.append(it)
        rows.append((it, e, w))

    if not ok:
        sys.exit("\n⛔ هیچ موردی سالم نبود. چیزی ساخته نشد.")

    # ── ۱) پیش‌نمایش بصری ──
    cards = "\n<hr class='qbi-sep'>\n".join(x["content_html"] for x in ok)
    prev = (
        '<!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f'<title>پیش‌نمایش — {len(ok)} کارت</title>\n<style>\n'
        'body{margin:0;background:#070b1e;padding:18px}\n'
        ".qbi-sep{border:0;height:1px;background:rgba(125,220,255,.2);margin:34px 0}\n"
        '.qbi-bar{font:600 13px system-ui;color:#7ddcff;background:rgba(0,212,255,.08);'
        'border:1px solid rgba(0,212,255,.25);border-radius:10px;padding:9px 13px;'
        'margin-bottom:16px;direction:rtl}\n'
        f'{tpl.CSS}\n</style></head><body>\n'
        f'<div class="qbi-bar">پیش‌نمایش آفلاین · {len(ok)} کارت · '
        f'{datetime.now():%Y-%m-%d %H:%M} · CSS واقعی سایت ({len(tpl.CSS):,} نویسه)</div>\n'
        f'{cards}\n</body></html>'
    )
    open(f"{OUT}/preview.html", "w", encoding="utf-8").write(prev)

    # ── ۲) برگهٔ بازبینی ──
    md = [f"# برگهٔ بازبینی — {datetime.now():%Y-%m-%d}\n",
          f"{len(ok)} کارت آماده · {bad} مورد رد شد\n",
          "پیش‌نمایش بصری: `preview.html`\n", "---\n"]
    for it, e, w in rows:
        if e:
            continue
        md.append(f"## {it['title']}\n")
        md.append(f"- **اسلاگ:** `{it['slug']}` → `/glossary/{it['slug']}/`")
        cat = it.get("category", "—")
        md.append(f"- **دسته:** {cat} (id={TERM_CATS.get(cat,'?')})")
        md.append(f"- **طول:** {len(it['content_html']):,} نویسه")
        nums = numbers(it["content_html"])
        if nums:
            md.append(f"- **⚠ اعداد برای راستی‌آزمایی:** {' · '.join(nums[:18])}")
        md.append("- **منابع:**")
        for s in it.get("sources", ["⚠ ندارد"]):
            md.append(f"    - {s}")
        if w:
            md.append(f"- **هشدار:** {'؛ '.join(w)}")
        md.append("\n**چک‌لیست:**")
        md.append("- [ ] اعداد و تاریخ‌ها درست است")
        md.append("- [ ] نام دانشمندان و سال‌ها درست است")
        md.append("- [ ] لحن با بقیهٔ سایت یکی است")
        md.append("- [ ] دسته درست است\n\n---\n")
    open(f"{OUT}/review.md", "w", encoding="utf-8").write("\n".join(md))

    # ── ۳) افزونهٔ یک‌بارمصرف ──
    payload = [{"title": x["title"], "slug": x["slug"], "desc": x.get("desc", ""),
                "cat": TERM_CATS.get(x.get("category"), 0),
                "content": x["content_html"]} for x in ok]
    b64 = base64.b64encode(json.dumps(payload, ensure_ascii=False).encode()).decode()
    parts = [f"\t\t'{b64[i:i+76]}'" for i in range(0, len(b64), 76)]
    chunks = " .\n".join(parts) + ";"
    php = PHP_TEMPLATE.replace("__N__", str(len(ok))).replace("__CHUNKS__", chunks)
    open(f"{OUT}/importer.php", "w", encoding="utf-8").write(php)

    print(f"\n{'─'*54}")
    print(f"  ✅ {len(ok)} سالم · ❌ {bad} رد")
    for f in ("preview.html", "review.md", "importer.php"):
        print(f"  · {f}  ({os.path.getsize(os.path.join(OUT,f)):,} بایت)")
    print(f"\n  مرحلهٔ بعد: preview.html را در مرورگر باز کنید.")


if __name__ == "__main__":
    main()
