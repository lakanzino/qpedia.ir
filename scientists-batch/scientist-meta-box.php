<?php
/**
 * جعبهٔ ورود اطلاعات دانشمندان (متاباکس) + ثبت استایل گرید.
 *
 * نصب: این کد را در functions.php قالب فرزند قرار بده (یا به‌صورت include).
 * پس از آن، در ویرایش هر مدخلِ دانشمند، باکس «شناسنامهٔ سریع دانشمند» ظاهر می‌شود
 * و این فیلدها گریدِ بالای صفحه را می‌سازند.
 *
 * @package Quantum_Pedia_Child
 */

defined( 'ABSPATH' ) || exit;

/**
 * ثبت استایل مدخل دانشمندان (قلاب، گرید، نقل‌قول، گاه‌شمار، آکاردئون).
 */
function qpedia_enqueue_scientist_assets() {
	if ( is_singular( 'quantum_scientist' ) ) {
		wp_enqueue_style(
			'qpedia-scientist',
			get_stylesheet_directory_uri() . '/qpedia-scientist.css',
			array(),
			'1.0.0'
		);
	}
}
add_action( 'wp_enqueue_scripts', 'qpedia_enqueue_scientist_assets' );

/**
 * ثبت متاباکس شناسنامهٔ سریع.
 */
function qpedia_scientist_meta_box_register() {
	add_meta_box(
		'qpedia_scientist_identity',
		'شناسنامهٔ سریع دانشمند (گرید)',
		'qpedia_scientist_meta_box_render',
		'quantum_scientist',
		'normal',
		'high'
	);
}
add_action( 'add_meta_boxes', 'qpedia_scientist_meta_box_register' );

/**
 * فهرست فیلدهای گرید: برچسب => کلید متا.
 */
function qpedia_scientist_identity_fields() {
	return array(
		'_scientist_en_name'     => 'نام لاتین (زیر عنوان)',
		'_scientist_fullname'    => 'نام کامل',
		'_scientist_born_died'   => 'زادروز و درگذشت',
		'_scientist_birthplace'  => 'زادگاه و ملیت',
		'_scientist_institutions' => 'پایگاه‌های دانشگاهی',
		'_scientist_achievement' => 'دستاورد کلیدی در کوانتوم',
		'_scientist_nobel'       => 'جایزهٔ نوبل',
		'_scientist_concepts'    => 'مفاهیم و فرمول‌های جاودانه',
		'_scientist_family'      => 'خانواده',
	);
}

/**
 * رندر متاباکس.
 *
 * @param WP_Post $post مدخل جاری.
 */
function qpedia_scientist_meta_box_render( $post ) {
	wp_nonce_field( 'qpedia_scientist_identity_save', 'qpedia_scientist_identity_nonce' );

	echo '<style>.qp-meta-row{margin:12px 0}.qp-meta-row label{display:block;font-weight:600;margin-bottom:4px}.qp-meta-row input,.qp-meta-row textarea{width:100%;max-width:640px}</style>';

	foreach ( qpedia_scientist_identity_fields() as $key => $label ) {
		$value = (string) get_post_meta( $post->ID, $key, true );
		$is_long = in_array( $key, array( '_scientist_institutions', '_scientist_achievement', '_scientist_concepts', '_scientist_family' ), true );
		?>
		<div class="qp-meta-row">
			<label for="<?php echo esc_attr( $key ); ?>"><?php echo esc_html( $label ); ?></label>
			<?php if ( $is_long ) : ?>
				<textarea id="<?php echo esc_attr( $key ); ?>" name="<?php echo esc_attr( $key ); ?>" rows="2"><?php echo esc_textarea( $value ); ?></textarea>
			<?php else : ?>
				<input type="text" id="<?php echo esc_attr( $key ); ?>" name="<?php echo esc_attr( $key ); ?>" value="<?php echo esc_attr( $value ); ?>" />
			<?php endif; ?>
		</div>
		<?php
	}
}

/**
 * ذخیرهٔ متاباکس.
 *
 * @param int $post_id شناسهٔ مدخل.
 */
function qpedia_scientist_meta_box_save( $post_id ) {
	if ( ! isset( $_POST['qpedia_scientist_identity_nonce'] )
		|| ! wp_verify_nonce( sanitize_key( $_POST['qpedia_scientist_identity_nonce'] ), 'qpedia_scientist_identity_save' ) ) {
		return;
	}
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
		return;
	}
	if ( ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}

	foreach ( qpedia_scientist_identity_fields() as $key => $label ) {
		if ( isset( $_POST[ $key ] ) ) {
			$value = in_array( $key, array( '_scientist_institutions', '_scientist_achievement', '_scientist_concepts', '_scientist_family' ), true )
				? sanitize_textarea_field( wp_unslash( $_POST[ $key ] ) )
				: sanitize_text_field( wp_unslash( $_POST[ $key ] ) );
			update_post_meta( $post_id, $key, $value );
		}
	}
}
add_action( 'save_post_quantum_scientist', 'qpedia_scientist_meta_box_save' );
