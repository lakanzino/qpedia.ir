<?php
/**
 * Plugin Name: QPedia 14 Articles Importer (بسته ۲)
 * Plugin URI: https://qpedia.ir
 * Description: درون‌ریز خودکار و یک‌کلیکهٔ ۱۴ مقالهٔ تخصصی جدید دانشنامه کوانتوم‌پدیا در بخش مقالات کوانتوم (quantum_article) به همراه دسته‌بندی سلسله‌مراتبی، چکیده و متادیتا.
 * Version: 2.4.0
 * Author: تیم علمی کوانتوم‌پدیا
 * Author URI: https://qpedia.ir
 * License: GPLv2 or later
 * Text Domain: qpedia-14-importer
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'QPEDIA_IMP14_CPT', 'quantum_article' );
define( 'QPEDIA_IMP14_TAX', 'quantum_category' );
define( 'QPEDIA_IMP14_VERSION', '2.4.0' );

/**
 * افزودن صفحه درون‌ریزی به منوی ابزارها در پیشخوان وردپرس
 */
function qpedia_14_importer_add_admin_menu() {
	add_management_page(
		'درون‌ریز ۱۴ مقاله QPedia (بسته ۲)',
		'درون‌ریز ۱۴ مقاله QPedia (بسته ۲)',
		'manage_options',
		'qpedia-14-importer',
		'qpedia_14_importer_render_page'
	);
}
add_action( 'admin_menu', 'qpedia_14_importer_add_admin_menu' );

/**
 * ایجاد یا دریافت دسته کوانتومی به همراه والد
 *
 * @param string $slug اسلاگ دسته.
 * @param string $name نام دسته.
 * @param string $parent_slug اسلاگ والد.
 * @return int|WP_Error
 */
function qpedia_14_importer_ensure_category( $slug, $name, $parent_slug = '' ) {
	$term = get_term_by( 'slug', $slug, QPEDIA_IMP14_TAX );
	$parent_id = 0;

	if ( ! empty( $parent_slug ) ) {
		$parent_term = get_term_by( 'slug', $parent_slug, QPEDIA_IMP14_TAX );
		if ( $parent_term ) {
			$parent_id = $parent_term->term_id;
		}
	}

	if ( $term ) {
		if ( ! empty( $parent_id ) && $term->parent !== $parent_id ) {
			wp_update_term( $term->term_id, QPEDIA_IMP14_TAX, array( 'parent' => $parent_id ) );
		}
		return (int) $term->term_id;
	}

	$res = wp_insert_term(
		$name,
		QPEDIA_IMP14_TAX,
		array(
			'slug'   => $slug,
			'parent' => $parent_id,
		)
	);

	if ( is_wp_error( $res ) ) {
		return $res;
	}

	return (int) $res['term_id'];
}

/**
 * اجرای عملیات درون‌ریزی مقالات
 *
 * @param string $status وضعیت انتشار (publish یا draft).
 * @return array<string,mixed>
 */
function qpedia_14_importer_execute( $status = 'publish' ) {
	$json_file = plugin_dir_path( __FILE__ ) . 'articles.json';
	if ( ! file_exists( $json_file ) ) {
		return array(
			'success' => false,
			'message' => 'فایل داده‌های مقالات (articles.json) یافت نشد.',
			'logs'    => array(),
		);
	}

	$raw_data = file_get_contents( $json_file );
	$data     = json_decode( $raw_data, true );

	if ( empty( $data ) || ! isset( $data['articles'] ) ) {
		return array(
			'success' => false,
			'message' => 'فرمت داده‌های فایل مقالات نامعتبر است.',
			'logs'    => array(),
		);
	}

	$logs    = array();
	$created = 0;
	$updated = 0;

	// ۱. ایجاد و همگام‌سازی دسته‌ها
	if ( ! empty( $data['categories'] ) ) {
		foreach ( $data['categories'] as $cat ) {
			qpedia_14_importer_ensure_category(
				$cat['slug'] ?? '',
				$cat['name'] ?? '',
				$cat['parent'] ?? ''
			);
		}
	}

	// ۲. واردسازی تک‌تک مقالات
	foreach ( $data['articles'] as $art ) {
		$title   = sanitize_text_field( $art['title'] ?? '' );
		$slug    = sanitize_title( $art['slug'] ?? '' );
		$excerpt = sanitize_textarea_field( $art['excerpt'] ?? '' );
		$content = $art['content'] ?? '';
		$cat_slug = $art['category_slug'] ?? '';

		if ( empty( $title ) || empty( $slug ) ) {
			continue;
		}

		// بررسی وجود پست از قبل
		$existing = get_page_by_path( $slug, OBJECT, QPEDIA_IMP14_CPT );
		$post_id  = 0;

		$post_args = array(
			'post_title'   => $title,
			'post_name'    => $slug,
			'post_content' => $content,
			'post_excerpt' => $excerpt,
			'post_status'  => $status,
			'post_type'    => QPEDIA_IMP14_CPT,
		);

		if ( $existing ) {
			$post_args['ID'] = $existing->ID;
			$post_id = wp_update_post( $post_args );
			$updated++;
			$logs[] = sprintf( '🔄 به‌روزرسانی شد: %s (/ %s /)', esc_html( $title ), esc_html( $slug ) );
		} else {
			$post_id = wp_insert_post( $post_args );
			$created++;
			$logs[] = sprintf( '✅ مقالهٔ جدید درج شد: %s (/ %s /)', esc_html( $title ), esc_html( $slug ) );
		}

		// انتساب دسته
		if ( $post_id && ! is_wp_error( $post_id ) && ! empty( $cat_slug ) ) {
			$term = get_term_by( 'slug', $cat_slug, QPEDIA_IMP14_TAX );
			if ( $term ) {
				wp_set_object_terms( $post_id, array( (int) $term->term_id ), QPEDIA_IMP14_TAX );
			}
		}
	}

	return array(
		'success' => true,
		'message' => sprintf( 'عملیات با موفقیت انجام شد: %d مقاله درج و %d مقاله به‌روزرسانی گردید.', $created, $updated ),
		'logs'    => $logs,
	);
}

/**
 * رندر صفحه پیشخوان افزونه
 */
function qpedia_14_importer_render_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		wp_die( 'شما اجازه دسترسی به این صفحه را ندارید.' );
	}

	$result = null;

	if ( isset( $_POST['qpedia_do_import_14'] ) && check_admin_referer( 'qpedia_import_action_14', 'qpedia_import_nonce_14' ) ) {
		$status = isset( $_POST['post_status'] ) && 'draft' === $_POST['post_status'] ? 'draft' : 'publish';
		$result = qpedia_14_importer_execute( $status );
	}
	?>
	<div class="wrap" style="max-width: 900px; margin-top: 20px; font-family: Tahoma, sans-serif;">
		<h1 style="display: flex; align-items: center; gap: 10px;">
			<span class="dashicons dashicons-database-import" style="font-size: 32px; width: 32px; height: 32px;"></span>
			درون‌ریز ۱۴ مقاله تخصصی جدید دانشنامه کوانتوم‌پدیا (بسته ۲)
		</h1>

		<p style="font-size: 14px; color: #555; line-height: 1.8;">
			این افزونه ۱۴ مقالهٔ استاندارد کوانتومی جدید (شامل متن کامل علمی، سرفصل‌های تخصصی، تیترهای استاندارد، چکیده و دسته‌بندی موضوعی) را با یک کلیک مستقیماً در بخش <strong>مقالات کوانتوم (quantum_article)</strong> سایت شما درج می‌کند.
		</p>

		<?php if ( $result ) : ?>
			<div class="notice notice-<?php echo $result['success'] ? 'success' : 'error'; ?> is-dismissible" style="padding: 15px; margin: 20px 0;">
				<p style="font-weight: bold; font-size: 15px;"><?php echo esc_html( $result['message'] ); ?></p>
				<?php if ( ! empty( $result['logs'] ) ) : ?>
					<div style="max-height: 250px; overflow-y: auto; background: #fff; border: 1px solid #ccd0d4; padding: 12px; margin-top: 10px; border-radius: 4px; font-size: 13px; line-height: 1.8;">
						<?php foreach ( $result['logs'] as $log_line ) : ?>
							<div><?php echo esc_html( $log_line ); ?></div>
						<?php endforeach; ?>
					</div>
				<?php endif; ?>
			</div>
		<?php endif; ?>

		<div class="card" style="padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-top: 20px;">
			<form method="post" action="">
				<?php wp_nonce_field( 'qpedia_import_action_14', 'qpedia_import_nonce_14' ); ?>

				<table class="form-table" role="presentation">
					<tbody>
						<tr>
							<th scope="row"><label for="post_status">وضعیت انتشار مقالات:</label></th>
							<td>
								<select name="post_status" id="post_status" style="min-width: 200px; height: 36px;">
									<option value="publish" selected>انتشار عمومی (Publish)</option>
									<option value="draft">پیش‌نویس (Draft)</option>
								</select>
								<p class="description">پیشنهاد: روی «انتشار عمومی» بگذارید تا مقالات فوراً در سایت قابل مشاهده شوند.</p>
							</td>
						</tr>
					</tbody>
				</table>

				<p class="submit" style="margin-top: 20px;">
					<input type="submit" name="qpedia_do_import_14" class="button button-primary button-hero" value="⚡ شروع درون‌ریزی ۱۴ مقاله" style="font-weight: bold; height: 46px; line-height: 44px; padding: 0 30px;" onclick="return confirm('آیا برای شروع واردسازی ۱۴ مقاله اطمینان دارید؟');" />
				</p>
			</form>
		</div>

		<div class="card" style="padding: 20px; border-radius: 8px; margin-top: 20px; background: #f8fafc;">
			<h3 style="margin-top: 0;">📋 لیست ۱۴ مقاله‌ای که درون‌ریزی می‌شوند:</h3>
			<ol style="line-height: 2; margin-right: 20px; color: #333;">
				<li>عدد کوانتومی چیست؟ (<code>quantum-number</code>)</li>
				<li>اصل مکملیت چیست؟ (<code>complementarity-principle</code>)</li>
				<li>ناظر در کوانتوم چیست؟ (<code>observer</code>)</li>
				<li>اصل عدم قطعیت هایزنبرگ (رویکرد تحلیلی) (<code>uncertainty-principle</code>)</li>
				<li>حالت کوانتومی چیست؟ (<code>quantum-state</code>)</li>
				<li>فضای هیلبرت چیست؟ (<code>hilbert-space</code>)</li>
				<li>عملگر در کوانتوم چیست؟ (<code>operator</code>)</li>
				<li>کامپیوتر کوانتومی چیست؟ (<code>quantum-computer</code>)</li>
				<li>توزیع کلید کوانتومی QKD چیست؟ (<code>quantum-key-distribution</code>)</li>
				<li>گیت کوانتومی چیست؟ (<code>quantum-gate</code>)</li>
				<li>قضیه عدم تکثیر چیست؟ (<code>no-cloning-theorem</code>)</li>
				<li>رمزنگاری کوانتومی چیست؟ (<code>quantum-cryptography</code>)</li>
				<li>رمزنگاری پساکوانتومی PQC چیست؟ (<code>post-quantum-cryptography</code>)</li>
				<li>الگوریتم‌های کوانتومی چیست؟ (<code>quantum-algorithm</code>)</li>
			</ol>
			<p style="color: #666; font-size: 13px; margin-bottom: 0;">💡 پس از اتمام درون‌ریزی، می‌توانید این افزونه را از بخش افزونه‌ها غیرفعال و حذف نمایید.</p>
		</div>
	</div>
	<?php
}
