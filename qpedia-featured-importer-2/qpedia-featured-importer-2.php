<?php
/**
 * Plugin Name: Qpedia Featured Importer 2 (one-shot)
 * Description: جایگزینی اجباری سری دوم تصاویر شاخص + ثبت آلت. بعد از اجرا، افزونه را حذف کنید.
 * Version: 2.0.0
 */

defined( 'ABSPATH' ) || exit;

function qp_feat2_alts() {
	return array(
		'superfluidity' => 'تصویر شاخص مقالهٔ «ابرشارگی؛ مایعی که از لیوان بالا می‌رود»',
		'fiber-optics' => 'تصویر شاخص مقالهٔ «فیبر نوری چگونه کار می‌کند؟»',
		'aspect-experiment-1982' => 'تصویر شاخص مقالهٔ «آزمایش آسپه ۱۹۸۲ چه بود؟»',
		'is-classical-physics-wrong' => 'تصویر شاخص مقالهٔ «آیا فیزیک کلاسیک اشتباه بود؟ نه، محدود بود»',
		'quantum-interpretation-debate' => 'تصویر شاخص مقالهٔ «آیا فیزیک‌دانان بر سر معنای اندازه‌گیری توافق دارند؟»',
		'stimulated-emission' => 'تصویر شاخص مقالهٔ «گسیل تحریکی چیست؟»',
		'genetic-mutation' => 'تصویر شاخص مقالهٔ «آیا جهش ژنتیکی کوانتومی است؟»',
		'quantum-analogy-exercise-boundary' => 'تصویر شاخص مقالهٔ «تمرین ذهنی: خودتان یک تمثیل بسازید و مرزش را پیدا کنید»',
		'quantum-thermodynamics' => 'تصویر شاخص مقالهٔ «ترمودینامیک کوانتومی؛ موتوری به اندازهٔ یک اتم»',
		'quantum-understanding-achievement' => 'تصویر شاخص مقالهٔ «چرا نفهمیدن درست کوانتوم، خودش یک دستاورد است؟»',
		'enzyme-quantum-tunneling' => 'تصویر شاخص مقالهٔ «آنزیم‌ها؛ عبور از دیوار به‌جای پریدن»',
		'solar-cells-photoelectric' => 'تصویر شاخص مقالهٔ «پنل خورشیدی و اثر فوتوالکتریک؛ تبدیل نور به جریان زندگی»',
		'attosecond-nobel-2023' => 'تصویر شاخص مقالهٔ «نوبل فیزیک ۲۰۲۳؛ عکاسی از حرکت الکترون»',
		'schrodinger-life-equation' => 'تصویر شاخص مقالهٔ «شرودینگر: زندگی، معادله و گربه‌ای که هرگز نداشت»',
		'quantum-career-future-learn' => 'تصویر شاخص مقالهٔ «آینده شغلی: آیا باید فیزیک کوانتوم یاد بگیریم؟»',
		'quantum-classical-boundary' => 'تصویر شاخص مقالهٔ «چرا کوانتوم را در زندگی روزمره حس نمی‌کنیم؟»',
		'time-crystal' => 'تصویر شاخص مقالهٔ «کریستال زمان چیست؟ ماده‌ای که در زمان تکرار می‌شود»',
		'transistor-quantum' => 'تصویر شاخص مقالهٔ «ترانزیستور؛ کوانتوم در جیب شما»',
		'casimir-effect' => 'تصویر شاخص مقالهٔ «اثر کازیمیر؛ نیرویی از خلأ»',
		'mind-quantum-reality' => 'تصویر شاخص مقالهٔ «آیا با فکر کردن می‌توان واقعیت کوانتومی را تغییر داد؟»',
		'quantum-fivefold-mental-map' => 'تصویر شاخص مقالهٔ «نقشهٔ ذهنی پنج‌گانه برای فهم درست کوانتوم»',
		'quantum-fluctuations-cosmos' => 'تصویر شاخص مقالهٔ «افت و خیز کوانتومی؛ چطور کهکشان‌ها متولد شدند؟»',
		'does-quantum-prove-god' => 'تصویر شاخص مقالهٔ «آیا کوانتوم ثابت می‌کند خدا وجود دارد یا ندارد؟»',
		'ibm-condor-processor' => 'تصویر شاخص مقالهٔ «پردازندهٔ IBM Condor؛ چرا هزار کیوبیت کافی نیست»',
		'forgotten-women-quantum' => 'تصویر شاخص مقالهٔ «زنان فراموش‌شدهٔ فیزیک کوانتوم»',
		'planck-constant' => 'تصویر شاخص مقالهٔ «پلانک و بحران تابش جسم سیاه»',
		'quantum-spin-liquid' => 'تصویر شاخص مقالهٔ «مایع اسپینی کوانتومی؛ ماده‌ای که هرگز آرام نمی‌گیرد»',
		'coin-vs-dice-quantum-uncertainty' => 'تصویر شاخص مقالهٔ «تمثیل تاس در مقابل تمثیل سکه: کدام برای عدم‌قطعیت بهتر است؟»',
		'bell-experiments' => 'تصویر شاخص مقالهٔ «آزمایش‌های بل: چگونه درهم‌تنیدگی اثبات شد!»',
		'nuclear-spin' => 'تصویر شاخص مقالهٔ «اسپین هسته‌ای چیست؟»',
		'quantum-zeno-effect' => 'تصویر شاخص مقالهٔ «اثر زنون کوانتومی»',
		'atomic-clock-gps' => 'تصویر شاخص مقالهٔ «ساعت اتمی و جی‌پی‌اس»',
		'antimatter' => 'تصویر شاخص مقالهٔ «پادماده چیست؟ — دیراک و پیش‌بینی پادماده»',
		'mri-quantum' => 'تصویر شاخص مقالهٔ «ام‌آرآی چگونه کار می‌کند؟ ریشهٔ کوانتومی آن»',
		'entanglement-quantum-computers' => 'تصویر شاخص مقالهٔ «درهم‌تنیدگی در کامپیوترهای کوانتومی امروزی»',
		'einstein-bohr-debate' => 'تصویر شاخص مقالهٔ «نبرد اینشتین و بور بر سر معنای کوانتوم»',
		'pet-scan-antimatter' => 'تصویر شاخص مقالهٔ «پادماده در پزشکی؛ اسکن پت چطور کار می‌کند؟»',
		'alpha-decay' => 'تصویر شاخص مقالهٔ «واپاشی آلفا چیست؟»',
		'bose-einstein-condensate' => 'تصویر شاخص مقالهٔ «چگالش بوز-اینشتین چیست؟»',
		'entanglement-myths' => 'تصویر شاخص مقالهٔ «آیا درهم‌تنیدگی یعنی اطلاعات سریع‌تر از نور منتقل می‌شود؟»',
		'black-hole-information-paradox' => 'تصویر شاخص مقالهٔ «پارادوکس اطلاعات سیاه‌چاله؛ معمای هاوکینگ»',
		'feynman-quantum-explainer' => 'تصویر شاخص مقالهٔ «فاینمن: نابغه‌ای که کوانتوم را ساده توضیح می‌داد»',
		'quantum-healing-debunked' => 'تصویر شاخص مقالهٔ «شفای کوانتومی؛ چرا این ادعا شبه‌علم است؟»',
		'physicists-on-quantum-weirdness' => 'تصویر شاخص مقالهٔ «ده دیدگاه فیزیکدانان بزرگ دربارهٔ عجایب کوانتوم»',
		'pending-photosynthesis' => 'تصویر شاخص مقالهٔ «فتوسنتز؛ کارآمدترین ماشین جهان و رد پای کوانتوم»',
		'einstein-photoelectric-effect' => 'تصویر شاخص مقالهٔ «اینشتین و اثر فوتوالکتریک»',
		'human-teleportation' => 'تصویر شاخص مقالهٔ «چرا تله‌پورت انسان از نظر علمی غیرممکن است؟»',
		'post-quantum-cryptography' => 'تصویر شاخص مقالهٔ «رمزنگاری پساکوانتومی؛ قفل‌های تازهٔ اینترنت»',
		'everything-is-energy-claim' => 'تصویر شاخص مقالهٔ «همه‌چیز انرژی است — بررسی یک ادعا»',
		'is-many-worlds-real' => 'تصویر شاخص مقالهٔ «آیا چندجهانی واقعی است؟»',
	);
}

add_action( 'admin_menu', 'qp_feat2_menu' );
function qp_feat2_menu() {
	add_management_page(
		'ایمپورتر تصاویر سری ۲',
		'ایمپورتر تصاویر ۲',
		'manage_options',
		'qp-feat-import-2',
		'qp_feat2_page'
	);
}

function qp_feat2_images() {
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

function qp_feat2_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}

	$files  = qp_feat2_images();
	$alts   = qp_feat2_alts();
	$total  = count( $files );
	$batch  = 10;
	$offset = isset( $_GET['qp_offset'] ) ? max( 0, intval( $_GET['qp_offset'] ) ) : 0;
	$run    = isset( $_GET['qp_run'] ) && '1' === $_GET['qp_run'];

	$log = array();

	if ( $run && $offset < $total ) {
		check_admin_referer( 'qp_feat2_run' );
		require_once ABSPATH . 'wp-admin/includes/media.php';
		require_once ABSPATH . 'wp-admin/includes/file.php';
		require_once ABSPATH . 'wp-admin/includes/image.php';

		foreach ( array_slice( $files, $offset, $batch ) as $path ) {
			$slug = sanitize_title( basename( $path, '.webp' ) );
			$post = get_page_by_path( $slug, OBJECT, 'quantum_article' );

			if ( ! $post instanceof WP_Post ) {
				$log[] = '⏭ ' . $slug . ' — مقاله پیدا نشد';
				continue;
			}

			$data = @file_get_contents( $path );
			if ( false === $data ) {
				$log[] = '❌ ' . $slug . ' — خواندن فایل ناممکن بود';
				continue;
			}

			$bits = wp_upload_bits( basename( $path ), null, $data );
			if ( ! empty( $bits['error'] ) ) {
				$log[] = '❌ ' . $slug . ' — خطای آپلود: ' . $bits['error'];
				continue;
			}

			$alt    = isset( $alts[ $slug ] ) ? $alts[ $slug ] : '';
			$att_id = wp_insert_attachment(
				array(
					'post_mime_type' => 'image/webp',
					'post_title'     => $alt ? $alt : $post->post_title,
					'post_status'    => 'inherit',
				),
				$bits['file'],
				$post->ID
			);
			if ( ! $att_id || is_wp_error( $att_id ) ) {
				$log[] = '❌ ' . $slug . ' — خطای درج در مدیا';
				continue;
			}

			wp_update_attachment_metadata( $att_id, wp_generate_attachment_metadata( $att_id, $bits['file'] ) );
			if ( $alt ) {
				update_post_meta( $att_id, '_wp_attachment_image_alt', $alt );
			}

			$old = get_post_thumbnail_id( $post->ID );
			if ( $old && (int) $old !== (int) $att_id ) {
				wp_delete_attachment( $old, true );
			}
			set_post_thumbnail( $post->ID, $att_id );

			$log[] = '✅ ' . $slug . ' (#' . $post->ID . ')';
		}
	}

	$next     = $offset + $batch;
	$finished = $run && $next >= $total;

	echo '<div class="wrap"><h1>ایمپورتر تصاویر سری ۲</h1>';
	echo '<p>تعداد تصاویر داخل افزونه: <b>' . esc_html( number_format_i18n( $total ) ) . '</b></p>';

	if ( ! $run ) {
		echo '<p>با زدن دکمه، برای هر تصویر (نام فایل = اسلاگ مقاله) تصویر شاخص جایگزین، <b>آلت ثبت</b> و تصویر قبلی <b>حذف</b> می‌شود.</p>';
		$url = wp_nonce_url(
			add_query_arg( array( 'page' => 'qp-feat-import-2', 'qp_run' => '1', 'qp_offset' => 0 ), admin_url( 'tools.php' ) ),
			'qp_feat2_run'
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
				add_query_arg( array( 'page' => 'qp-feat-import-2', 'qp_run' => '1', 'qp_offset' => $next ), admin_url( 'tools.php' ) ),
				'qp_feat2_run'
			);
			echo '<p>در حال ادامه… <a href="' . esc_url( $url ) . '">ادامه دستی</a></p>';
			echo '<script>setTimeout(function(){window.location.href=' . wp_json_encode( $url ) . ';},900);</script>';
		}
	}
	echo '</div>';
}
