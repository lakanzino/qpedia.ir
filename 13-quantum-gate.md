# گیت کوانتومی چیست؟ الفبای عمل روی کیوبیت‌ها در رایانش کوانتومی

اگر **کیوبیت** را مادهٔ خامِ رایانش کوانتومی بدانیم، **گیت کوانتومی** همان چیزی است که این مادهٔ خام را شکل می‌دهد. در کامپیوترهای معمولی، گیت‌های منطقی مثل AND و NOT روی بیت‌ها عمل می‌کنند. در دنیای کوانتوم هم ما با «گیت» طرفیم، اما جنسِ کار فرق دارد: این‌جا گیت‌ها فقط صفر را به یک یا یک را به صفر تبدیل نمی‌کنند؛ آن‌ها می‌توانند **برهم‌نهی، فاز، و رابطهٔ میان چند کیوبیت** را تغییر دهند [1](https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits) [2](https://learn.microsoft.com/en-us/azure/quantum/concepts-circuits).

برای همین، اگر مقالهٔ <a href="https://qpedia.ir/quantum-computer/">کامپیوتر کوانتومی چیست؟</a> را خوانده باشی و این سؤال برایت مانده باشد که «این ماشین دقیقاً با کیوبیت چه کار می‌کند؟»، جواب کوتاه این است: با **گیت‌های کوانتومی** روی آن‌ها عمل می‌کند.

## گیت کوانتومی دقیقاً چیست؟

گیت کوانتومی یک **عملِ قابل‌کنترل روی یک یا چند کیوبیت** است که حالت کوانتومی آن‌ها را تغییر می‌دهد. در زبان رسمی‌تر، گیت‌های کوانتومی با **عملگرهای یکانی** یا unitary توصیف می‌شوند؛ یعنی عملیات‌هایی که ساختار احتمال را حفظ می‌کنند و در اصل برگشت‌پذیرند [1](https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits) [3](https://learn.microsoft.com/en-us/azure/quantum/concepts-multiple-qubits).

همین یک نکته خیلی مهم است: **بیشتر گیت‌های کوانتومی ذاتاً برگشت‌پذیرند**. این با بسیاری از گیت‌های کلاسیک فرق دارد. مثلاً در دنیای کلاسیک، از روی خروجی یک گیت AND همیشه نمی‌توان ورودی‌ها را دقیق برگرداند؛ اما در رایانش کوانتومی، گیت باید طوری باشد که اطلاعات را نابود نکند [2](https://learn.microsoft.com/en-us/azure/quantum/concepts-circuits).

## چرا به آن «گیت» می‌گویند؟

چون مثل دروازه‌ای است که حالت ورودی را می‌گیرد و به حالت خروجی دیگری تبدیل می‌کند. اما اگر بخواهیم ساده‌سازی نکنیم، گیت کوانتومی را نباید فقط شبیه یک کلید روشن/خاموش کلاسیک ببینیم. گیت کوانتومی بیشتر شبیه **دستورِ تغییرِ جهت روی فضای حالت** است.

اگر مقالهٔ <a href="https://qpedia.ir/operator/">عملگر چیست؟</a> را یادت باشد، این‌جا همان ایده خیلی زنده می‌شود: گیت کوانتومی در عمل، یکی از صورت‌های فیزیکیِ همان «عملگر» است که بر حالت اثر می‌گذارد.

## یک مثال بومی برای فهم شهودی

فرض کن در **متروی تهران** فقط قرار نیست مسافر را از ایستگاه «صفر» به ایستگاه «یک» ببری. گاهی باید او را طوری وارد شبکه کنی که در مسیرهای ممکن، الگوهای متفاوتی از احتمال و رابطه شکل بگیرد؛ تازه اگر چند مسافر به هم وابسته باشند، تغییر مسیر یکی می‌تواند در آرایش کلیِ حرکت اثر بگذارد.

این تشبیه کامل نیست، اما برای فهم فرق مهمی بد نیست: گیت کوانتومی فقط «تعویض مقدار» نیست؛ **آرایشِ حالت** را عوض می‌کند.

## چه فرقی با گیت کلاسیک دارد؟

چند فرق مهم دارد:

### ۱) روی کیوبیت عمل می‌کند، نه فقط بیت
یعنی روی چیزی عمل می‌کند که می‌تواند در <a href="https://qpedia.ir/quantum-superposition/">برهم‌نهی کوانتومی</a> باشد، نه فقط صفر یا یک.

### ۲) با فاز هم سر و کار دارد
در دنیای کوانتوم، فقط این مهم نیست که احتمال صفر و یک چقدر است؛ **فاز نسبی** هم اهمیت دارد. بعضی گیت‌ها مثل Z ،S و T بیشتر از آنکه «مقدار» را عوض کنند، ساختار فاز را تغییر می‌دهند [1](https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits).

### ۳) باید برگشت‌پذیر باشد
چون گیت‌های کوانتومی با عملگرهای یکانی نمایش داده می‌شوند، در اصل می‌توان عملیات را وارونه کرد [1](https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits) [2](https://learn.microsoft.com/en-us/azure/quantum/concepts-circuits).

### ۴) بعضی گیت‌ها می‌توانند درهم‌تنیدگی بسازند
گیت‌های چندکیوبیتی، به‌ویژه گیت‌هایی مثل CNOT، فقط روی دو سیم جداگانه کار نمی‌کنند؛ می‌توانند بین کیوبیت‌ها رابطه‌ای بسازند که با زبان کلاسیک خوب توصیف نمی‌شود [1](https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits) [3](https://learn.microsoft.com/en-us/azure/quantum/concepts-multiple-qubits).

## چند گیت معروف که باید بشناسیم

### گیت X
این گیت از بعضی جهت‌ها شبیه NOT کلاسیک است: اگر کیوبیت در حالت پایهٔ صفر باشد، آن را به یک می‌برد و برعکس [1](https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits).

### گیت H یا هادامارد
این یکی از مهم‌ترین گیت‌ها برای شروع فهم کوانتوم است. گیت هادامارد می‌تواند از یک حالت پایه، **برهم‌نهی** بسازد؛ مثلاً از |0⟩ حالتی شبیه جمعِ متوازن صفر و یک تولید کند [1](https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits).

برای همین، اگر مقالهٔ <a href="https://qpedia.ir/quantum-superposition/">برهم‌نهی کوانتومی</a> را بخوانی، در پس‌زمینهٔ خیلی از مثال‌هایش ردّ هادامارد را می‌بینی.

### گیت‌های Z ،S و T
این‌ها بیشتر به تغییر فاز مربوط‌اند تا برگرداندنِ سادهٔ صفر و یک [1](https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits). خیلی از تفاوت‌های ظریف میان مدارهای کوانتومی در همین بخش خودش را نشان می‌دهد.

### گیت CNOT
یکی از مشهورترین گیت‌های دوکیوبیتی است. در این‌جا یک کیوبیت نقش کنترل دارد و دیگری هدف. CNOT در بسیاری از مدارهای مهم، از جمله مدارهایی که درهم‌تنیدگی می‌سازند، نقش محوری دارد [2](https://learn.microsoft.com/en-us/azure/quantum/concepts-circuits) [3](https://learn.microsoft.com/en-us/azure/quantum/concepts-multiple-qubits).

## گیت کوانتومی چه ربطی به مدار کوانتومی دارد؟

مدار کوانتومی در اصل **چیدمانی از گیت‌ها و اندازه‌گیری‌ها** است. یعنی تو کیوبیت‌ها را آماده می‌کنی، روی آن‌ها دنباله‌ای از گیت‌ها می‌گذاری، و در پایان اندازه‌گیری می‌کنی تا خروجی کلاسیکی بگیری [1](https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits) [2](https://learn.microsoft.com/en-us/azure/quantum/concepts-circuits).

اگر بخواهیم خیلی خلاصه بگوییم:
- **کیوبیت** = واحد اطلاعات
- **گیت کوانتومی** = عمل روی اطلاعات
- **مدار کوانتومی** = ترکیب این عمل‌ها در طول زمان
- **اندازه‌گیری** = تبدیل نتیجه به خروجی قابل‌خواندن

## آیا هر گیت چندکیوبیتی را می‌شود با گیت‌های ساده‌تر ساخت؟

در عمل، خیلی از مدارها با یک مجموعهٔ پایه از گیت‌ها ساخته می‌شوند. در نظریهٔ رایانش کوانتومی، مفهوم **مجموعهٔ جهان‌شمول** اهمیت دارد؛ یعنی مجموعه‌ای از گیت‌ها که بتوان با ترکیبشان هر تحولِ لازم را با دقت کافی تقریب زد [3](https://learn.microsoft.com/en-us/azure/quantum/concepts-multiple-qubits).

این نکته مهم است، چون در سخت‌افزار واقعی، ما معمولاً به بی‌نهایت گیت آماده دسترسی نداریم؛ بلکه دستگاه روی مجموعه‌ای محدود از عملیات فیزیکی سوار می‌شود.

## چرا در عمل، تعداد و عمق گیت‌ها مهم است؟

چون هرچه مدار طولانی‌تر و شلوغ‌تر شود، خطر نویز و <a href="https://qpedia.ir/decoherence/">واهمدوسی</a> بیشتر می‌شود. حتی اگر از نظر نظری مدار درست باشد، در سخت‌افزار واقعی باید دید چند گیت لازم دارد و این گیت‌ها با چه دقتی اجرا می‌شوند [1](https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits).

برای همین در رایانش کوانتومی، فقط «درست بودنِ الگوریتم» کافی نیست؛ **سبک بودن مدار** هم مهم است.

## آیا گیت کوانتومی همان عملگر در فیزیک کوانتوم است؟

به‌طور کلی، گیت‌ها را می‌توان نوعی عملگر دانست که برای پردازش اطلاعات در مدار کوانتومی به‌کار می‌رود. اما در زبان آموزشی بهتر است این تفاوت را نگه داریم: هر جا در فیزیک از عملگر حرف می‌زنیم، لزوماً منظورمان «گیتِ قابل‌اجرا روی پردازنده» نیست. با این حال، برای خوانندهٔ عمومی، نزدیک‌ترین پل مفهومی همین است که گیت، **نسخهٔ محاسباتیِ عملگر** است.

## یک سوءتفاهم رایج

سوءتفاهم رایج این است که فکر کنیم گیت کوانتومی فقط معادل فانتزیِ همان گیت‌های صفر و یکیِ کلاسیک است. نه. اگر این‌طور نگاه کنی، نقش فاز، برهم‌نهی، و درهم‌تنیدگی را از دست می‌دهی. آن‌وقت دیگر نمی‌فهمی چرا اصلاً کامپیوتر کوانتومی چیزی بیش از یک کامپیوتر معمولیِ سریع‌تر است.

## جمع‌بندی

گیت کوانتومی ابزار اصلیِ عمل روی کیوبیت‌ها در رایانش کوانتومی است. این گیت‌ها:

- روی یک یا چند کیوبیت اثر می‌گذارند
- با عملگرهای یکانی توصیف می‌شوند
- در اصل برگشت‌پذیرند
- می‌توانند برهم‌نهی، فاز و درهم‌تنیدگی را تغییر دهند
- و بلوک‌های سازندهٔ مدارهای کوانتومی‌اند [1](https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits) [2](https://learn.microsoft.com/en-us/azure/quantum/concepts-circuits) [3](https://learn.microsoft.com/en-us/azure/quantum/concepts-multiple-qubits)

اگر بخواهم همهٔ مقاله را در یک جمله جمع کنم، می‌گویم: **گیت کوانتومی همان زبانی است که کامپیوتر کوانتومی با آن روی کیوبیت‌ها فکر و عمل می‌کند.**

---

## پیوندهای داخلی پیشنهادی

- <a href="https://qpedia.ir/quantum-computer/">کامپیوتر کوانتومی چیست؟</a>
- <a href="https://qpedia.ir/qubit/">کیوبیت چیست؟</a>
- <a href="https://qpedia.ir/operator/">عملگر چیست؟</a>
- <a href="https://qpedia.ir/quantum-superposition/">برهم‌نهی کوانتومی</a>
- <a href="https://qpedia.ir/quantum-entanglement-explained/">درهم‌تنیدگی کوانتومی</a>
- <a href="https://qpedia.ir/decoherence/">واهمدوسی</a>
- <a href="https://qpedia.ir/quantum-measurement/">اندازه‌گیری و فروپاشی</a>
- <a href="https://qpedia.ir/quantum-algorithm/">الگوریتم کوانتومی چیست؟</a>

## منبع معتبر خارجی

- IBM Quantum Learning — Bits, gates, and circuits: https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits
- Microsoft Azure Quantum — Quantum circuit diagram conventions: https://learn.microsoft.com/en-us/azure/quantum/concepts-circuits
- Microsoft Azure Quantum — Operations on multiple qubits: https://learn.microsoft.com/en-us/azure/quantum/concepts-multiple-qubits

---

## بستهٔ ثبت و سئو — خارج از متن مقاله

**عنوان نوشته:** گیت کوانتومی چیست؟ الفبای عمل روی کیوبیت‌ها در رایانش کوانتومی  
**اسلاگ:** `quantum-gate`  
**author:** `Reza Darvishi`  
**نوع محتوا:** `quantum_article`

**دسته‌ها / taxonomy:**
- `technology`
- `quantum-computing`

**برچسب‌های پیشنهادی:**
- گیت کوانتومی
- گیت هادامارد
- CNOT
- مدار کوانتومی
- کیوبیت
- عملگر یکانی

**چکیدهٔ وردپرس:**
گیت کوانتومی عملی برگشت‌پذیر روی یک یا چند کیوبیت است که حالت، فاز و گاهی درهم‌تنیدگی را در مدار کوانتومی تغییر می‌دهد.

**عنوان سئو:**
گیت کوانتومی چیست؟ توضیح ساده و دقیق quantum gate | کوانتوم پدیا

**متای توضیحات:**
گیت کوانتومی چیست و چه فرقی با گیت کلاسیک دارد؟ توضیحی روشن دربارهٔ X، هادامارد، CNOT، برگشت‌پذیری و نقش گیت‌ها در مدار کوانتومی.

**عبارت کلیدی اصلی:**
- گیت کوانتومی چیست

**عبارت‌های کلیدی فرعی:**
- quantum gate
- گیت هادامارد
- CNOT چیست
- مدار کوانتومی
- عملگر یکانی

**لینک‌های داخلی استفاده‌شده در متن:**
- `https://qpedia.ir/quantum-computer/`
- `https://qpedia.ir/qubit/`
- `https://qpedia.ir/operator/`
- `https://qpedia.ir/quantum-superposition/`
- `https://qpedia.ir/quantum-entanglement-explained/`
- `https://qpedia.ir/decoherence/`
- `https://qpedia.ir/quantum-measurement/`

**منابع خارجی برای ثبت:**
- https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits
- https://learn.microsoft.com/en-us/azure/quantum/concepts-circuits
- https://learn.microsoft.com/en-us/azure/quantum/concepts-multiple-qubits

**یادداشت انتشار:**
- بهتر است بعد از «کامپیوتر کوانتومی» منتشر شود.
- این مقاله بعداً باید از مقاله‌های الگوریتم‌های کوانتومی لینک داخلی بگیرد.
