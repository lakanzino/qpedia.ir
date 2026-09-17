<?php
/**
 * Plugin Name: Qpedia Featured Importer (one-shot)
 * Description: جایگزینی اجباری تصاویر شاخص مقالات کوانتوم از روی اسلاگ. بعد از اجرا، افزونه را حذف کنید.
 * Version: 1.0.0
 */

defined( 'ABSPATH' ) || exit;

add_action( 'admin_menu', 'qp_feat_import_menu' );
function qp_feat_import_menu() {
	add_management_page(
		'ایمپورتر تصاویر شاخص',
		'ایمپورتر تصاویر',
		'manage_options',
		'qp-feat-import',
		'qp_feat_import_page'
	);
}

function qp_feat_import_images() {
	$dir   = plugin_dir_path( __FILE__ ) . 'images/';
	$files = array();
	if ( ! is_dir( $dir ) ) {
		return $files;
	}
	foreach ( scandir( $dir ) as $f ) {
		if ( '.webp' === substr( $f, -5 ) ) {
			$files[] = $dir . $f;
		}
	}
	sort( $files );
	return $files;
}

function qp_feat_import_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}

	$files  = qp_feat_import_images();
	$total  = count( $files );
	$batch  = 10;
	$offset = isset( $_GET['qp_offset'] ) ? max( 0, intval( $_GET['qp_offset'] ) ) : 0;
	$run    = isset( $_GET['qp_run'] ) && '1' === $_GET['qp_run'];

	$log     = array();
	$done    = 0;
	$skipped = 0;
	$errors  = 0;

	if ( $run && $offset < $total ) {
		check_admin_referer( 'qp_feat_run' );
		require_once ABSPATH . 'wp-admin/includes/media.php';
		require_once ABSPATH . 'wp-admin/includes/file.php';
		require_once ABSPATH . 'wp-admin/includes/image.php';

		foreach ( array_slice( $files, $offset, $batch ) as $path ) {
			$slug = sanitize_title( basename( $path, '.webp' ) );
			$post = get_page_by_path( $slug, OBJECT, 'quantum_article' );

			if ( ! $post instanceof WP_Post ) {
				$log[] = '⏭ ' . $slug . ' — مقاله پیدا نشد';
				$skipped++;
				continue;
			}

			$data = @file_get_contents( $path );
			if ( false === $data ) {
				$log[] = '❌ ' . $slug . ' — خواندن فایل ناممکن بود';
				$errors++;
				continue;
			}

			$bits = wp_upload_bits( basename( $path ), null, $data );
			if ( ! empty( $bits['error'] ) ) {
				$log[] = '❌ ' . $slug . ' — خطای آپلود: ' . $bits['error'];
				$errors++;
				continue;
			}

			$att_id = wp_insert_attachment(
				array(
					'post_mime_type' => 'image/webp',
					'post_title'     => $post->post_title,
					'post_status'    => 'inherit',
				),
				$bits['file'],
				$post->ID
			);
			if ( ! $att_id || is_wp_error( $att_id ) ) {
				$log[] = '❌ ' . $slug . ' — خطای درج در مدیا';
				$errors++;
				continue;
			}

			wp_update_attachment_metadata( $att_id, wp_generate_attachment_metadata( $att_id, $bits['file'] ) );

			$old = get_post_thumbnail_id( $post->ID );
			if ( $old && (int) $old !== (int) $att_id ) {
				wp_delete_attachment( $old, true );
			}
			set_post_thumbnail( $post->ID, $att_id );

			$log[] = '✅ ' . $slug . ' (#' . $post->ID . ')';
			$done++;
		}
	}

	$next     = $offset + $batch;
	$finished = $run && $next >= $total;

	echo '<div class="wrap"><h1>ایمپورتر تصاویر شاخص</h1>';
	echo '<p>تعداد تصاویر داخل افزونه: <b>' . esc_html( number_format_i18n( $total ) ) . '</b></p>';

	if ( ! $run ) {
		echo '<p>با زدن دکمه، برای هر تصویر (نام فایل = اسلاگ مقاله) تصویر شاخص جایگزین و تصویر قبلی <b>حذف</b> می‌شود.</p>';
		$url = wp_nonce_url(
			add_query_arg( array( 'page' => 'qp-feat-import', 'qp_run' => '1', 'qp_offset' => 0 ), admin_url( 'tools.php' ) ),
			'qp_feat_run'
		);
		echo '<p><a class="button button-primary button-large" href="' . esc_url( $url ) . '">شروع جایگزینی</a></p>';
	} else {
		echo '<p>پیشرفت: <b>' . esc_html( number_format_i18n( min( $next, $total ) ) ) . ' از ' . esc_html( number_format_i18n( $total ) ) . '</b></p>';
		if ( $log ) {
			echo '<div style="background:#fff;border:1px solid #ccd0d4;padding:12px 16px;max-width:640px;font-size:13px;line-height:2">';
			foreach ( $log as $line ) {
				echo esc_html( $line ) . '<br>';
			}
			echo '</div>';
		}
		if ( $finished ) {
			echo '<h2>✅ تمام شد</h2>';
			echo '<p>حالا: ۱) کش LiteSpeed را پاک کنید ۲) این افزونه را <b>حذف</b> کنید.</p>';
		} else {
			$url = wp_nonce_url(
				add_query_arg( array( 'page' => 'qp-feat-import', 'qp_run' => '1', 'qp_offset' => $next ), admin_url( 'tools.php' ) ),
				'qp_feat_run'
			);
			echo '<p>در حال ادامه… <a href="' . esc_url( $url ) . '">ادامه دستی</a></p>';
			echo '<script>setTimeout(function(){window.location.href=' . wp_json_encode( $url ) . ';},900);</script>';
		}
	}
	echo '</div>';
}
