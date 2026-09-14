<?php
/**
 * Template Name: صفحه اصلی
 * Description: صفحه اصلی با هاب دسته‌ها و جدیدترین مقالات
 *
 * @package Quantum_Pedia_Child
 * @since   1.0.2
 */
get_header();
?>
<main id="primary" class="site-main">
<div class="container">

<?php
// ── هاب دسته‌ها ──
$parents = get_terms( array(
    'taxonomy'   => 'quantum_category',
    'hide_empty' => true,
    'parent'     => 0,
    'orderby'    => 'count',
    'order'      => 'DESC',
) );

if ( ! is_wp_error( $parents ) && ! empty( $parents ) ) :
    $count = wp_count_posts( 'quantum_article' );
    $n     = isset( $count->publish ) ? (int) $count->publish : 0;
?>
<section class="qp-hub">
    <h1 class="qp-hub__t">دانشنامهٔ کوانتوم</h1>
    <p class="qp-hub__s"><?php echo esc_html( $n ); ?> مقاله در <?php echo esc_html( count( $parents ) ); ?> موضوع</p>
    <div class="qp-hub__g">
        <?php foreach ( $parents as $p ) :
            $kids = get_terms( array(
                'taxonomy'   => 'quantum_category',
                'hide_empty' => true,
                'parent'     => $p->term_id,
            ) );
        ?>
        <a class="qp-hub__c" href="<?php echo esc_url( get_term_link( $p ) ); ?>">
            <span class="qp-hub__b"><?php echo (int) $p->count; ?></span>
            <span class="qp-hub__n"><?php echo esc_html( $p->name ); ?></span>
            <?php if ( ! is_wp_error( $kids ) && ! empty( $kids ) ) : ?>
            <span class="qp-hub__k"><?php echo esc_html( implode( ' · ', wp_list_pluck( $kids, 'name' ) ) ); ?></span>
            <?php endif; ?>
        </a>
        <?php endforeach; ?>
    </div>
</section>
<?php endif; ?>

<?php
// ── جدیدترین مقالات ──
$latest = new WP_Query( array(
    'post_type'      => 'quantum_article',
    'posts_per_page' => 12,
    'orderby'        => 'date',
    'order'          => 'DESC',
    'no_found_rows'  => true,
) );

if ( $latest->have_posts() ) :
?>
<h2 class="qp-recent">تازه‌ترین‌ها</h2>
<?php while ( $latest->have_posts() ) : $latest->the_post(); ?>
    <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
        <h3 class="entry-title">
            <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
        </h3>
    </article>
<?php endwhile; wp_reset_postdata(); ?>
<?php endif; ?>

</div>
</main>

<?php
get_footer();