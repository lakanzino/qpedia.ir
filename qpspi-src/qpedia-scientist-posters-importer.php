<?php
/**
 * Plugin Name:       QPedia — تصاویر شاخص دانشمندان
 * Plugin URI:        https://qpedia.ir
 * Description:       اعمال پوسترهای WebP دانشمندان به‌عنوان تصویر شاخصِ مدخل‌های quantum_scientist با یک کلیک. منبع تصاویر: فایل‌های داخل خود افزونه (پوشهٔ images) یا پوشهٔ آپلود دلخواه شما.
 * Version:           1.0.0
 * Author:            QPedia
 * Author URI:        https://qpedia.ir
 * Text Domain:       qpspi
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'QPSPI_VERSION', '1.0.0' );
define( 'QPSPI_DIR', plugin_dir_path( __FILE__ ) );
define( 'QPSPI_IMAGES_DIR', QPSPI_DIR . 'images' . DIRECTORY_SEPARATOR );
define( 'QPSPI_DEFAULT_UPLOAD_SUBDIR', 'qpedia-scientist-posters' );
define( 'QPSPI_ALLOWED_EXT', array( 'webp', 'png', 'jpg', 'jpeg' ) );

/* -------------------------------------------------------------------------
 * منوی ابزارها
 * ---------------------------------------------------------------------- */
add_action( 'admin_menu', 'qpspi_admin_menu' );
function qpspi_admin_menu() {
	add_management_page(
		'تصاویر شاخص دانشمندان',
		'تصاویر شاخص دانشمندان',
		'manage_options',
		'qpspi-posters',
		'qpspi_render_page'
	);
}

/* -------------------------------------------------------------------------
 * ابزارهای کمکی
 * ---------------------------------------------------------------------- */
function qpspi_norm( $s ) {
	$s = strtolower( (string) $s );
	$map = array(
		'ö' => 'o', 'ü' => 'u', 'ä' => 'a', 'é' => 'e', 'è' => 'e',
		'á' => 'a', 'à' => 'a', 'í' => 'i', 'ó' => 'o', 'ú' => 'u',
		'ñ' => 'n', 'ç' => 'c', 'š' => 's', 'ž' => 'z', 'ß' => 'ss',
	);
	$s = strtr( $s, $map );
	$s = preg_replace( '/[^a-z0-9]+/', '', $s );
	return $s;
}

function qpspi_surname_token( $base ) {
	$parts = explode( '-', $base );
	$last  = end( $parts );
	if ( strlen( $last ) < 4 ) {
		return '';
	}
	return qpspi_norm( $last );
}

/* اصلاحات شناخته‌شدهٔ اسلاگ در سایت زنده */
function qpspi_known_aliases() {
	return array(
		'max-planck' => array( 'max-plank' ),
	);
}

function qpspi_all_scientists() {
	$ids = get_posts( array(
		'post_type'      => 'quantum_scientist',
		'post_status'    => array( 'publish', 'draft', 'pending', 'private' ),
		'posts_per_page' => -1,
		'fields'         => 'ids',
		'orderby'        => 'title',
		'order'          => 'ASC',
	) );
	return $ids;
}

/* پیدا کردن مدخل دانشمند برای یک نام‌فایل (مثلاً louis-de-broglie) */
function qpspi_find_scientist( $base ) {
	$ids   = qpspi_all_scientists();
	$norm  = qpspi_norm( $base );
	$alias = qpspi_known_aliases();

	$alias_norms = array();
	if ( isset( $alias[ $base ] ) ) {
		foreach ( $alias[ $base ] as $a ) {
			$alias_norms[] = qpspi_norm( $a );
		}
	}

	/* گام ۱: تطبیق دقیق اسلاگ / نام انگلیسی / عنوان */
	foreach ( $ids as $pid ) {
		$post  = get_post( $pid );
		$slug  = qpspi_norm( $post->post_name );
		$en    = qpspi_norm( get_post_meta( $pid, '_scientist_en_name', true ) );
		$title = qpspi_norm( $post->post_title );

		if ( $slug === $norm || $en === $norm || $title === $norm ) {
			return $pid;
		}
		foreach ( $alias_norms as $an ) {
			if ( $slug === $an || $en === $an || $title === $an ) {
				return $pid;
			}
		}
	}

	/* گام ۲: تطبیق با نام خانوادگی (توکن آخر) — فقط اگر یکتا باشد */
	$token = qpspi_surname_token( $base );
	if ( '' !== $token ) {
		$hits = array();
		foreach ( $ids as $pid ) {
			$post = get_post( $pid );
			$hay  = qpspi_norm( $post->post_name )
				. ' ' . qpspi_norm( get_post_meta( $pid, '_scientist_en_name', true ) )
				. ' ' . qpspi_norm( $post->post_title );
			if ( false !== strpos( $hay, $token ) ) {
				$hits[] = $pid;
			}
		}
		if ( 1 === count( $hits ) ) {
			return $hits[0];
		}
	}

	return 0;
}

/* لیست نام‌فایل‌های موجود به تفکیک منبع */
function qpspi_source_files( $source, $custom_dir = '' ) {
	$files = array();
	if ( 'bundled' === $source ) {
		if ( is_dir( QPSPI_IMAGES_DIR ) ) {
			foreach ( QPSPI_ALLOWED_EXT as $ext ) {
				$glob = glob( QPSPI_IMAGES_DIR . '*.' . $ext );
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
			$dir = trailingslashit( $up['basedir'] ) . QPSPI_DEFAULT_UPLOAD_SUBDIR;
		}
		if ( is_dir( $dir ) ) {
			foreach ( QPSPI_ALLOWED_EXT as $ext ) {
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

/* آپلود محتوای یک تصویر به کتابخانهٔ رسانه و بازگرداندن attachment_id (با جلوگیری از تکرار) */
function qpspi_import_image( $basename, $contents ) {
	require_once ABSPATH . 'wp-admin/includes/file.php';

	/* اگر تصویری با همین نام قبلاً وارد شده، همان را برگردان */
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
		return new WP_Error( 'qpspi_upload', $upload['error'] );
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
function qpspi_build_plan( $source, $custom_dir ) {
	$files = qpspi_source_files( $source, $custom_dir );
	$plan  = array();
	foreach ( $files as $base => $path ) {
		$pid = qpspi_find_scientist( $base );
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
add_action( 'admin_init', 'qpspi_handle_actions' );
function qpspi_handle_actions() {
	if ( ! isset( $_POST['qpspi_nonce'] ) || ! isset( $_POST['qpspi_action'] ) ) {
		return;
	}
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$action = sanitize_key( $_POST['qpspi_action'] );
	if ( 'preview' !== $action && 'apply' !== $action ) {
		return;
	}
	if ( ! wp_verify_nonce( $_POST['qpspi_nonce'], 'qpspi_action' ) ) {
		wp_die( 'خطای امنیتی (nonce). صفحه را دوباره باز کنید.' );
	}

	$source     = isset( $_POST['qpspi_source'] ) ? sanitize_key( $_POST['qpspi_source'] ) : 'bundled';
	$custom_dir = isset( $_POST['qpspi_custom_dir'] ) ? sanitize_text_field( wp_unslash( $_POST['qpspi_custom_dir'] ) ) : '';
	$overwrite  = isset( $_POST['qpspi_overwrite'] ) && '1' === $_POST['qpspi_overwrite'];

	if ( ! in_array( $source, array( 'bundled', 'folder' ), true ) ) {
		$source = 'bundled';
	}

	$plan = qpspi_build_plan( $source, $custom_dir );

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
			$attach = qpspi_import_image( basename( $item['path'] ), $contents );
			if ( is_wp_error( $attach ) ) {
				$report['fail'][] = array( 'base' => $item['base'], 'why' => $attach->get_error_message() );
				continue;
			}
			set_post_thumbnail( $item['post'], $attach );
			$report['ok'][] = array( 'base' => $item['base'], 'post' => $item['post'] );
		}

		set_transient( 'qpspi_report', $report, 120 );
		set_transient( 'qpspi_plan', $plan, 120 );
		wp_safe_redirect( admin_url( 'tools.php?page=qpspi-posters&qpspi_done=1' ) );
		exit;
	}

	if ( 'preview' === $action ) {
		set_transient( 'qpspi_plan', $plan, 120 );
		wp_safe_redirect( admin_url( 'tools.php?page=qpspi-posters&qpspi_preview=1' ) );
		exit;
	}
}

/* -------------------------------------------------------------------------
 * صفحهٔ ابزار
 * ---------------------------------------------------------------------- */
function qpspi_render_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}

	$total_scientists = count( qpspi_all_scientists() );
	$bundled_files    = qpspi_source_files( 'bundled' );
	$up               = wp_upload_dir();
	$default_dir      = trailingslashit( $up['basedir'] ) . QPSPI_DEFAULT_UPLOAD_SUBDIR;
	$folder_files     = qpspi_source_files( 'folder', $default_dir );

	$show_preview = isset( $_GET['qpspi_preview'] );
	$show_done    = isset( $_GET['qpspi_done'] );
	$plan         = get_transient( 'qpspi_plan' );
	$report       = get_transient( 'qpspi_report' );

	echo '<div class="wrap">';
	echo '<h1>🖼️ تصاویر شاخص دانشمندان</h1>';

	echo '<p style="max-width:820px">این ابزار، پوسترهای دانشمندان را به‌عنوان <strong>تصویر شاخص</strong> مدخل‌های <code>quantum_scientist</code> ثبت می‌کند. تطبیق بر اساس نام‌فایل (مثلاً <code>louis-de-broglie.webp</code>) با اسلاگ / نام انگلیسی / عنوان انجام می‌شود. پیش از اعمال، حتماً «پیش‌نمایش تطبیق» را بزنید.</p>';

	/* کارت وضعیت */
	echo '<div style="display:flex;flex-wrap:wrap;gap:14px;margin:14px 0">';
	echo '<div style="border:1px solid #dcdcde;border-radius:8px;padding:12px 16px;min-width:160px"><div style="font-size:22px;font-weight:700">' . (int) $total_scientists . '</div><div style="color:#646970">مدخل دانشمند</div></div>';
	echo '<div style="border:1px solid #dcdcde;border-radius:8px;padding:12px 16px;min-width:160px"><div style="font-size:22px;font-weight:700">' . (int) count( $bundled_files ) . '</div><div style="color:#646970">تصویر داخل افزونه</div></div>';
	echo '<div style="border:1px solid #dcdcde;border-radius:8px;padding:12px 16px;min-width:160px"><div style="font-size:22px;font-weight:700">' . (int) count( $folder_files ) . '</div><div style="color:#646970">تصویر در پوشهٔ آپلود</div></div>';
	echo '</div>';

	if ( ! empty( $bundled_files ) ) {
		echo '<p style="color:#646970">✅ حالت <strong>تصاویر داخل افزونه</strong> فعال است (این افزونه همراه ' . (int) count( $bundled_files ) . ' پوستر ارسال شده).</p>';
	} else {
		echo '<p style="color:#b32d2e">این نسخه تصویرِ همراه ندارد. پوسترها را در پوشهٔ آپلود قرار دهید و از حالت «پوشهٔ آپلود» استفاده کنید.</p>';
	}

	/* فرم */
	echo '<form method="post" action="">';
	wp_nonce_field( 'qpspi_action', 'qpspi_nonce' );
	echo '<h2>۱) منبع تصاویر</h2>';
	echo '<table class="form-table"><tbody>';
	echo '<tr><th scope="row">منبع</th><td>';
	echo '<label style="margin-inline-end:16px"><input type="radio" name="qpspi_source" value="bundled" ' . ( isset( $_POST['qpspi_source'] ) && 'folder' === $_POST['qpspi_source'] ? '' : 'checked' ) . '> تصاویر داخل افزونه (پوشهٔ images)</label>';
	echo '<label><input type="radio" name="qpspi_source" value="folder" ' . ( isset( $_POST['qpspi_source'] ) && 'folder' === $_POST['qpspi_source'] ? 'checked' : '' ) . '> پوشهٔ آپلود (مسیر روی سرور)</label>';
	echo '</td></tr>';
	echo '<tr><th scope="row">مسیر پوشهٔ آپلود</th><td><input type="text" name="qpspi_custom_dir" class="regular-text" style="direction:ltr;text-align:left" placeholder="' . esc_attr( $default_dir ) . '" value="' . esc_attr( isset( $_POST['qpspi_custom_dir'] ) ? $_POST['qpspi_custom_dir'] : '' ) . '"><p class="description">پیش‌فرض: <code style="direction:ltr;display:inline-block">' . esc_html( $default_dir ) . '</code> — فایل‌های WebP را با همان نام اسلاگ (مثلاً <code>louis-de-broglie.webp</code>) در آن بریزید.</p></td></tr>';
	echo '<tr><th scope="row">گزینه‌ها</th><td><label><input type="checkbox" name="qpspi_overwrite" value="1"> بازنویسی تصویر شاخصِ دانشمندانی که قبلاً تصویر دارند</label></td></tr>';
	echo '</tbody></table>';

	echo '<p class="submit">';
	echo '<button type="submit" name="qpspi_action" value="preview" class="button button-secondary">👁 پیش‌نمایش تطبیق (بدون تغییر)</button> ';
	echo '<button type="submit" name="qpspi_action" value="apply" class="button button-primary">⬇ اعمال تصاویر شاخص</button>';
	echo '</p>';
	echo '</form>';

	/* نتایج preview */
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

	/* نتایج apply */
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

	/* جدول تشخیصی همهٔ دانشمندان */
	echo '<h2>۲) فهرست مدخل‌های موجود (برای تطبیق نام‌فایل‌ها)</h2>';
	$ids = qpspi_all_scientists();
	if ( empty( $ids ) ) {
		echo '<p style="color:#b32d2e">هیچ مدخل <code>quantum_scientist</code> یافت نشد. ابتدا مدخل‌های دانشمندان را وارد کنید.</p>';
	} else {
		echo '<table class="widefat striped" style="max-width:900px"><thead><tr><th>ID</th><th>اسلاگ</th><th>نام انگلیسی (متا)</th><th>عنوان</th><th>تصویر شاخص</th></tr></thead><tbody>';
		foreach ( $ids as $pid ) {
			$p   = get_post( $pid );
			$en  = get_post_meta( $pid, '_scientist_en_name', true );
			$th  = (int) get_post_thumbnail_id( $pid );
			echo '<tr>';
			echo '<td>' . (int) $pid . '</td>';
			echo '<td><code style="direction:ltr">' . esc_html( $p->post_name ) . '</code></td>';
			echo '<td style="direction:ltr;text-align:left">' . esc_html( $en ? $en : '—' ) . '</td>';
			echo '<td>' . esc_html( $p->post_title ) . '</td>';
			echo '<td>' . ( $th ? '✅ دارد' : '—' ) . '</td>';
			echo '</tr>';
		}
		echo '</tbody></table>';
	}

	echo '</div>';
}
