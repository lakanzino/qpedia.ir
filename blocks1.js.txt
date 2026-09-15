/* ══════════════════════════════════════════════════════════════
   بلوک‌های صفحه اصلی کوانتوم‌پدیا (v1.6.0) — بدون بیلد، JS ساده
   چهار بلوک داینامیک با کارت‌های سرمه‌ای و داده زنده.
   ══════════════════════════════════════════════════════════════ */
(function (blocks, element, blockEditor, components, i18n) {
	if (!blocks || !element || !blockEditor || !components) {
		return;
	}

	var el = element.createElement;
	var Fragment = element.Fragment;
	var __ = i18n.__;
	var InspectorControls = blockEditor.InspectorControls;
	var TextControl = components.TextControl;
	var TextareaControl = components.TextareaControl;
	var RangeControl = components.RangeControl;
	var SelectControl = components.SelectControl;
	var ToggleControl = components.ToggleControl;

	/* قاب پیش‌نمایش داخل ویرایشگر */
	function ph(icon, title, lines) {
		var kids = [
			el('div', { className: 'qp-block-ph__icon', key: 'i' }, icon),
			el('strong', { className: 'qp-block-ph__title', key: 't' }, title)
		];
		(lines || []).forEach(function (ln, idx) {
			if (ln) {
				kids.push(el('p', { className: 'qp-block-ph__line', key: 'l' + idx }, ln));
			}
		});
		kids.push(el('p', { className: 'qp-block-ph__hint', key: 'h' }, 'تنظیمات این بلوک در ستون کناری است'));
		return el('div', { className: 'qp-block-ph' }, kids);
	}

	function onAttr(props, key) {
		return function (val) {
			var upd = {};
			upd[key] = val;
			props.setAttributes(upd);
		};
	}

	function orderOptions(scientist) {
		var opts = [
			{ label: 'تازه‌ترین‌ها', value: 'date' },
			{ label: 'تازه‌ویرایش‌شده‌ها', value: 'modified' }
		];
		if (!scientist) {
			opts.push({ label: 'پربحث‌ترین‌ها (جذاب‌ترین)', value: 'comment_count' });
		}
		opts.push({ label: 'تصادفی', value: 'rand' });
		opts.push({ label: 'الفبا', value: 'title' });
		return opts;
	}

	/* ─── ۱) هیرو ─── */
	blocks.registerBlockType('qp/hero', {
		title: 'هیروی صفحه اصلی',
		description: 'تیتر و توضیح بالای صفحه اول.',
		icon: 'cover-image',
		category: 'common',
		keywords: ['صفحه اصلی', 'هیرو'],
		attributes: {
			title: { type: 'string', default: 'کوانتوم پدیا فارسی' },
			desc: { type: 'string', default: 'دانشنامه‌ای دقیق، کاربردی و خوش‌خوان برای یادگیری کوانتوم' }
		},
		edit: function (props) {
			var a = props.attributes;
			return el(
				Fragment,
				{},
				el(
					InspectorControls,
					{ key: 'ins' },
					el(TextControl, { label: 'تیتر اصلی', value: a.title, onChange: onAttr(props, 'title') }),
					el(TextareaControl, { label: 'توضیح زیر تیتر', value: a.desc, onChange: onAttr(props, 'desc') })
				),
				ph('◈', 'هیروی صفحه اصلی', [a.title])
			);
		},
		save: function () {
			return null;
		}
	});

	/* ─── ۲) دسته‌بندی‌ها (زنده) ─── */
	blocks.registerBlockType('qp/cats', {
		title: 'دسته‌بندی‌های صفحه اصلی',
		description: 'کارت‌های سرمه‌ای دسته‌ها با شمارش زنده مقاله‌ها.',
		icon: 'grid-view',
		category: 'common',
		keywords: ['صفحه اصلی', 'دسته', 'موضوع'],
		attributes: {
			title: { type: 'string', default: 'دسته‌بندی موضوعات' },
			num: { type: 'string', default: '۰۱' },
			note: { type: 'string', default: '' },
			count: { type: 'number', default: 7 },
			showSubs: { type: 'boolean', default: true }
		},
		edit: function (props) {
			var a = props.attributes;
			return el(
				Fragment,
				{},
				el(
					InspectorControls,
					{ key: 'ins' },
					el(TextControl, { label: 'تیتر بخش', value: a.title, onChange: onAttr(props, 'title') }),
					el(TextControl, { label: 'شماره بخش', value: a.num, onChange: onAttr(props, 'num') }),
					el(TextControl, { label: 'یادداشت کنار تیتر', value: a.note, onChange: onAttr(props, 'note'), help: 'خالی بماند = خودکار و زنده' }),
					el(RangeControl, { label: 'تعداد دسته‌ها', value: a.count, min: 1, max: 20, onChange: onAttr(props, 'count') }),
					el(ToggleControl, { label: 'نمایش زیردسته‌ها', checked: a.showSubs, onChange: onAttr(props, 'showSubs') })
				),
				ph('▦', 'دسته‌بندی موضوعات', [a.title, 'نمایش ' + a.count + ' دسته'])
			);
		},
		save: function () {
			return null;
		}
	});

	/* ─── ۳) مطالب (زنده) ─── */
	blocks.registerBlockType('qp/posts', {
		title: 'مطالب صفحه اصلی',
		description: 'فهرست خودکار مقاله‌ها با شمارش زنده.',
		icon: 'list-view',
		category: 'common',
		keywords: ['صفحه اصلی', 'مقاله', 'آخرین'],
		attributes: {
			title: { type: 'string', default: 'تازه‌ترین مقاله‌ها' },
			num: { type: 'string', default: '۰۲' },
			note: { type: 'string', default: '' },
			count: { type: 'number', default: 8 },
			orderby: { type: 'string', default: 'date' },
			exclude: { type: 'string', default: 'start,شروع' },
			showExcerpt: { type: 'boolean', default: false }
		},
		edit: function (props) {
			var a = props.attributes;
			return el(
				Fragment,
				{},
				el(
					InspectorControls,
					{ key: 'ins' },
					el(TextControl, { label: 'تیتر بخش', value: a.title, onChange: onAttr(props, 'title') }),
					el(TextControl, { label: 'شماره بخش', value: a.num, onChange: onAttr(props, 'num') }),
					el(TextControl, { label: 'یادداشت کنار تیتر', value: a.note, onChange: onAttr(props, 'note'), help: 'خالی بماند = خودکار و زنده (مثل: ۸ مورد از ۱۷۱ مقاله)' }),
					el(RangeControl, { label: 'تعداد مطالب', value: a.count, min: 1, max: 12, onChange: onAttr(props, 'count') }),
					el(SelectControl, {
						label: 'ترتیب مطالب',
						value: a.orderby,
						options: orderOptions(false),
						onChange: onAttr(props, 'orderby')
					}),
					el(TextControl, { label: 'حذف از لیست (نامک یا تیتر، با ویرگول)', value: a.exclude, onChange: onAttr(props, 'exclude'), help: 'مقاله‌هایی که نباید در لیست بیایند.' }),
					el(ToggleControl, { label: 'نمایش خلاصه مقاله', checked: a.showExcerpt, onChange: onAttr(props, 'showExcerpt') })
				),
				ph('☰', 'مطالب صفحه اصلی', [a.title, 'نمایش ' + a.count + ' مطلب'])
			);
		},
		save: function () {
			return null;
		}
	});

	/* ─── ۴) دانشمندان (زنده) ─── */
	blocks.registerBlockType('qp/scientists', {
		title: 'دانشمندان صفحه اصلی',
		description: 'کارت‌های چهره‌های کوانتوم با شمارش زنده.',
		icon: 'groups',
		category: 'common',
		keywords: ['صفحه اصلی', 'دانشمند', 'چهره'],
		attributes: {
			title: { type: 'string', default: 'چهره‌های کوانتوم' },
			num: { type: 'string', default: '۰۳' },
			note: { type: 'string', default: '' },
			count: { type: 'number', default: 6 },
			orderby: { type: 'string', default: 'date' }
		},
		edit: function (props) {
			var a = props.attributes;
			return el(
				Fragment,
				{},
				el(
					InspectorControls,
					{ key: 'ins' },
					el(TextControl, { label: 'تیتر بخش', value: a.title, onChange: onAttr(props, 'title') }),
					el(TextControl, { label: 'شماره بخش', value: a.num, onChange: onAttr(props, 'num') }),
					el(TextControl, { label: 'یادداشت کنار تیتر', value: a.note, onChange: onAttr(props, 'note'), help: 'خالی بماند = خودکار و زنده' }),
					el(RangeControl, { label: 'تعداد دانشمندان', value: a.count, min: 1, max: 12, onChange: onAttr(props, 'count') }),
					el(SelectControl, {
						label: 'ترتیب',
						value: a.orderby,
						options: orderOptions(true),
						onChange: onAttr(props, 'orderby')
					})
				),
				ph('◉', 'چهره‌های کوانتوم', [a.title, 'نمایش ' + a.count + ' دانشمند'])
			);
		},
		save: function () {
			return null;
		}
	});
})(window.wp.blocks, window.wp.element, window.wp.blockEditor, window.wp.components, window.wp.i18n);
