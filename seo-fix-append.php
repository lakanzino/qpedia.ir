
/* ══════════════════════════════════════════════════════════════
   ۲۲. فیکس‌های سئوی فنی (۱۴۰۵/۰۶): canonical سراسری + sitemap + تاکسونومی
   ══════════════════════════════════════════════════════════════ */

/* canonical یکتا برای همهٔ صفحات — تک‌مقاله در بخش ۱۶ پوشش دارد؛ 404 و جست‌وجو canonical نمی‌گیرند */
remove_action( 'wp_head', 'rel_canonical' );
function qpedia_universal_canonical() {
	if ( is_404() || is_search() || is_singular( 'quantum_article' ) ) {
		return;
	}

	$url = '';
	if ( is_front_page() ) {
		$url = home_url( '/' );
	} elseif ( is_home() ) {
		$posts_page = get_option( 'page_for_posts' );
		$url        = $posts_page ? get_permalink( $posts_page ) : home_url( '/' );
	} elseif ( is_post_type_archive() ) {
		$archive_object = get_queried_object();
		$url            = $archive_object ? get_post_type_archive_link( $archive_object->name ) : '';
	} elseif ( is_tax() || is_category() || is_tag() ) {
		$url = get_term_link( get_queried_object() );
	} elseif ( is_singular() ) {
		$url = get_permalink();
	} elseif ( is_author() ) {
		$url = get_author_posts_url( get_queried_object_id() );
	} elseif ( is_date() ) {
		$year  = get_query_var( 'year' );
		$month = get_query_var( 'monthnum' );
		$day   = get_query_var( 'day' );
		if ( $day ) {
			$url = get_day_link( $year, $month, $day );
		} elseif ( $month ) {
			$url = get_month_link( $year, $month );
		} else {
			$url = get_year_link( $year );
		}
	}

	if ( empty( $url ) || is_wp_error( $url ) ) {
		return;
	}

	if ( is_paged() && ( is_archive() || is_home() ) ) {
		$paged_url = get_pagenum_link( get_query_var( 'paged' ) );
		if ( $paged_url && ! is_wp_error( $paged_url ) ) {
			$url = $paged_url;
		}
	}

	echo '<link rel="canonical" href="' . esc_url( $url ) . '">' . "\n";
}
add_action( 'wp_head', 'qpedia_universal_canonical', 1 );

/* ریدایرکت مسیرهای رایج نقشهٔ سایت به نقشهٔ اصلی وردپرس */
function qpedia_redirect_common_sitemap_paths() {
	if ( is_admin() || ! is_404() ) {
		return;
	}

	$request_path = wp_parse_url( wp_unslash( $_SERVER['REQUEST_URI'] ?? '' ), PHP_URL_PATH );
	$request_path = is_string( $request_path ) ? trim( $request_path, '/' ) : '';

	if ( 'sitemap.xml' === $request_path || 'sitemap_index.xml' === $request_path ) {
		wp_safe_redirect( home_url( '/wp-sitemap.xml' ), 301 );
		exit;
	}
}
add_action( 'template_redirect', 'qpedia_redirect_common_sitemap_paths', 1 );

/* معرفی نقشهٔ سایت در robots.txt */
function qpedia_robots_sitemap_line( $output ) {
	$output .= 'Sitemap: ' . esc_url( home_url( '/wp-sitemap.xml' ) ) . "\n";
	return $output;
}
add_filter( 'robots_txt', 'qpedia_robots_sitemap_line' );

/* پنهان نگه‌داشتن تاکسونومی‌های قدیمی/خالی از نقشهٔ سایت و رویهٔ سایت */
function qpedia_hide_retired_taxonomies() {
	global $wp_taxonomies;
	foreach ( array( 'scientist_field', 'article_domain' ) as $taxonomy ) {
		if ( isset( $wp_taxonomies[ $taxonomy ] ) ) {
			$wp_taxonomies[ $taxonomy ]->public             = false;
			$wp_taxonomies[ $taxonomy ]->publicly_queryable = false;
		}
	}
}
add_action( 'init', 'qpedia_hide_retired_taxonomies', 99 );
