<?php
/**
 * Plugin Name:       QPedia — قالب دانشمندان کوانتوم
 * Plugin URI:        https://qpedia.ir/
 * Description:       گریدِ «شناسنامهٔ سریع»، قلاب، نقل‌قول، گاه‌شمار و پرسش‌های آکاردئونی برای مدخل‌های دانشمندان کوانتوم (نوع نوشتهٔ quantum_scientist). قالب تک‌مدخلی و باکسِ ورود اطلاعات را بدونِ دست‌زدن به فایل‌های پوسته فراهم می‌کند.
 * Version:           1.0.0
 * Requires at least: 5.6
 * Requires PHP:      7.2
 * Author:            QPedia
 * License:           GPL-2.0-or-later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       qpedia
 */

defined( 'ABSPATH' ) || exit;

if ( ! class_exists( 'QPedia_Scientist_Template' ) ) {

	/**
	 * کلاس اصلی افزونهٔ قالب دانشمندان.
	 */
	final class QPedia_Scientist_Template {

		const VERSION = '1.0.0';

		/**
		 * @var QPedia_Scientist_Template|null
		 */
		private static $instance = null;

		/**
		 * نمونهٔ یکتا.
		 *
		 * @return QPedia_Scientist_Template
		 */
		public static function instance() {
			if ( null === self::$instance ) {
				self::$instance = new self();
			}
			return self::$instance;
		}

		/**
		 * سازنده — ثبت قلاب‌ها.
		 */
		private function __construct() {
			add_action( 'wp_enqueue_scripts', array( $this, 'enqueue_assets' ) );
			add_filter( 'template_include', array( $this, 'template_include' ), 99 );
			add_action( 'add_meta_boxes', array( $this, 'register_meta_box' ) );
			add_action( 'save_post_quantum_scientist', array( $this, 'save_meta_box' ) );
		}

		/**
		 * فیلدهای گرید: کلیدِ متا => برچسب فارسی.
		 *
		 * @return array<string,string>
		 */
		public static function identity_fields() {
			return array(
				'_scientist_en_name'      => 'نام لاتین (زیر عنوان)',
				'_scientist_fullname'     => 'نام کامل',
				'_scientist_born_died'    => 'زادروز و درگذشت',
				'_scientist_birthplace'   => 'زادگاه و ملیت',
				'_scientist_institutions' => 'پایگاه‌های دانشگاهی',
				'_scientist_achievement'  => 'دستاورد کلیدی در کوانتوم',
				'_scientist_nobel'        => 'جایزهٔ نوبل',
				'_scientist_concepts'     => 'مفاهیم و فرمول‌های جاودانه',
				'_scientist_family'       => 'خانواده',
			);
		}

		/**
		 * بارگذاری استایل فقط در صفحهٔ تک‌دانشمند.
		 */
		public function enqueue_assets() {
			if ( ! is_singular( 'quantum_scientist' ) ) {
				return;
			}

			wp_enqueue_style(
				'qpedia-scientist',
				plugin_dir_url( __FILE__ ) . 'qpedia-scientist.css',
				array(),
				self::VERSION
			);
		}

		/**
		 * جایگزینی قالب تک‌مدخلی دانشمند با نسخهٔ افزونه.
		 *
		 * @param string $template مسیر قالبِ انتخاب‌شده توسط وردپرس/پوسته.
		 * @return string
		 */
		public function template_include( $template ) {
			if ( ! is_singular( 'quantum_scientist' ) ) {
				return $template;
			}

			// در صورت نیاز می‌توان با این فیلتر قالبِ افزونه را غیرفعال کرد.
			if ( ! apply_filters( 'qpedia_sci_use_plugin_template', true ) ) {
				return $template;
			}

			$plugin_template = plugin_dir_path( __FILE__ ) . 'templates/single-quantum_scientist.php';

			return file_exists( $plugin_template ) ? $plugin_template : $template;
		}

		/**
		 * ثبت متاباکسِ «شناسنامهٔ سریع».
		 */
		public function register_meta_box() {
			add_meta_box(
				'qpedia_scientist_identity',
				'شناسنامهٔ سریع دانشمند (گرید)',
				array( $this, 'render_meta_box' ),
				'quantum_scientist',
				'normal',
				'high'
			);
		}

		/**
		 * رندر متاباکس.
		 *
		 * @param WP_Post $post مدخل جاری.
		 */
		public function render_meta_box( $post ) {
			wp_nonce_field( 'qpedia_scientist_identity_save', 'qpedia_scientist_identity_nonce' );

			echo '<style>.qp-meta-row{margin:12px 0}.qp-meta-row label{display:block;font-weight:600;margin-bottom:4px}.qp-meta-row input,.qp-meta-row textarea{width:100%;max-width:640px}</style>';

			foreach ( self::identity_fields() as $key => $label ) {
				$value   = (string) get_post_meta( $post->ID, $key, true );
				$is_long = in_array( $key, array( '_scientist_institutions', '_scientist_achievement', '_scientist_concepts', '_scientist_family' ), true );

				echo '<div class="qp-meta-row">';
				echo '<label for="' . esc_attr( $key ) . '">' . esc_html( $label ) . '</label>';

				if ( $is_long ) {
					echo '<textarea id="' . esc_attr( $key ) . '" name="' . esc_attr( $key ) . '" rows="2">' . esc_textarea( $value ) . '</textarea>';
				} else {
					echo '<input type="text" id="' . esc_attr( $key ) . '" name="' . esc_attr( $key ) . '" value="' . esc_attr( $value ) . '" />';
				}

				echo '</div>';
			}
		}

		/**
		 * ذخیرهٔ متاباکس.
		 *
		 * @param int $post_id شناسهٔ مدخل.
		 */
		public function save_meta_box( $post_id ) {
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

			foreach ( self::identity_fields() as $key => $label ) {
				if ( ! isset( $_POST[ $key ] ) ) {
					continue;
				}

				$value = in_array( $key, array( '_scientist_institutions', '_scientist_achievement', '_scientist_concepts', '_scientist_family' ), true )
					? sanitize_textarea_field( wp_unslash( $_POST[ $key ] ) )
					: sanitize_text_field( wp_unslash( $_POST[ $key ] ) );

				update_post_meta( $post_id, $key, $value );
			}
		}

		/**
		 * ساخت HTML گرید شناسنامهٔ سریع.
		 *
		 * @param int $post_id شناسهٔ مدخل.
		 * @return string
		 */
		public static function identity_grid( $post_id ) {
			$cells = '';

			foreach ( self::identity_fields() as $key => $label ) {
				if ( '_scientist_en_name' === $key ) {
					continue; // نام لاتین زیرِ عنوان می‌آید، نه داخل گرید.
				}

				$value = trim( (string) get_post_meta( $post_id, $key, true ) );
				if ( '' === $value ) {
					continue;
				}

				$cells .= '<div class="qp-ident-cell">'
					. '<div class="qp-ident-cell__k">' . esc_html( $label ) . '</div>'
					. '<div class="qp-ident-cell__v">' . esc_html( $value ) . '</div>'
					. '</div>';
			}

			if ( '' === $cells ) {
				return '';
			}

			return '<div class="qp-ident-grid">' . $cells . '</div>';
		}
	}

	QPedia_Scientist_Template::instance();
}

/**
 * تابع کمکی سراسری برای قالب.
 *
 * @param int $post_id شناسهٔ مدخل.
 * @return string
 */
function qpedia_sci_identity_grid( $post_id = 0 ) {
	if ( class_exists( 'QPedia_Scientist_Template' ) ) {
		return QPedia_Scientist_Template::identity_grid( (int) $post_id );
	}

	return '';
}
