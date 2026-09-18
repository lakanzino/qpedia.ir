<?php
/**
 * Plugin Name: Qpedia Final Images (one-shot)
 * Description: جایگزینی اجباری هر ۱۲۶ تصویر شاخص + آلت استاندارد، تکی‌تکی با نمایش زنده. بعد از اجرا حذفش کنید.
 * Version: 3.0.0
 */

defined( 'ABSPATH' ) || exit;

function qp_final_alts() {
	return array(
		'absolute-zero' => 'اینفوگرافیک آموزشی «صفر مطلق چیست؟»',
		'alpha-decay' => 'اینفوگرافیک آموزشی «واپاشی آلفا چیست؟»',
		'antimatter' => 'اینفوگرافیک آموزشی «پادماده چیست؟»',
		'aspect-experiment-1982' => 'اینفوگرافیک آموزشی «آزمایش آسپه ۱۹۸۲ چه بود؟»',
		'atomic-clock-gps' => 'اینفوگرافیک آموزشی «ساعت اتمی و جی‌پی‌اس»',
		'attosecond-nobel-2023' => 'اینفوگرافیک آموزشی «نوبل فیزیک ۲۰۲۳؛ عکاسی از حرکت الکترون»',
		'bell-experiments' => 'اینفوگرافیک آموزشی «آزمایش های بل: چگونه درهم تنیدگی اثبات شد!»',
		'bell-inequality' => 'اینفوگرافیک آموزشی «نامساوی بل»',
		'bird-quantum-compass' => 'اینفوگرافیک آموزشی «قطب‌نمای پرندگان»',
		'black-hole-information-paradox' => 'اینفوگرافیک آموزشی «پارادوکس اطلاعات سیاه چاله؛ معمای هاوکینگ»',
		'bohr-atomic-model' => 'اینفوگرافیک آموزشی «مدل اتمی بور»',
		'bose-einstein-condensate' => 'اینفوگرافیک آموزشی «چگالش بوز-اینشتین چیست؟»',
		'casimir-effect' => 'اینفوگرافیک آموزشی «اثر کازیمیر»',
		'coherence' => 'اینفوگرافیک آموزشی «همدوسی چیست؟»',
		'coin-vs-dice-quantum-uncertainty' => 'اینفوگرافیک آموزشی «تمثیل تاس در مقابل تمثیل سکه: کدام برای عدم قطعیت بهتر است؟»',
		'copenhagen-interpretation' => 'اینفوگرافیک آموزشی «تفسیر کپنهاگی»',
		'decoherence' => 'اینفوگرافیک آموزشی «واهمدوسی (Decoherence)؛ چرا گربه‌ای را نمی‌بینیم که هم‌زمان زنده و مرده باشد؟»',
		'determinism-vs-probability' => 'اینفوگرافیک آموزشی «تفاوت جبرگرایی کلاسیک و احتمال کوانتمی»',
		'does-ai-use-quantum' => 'اینفوگرافیک آموزشی «آیا هوش مصنوعی از کوانتوم استفاده می کند؟»',
		'does-quantum-prove-god' => 'اینفوگرافیک آموزشی «آیا کوانتوم ثابت می کند خدا وجود دارد یا ندارد؟»',
		'double-slit-experiment' => 'اینفوگرافیک آموزشی «آزمایش دو شکاف؛ معروف‌ترین آزمایش فیزیک، که هنوز هم درک کاملش سخت است»',
		'einstein-bohr-debate' => 'اینفوگرافیک آموزشی «نبرد اینشتین و بور بر سر معنای کوانتوم»',
		'einstein-photoelectric-effect' => 'اینفوگرافیک آموزشی «اینشتین و اثر فوتوالکتریک (نه فقط نسبیت)»',
		'electron' => 'اینفوگرافیک آموزشی «الکترون چیست؟ ویژگی‌ها، نقش در اتم و برق»',
		'energy-levels' => 'اینفوگرافیک آموزشی «ترازهای انرژی و کوانتش»',
		'entanglement-myths' => 'اینفوگرافیک آموزشی «آیا درهم تنیدگی یعنی اطلاعات سریع تر از نور منتقل می شود؟»',
		'entanglement-quantum-computers' => 'اینفوگرافیک آموزشی «درهم‌تنیدگی در کامپیوترهای کوانتمی امروزی»',
		'enzyme-quantum-tunneling' => 'اینفوگرافیک آموزشی «آنزیم‌ها؛ عبور از دیوار به‌جای پریدن»',
		'everything-is-energy-claim' => 'اینفوگرافیک آموزشی ««همه‌چیز انرژی است» — بررسی یک ادعا»',
		'feynman-quantum-explainer' => 'اینفوگرافیک آموزشی «فاینمن: نابغه‌ای که کوانتوم را ساده توضیح می‌داد»',
		'fiber-optics' => 'اینفوگرافیک آموزشی «فیبر نوری چگونه کار می‌کند؟»',
		'flash-memory' => 'اینفوگرافیک آموزشی «حافظهٔ فلش چطور کار می‌کند؟»',
		'forgotten-women-quantum' => 'اینفوگرافیک آموزشی «زنان فراموش‌شدهٔ فیزیک کوانتوم»',
		'genetic-mutation' => 'اینفوگرافیک آموزشی «آیا جهش ژنتیکی کوانتمی است؟»',
		'grover-algorithm' => 'اینفوگرافیک آموزشی «الگوریتم گروور چیست؟»',
		'heisenberg-uncertainty-principle' => 'اینفوگرافیک آموزشی «اصل عدم قطعیت هایزنبرگ به زبان ساده»',
		'higgs-boson' => 'اینفوگرافیک آموزشی «بوزون هیگز چیست؟»',
		'holographic-principle' => 'اینفوگرافیک آموزشی «اصل هولوگرافیک؛ آیا جهان ما یک هولوگرام است؟»',
		'how-lasers-work' => 'اینفوگرافیک آموزشی «لیزر چطور کار می‌کند؟»',
		'human-teleportation' => 'اینفوگرافیک آموزشی «چرا تله پورت انسان از نظر علمی غیرممکن است؟»',
		'ibm-condor-processor' => 'اینفوگرافیک آموزشی «پردازندهٔ IBM Condor؛ چرا هزار کیوبیت کافی نیست»',
		'is-classical-physics-wrong' => 'اینفوگرافیک آموزشی «آیا فیزیک کلاسیک اشتباه بود؟ نه، محدود بود»',
		'is-many-worlds-real' => 'اینفوگرافیک آموزشی «آیا کوانتوم یعنی چندجهانی واقعی است؟»',
		'is-the-brain-quantum' => 'اینفوگرافیک آموزشی «آیا مغز کوانتمی است؟»',
		'law-of-attraction-quantum' => 'اینفوگرافیک آموزشی «قانون جذب و کوانتوم؛ کجای این استدلال می لنگد؟»',
		'many-worlds-interpretation' => 'اینفوگرافیک آموزشی «تفسیر جهان‌های موازی»',
		'mind-quantum-reality' => 'اینفوگرافیک آموزشی «آیا با فکر کردن می توان واقعیت کوانتمی را تغییر داد؟»',
		'mitochondria-proton-tunneling' => 'اینفوگرافیک آموزشی «تونل زنی در میتوکندری؛ الکترون یا پروتون؟»',
		'mri-quantum' => 'اینفوگرافیک آموزشی «ام‌آرآی (MRI) چگونه کار می‌کند؟ ریشهٔ کوانتمی آن»',
		'neutrino' => 'اینفوگرافیک آموزشی «نوترینو چیست؟»',
		'nuclear-spin' => 'اینفوگرافیک آموزشی «اسپین هسته‌ای چیست؟»',
		'pauli-exclusion-principle' => 'اینفوگرافیک آموزشی «اصل طرد پاولی دقیقاً چه می‌گوید؟ به زبان ساده»',
		'pending-photosynthesis' => 'اینفوگرافیک آموزشی «فتوسنتز؛ کارآمدترین ماشین جهان و رد پای کوانتوم»',
		'pet-scan-antimatter' => 'اینفوگرافیک آموزشی «پادماده در پزشکی؛ اسکن پت چطور کار می کند؟»',
		'photoelectric-effect' => 'اینفوگرافیک آموزشی «اثر فوتوالکتریک»',
		'photon' => 'اینفوگرافیک آموزشی «فوتون دقیقاً چیست؟»',
		'physicists-on-quantum-weirdness' => 'اینفوگرافیک آموزشی «ده دیدگاه فیزیکدانان بزرگ دربارهٔ عجایب کوانتوم»',
		'pilot-wave' => 'اینفوگرافیک آموزشی «تفسیر دوبروی-بوهم چیست؟»',
		'planck-constant' => 'اینفوگرافیک آموزشی «ثابت پلانک؛ کوچک‌ترین واحد جهان»',
		'post-quantum-cryptography' => 'اینفوگرافیک آموزشی «رمزنگاری پساکوانتمی؛ قفل های تازهٔ اینترنت»',
		'q-day' => 'اینفوگرافیک آموزشی «روز کیو چیست و واقعاً کِی می رسد؟»',
		'quantum-alternative-medicine-science' => 'اینفوگرافیک آموزشی «کوانتوم و پزشکی»',
		'quantum-analogy-exercise-boundary' => 'اینفوگرافیک آموزشی «تمرین ذهنی: خودتان یک تمثیل بسازید و مرزش را پیدا کنید»',
		'quantum-battery' => 'اینفوگرافیک آموزشی «باتری کوانتمی؛ چرا بزرگ تر یعنی سریع تر؟»',
		'quantum-career-future-learn' => 'اینفوگرافیک آموزشی «آینده شغلی: آیا باید فیزیک کوانتوم یاد بگیریم؟»',
		'quantum-century-2025' => 'اینفوگرافیک آموزشی «صد سالگی کوانتوم؛ از جزیرهٔ هلگولاند تا امروز»',
		'quantum-chemistry' => 'اینفوگرافیک آموزشی «شیمی کوانتمی چیست؟ چرا دستتان از دیوار رد نمی شود»',
		'quantum-classical-boundary' => 'اینفوگرافیک آموزشی «چرا کوانتوم را در زندگی روزمره حس نمی کنیم؟»',
		'quantum-computer-reality' => 'اینفوگرافیک آموزشی «کامپیوتر کوانتمی چیست و چقدر با واقعیت فاصله دارد؟»',
		'quantum-darwinism' => 'اینفوگرافیک آموزشی «داروینیسم کوانتمی؛ چرا همه یک واقعیت می بینیم؟»',
		'quantum-entanglement-explained' => 'اینفوگرافیک آموزشی «درهم‌تنیدگی کوانتمی؛ «اثر شبح‌وار» که واقعی است، اما پیام نمی‌فرستد»',
		'quantum-eraser' => 'اینفوگرافیک آموزشی «پاک کن کوانتمی؛ آیا آینده بر گذشته اثر می گذارد؟»',
		'quantum-error-correction' => 'اینفوگرافیک آموزشی «تصحیح خطای کوانتمی چیست؟»',
		'quantum-fivefold-mental-map' => 'اینفوگرافیک آموزشی «نقشهٔ ذهنی پنج‌گانه برای فهم درست کوانتوم»',
		'quantum-fluctuations-cosmos' => 'اینفوگرافیک آموزشی «افت وخیز کوانتمی؛ چطور کهکشان ها متولد شدند؟»',
		'quantum-free-will' => 'اینفوگرافیک آموزشی «کوانتوم و ارادهٔ آزاد؛ آیا آینده از قبل نوشته شده؟»',
		'quantum-gate' => 'اینفوگرافیک آموزشی «گیت کوانتمی چیست؟»',
		'quantum-gravity' => 'اینفوگرافیک آموزشی «گرانش کوانتمی چیست؟ بزرگ ترین چالش فیزیک»',
		'quantum-healing-debunked' => 'اینفوگرافیک آموزشی «شفای کوانتمی؛ چرا این ادعا شبه علم است؟»',
		'quantum-immortality' => 'اینفوگرافیک آموزشی «جاودانگی کوانتمی؛ کجای این استدلال می لنگد؟»',
		'quantum-internet-satellite' => 'اینفوگرافیک آموزشی «اینترنت کوانتمی فضایی؛ ماجرای ماهوارهٔ میسیوس»',
		'quantum-interpretation-debate' => 'اینفوگرافیک آموزشی «آیا فیزیک دانان بر سر معنای اندازه گیری توافق دارند؟»',
		'quantum-machine-learning' => 'اینفوگرافیک آموزشی «یادگیری ماشین کوانتمی؛ وعده ها و واقعیت ها»',
		'quantum-measurement' => 'اینفوگرافیک آموزشی «اندازه‌گیری و فروپاشی در کوانتوم؛ بزرگ‌ترین درزِ مکانیک کوانتمی»',
		'quantum-navigation' => 'اینفوگرافیک آموزشی «ناوبری کوانتمی؛ مسیریابی بدون ماهواره»',
		'quantum-physics-vs-quantum-mechanics' => 'اینفوگرافیک آموزشی «تفاوت فیزیک کوانتوم و مکانیک کوانتمی چیست؟»',
		'quantum-radar' => 'اینفوگرافیک آموزشی «رادار کوانتمی؛ آیا جنگندهٔ رادارگریز را می بیند؟»',
		'quantum-random-number-generator' => 'اینفوگرافیک آموزشی «عدد تصادفی کوانتمی؛ تنها تصادف واقعی جهان»',
		'quantum-sensors' => 'اینفوگرافیک آموزشی «حسگرهای کوانتمی؛ آیندهٔ دقت اندازه‌گیری»',
		'quantum-simulation' => 'اینفوگرافیک آموزشی «شبیه‌سازی کوانتمی چیست؟»',
		'quantum-smell' => 'اینفوگرافیک آموزشی «حس بویایی؛ شکل یا ارتعاش؟»',
		'quantum-spin' => 'اینفوگرافیک آموزشی «اسپین؛ چرخشی که چرخش نیست»',
		'quantum-spin-liquid' => 'اینفوگرافیک آموزشی «مایع اسپینی کوانتمی؛ ماده ای که هرگز آرام نمی گیرد»',
		'quantum-superposition' => 'اینفوگرافیک آموزشی «برهم‌نهی کوانتمی؛ چرا سکهٔ چرخان، الکترون نیست؟»',
		'quantum-supremacy' => 'اینفوگرافیک آموزشی «برتری کوانتمی چیست؟»',
		'quantum-teleportation' => 'اینفوگرافیک آموزشی «تله پورت کوانتمی چیست؟»',
		'quantum-thermodynamics' => 'اینفوگرافیک آموزشی «ترمودینامیک کوانتمی؛ موتوری به اندازهٔ یک اتم»',
		'quantum-tunneling' => 'اینفوگرافیک آموزشی «تونل‌زنی کوانتمی؛ پدیده‌ای که بدونش خورشید نمی‌تابید»',
		'quantum-understanding-achievement' => 'اینفوگرافیک آموزشی «چرا «نفهمیدنِ درست» کوانتوم، خودش یک دستاورد است؟»',
		'quantum-zeno-effect' => 'اینفوگرافیک آموزشی «اثر زنون کوانتمی»',
		'quark' => 'اینفوگرافیک آموزشی «کوارک چیست؟»',
		'qubit' => 'اینفوگرافیک آموزشی «کیوبیت چیست؟ چرا «بیت کوانتمی» یک بیت بهتر نیست؟»',
		'scanning-tunneling-microscope' => 'اینفوگرافیک آموزشی «میکروسکوپ تونلی چیست؟»',
		'schrodinger-cat' => 'اینفوگرافیک آموزشی «گربهٔ شرودینگر»',
		'schrodinger-life-equation' => 'اینفوگرافیک آموزشی «شرودینگر: زندگی، معادله و گربه‌ای که هرگز نداشت»',
		'shor-algorithm' => 'اینفوگرافیک آموزشی «الگوریتم شور چیست؟»',
		'solar-cells-photoelectric' => 'اینفوگرافیک آموزشی «پنل خورشیدی و اثر فوتوالکتریک؛ تبدیل نور به جریان زندگی»',
		'solvay-conference-1927' => 'اینفوگرافیک آموزشی «کنفرانس سولوی ۱۹۲۷ چه بود؟»',
		'spot-pseudoscience-one-sentence' => 'اینفوگرافیک آموزشی «چگونه ادعای شبه‌علمی را در یک جمله تشخیص دهیم»',
		'standard-model' => 'اینفوگرافیک آموزشی «مدل استاندارد چیست؟»',
		'stern-gerlach-experiment' => 'اینفوگرافیک آموزشی «آزمایش اشترن-گرلاخ چیست؟»',
		'stimulated-emission' => 'اینفوگرافیک آموزشی «گسیل تحریکی چیست؟»',
		'string-theory-quantum' => 'اینفوگرافیک آموزشی «نظریهٔ ریسمان و کوانتوم؛ جهان از جنس نت است؟»',
		'superconductivity' => 'اینفوگرافیک آموزشی «ابررسانایی»',
		'superfluidity' => 'اینفوگرافیک آموزشی «ابرشارگی؛ مایعی که از لیوان بالا می‌رود»',
		'time-crystal' => 'اینفوگرافیک آموزشی «کریستال زمان چیست؟ ماده ای که در زمان تکرار می شود»',
		'topological-quantum-computing' => 'اینفوگرافیک آموزشی «کامپیوتر توپولوژیک؛ گره ای که خطا را نمی بیند»',
		'transistor-quantum' => 'اینفوگرافیک آموزشی «ترانزیستور؛ کوانتوم در جیب شما»',
		'ultraviolet-catastrophe' => 'اینفوگرافیک آموزشی «فاجعهٔ فرابنفش»',
		'virtual-particles' => 'اینفوگرافیک آموزشی «ذرات مجازی چیستند؟»',
		'wave-function' => 'اینفوگرافیک آموزشی «تابع موج چیست؟ کامل‌ترین نقشهٔ یک ذره — ولی خودش واقعیت نیست»',
		'wave-particle-duality' => 'اینفوگرافیک آموزشی «دوگانگی موج و ذره»',
		'what-is-quantum' => 'اینفوگرافیک آموزشی «کوانتوم یعنی چه؟»',
		'wheeler-delayed-choice' => 'اینفوگرافیک آموزشی «انتخاب تأخیری ویلر؛ فوتون از قبل تصمیم نگرفته»',
		'wigner-friend' => 'اینفوگرافیک آموزشی «پارادوکس دوست ویگنر؛ آیا واقعیت برای همه یکی است؟»',
		'willow-chip' => 'اینفوگرافیک آموزشی «تراشهٔ ویلو؛ گوگل واقعاً چه چیزی را ثابت کرد؟»',
	);
}

function qp_final_images() {
	$dir   = plugin_dir_path( __FILE__ ) . 'images/';
	$files = array();
	if ( ! is_dir( $dir ) ) {
		return $files;
	}
	foreach ( scandir( $dir ) as $f ) {
		if ( '.webp' === substr( $f, -5 ) ) {
			$slug          = basename( $f, '.webp' );
			$files[ $slug ] = $dir . $f;
		}
	}
	ksort( $files );
	return $files;
}

add_action( 'admin_menu', 'qp_final_menu' );
function qp_final_menu() {
	add_management_page(
		'ایمپورتر نهایی تصاویر',
		'ایمپورتر نهایی',
		'manage_options',
		'qp-final-images',
		'qp_final_page'
	);
}

function qp_final_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$files = qp_final_images();
	$alts  = qp_final_alts();
	$slugs = array_keys( $files );
	?>
	<div class="wrap">
		<h1>ایمپورتر نهایی تصاویر شاخص (۱۲۶ تصویر)</h1>
		<p>هر تصویر تکی‌تکی روی مقالهٔ خودش می‌نشیند، آلت ثبت و تصویر قبلی حذف می‌شود. لیست کامل پایین است و لحظه‌به‌لحظه تیک می‌خورد.</p>
		<p>
			<button id="qp-start" class="button button-primary button-large">شروع جایگزینی همه</button>
			<button id="qp-retry" class="button button-large" style="display:none">تلاش مجدد ناموفق‌ها</button>
			<button id="qp-stop" class="button button-large" style="display:none">توقف</button>
		</p>
		<div id="qp-bar-wrap" style="background:#e5e5e5;border-radius:8px;max-width:640px;height:22px;overflow:hidden">
			<div id="qp-bar" style="background:#46b450;height:22px;width:0%;color:#fff;font-size:12px;line-height:22px;text-align:center">۰٪</div>
		</div>
		<p id="qp-counts" style="font-size:14px">آماده… (<?php echo esc_html( number_format_i18n( count( $slugs ) ) ); ?> تصویر)</p>
		<div id="qp-summary" style="display:none;max-width:640px"></div>
		<table class="widefat striped" style="max-width:900px">
			<thead><tr><th style="width:50px">ردیف</th><th>اسلاگ</th><th>آلت</th><th style="width:220px">وضعیت</th></tr></thead>
			<tbody>
			<?php $i = 0; foreach ( $slugs as $s ) : $i++; ?>
				<tr id="qp-row-<?php echo esc_attr( $s ); ?>">
					<td><?php echo esc_html( number_format_i18n( $i ) ); ?></td>
					<td><code><?php echo esc_html( $s ); ?></code></td>
					<td style="font-size:12px"><?php echo esc_html( isset( $alts[ $s ] ) ? $alts[ $s ] : '—' ); ?></td>
					<td class="qp-st" data-s="pending">⏳ در انتظار</td>
				</tr>
			<?php endforeach; ?>
			</tbody>
		</table>
	</div>
	<script>
	(function(){
		var slugs = <?php echo wp_json_encode( $slugs ); ?>;
		var nonce = <?php echo wp_json_encode( wp_create_nonce( 'qp_final' ) ); ?>;
		var stop = false, running = false, ok = 0, skip = 0, err = 0, doneN = 0;
		var fa = function(n){ return Number(n).toLocaleString('fa-IR'); };
		function setRow(s, html, st){ var r = document.getElementById('qp-row-'+s); if(!r) return; var c = r.querySelector('.qp-st'); c.innerHTML = html; c.setAttribute('data-s', st); }
		function paint(){
			var total = slugs.length, p = total ? Math.round(doneN/total*100) : 0;
			var bar = document.getElementById('qp-bar');
			bar.style.width = p + '%'; bar.textContent = fa(p) + '٪';
			document.getElementById('qp-counts').innerHTML = 'پیشرفت: <b>'+fa(doneN)+' از '+fa(total)+'</b> — ✅ '+fa(ok)+' | ⏭ '+fa(skip)+' | ❌ '+fa(err);
		}
		function finish(){
			running = false;
			document.getElementById('qp-stop').style.display = 'none';
			var box = document.getElementById('qp-summary');
			var skipped = [], errors = [];
			slugs.forEach(function(s){ var r = document.getElementById('qp-row-'+s); if(!r) return; var st = r.querySelector('.qp-st').getAttribute('data-s'); if(st==='skip') skipped.push(s); if(st==='error') errors.push(s); });
			var h = '<h2>✅ تمام شد</h2><p>نشست: <b>'+fa(ok)+'</b> — مقاله پیدا نشد: <b>'+fa(skip)+'</b> — خطا: <b>'+fa(err)+'</b></p>';
			if (skipped.length) h += '<p><b>⏭ مقاله پیدا نشد:</b><br><code>'+skipped.join(', ')+'</code></p>';
			if (errors.length) h += '<p><b>❌ خطا:</b><br><code>'+errors.join(', ')+'</code></p>';
			h += '<p>حالا: ۱) کش LiteSpeed را پاک کنید ۲) این افزونه (و ایمپورترهای قبلی) را <b>حذف</b> کنید.</p>';
			box.innerHTML = h; box.style.display = 'block';
			if (errors.length || skipped.length) document.getElementById('qp-retry').style.display = '';
		}
		function one(s, cb){
			setRow(s, '🔄 در حال پردازش…', 'run');
			var fd = new FormData();
			fd.append('action', 'qp_final_one');
			fd.append('_ajax_nonce', nonce);
			fd.append('slug', s);
			fetch(ajaxurl, {method:'POST', body:fd, credentials:'same-origin'})
				.then(function(r){ return r.json(); })
				.then(function(j){
					if (j && j.success && j.data && j.data.status === 'ok') { ok++; setRow(s, '✅ نشست (#' + j.data.post_id + ')', 'ok'); }
					else if (j && j.success && j.data && j.data.status === 'skip') { skip++; setRow(s, '⏭ مقاله پیدا نشد', 'skip'); }
					else { err++; var m = (j && j.data && j.data.msg) ? j.data.msg : 'خطا'; setRow(s, '❌ ' + m, 'error'); }
					doneN++; paint(); cb();
				})
				.catch(function(){ err++; setRow(s, '❌ خطای ارتباط', 'error'); doneN++; paint(); cb(); });
		}
		function run(list){
			if (running) return;
			running = true; stop = false;
			document.getElementById('qp-stop').style.display = '';
			document.getElementById('qp-retry').style.display = 'none';
			document.getElementById('qp-summary').style.display = 'none';
			var i = 0;
			(function next(){
				if (stop || i >= list.length) { finish(); return; }
				one(list[i], function(){ i++; setTimeout(next, 150); });
			})();
		}
		document.getElementById('qp-start').addEventListener('click', function(){
			ok = 0; skip = 0; err = 0; doneN = 0; paint(); run(slugs);
		});
		document.getElementById('qp-retry').addEventListener('click', function(){
			var list = slugs.filter(function(s){ var r = document.getElementById('qp-row-'+s); if(!r) return false; var st = r.querySelector('.qp-st').getAttribute('data-s'); return (st === 'error' || st === 'skip'); });
			err = 0; skip = 0; doneN = ok; paint(); run(list);
		});
		document.getElementById('qp-stop').addEventListener('click', function(){ stop = true; });
	})();
	</script>
	<?php
}

add_action( 'wp_ajax_qp_final_one', 'qp_final_one' );
function qp_final_one() {
	if ( ! current_user_can( 'manage_options' ) ) {
		wp_send_json_error( array( 'msg' => 'دسترسی غیرمجاز' ) );
	}
	check_ajax_referer( 'qp_final' );

	$slug = isset( $_POST['slug'] ) ? sanitize_title( wp_unslash( $_POST['slug'] ) ) : '';
	if ( '' === $slug || ! preg_match( '/^[a-z0-9-]+$/', $slug ) ) {
		wp_send_json_error( array( 'msg' => 'اسلاگ نامعتبر' ) );
	}
	$path = plugin_dir_path( __FILE__ ) . 'images/' . $slug . '.webp';
	if ( ! is_file( $path ) ) {
		wp_send_json_error( array( 'msg' => 'فایل پیدا نشد' ) );
	}

	$post = get_page_by_path( $slug, OBJECT, 'quantum_article' );
	if ( ! $post instanceof WP_Post ) {
		wp_send_json_success( array( 'status' => 'skip' ) );
	}

	require_once ABSPATH . 'wp-admin/includes/media.php';
	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/image.php';

	$data = @file_get_contents( $path );
	if ( false === $data ) {
		wp_send_json_error( array( 'msg' => 'خواندن فایل' ) );
	}
	$bits = wp_upload_bits( $slug . '.webp', null, $data );
	if ( ! empty( $bits['error'] ) ) {
		wp_send_json_error( array( 'msg' => 'آپلود' ) );
	}

	$alts   = qp_final_alts();
	$alt    = isset( $alts[ $slug ] ) ? $alts[ $slug ] : $post->post_title;
	$att_id = wp_insert_attachment(
		array(
			'post_mime_type' => 'image/webp',
			'post_title'     => $alt,
			'post_status'    => 'inherit',
		),
		$bits['file'],
		$post->ID
	);
	if ( ! $att_id || is_wp_error( $att_id ) ) {
		wp_send_json_error( array( 'msg' => 'درج در مدیا' ) );
	}
	wp_update_attachment_metadata( $att_id, wp_generate_attachment_metadata( $att_id, $bits['file'] ) );
	update_post_meta( $att_id, '_wp_attachment_image_alt', $alt );

	$old = get_post_thumbnail_id( $post->ID );
	if ( $old && (int) $old !== (int) $att_id ) {
		wp_delete_attachment( $old, true );
	}
	set_post_thumbnail( $post->ID, $att_id );

	wp_send_json_success( array( 'status' => 'ok', 'post_id' => $post->ID ) );
}
