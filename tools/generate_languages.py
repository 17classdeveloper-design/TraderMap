#!/usr/bin/env python3
"""Generate additional TraderMap language pages and synchronize language metadata."""

from __future__ import annotations

import re
from html import escape
from pathlib import Path

from translations_extra import EXTRA_TEXTS


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://17classdeveloper-design.github.io/TraderMap"
BASE = "/TraderMap"
EFFECTIVE_DATE = "2026-07-22"
LAST_MODIFIED = "2026-07-30"

ALL_LANGUAGES = [
    ("en", "en", "English", False),
    ("ja", "ja", "日本語", False),
    ("ko", "ko", "한국어", False),
    ("zh-hans", "zh-Hans", "简体中文", False),
    ("zh-hant", "zh-Hant", "繁體中文", False),
    ("de", "de", "Deutsch", False),
    ("fr", "fr", "Français", False),
    ("ro", "ro", "Română", False),
    ("uk", "uk", "Українська", False),
    ("ru", "ru", "Русский", False),
    ("id", "id", "Bahasa Indonesia", False),
    ("tr", "tr", "Türkçe", False),
    ("pt", "pt", "Português", False),
    ("es", "es", "Español", False),
    ("ar", "ar", "العربية", True),
]

EXISTING_SLUGS = {"en", "ja", "ko", "zh-hans", "zh-hant", "de", "fr"}

TEXTS = {
    "ro": {
        "lang": "ro",
        "name": "Română",
        "language_label": "Limbă · Română",
        "nav": {
            "home": "Prezentare",
            "privacy": "Confidențialitate",
            "support": "Asistență",
            "terms": "Termeni",
            "operator": "Operator",
        },
        "official": "Informații oficiale TraderMap",
        "effective": f"Data intrării în vigoare: {EFFECTIVE_DATE}",
        "scope": "TraderMap pentru iOS/iPadOS (com.17class.TraderMap) și TraderMapTV pentru tvOS (com.17class.TraderMapTV)",
        "footer": "Doar informații despre piață — nu constituie consultanță de investiții și nici serviciu de executare a ordinelor.",
        "home": {
            "title": "Piețele cripto, cartografiate clar.",
            "eyebrow": "O singură politică · două platforme Apple",
            "lede": "TraderMap prezintă prețuri de piață, grafice, tranzacții mari, lichidări, știri și semnale analitice pe iPhone, iPad și Apple TV.",
            "intro": "Acest site oficial oferă politica de confidențialitate, asistență tehnică, termenii și informațiile despre operator pentru ambele versiuni TraderMap.",
            "no_tracking": "Fără reclame. Fără analiză terță. Fără urmărire.",
            "platform_title": "Conceput pentru platformele Apple",
            "platform_desc": "Aplicația iOS/iPadOS oferă un spațiu interactiv pentru piețe. Aplicația tvOS oferă un tablou de bord pentru sufragerie, adaptat telecomenzii. Niciuna dintre aplicații nu conectează portofele, nu execută ordine și nu păstrează active.",
        },
        "privacy": {
            "title": "Politica de confidențialitate",
            "desc": "Modul în care TraderMap gestionează informațiile pe iOS, iPadOS și tvOS.",
            "sections": [
                {
                    "heading": "Domeniu de aplicare",
                    "paragraphs": [
                        "Această politică se aplică aplicației TraderMap pentru iOS și iPadOS (ID pachet com.17class.TraderMap), aplicației TraderMapTV pentru tvOS (ID pachet com.17class.TraderMapTV) și acestui site de asistență. Ambele aplicații urmează aceleași practici privind datele."
                    ],
                },
                {
                    "heading": "Date pe care nu le solicităm",
                    "paragraphs": [
                        "TraderMap nu necesită un cont și nu solicită numele, adresa de e-mail, numărul de telefon, adresa poștală, informațiile de plată, adresa portofelului, fraza seed sau cheia privată. Aplicațiile nu conțin SDK-uri publicitare, SDK-uri de analiză terță sau tehnologii de urmărire între aplicații."
                    ],
                },
                {
                    "heading": "Informații păstrate pe dispozitiv",
                    "paragraphs": [
                        "Aplicațiile păstrează local următoarele informații pentru ca setările și vizualizările recente să funcționeze conform așteptărilor. Aceste informații nu sunt încărcate ca profil de utilizator."
                    ],
                    "items": [
                        "Limba aleasă; setările de sunet și volum",
                        "Simbolurile selectate, pragurile alertelor și graficele favorite",
                        "Un identificator aleatoriu limitat la aplicație, folosit de o conexiune pentru date de predicție disponibilă numai în dezvoltare",
                        "Răspunsuri de piață și de conținut păstrate temporar în cache",
                    ],
                },
                {
                    "heading": "Prelucrare în rețea",
                    "paragraphs": [
                        "Pentru a furniza informații în timp real, aplicațiile se conectează la gateway-ul TraderMap configurat și la furnizorii de date de piață și conținut. Ca orice serviciu de internet, aceste conexiuni expun în mod necesar adresa IP și pot prelucra ora solicitării, agentul utilizator al aplicației, limba selectată, endpointul solicitat și filtrele de piață. Gateway-ul TraderMap actual folosește temporar adresa IP pentru limitarea ratei și nu creează profiluri de utilizator pe baza acesteia.",
                        "Furnizorii de infrastructură pot prelucra jurnale de conexiune limitate pentru livrare, fiabilitate și securitate, conform propriilor condiții. Deschiderea unui articol de știri original părăsește TraderMap și este guvernată de politica de confidențialitate a editorului. Acest site este găzduit de GitHub Pages, astfel încât GitHub poate prelucra informații standard despre solicitările web conform Declarației de confidențialitate GitHub.",
                    ],
                },
                {
                    "heading": "Scopuri și divulgare",
                    "paragraphs": [
                        "Informațiile sunt prelucrate numai pentru a furniza conținutul de piață solicitat, a reține preferințele de pe dispozitiv, a proteja disponibilitatea serviciului, a diagnostica defecțiunile și a respecta legea. TraderMap nu vinde informații cu caracter personal și nu le distribuie pentru publicitate direcționată. Furnizorii de servicii pot prelucra doar ceea ce este necesar pentru operarea serviciului solicitat și trebuie să ofere protecții conforme cu această politică și cu legea aplicabilă."
                    ],
                },
                {
                    "heading": "Păstrarea datelor și opțiunile dvs.",
                    "paragraphs": [
                        "Preferințele de pe dispozitiv rămân până când le modificați, resetați setarea relevantă sau eliminați aplicația. Răspunsurile din cache sunt temporare și pot fi șterse de aplicație sau de sistemul de operare. În implementarea de referință, intrările temporare de limitare a ratei din gateway expiră după aproximativ 60 de secunde. Puteți opri orice prelucrare în rețea a aplicației dezinstalând-o sau deconectând-o de la rețea."
                    ],
                    "items": [
                        "Ștergeți aplicația pentru a elimina datele locale ale acesteia",
                        "Folosiți comenzile din aplicație pentru a schimba limba, filtrele, favoritele și setările de sunet",
                        "Contactați asistența dacă considerați că serviciul deține informații despre dvs. sau doriți să exercitați un drept legal privind confidențialitatea",
                    ],
                },
                {
                    "heading": "Copii, transferuri și securitate",
                    "paragraphs": [
                        "TraderMap este un produs general de informare despre piețe și nu se adresează copiilor. Furnizorii de rețea pot prelucra informații în alte țări decât cea în care vă aflați. TraderMap utilizează HTTPS/WSS în producție și aplică măsuri de protecție rezonabile, însă nicio transmisie prin internet nu poate fi garantată ca fiind complet sigură."
                    ],
                },
                {
                    "heading": "Modificări și contact",
                    "paragraphs": [
                        "Putem actualiza această politică atunci când se modifică funcțiile aplicației, furnizorii de servicii sau legislația. Data intrării în vigoare de mai sus identifică versiunea curentă. Întrebările și solicitările privind confidențialitatea pot fi trimise prin canalul oficial de asistență."
                    ],
                },
            ],
        },
        "support": {
            "title": "Asistență tehnică",
            "desc": "Ajutor pentru TraderMap pe iPhone, iPad și Apple TV.",
            "sections": [
                {
                    "heading": "Înainte de a raporta o problemă",
                    "paragraphs": [
                        "TraderMap necesită iOS/iPadOS 16 sau o versiune ulterioară ori tvOS 16 sau o versiune ulterioară și o conexiune la internet pentru date în timp real. Sursele de piață pot întârzia sau pot fi indisponibile ocazional."
                    ],
                    "items": [
                        "Confirmați că dispozitivul este conectat la internet",
                        "Închideți și redeschideți TraderMap",
                        "Încercați alt simbol sau altă pagină",
                        "Confirmați că aplicația și sistemul de operare sunt actualizate",
                    ],
                },
                {
                    "heading": "Ce trebuie inclus",
                    "paragraphs": [
                        "Deschideți un issue pe GitHub și indicați versiunea: TraderMap (iOS/iPadOS) sau TraderMapTV (tvOS). Includeți versiunea aplicației, modelul dispozitivului, versiunea sistemului de operare, limba selectată, pașii de reproducere și capturi de ecran, dacă sunt utile."
                    ],
                    "items": [
                        "Eliminați informațiile personale sau confidențiale din capturile de ecran",
                        "Nu publicați niciodată parole, tokenuri API, fraze seed sau chei private",
                        "Nu publicați evidențe private de tranzacționare sau financiare",
                    ],
                },
                {
                    "heading": "Canal de contact",
                    "paragraphs": [
                        "Asistența tehnică, feedbackul general și solicitările de funcții sunt gestionate prin sistemul public de issue-uri al depozitului. Operatorul este 17ClassDeveloper (cont GitHub: 17classdeveloper-design). Nu se garantează un timp de răspuns."
                    ],
                },
            ],
            "primary_action": "Contactați asistența tehnică",
            "secondary_action": "Vedeți depozitul",
        },
        "terms": {
            "title": "Termeni de utilizare și declinarea răspunderii",
            "desc": "Termenii aplicabili ambelor aplicații TraderMap pentru platformele Apple.",
            "sections": [
                {
                    "heading": "Acceptare și domeniu",
                    "paragraphs": [
                        "Prin utilizarea TraderMap sau TraderMapTV, acceptați acești termeni. Dacă nu sunteți de acord, nu utilizați aplicațiile. Acești termeni se aplică ambelor ID-uri de pachet menționate mai sus."
                    ],
                },
                {
                    "heading": "Numai în scop informativ",
                    "paragraphs": [
                        "TraderMap afișează date de piață, grafice, tranzacții mari, lichidări, știri, indicatori generați de AI sau algoritmici și alte materiale analitice numai în scop informativ și educațional. Nu oferă consultanță de investiții, juridică, fiscală sau contabilă; nu conectează portofele, nu intermediază ori execută ordine și nu păstrează active."
                    ],
                },
                {
                    "heading": "Riscul pieței și al datelor",
                    "paragraphs": [
                        "Activele digitale sunt volatile și își pot pierde întreaga valoare. Datele pot fi întârziate, incomplete, traduse greșit, indisponibile sau incorecte. Indicatorii și rezultatele simulate sau istorice nu garantează performanțe viitoare. Verificați independent informațiile importante și consultați profesioniști calificați înainte de a lua decizii financiare."
                    ],
                },
                {
                    "heading": "Conținut terț",
                    "paragraphs": [
                        "Prețurile, știrile și linkurile pot proveni de la terți. Numele și mărcile lor aparțin proprietarilor respectivi. TraderMap nu controlează site-urile externe și nu răspunde pentru disponibilitatea, conținutul sau practicile lor de confidențialitate."
                    ],
                },
                {
                    "heading": "Utilizare permisă",
                    "paragraphs": [
                        "Puteți utiliza aplicațiile în scopuri personale și legale. Nu aveți voie să perturbați serviciul, să ocoliți controalele de acces, să automatizați volume abuzive de solicitări, să denaturați conținutul, să încălcați drepturi sau să utilizați aplicațiile pentru activități de piață ilegale."
                    ],
                },
                {
                    "heading": "Disponibilitate și răspundere",
                    "paragraphs": [
                        "Aplicațiile și datele sunt furnizate „în forma disponibilă”, fără promisiunea funcționării neîntrerupte sau a adecvării pentru un anumit scop. În măsura maximă permisă de lege, operatorul nu răspunde pentru pierderi din tranzacționare, profituri pierdute, date pierdute sau daune indirecte rezultate din utilizarea ori încrederea în aplicații. Drepturile care nu pot fi excluse legal rămân neafectate."
                    ],
                },
                {
                    "heading": "Modificări și contact",
                    "paragraphs": [
                        "Funcțiile și acești termeni se pot modifica. Continuarea utilizării după o actualizare înseamnă că acceptați termenii actualizați. Întrebările pot fi trimise prin canalul oficial de asistență."
                    ],
                },
            ],
        },
        "operator": {
            "title": "Informații despre operator",
            "desc": "Proprietatea oficială, domeniul serviciului și canalele de contact.",
            "sections": [
                {
                    "heading": "Dezvoltator și operator",
                    "paragraphs": [
                        "TraderMap și TraderMapTV sunt dezvoltate și operate sub numele 17ClassDeveloper prin contul GitHub 17classdeveloper-design."
                    ],
                    "items": [
                        "iOS/iPadOS: TraderMap — com.17class.TraderMap",
                        "tvOS: TraderMapTV — com.17class.TraderMapTV",
                    ],
                },
                {
                    "heading": "Domeniul serviciului",
                    "paragraphs": [
                        "Ambele aplicații sunt clienți de informare despre piețe, numai pentru citire. Operatorul nu oferă servicii de brokeraj, conectare de portofele, custodie de active, depuneri, retrageri sau executare de ordine."
                    ],
                },
                {
                    "heading": "Canale oficiale",
                    "paragraphs": [
                        "Acest site și depozitul de mai jos sunt canalele publice oficiale de informare și asistență. Informațiile despre vânzătorul din App Store și statutul de comerciant, acolo unde sunt necesare, sunt afișate de Apple în magazinul aplicabil."
                    ],
                },
                {
                    "heading": "Proprietate intelectuală",
                    "paragraphs": [
                        "Software-ul, interfața și materialele originale TraderMap sunt protejate de legislația aplicabilă privind proprietatea intelectuală. Datele de piață, conținutul articolelor, numele și mărcile terților rămân proprietatea titularilor respectivi și sunt utilizate conform permisiunilor aplicabile."
                    ],
                },
            ],
            "primary_action": "Contactați asistența tehnică",
            "secondary_action": "Vedeți depozitul",
        },
    },
    "uk": {
        "lang": "uk",
        "name": "Українська",
        "language_label": "Мова · Українська",
        "nav": {
            "home": "Огляд",
            "privacy": "Конфіденційність",
            "support": "Підтримка",
            "terms": "Умови",
            "operator": "Оператор",
        },
        "official": "Офіційна інформація TraderMap",
        "effective": f"Дата набрання чинності: {EFFECTIVE_DATE}",
        "scope": "TraderMap для iOS/iPadOS (com.17class.TraderMap) і TraderMapTV для tvOS (com.17class.TraderMapTV)",
        "footer": "Лише ринкова інформація — не інвестиційна порада й не сервіс виконання ордерів.",
        "home": {
            "title": "Крипторинок — чітко на карті.",
            "eyebrow": "Єдина політика · дві платформи Apple",
            "lede": "TraderMap показує ринкові ціни, графіки, великі угоди, ліквідації, новини та аналітичні сигнали на iPhone, iPad і Apple TV.",
            "intro": "Цей офіційний сайт містить політику конфіденційності, технічну підтримку, умови та інформацію про оператора для обох версій TraderMap.",
            "no_tracking": "Без реклами. Без сторонньої аналітики. Без відстеження.",
            "platform_title": "Створено для платформ Apple",
            "platform_desc": "Застосунок для iOS/iPadOS пропонує інтерактивний робочий простір для ринку. Застосунок для tvOS пропонує зручну для пульта панель на великому екрані. Жоден застосунок не підключає гаманець, не виконує ордери й не зберігає активи.",
        },
        "privacy": {
            "title": "Політика конфіденційності",
            "desc": "Як TraderMap обробляє інформацію в iOS, iPadOS і tvOS.",
            "sections": [
                {
                    "heading": "Сфера дії",
                    "paragraphs": [
                        "Ця політика поширюється на TraderMap для iOS та iPadOS (ідентифікатор пакета com.17class.TraderMap), TraderMapTV для tvOS (ідентифікатор пакета com.17class.TraderMapTV) і цей сайт підтримки. Обидва застосунки дотримуються однакових практик роботи з даними."
                    ],
                },
                {
                    "heading": "Дані, які ми не запитуємо",
                    "paragraphs": [
                        "TraderMap не вимагає облікового запису й не запитує ваше ім’я, адресу електронної пошти, номер телефону, поштову адресу, платіжні дані, адресу гаманця, seed-фразу або приватний ключ. Застосунки не містять рекламних SDK, сторонніх SDK аналітики чи технологій міжзастосункового відстеження."
                    ],
                },
                {
                    "heading": "Інформація, що зберігається на пристрої",
                    "paragraphs": [
                        "Застосунки локально зберігають наведену нижче інформацію, щоб налаштування й нещодавні перегляди працювали належним чином. Ця інформація не завантажується як профіль користувача."
                    ],
                    "items": [
                        "Вибір мови; налаштування звуку та гучності",
                        "Вибрані символи, пороги сповіщень і улюблені графіки",
                        "Випадковий ідентифікатор у межах застосунку, який використовується лише в середовищі розробки для підключення даних прогнозування",
                        "Короткочасно кешовані відповіді з ринковими даними та контентом",
                    ],
                },
                {
                    "heading": "Мережева обробка",
                    "paragraphs": [
                        "Для надання інформації в реальному часі застосунки підключаються до налаштованого шлюзу TraderMap і постачальників ринкових даних та контенту. Як і будь-який інтернет-сервіс, такі з’єднання неминуче розкривають IP-адресу та можуть обробляти час запиту, user agent застосунку, вибрану мову, запитувану кінцеву точку й ринкові фільтри. Поточний шлюз TraderMap тимчасово використовує IP-адресу для обмеження частоти запитів і не створює на її основі профілі користувачів.",
                        "Постачальники інфраструктури можуть обробляти обмежені журнали з’єднань для доставки, надійності та безпеки відповідно до власних умов. Відкриття оригінальної новинної статті переводить вас за межі TraderMap, і на неї поширюється політика конфіденційності видавця. Цей сайт розміщено на GitHub Pages, тому GitHub може обробляти стандартну інформацію вебзапитів відповідно до Заяви GitHub про конфіденційність.",
                    ],
                },
                {
                    "heading": "Цілі та передавання",
                    "paragraphs": [
                        "Інформація обробляється лише для надання запитаного ринкового контенту, збереження налаштувань на пристрої, захисту доступності сервісу, діагностики збоїв і виконання вимог закону. TraderMap не продає персональну інформацію й не передає її для таргетованої реклами. Постачальники послуг можуть обробляти лише те, що необхідно для роботи запитаного сервісу, і повинні забезпечувати захист відповідно до цієї політики та чинного законодавства."
                    ],
                },
                {
                    "heading": "Зберігання та ваш вибір",
                    "paragraphs": [
                        "Налаштування на пристрої зберігаються, доки ви їх не зміните, не скинете відповідне налаштування або не видалите застосунок. Кешовані відповіді є тимчасовими й можуть бути видалені застосунком або операційною системою. У еталонній реалізації тимчасові записи шлюзу для обмеження частоти запитів спливають приблизно через 60 секунд. Ви можете припинити всю мережеву обробку застосунком, видаливши його або від’єднавши від мережі."
                    ],
                    "items": [
                        "Видаліть застосунок, щоб прибрати його локальні дані",
                        "Використовуйте елементи керування в застосунку, щоб змінити мову, фільтри, обране та налаштування звуку",
                        "Зверніться до підтримки, якщо вважаєте, що сервіс має інформацію про вас, або хочете реалізувати законне право на конфіденційність",
                    ],
                },
                {
                    "heading": "Діти, передавання та безпека",
                    "paragraphs": [
                        "TraderMap є загальним інформаційним продуктом про ринок і не призначений для дітей. Постачальники мережевих послуг можуть обробляти інформацію в країнах, відмінних від вашої. У робочому середовищі TraderMap використовує HTTPS/WSS і застосовує розумні заходи захисту, однак жодна передача через інтернет не може бути гарантовано повністю безпечною."
                    ],
                },
                {
                    "heading": "Зміни та зв’язок",
                    "paragraphs": [
                        "Ми можемо оновлювати цю політику, коли змінюються функції застосунку, постачальники послуг або законодавство. Дата набрання чинності вище вказує на поточну версію. Запитання та звернення щодо конфіденційності можна надсилати через офіційний канал підтримки."
                    ],
                },
            ],
        },
        "support": {
            "title": "Технічна підтримка",
            "desc": "Допомога щодо TraderMap на iPhone, iPad і Apple TV.",
            "sections": [
                {
                    "heading": "Перш ніж повідомляти про проблему",
                    "paragraphs": [
                        "TraderMap потребує iOS/iPadOS 16 або новішої версії чи tvOS 16 або новішої версії, а для даних у реальному часі — підключення до інтернету. Джерела ринкових даних іноді можуть затримуватися або бути недоступними."
                    ],
                    "items": [
                        "Переконайтеся, що пристрій підключено до інтернету",
                        "Закрийте та знову відкрийте TraderMap",
                        "Спробуйте інший символ або сторінку",
                        "Переконайтеся, що застосунок і операційна система оновлені",
                    ],
                },
                {
                    "heading": "Що додати до звернення",
                    "paragraphs": [
                        "Створіть issue на GitHub і вкажіть версію: TraderMap (iOS/iPadOS) або TraderMapTV (tvOS). Додайте версію застосунку, модель пристрою, версію операційної системи, вибрану мову, кроки для відтворення та, за потреби, знімки екрана."
                    ],
                    "items": [
                        "Видаліть особисту або конфіденційну інформацію зі знімків екрана",
                        "Ніколи не публікуйте паролі, API-токени, seed-фрази або приватні ключі",
                        "Не публікуйте приватні торгові чи фінансові записи",
                    ],
                },
                {
                    "heading": "Канал зв’язку",
                    "paragraphs": [
                        "Технічна підтримка, загальні відгуки та запити на функції опрацьовуються через публічний трекер issue-ів репозиторію. Оператор — 17ClassDeveloper (обліковий запис GitHub: 17classdeveloper-design). Час відповіді не гарантується."
                    ],
                },
            ],
            "primary_action": "Звернутися до технічної підтримки",
            "secondary_action": "Переглянути репозиторій",
        },
        "terms": {
            "title": "Умови використання та застереження",
            "desc": "Умови, що регулюють обидва застосунки TraderMap для платформ Apple.",
            "sections": [
                {
                    "heading": "Прийняття та сфера дії",
                    "paragraphs": [
                        "Використовуючи TraderMap або TraderMapTV, ви погоджуєтеся з цими умовами. Якщо ви не погоджуєтеся, не використовуйте застосунки. Ці умови поширюються на обидва ідентифікатори пакетів, наведені вище."
                    ],
                },
                {
                    "heading": "Лише інформаційна мета",
                    "paragraphs": [
                        "TraderMap відображає ринкові дані, графіки, великі угоди, ліквідації, новини, згенеровані ШІ або алгоритмічні індикатори й інший аналітичний контент виключно з інформаційною та освітньою метою. Він не надає інвестиційних, юридичних, податкових чи бухгалтерських консультацій; не підключає гаманець, не посередничає та не виконує ордери й не зберігає активи."
                    ],
                },
                {
                    "heading": "Ризик ринку та даних",
                    "paragraphs": [
                        "Цифрові активи є волатильними й можуть повністю втратити вартість. Дані можуть бути затриманими, неповними, неправильно перекладеними, недоступними або неточними. Індикатори, змодельовані чи історичні результати не гарантують майбутньої ефективності. Самостійно перевіряйте важливу інформацію та консультуйтеся з кваліфікованими фахівцями перед прийняттям фінансових рішень."
                    ],
                },
                {
                    "heading": "Сторонній контент",
                    "paragraphs": [
                        "Ціни, новини та посилання можуть надходити від третіх сторін. Їхні назви й торговельні марки належать відповідним власникам. TraderMap не контролює зовнішні сайти й не відповідає за їх доступність, контент або практики конфіденційності."
                    ],
                },
                {
                    "heading": "Дозволене використання",
                    "paragraphs": [
                        "Ви можете використовувати застосунки в особистих і законних цілях. Заборонено порушувати роботу сервісу, обходити контроль доступу, автоматизувати зловмисні обсяги запитів, спотворювати контент, порушувати права або використовувати застосунки для незаконної ринкової діяльності."
                    ],
                },
                {
                    "heading": "Доступність і відповідальність",
                    "paragraphs": [
                        "Застосунки й дані надаються «як доступно» без обіцянки безперервної роботи чи придатності для певної мети. У максимально дозволеному законом обсязі оператор не відповідає за торгові збитки, втрачений прибуток, втрачені дані або непрямі збитки, що виникли через використання застосунків чи довіру до них. Права, які не можна законно виключити, залишаються чинними."
                    ],
                },
                {
                    "heading": "Зміни та зв’язок",
                    "paragraphs": [
                        "Функції та ці умови можуть змінюватися. Подальше використання після оновлення означає прийняття оновлених умов. Запитання можна надсилати через офіційний канал підтримки."
                    ],
                },
            ],
        },
        "operator": {
            "title": "Інформація про оператора",
            "desc": "Офіційна належність, обсяг сервісу та канали зв’язку.",
            "sections": [
                {
                    "heading": "Розробник і оператор",
                    "paragraphs": [
                        "TraderMap і TraderMapTV розробляються та експлуатуються під назвою 17ClassDeveloper через обліковий запис GitHub 17classdeveloper-design."
                    ],
                    "items": [
                        "iOS/iPadOS: TraderMap — com.17class.TraderMap",
                        "tvOS: TraderMapTV — com.17class.TraderMapTV",
                    ],
                },
                {
                    "heading": "Обсяг сервісу",
                    "paragraphs": [
                        "Обидва застосунки є клієнтами ринкової інформації лише для читання. Оператор не надає брокерських послуг, підключення гаманців, зберігання активів, внесення коштів, виведення коштів або виконання ордерів."
                    ],
                },
                {
                    "heading": "Офіційні канали",
                    "paragraphs": [
                        "Цей сайт і репозиторій нижче є офіційними публічними каналами інформації та підтримки. Інформацію про продавця в App Store і статус трейдера, де це вимагається, Apple відображає у відповідній вітрині."
                    ],
                },
                {
                    "heading": "Інтелектуальна власність",
                    "paragraphs": [
                        "Програмне забезпечення, інтерфейс та оригінальні матеріали TraderMap захищені чинним законодавством про інтелектуальну власність. Сторонні ринкові дані, вміст статей, назви й торговельні марки залишаються власністю відповідних правовласників і використовуються згідно з наданими дозволами."
                    ],
                },
            ],
            "primary_action": "Звернутися до технічної підтримки",
            "secondary_action": "Переглянути репозиторій",
        },
    },
    "ru": {
        "lang": "ru",
        "name": "Русский",
        "language_label": "Язык · Русский",
        "nav": {
            "home": "Обзор",
            "privacy": "Конфиденциальность",
            "support": "Поддержка",
            "terms": "Условия",
            "operator": "Оператор",
        },
        "official": "Официальная информация TraderMap",
        "effective": f"Дата вступления в силу: {EFFECTIVE_DATE}",
        "scope": "TraderMap для iOS/iPadOS (com.17class.TraderMap) и TraderMapTV для tvOS (com.17class.TraderMapTV)",
        "footer": "Только рыночная информация — не инвестиционная рекомендация и не сервис исполнения ордеров.",
        "home": {
            "title": "Крипторынок — наглядно и понятно.",
            "eyebrow": "Единая политика · две платформы Apple",
            "lede": "TraderMap показывает рыночные цены, графики, крупные сделки, ликвидации, новости и аналитические сигналы на iPhone, iPad и Apple TV.",
            "intro": "На этом официальном сайте размещены политика конфиденциальности, техническая поддержка, условия и информация об операторе для обеих версий TraderMap.",
            "no_tracking": "Без рекламы. Без сторонней аналитики. Без отслеживания.",
            "platform_title": "Создано для платформ Apple",
            "platform_desc": "Приложение для iOS/iPadOS предоставляет интерактивное рабочее пространство для рынка. Приложение для tvOS предлагает удобную для пульта панель на большом экране. Ни одно из приложений не подключает кошелёк, не исполняет ордера и не хранит активы.",
        },
        "privacy": {
            "title": "Политика конфиденциальности",
            "desc": "Как TraderMap обрабатывает информацию в iOS, iPadOS и tvOS.",
            "sections": [
                {
                    "heading": "Область применения",
                    "paragraphs": [
                        "Настоящая политика распространяется на TraderMap для iOS и iPadOS (идентификатор пакета com.17class.TraderMap), TraderMapTV для tvOS (идентификатор пакета com.17class.TraderMapTV) и этот сайт поддержки. Оба приложения используют одинаковые методы работы с данными."
                    ],
                },
                {
                    "heading": "Данные, которые мы не запрашиваем",
                    "paragraphs": [
                        "TraderMap не требует учётной записи и не запрашивает имя, адрес электронной почты, номер телефона, почтовый адрес, платёжные данные, адрес кошелька, seed-фразу или закрытый ключ. Приложения не содержат рекламных SDK, сторонних SDK аналитики или технологий межприложенческого отслеживания."
                    ],
                },
                {
                    "heading": "Информация, хранящаяся на устройстве",
                    "paragraphs": [
                        "Приложения локально хранят следующую информацию, чтобы настройки и недавние просмотры работали должным образом. Эти данные не загружаются в виде профиля пользователя."
                    ],
                    "items": [
                        "Выбранный язык; настройки звука и громкости",
                        "Выбранные символы, пороги уведомлений и избранные графики",
                        "Случайный идентификатор в рамках приложения, используемый только в среде разработки для подключения данных прогнозирования",
                        "Кратковременно кэшируемые ответы с рыночными данными и контентом",
                    ],
                },
                {
                    "heading": "Сетевая обработка",
                    "paragraphs": [
                        "Для предоставления информации в реальном времени приложения подключаются к настроенному шлюзу TraderMap и поставщикам рыночных данных и контента. Как и любой интернет-сервис, такие соединения неизбежно раскрывают IP-адрес и могут обрабатывать время запроса, user agent приложения, выбранный язык, запрошенную конечную точку и рыночные фильтры. Текущий шлюз TraderMap временно использует IP-адрес для ограничения частоты запросов и не создаёт на его основе профили пользователей.",
                        "Поставщики инфраструктуры могут обрабатывать ограниченные журналы соединений для доставки, надёжности и безопасности в соответствии со своими условиями. При открытии оригинальной новостной статьи вы покидаете TraderMap, и дальнейшая обработка регулируется политикой конфиденциальности издателя. Этот сайт размещён на GitHub Pages, поэтому GitHub может обрабатывать стандартную информацию веб-запросов в соответствии с Заявлением GitHub о конфиденциальности.",
                    ],
                },
                {
                    "heading": "Цели и передача",
                    "paragraphs": [
                        "Информация обрабатывается только для предоставления запрошенного рыночного контента, сохранения настроек на устройстве, защиты доступности сервиса, диагностики сбоев и соблюдения закона. TraderMap не продаёт персональную информацию и не передаёт её для таргетированной рекламы. Поставщики услуг могут обрабатывать только то, что необходимо для работы запрошенного сервиса, и обязаны обеспечивать защиту в соответствии с этой политикой и применимым законодательством."
                    ],
                },
                {
                    "heading": "Хранение и ваш выбор",
                    "paragraphs": [
                        "Настройки на устройстве сохраняются, пока вы их не измените, не сбросите соответствующую настройку или не удалите приложение. Кэшированные ответы носят временный характер и могут быть удалены приложением или операционной системой. Во вспомогательной реализации временные записи шлюза для ограничения частоты запросов истекают примерно через 60 секунд. Вы можете прекратить всю сетевую обработку приложением, удалив его или отключив от сети."
                    ],
                    "items": [
                        "Удалите приложение, чтобы убрать его локальные данные",
                        "Используйте элементы управления в приложении для изменения языка, фильтров, избранного и настроек звука",
                        "Обратитесь в поддержку, если считаете, что сервис располагает информацией о вас, или хотите реализовать законное право на конфиденциальность",
                    ],
                },
                {
                    "heading": "Дети, передача и безопасность",
                    "paragraphs": [
                        "TraderMap является общим информационным продуктом о рынке и не предназначен для детей. Поставщики сетевых услуг могут обрабатывать информацию в странах, отличных от вашей. В рабочей среде TraderMap использует HTTPS/WSS и применяет разумные меры защиты, однако ни одна передача через интернет не может быть гарантированно полностью безопасной."
                    ],
                },
                {
                    "heading": "Изменения и связь",
                    "paragraphs": [
                        "Мы можем обновлять эту политику при изменении функций приложения, поставщиков услуг или законодательства. Указанная выше дата вступления в силу определяет текущую версию. Вопросы и запросы о конфиденциальности можно направлять через официальный канал поддержки."
                    ],
                },
            ],
        },
        "support": {
            "title": "Техническая поддержка",
            "desc": "Помощь по TraderMap на iPhone, iPad и Apple TV.",
            "sections": [
                {
                    "heading": "Перед сообщением о проблеме",
                    "paragraphs": [
                        "Для TraderMap требуется iOS/iPadOS 16 или новее либо tvOS 16 или новее, а для данных в реальном времени — подключение к интернету. Источники рыночных данных иногда могут задерживаться или быть недоступными."
                    ],
                    "items": [
                        "Убедитесь, что устройство подключено к интернету",
                        "Закройте и снова откройте TraderMap",
                        "Попробуйте другой символ или страницу",
                        "Убедитесь, что приложение и операционная система обновлены",
                    ],
                },
                {
                    "heading": "Что указать",
                    "paragraphs": [
                        "Создайте issue на GitHub и укажите версию: TraderMap (iOS/iPadOS) или TraderMapTV (tvOS). Добавьте версию приложения, модель устройства, версию операционной системы, выбранный язык, шаги для воспроизведения и при необходимости снимки экрана."
                    ],
                    "items": [
                        "Удалите личную или конфиденциальную информацию со снимков экрана",
                        "Никогда не публикуйте пароли, API-токены, seed-фразы или закрытые ключи",
                        "Не публикуйте частные торговые или финансовые записи",
                    ],
                },
                {
                    "heading": "Канал связи",
                    "paragraphs": [
                        "Техническая поддержка, общие отзывы и запросы функций обрабатываются через публичный трекер issue-ов репозитория. Оператор — 17ClassDeveloper (учётная запись GitHub: 17classdeveloper-design). Срок ответа не гарантируется."
                    ],
                },
            ],
            "primary_action": "Связаться с технической поддержкой",
            "secondary_action": "Открыть репозиторий",
        },
        "terms": {
            "title": "Условия использования и отказ от ответственности",
            "desc": "Условия для обоих приложений TraderMap на платформах Apple.",
            "sections": [
                {
                    "heading": "Принятие и область действия",
                    "paragraphs": [
                        "Используя TraderMap или TraderMapTV, вы соглашаетесь с настоящими условиями. Если вы не согласны, не используйте приложения. Эти условия распространяются на оба идентификатора пакета, указанные выше."
                    ],
                },
                {
                    "heading": "Только в информационных целях",
                    "paragraphs": [
                        "TraderMap показывает рыночные данные, графики, крупные сделки, ликвидации, новости, созданные ИИ или алгоритмические индикаторы и другой аналитический контент исключительно в информационных и образовательных целях. Он не предоставляет инвестиционные, юридические, налоговые или бухгалтерские консультации; не подключает кошелёк, не посредничает и не исполняет ордера и не хранит активы."
                    ],
                },
                {
                    "heading": "Риск рынка и данных",
                    "paragraphs": [
                        "Цифровые активы волатильны и могут полностью потерять стоимость. Данные могут быть задержанными, неполными, неверно переведёнными, недоступными или неточными. Индикаторы, смоделированные или исторические результаты не гарантируют будущую доходность. Самостоятельно проверяйте важную информацию и консультируйтесь с квалифицированными специалистами до принятия финансовых решений."
                    ],
                },
                {
                    "heading": "Сторонний контент",
                    "paragraphs": [
                        "Цены, новости и ссылки могут поступать от третьих лиц. Их названия и товарные знаки принадлежат соответствующим владельцам. TraderMap не контролирует внешние сайты и не отвечает за их доступность, контент или методы обеспечения конфиденциальности."
                    ],
                },
                {
                    "heading": "Разрешённое использование",
                    "paragraphs": [
                        "Вы можете использовать приложения в личных законных целях. Запрещается нарушать работу сервиса, обходить контроль доступа, автоматизировать вредоносные объёмы запросов, искажать контент, нарушать права или использовать приложения для незаконной рыночной деятельности."
                    ],
                },
                {
                    "heading": "Доступность и ответственность",
                    "paragraphs": [
                        "Приложения и данные предоставляются «по мере доступности» без обещания бесперебойной работы или пригодности для конкретной цели. В максимальной степени, разрешённой законом, оператор не несёт ответственности за торговые убытки, упущенную прибыль, утраченные данные или косвенный ущерб, возникшие в результате использования приложений или доверия к ним. Права, которые нельзя законно исключить, сохраняются."
                    ],
                },
                {
                    "heading": "Изменения и связь",
                    "paragraphs": [
                        "Функции и настоящие условия могут изменяться. Продолжение использования после обновления означает принятие обновлённых условий. Вопросы можно направлять через официальный канал поддержки."
                    ],
                },
            ],
        },
        "operator": {
            "title": "Информация об операторе",
            "desc": "Официальная принадлежность, область сервиса и каналы связи.",
            "sections": [
                {
                    "heading": "Разработчик и оператор",
                    "paragraphs": [
                        "TraderMap и TraderMapTV разрабатываются и управляются под именем 17ClassDeveloper через учётную запись GitHub 17classdeveloper-design."
                    ],
                    "items": [
                        "iOS/iPadOS: TraderMap — com.17class.TraderMap",
                        "tvOS: TraderMapTV — com.17class.TraderMapTV",
                    ],
                },
                {
                    "heading": "Область сервиса",
                    "paragraphs": [
                        "Оба приложения являются клиентами рыночной информации только для чтения. Оператор не предоставляет брокерские услуги, подключение кошельков, хранение активов, внесение средств, вывод средств или исполнение ордеров."
                    ],
                },
                {
                    "heading": "Официальные каналы",
                    "paragraphs": [
                        "Этот сайт и указанный ниже репозиторий являются официальными публичными каналами информации и поддержки. Информация о продавце в App Store и статусе трейдера, где это требуется, отображается Apple в соответствующей витрине."
                    ],
                },
                {
                    "heading": "Интеллектуальная собственность",
                    "paragraphs": [
                        "Программное обеспечение, интерфейс и оригинальные материалы TraderMap защищены применимым законодательством об интеллектуальной собственности. Сторонние рыночные данные, содержимое статей, названия и товарные знаки остаются собственностью соответствующих правообладателей и используются согласно применимым разрешениям."
                    ],
                },
            ],
            "primary_action": "Связаться с технической поддержкой",
            "secondary_action": "Открыть репозиторий",
        },
    },
    "id": {
        "lang": "id",
        "name": "Bahasa Indonesia",
        "language_label": "Bahasa · Bahasa Indonesia",
        "nav": {
            "home": "Ikhtisar",
            "privacy": "Privasi",
            "support": "Dukungan",
            "terms": "Ketentuan",
            "operator": "Operator",
        },
        "official": "Informasi resmi TraderMap",
        "effective": f"Tanggal berlaku: {EFFECTIVE_DATE}",
        "scope": "TraderMap untuk iOS/iPadOS (com.17class.TraderMap) dan TraderMapTV untuk tvOS (com.17class.TraderMapTV)",
        "footer": "Hanya informasi pasar — bukan nasihat investasi atau layanan pelaksanaan order.",
        "home": {
            "title": "Pasar kripto, dipetakan dengan jelas.",
            "eyebrow": "Satu kebijakan · dua platform Apple",
            "lede": "TraderMap menyajikan harga pasar, grafik, transaksi besar, likuidasi, berita, dan sinyal analitis di iPhone, iPad, dan Apple TV.",
            "intro": "Situs resmi ini menyediakan kebijakan privasi, dukungan teknis, ketentuan, dan informasi operator untuk kedua versi TraderMap.",
            "no_tracking": "Tanpa iklan. Tanpa analitik pihak ketiga. Tanpa pelacakan.",
            "platform_title": "Dirancang untuk platform Apple",
            "platform_desc": "Aplikasi iOS/iPadOS menyediakan ruang kerja pasar interaktif. Aplikasi tvOS menyediakan dasbor layar besar yang ramah kendali jarak jauh. Keduanya tidak menghubungkan dompet, melaksanakan order, atau menyimpan aset.",
        },
        "privacy": {
            "title": "Kebijakan Privasi",
            "desc": "Cara TraderMap menangani informasi di iOS, iPadOS, dan tvOS.",
            "sections": [
                {
                    "heading": "Cakupan",
                    "paragraphs": [
                        "Kebijakan ini berlaku untuk TraderMap bagi iOS dan iPadOS (ID bundel com.17class.TraderMap), TraderMapTV bagi tvOS (ID bundel com.17class.TraderMapTV), serta situs dukungan ini. Kedua aplikasi mengikuti praktik data yang sama."
                    ],
                },
                {
                    "heading": "Data yang tidak kami minta",
                    "paragraphs": [
                        "TraderMap tidak memerlukan akun dan tidak meminta nama, alamat email, nomor telepon, alamat pos, informasi pembayaran, alamat dompet, seed phrase, atau kunci privat Anda. Aplikasi tidak memuat SDK iklan, SDK analitik pihak ketiga, atau teknologi pelacakan lintas aplikasi."
                    ],
                },
                {
                    "heading": "Informasi yang disimpan di perangkat",
                    "paragraphs": [
                        "Aplikasi menyimpan informasi berikut secara lokal agar pengaturan dan tampilan terkini berfungsi sebagaimana mestinya. Informasi ini tidak diunggah sebagai profil pengguna."
                    ],
                    "items": [
                        "Pilihan bahasa; pengaturan suara dan volume",
                        "Simbol yang dipilih, ambang peringatan, dan grafik favorit",
                        "Pengenal acak yang terbatas pada aplikasi dan digunakan oleh koneksi data prediksi khusus pengembangan",
                        "Respons pasar dan konten yang disimpan sementara dalam cache",
                    ],
                },
                {
                    "heading": "Pemrosesan jaringan",
                    "paragraphs": [
                        "Untuk menyediakan informasi langsung, aplikasi terhubung ke gateway TraderMap yang dikonfigurasi serta penyedia pasar dan konten. Seperti layanan internet lainnya, koneksi tersebut secara inheren menampilkan alamat IP dan dapat memproses waktu permintaan, user agent aplikasi, bahasa yang dipilih, endpoint yang diminta, dan filter pasar. Gateway TraderMap saat ini menggunakan alamat IP secara sementara untuk pembatasan laju dan tidak membuat profil pengguna darinya.",
                        "Penyedia infrastruktur dapat memproses log koneksi terbatas untuk pengiriman, keandalan, dan keamanan berdasarkan ketentuan mereka sendiri. Membuka artikel berita asli akan membawa Anda keluar dari TraderMap dan tunduk pada kebijakan privasi penerbit tersebut. Situs ini dihosting oleh GitHub Pages, sehingga GitHub dapat memproses informasi permintaan web standar berdasarkan Pernyataan Privasi GitHub.",
                    ],
                },
                {
                    "heading": "Tujuan dan pembagian",
                    "paragraphs": [
                        "Informasi diproses hanya untuk menyampaikan konten pasar yang diminta, mengingat preferensi di perangkat, menjaga ketersediaan layanan, mendiagnosis kegagalan, dan mematuhi hukum. TraderMap tidak menjual informasi pribadi dan tidak membagikannya untuk iklan bertarget. Penyedia layanan hanya dapat memproses hal yang diperlukan untuk mengoperasikan layanan yang diminta dan wajib memberikan perlindungan sesuai kebijakan ini serta hukum yang berlaku."
                    ],
                },
                {
                    "heading": "Penyimpanan dan pilihan Anda",
                    "paragraphs": [
                        "Preferensi di perangkat tetap tersimpan sampai Anda mengubahnya, mereset pengaturan terkait, atau menghapus aplikasi. Respons cache bersifat sementara dan dapat dihapus oleh aplikasi atau sistem operasi. Entri pembatasan laju gateway yang bersifat sementara kedaluwarsa setelah sekitar 60 detik dalam implementasi referensi. Anda dapat menghentikan seluruh pemrosesan jaringan aplikasi dengan menghapus aplikasi atau memutuskan koneksinya dari jaringan."
                    ],
                    "items": [
                        "Hapus aplikasi untuk menghapus data lokalnya",
                        "Gunakan kontrol dalam aplikasi untuk mengubah bahasa, filter, favorit, dan pengaturan suara",
                        "Hubungi dukungan jika Anda yakin layanan memiliki informasi tentang Anda atau ingin menggunakan hak privasi berdasarkan hukum",
                    ],
                },
                {
                    "heading": "Anak-anak, transfer, dan keamanan",
                    "paragraphs": [
                        "TraderMap adalah produk informasi pasar umum dan tidak ditujukan bagi anak-anak. Penyedia jaringan dapat memproses informasi di negara selain negara Anda. TraderMap menggunakan HTTPS/WSS dalam produksi dan menerapkan perlindungan yang wajar, tetapi tidak ada transmisi internet yang dapat dijamin sepenuhnya aman."
                    ],
                },
                {
                    "heading": "Perubahan dan kontak",
                    "paragraphs": [
                        "Kami dapat memperbarui kebijakan ini ketika fitur aplikasi, penyedia layanan, atau hukum berubah. Tanggal berlaku di atas menunjukkan versi saat ini. Pertanyaan dan permintaan privasi dapat diajukan melalui saluran dukungan resmi."
                    ],
                },
            ],
        },
        "support": {
            "title": "Dukungan Teknis",
            "desc": "Bantuan untuk TraderMap di iPhone, iPad, dan Apple TV.",
            "sections": [
                {
                    "heading": "Sebelum melaporkan masalah",
                    "paragraphs": [
                        "TraderMap memerlukan iOS/iPadOS 16 atau yang lebih baru, atau tvOS 16 atau yang lebih baru, serta koneksi internet untuk data langsung. Sumber pasar terkadang dapat tertunda atau tidak tersedia."
                    ],
                    "items": [
                        "Pastikan perangkat terhubung ke internet",
                        "Tutup lalu buka kembali TraderMap",
                        "Coba simbol atau halaman lain",
                        "Pastikan aplikasi dan sistem operasi Anda sudah diperbarui",
                    ],
                },
                {
                    "heading": "Informasi yang perlu disertakan",
                    "paragraphs": [
                        "Buat issue GitHub dan sebutkan versi yang digunakan: TraderMap (iOS/iPadOS) atau TraderMapTV (tvOS). Sertakan versi aplikasi, model perangkat, versi sistem operasi, bahasa yang dipilih, langkah reproduksi, dan tangkapan layar jika bermanfaat."
                    ],
                    "items": [
                        "Hapus informasi pribadi atau rahasia dari tangkapan layar",
                        "Jangan pernah memposting kata sandi, token API, seed phrase, atau kunci privat",
                        "Jangan memposting catatan perdagangan atau keuangan pribadi",
                    ],
                },
                {
                    "heading": "Saluran kontak",
                    "paragraphs": [
                        "Dukungan teknis, masukan umum, dan permintaan fitur ditangani melalui pelacak issue publik repositori. Operatornya adalah 17ClassDeveloper (akun GitHub: 17classdeveloper-design). Waktu tanggapan tidak dijamin."
                    ],
                },
            ],
            "primary_action": "Hubungi dukungan teknis",
            "secondary_action": "Lihat repositori",
        },
        "terms": {
            "title": "Ketentuan Penggunaan & Penafian",
            "desc": "Ketentuan yang mengatur kedua aplikasi TraderMap untuk platform Apple.",
            "sections": [
                {
                    "heading": "Penerimaan dan cakupan",
                    "paragraphs": [
                        "Dengan menggunakan TraderMap atau TraderMapTV, Anda menyetujui ketentuan ini. Jika tidak setuju, jangan gunakan aplikasi. Ketentuan ini berlaku untuk kedua ID bundel yang tercantum di atas."
                    ],
                },
                {
                    "heading": "Hanya untuk informasi",
                    "paragraphs": [
                        "TraderMap menampilkan data pasar, grafik, transaksi besar, likuidasi, berita, indikator yang dihasilkan AI atau algoritme, dan konten analitis lainnya hanya untuk tujuan informasi dan pendidikan. TraderMap tidak memberikan nasihat investasi, hukum, pajak, atau akuntansi; tidak menghubungkan dompet, memperantarai atau melaksanakan order, dan tidak menyimpan aset."
                    ],
                },
                {
                    "heading": "Risiko pasar dan data",
                    "paragraphs": [
                        "Aset digital bersifat volatil dan dapat kehilangan seluruh nilainya. Data dapat terlambat, tidak lengkap, salah terjemah, tidak tersedia, atau tidak akurat. Indikator serta hasil simulasi atau historis tidak menjamin kinerja di masa mendatang. Verifikasi informasi penting secara mandiri dan konsultasikan dengan profesional yang berkualifikasi sebelum membuat keputusan keuangan."
                    ],
                },
                {
                    "heading": "Konten pihak ketiga",
                    "paragraphs": [
                        "Harga, berita, dan tautan dapat berasal dari pihak ketiga. Nama dan merek mereka dimiliki oleh pemilik masing-masing. TraderMap tidak mengendalikan situs eksternal dan tidak bertanggung jawab atas ketersediaan, konten, atau praktik privasinya."
                    ],
                },
                {
                    "heading": "Penggunaan yang diizinkan",
                    "paragraphs": [
                        "Anda dapat menggunakan aplikasi untuk tujuan pribadi yang sah. Anda tidak boleh mengganggu layanan, melewati kontrol akses, mengotomatiskan volume permintaan yang menyalahgunakan layanan, menyalahartikan konten, melanggar hak, atau menggunakan aplikasi untuk aktivitas pasar yang melanggar hukum."
                    ],
                },
                {
                    "heading": "Ketersediaan dan tanggung jawab",
                    "paragraphs": [
                        "Aplikasi dan data disediakan “sebagaimana tersedia” tanpa janji pengoperasian tanpa gangguan atau kesesuaian untuk tujuan tertentu. Sejauh diizinkan hukum, operator tidak bertanggung jawab atas kerugian perdagangan, hilangnya keuntungan, hilangnya data, atau kerugian tidak langsung yang timbul dari penggunaan atau ketergantungan pada aplikasi. Hak yang secara hukum tidak dapat dikecualikan tetap berlaku."
                    ],
                },
                {
                    "heading": "Perubahan dan kontak",
                    "paragraphs": [
                        "Fitur dan ketentuan ini dapat berubah. Penggunaan berkelanjutan setelah pembaruan berarti Anda menerima ketentuan yang diperbarui. Pertanyaan dapat diajukan melalui saluran dukungan resmi."
                    ],
                },
            ],
        },
        "operator": {
            "title": "Informasi Operator",
            "desc": "Kepemilikan resmi, cakupan layanan, dan saluran kontak.",
            "sections": [
                {
                    "heading": "Pengembang dan operator",
                    "paragraphs": [
                        "TraderMap dan TraderMapTV dikembangkan dan dioperasikan atas nama 17ClassDeveloper melalui akun GitHub 17classdeveloper-design."
                    ],
                    "items": [
                        "iOS/iPadOS: TraderMap — com.17class.TraderMap",
                        "tvOS: TraderMapTV — com.17class.TraderMapTV",
                    ],
                },
                {
                    "heading": "Cakupan layanan",
                    "paragraphs": [
                        "Kedua aplikasi merupakan klien informasi pasar hanya-baca. Operator tidak menyediakan jasa pialang, koneksi dompet, penyimpanan aset, deposit, penarikan, atau pelaksanaan order."
                    ],
                },
                {
                    "heading": "Saluran resmi",
                    "paragraphs": [
                        "Situs ini dan repositori di bawah merupakan saluran informasi publik dan dukungan resmi. Informasi penjual App Store dan status pedagang, jika diwajibkan, ditampilkan oleh Apple di etalase yang berlaku."
                    ],
                },
                {
                    "heading": "Kekayaan intelektual",
                    "paragraphs": [
                        "Perangkat lunak, antarmuka, dan materi asli TraderMap dilindungi oleh hukum kekayaan intelektual yang berlaku. Data pasar pihak ketiga, konten artikel, nama, dan merek tetap menjadi milik pemiliknya masing-masing dan digunakan sesuai izin yang berlaku."
                    ],
                },
            ],
            "primary_action": "Hubungi dukungan teknis",
            "secondary_action": "Lihat repositori",
        },
    },
}

TEXTS.update(EXTRA_TEXTS)


def page_suffix(page: str) -> str:
    return "" if page == "home" else f"{page}/"


def alternate_links(page: str) -> str:
    suffix = page_suffix(page)
    lines = [
        f'  <link rel="alternate" hreflang="{html_lang}" href="{SITE}/{slug}/{suffix}">'
        for slug, html_lang, _name, _rtl in ALL_LANGUAGES
    ]
    lines.append(
        f'  <link rel="alternate" hreflang="x-default" href="{SITE}/en/{suffix}">'
    )
    return "\n".join(lines) + "\n"


def language_menu(current_slug: str, page: str) -> str:
    suffix = page_suffix(page)
    links = []
    for slug, html_lang, name, rtl in ALL_LANGUAGES:
        current = ' aria-current="true"' if slug == current_slug else ""
        direction = ' dir="rtl"' if rtl else ""
        links.append(
            f'<a lang="{html_lang}"{direction} href="{BASE}/{slug}/{suffix}"{current}>{name}</a>'
        )
    return "<div>" + "".join(links) + "</div>"


def nav(data: dict, slug: str, current_page: str) -> str:
    links = []
    for page in ("home", "privacy", "support", "terms", "operator"):
        current = ' aria-current="page"' if page == current_page else ""
        suffix = page_suffix(page)
        links.append(
            f'<a{current} href="{BASE}/{slug}/{suffix}">{escape(data["nav"][page])}</a>'
        )
    return "".join(links)


def render_sections(sections: list[dict]) -> str:
    rendered = []
    for index, section in enumerate(sections, 1):
        paragraphs = "".join(
            f"<p>{escape(paragraph)}</p>" for paragraph in section.get("paragraphs", [])
        )
        items = section.get("items", [])
        item_html = ""
        if items:
            item_html = "<ul>" + "".join(
                f"<li>{escape(item)}</li>" for item in items
            ) + "</ul>"
        rendered.append(
            f'''  <section class="policy-section" id="section-{index}">
  <div class="section-number">{index:02d}</div>
  <div><h2>{escape(section["heading"])}</h2>{paragraphs}{item_html}</div>
</section>'''
        )
    return "\n".join(rendered)


def head(data: dict, slug: str, page: str, title: str, description: str) -> str:
    suffix = page_suffix(page)
    direction = ' dir="rtl"' if slug == "ar" else ""
    return f'''<!doctype html>
<html lang="{data["lang"]}"{direction}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <meta name="theme-color" content="#07111f">
  <title>{escape(title)} · TraderMap</title>
  <meta name="description" content="{escape(description, quote=True)}">
  <link rel="canonical" href="{SITE}/{slug}/{suffix}">
{alternate_links(page)}  <link rel="icon" href="{BASE}/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{BASE}/assets/site.css">
</head>'''


def footer(data: dict) -> str:
    return f'''<footer><p>{escape(data["footer"])}</p><p>© 2026 17ClassDeveloper · <a href="https://github.com/17classdeveloper-design/TraderMap">GitHub</a></p></footer>'''


def render_home(slug: str, data: dict) -> str:
    h = data["home"]
    cards = []
    for page in ("privacy", "support", "terms", "operator"):
        doc = data[page]
        cards.append(
            f'<a class="link-card" href="{BASE}/{slug}/{page}/"><span>{escape(data["nav"][page])}</span><strong>{escape(doc["title"])}</strong><p>{escape(doc["desc"])}</p><b aria-hidden="true">↗</b></a>'
        )
    return f'''{head(data, slug, "home", h["title"], h["lede"])}
<body>
<div class="shell">
<header class="site-header">
  <a class="brand" href="{BASE}/{slug}/" aria-label="TraderMap"><span class="brand-mark">TM</span><span>TraderMap</span></a>
  <nav aria-label="Primary">{nav(data, slug, "home")}</nav>
</header>
<main>
  <section class="hero">
    <div><div class="eyebrow">{escape(h["eyebrow"])}</div><h1>{escape(h["title"])}</h1><p class="lede">{escape(h["lede"])}</p><p>{escape(h["intro"])}</p><div class="actions"><a class="button primary" href="{BASE}/{slug}/privacy/">{escape(data["nav"]["privacy"])}</a><a class="button" href="{BASE}/{slug}/support/">{escape(data["nav"]["support"])}</a></div></div>
    <div class="signal-card"><div class="signal-grid"></div><span>BTC · ETH · SOL · XRP</span><strong>MARKET PULSE</strong><small>{escape(h["no_tracking"])}</small></div>
  </section>
  <section class="platform-card"><div><span class="platform-icon"></span></div><div><h2>{escape(h["platform_title"])}</h2><p>{escape(h["platform_desc"])}</p><div class="bundle"><code>com.17class.TraderMap</code><code>com.17class.TraderMapTV</code></div></div></section>
  <section class="link-grid">{"".join(cards)}</section>
  <div class="home-language"><details class="language"><summary>{escape(data["language_label"])}</summary>{language_menu(slug, "home")}</details></div>
</main>
{footer(data)}
</div>
</body>
</html>
'''


def render_document(slug: str, data: dict, page: str) -> str:
    doc = data[page]
    actions = ""
    if page in {"support", "operator"}:
        actions = f'''  <div class="actions"><a class="button primary" href="https://github.com/17classdeveloper-design/TraderMap/issues/new/choose">{escape(doc["primary_action"])}</a><a class="button" href="https://github.com/17classdeveloper-design/TraderMap">{escape(doc["secondary_action"])}</a></div>'''
    return f'''{head(data, slug, page, doc["title"], doc["desc"])}
<body>
<div class="shell">
<header class="site-header">
  <a class="brand" href="{BASE}/{slug}/" aria-label="TraderMap"><span class="brand-mark">TM</span><span>TraderMap</span></a>
  <nav aria-label="Primary">{nav(data, slug, page)}</nav>
</header>
<main>
  <div class="eyebrow">{escape(data["official"])}</div>
  <div class="document-heading"><div><h1>{escape(doc["title"])}</h1><p>{escape(doc["desc"])}</p></div><details class="language"><summary>{escape(data["language_label"])}</summary>{language_menu(slug, page)}</details></div>
  <div class="scope"><span>{escape(data["effective"])}</span><span>{escape(data["scope"])}</span></div>
{render_sections(doc["sections"])}
{actions}
</main>
{footer(data)}
</div>
</body>
</html>
'''


def update_existing_pages() -> None:
    alternate_pattern = re.compile(
        r'  <link rel="alternate" hreflang="en".*?'
        r'  <link rel="alternate" hreflang="x-default"[^\n]*\n',
        re.DOTALL,
    )
    menu_pattern = re.compile(
        r'(<details class="language"><summary>.*?</summary>)<div>.*?</div>(</details>)'
    )
    for slug in EXISTING_SLUGS:
        for html_file in sorted((ROOT / slug).rglob("index.html")):
            relative = html_file.relative_to(ROOT / slug)
            page = "home" if len(relative.parts) == 1 else relative.parts[0]
            source = html_file.read_text(encoding="utf-8")
            source, count = alternate_pattern.subn(alternate_links(page), source, count=1)
            if count != 1:
                raise RuntimeError(f"Could not update hreflang block in {html_file}")
            source, count = menu_pattern.subn(
                lambda match: match.group(1)
                + language_menu(slug, page)
                + match.group(2),
                source,
                count=1,
            )
            if count != 1:
                raise RuntimeError(f"Could not update language menu in {html_file}")
            html_file.write_text(source, encoding="utf-8")


def write_new_pages() -> None:
    for slug, data in TEXTS.items():
        (ROOT / slug).mkdir(parents=True, exist_ok=True)
        (ROOT / slug / "index.html").write_text(
            render_home(slug, data), encoding="utf-8"
        )
        for page in ("privacy", "support", "terms", "operator"):
            directory = ROOT / slug / page
            directory.mkdir(parents=True, exist_ok=True)
            (directory / "index.html").write_text(
                render_document(slug, data, page), encoding="utf-8"
            )


def write_root_index() -> None:
    links = []
    for slug, html_lang, name, rtl in ALL_LANGUAGES:
        direction = ' dir="rtl"' if rtl else ""
        links.append(
            f'<a lang="{html_lang}"{direction} href="{BASE}/{slug}/">{name}</a>'
        )
    source = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <meta name="theme-color" content="#07111f">
  <title>TraderMap</title>
  <meta name="description" content="Official TraderMap privacy, support, terms and operator information.">
  <link rel="icon" href="{BASE}/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{BASE}/assets/site.css">
</head>
<body>
<main class="language-landing">
  <div class="brand-mark">TM</div>
  <h1>TraderMap</h1>
  <p>Choose a language · 选择语言 · اختر اللغة</p>
  <div>{"".join(links)}</div>
</main>
</body>
</html>
'''
    (ROOT / "index.html").write_text(source, encoding="utf-8")


def write_sitemap() -> None:
    urls = []
    for slug, _html_lang, _name, _rtl in ALL_LANGUAGES:
        for page in ("home", "privacy", "support", "terms", "operator"):
            suffix = page_suffix(page)
            urls.append(
                f"  <url><loc>{SITE}/{slug}/{suffix}</loc><lastmod>{LAST_MODIFIED}</lastmod></url>"
            )
    source = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(source, encoding="utf-8")


def main() -> None:
    update_existing_pages()
    write_new_pages()
    write_root_index()
    write_sitemap()
    print(
        f"Generated {len(TEXTS) * 5} localized pages and synchronized "
        f"{len(ALL_LANGUAGES)} language links."
    )


if __name__ == "__main__":
    main()
