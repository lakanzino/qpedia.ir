# -*- coding: utf-8 -*-
"""
QPEDIA / Quantum Pedia — 16:9 featured-image (thumbnail) generator
Minimal educational infographic style, tech/cyber paper-textured background.
Deterministic per-article output. Generates 1920x1080 PNGs + CSV + ZIP.
"""
import os, math, random, csv, zipfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "featured-images")
FONTS = os.path.join(HERE, "fonts")

W, H = 1920, 1080

# ------------------------------------------------------------------ fonts
def F(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

# ------------------------------------------------------------------ palette
PAPER = (252, 251, 246, 255)
INK = (30, 39, 73, 255)          # dark navy for FA title / accents
GRID = (196, 205, 222, 120)      # faint blueprint grid
HALF = (178, 188, 208, 70)       # halftone dots
KW = (158, 168, 190, 150)        # scattered keywords
WM = (150, 160, 184, 120)        # watermarks
CIRC = (172, 182, 204, 110)      # scattered line-work

MOODS = {
    "blue":   ((62, 130, 246), (18, 34, 88)),     # blue -> navy
    "orange": ((255, 138, 61), (24, 42, 104)),    # orange -> dark navy
    "purple": ((139, 92, 246), (40, 26, 92)),     # purple -> navy
}

# ------------------------------------------------------------------ manifest
# slug, fa title, en title, mood, icon, keywords (EN, 4)
ARTICLES = [
 ("what-is-quantum","کوانتوم یعنی چه؟","What Is Quantum?","blue","levels",["quanta","discrete","energy","packets"]),
 ("quantum-superposition","برهم‌نهی کوانتومی","Quantum Superposition","blue","superpose",["states","overlap","probability","wave"]),
 ("wave-particle-duality","دوگانگی موج و ذره","Wave–Particle Duality","blue","duality",["wave","particle","light","electron"]),
 ("wave-function","تابع موج چیست؟","The Wave Function","blue","psi",["psi","amplitude","probability","collapse"]),
 ("quantum-measurement","اندازه‌گیری و فروپاشی","Measurement & Collapse","blue","measure",["observer","collapse","eigenstate","probe"]),
 ("quantum-spin","اسپین؛ چرخشی که چرخش نیست","Quantum Spin","blue","spin",["spin up","spin down","magnet","axis"]),
 ("energy-levels","ترازهای انرژی و کوانتش","Energy Levels","blue","ladder",["orbitals","quantization","photon","transition"]),
 ("decoherence","واهم‌دوسی؛ چرا دنیا عادی است!","Decoherence","blue","decohere",["environment","classical","interference","loss"]),
 ("planck-constant","ثابت پلانک؛ کوچک‌ترین واحد جهان","Planck's Constant","blue","planck",["h","quantum of action","energy","photon"]),
 ("pauli-exclusion-principle","اصل طرد پاولی دقیقاً چه می‌گوید؟ به زبان ساده","Pauli Exclusion Principle","blue","pauli",["fermions","orbitals","spin","exclusion"]),
 ("photon","فوتون دقیقا چیست؟","The Photon","orange","photon",["light","quanta","frequency","electromagnetic"]),
 ("electron","الکترون چیست؟ ویژگی‌ها، نقش در اتم و برق","The Electron","orange","electron",["charge","orbit","current","atom"]),
 ("photoelectric-effect","اثر فوتوالکتریک","Photoelectric Effect","orange","photo",["light","electron","threshold","Einstein"]),
 ("ultraviolet-catastrophe","فاجعهٔ فرابنفش","Ultraviolet Catastrophe","orange","uv",["blackbody","spectrum","divergence","UV"]),
 ("bohr-atomic-model","مدل اتمی بور","Bohr's Atomic Model","orange","bohr",["orbit","nucleus","shells","spectrum"]),
 ("bell-inequality","نامساوی بل","Bell's Inequality","orange","bellcurve",["locality","hidden variables","correlation","EPR"]),
 ("double-slit-experiment","آزمایش دو شکاف","Double-Slit Experiment","orange","slits",["interference","wave","fringes","electron"]),
 ("quantum-zeno-effect","اثر زنون کوانتومی","Quantum Zeno Effect","orange","zeno",["measurement","freeze","evolution","watch"]),
 ("quantum-entanglement-explained","درهم‌تنیدگی کوانتومی","Quantum Entanglement","blue","entangle",["correlation","spooky action","pair","state"]),
 ("quantum-tunneling","تونل‌زنی کوانتومی","Quantum Tunneling","blue","tunnel",["barrier","probability","wave","penetrate"]),
 ("schrodinger-cat","گربهٔ شرودینگر","Schrödinger's Cat","purple","cat",["superposition","box","thought experiment","decay"]),
 ("vacuum-fluctuations","نوسانات خلأ","Vacuum Fluctuations","orange","pair",["virtual particles","empty space","energy","field"]),
 ("casimir-effect","اثر کازیمیر","The Casimir Effect","orange","plates",["plates","vacuum","force","attraction"]),
 ("superconductivity","ابررسانایی","Superconductivity","blue","levitate",["zero resistance","levitation","Meissner","cooling"]),
 ("superfluidity","ابرشارگی؛ مایعی که از لیوان بالا می‌رود","Superfluidity","blue","liquid",["zero viscosity","helium","climb","flow"]),
 ("mri-quantum","ام‌آرآی (MRI) چگونه کار می‌کند؟ ریشهٔ کوانتومی آن","MRI & Quantum Spin","blue","mri",["magnet","spin","imaging","scan"]),
 ("how-lasers-work","لیزر چطور کار می‌کند؟","How Lasers Work","orange","laser",["stimulated emission","coherent","beam","photon"]),
 ("transistor-quantum","ترانزیستور؛ کوانتوم در جیب شما","Transistors: Quantum in Your Pocket","blue","chip",["semiconductor","band","switch","chip"]),
 ("atomic-clock-gps","ساعت اتمی و جی‌پی‌اس","Atomic Clocks & GPS","blue","clock",["cesium","frequency","time","satellite"]),
 ("qubit","کیوبیت چیست؟","The Qubit","blue","bloch",["0 and 1","superposition","sphere","quantum bit"]),
 ("quantum-cryptography-internet-security","رمزنگاری کوانتومی و آیندهٔ امنیت اینترنت","Quantum Cryptography","blue","key",["key","QKD","security","eavesdrop"]),
 ("bird-quantum-compass","قطب‌نمای پرندگان","The Bird's Quantum Compass","blue","compass",["magnetoreception","migration","radical pair","Earth"]),
 ("quantum-smell","حس بویایی؛ شکل یا ارتعاش؟","Quantum Smell","blue","molecule",["olfaction","vibration","molecule","nose"]),
 ("enzyme-quantum-tunneling","آنزیم‌ها؛ عبور از دیوار به‌جای پریدن","Enzyme Quantum Tunneling","blue","enzyme",["catalysis","barrier","proton","biology"]),
 ("quantum-photosynthesis","فتوسنتز؛ کارآمدترین ماشین جهان و رد پای کوانتوم","Quantum Photosynthesis","orange","leaf",["exciton","energy transfer","leaf","efficiency"]),
 ("copenhagen-interpretation","تفسیر کپنهاگی","Copenhagen Interpretation","purple","collapse",["collapse","measurement","Born rule","probabilistic"]),
 ("many-worlds-interpretation","تفسیر جهان‌های موازی","Many-Worlds Interpretation","purple","branch",["branching","parallel worlds","Everett","universes"]),
 ("quantum-alternative-medicine-science","کوانتوم و پزشکی جایگزین: کجا علم است، کجا نیست","Quantum Alternative Medicine","purple","med",["evidence","claims","science","medicine"]),
 ("everything-is-energy-claim","«همه‌چیز انرژی است» — بررسی یک ادعا","'Everything Is Energy'?","purple","bolt",["energy","claim","pseudoscience","skeptic"]),
 ("is-the-brain-quantum","آیا مغز کوانتومی است؟","Is the Brain Quantum?","purple","brain",["consciousness","neuron","coherence","claim"]),
 ("spot-pseudoscience-one-sentence","چگونه ادعای شبه‌علمی را در یک جمله تشخیص دهیم","Spotting Pseudoscience","purple","lens",["red flags","skepticism","evidence","claim"]),
 ("quantum-computer-reality","کامپیوتر کوانتومی چیست و چقدر با واقعیت فاصله دارد","The Quantum Computer","blue","qchip",["qubit","processor","error","supremacy"]),
 ("why-quantum-math-works","چرا ریاضیات کوانتوم درست است ولی «فهمش» سخت است","Why Quantum Math Works","purple","math",["formalism","Hilbert","abstract","prediction"]),
 ("solar-cells-photoelectric","پنل خورشیدی و اثر فوتوالکتریک؛ تبدیل نور به جریان زندگی","Solar Cells & Photoelectric Effect","orange","solar",["photovoltaic","sunlight","current","panel"]),
 ("max-planck-blackbody","پلانک و بحران تابش جسم سیاه؛ جرقه‌ای که فیزیک را متحول کرد","Planck & Blackbody Radiation","orange","blackbody",["spectrum","cavity","radiation","1900"]),
 ("einstein-bohr-debate","نبرد اینشتین و بور بر سر معنای کوانتوم","Einstein vs. Bohr","orange","debate",["debate","determinism","dice","reality"]),
 ("quantum-learning-resources","منابع معتبر فارسی و انگلیسی برای یادگیری عمیق‌تر کوانتوم","Learning Quantum Physics","blue","book",["books","courses","study","resources"]),
 ("feynman-quantum-explainer","فاینمن: نابغه‌ای که کوانتوم را ساده توضیح می‌داد","Feynman Explains Quantum","orange","diagram",["path integral","diagram","lectures","QED"]),
 ("schrodinger-life-equation","شرودینگر: زندگی، معادله و گربه‌ای که هرگز نداشت","Schrödinger: Life & Equation","purple","equation",["wave equation","cat","biography","1926"]),
 ("forgotten-women-quantum","زنان فراموش‌شدهٔ فیزیک کوانتوم","Forgotten Women of Quantum","orange","star",["Noether","Meitner","Wu","women"]),
 ("dirac-antimatter","دیراک و پیش‌بینی پادماده؛ وقتی ریاضیات از واقعیت جلو زد","Dirac & Antimatter","orange","antimatter",["positron","antiparticle","annihilation","prediction"]),
 ("entanglement-quantum-computers","درهم‌تنیدگی در کامپیوترهای کوانتومی امروزی","Entanglement in Quantum Computers","blue","qchip",["qubits","gate","circuit","correlation"]),
 ("quantum-sensors","حسگرهای کوانتومی؛ آیندهٔ دقت اندازه‌گیری","Quantum Sensors","blue","signal",["precision","measurement","magnetometry","sensitivity"]),
 ("quantum-fivefold-mental-map","نقشهٔ ذهنی پنج‌گانه برای فهم درست کوانتوم","A Mental Map of Quantum","purple","mindmap",["map","concepts","mind","framework"]),
 ("quantum-understanding-achievement","جمع بندی نهایی: چرا «نفهمیدنِ درست» کوانتوم خودش یک دستاورد است؟","Understanding Quantum","purple","bulb",["insight","conceptual","understanding","aha"]),
 ("quantum-analogy-exercise-boundary","تمرین ذهنی: خودتان یک تمثیل بسازید و مرزش را پیدا کنید","Building Quantum Analogies","purple","pencil",["analogy","exercise","limits","model"]),
 ("coin-vs-dice-quantum-uncertainty","تمثیل تاس در مقابل تمثیل سکه: کدام برای عدم قطعیت بهتر است؟","Coin vs. Dice","purple","dice",["probability","uncertainty","random","chance"]),
 ("quantum-physics-vs-quantum-mechanics","تفاوت فیزیک کوانتوم و مکانیک کوانتومی چیست؟","Quantum Physics vs. Mechanics","blue","compare",["terminology","theory","field","formalism"]),
 ("determinism-vs-probability","تفاوت جبرگرایی کلاسیک و احتمال کوانتومی","Determinism vs. Probability","purple","bellcurve",["chance","causality","random","predict"]),
 ("why-large-objects-dont-superpose","برهم‌نهی یعنی چه، و چرا اشیای بزرگ برهم‌نهی نمی‌شوند","Why Big Things Don't Superpose","blue","compare",["macro","decoherence","scale","interference"]),
 ("superposition-explained","برهم‌نهی چیست؟ وقتی یک ذره «هم این است هم آن»","Superposition Explained","blue","superpose",["both","state","probability","overlap"]),
 ("heisenberg-uncertainty-principle","اصل عدم قطعیت هایزنبرگ به زبان ساده","Heisenberg Uncertainty","blue","uncertain",["position","momentum","limit","precise"]),
 ("quantum-career-future-learn","آینده شغلی: آیا باید فیزیک کوانتوم یاد بگیریم؟","A Career in Quantum?","blue","path",["career","skills","industry","future"]),
 ("is-many-worlds-real","آیا کوانتوم یعنی چندجهانی واقعی است؟","Are Many Worlds Real?","purple","branch",["universes","interpretation","testability","reality"]),
 ("does-ai-use-quantum","آیا هوش مصنوعی از کوانتوم استفاده می‌کند؟","Does AI Use Quantum?","blue","ai",["neural network","machine learning","qubits","compute"]),
 ("brain-quantum-phenomena","آیا مغز انسان از پدیده‌های کوانتومی استفاده می‌کند؟ (بررسی ادعا‌ها)","Quantum in the Brain?","purple","brain",["consciousness","microtubules","claim","evidence"]),
 ("quantum-interpretation-debate","آیا فیزیک‌دانان بر سر معنای اندازه‌گیری توافق دارند؟","The Measurement Debate","purple","debate",["interpretation","measurement","consensus","philosophy"]),
 ("is-classical-physics-wrong","آیا فیزیک کلاسیک اشتباه بود؟ نه، محدود بود","Was Classical Physics Wrong?","orange","compare",["Newton","limit","approximation","classical"]),
 ("einstein-photoelectric-effect","اینشتین و اثر فوتوالکتریک (نه فقط نسبیت)","Einstein & Photoelectric Effect","orange","photo",["light quantum","Nobel","photon","1905"]),
 ("does-quantum-prove-god","آیا کوانتوم ثابت می‌کند خدا وجود دارد یا ندارد؟","Does Quantum Prove God?","purple","qmark",["belief","science","philosophy","claim"]),
 ("entanglement-myths","آیا درهم‌تنیدگی یعنی اطلاعات سریع‌تر از نور منتقل می‌شود؟","Entanglement Myths","purple","entangle",["faster than light","myth","no-communication","correlation"]),
 ("bell-experiments","آزمایش‌های بل: چگونه درهم‌تنیدگی اثبات شد!","Bell's Experiments","orange","belltest",["test","locality","detector","violation"]),
 ("mind-quantum-reality","آیا با فکر کردن می‌توان واقعیت کوانتومی را تغییر داد؟","Can Mind Change Reality?","purple","mind",["consciousness","observer","reality","claim"]),
 ("quantum-teleportation","تله‌پورت کوانتومی چیست؟","Quantum Teleportation","blue","teleport",["state transfer","entanglement","information","protocol"]),
]
assert len(ARTICLES) == 74, len(ARTICLES)
assert len({a[0] for a in ARTICLES}) == 74

# ------------------------------------------------------------------ drawing helpers
def ellipse_pts(cx, cy, rx, ry, rot=0.0, n=80):
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        x = rx * math.cos(t); y = ry * math.sin(t)
        xr = cx + x * math.cos(rot) - y * math.sin(rot)
        yr = cy + x * math.sin(rot) + y * math.cos(rot)
        pts.append((xr, yr))
    return pts

def sine_pts(cx, cy, amp, wlen, phases, n=120, rot=0.0):
    pts = []
    for i in range(n + 1):
        t = -1 + 2 * i / n
        x = t * wlen
        y = amp * math.sin(t * phases * math.pi)
        xr = cx + x * math.cos(rot) - y * math.sin(rot)
        yr = cy + x * math.sin(rot) + y * math.cos(rot)
        pts.append((xr, yr))
    return pts

def dashed_ellipse(d, cx, cy, rx, ry, color, width=1, dash=14, gap=10, start=0.0):
    a = start
    while a < 360:
        b = min(a + dash, 360)
        pts = []
        for i in range(8):
            t = math.radians(a + (b - a) * i / 7)
            pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
        d.line(pts, fill=color, width=width)
        a += dash + gap

def fade(img, k):
    r, g, b, a = img.split()
    a = a.point(lambda v: int(v * k))
    return Image.merge("RGBA", (r, g, b, a))

def v_gradient(size, c1, c2):
    w, h = size
    grad = Image.new("RGBA", (w, h))
    gd = ImageDraw.Draw(grad)
    for y in range(h):
        t = y / max(h - 1, 1)
        c = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)) + (255,)
        gd.line([(0, y), (w, y)], fill=c)
    return grad

def icon_layer(size, c1, c2, draw_fn):
    """Render draw_fn (white-on-black mask) and colorize with vertical gradient."""
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    draw_fn(d, size)
    grad = v_gradient((size, size), c1, c2)
    grad.putalpha(mask)
    return grad

# ------------------------------------------------------------------ icons
def I_atom(d, S):
    cx = cy = S/2; lw = max(3, S//46)
    r = S*0.28
    d.ellipse([cx-r*0.22, cy-r*0.22, cx+r*0.22, cy+r*0.22], fill=255)
    for rot, dr in [(0.35, 0.95), (-0.35, 0.95), (1.57, 0.95)]:
        d.line(ellipse_pts(cx, cy, r, r*dr, rot), fill=255, width=lw)
    for rot, dr in [(0.35, 0.95), (-0.35, 0.95), (1.57, 0.95)]:
        x = cx + r*math.cos(rot); y = cy + r*dr*math.sin(rot)
        d.ellipse([x-lw*1.6, y-lw*1.6, x+lw*1.6, y+lw*1.6], fill=255)

def I_wave(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46)
    d.line(sine_pts(cx, cy, S*0.20, S*0.62, 2), fill=255, width=lw)
    d.line(sine_pts(cx, cy+S*0.11, S*0.13, S*0.62, 2), fill=255, width=max(2,lw-1))
    # arrow head
    ex, ey = cx+S*0.30, cy
    d.line([(ex-12, ey-12), (ex, ey), (ex-12, ey+12)], fill=255, width=lw)

def I_psi(d, S):
    cx, cy = S/2, S*0.54; lw = max(3, S//40)
    d.line(sine_pts(cx, cy, S*0.16, S*0.6, 1), fill=255, width=lw)
    x0, y0 = cx - S*0.30, cy + S*0.02
    d.line([(x0, y0), (x0, y0 + S*0.30)], fill=255, width=lw)
    d.arc([cx-S*0.10, cy-S*0.02, cx+S*0.10, cy+S*0.18], 0, 180, fill=255, width=lw)

def I_levels(d, S):
    lw = max(3, S//40); x0 = S*0.16; x1 = S*0.84
    d.line([(x0, S*0.80), (x0, S*0.22)], fill=255, width=lw)
    for i, h in enumerate([0.78, 0.62, 0.46, 0.30]):
        y = S*h
        d.line([(x0, y), (x1, y)], fill=255, width=lw)
        d.ellipse([x1-4, y-4, x1+4, y+4], fill=255)
    # dashed connector
    d.line([(x0+ (x1-x0)*0.3, S*0.80), (x0+(x1-x0)*0.3, S*0.30)], fill=255, width=1)

def I_ladder(d, S):
    lw = max(3, S//40)
    x0, x1 = S*0.22, S*0.78
    for i, h in enumerate([0.76, 0.60, 0.44, 0.28]):
        y = S*h
        d.line([(x0, y), (x1, y)], fill=255, width=lw)
    d.line([(x0, S*0.76), (x0, S*0.28)], fill=255, width=lw//2)
    d.line([(x1, S*0.76), (x1, S*0.28)], fill=255, width=lw//2)
    d.ellipse([x0-5, S*0.76-5, x0+5, S*0.76+5], fill=255)

def I_superpose(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//44); r = S*0.24
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=None, outline=255, width=lw)
    d.ellipse([cx-r*0.9, cy-r*0.9, cx+r*0.9, cy+r*0.9], fill=None, outline=255, width=lw//2)
    d.ellipse([cx-5, cy-5, cx+5, cy+5], fill=255)

def I_duality(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46)
    d.line([(cx, S*0.18), (cx, S*0.82)], fill=255, width=1)
    d.line(sine_pts(cx - S*0.24, cy, S*0.15, S*0.34, 1.5), fill=255, width=lw)
    r = S*0.13
    d.ellipse([cx+S*0.11-r, cy-r, cx+S*0.11+r, cy+r], fill=None, outline=255, width=lw)
    for rr in [S*0.20, S*0.28]:
        d.arc([cx+S*0.11-rr, cy-rr, cx+S*0.11+rr, cy+rr], 180, 360, fill=255, width=1)

def I_slits(d, S):
    lw = max(3, S//46)
    bx = S*0.34
    d.line([(bx, S*0.20), (bx, S*0.80)], fill=255, width=lw+2)
    for y in [S*0.34, S*0.56]:
        d.line([(bx, y), (bx, y+S*0.10)], fill=0, width=lw+3)
    # fringes to the right
    x0 = S*0.52
    for i in range(4):
        x = x0 + i*(S*0.09)
        w = max(1, lw-1)
        d.line([(x, S*0.30), (x, S*0.70)], fill=255, width=w if i != 2 else lw+2)

def I_entangle(d, S):
    cy = S/2; lw = max(3, S//46); r = S*0.16
    for cx in [S*0.30, S*0.70]:
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=None, outline=255, width=lw)
        d.ellipse([cx-5, cy-5, cx+5, cy+5], fill=255)
    d.line(sine_pts(S/2, cy, S*0.05, S*0.30, 3), fill=255, width=lw-1)

def I_tunnel(d, S):
    lw = max(3, S//46)
    bx = S*0.55
    d.line([(bx, S*0.24), (bx, S*0.76)], fill=255, width=lw+2)
    r = S*0.09
    d.ellipse([S*0.26-r, S*0.58-r, S*0.26+r, S*0.58+r], fill=255)
    # tunneling arc through barrier
    d.arc([S*0.18, S*0.30, S*0.72, S*0.74], 200, 320, fill=255, width=lw)
    d.ellipse([S*0.66-r, S*0.46-r, S*0.66+r, S*0.46+r], fill=255)

def I_cat(d, S):
    cx, cy = S/2, S*0.52; lw = max(3, S//46)
    w, h = S*0.40, S*0.44
    d.rectangle([cx-w/2, cy-h/2, cx+w/2, cy+h/2], outline=255, width=lw)
    # cat ears
    for sx in [-1, 1]:
        ex = cx + sx*w*0.30
        d.polygon([(ex-sx*w*0.12, cy-h/2), (ex, cy-h/2-S*0.12), (ex+sx*w*0.06, cy-h/2)], outline=255)
    # psi inside
    d.line(sine_pts(cx, cy, S*0.06, S*0.20, 1), fill=255, width=2)
    x0 = cx - S*0.10
    d.line([(x0, cy), (x0, cy+S*0.10)], fill=255, width=2)

def I_photon(d, S):
    cy = S/2; lw = max(3, S//46)
    d.line(sine_pts(S/2, cy, S*0.14, S*0.6, 1.5), fill=255, width=lw)
    ex, ey = S*0.78, cy
    d.line([(ex-14, ey-12), (ex, ey), (ex-14, ey+12)], fill=255, width=lw)
    r = S*0.09
    d.ellipse([S*0.30-r, cy-r, S*0.30+r, cy+r], fill=None, outline=255, width=lw-1)

def I_electron(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46)
    d.ellipse([cx-8, cy-8, cx+8, cy+8], fill=255)
    d.line(ellipse_pts(cx, cy, S*0.30, S*0.16, 0.5), fill=255, width=lw)
    x = cx + S*0.30*math.cos(0.5); y = cy + S*0.16*math.sin(0.5)
    d.ellipse([x-7, y-7, x+7, y+7], fill=255)
    d.line([(x-7, y), (x+7, y)], fill=0, width=2)

def I_photo(d, S):
    lw = max(3, S//46)
    plate = [S*0.20, S*0.52, S*0.46, S*0.80]
    d.rectangle(plate, outline=255, width=lw)
    d.line([(S*0.16, S*0.52), (S*0.52, S*0.52)], fill=255, width=lw)
    # incoming rays
    for x in [S*0.60, S*0.70, S*0.80]:
        d.line([(x, S*0.28), (x+ (S*0.46-x)*0.4, S*0.52)], fill=255, width=max(1,lw-2))
    # ejected electron
    d.ellipse([S*0.62-8, S*0.62-8, S*0.62+8, S*0.62+8], fill=255)
    d.line([(S*0.56, S*0.72), (S*0.68, S*0.62)], fill=255, width=1)

def I_uv(d, S):
    lw = max(3, S//46)
    ox, oy = S*0.18, S*0.74
    d.line([(ox, oy), (ox, S*0.22)], fill=255, width=lw)
    d.line([(ox, oy), (S*0.84, oy)], fill=255, width=lw)
    pts = []
    for i in range(40):
        t = i/39
        x = ox + t*(S*0.66)
        y = oy - S*0.42 * (t**2 + 0.35*t) / 1.35
        pts.append((x, y))
    d.line(pts, fill=255, width=lw)
    # UV spike arrow
    d.line([(S*0.80, S*0.30), (S*0.84, S*0.20)], fill=255, width=lw)

def I_bohr(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46)
    d.ellipse([cx-9, cy-9, cx+9, cy+9], fill=255)
    for r in [0.16, 0.24, 0.32]:
        d.ellipse([cx-r*S, cy-r*S, cx+r*S, cy+r*S], outline=255, width=lw)
    for r, ang in [(0.16, 0.6), (0.24, 2.6), (0.32, 4.6)]:
        x = cx + r*S*math.cos(ang); y = cy + r*S*math.sin(ang)
        d.ellipse([x-6, y-6, x+6, y+6], fill=255)

def I_bellcurve(d, S):
    lw = max(3, S//46)
    ox, oy = S*0.16, S*0.74
    d.line([(ox, oy), (ox, S*0.20)], fill=255, width=lw)
    d.line([(ox, oy), (S*0.84, oy)], fill=255, width=lw)
    pts = []
    import math as m
    for i in range(60):
        t = -2.6 + 5.2*i/59
        x = ox + (t+2.6)/5.2*S*0.66
        y = oy - S*0.44*m.exp(-t*t/2)
        pts.append((x, y))
    d.line(pts, fill=255, width=lw)

def I_zeno(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46); r = S*0.30
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=255, width=lw)
    d.line([(cx, cy), (cx, cy - r*0.7)], fill=255, width=lw)
    d.line([(cx, cy), (cx + r*0.45, cy + r*0.1)], fill=255, width=lw)
    # pause bars
    for sx in [-1, 1]:
        x = cx + sx*S*0.07
        d.line([(x, cy-r*0.4), (x, cy+r*0.15)], fill=0, width=lw)

def I_pair(d, S):
    cy = S/2; lw = max(3, S//46); r = S*0.12
    for cx, a in [(S*0.32, 0), (S*0.68, 255)]:
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=a, outline=255, width=lw)
    d.line([(S*0.46, cy), (S*0.54, cy)], fill=255, width=1)
    # spark
    d.line([(S/2, cy-S*0.10), (S/2-5, cy-S*0.02), (S/2, cy), (S/2-5, cy+S*0.08)], fill=255, width=1)

def I_plates(d, S):
    lw = max(3, S//46)
    for x in [S*0.30, S*0.66]:
        d.line([(x, S*0.24), (x, S*0.76)], fill=255, width=lw+2)
    d.line(sine_pts(S*0.48, S/2, S*0.06, S*0.22, 3), fill=255, width=lw-1)
    d.line([(S*0.30, S*0.30), (S*0.22, S*0.30)], fill=255, width=1)
    d.line([(S*0.66, S*0.70), (S*0.74, S*0.70)], fill=255, width=1)

def I_levitate(d, S):
    lw = max(3, S//46)
    # magnet
    d.line([(S*0.28, S*0.62), (S*0.28, S*0.80)], fill=255, width=lw)
    d.line([(S*0.72, S*0.62), (S*0.72, S*0.80)], fill=255, width=lw)
    d.line([(S*0.28, S*0.62), (S*0.72, S*0.62)], fill=255, width=lw)
    d.line([(S*0.28, S*0.80), (S*0.72, S*0.80)], fill=255, width=lw)
    # floating disc
    d.ellipse([S*0.36, S*0.30, S*0.64, S*0.50], outline=255, width=lw)
    d.line([(S*0.44, S*0.50), (S*0.40, S*0.58)], fill=255, width=1)
    d.line([(S*0.56, S*0.50), (S*0.60, S*0.58)], fill=255, width=1)

def I_liquid(d, S):
    lw = max(3, S//46)
    d.line([(S*0.24, S*0.30), (S*0.24, S*0.78)], fill=255, width=lw)
    d.line([(S*0.58, S*0.30), (S*0.58, S*0.78)], fill=255, width=lw)
    d.line([(S*0.24, S*0.78), (S*0.58, S*0.78)], fill=255, width=lw)
    d.line([(S*0.24, S*0.52), (S*0.58, S*0.52)], fill=255, width=1)
    d.line(sine_pts(S*0.41, S*0.44, S*0.05, S*0.20, 2), fill=255, width=1)

def I_mri(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46)
    d.ellipse([cx-S*0.30, cy-S*0.16, cx+S*0.30, cy+S*0.16], outline=255, width=lw)
    d.ellipse([cx-S*0.30, cy-S*0.05, cx+S*0.30, cy+S*0.05], outline=255, width=lw//2)
    d.line([(cx-S*0.16, cy), (cx+S*0.16, cy)], fill=255, width=1)
    d.ellipse([cx-6, cy-6, cx+6, cy+6], fill=255)
    d.line([(cx, cy), (cx, cy-S*0.10)], fill=255, width=1)

def I_laser(d, S):
    lw = max(3, S//46)
    d.rectangle([S*0.14, S*0.40, S*0.30, S*0.60], outline=255, width=lw)
    d.line([(S*0.30, S/2), (S*0.76, S/2)], fill=255, width=lw)
    for y in [S*0.40, S*0.46, S*0.54, S*0.60]:
        d.line([(S*0.76, S/2), (S*0.84, y)], fill=255, width=1)

def I_chip(d, S):
    lw = max(3, S//46)
    x0, y0, x1, y1 = S*0.30, S*0.30, S*0.70, S*0.70
    d.rectangle([x0, y0, x1, y1], outline=255, width=lw)
    d.rectangle([S*0.40, S*0.40, S*0.60, S*0.60], outline=255, width=1)
    for k in range(6):
        t = (k+0.5)/6
        x = x0 + (x1-x0)*t
        d.line([(x, y0), (x, y0-S*0.06)], fill=255, width=lw-1)
        d.line([(x, y1), (x, y1+S*0.06)], fill=255, width=lw-1)

def I_bloch(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46); r = S*0.32
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=255, width=lw)
    d.ellipse([cx-5, cy-5, cx+5, cy+5], fill=255)
    ang = math.radians(-38)
    x = cx + r*0.8*math.cos(ang); y = cy + r*0.8*math.sin(ang)
    d.line([(cx, cy), (x, y)], fill=255, width=lw)
    d.ellipse([x-5, y-5, x+5, y+5], fill=255)

def I_key(d, S):
    lw = max(3, S//46)
    d.ellipse([S*0.42, S*0.40, S*0.58, S*0.56], outline=255, width=lw)
    d.line([(S*0.50, S*0.56), (S*0.50, S*0.74)], fill=255, width=lw)
    d.line([(S*0.42, S*0.74), (S*0.58, S*0.74)], fill=255, width=lw)
    # key hole waves
    for i in range(3):
        y = S*0.30 - i*S*0.05
        d.arc([S*0.42, y, S*0.58, y+S*0.10], 180, 360, fill=255, width=1)

def I_compass(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46); r = S*0.34
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=255, width=lw)
    d.line([(cx, cy-r), (cx, cy+r)], fill=255, width=1)
    d.line([(cx-r, cy), (cx+r, cy)], fill=255, width=1)
    d.polygon([(cx, cy-r*0.8), (cx-lw*1.2, cy), (cx+lw*1.2, cy)], fill=255)
    d.polygon([(cx, cy+r*0.8), (cx-lw*1.2, cy), (cx+lw*1.2, cy)], fill=200)

def I_molecule(d, S):
    lw = max(3, S//46)
    pts = [(S*0.30, S*0.60), (S*0.56, S*0.34), (S*0.72, S*0.62)]
    d.line([pts[0], pts[1]], fill=255, width=lw-1)
    d.line([pts[1], pts[2]], fill=255, width=lw-1)
    for i, (x, y) in enumerate(pts):
        r = S*0.09 if i == 1 else S*0.12
        d.ellipse([x-r, y-r, x+r, y+r], outline=255, width=lw)

def I_leaf(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46)
    d.ellipse([S*0.28, S*0.30, S*0.72, S*0.74], outline=255, width=lw)
    d.line([(cx, S*0.30), (cx, S*0.74)], fill=255, width=1)
    d.line([(cx, S*0.44), (S*0.40, S*0.40)], fill=255, width=1)
    d.line([(cx, S*0.58), (S*0.60, S*0.54)], fill=255, width=1)
    # sun
    d.ellipse([S*0.72, S*0.18, S*0.86, S*0.32], outline=255, width=lw)
    for ang in [45, 90, 135]:
        r = S*0.085
        x = S*0.79 + r*1.4*math.cos(math.radians(ang))
        y = S*0.25 + r*1.4*math.sin(math.radians(ang))
        d.line([(S*0.79 + r*math.cos(math.radians(ang)), S*0.25 + r*math.sin(math.radians(ang))), (x, y)], fill=255, width=1)

def I_branch(d, S):
    lw = max(3, S//46)
    root = (S*0.30, S*0.50)
    d.ellipse([root[0]-6, root[1]-6, root[0]+6, root[1]+6], fill=255)
    l1 = (S*0.52, S*0.34); l2 = (S*0.52, S*0.66)
    d.line([root, l1], fill=255, width=lw-1)
    d.line([root, l2], fill=255, width=lw-1)
    for (a, b) in [(l1, (S*0.72, S*0.22)), (l1, (S*0.72, S*0.42)),
                   (l2, (S*0.72, S*0.58)), (l2, (S*0.72, S*0.78))]:
        d.line([a, b], fill=255, width=1)
        d.ellipse([b[0]-4, b[1]-4, b[0]+4, b[1]+4], fill=255)

def I_brain(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46)
    d.ellipse([cx-S*0.30, cy-S*0.22, cx, cy+S*0.22], outline=255, width=lw)
    d.ellipse([cx, cy-S*0.22, cx+S*0.30, cy+S*0.22], outline=255, width=lw)
    d.line([(cx-S*0.12, cy-S*0.05), (cx-S*0.05, cy+S*0.06), (cx-S*0.14, cy+S*0.16)], fill=255, width=1)
    d.line([(cx+S*0.12, cy-S*0.05), (cx+S*0.05, cy+S*0.06), (cx+S*0.14, cy+S*0.16)], fill=255, width=1)

def I_med(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46); r = S*0.30
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=255, width=lw)
    d.line([(cx, cy-S*0.18), (cx, cy+S*0.18)], fill=255, width=lw)
    d.line([(cx-S*0.18, cy), (cx+S*0.18, cy)], fill=255, width=lw)
    d.line([(cx+r+6, cy-S*0.10), (cx+r+14, cy-S*0.16)], fill=255, width=1)
    d.line([(cx+r+12, cy-S*0.06), (cx+r+20, cy-S*0.14)], fill=255, width=1)

def I_bolt(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46); r = S*0.30
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=255, width=lw)
    d.polygon([(cx+S*0.10, cy-S*0.22), (cx-S*0.10, cy+S*0.02), (cx-S*0.02, cy+S*0.02), (cx-S*0.10, cy+S*0.22), (cx+S*0.10, cy-S*0.02), (cx+S*0.02, cy-S*0.02)], fill=255)

def I_lens(d, S):
    lw = max(3, S//46); r = S*0.24
    cx, cy = S*0.44, S*0.44
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=255, width=lw)
    d.line([(cx+r*0.7, cy+r*0.7), (cx+r*1.5, cy+r*1.5)], fill=255, width=lw)
    # question mark
    d.text((S*0.40, S*0.30), "?", font=F("Montserrat-ExtraBold.ttf", int(S*0.26)), fill=255)

def I_book(d, S):
    lw = max(3, S//46)
    d.line([(S*0.30, S*0.34), (S*0.30, S*0.74)], fill=255, width=lw)
    d.line([(S*0.70, S*0.34), (S*0.70, S*0.74)], fill=255, width=lw)
    d.line([(S*0.30, S*0.34), (S*0.70, S*0.34)], fill=255, width=1)
    d.line([(S*0.30, S*0.74), (S*0.70, S*0.74)], fill=255, width=1)
    d.line([(S/2, S*0.34), (S/2, S*0.74)], fill=255, width=1)
    for i in range(3):
        y = S*0.42 + i*S*0.10
        d.line([(S*0.34, y), (S*0.46, y)], fill=255, width=1)
        d.line([(S*0.54, y), (S*0.66, y)], fill=255, width=1)

def I_signal(d, S):
    cx, cy = S*0.46, S*0.60; lw = max(3, S//46)
    d.ellipse([cx-6, cy-6, cx+6, cy+6], fill=255)
    for i, r in enumerate([S*0.12, S*0.20, S*0.28]):
        d.arc([cx-r, cy-r, cx+r, cy+r], 215, 325, fill=255, width=lw if i == 2 else lw-1)

def I_star(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46)
    r_out, r_in = S*0.30, S*0.13
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi/2 + i*math.pi/5
        pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
    d.polygon(pts, outline=255)
    d.ellipse([cx-S*0.06, cy-S*0.06, cx+S*0.06, cy+S*0.06], fill=255)

def I_bulb(d, S):
    cx, cy = S/2, S*0.46; lw = max(3, S//46); r = S*0.20
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=255, width=lw)
    d.line([(cx-S*0.08, cy+r), (cx+S*0.08, cy+r)], fill=255, width=lw)
    d.line([(cx-S*0.04, cy+r), (cx-S*0.04, cy+r+S*0.10)], fill=255, width=1)
    d.line([(cx+S*0.04, cy+r), (cx+S*0.04, cy+r+S*0.10)], fill=255, width=1)
    for ang in [90, 45, 135, 180, 0]:
        a = math.radians(ang)
        x = cx + r*math.cos(a); y = cy + r*math.sin(a)
        d.line([(cx + r*1.15*math.cos(a), cy + r*1.15*math.sin(a)), (cx + r*1.4*math.cos(a), cy + r*1.4*math.sin(a))], fill=255, width=1)

def I_dice(d, S):
    lw = max(3, S//46)
    x0, y0, x1, y1 = S*0.28, S*0.28, S*0.58, S*0.58
    d.rectangle([x0, y0, x1, y1], outline=255, width=lw)
    for (dx, dy) in [(-0.09, -0.09), (0.09, 0.09), (0, 0)]:
        d.ellipse([S*0.43+dx*S-4, S*0.43+dy*S-4, S*0.43+dx*S+4, S*0.43+dy*S+4], fill=255)
    # coin
    d.ellipse([S*0.62, S*0.52, S*0.82, S*0.72], outline=255, width=lw)
    d.line([(S*0.72, S*0.52), (S*0.72, S*0.72)], fill=255, width=1)

def I_compare(d, S):
    cy = S/2; lw = max(3, S//46); r = S*0.20
    d.ellipse([S*0.22-r, cy-r, S*0.22+r, cy+r], outline=255, width=lw)
    d.ellipse([S*0.78-r, cy-r, S*0.78+r, cy+r], outline=255, width=lw)
    d.ellipse([S*0.22-4, cy-4, S*0.22+4, cy+4], fill=255)
    d.line([(S/2, S*0.34), (S/2, S*0.66)], fill=255, width=1)
    d.line([(S/2, S*0.34), (S/2-S*0.04, S*0.42)], fill=255, width=1)
    d.line([(S/2, S*0.34), (S/2+S*0.04, S*0.42)], fill=255, width=1)

def I_uncertain(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46)
    d.ellipse([cx-S*0.16, cy-S*0.16, cx+S*0.16, cy+S*0.16], outline=255, width=lw)
    for i in range(5):
        r = S*(0.20 + i*0.035)
        d.arc([cx-r, cy-r, cx+r, cy+r], 0, 360, fill=255, width=1)
    d.line([(cx, cy), (cx+S*0.26, cy-S*0.20)], fill=255, width=1)
    d.line([(cx, cy), (cx-S*0.24, cy+S*0.20)], fill=255, width=1)

def I_path(d, S):
    lw = max(3, S//46)
    pts = [(S*0.20, S*0.70), (S*0.40, S*0.70), (S*0.40, S*0.46), (S*0.62, S*0.46), (S*0.62, S*0.30), (S*0.82, S*0.30)]
    d.line(pts, fill=255, width=lw)
    for (x, y) in pts:
        d.ellipse([x-5, y-5, x+5, y+5], fill=255)

def I_ai(d, S):
    lw = max(3, S//46)
    x0, y0, x1, y1 = S*0.30, S*0.34, S*0.62, S*0.66
    d.rectangle([x0, y0, x1, y1], outline=255, width=lw)
    d.rectangle([S*0.38, S*0.42, S*0.54, S*0.58], outline=255, width=1)
    for k in range(4):
        x = x0 + (x1-x0)*(k+0.5)/4
        d.line([(x, y0), (x, y0-S*0.05)], fill=255, width=lw-1)
        d.line([(x, y1), (x, y1+S*0.05)], fill=255, width=lw-1)
    d.ellipse([S*0.64, S*0.18, S*0.84, S*0.38], outline=255, width=lw)
    d.line([(S*0.74, S*0.22), (S*0.74, S*0.34)], fill=255, width=1)

def I_qmark(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46); r = S*0.30
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=255, width=lw)
    d.text((S*0.36, S*0.30), "?", font=F("Montserrat-ExtraBold.ttf", int(S*0.34)), fill=255)
    for ang in [30, 150, 270]:
        a = math.radians(ang)
        x = cx + r*1.25*math.cos(a); y = cy + r*1.25*math.sin(a)
        d.ellipse([x-5, y-5, x+5, y+5], fill=255)

def I_mind(d, S):
    lw = max(3, S//46)
    d.ellipse([S*0.30, S*0.26, S*0.70, S*0.66], outline=255, width=lw)
    d.arc([S*0.30, S*0.66, S*0.70, S*0.86], 0, 180, fill=255, width=lw)
    d.line(sine_pts(S*0.50, S*0.46, S*0.08, S*0.20, 1), fill=255, width=1)

def I_teleport(d, S):
    lw = max(3, S//46)
    for x in [S*0.22, S*0.78]:
        d.rectangle([x-S*0.10, S*0.34, x+S*0.10, S*0.62], outline=255, width=lw)
        d.ellipse([x-4, S*0.48-4, x+4, S*0.48+4], fill=255)
    d.line(sine_pts(S/2, S*0.48, S*0.04, S*0.46, 2), fill=255, width=lw-1)

def I_debate(d, S):
    lw = max(3, S//46)
    for x, cy in [(S*0.30, S*0.42), (S*0.70, S*0.60)]:
        d.ellipse([x-S*0.16, cy-S*0.12, x+S*0.16, cy+S*0.12], outline=255, width=lw)
        d.polygon([(x-S*0.04, cy+S*0.11), (x+S*0.04, cy+S*0.11), (x, cy+S*0.20)], outline=255)
    d.polygon([(S/2+S*0.06, S*0.30), (S/2-S*0.10, S*0.52), (S/2-S*0.02, S*0.52), (S/2-S*0.06, S*0.72), (S/2+S*0.10, S*0.48), (S/2+S*0.02, S*0.48)], fill=255)

def I_solar(d, S):
    lw = max(3, S//46)
    d.ellipse([S*0.20, S*0.22, S*0.40, S*0.42], outline=255, width=lw)
    for ang in [45, 90, 135, 180]:
        a = math.radians(ang)
        cx, cy = S*0.30, S*0.32
        d.line([(cx+S*0.13*math.cos(a), cy+S*0.13*math.sin(a)), (cx+S*0.20*math.cos(a), cy+S*0.20*math.sin(a))], fill=255, width=1)
    # panel
    d.rectangle([S*0.52, S*0.48, S*0.84, S*0.78], outline=255, width=lw)
    for i in range(1, 4):
        x = S*0.52 + i*S*0.08
        d.line([(x, S*0.48), (x, S*0.78)], fill=255, width=1)
    d.line([(S*0.52, S*0.63), (S*0.84, S*0.63)], fill=255, width=1)
    d.line([(S*0.60, S*0.40), (S*0.60, S*0.48)], fill=255, width=1)

def I_blackbody(d, S):
    lw = max(3, S//46)
    d.rectangle([S*0.20, S*0.26, S*0.42, S*0.74], outline=255, width=lw)
    d.ellipse([S*0.26, S*0.32, S*0.36, S*0.42], fill=255)
    d.line([(S*0.42, S/2), (S*0.50, S/2)], fill=255, width=1)
    pts = []
    for i in range(40):
        t = i/39
        x = S*0.50 + t*S*0.34
        y = S*0.72 - S*0.30*(t*(1.6-t))*0.9
        pts.append((x, y))
    d.line(pts, fill=255, width=lw)

def I_diagram(d, S):
    lw = max(3, S//46)
    d.line([(S*0.24, S*0.30), (S/2, S*0.50)], fill=255, width=lw-1)
    d.line([(S/2, S*0.50), (S*0.78, S*0.28)], fill=255, width=lw-1)
    d.line(sine_pts(S/2, S*0.66, S*0.08, S*0.30, 2), fill=255, width=1)
    d.ellipse([S/2-4, S*0.50-4, S/2+4, S*0.50+4], fill=255)

def I_equation(d, S):
    lw = max(3, S//46)
    d.line(sine_pts(S/2, S*0.50, S*0.14, S*0.5, 1), fill=255, width=lw)
    d.line([(S*0.26, S*0.36), (S*0.26, S*0.68)], fill=255, width=lw)
    d.arc([S*0.28, S*0.36, S*0.40, S*0.48], 0, 180, fill=255, width=lw-1)

def I_clock(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46); r = S*0.32
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=255, width=lw)
    d.line([(cx, cy), (cx, cy-r*0.62)], fill=255, width=lw)
    d.line([(cx, cy), (cx+r*0.4, cy+r*0.2)], fill=255, width=lw)
    for ang in range(0, 360, 90):
        a = math.radians(ang)
        d.line([(cx+r*0.85*math.cos(a), cy+r*0.85*math.sin(a)), (cx+r*math.cos(a), cy+r*math.sin(a))], fill=255, width=1)
    d.ellipse([cx-r*0.02, cy-r*0.02, cx+r*0.02, cy+r*0.02], fill=255)

def I_mindmap(d, S):
    cx, cy = S/2, S/2; lw = max(3, S//46)
    d.ellipse([cx-8, cy-8, cx+8, cy+8], fill=255)
    for ang in [0, 72, 144, 216, 288]:
        a = math.radians(ang)
        ex = cx + S*0.26*math.cos(a); ey = cy + S*0.26*math.sin(a)
        d.line([(cx, cy), (ex, ey)], fill=255, width=lw-1)
        d.ellipse([ex-7, ey-7, ex+7, ey+7], outline=255, width=lw-1)

def I_pencil(d, S):
    lw = max(3, S//46)
    d.polygon([(S*0.30, S*0.70), (S*0.40, S*0.28), (S*0.56, S*0.28), (S*0.70, S*0.70)], outline=255)
    d.line([(S*0.30, S*0.70), (S*0.70, S*0.70)], fill=255, width=lw)
    d.line([(S*0.44, S*0.28), (S*0.52, S*0.28)], fill=255, width=1)
    d.line([(S*0.48, S*0.28), (S*0.48, S*0.70)], fill=255, width=1)
    d.polygon([(S*0.48, S*0.28), (S*0.44, S*0.18), (S*0.52, S*0.18)], fill=255)

def I_decohere(d, S):
    cx, cy = S/2, S*0.46; lw = max(3, S//46)
    d.line(sine_pts(cx, cy, S*0.14, S*0.64, 2), fill=255, width=lw)
    d.line(sine_pts(cx, cy+S*0.13, S*0.09, S*0.64, 2), fill=255, width=max(2, lw-1))
    d.line(sine_pts(cx, cy+S*0.26, S*0.05, S*0.64, 2), fill=255, width=1)

def I_measure(d, S):
    cx, cy = S/2, S*0.52; lw = max(3, S//46)
    d.line(sine_pts(cx, cy, S*0.16, S*0.7, 1.5), fill=255, width=lw)
    d.line([(cx, cy-S*0.16), (cx, cy+S*0.20)], fill=255, width=1)
    d.ellipse([cx-7, cy+S*0.24-7, cx+7, cy+S*0.24+7], fill=255)
    d.line([(cx, cy+S*0.34), (cx+S*0.05, cy+S*0.28), (cx-S*0.05, cy+S*0.28)], fill=255, width=1)

def I_spin(d, S):
    cy = S/2; lw = max(3, S//46)
    d.line([(S*0.30, cy-S*0.22), (S*0.30, cy+S*0.22)], fill=255, width=lw)
    d.line([(S*0.30, cy+S*0.22), (S*0.22, cy+S*0.12)], fill=255, width=lw)
    d.line([(S*0.30, cy+S*0.22), (S*0.38, cy+S*0.12)], fill=255, width=lw)
    d.line([(S*0.70, cy-S*0.22), (S*0.70, cy+S*0.22)], fill=255, width=lw)
    d.line([(S*0.70, cy-S*0.22), (S*0.62, cy-S*0.12)], fill=255, width=lw)
    d.line([(S*0.70, cy-S*0.22), (S*0.78, cy-S*0.12)], fill=255, width=lw)
    d.ellipse([S*0.50-6, cy-6, S*0.50+6, cy+6], fill=255)
    d.line(ellipse_pts(S*0.50, cy, S*0.13, S*0.05, 0.5), fill=255, width=1)

def I_planck(d, S):
    cx, cy = S/2, S*0.5; lw = max(3, S//46)
    # letter h
    d.line([(cx-S*0.16, S*0.30), (cx-S*0.16, S*0.78)], fill=255, width=lw)
    d.arc([cx-S*0.16, S*0.48, cx+S*0.16, S*0.78], 0, 180, fill=255, width=lw)
    # quantized steps
    for i, h in enumerate([0.30, 0.44, 0.58, 0.72]):
        d.line([(S*0.62, S*h), (S*0.82, S*h)], fill=255, width=lw-1)

def I_pauli(d, S):
    lw = max(3, S//46)
    for x, arrow in [(S*0.32, -1), (S*0.68, 1)]:
        d.rectangle([x-S*0.12, S*0.34, x+S*0.12, S*0.66], outline=255, width=lw)
    # up arrow left, down arrow right
    d.line([(S*0.32, S*0.58), (S*0.32, S*0.42)], fill=255, width=lw)
    d.line([(S*0.32, S*0.42), (S*0.26, S*0.50)], fill=255, width=lw)
    d.line([(S*0.32, S*0.42), (S*0.38, S*0.50)], fill=255, width=lw)
    d.line([(S*0.68, S*0.42), (S*0.68, S*0.58)], fill=255, width=lw)
    d.line([(S*0.68, S*0.58), (S*0.62, S*0.50)], fill=255, width=lw)
    d.line([(S*0.68, S*0.58), (S*0.74, S*0.50)], fill=255, width=lw)

def I_collapse(d, S):
    cx, cy = S/2, S*0.42; lw = max(3, S//46)
    d.line(sine_pts(cx, cy, S*0.14, S*0.7, 1.5), fill=255, width=lw)
    d.line([(cx, cy), (cx, cy+S*0.34)], fill=255, width=1)
    d.ellipse([cx-6, cy+S*0.34-6, cx+6, cy+S*0.34+6], fill=255)
    d.arc([cx-10, cy+S*0.20, cx+10, cy+S*0.30], 180, 360, fill=255, width=1)

def I_enzyme(d, S):
    lw = max(3, S//46)
    # molecule (enzyme) left
    pts = [(S*0.26, S*0.42), (S*0.36, S*0.30), (S*0.30, S*0.60)]
    d.line([pts[0], pts[1]], fill=255, width=lw-1)
    d.line([pts[0], pts[2]], fill=255, width=lw-1)
    for (x, y) in pts:
        d.ellipse([x-7, y-7, x+7, y+7], outline=255, width=lw)
    # barrier right
    d.line([(S*0.60, S*0.28), (S*0.60, S*0.72)], fill=255, width=lw)
    d.arc([S*0.40, S*0.34, S*0.80, S*0.66], 210, 330, fill=255, width=lw-1)
    d.ellipse([S*0.78-5, S*0.40-5, S*0.78+5, S*0.40+5], fill=255)

def I_antimatter(d, S):
    lw = max(3, S//46)
    d.line([(S/2, S*0.20), (S/2, S*0.80)], fill=255, width=1)
    for cx, f in [(S*0.34, 255), (S*0.66, 0)]:
        r = S*0.13
        d.ellipse([cx-r, S/2-r, cx+r, S/2+r], outline=255, width=lw)
        d.ellipse([cx-3, S/2-3, cx+3, S/2+3], fill=f)
    d.line([(S*0.50, S/2), (S*0.46, S/2-S*0.04), (S*0.54, S/2), (S*0.50, S/2+S*0.04)], fill=255, width=1)

def I_belltest(d, S):
    lw = max(3, S//46)
    d.line([(S*0.30, S/2), (S*0.70, S/2)], fill=255, width=lw-1)
    for x, ang in [(S*0.30, 45), (S*0.70, 135)]:
        a = math.radians(ang)
        r = S*0.10
        d.line([(x, S/2), (x + r*math.cos(a), S/2 - r*math.sin(a))], fill=255, width=lw)
    for x in [S*0.20, S*0.80]:
        d.ellipse([x-6, S/2-6, x+6, S/2+6], fill=255)
    d.line([(S*0.30, S*0.42), (S*0.30, S*0.58)], fill=255, width=1)
    d.line([(S*0.70, S*0.42), (S*0.70, S*0.58)], fill=255, width=1)

def I_math(d, S):
    lw = max(3, S//46)
    d.line(sine_pts(S*0.34, S*0.34, S*0.10, S*0.24, 1), fill=255, width=lw)
    # bracket
    d.line([(S*0.72, S*0.26), (S*0.66, S*0.26), (S*0.66, S*0.70), (S*0.72, S*0.70)], fill=255, width=lw-1)
    d.line([(S*0.70, S*0.38), (S*0.80, S*0.38)], fill=255, width=1)
    d.line([(S*0.70, S*0.58), (S*0.80, S*0.58)], fill=255, width=1)

def I_qchip(d, S):
    lw = max(3, S//46)
    x0, y0, x1, y1 = S*0.34, S*0.34, S*0.66, S*0.66
    d.rectangle([x0, y0, x1, y1], outline=255, width=lw)
    d.ellipse([S*0.44, S*0.44, S*0.56, S*0.56], outline=255, width=lw-1)
    d.ellipse([S/2-4, S/2-4, S/2+4, S/2+4], fill=255)
    for k in range(4):
        x = x0 + (x1-x0)*(k+0.5)/4
        d.line([(x, y0), (x, y0-S*0.05)], fill=255, width=lw-1)
        d.line([(x, y1), (x, y1+S*0.05)], fill=255, width=lw-1)
    d.line(sine_pts(S*0.74, S*0.28, S*0.03, S*0.12, 2), fill=255, width=1)

def I_star_ring(d, S):
    I_star(d, S)

ICONS = {
 "atom": I_atom, "wave": I_wave, "psi": I_psi, "levels": I_levels, "ladder": I_ladder,
 "superpose": I_superpose, "duality": I_duality, "slits": I_slits, "entangle": I_entangle,
 "tunnel": I_tunnel, "cat": I_cat, "photon": I_photon, "electron": I_electron,
 "photo": I_photo, "uv": I_uv, "bohr": I_bohr, "bellcurve": I_bellcurve, "zeno": I_zeno,
 "pair": I_pair, "plates": I_plates, "levitate": I_levitate, "liquid": I_liquid,
 "mri": I_mri, "laser": I_laser, "chip": I_chip, "bloch": I_bloch, "key": I_key,
 "compass": I_compass, "molecule": I_molecule, "leaf": I_leaf, "branch": I_branch,
 "brain": I_brain, "med": I_med, "bolt": I_bolt, "lens": I_lens, "book": I_book,
 "signal": I_signal, "star": I_star, "bulb": I_bulb, "dice": I_dice, "compare": I_compare,
 "uncertain": I_uncertain, "path": I_path, "ai": I_ai, "qmark": I_qmark, "mind": I_mind,
 "teleport": I_teleport, "debate": I_debate, "solar": I_solar, "blackbody": I_blackbody,
 "diagram": I_diagram, "equation": I_equation, "clock": I_clock, "mindmap": I_mindmap,
 "pencil": I_pencil, "decohere": I_decohere, "measure": I_measure, "spin": I_spin,
 "planck": I_planck, "pauli": I_pauli, "collapse": I_collapse, "enzyme": I_enzyme,
 "antimatter": I_antimatter, "belltest": I_belltest, "math": I_math, "qchip": I_qchip,
}

# ------------------------------------------------------------------ text helpers
import arabic_reshaper
from bidi.algorithm import get_display

RESHAPER = arabic_reshaper.ArabicReshaper(configuration={
    "delete_harakat": False, "support_ligatures": True, "delete_tatweel": False})

def fa_display(s):
    return get_display(RESHAPER.reshape(s))

def layout_en(text, size, max_w, max_lines=2):
    words = text.split()
    while size >= 24:
        f = F("Montserrat-ExtraBold.ttf", size)
        lines, cur = [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if f.getlength(t) <= max_w:
                cur = t
            else:
                if cur: lines.append(cur)
                cur = w
        if cur: lines.append(cur)
        # handle single overlong word
        if len(lines) <= max_lines and all(f.getlength(l) <= max_w for l in lines):
            return lines, size
        size -= 2
    # force fit: truncate last line
    f = F("Montserrat-ExtraBold.ttf", 24)
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if f.getlength(t) <= max_w: cur = t
        else:
            if len(lines) < max_lines - 1:
                lines.append(cur); cur = w
            else:
                while cur and f.getlength(cur + "…") > max_w: cur = cur[:-1]
                cur += "…"; break
    if cur and len(lines) < max_lines: lines.append(cur)
    return lines[:max_lines], 24

def layout_fa(text, size, max_w, max_lines=2):
    words = text.split()
    while size >= 24:
        f = F("Vazirmatn-ExtraBold.ttf", size)
        lines, cur = [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if f.getlength(fa_display(t)) <= max_w:
                cur = t
            else:
                if cur: lines.append(cur)
                cur = w
        if cur: lines.append(cur)
        if len(lines) <= max_lines and all(f.getlength(fa_display(l)) <= max_w for l in lines):
            return lines, size
        size -= 2
    f = F("Vazirmatn-ExtraBold.ttf", 24)
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if f.getlength(fa_display(t)) <= max_w: cur = t
        else:
            if len(lines) < max_lines - 1:
                lines.append(cur); cur = w
            else:
                while cur and f.getlength(fa_display(cur + "…")) > max_w: cur = cur[:-1]
                cur += "…"; break
    if cur and len(lines) < max_lines: lines.append(cur)
    return lines[:max_lines], 24

def gradient_text(text, font, c1, c2):
    tmp = Image.new("RGBA", (1, 1))
    tt = ImageDraw.Draw(tmp)
    bbox = tt.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    mask = Image.new("L", (w + 4, h + 4), 0)
    md = ImageDraw.Draw(mask)
    md.text((2 - bbox[0], 2 - bbox[1]), text, font=font, fill=255)
    grad = v_gradient((w + 4, h + 4), c1, c2)
    grad.putalpha(mask)
    return grad

# ------------------------------------------------------------------ background
_grain_cache = None
def grain():
    global _grain_cache
    if _grain_cache is None:
        noise = Image.effect_noise((W, H), 22).convert("L")
        alpha = noise.point(lambda v: (int(abs(v - 128) / 128 * 12) // 3) * 3)
        g = Image.new("RGBA", (W, H), (108, 112, 126, 0))
        g.putalpha(alpha)
        _grain_cache = g
    return _grain_cache

def draw_background(img, rnd):
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 0, W, H], fill=PAPER)
    # faint blueprint grid
    step = 96
    for x in range(0, W, step):
        d.line([(x, 0), (x, H)], fill=GRID, width=1)
    for y in range(0, H, step):
        d.line([(0, y), (W, y)], fill=GRID, width=1)
    # halftone dots (aged print)
    for y in range(0, H, 26):
        for x in range(0, W, 26):
            if rnd.random() < 0.55:
                rr = 1.2
                d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=HALF)
    # faint worn stains
    for _ in range(3):
        x = rnd.randint(0, W); y = rnd.randint(0, H)
        r = rnd.randint(160, 340)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(150, 132, 104, 10))
    # circuit traces
    for _ in range(5):
        x, y = rnd.randint(40, W - 40), rnd.randint(40, H - 40)
        for _s in range(rnd.randint(2, 4)):
            nx = x + rnd.choice([-1, 1]) * rnd.randint(60, 180)
            ny = y + rnd.choice([-1, 1]) * rnd.randint(40, 140)
            nx = max(30, min(W - 30, nx)); ny = max(30, min(H - 30, ny))
            d.line([(x, y), (nx, y)], fill=CIRC, width=1)
            d.line([(nx, y), (nx, ny)], fill=CIRC, width=1)
            d.ellipse([nx - 3, ny - 3, nx + 3, ny + 3], fill=(140, 150, 172, 140))
            x, y = nx, ny
    img.alpha_composite(grain())

# ------------------------------------------------------------------ scatter
def scatter(img, slug, icon, keywords, rnd, c1):
    d = ImageDraw.Draw(img, "RGBA")
    # keywords (EN)
    kf_sizes = [30, 34, 40, 46]
    for kw in keywords:
        size = rnd.choice(kf_sizes)
        f = F("Montserrat-Medium.ttf", size)
        tw = f.getlength(kw)
        # place away from center icon (r>260) and title band (y 630..1000, x 500..1420)
        for _ in range(60):
            x = rnd.randint(40, W - 40 - int(tw))
            y = rnd.randint(40, H - 70)
            if math.hypot(x - W/2, y - 360) < 280: continue
            if 560 < y < 1010 and 460 < x < 1460: continue
            break
        ang = rnd.choice([-8, -5, -3, 0, 0, 3, 5, 8])
        layer = Image.new("RGBA", (int(tw) + 20, size + 20), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.text((10, 10), kw, font=f, fill=(146, 156, 178, 170))
        layer = layer.rotate(ang, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(layer, (x, y))
    # small scattered icons
    for _ in range(2):
        s = rnd.randint(70, 110)
        sub = icon_layer(s, (150, 160, 184), (196, 205, 222), ICONS[icon])
        sub = fade(sub, 0.5)
        for _ in range(40):
            x = rnd.randint(30, W - 30 - s); y = rnd.randint(30, H - 30 - s)
            if math.hypot(x - W/2, y - 360) < 300: continue
            if 560 < y < 1010: continue
            break
        img.alpha_composite(sub, (x, y))
    # a generic atom + wave in corners
    for k, pos in [("atom", (60, 90)), ("wave", (W - 170, H - 200))]:
        sub = icon_layer(100, (150, 160, 184), (196, 205, 222), ICONS[k])
        sub = fade(sub, 0.45)
        img.alpha_composite(sub, pos)

# ------------------------------------------------------------------ watermarks
def watermark_block(text_lines, size, x, y, anchor_right=False):
    """Return an RGBA layer of stacked lines."""
    fonts = [(F("Montserrat-Black.ttf", size), 0), (F("Montserrat-Medium.ttf", size), 0)]
    layers = []
    maxw = 0
    rendered = []
    for i, ln in enumerate(text_lines):
        f = F("Montserrat-Black.ttf", size) if i == 0 else F("Montserrat-SemiBold.ttf", int(size * 0.78))
        bbox = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), ln, font=f)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        rendered.append((ln, f, w, h, bbox))
        maxw = max(maxw, w)
    total_h = sum(r[3] for r in rendered) + (len(rendered) - 1) * 4
    layer = Image.new("RGBA", (maxw + 6, total_h + 6), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    yy = 3
    for ln, f, w, h, bbox in rendered:
        xx = maxw - w if anchor_right else 0
        ld.text((xx - bbox[0] + 3, yy - bbox[1]), ln, font=f, fill=WM)
        yy += h + 4
    return layer

def draw_branding(img, rnd):
    d = ImageDraw.Draw(img, "RGBA")
    # top-right: QPEDIA / QUANTUM PEDIA
    tr = watermark_block(["QPEDIA", "QUANTUM PEDIA"], 46, 0, 0, anchor_right=True)
    img.alpha_composite(tr, (W - tr.width - 64, 48))
    # bottom-left: QPEDIA / QUANTUM PEDIA
    bl = watermark_block(["QPEDIA", "QUANTUM PEDIA"], 46, 0, 0)
    img.alpha_composite(bl, (64, H - bl.height - 52))
    # top-left + bottom-right: qpedia.ir
    f = F("Montserrat-SemiBold.ttf", 34)
    for (x, y) in [(64, 42), (W - 220, H - 46)]:
        d.text((x, y), "qpedia.ir", font=f, fill=(150, 160, 184, 130))
    # faint background name repeats
    f2 = F("Montserrat-SemiBold.ttf", 40)
    f3 = F("Montserrat-SemiBold.ttf", 26)
    spots = [(W*0.20, H*0.12), (W*0.80, H*0.86), (W*0.50, H*0.045)]
    for (x, y) in spots:
        d.text((x, y), "qpedia.ir", font=f3, fill=(150, 160, 184, 60))
    # tiny atom glyph beside top-right logo
    a = icon_layer(46, (150, 160, 184), (170, 178, 200), I_atom)
    a = fade(a, 0.8)
    img.alpha_composite(a, (W - 64 - tr.width - 52, 48))

# ------------------------------------------------------------------ main
def build(art):
    slug, fa, en, mood, icon, kw = art
    c1, c2 = MOODS[mood]
    rnd = random.Random(slug)

    img = Image.new("RGBA", (W, H), PAPER)
    draw_background(img, rnd)
    scatter(img, slug, icon, kw, rnd, c1)
    draw_branding(img, rnd)

    d = ImageDraw.Draw(img, "RGBA")

    # ---- center icon with dashed circles
    cx, cy = W/2, 360
    r1, r2 = 176, 208
    dashed_ellipse(d, cx, cy, r1, r1, (c1[0], c1[1], c1[2], 90), 2, dash=16, gap=12)
    dashed_ellipse(d, cx, cy, r2, r2, (c1[0], c1[1], c1[2], 55), 2, dash=10, gap=16)
    for ang in [0, 90, 180, 270]:
        a = math.radians(ang)
        d.ellipse([cx + r1*math.cos(a)-4, cy + r1*math.sin(a)-4,
                   cx + r1*math.cos(a)+4, cy + r1*math.sin(a)+4], fill=(c1[0], c1[1], c1[2], 120))
    icon = icon_layer(300, c1, c2, ICONS[icon])
    img.alpha_composite(icon, (int(cx - 150), int(cy - 150)))

    # ---- titles
    max_w = 1560
    en_lines, en_size = layout_en(en, 76, max_w, 2)
    fa_lines, fa_size = layout_fa(fa, 46, max_w, 2)

    en_f = F("Montserrat-ExtraBold.ttf", en_size)
    fa_f = F("Vazirmatn-ExtraBold.ttf", fa_size)
    en_h = en_size * 1.25
    fa_h = fa_size * 1.45
    gap = 26
    block_h = en_h * len(en_lines) + gap + fa_h * len(fa_lines)
    top = 760 - block_h / 2

    y = top
    for ln in en_lines:
        g = gradient_text(ln, en_f, c1, c2)
        img.alpha_composite(g, (int(W/2 - g.width/2), int(y)))
        y += en_h
    y += gap
    # small over-dot separator
    for k in range(3):
        x = W/2 + (k - 1) * 30
        d.ellipse([x - 3, y - 14, x + 3, y - 8], fill=(c1[0], c1[1], c1[2], 200))
    for ln in fa_lines:
        disp = fa_display(ln)
        bbox = fa_f.getbbox(disp)
        w = bbox[2] - bbox[0]
        mask = Image.new("L", (w + 4, int(fa_h) + 4), 0)
        md = ImageDraw.Draw(mask)
        md.text((2 - bbox[0], 2 - bbox[1]), disp, font=fa_f, fill=255)
        ink_layer = Image.new("RGBA", mask.size, INK)
        ink_layer.putalpha(mask)
        img.alpha_composite(ink_layer, (int(W/2 - w/2), int(y)))
        y += fa_h

    return img.convert("RGB")

def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for i, art in enumerate(ARTICLES, 1):
        slug = art[0]
        img = build(art)
        out = os.path.join(OUT, f"{slug}.png")
        q = img.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
        q.save(out, optimize=True)
        rows.append([i, slug, art[1], art[2], art[3]])
        print(f"[{i:02d}/74] {slug}")
    # CSV manifest
    with open(os.path.join(OUT, "manifest.csv"), "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["#", "slug", "title_fa", "title_en", "mood"])
        wr.writerows(rows)
    # ZIP
    zp = os.path.join(OUT, "QPEDIA-74-thumbnails.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(OUT, "manifest.csv"), "manifest.csv")
        for art in ARTICLES:
            z.write(os.path.join(OUT, f"{art[0]}.png"), f"{art[0]}.png")
    print("done ->", OUT)
    print("zip  ->", zp)

if __name__ == "__main__":
    main()
