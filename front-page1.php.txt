<?php
/**
 * Front page template — minimal landing (v1.3.1).
 *
 * صفحهٔ نخست مینیمال با دو لینک اصلی: برگهٔ شروع + دانشمندان.
 * بخش اسلایدر دانشمندان حذف شده؛ دانشمندان فقط از لینک اصلی در دسترس‌اند.
 * این فایل مستقل از برگهٔ سفارشی عمل می‌کند و وردپرس مستقیماً همین فایل
 * را برای صفحهٔ اول به‌کار می‌گیرد.
 *
 * @package Quantum_Pedia_Child
 */

defined( 'ABSPATH' ) || exit;

get_header();

$article_counts = wp_count_posts( 'quantum_article' );
$article_total  = isset( $article_counts->publish ) ? (int) $article_counts->publish : 0;

$parent_categories = get_terms(
	array(
		'taxonomy'   => 'quantum_category',
		'hide_empty' => true,
		'parent'     => 0,
		'orderby'    => 'count',
		'order'      => 'DESC',
	)
);
$parent_total = ( ! is_wp_error( $parent_categories ) && ! empty( $parent_categories ) ) ? count( $parent_categories ) : 0;

$scientist_counts = wp_count_posts( 'quantum_scientist' );
$scientist_total  = isset( $scientist_counts->publish ) ? (int) $scientist_counts->publish : 0;

$all_categories = get_terms(
	array(
		'taxonomy'   => 'quantum_category',
		'hide_empty' => true,
	)
);
$sub_total = 0;
if ( ! is_wp_error( $all_categories ) && ! empty( $all_categories ) ) {
	foreach ( $all_categories as $term ) {
		if ( ! empty( $term->parent ) ) {
			$sub_total++;
		}
	}
}

$cat_descriptions = array(
	'fundamentals'        => 'سنگ‌بنای مکانیک کوانتومی؛ از مفاهیم پایه تا ذرات بنیادی.',
	'technology'          => 'از لیزر و GPS تا رایانش و کاربردهای واقعی کوانتوم.',
	'history-experiments' => 'روایت تاریخی نظریه و آزمایش‌هایی که فهم ما را تغییر دادند.',
	'phenomena'           => 'درهم‌تنیدگی، تونل‌زنی و پدیده‌هایی که شهود کلاسیک را می‌شکنند.',
	'mathematics'         => 'زبان ریاضی کوانتوم؛ فضای هیلبرت، عملگرها و معادلات.',
	'interpretations'     => 'خوانش‌های فلسفی و تفسیری از معنای نظریهٔ کوانتوم.',
	'pseudoscience'       => 'مرزبندی علم دقیق با سوءاستفاده‌های بازاری و شبه‌علم.',
);

$cat_icons = array(
	'fundamentals'        => 'مبانی',
	'technology'          => 'فناوری',
	'history-experiments' => 'تاریخ',
	'phenomena'           => 'پدیده',
	'mathematics'         => 'ریاضی',
	'interpretations'     => 'تفسیر',
	'pseudoscience'       => 'نقد',
);

// دو لینک اصلی صفحهٔ نخست.
$start_url = function_exists( 'qpedia_child_find_page_url' )
	? qpedia_child_find_page_url( array( 'start', 'شروع', 'از-کجا-شروع-کنیم' ), '/start/' )
	: home_url( '/start/' );
$scientists_url = home_url( '/scientists/' );

$latest_articles = new WP_Query(
	array(
		'post_type'              => 'quantum_article',
		'posts_per_page'         => 6,
		'post_status'            => 'publish',
		'orderby'                => 'date',
		'order'                  => 'DESC',
		'ignore_sticky_posts'    => true,
		'no_found_rows'          => true,
		'update_post_meta_cache' => false,
	)
);
?>
<main id="primary" class="site-main">
	<div class="container qp-front">
		<section class="qp-front-hero">
			<div class="qp-front-hero__badge">دانشنامهٔ فارسی فیزیک کوانتوم</div>
			<h1 class="qp-front-hero__title">کوانتوم را از پایه، دقیق و روان یاد بگیرید</h1>
			<p class="qp-front-hero__desc">از مبانی نظری تا فناوری‌های واقعی — با مقاله‌های کوتاه، دسته‌بندی روشن و مسیر مطالعهٔ قابل‌فهم.</p>

			<div class="qp-front-hero__stats" aria-label="آمار دانشنامه">
				<div class="qp-front-stat">
					<span class="qp-front-stat__num"><?php echo esc_html( number_format_i18n( $article_total ) ); ?></span>
					<span class="qp-front-stat__label">مقاله</span>
				</div>
				<div class="qp-front-stat">
					<span class="qp-front-stat__num"><?php echo esc_html( number_format_i18n( $parent_total ) ); ?></span>
					<span class="qp-front-stat__label">دستهٔ اصلی</span>
				</div>
				<div class="qp-front-stat">
					<span class="qp-front-stat__num"><?php echo esc_html( number_format_i18n( $sub_total ) ); ?></span>
					<span class="qp-front-stat__label">زیردسته</span>
				</div>
				<div class="qp-front-stat">
					<span class="qp-front-stat__num"><?php echo esc_html( number_format_i18n( $scientist_total ) ); ?></span>
					<span class="qp-front-stat__label">دانشمند</span>
				</div>
			</div>

			<div class="qp-front-search">
				<?php get_search_form(); ?>
			</div>

		</section>

		<section class="qp-front-section qp-front-section--cta" aria-label="دو مسیر اصلی">
			<div class="qp-front-cta-grid">
				<a class="qp-front-cta-card qp-front-cta-card--start" href="<?php echo esc_url( $start_url ); ?>">
					<span class="qp-front-cta-card__icon" aria-hidden="true">01</span>
					<span class="qp-front-cta-card__body">
						<span class="qp-front-cta-card__title"><strong>از کجا شروع کنیم؟</strong></span>
						<span class="qp-front-cta-card__desc">نقشهٔ راه ورود به سایت: ۶۰ ثانیه، ۵ دقیقه یا مسیر کامل — انتخاب با توست.</span>
					</span>
					<span class="qp-front-cta-card__arrow" aria-hidden="true">←</span>
				</a>
				<a class="qp-front-cta-card qp-front-cta-card--scientists" href="<?php echo esc_url( $scientists_url ); ?>">
					<span class="qp-front-cta-card__icon" aria-hidden="true">02</span>
					<span class="qp-front-cta-card__body">
						<span class="qp-front-cta-card__title"><strong>بیوگرافی دانشمندان</strong></span>
						<span class="qp-front-cta-card__desc">با چهره‌هایی آشنا شو که این علم را ساختند: از پلانک و اینشتین تا بل و فاینمن.</span>
					</span>
					<span class="qp-front-cta-card__arrow" aria-hidden="true">←</span>
				</a>
			</div>
		</section>

		<section id="qp-front-cats" class="qp-front-section qp-front-section--cats">
			<div class="qp-front-section__head">
				<div>
					<div class="qp-front-section__eyebrow">ساختار دانشنامه</div>
					<h2 class="qp-front-section__title">دسته‌بندی موضوعات</h2>
					<p class="qp-front-section__desc">هفت مسیر اصلی برای خواندن موضوعی مقاله‌ها.</p>
				</div>
			</div>

			<?php if ( ! is_wp_error( $parent_categories ) && ! empty( $parent_categories ) ) : ?>
				<div class="qp-front-cats">
					<?php foreach ( $parent_categories as $category ) : ?>
						<?php
						$children = get_terms(
							array(
								'taxonomy'   => 'quantum_category',
								'hide_empty' => true,
								'parent'     => $category->term_id,
							)
						);
						$slug      = isset( $category->slug ) ? $category->slug : '';
						$cat_desc  = isset( $cat_descriptions[ $slug ] ) ? $cat_descriptions[ $slug ] : '';
						$cat_icon  = isset( $cat_icons[ $slug ] ) ? $cat_icons[ $slug ] : 'موضوع';
						?>
						<a class="qp-front-cat" href="<?php echo esc_url( get_term_link( $category ) ); ?>">
							<div class="qp-front-cat__top">
								<span class="qp-front-cat__icon"><?php echo esc_html( $cat_icon ); ?></span>
								<span class="qp-front-cat__count"><?php echo esc_html( number_format_i18n( (int) $category->count ) ); ?> مقاله</span>
							</div>
							<h3 class="qp-front-cat__title"><?php echo esc_html( $category->name ); ?></h3>
							<?php if ( $cat_desc ) : ?>
								<p class="qp-front-cat__desc"><?php echo esc_html( $cat_desc ); ?></p>
							<?php endif; ?>

							<?php if ( ! is_wp_error( $children ) && ! empty( $children ) ) : ?>
								<div class="qp-front-cat__subs">
									<?php foreach ( $children as $child ) : ?>
										<span class="qp-front-cat__sub"><?php echo esc_html( $child->name ); ?></span>
									<?php endforeach; ?>
								</div>
							<?php endif; ?>
						</a>
					<?php endforeach; ?>
				</div>
			<?php endif; ?>
		</section>

		<section class="qp-front-section qp-front-section--articles">
			<div class="qp-front-section__head">
				<div>
					<div class="qp-front-section__eyebrow">تازه‌ترین‌ها</div>
					<h2 class="qp-front-section__title">آخرین مقاله‌ها</h2>
				</div>
				<a class="qp-front-section__link" href="#qp-front-cats">مرور دسته‌ها</a>
			</div>

			<?php if ( $latest_articles->have_posts() ) : ?>
				<div class="qp-front-articles">
					<?php while ( $latest_articles->have_posts() ) : $latest_articles->the_post(); ?>
						<?php
						$terms      = get_the_terms( get_the_ID(), 'quantum_category' );
						$term_label = '';
						if ( ! is_wp_error( $terms ) && ! empty( $terms ) ) {
							$term_label = $terms[0]->name;
						}
						?>
						<a class="qp-front-article" href="<?php the_permalink(); ?>">
							<div class="qp-front-article__meta">
								<?php if ( $term_label ) : ?>
									<span class="qp-front-article__term"><?php echo esc_html( $term_label ); ?></span>
								<?php endif; ?>
								<time datetime="<?php echo esc_attr( get_the_date( 'c' ) ); ?>"><?php echo esc_html( get_the_date( 'j F Y' ) ); ?></time>
							</div>
							<h3 class="qp-front-article__title"><?php the_title(); ?></h3>
							<p class="qp-front-article__excerpt"><?php echo esc_html( get_the_excerpt() ); ?></p>
						</a>
					<?php endwhile; ?>
				</div>
				<?php wp_reset_postdata(); ?>
			<?php endif; ?>
		</section>
	</div>
</main>
<?php
get_footer();
