<?php
/**
 * Plugin Name: Qpedia Site Fixes (اصلاحات ساختاری — یک‌بارمصرف)
 * Plugin URI: https://qpedia.ir
 * Description: حذف رکورد تکراری اینشتین (slug عددی «2060») و اصلاح اسلاگ ماکس پلانک (max-plank → max-planck). پس از اجرا، این افزونه حذف شود.
 * Version: 1.0.0
 * Author: QPedia
 * License: GPL-2.0-or-later
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'admin_menu', function () {
	add_management_page( 'اصلاحات کیوپدیا', 'اصلاحات کیوپدیا', 'manage_options', 'qpedia-fixes', 'qpedia_fixes_screen' );
} );

function qpedia_fixes_screen() {
	if ( ! current_user_can( 'manage_options' ) ) { wp_die( 'دسترسی ندارید.' ); }
	echo '<div class="wrap" dir="rtl"><h1>اصلاحات ساختاری کیوپدیا</h1>';

	// ۱) حذف رکورد تکراری اینشتین (slug «2060»)
	if ( isset( $_POST['qpf_fix_einstein'] ) && check_admin_referer( 'qpf_run' ) ) {
		$dup = get_posts(
			array(
				'post_type'      => 'quantum_scientist',
				'name'           => '2060',
				'post_status'    => 'any',
				'posts_per_page' => 1,
				'fields'         => 'ids',
			)
		);
		if ( ! empty( $dup ) ) {
			$id = (int) $dup[0];
			$t  = get_the_title( $id );
			wp_delete_post( $id, true );
			echo '<div class="notice notice-success"><p>رکورد تکراری اینشتین حذف شد: <strong>' . esc_html( $t ) . '</strong> (شناسه ' . intval( $id ) . ')</p></div>';
		} else {
			echo '<div class="notice notice-info"><p>رکوردی با slug «2060» پیدا نشد (شاید قبلاً حذف شده).</p></div>';
		}
	}

	// ۲) اصلاح اسلاگ ماکس پلانک
	if ( isset( $_POST['qpf_fix_planck'] ) && check_admin_referer( 'qpf_run' ) ) {
		$p = get_posts(
			array(
				'post_type'      => 'quantum_scientist',
				'name'           => 'max-plank',
				'post_status'    => 'any',
				'posts_per_page' => 1,
				'fields'         => 'ids',
			)
		);
		if ( ! empty( $p ) ) {
			$id = (int) $p[0];
			$r  = wp_update_post( array( 'ID' => $id, 'post_name' => 'max-planck' ) );
			if ( $r && ! is_wp_error( $r ) ) {
				echo '<div class="notice notice-success"><p>اسلاگ ماکس پلانک اصلاح شد: <code>max-plank</code> → <code>max-planck</code> (وردپرس ریدایرکت خودکار از اسلاگ قدیمی ثبت می‌کند).</p></div>';
			} else {
				echo '<div class="notice notice-error"><p>اصلاح اسلاگ ناموفق بود.</p></div>';
			}
		} else {
			echo '<div class="notice notice-info"><p>اسلاگ «max-plank» پیدا نشد (شاید قبلاً اصلاح شده).</p></div>';
		}
	}

	echo '<p>دو اصلاح ساختاری/سئویی کوچک برای سایت (هرکدام با یک کلیک):</p>';
	echo '<table class="widefat striped" style="max-width:820px"><thead><tr><th>مشکل</th><th>اقدام</th></tr></thead><tbody>';
	echo '<tr><td>رکورد تکراری «آلبرت اینشتین» با slug عددی <code>2060</code></td><td>حذف رکورد تکراری</td></tr>';
	echo '<tr><td>املای غلط اسلاگ ماکس پلانک: <code>max-plank</code> به‌جای <code>max-planck</code></td><td>اصلاح اسلاگ + ریدایرکت خودکار</td></tr>';
	echo '</tbody></table>';

	echo '<form method="post" style="margin-top:14px">';
	wp_nonce_field( 'qpf_run' );
	echo '<button name="qpf_fix_einstein" class="button button-primary">۱) حذف اینشتینِ تکراری</button> ';
	echo '<button name="qpf_fix_planck" class="button button-primary">۲) اصلاح اسلاگ پلانک</button></form>';

	echo '<div class="notice notice-warning"><p>پس از اجرای هر دو، این افزونه را حذف کنید.</p></div>';
	echo '</div>';
}
