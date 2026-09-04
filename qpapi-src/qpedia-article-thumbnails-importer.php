<?php
/**
 * Plugin Name:       QPedia — تصاویر شاخص مقالات
 * Plugin URI:        https://qpedia.ir
 * Description:       اعمال هدرهای WebP مقالات به‌عنوان تصویر شاخصِ مدخل‌های quantum_article با یک کلیک. منبع تصاویر: فایل‌های داخل خود افزونه (پوشهٔ images) یا پوشهٔ آپلود دلخواه شما.
 * Version:           1.0.0
 * Author:            QPedia
 * Author URI:        https://qpedia.ir
 * Text Domain:       qpapi
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'QPAPI_VERSION', '1.0.0' );
define( 'QPAPI_DIR', plugin_dir_path( __FILE__ ) );
define( 'QPAPI_IMAGES_DIR', QPAPI_DIR . 'images' . DIRECTORY_SEPARATOR );
define( 'QPAPI_DEFAULT_UPLOAD_SUBDIR', 'qpedia-article-thumbnails' );
define( 'QPAPI_ALLOWED_EXT', array( 'webp', 'png', 'jpg', 'jpeg' ) );

/* -------------------------------------------------------------------------
 * منوی ابزارها
 * ---------------------------------------------------------------------- */
add_action( 'admin_menu', 'qpapi_admin_menu' );
function qpapi_admin_menu() {
	add_management_page(
		'تصاویر شاخص مقالات',
		'تصاویر شاخص مقالات',
		'manage_options',
		'qpapi-thumbs',
		'qpapi_render_page'
	);
}

/* -------------------------------------------------------------------------
 * ابزارهای کمکی
 * ---------------------------------------------------------------------- */
function qpapi_norm( $s ) {
	$s = strtolower( (string) $s );
	$s = preg_replace( '/[^a-z0-9]+/', '-', $s );
	$s = trim( $s, '-' );
	return $s;
}

function qpapi_all_articles() {
	return get_posts( array(
		'post_type'      => 'quantum_article',
		'post_status'    => array( 'publish', 'draft', 'pending', 'private' ),
		'posts_per_page' => -1,
		'fields'         => 'ids',
		'orderby'        => 'title',
		'order'          => 'ASC',
	) );
}

/* پیدا کردن مدخل مقاله برای یک نام‌فایل (مثلاً quantum-state) */
function qpapi_find_article( $base ) {
	$ids  = qpapi_all_articles();
	$norm = qpapi_norm( $base );

	/* گام ۱: تطبیق دقیق اسلاگ */
	foreach ( $ids as $pid ) {
		$post = get_post( $pid );
		if ( qpapi_norm( $post->post_name ) === $norm ) {
			return $pid;
		}
	}

	/* گام ۲: تطبیق عنوان (نرمال‌شده) */
	foreach ( $ids as $pid ) {
		$post = get_post( $pid );
		if ( qpapi_norm( $post->post_title ) === $norm ) {
			return $pid;
		}
	}

	return 0;
}

/* لیست نام‌فایل‌های موجود به تفکیک منبع */
function qpapi_source_files( $source, $custom_dir = '' ) {
	$files = array();
	if ( 'bundled' === $source ) {
		if ( is_dir( QPAPI_IMAGES_DIR ) ) {
			foreach ( QPAPI_ALLOWED_EXT as $ext ) {
				$glob = glob( QPAPI_IMAGES_DIR . '*.' . $ext );
				if ( is_array( $glob ) ) {
					foreach ( $glob as $p ) {
						$files[ basename( $p, '.' . $ext ) ] = $p;
					}
				}
			}
		}
	} elseif ( 'folder' === $source ) {
		$dir = rtrim( $custom_dir, '/\\' );
		if ( '' === $dir ) {
			$up  = wp_upload_dir();
			$dir = trailingslashit( $up['basedir'] ) . QPAPI_DEFAULT_UPLOAD_SUBDIR;
		}
		if ( is_dir( $dir ) ) {
			foreach ( QPAPI_ALLOWED_EXT as $ext ) {
				$glob = glob( $dir . '/*.' . $ext );
				if ( is_array( $glob ) ) {
					foreach ( $glob as $p ) {
						$files[ basename( $p, '.' . $ext ) ] = $p;
					}
				}
			}
		}
	}
	ksort( $files );
	return $files;
}

/* آپلود محتوای یک تصویر به کتابخانهٔ رسانه (با جلوگیری از تکرار) */
function qpapi_import_image( $basename, $contents ) {
	require_once ABSPATH . 'wp-admin/includes/file.php';

	$existing = get_posts( array(
		'post_type'      => 'attachment',
		'post_status'    => 'inherit',
		'posts_per_page' => 1,
		'fields'         => 'ids',
		'meta_query'     => array(
			array(
				'key'     => '_wp_attached_file',
				'value'   => $basename,
				'compare' => 'LIKE',
			),
		),
	) );
	if ( ! empty( $existing ) ) {
		return (int) $existing[0];
	}

	$upload = wp_upload_bits( $basename, null, $contents );
	if ( ! empty( $upload['error'] ) ) {
		return new WP_Error( 'qpapi_upload', $upload['error'] );
	}

	$filetype = wp_check_filetype( $basename, null );
	$mime     = ! empty( $filetype['type'] ) ? $filetype['type'] : 'image/webp';
	$title    = preg_replace( '/\.[^.]+$/', '', $basename );

	$attach_id = wp_insert_attachment( array(
		'post_mime_type' => $mime,
		'post_title'     => $title,
		'post_content'   => '',
		'post_status'    => 'inherit',
	), $upload['file'] );

	if ( is_wp_error( $attach_id ) ) {
		return $attach_id;
	}

	$meta = array();
	if ( function_exists( 'wp_getimagesize' ) ) {
		$size = @wp_getimagesize( $upload['file'] );
	} else {
		$size = @getimagesize( $upload['file'] );
	}
	if ( is_array( $size ) && ! empty( $size[0] ) ) {
		$meta['width']  = (int) $size[0];
		$meta['height'] = (int) $size[1];
		$meta['file']   = basename( $upload['file'] );
	}
	wp_update_attachment_metadata( $attach_id, $meta );

	return (int) $attach_id;
}

/* محاسبهٔ نتیجهٔ تطبیق (بدون تغییر چیزی) */
function qpapi_build_plan( $source, $custom_dir ) {
	$files = qpapi_source_files( $source, $custom_dir );
	$plan  = array();
	foreach ( $files as $base => $path ) {
		$pid = qpapi_find_article( $base );
		$plan[] = array(
			'base' => $base,
			'path' => $path,
			'post' => $pid,
		);
	}
	return $plan;
}

/* -------------------------------------------------------------------------
 * پردازش فرم‌ها
 * ---------------------------------------------------------------------- */
add_action( 'admin_init', 'qpapi_handle_actions' );
function qpapi_handle_actions() {
	if ( ! isset( $_POST['qpapi_nonce'] ) || ! isset( $_POST['qpapi_action'] ) ) {
		return;
	}
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$action = sanitize_key( $_POST['qpapi_action'] );
	if ( 'preview' !== $action && 'apply' !== $action ) {
		return;
	}
	if ( ! wp_verify_nonce( $_POST['qpapi_nonce'], 'qpapi_action' ) ) {
		wp_die( 'خطای امنیتی (nonce). صفحه را دوباره باز کنید.' );
	}

	$source     = isset( $_POST['qpapi_source'] ) ? sanitize_key( $_POST['qpapi_source'] ) : 'bundled';
	$custom_dir = isset( $_POST['qpapi_custom_dir'] ) ? sanitize_text_field( wp_unslash( $_POST['qpapi_custom_dir'] ) ) : '';
	$overwrite  = isset( $_POST['qpapi_overwrite'] ) && '1' === $_POST['qpapi_overwrite'];

	if ( ! in_array( $source, array( 'bundled', 'folder' ), true ) ) {
		$source = 'bundled';
	}

	$plan = qpapi_build_plan( $source, $custom_dir );

	if ( 'apply' === $action ) {
		$report = array( 'ok' => array(), 'skip' => array(), 'fail' => array() );

		foreach ( $plan as $item ) {
			if ( empty( $item['post'] ) ) {
				$report['fail'][] = array( 'base' => $item['base'], 'why' => 'مدخل پیدا نشد' );
				continue;
			}
			$has = (int) get_post_thumbnail_id( $item['post'] );
			if ( $has && ! $overwrite ) {
				$report['skip'][] = array( 'base' => $item['base'], 'post' => $item['post'], 'why' => 'تصویر شاخص دارد' );
				continue;
			}
			$contents = @file_get_contents( $item['path'] );
			if ( false === $contents ) {
				$report['fail'][] = array( 'base' => $item['base'], 'why' => 'خواندن فایل ناموفق' );
				continue;
			}
			$attach = qpapi_import_image( basename( $item['path'] ), $contents );
			if ( is_wp_error( $attach ) ) {
				$report['fail'][] = array( 'base' => $item['base'], 'why' => $attach->get_error_message() );
				continue;
			}
			set_post_thumbnail( $item['post'], $attach );
			$report['ok'][] = array( 'base' => $item['base'], 'post' => $item['post'] );
		}

		set_transient( 'qpapi_report', $report, 120 );
		set_transient( 'qpapi_plan', $plan, 120 );
		wp_safe_redirect( admin_url( 'tools.php?page=qpapi-thumbs&qpapi_done=1' ) );
		exit;
	}

	if ( 'preview' === $action ) {
		set_transient( 'qpapi_plan', $plan, 120 );
		wp_safe_redirect( admin_url( 'tools.php?page=qpapi-thumbs&qpapi_preview=1' ) );
		exit;
	}
}

/* -------------------------------------------------------------------------
 * صفحهٔ ابزار
 * ---------------------------------------------------------------------- */
function qpapi_render_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}

	$total_articles = count( qpapi_all_articles() );
	$bundled_files  = qpapi_source_files( 'bundled' );
	$up             = wp_upload_dir();
	$default_dir    = trailingslashit( $up['basedir'] ) . QPAPI_DEFAULT_UPLOAD_SUBDIR;
	$folder_files   = qpapi_source_files( 'folder', $default_dir );

	$show_preview = isset( $_GET['qpapi_preview'] );
	$show_done    = isset( $_GET['qpapi_done'] );
	$plan         = get_transient( 'qpapi_plan' );
	$report       = get_transient( 'qpapi_report' );

	echo '<div class="wrap">';
	echo '<h1>🖼️ تصاویر شاخص مقالات</h1>';

	echo '<p style="max-width:820px">این ابزار، هدرهای مقالات را به‌عنوان <strong>تصویر شاخص</strong> مدخل‌های <code>quantum_article</code> ثبت می‌کند. تطبیق بر اساس نام‌فایل (مثلاً <code>quantum-state.webp</code>) با اسلاگ / عنوان انجام می‌شود. پیش از اعمال، حتماً «پیش‌نمایش تطبیق» را بزنید.</p>';

	echo '<div style="display:flex;flex-wrap:wrap;gap:14px;margin:14px 0">';
	echo '<div style="border:1px solid #dcdcde;border-radius:8px;padding:12px 16px;min-width:160px"><div style="font-size:22px;font-weight:700">' . (int) $total_articles . '</div><div style="color:#646970">مدخل مقاله</div></div>';
	echo '<div style="border:1px solid #dcdcde;border-radius:8px;padding:12px 16px;min-width:160px"><div style="font-size:22px;font-weight:700">' . (int) count( $bundled_files ) . '</div><div style="color:#646970">تصویر داخل افزونه</div></div>';
	echo '<div style="border:1px solid #dcdcde;border-radius:8px;padding:12px 16px;min-width:160px"><div style="font-size:22px;font-weight:700">' . (int) count( $folder_files ) . '</div><div style="color:#646970">تصویر در پوشهٔ آپلود</div></div>';
	echo '</div>';

	if ( ! empty( $bundled_files ) ) {
		echo '<p style="color:#646970">✅ حالت <strong>تصاویر داخل افزونه</strong> فعال است (این افزونه همراه ' . (int) count( $bundled_files ) . ' هدر ارسال شده).</p>';
	} else {
		echo '<p style="color:#b32d2e">این نسخه تصویرِ همراه ندارد. هدرها را در پوشهٔ آپلود قرار دهید و از حالت «پوشهٔ آپلود» استفاده کنید.</p>';
	}

	echo '<form method="post" action="">';
	wp_nonce_field( 'qpapi_action', 'qpapi_nonce' );
	echo '<h2>۱) منبع تصاویر</h2>';
	echo '<table class="form-table"><tbody>';
	echo '<tr><th scope="row">منبع</th><td>';
	echo '<label style="margin-inline-end:16px"><input type="radio" name="qpapi_source" value="bundled" ' . ( isset( $_POST['qpapi_source'] ) && 'folder' === $_POST['qpapi_source'] ? '' : 'checked' ) . '> تصاویر داخل افزونه (پوشهٔ images)</label>';
	echo '<label><input type="radio" name="qpapi_source" value="folder" ' . ( isset( $_POST['qpapi_source'] ) && 'folder' === $_POST['qpapi_source'] ? 'checked' : '' ) . '> پوشهٔ آپلود (مسیر روی سرور)</label>';
	echo '</td></tr>';
	echo '<tr><th scope="row">مسیر پوشهٔ آپلود</th><td><input type="text" name="qpapi_custom_dir" class="regular-text" style="direction:ltr;text-align:left" placeholder="' . esc_attr( $default_dir ) . '" value="' . esc_attr( isset( $_POST['qpapi_custom_dir'] ) ? $_POST['qpapi_custom_dir'] : '' ) . '"><p class="description">پیش‌فرض: <code style="direction:ltr;display:inline-block">' . esc_html( $default_dir ) . '</code> — فایل‌های WebP را با همان نام اسلاگ (مثلاً <code>quantum-state.webp</code>) در آن بریزید.</p></td></tr>';
	echo '<tr><th scope="row">گزینه‌ها</th><td><label><input type="checkbox" name="qpapi_overwrite" value="1"> بازنویسی تصویر شاخصِ مقاله‌هایی که قبلاً تصویر دارند</label></td></tr>';
	echo '</tbody></table>';

	echo '<p class="submit">';
	echo '<button type="submit" name="qpapi_action" value="preview" class="button button-secondary">👁 پیش‌نمایش تطبیق (بدون تغییر)</button> ';
	echo '<button type="submit" name="qpapi_action" value="apply" class="button button-primary">⬇ اعمال تصاویر شاخص</button>';
	echo '</p>';
	echo '</form>';

	if ( $show_preview && is_array( $plan ) ) {
		echo '<h2>پیش‌نمایش تطبیق</h2>';
		$ok = 0; $miss = 0;
		echo '<table class="widefat striped" style="max-width:820px"><thead><tr><th>نام‌فایل</th><th>مدخل</th></tr></thead><tbody>';
		foreach ( $plan as $item ) {
			if ( ! empty( $item['post'] ) ) {
				$p = get_post( $item['post'] );
				echo '<tr><td><code style="direction:ltr">' . esc_html( $item['base'] ) . '</code></td><td style="color:#007017">' . esc_html( $p->post_title ) . ' <small style="color:#646970;direction:ltr;display:inline-block">(' . esc_html( $p->post_name ) . ')</small></td></tr>';
				$ok++;
			} else {
				echo '<tr><td><code style="direction:ltr">' . esc_html( $item['base'] ) . '</code></td><td style="color:#b32d2e">⚠️ پیدا نشد</td></tr>';
				$miss++;
			}
		}
		echo '</tbody></table>';
		echo '<p><strong>' . (int) $ok . '</strong> تطبیق موفق · <strong style="color:#b32d2e">' . (int) $miss . '</strong> پیدا نشد.</p>';
		if ( $miss > 0 ) {
			echo '<p style="color:#646970">برای موارد پیدا‌نشده، نام‌فایل را با اسلاگ واقعی مدخل (ستون زیر) هم‌نام کنید و دوباره پیش‌نمایش بگیرید.</p>';
		}
	}

	if ( $show_done && is_array( $report ) ) {
		echo '<h2>نتیجهٔ اعمال</h2>';
		echo '<table class="widefat striped" style="max-width:820px"><thead><tr><th>نام‌فایل</th><th>وضعیت</th></tr></thead><tbody>';
		foreach ( $report['ok'] as $r ) {
			$p = get_post( $r['post'] );
			echo '<tr><td><code style="direction:ltr">' . esc_html( $r['base'] ) . '</code></td><td style="color:#007017">✅ تصویر شاخص شد — ' . esc_html( $p->post_title ) . '</td></tr>';
		}
		foreach ( $report['skip'] as $r ) {
			$p = get_post( $r['post'] );
			echo '<tr><td><code style="direction:ltr">' . esc_html( $r['base'] ) . '</code></td><td style="color:#b35600">↷ رد شد (تصویر دارد) — ' . esc_html( $p->post_title ) . '</td></tr>';
		}
		foreach ( $report['fail'] as $r ) {
			echo '<tr><td><code style="direction:ltr">' . esc_html( $r['base'] ) . '</code></td><td style="color:#b32d2e">✗ ' . esc_html( $r['why'] ) . '</td></tr>';
		}
		echo '</tbody></table>';
		echo '<p><strong>' . count( $report['ok'] ) . '</strong> موفق · <strong>' . count( $report['skip'] ) . '</strong> ردشده · <strong style="color:#b32d2e">' . count( $report['fail'] ) . '</strong> ناموفق.</p>';
	}

	echo '<h2>۲) فهرست مدخل‌های موجود (برای تطبیق نام‌فایل‌ها)</h2>';
	$ids = qpapi_all_articles();
	if ( empty( $ids ) ) {
		echo '<p style="color:#b32d2e">هیچ مدخل <code>quantum_article</code> یافت نشد.</p>';
	} else {
		echo '<table class="widefat striped" style="max-width:900px"><thead><tr><th>ID</th><th>اسلاگ</th><th>عنوان</th><th>تصویر شاخص</th></tr></thead><tbody>';
		foreach ( $ids as $pid ) {
			$p  = get_post( $pid );
			$th = (int) get_post_thumbnail_id( $pid );
			echo '<tr>';
			echo '<td>' . (int) $pid . '</td>';
			echo '<td><code style="direction:ltr">' . esc_html( $p->post_name ) . '</code></td>';
			echo '<td>' . esc_html( $p->post_title ) . '</td>';
			echo '<td>' . ( $th ? '✅ دارد' : '—' ) . '</td>';
			echo '</tr>';
		}
		echo '</tbody></table>';
	}

	echo '</div>';
}
