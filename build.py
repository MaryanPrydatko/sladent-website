#!/usr/bin/env python3
"""Generates the 14 Sladent pages (Ukrainian and English) as plain HTML.

The site has no build step on purpose: Netlify serves the HTML as it is. This
script only keeps the shared header, footer and metadata identical on every page.
Edit copy here, run `python3 build.py` from this folder (needs Pillow, for the
photo placeholder colours), check the pages, then commit the generated HTML.
"""
from pathlib import Path
import json

SITE = Path(__file__).resolve().parent
ORIGIN = "https://sladent.com"
PHONE = "+380979351535"
PHONE_UK = "+380 97 935 15 35"
EMAIL = "sladent8@gmail.com"
IG = "https://www.instagram.com/sladent_dentistry_ternopil/"
BOOK = "contact.html#booking-form"

MARK = ('<svg viewBox="0 0 40 40" aria-hidden="true"><path fill="#D81F27" d="M20 36C8.2 28 2.5 20.6 2.5 13.2 2.5 7.6 6.8 3.5 12 3.5c3.4 0 6.3 1.9 8 4.8 1.7-2.9 4.6-4.8 8-4.8 5.2 0 9.5 4.1 9.5 9.7C37.5 20.6 31.8 28 20 36Z"/>'
        '<path fill="#fff" d="M14.6 10.8c-2 0-3.2 1.5-3.1 3.5.2 3 1.2 5 1.8 8 .5 2.4 1 4.6 2.2 4.6 1.3 0 1.6-2.8 2.2-4.8.4-1.2 1.1-1.8 2.3-1.8s1.9.6 2.3 1.8c.6 2 .9 4.8 2.2 4.8 1.2 0 1.7-2.2 2.2-4.6.6-3 1.6-5 1.8-8 .1-2-1.1-3.5-3.1-3.5-1.9 0-3.4 1.1-5.4 1.1s-3.5-1.1-5.4-1.1Z"/></svg>')
ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.96.4 1.9.7 2.8a2 2 0 0 1-.4 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.85.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>'
ICON_CAL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4.5" width="18" height="17" rx="3"/><path d="M16 2.5v4M8 2.5v4M3 10h18"/></svg>'
ICON_DRAG = '<svg viewBox="0 0 24 24" fill="none" stroke="#111215" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l-5 6 5 6M15 6l5 6-5 6"/></svg>'

# Real Google reviews (captured 2026-10-15 from the live widget, 4.8 from 93). Short excerpts, wording kept.
REVIEWS = [
    ("Олег Б.", "Oleh B.", "Послугами лікаря-стоматолога Придатка Ярослава Григоровича користуюся з 90-х років. За стоматологічною усмішкою завжди повертатимуся в клініку SLADENT.", "I have been a patient of Dr. Yaroslav Prydatko since the 1990s. For a dentist I will always come back to SLADENT."),
    ("Tati B.", "Tati B.", "Перевірено всією сімʼєю вже впродовж не одного десятка років. Щира рекомендація!", "Trusted by our whole family for more than a decade. Sincerely recommend."),
    ("Святослав Б.", "Sviatoslav B.", "Сподобався зручний графік роботи (приймають до 20:00) і те що не потрібно чекати декілька тижнів своєї черги на прийом (очікування 1-2 дні).", "I liked the convenient hours (they see patients until 8 pm) and that you don't wait weeks for an appointment (1 to 2 days)."),
    ("Іван М.", "Ivan M.", "Лікували сьогодні зуб 4-річному сину, щиро дякуємо лікарю Софії Романівні та асистенту, за професійну роботу та гарний настрій!", "Today they treated a tooth for our 4-year-old son. Many thanks to Dr. Sofiia Romanivna and the assistant for the professional work and the good mood!"),
    ("Valia S.", "Valia S.", "Вже коло 10 років всією сім'єю відвідуємо цю стоматологію. Задоволені всім! Ціна відповідає якості.", "Our whole family has been coming here for about 10 years. We are happy with everything. The price matches the quality."),
    ("Світлана Р.", "Svitlana R.", "Лікар все детально пояснює, працює дуже акуратно і викликає повну довіру.", "The doctor explains everything in detail, works very carefully and earns complete trust."),
    ("Yana D.", "Yana D.", "Робила там 8 зубів, 4 з яких без анестезії. Після лікування порадили як краще доглядати за моїми зубами.", "I had 8 teeth done there, 4 of them without anaesthesia. Afterwards they advised me how to look after my teeth."),
    ("Єлизавета Н.", "Yelyzaveta N.", "Як завжди, професійне ведення клієнтів, особистий підхід і якісне надання послуг. Обслуговуємося всією сім'єю більше 10 років.", "As always, professional care, a personal approach and quality work. Our whole family has been coming here for more than 10 years."),
    ("Пацієнт після імплантації", "Implant patient", "Перед імплантацією трохи хвилювався, але завдяки вашому досвіду, чіткості та злагодженій роботі все пройшло спокійно й значно легше, ніж я очікував.", "I was a little nervous before the implant, but thanks to your experience and well-coordinated work it went calmly and much easier than I expected."),
    ("Юлія Ч.", "Yuliia Ch.", "Світлана Карлівна прекрасний лікар, з великим досвідом роботи, професіонал своєї справи.", "Svitlana Karlivna is a wonderful doctor with great experience, a true professional."),
    ("Sergii K.", "Sergii K.", "Відбілював зуби в стоматології SlaDent, і все пройшло чудово! Результат просто відмінний.", "I had my teeth whitened at SlaDent and it went great. The result is excellent."),
    ("Людмила К.", "Liudmyla K.", "Професійні лікарі та привітний персонал. Ірина Василівна чудовий лікар!", "Professional doctors and friendly staff. Iryna Vasylivna is a wonderful doctor!"),
    ("Люба П.", "Liuba P.", "Ходжу в стоматологію Сладент вже 5 років і раджу своїм друзям і рідним.", "I have been coming to Sladent for 5 years and recommend it to my friends and family."),
    ("Віктор М.", "Viktor M.", "Гарна клініка. Привітний персонал, досвідчені фахівці, приємна атмосфера, ціни адекватні.", "A good clinic. Friendly staff, experienced specialists, a pleasant atmosphere and fair prices."),
]

T = {
    "uk": {
        "lang": "uk", "prefix": "", "brand_sub": "Стоматологія родини Придатко",
        "nav": [("services.html", "Послуги"), ("team.html", "Лікарі"), ("about.html", "Про клініку"), ("reviews.html", "Відгуки"), ("contact.html", "Контакти")],
        "book": "Записатися", "book_long": "Записатися на прийом", "call": "Подзвонити", "menu": "Відкрити меню",
        "other": "EN", "other_label": "English version",
        "addr1": "просп. Злуки, 8", "addr2": "Тернопіль, 46010",
        "hours": [("1,2,3,4,5", "Пн–Пт", "09:00–20:00"), ("6", "Субота", "10:00–15:00"), ("0", "Неділя", "вихідний")],
        "footer_lead": "Сімейна стоматологія в Тернополі з 2008 року.",
        "f_pages": "Сторінки", "f_contact": "Контакти", "f_hours": "Графік", "f_kids": "Ігри та мультики для дітей",
        "copy": "© 2026 Sladent. Стоматологія родини Придатко", "ig": "Instagram",
        "site_name": "Sladent · Стоматологія родини Придатко · Тернопіль",
    },
    "en": {
        "lang": "en", "prefix": "../", "brand_sub": "Prydatko Family Dentistry",
        "nav": [("services.html", "Services"), ("team.html", "Doctors"), ("about.html", "About"), ("reviews.html", "Reviews"), ("contact.html", "Contact")],
        "book": "Book", "book_long": "Book an appointment", "call": "Call us", "menu": "Open menu",
        "other": "UA", "other_label": "Українська версія",
        "addr1": "8 Zluky Avenue", "addr2": "Ternopil 46010, Ukraine",
        "hours": [("1,2,3,4,5", "Mon–Fri", "09:00–20:00"), ("6", "Saturday", "10:00–15:00"), ("0", "Sunday", "closed")],
        "footer_lead": "Family dentistry in Ternopil since 2008.",
        "f_pages": "Pages", "f_contact": "Contact", "f_hours": "Hours", "f_kids": "Games and cartoons for kids",
        "copy": "© 2026 Sladent. Prydatko Family Dentistry", "ig": "Instagram",
        "site_name": "Sladent · Prydatko Family Dentistry · Ternopil",
    },
}


def url(lang, page):
    base = ORIGIN + ("/en/" if lang == "en" else "/")
    return base if page == "index.html" else base + page


def other_href(lang, page):
    if lang == "uk":
        return "en/" if page == "index.html" else "en/" + page
    return "../" if page == "index.html" else "../" + page


def head(lang, page, title, desc, og_image="images/photos/og.jpg", schema=None, noindex=False):
    t = T[lang]
    p = t["prefix"]
    preload = (f'\n  <link rel="preload" as="image" href="{p}images/photos/team-sofa.jpg" imagesrcset="{p}images/photos/team-sofa-800.jpg 800w, {p}images/photos/team-sofa-1400.jpg 1400w, {p}images/photos/team-sofa.jpg 2400w" imagesizes="(max-width: 1400px) 100vw, 1300px" fetchpriority="high">'
               if page == "index.html" else "")
    alt_uk, alt_en = url("uk", page), url("en", page)
    ld = "".join(f'\n  <script type="application/ld+json">\n{json.dumps(s, ensure_ascii=False, indent=2)}\n  </script>' for s in (schema or []))
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#FFFFFF">{robots}
  <link rel="canonical" href="{url(lang, page) if not noindex else url(lang, 'index.html')}">
  <link rel="alternate" hreflang="uk" href="{alt_uk}">
  <link rel="alternate" hreflang="en" href="{alt_en}">
  <link rel="alternate" hreflang="x-default" href="{alt_uk}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{'uk_UA' if lang == 'uk' else 'en_US'}">
  <meta property="og:site_name" content="Sladent">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{ORIGIN}/{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:url" content="{url(lang, page)}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{p}images/icon.ico">
  <link rel="apple-touch-icon" href="{p}images/logo-removebg-preview.png">
  <link rel="preload" href="{p}fonts/geist-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{p}fonts/geist-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{p}site.css">{preload}
  <script>document.documentElement.classList.add('js')</script>{ld}
</head>
<body>
"""


def header(lang, page):
    t = T[lang]
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == page else ""}>{l}</a>' for h, l in t["nav"])
    mnav = "".join(f'<a class="big" href="{h}"{" aria-current=\"page\"" if h == page else ""}>{l}</a>' for h, l in t["nav"])
    home = "index.html"
    return f"""
<a class="skip" href="#main">{'Перейти до змісту' if lang == 'uk' else 'Skip to content'}</a>
<header class="hdr">
  <div class="wrap hdr__in">
    <a class="logo" href="{home}"><img src="{t['prefix']}images/logo-192.png" width="52" height="52" alt=""><span>Sladent<small>{t['brand_sub']}</small></span></a>
    <nav class="nav" aria-label="{'Основна навігація' if lang == 'uk' else 'Main navigation'}">{nav}</nav>
    <div class="hdr__tools">
      <a class="hdr__phone" href="tel:{PHONE}">{PHONE_UK}</a>
      <a class="lang" href="{other_href(lang, page)}" hreflang="{'en' if lang == 'uk' else 'uk'}" aria-label="{t['other_label']}">{t['other']}</a>
      <a class="btn btn--red btn--sm" href="{BOOK}">{t['book']}</a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="mmenu" aria-label="{t['menu']}"><span></span></button>
    </div>
  </div>
</header>
<div class="mmenu" id="mmenu">
  <nav aria-label="{'Мобільне меню' if lang == 'uk' else 'Mobile menu'}"><a class="big" href="{home}"{' aria-current="page"' if page == home else ''}>{'Головна' if lang == 'uk' else 'Home'}</a>{mnav}</nav>
  <div class="btns">
    <a class="btn btn--red" href="{BOOK}">{t['book_long']}</a>
    <a class="btn btn--soft" href="tel:{PHONE}">{ICON_PHONE}{PHONE_UK}</a>
  </div>
</div>
"""


def hours_rows(lang, cls=""):
    return "".join(f'<span data-days="{d}">{a}</span><span data-days="{d}">{b}</span>' for d, a, b in T[lang]["hours"])


def footer(lang):
    t = T[lang]
    p = t["prefix"]
    pages = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in t["nav"])
    hours = "".join(f'<li>{a} · {b}</li>' for _, a, b in t["hours"])
    return f"""
<footer class="ftr">
  <div class="wrap">
    <div class="ftr__top">
      <div>
        <img class="ftr__logo" src="{p}images/logo-removebg-preview.png" width="92" height="92" alt="Логотип: Sladent, стоматологія родини Придатко" loading="lazy">
        <p class="d3" style="color:#fff;max-width:18ch">{t['footer_lead']}</p>
      </div>
      <div><h3>{t['f_pages']}</h3><ul>{pages}<li><a href="{p}kids/">{t['f_kids']}</a></li></ul></div>
      <div><h3>{t['f_contact']}</h3><ul><li><a href="tel:{PHONE}">{PHONE_UK}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{t['addr1']}<br>{t['addr2']}</li><li><a href="{IG}" rel="noopener" target="_blank">{t['ig']}</a></li></ul></div>
      <div><h3>{t['f_hours']}</h3><ul>{hours}</ul></div>
    </div>
    <div class="ftr__mark" aria-hidden="true"></div>
    <div class="ftr__bottom"><span>{t['copy']}</span><span>{'Тернопіль' if lang == 'uk' else 'Ternopil'} · 2008</span></div>
  </div>
</footer>
<nav class="mbar" aria-label="{'Швидкі дії' if lang == 'uk' else 'Quick actions'}">
  <a class="btn btn--soft" href="tel:{PHONE}">{ICON_PHONE}{t['call']}</a>
  <a class="btn btn--red" href="{BOOK}">{ICON_CAL}{t['book']}</a>
</nav>
<script src="{p}site.js" defer></script>
</body>
</html>
"""


def stars(fill=100):
    return f'<span class="stars" aria-hidden="true"><i style="--fill:{fill}%"></i></span>'


def rcard(r, lang):
    name, name_en, uk, en = r
    return f'<figure class="rcard"><p>{uk if lang == "uk" else en}</p><footer><b>{name if lang == "uk" else name_en}</b>{stars()}</footer></figure>'


def marquee(lang):
    cards = "".join(rcard(r, lang) for r in REVIEWS[1:])
    label = "Відгуки пацієнтів з Google" if lang == "uk" else "Patient reviews from Google"
    prev, nxt = ("Попередні відгуки", "Наступні відгуки") if lang == "uk" else ("Previous reviews", "Next reviews")
    return (f'<div class="rrow-wrap"><div class="rrow" tabindex="0" role="region" aria-label="{label}">{cards}</div>'
            f'<div class="wrap rrow-foot"><span class="small muted">{"Гортайте вбік" if lang == "uk" else "Swipe for more"}</span>'
            f'<div class="rrow-nav"><button type="button" aria-label="{prev}">←</button><button type="button" aria-label="{nxt}">→</button></div></div></div>')


def dentist_schema(lang):
    return {
        "@context": "https://schema.org", "@type": "Dentist",
        "name": "Sladent — Стоматологія Родини Придатко", "alternateName": "Стоматологія Родини Придатко",
        "url": ORIGIN + "/", "logo": ORIGIN + "/images/logo.png", "image": ORIGIN + "/images/photos/team-sofa.jpg",
        "telephone": PHONE, "email": EMAIL, "priceRange": "$$", "foundingDate": "2008-09-23", "currenciesAccepted": "UAH",
        "address": {"@type": "PostalAddress", "streetAddress": "просп. Злуки, 8", "addressLocality": "Тернопіль", "addressRegion": "Тернопільська область", "postalCode": "46010", "addressCountry": "UA"},
        "geo": {"@type": "GeoCoordinates", "latitude": 49.553722, "longitude": 25.593934},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "20:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "10:00", "closes": "15:00"}],
        "areaServed": {"@type": "City", "name": "Тернопіль"},
        "medicalSpecialty": ["Dentistry", "Orthodontics", "PediatricDentistry", "Implantology", "Prosthodontics"],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.8", "bestRating": "5", "ratingCount": "93"},
        "sameAs": [IG],
    }


def faq_schema(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a_plain}} for q, _, a_plain in items]}


def faq_block(items):
    return "".join(f'<details class="rv"><summary>{q}</summary><div><p>{a}</p></div></details>' for q, a, _ in items)

def booking_panel(lang):
    t = T[lang]
    if lang == "uk":
        h, lead = "Запишіться на прийом", "Зателефонуйте або залиште заявку на сайті, і адміністратор підбере зручний час."
        lbl = ("Телефон", "Адреса", "Графік")
    else:
        h, lead = "Book an appointment", "Call us or leave a request on the site and our administrator will find a time that suits you."
        lbl = ("Phone", "Address", "Hours")
    return f"""
<section class="sec sec--tight" aria-labelledby="book-title">
  <div class="wrap">
    <div class="panel rv">
      <div>
        <h2 class="d2" id="book-title">{h}</h2>
        <p class="lead">{lead}</p>
        <div class="btns"><a class="btn btn--red" href="{BOOK}">{ICON_CAL}{t['book_long']}</a><a class="btn btn--white" href="tel:{PHONE}">{ICON_PHONE}{PHONE_UK}</a></div>
      </div>
      <dl class="panel__info">
        <div><dt>{lbl[0]}</dt><dd><a href="tel:{PHONE}">{PHONE_UK}</a></dd></div>
        <div><dt>{lbl[1]}</dt><dd>{t['addr1']}, {t['addr2'].split(',')[0].split(' ')[0]}</dd></div>
        <div><dt>{lbl[2]}</dt><dd><div class="hours">{hours_rows(lang)}</div></dd></div>
        <div><dd><span data-status></span></dd></div>
      </dl>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- pages (uk)


def faq_items(lang):
    p = T[lang]["prefix"]
    if lang == "uk":
        return [
            ("Чи приймаєте ви нових пацієнтів?", f'Так. Записатися можна за телефоном <a href="tel:{PHONE}">{PHONE_UK}</a>, через <a href="{BOOK}">форму на сайті</a> або в клініці. Перша консультація включає огляд і діагностику.',
             f"Так. Записатися можна за телефоном {PHONE_UK}, через форму на сайті або в клініці. Перша консультація включає огляд і діагностику."),
            ("Які способи оплати ви приймаєте?", "Готівку, банківські картки (Visa, Mastercard) і безготівковий розрахунок.", "Готівку, банківські картки (Visa, Mastercard) і безготівковий розрахунок."),
            ("Скільки триває прийом?", "Консультація триває 30–45 хвилин, професійна чистка близько години, імплантація чи протезування від 1,5 до 3 годин.", "Консультація триває 30–45 хвилин, професійна чистка близько години, імплантація чи протезування від 1,5 до 3 годин."),
            ("Чи лікуєте дітей?", f'Так, з трьох років. Поки ви чекаєте, дитина може погратися в <a href="{p}kids/">наші ігри або подивитися мультик</a>.', "Так, з трьох років."),
            ("Чи є паркування?", "Так, біля клініки є безкоштовна парковка для пацієнтів. Сюди зручно доїхати і громадським транспортом.", "Так, біля клініки є безкоштовна парковка для пацієнтів."),
            ("Що взяти на перший прийом?", "Документ, що посвідчує особу, і медичну картку, якщо є. Якщо маєте рентгенівські знімки чи висновки інших лікарів, візьміть їх теж.", "Документ, що посвідчує особу, і медичну картку, якщо є. Якщо маєте рентгенівські знімки чи висновки інших лікарів, візьміть їх теж."),
        ]
    return [
        ("Do you accept new patients?", f'Yes. Book by phone at <a href="tel:{PHONE}">{PHONE_UK}</a>, through the <a href="{BOOK}">form on this site</a> or at the clinic. The first consultation includes an examination and diagnosis.',
         f"Yes. Book by phone at {PHONE_UK}, through the form on this site or at the clinic. The first consultation includes an examination and diagnosis."),
        ("How can I pay?", "Cash, bank cards (Visa, Mastercard) and bank transfer.", "Cash, bank cards (Visa, Mastercard) and bank transfer."),
        ("How long does a visit take?", "A consultation takes 30–45 minutes, a professional cleaning about an hour, implants or prosthetics 1.5 to 3 hours.", "A consultation takes 30–45 minutes, a professional cleaning about an hour, implants or prosthetics 1.5 to 3 hours."),
        ("Do you treat children?", f'Yes, from the age of three. While you wait, your child can play <a href="{p}kids/">our games or watch a cartoon</a>.', "Yes, from the age of three."),
        ("Is there parking?", "Yes, there is free parking for patients next to the clinic. It is also easy to reach by public transport.", "Yes, there is free parking for patients next to the clinic."),
        ("What should I bring to my first visit?", "An ID and your medical record if you have one. If you have X-rays or reports from other doctors, bring them too.", "An ID and your medical record if you have one. If you have X-rays or reports from other doctors, bring them too."),
    ]


def x_for(lang):
    return lambda uk, en: uk if lang == "uk" else en


def srcset(src, small):
    """'images/photos/x.jpg', [800, 1400] -> srcset string listing the smaller copies and the original."""
    stem, w_full = src[:-4], None
    return ", ".join([f"{stem}-{w}.jpg {w}w" for w in small])


def img(src, w, h, alt, cls="media rv", style="", small=(), sizes="(max-width: 900px) 100vw, 50vw"):
    st = f' style="{style}"' if style else ""
    ss = f' srcset="{srcset(src, small)}, {src} {w}w" sizes="{sizes}"' if small else ""
    return f'<div class="{cls}"{st}><img src="{src}"{ss} width="{w}" height="{h}" loading="lazy" alt="{alt}"></div>'


def video(p, name, alt, ratio="4/5"):
    return (f'<div class="media media--video rv" style="aspect-ratio:{ratio}"><video data-loop muted playsinline loop preload="none" poster="{p}videos/{name}-poster.jpg" '
            f'width="720" height="1280" aria-label="{alt}"><source src="{p}videos/{name}.mp4" type="video/mp4"></video></div>')


def person(p, file, name, role, quote=None, cls="person"):
    q = f"<blockquote>{quote[0]}<footer>{quote[1]}</footer></blockquote>" if quote else ""
    return (f'<article class="{cls} rv"><div class="media"><img src="{p}images/team/{file}.jpg" width="960" height="1200" loading="lazy" alt="{name}"></div>'
            f'<h3>{name}</h3><p class="role">{role}</p>{q}</article>')


def facts(lang):
    x = x_for(lang)
    return f"""<div class="facts">
      <div class="fact rv"><b>2008</b><span>{x('рік, коли родина Придатко відкрила клініку', 'the year the Prydatko family opened the clinic')}</span></div>
      <div class="fact rv"><b>{x('4,8', '4.8')}</b><span>{x('середня оцінка з 93 відгуків на Google', 'average rating from 93 Google reviews')}</span></div>
      <div class="fact rv"><b>{x('до 20:00', 'until 8 pm')}</b><span>{x('приймаємо в будні, у суботу до 15:00', 'on weekdays, and until 3 pm on Saturday')}</span></div>
      <div class="fact rv"><b>{x('з 3 років', 'age 3+')}</b><span>{x('лікуємо дітей, а поки чекаєте, є ігри й мультики', 'we treat children, with games and cartoons while you wait')}</span></div>
    </div>"""


def reviews_grid(lang):
    cards = "".join(rcard(r, lang) for r in REVIEWS[1:])
    return f'<div class="rgrid">{cards}</div>'


DOCTORS = [
    ("yaroslav-prydatko", "Ярослав Григорович Придатко", "Yaroslav Prydatko", "Засновник і головний лікар. Терапія, протезування, естетичні реставрації.", "Founder and head doctor. General dentistry, prosthetics, aesthetic restorations.", 5),
    ("yurii-prydatko", "Юрій Ярославович Придатко", "Yurii Prydatko", "Лікар-стоматолог, хірург-імплантолог. Імплантація, кісткова пластика, синус-ліфтинг.", "Dentist and implant surgeon. Implants, bone grafting, sinus lift.", None),
    ("svitlana-prydatko", "Світлана Карлівна Придатко", "Svitlana Prydatko", "Лікар-стоматолог. Лікує дорослих і дітей.", "Dentist. Treats adults and children.", 9),
    ("iryna-hlova", "Ірина Іванівна Глова", "Iryna Hlova", "Лікар-ортодонт. Брекети, елайнери, прикус у дітей і дорослих.", "Orthodontist. Braces, aligners, bite correction for children and adults.", None),
    ("iryna-vasylivna", "Ірина Василівна", "Iryna Vasylivna", "Лікар-стоматолог.", "Dentist.", 11),
    ("sofiia-hapii", "Софія Романівна Гапій", "Sofiia Hapii", "Лікар-стоматолог. Лікує і маленьких пацієнтів.", "Dentist. Also treats young children.", 3),
]
STAFF = [
    ("nataliia-admin", "Наталія Сергіївна", "Nataliia Serhiivna", "Адміністратор", "Administrator"),
    ("liubov-shvarchovska", "Любов Шварчовська", "Liubov Shvarchovska", "Медсестра", "Nurse"),
    ("olesia", "Олеся", "Olesia", "Асистент лікаря", "Dental assistant"),
    ("sofiia-assistant", "Софія", "Sofiia", "Асистент лікаря", "Dental assistant"),
    ("yuliia", "Юлія", "Yuliia", "Асистент лікаря", "Dental assistant"),
]


def doc_quote(lang, i):
    if i is None:
        return None
    r = REVIEWS[i]
    return (r[2] if lang == "uk" else r[3], (r[0] if lang == "uk" else r[1]) + (", Google" if lang == "uk" else ", Google review"))


# ------------------------------------------------------------------ home

def page_home(lang):
    x, p, page, t = x_for(lang), T[lang]["prefix"], "index.html", T[lang]
    faq = faq_items(lang)
    html = head(lang, page, x("Sladent · Стоматологія родини Придатко · Тернопіль", "Sladent · Prydatko Family Dentistry · Ternopil"),
                x("Сімейна стоматологія Sladent у Тернополі з 2008 року. Імплантація, естетика, ортодонтія, лікування дітей. 4,8 на Google. Записатися: +380 97 935 15 35.",
                  "Sladent family dental clinic in Ternopil since 2008. Implants, aesthetic dentistry, orthodontics, children. Rated 4.8 on Google. Book: +380 97 935 15 35."),
                schema=[dentist_schema(lang), faq_schema(faq)])
    html += header(lang, page)
    d = [doc_quote(lang, 5), doc_quote(lang, 9)]
    html += f"""
<main id="main">

<section class="hero" aria-labelledby="hero-title">
  <div class="wrap">
    <div class="hero__top">
      <h1 class="d1 rv" id="hero-title">{x('Тут лікуються цілими родинами.', 'Whole families come here.')}</h1>
      <div class="rv">
        <p class="lead">{x('Стоматологія родини Придатко в Тернополі з 2008 року. Дорослі й діти, від першого огляду до імплантів.', 'The Prydatko family dental clinic in Ternopil since 2008. Adults and children, from a first check-up to implants.')}</p>
        <div class="hero__cta"><a class="btn btn--red" href="{BOOK}">{ICON_CAL}{t['book_long']}</a><a class="btn btn--soft" href="tel:{PHONE}">{ICON_PHONE}{PHONE_UK}</a></div>
      </div>
    </div>
    <div class="media hero__media rv">
      <img src="{p}images/photos/team-sofa.jpg" srcset="{p}images/photos/team-sofa-800.jpg 800w, {p}images/photos/team-sofa-1400.jpg 1400w, {p}images/photos/team-sofa.jpg 2400w" sizes="(max-width: 1400px) 100vw, 1300px" width="2400" height="1600" alt="{x('Команда Sladent: лікарі, асистенти, медсестри й адміністратори у клініці', 'The Sladent team: doctors, assistants, nurses and administrators at the clinic')}" fetchpriority="high">
      <div class="hero__chips">
        <a class="chip" href="reviews.html">{stars(96)}<span>{x('4,8', '4.8')} <small>· {x('93 відгуки на Google', '93 Google reviews')}</small></span></a>
        <span class="chip"><span data-status>{x('Пн–Пт 09:00–20:00', 'Mon–Fri 9:00–20:00')}</span></span>
      </div>
    </div>
    {facts(lang)}
  </div>
</section>

<section class="sec" aria-labelledby="svc-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="d2 rv" id="svc-title">{x('Від профілактики до нових зубів', 'From check-ups to new teeth')}</h2>
      <p class="rv">{x('Лікування, естетика, ортодонтія та імплантація в одній клініці, у лікарів, які знають вашу історію.', 'Treatment, aesthetics, orthodontics and implants in one clinic, with doctors who know your history.')}</p>
    </div>
    <div class="bento">
      <a class="tile tile--photo rv" href="services.html#implants">
        <img src="{p}videos/surgery-poster.jpg" width="720" height="1280" alt="{x('Хірурги Sladent під час імплантації', 'Sladent surgeons placing an implant')}" loading="lazy">
        <h3>{x('Імплантація', 'Implants')}</h3><p>{x('Від одного зуба до всього ряду на шести імплантах.', 'From a single tooth to a full arch on six implants.')}</p><span class="arrow arrow--light">{x('Детальніше', 'Learn more')}</span>
      </a>
      <a class="tile rv" href="services.html#cosmetic"><h3>{x('Естетика', 'Aesthetics')}</h3><p>{x('Відбілювання Magic Smile, вініри, цирконієві коронки.', 'Magic Smile whitening, veneers, zirconia crowns.')}</p><span class="arrow">{x('Детальніше', 'Learn more')}</span></a>
      <a class="tile rv" href="services.html#general"><h3>{x('Лікування зубів', 'Fillings and root canals')}</h3><p>{x('Карієс, пломби, канали, відновлення форми зуба.', 'Cavities, fillings, root canals, rebuilding a broken tooth.')}</p><span class="arrow">{x('Детальніше', 'Learn more')}</span></a>
      <a class="tile rv" href="services.html#orthodontics"><h3>{x('Ортодонтія', 'Orthodontics')}</h3><p>{x('Брекети й елайнери для дітей і дорослих.', 'Braces and aligners for children and adults.')}</p><span class="arrow">{x('Детальніше', 'Learn more')}</span></a>
      <a class="tile rv" href="services.html#pediatric"><h3>{x('Дитяча стоматологія', 'Children')}</h3><p>{x('Діти з трьох років, без поспіху і страху.', 'From age three, calmly and without fear.')}</p><span class="arrow">{x('Детальніше', 'Learn more')}</span></a>
      <a class="tile rv" href="services.html#hygiene"><h3>{x('Гігієна', 'Hygiene')}</h3><p>{x('Професійна чистка і догляд за яснами.', 'Professional cleaning and gum care.')}</p><span class="arrow">{x('Детальніше', 'Learn more')}</span></a>
      <a class="tile tile--wide tile--red rv" href="{BOOK}"><h3>{x('Не знаєте, з чого почати?', 'Not sure where to start?')}</h3><p>{x('Запишіться на огляд. Лікар пояснить, що потрібно, і складе план лікування.', 'Book a check-up. The doctor will explain what you need and make a treatment plan.')}</p><span class="arrow">{x('Записатися на огляд', 'Book a check-up')}</span></a>
    </div>
  </div>
</section>

<section class="sec sec--tone" aria-labelledby="res-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="d2 rv" id="res-title">{x('Результати наших пацієнтів', 'Our patients’ results')}</h2>
      <p class="rv">{x('Фото з нашого', 'Photos from our')} <a class="arrow" href="{IG}" rel="noopener" target="_blank">Instagram</a>{x(', до і після лікування.', ', before and after treatment.')}</p>
    </div>
    {before_after(lang)}
    <div class="results">
      <figure class="result rv"><div class="media"><img src="{p}images/photos/case-crowns.jpg" width="1000" height="790" loading="lazy" alt="{x('Цирконієві коронки на моделі щелепи', 'Zirconia crowns on a jaw model')}"></div><figcaption class="cap"><b>{x('7 імплантів і 19 цирконієвих коронок.', '7 implants and 19 zirconia crowns.')}</b> {x('Лікування тривало рік.', 'Treatment took a year.')}</figcaption></figure>
      <figure class="result rv"><div class="media"><img src="{p}images/photos/case-allon6-xray.jpg" width="900" height="1200" loading="lazy" alt="{x('Рентген: зубний ряд на шести імплантах', 'X-ray: a full arch on six implants')}"></div><figcaption class="cap"><b>{x('Усі зуби на шести імплантах.', 'A full arch on six implants.')}</b> {x('Тимчасову конструкцію поставили через тиждень після операції.', 'The temporary bridge went in a week after surgery.')}</figcaption></figure>
      <figure class="result rv"><div class="media"><img src="{p}images/photos/case-zirconia.jpg" width="1000" height="1000" loading="lazy" alt="{x('Усмішка після заміни коронок на цирконієві', 'A smile after old crowns were replaced with zirconia')}"></div><figcaption class="cap"><b>{x('Нові цирконієві коронки.', 'New zirconia crowns.')}</b> {x('Власні зуби відбілили під їхній колір.', 'The natural teeth were whitened to match.')}</figcaption></figure>
    </div>
  </div>
</section>

<section class="sec" aria-labelledby="rev-title">
  <div class="wrap">
    <div class="reviews-top">
      <div>
        <h2 class="d2 rv" id="rev-title">{x('Приходять роками. І приводять своїх.', 'Patients come back for years.')}</h2>
        <div class="score rv"><b>{x('4,8', '4.8')}</b><div>{stars(96)}<small>{x('93 відгуки на Google', '93 Google reviews')}</small></div></div>
      </div>
      <blockquote class="quote rv"><p>{REVIEWS[0][2] if lang == 'uk' else REVIEWS[0][3]}</p><footer>{REVIEWS[0][0] if lang == 'uk' else REVIEWS[0][1]} · {x('відгук на Google', 'Google review, translated from Ukrainian')}</footer></blockquote>
    </div>
  </div>
  {marquee(lang)}
  <div class="wrap" style="margin-top:2rem"><a class="arrow rv" href="reviews.html">{x('Усі відгуки', 'All reviews')}</a>{'' if lang == 'uk' else '<p class="small muted" style="margin-top:.75rem">Reviews translated from Ukrainian.</p>'}</div>
</section>

<section class="sec sec--tone" aria-labelledby="doc-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="d2 rv" id="doc-title">{x('Родина лікарів Придатко', 'The Prydatko family of dentists')}</h2>
      <p class="rv">{x('Ярослав Григорович відкрив клініку у 2008 році. Сьогодні разом з ним працюють Юрій Ярославович і Світлана Карлівна Придатко.', 'Dr. Yaroslav Prydatko opened the clinic in 2008. Today Dr. Yurii Prydatko and Dr. Svitlana Prydatko work alongside him.')}</p>
    </div>
    <div class="people">
      {person(p, 'yaroslav-prydatko', x('Ярослав Григорович Придатко', 'Yaroslav Prydatko'), x('Засновник і головний лікар', 'Founder and head doctor'), d[0])}
      {person(p, 'yurii-prydatko', x('Юрій Ярославович Придатко', 'Yurii Prydatko'), x('Лікар-стоматолог, хірург-імплантолог', 'Dentist and implant surgeon'))}
      {person(p, 'svitlana-prydatko', x('Світлана Карлівна Придатко', 'Svitlana Prydatko'), x('Лікар-стоматолог, лікує дітей', 'Dentist, also treats children'), d[1])}
    </div>
    <p class="rv more">{x('А також ортодонт Ірина Іванівна Глова, лікарі Ірина Василівна і Софія Романівна Гапій та команда асистентів, медсестер і адміністраторів.', 'Also orthodontist Iryna Hlova, Dr. Iryna Vasylivna, Dr. Sofiia Hapii and a team of assistants, nurses and administrators.')} <a class="arrow" href="team.html">{x('Уся команда', 'Meet the team')}</a></p>
  </div>
</section>

<section class="sec" aria-labelledby="team-title">
  <div class="wrap split">
    {video(p, 'team', x('Команда Sladent у клініці', 'The Sladent team at the clinic'))}
    <div>
      <h2 class="d2 rv" id="team-title">{x('Велика команда, одна родина', 'A big team that feels like family')}</h2>
      <p class="lead rv" style="margin-top:1.25rem">{x('Лікарі, асистенти, медсестри й адміністратори. Багато пацієнтів приходять до нас усією сімʼєю роками, тож ми знаємо їх на імʼя.', 'Doctors, assistants, nurses and administrators. Many patients have come with their whole family for years, so we know them by name.')}</p>
      <ul class="ticks rv">
        <li><span><b>{x('Без довгих черг.', 'No long waits.')}</b> {x('Пацієнт у відгуку пише, що чекав на прийом 1–2 дні.', 'One patient writes that he waited 1–2 days for an appointment.')}</span></li>
        <li><span><b>{x('Працюємо до 20:00', 'Open until 8 pm')}</b> {x('у будні, тож можна прийти після роботи.', 'on weekdays, so you can come after work.')}</span></li>
        <li><span><b>{x('Пояснюємо все', 'We explain everything')}</b> {x('перед лікуванням і радимо, як доглядати за зубами після.', 'before treatment and tell you how to care for your teeth afterwards.')}</span></li>
      </ul>
      <a class="btn btn--dark rv" href="team.html">{x('Познайомитися з командою', 'Meet the team')}</a>
    </div>
  </div>
</section>

{kids_card(lang)}
{booking_panel(lang)}
{place(lang)}

<section class="sec sec--tone" aria-labelledby="faq-title">
  <div class="wrap faq">
    <div>
      <h2 class="d2 rv" id="faq-title">{x('Часті запитання', 'Questions')}</h2>
      <p class="lead rv" style="margin-top:1.25rem">{x('Не знайшли відповіді? Зателефонуйте, адміністратор підкаже:', 'Can’t find the answer? Call us and our administrator will help:')} <a class="arrow" href="tel:{PHONE}">{PHONE_UK}</a></p>
    </div>
    <div class="faq__list">{faq_block(faq)}</div>
  </div>
</section>

</main>
"""
    return html + footer(lang)


def before_after(lang):
    x, p = x_for(lang), T[lang]["prefix"]
    return f"""<figure class="rv" style="margin:0">
      <div class="ba">
        <img src="{p}images/photos/whitening-before.jpg" width="1200" height="984" loading="lazy" alt="{x('Зуби до відбілювання: жовтуватий відтінок емалі', 'Teeth before whitening, with yellowish enamel')}">
        <img class="ba__after" src="{p}images/photos/whitening-after.jpg" width="1200" height="984" loading="lazy" alt="{x('Ті самі зуби після відбілювання Magic Smile', 'The same teeth after Magic Smile whitening')}">
        <span class="chip chip--l" aria-hidden="true">{x('До', 'Before')}</span><span class="chip chip--r" aria-hidden="true">{x('Після', 'After')}</span>
        <span class="ba__line" aria-hidden="true"></span><span class="ba__knob" aria-hidden="true">{ICON_DRAG}</span>
        <input type="range" min="0" max="100" value="50" aria-label="{x('Порівняти до і після відбілювання', 'Compare before and after whitening')}">
      </div>
      <figcaption class="cap"><b>{x('Відбілювання Magic Smile за одну процедуру.', 'Magic Smile whitening in one visit.')}</b> {x('Проведіть пальцем по фото, щоб порівняти.', 'Drag across the photo to compare.')}</figcaption>
    </figure>"""


def kids_card(lang):
    x, p = x_for(lang), T[lang]["prefix"]
    return f"""
<section class="sec sec--tight" aria-labelledby="kids-title">
  <div class="wrap">
    <div class="kids rv">
      <a class="media" href="{p}kids/" tabindex="-1" aria-hidden="true"><img src="{p}kids/videos/visit-poster.jpg" width="1280" height="720" loading="lazy" alt=""></a>
      <div>
        <h2 class="d2" id="kids-title">{x('Дітям тут цікаво', 'Kids like it here')}</h2>
        <p>{x('Дітей лікуємо з трьох років. Поки ви чекаєте, дитина може погратися в наші ігри або подивитися мультик про Зубчика, який іде до лікаря.', 'We treat children from age three. While you wait, your child can play our games or watch a cartoon about Zubchyk the tooth visiting the dentist.')}</p>
        <div class="btns"><a class="btn btn--kids" href="{p}kids/">{x('Ігри та мультики', 'Games and cartoons')}</a><a class="btn btn--white" href="{BOOK}">{x('Записати дитину', 'Book for a child')}</a></div>
      </div>
    </div>
  </div>
</section>"""


def place(lang):
    x, p = x_for(lang), T[lang]["prefix"]
    return f"""
<section class="sec sec--tight" aria-labelledby="place-title">
  <div class="wrap">
    <h2 class="d2 rv" id="place-title" style="margin-bottom:clamp(1.5rem,3vw,2.5rem)">{x('Просп. Злуки, 8, Тернопіль', '8 Zluky Avenue, Ternopil')}</h2>
    <div class="place">
      <div class="media rv"><img src="{p}images/photos/clinic-outside.jpg" srcset="{p}images/photos/clinic-outside-800.jpg 800w, {p}images/photos/clinic-outside.jpg 1800w" sizes="(max-width: 900px) 100vw, 45vw" width="1800" height="2149" loading="lazy" alt="{x('Команда Sladent біля входу в клініку на просп. Злуки, 8', 'The Sladent team outside the clinic at 8 Zluky Avenue')}"></div>
      <div class="media rv"><iframe src="https://www.google.com/maps?q=%D0%BF%D1%80%D0%BE%D1%81%D0%BF.+%D0%97%D0%BB%D1%83%D0%BA%D0%B8+8,+%D0%A2%D0%B5%D1%80%D0%BD%D0%BE%D0%BF%D1%96%D0%BB%D1%8C&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="{x('Sladent на карті: просп. Злуки, 8, Тернопіль', 'Sladent on the map: 8 Zluky Avenue, Ternopil')}" allowfullscreen></iframe></div>
    </div>
  </div>
</section>"""


# ------------------------------------------------------------------ services

def svc(lang, id_, media, title, lead, ticks, note=None, cta=None, flip=False, extra=""):
    ticks_html = "".join(f"<li><span>{t}</span></li>" for t in ticks)
    note_html = f'<blockquote class="note rv">{note[0]}<footer>{note[1]}</footer></blockquote>' if note else ""
    cta = cta or ("Записатися на консультацію" if lang == "uk" else "Book a consultation")
    return f"""
<section class="wrap svc{' svc--flip' if flip else ''}" id="{id_}" aria-labelledby="{id_}-t">
  {media}
  <div>
    <h2 class="d2 rv" id="{id_}-t">{title}</h2>
    <p class="lead rv">{lead}</p>
    <ul class="ticks rv">{ticks_html}</ul>
    <div class="svc__btns rv"><a class="btn btn--red" href="{BOOK}">{cta}</a>{extra}</div>
    {note_html}
  </div>
</section>"""


def page_services(lang):
    x, p, page = x_for(lang), T[lang]["prefix"], "services.html"
    html = head(lang, page, x("Послуги · Sladent · Стоматологія родини Придатко · Тернопіль", "Services · Sladent · Prydatko Family Dentistry · Ternopil"),
                x("Послуги Sladent у Тернополі: імплантація зубів, естетика й відбілювання, лікування зубів, ортодонтія, дитяча стоматологія, гігієна, протезування.",
                  "Sladent services in Ternopil: dental implants, whitening and aesthetics, fillings and root canals, orthodontics, children’s dentistry, hygiene, prosthetics."))
    html += header(lang, page)
    q = lambda i, who_uk=None, who_en=None: (REVIEWS[i][2] if lang == "uk" else REVIEWS[i][3], (who_uk or REVIEWS[i][0]) + ", відгук на Google" if lang == "uk" else (who_en or REVIEWS[i][1]) + ", Google review (translated)")
    html += f"""
<main id="main">
<section class="phero" aria-labelledby="t">
  <div class="wrap">
    <h1 class="d1 rv" id="t">{x('Що ми лікуємо', 'What we treat')}</h1>
    <p class="lead rv">{x('Від профілактичного огляду до повної імплантації. Усе в одній клініці, у лікарів, які знають вашу історію.', 'From a routine check-up to a full set of implants. All in one clinic, with doctors who know your history.')}</p>
    <nav class="jump rv" aria-label="{x('Розділи сторінки', 'On this page')}"><a href="#implants">{x('Імплантація', 'Implants')}</a><a href="#cosmetic">{x('Естетика', 'Aesthetics')}</a><a href="#general">{x('Лікування зубів', 'Fillings')}</a><a href="#orthodontics">{x('Ортодонтія', 'Orthodontics')}</a><a href="#pediatric">{x('Дитяча стоматологія', 'Children')}</a><a href="#hygiene">{x('Гігієна', 'Hygiene')}</a><a href="#more">{x('Протезування і хірургія', 'Prosthetics and surgery')}</a></nav>
  </div>
</section>
"""
    html += svc(lang, "implants", video(p, "surgery", x("Лікарі Sladent під час операції", "Sladent doctors during surgery")),
        x("Імплантація зубів", "Dental implants"),
        x("Імпланти замінюють втрачені зуби: від одного зуба до всього ряду. Імплантацією займається хірург Юрій Ярославович Придатко.", "Implants replace missing teeth, from one tooth to a full arch. Implant surgery is done by Dr. Yurii Prydatko."),
        [x("<b>Один імплант</b> замість одного втраченого зуба", "<b>A single implant</b> for one missing tooth"),
         x("<b>Кілька імплантів</b>, коли бракує кількох зубів поспіль", "<b>Several implants</b> when a few teeth in a row are missing"),
         x("<b>Весь ряд на шести імплантах</b> (All-on-6), коли зубів майже не залишилось", "<b>A full arch on six implants</b> (All-on-6) when few teeth remain"),
         x("<b>Кісткова пластика і синус-ліфтинг</b>, коли для імпланта бракує кістки", "<b>Bone grafting and sinus lift</b> when there is not enough bone")],
        note=(REVIEWS[8][2] if lang == "uk" else REVIEWS[8][3], x("Пацієнт після імплантації, відгук на Google", "Implant patient, Google review (translated)")))
    html += svc(lang, "cosmetic", img(f"{p}images/photos/case-zirconia.jpg", 1000, 1000, x("Усмішка після заміни коронок на цирконієві", "A smile after old crowns were replaced with zirconia")),
        x("Естетика і відбілювання", "Aesthetics and whitening"),
        x("Світліші зуби, рівний колір, нові коронки замість старих. Підбираємо так, щоб результат виглядав природно.", "Whiter teeth, an even colour, new crowns instead of old ones. We match everything so the result looks natural."),
        [x("<b>Відбілювання Magic Smile</b> за одну процедуру", "<b>Magic Smile whitening</b> in one visit"),
         x("<b>Вініри</b> для зміни форми й кольору передніх зубів", "<b>Veneers</b> to change the shape and colour of front teeth"),
         x("<b>Цирконієві коронки</b> замість старих коронок", "<b>Zirconia crowns</b> to replace old crowns"),
         x("<b>Художня реставрація</b>: старі пломби замінюємо на непомітні", "<b>Aesthetic restorations</b>: old fillings replaced with invisible ones")],
        note=q(10), flip=True)
    html += svc(lang, "general", img(f"{p}images/photos/work-9368.jpg", 1600, 2133, x("Лікарі Sladent під час лікування пацієнта", "Sladent doctors treating a patient"), small=(800,)),
        x("Лікування зубів", "Fillings and root canals"),
        x("Лікуємо карієс і пульпіт, пломбуємо, відновлюємо зруйновані зуби. Спершу огляд і план, потім лікування.", "We treat cavities and inflamed nerves, place fillings and rebuild broken teeth. First an examination and a plan, then treatment."),
        [x("<b>Огляд і план лікування</b> на першому прийомі", "<b>Examination and treatment plan</b> at your first visit"),
         x("<b>Лікування карієсу</b> і пломби", "<b>Cavity treatment</b> and fillings"),
         x("<b>Лікування каналів</b> і пульпіту, щоб зберегти зуб", "<b>Root canal treatment</b> to save the tooth"),
         x("<b>Відновлення форми зуба</b> після руйнування", "<b>Rebuilding a broken tooth</b>"),
         x("<b>Видалення зубів</b>, коли зуб не врятувати", "<b>Extractions</b> when a tooth cannot be saved")],
        note=(x("Окрема подяка Максиму Петровичу, професіонал своєї справи. Особливо у відновленні форми зубів. Ідеально відновив зуб, крім того все зробив швидко і безболісно.",
                "Special thanks to Maksym Petrovych, a true professional, especially at restoring the shape of teeth. He restored my tooth perfectly, quickly and painlessly."),
              x("Святослав Б., відгук на Google", "Sviatoslav B., Google review (translated)")))
    html += svc(lang, "orthodontics", img(f"{p}images/photos/ortho-brackets.jpg", 720, 756, x("Набір брекетів у клініці перед встановленням", "A bracket kit at the clinic before fitting")),
        x("Ортодонтія", "Orthodontics"),
        x("Вирівнюємо зуби і виправляємо прикус у дітей і дорослих. Лікування веде лікар-ортодонт Ірина Іванівна Глова.", "We straighten teeth and correct bites for children and adults. Treatment is led by orthodontist Dr. Iryna Hlova."),
        [x("<b>Брекети</b> для дітей і дорослих", "<b>Braces</b> for children and adults"),
         x("<b>Елайнери</b>, прозорі капи замість брекетів", "<b>Aligners</b>, clear trays instead of braces"),
         x("<b>Ортодонтія для дітей</b>, коли прикус ще формується", "<b>Early treatment for children</b> while the bite is still forming"),
         x("<b>Ретейнери</b>, щоб зуби залишились рівними після лікування", "<b>Retainers</b> to keep teeth straight after treatment")],
        cta=x("Записатися до ортодонта", "Book with the orthodontist"), flip=True)
    html += svc(lang, "pediatric", img(f"{p}kids/videos/visit-poster.jpg", 1280, 720, x("Кадр з мультика Sladent: Зубчик сміливо сидить у кріслі", "A still from the Sladent cartoon: Zubchyk sits bravely in the chair"), style="aspect-ratio:16/11"),
        x("Дитяча стоматологія", "Children’s dentistry"),
        x("Лікуємо дітей з трьох років. Не поспішаємо: дитина має звикнути до лікаря, щоб наступного разу йти без страху.", "We treat children from age three. We take our time so the child gets used to the doctor and comes back without fear."),
        [x("<b>Перший огляд</b> і знайомство з кабінетом", "<b>A first check-up</b> and a look around the room"),
         x("<b>Лікування молочних зубів</b>", "<b>Treating baby teeth</b>"),
         x("<b>Герметизація фісур</b> і фторування для захисту від карієсу", "<b>Fissure sealants</b> and fluoride against cavities"),
         x("<b>Вчимо чистити зуби</b> в ігровій формі", "<b>Brushing lessons</b> as a game")],
        note=q(3), cta=x("Записати дитину", "Book for a child"),
        extra=f'<a class="btn btn--soft" href="{p}kids/">{x("Ігри та мультики", "Games and cartoons")}</a>')
    html += svc(lang, "hygiene", img(f"{p}images/photos/hygiene-tools.jpg", 686, 720, x("Стерильні інструменти на лотку перед прийомом", "Sterile instruments laid out before a visit")),
        x("Професійна гігієна", "Professional hygiene"),
        x("Регулярна чистка тримає зуби і ясна здоровими та помічає проблеми рано. Радимо приходити раз на пів року.", "Regular cleaning keeps teeth and gums healthy and catches problems early. We recommend coming every six months."),
        [x("<b>Ультразвукове чищення</b> від зубного каменю", "<b>Ultrasonic cleaning</b> to remove tartar"),
         x("<b>Чищення від нальоту</b> і пігментації", "<b>Stain and plaque removal</b>"),
         x("<b>Полірування</b> і фторування емалі", "<b>Polishing</b> and fluoride"),
         x("<b>Догляд за яснами</b>, лікування запалення", "<b>Gum care</b> and treating inflammation")],
        cta=x("Записатися на чистку", "Book a cleaning"), flip=True)
    html += f"""
<section class="sec sec--tone" id="more" aria-labelledby="more-t">
  <div class="wrap">
    <h2 class="d2 rv" id="more-t" style="margin-bottom:clamp(1.75rem,3.5vw,3rem)">{x('Ще ми робимо', 'We also do')}</h2>
    <div class="extra">
      <article class="rv"><h3 class="d3">{x('Протезування', 'Prosthetics')}</h3><p>{x('Коронки, мости і знімні протези, щоб повернути зубам форму й функцію.', 'Crowns, bridges and dentures to restore how your teeth look and work.')}</p></article>
      <article class="rv"><h3 class="d3">{x('Хірургія', 'Oral surgery')}</h3><p>{x('Видалення зубів, зокрема зубів мудрості, і підготовка до імплантації.', 'Extractions, including wisdom teeth, and preparation for implants.')}</p></article>
      <article class="rv"><h3 class="d3">{x('Лікування ясен', 'Gum treatment')}</h3><p>{x('Лікуємо запалення і кровоточивість ясен, допомагаємо зберегти зуби.', 'We treat inflamed and bleeding gums to help you keep your teeth.')}</p></article>
    </div>
  </div>
</section>
{booking_panel(lang)}
</main>
"""
    return html + footer(lang)


# ------------------------------------------------------------------ about

def page_about(lang):
    x, p, page = x_for(lang), T[lang]["prefix"], "about.html"
    html = head(lang, page, x("Про клініку · Sladent · Стоматологія родини Придатко · Тернопіль", "About · Sladent · Prydatko Family Dentistry · Ternopil"),
                x("Історія Sladent, стоматології родини Придатко в Тернополі: сімейна клініка з 2008 року на просп. Злуки, 8.", "The story of Sladent, the Prydatko family dental clinic in Ternopil: a family practice since 2008 at 8 Zluky Avenue."))
    html += header(lang, page)
    values = [
        (x("Сімейна клініка", "A family clinic"), x("Клініку заснувала родина лікарів Придатко, і вона досі працює тут щодня. Багато пацієнтів приходять до нас усією сімʼєю роками.", "The Prydatko family of dentists founded the clinic and still works here every day. Many patients have come with their whole family for years.")),
        (x("Пояснюємо все", "We explain everything"), x("Перед лікуванням лікар пояснює, що і навіщо робитиме, а після радить, як доглядати за зубами.", "Before treatment the doctor explains what will be done and why, and afterwards tells you how to care for your teeth.")),
        (x("Діти без страху", "Children without fear"), x("Дітей лікуємо з трьох років і не поспішаємо. Поки ви чекаєте, є ігри й мультики про Зубчика.", "We treat children from age three and take our time. While you wait, there are games and cartoons about Zubchyk the tooth.")),
        (x("Усе в одній клініці", "Everything in one place"), x("Лікування, гігієна, естетика, ортодонтія, хірургія та імплантація. Вам не треба шукати різних лікарів по місту.", "Fillings, hygiene, aesthetics, orthodontics, surgery and implants. No need to look for different doctors around the city.")),
        (x("Зручний графік", "Convenient hours"), x("У будні працюємо до 20:00, у суботу до 15:00, тож на прийом можна прийти після роботи.", "We are open until 8 pm on weekdays and until 3 pm on Saturday, so you can come after work.")),
        (x("Велика команда", "A big team"), x("Лікарі, асистенти, медсестри й адміністратори, які знають пацієнтів на імʼя.", "Doctors, assistants, nurses and administrators who know patients by name.")),
    ]
    v = "".join(f'<article class="rv"><h3 class="d3">{a}</h3><p>{b}</p></article>' for a, b in values)
    html += f"""
<main id="main">
<section class="phero" aria-labelledby="t">
  <div class="wrap phero__row">
    <h1 class="d1 rv" id="t">{x('Родинна клініка з 2008 року', 'A family clinic since 2008')}</h1>
    <p class="lead rv">{x('Sladent — це стоматологія родини Придатко на просп. Злуки, 8 у Тернополі. Один з пацієнтів лікується у Ярослава Григоровича ще з 90-х.', 'Sladent is the Prydatko family dental clinic at 8 Zluky Avenue in Ternopil. One patient has seen Dr. Yaroslav Prydatko since the 1990s.')}</p>
  </div>
</section>
<section aria-label="{x('Команда', 'The team')}">
  <div class="wrap">{img(f'{p}images/photos/team-sofa-2.jpg', 2000, 1333, x('Уся команда Sladent у клініці', 'The whole Sladent team at the clinic'), style='aspect-ratio:16/8', small=(800, 1300), sizes='(max-width: 1400px) 100vw, 1300px')}
    {facts(lang)}
  </div>
</section>
<section class="sec" aria-labelledby="story-t">
  <div class="wrap split">
    <div>
      <h2 class="d2 rv" id="story-t">{x('Як усе починалося', 'How it started')}</h2>
      <div class="prose rv" style="margin-top:1.5rem">
        <p>{x('<strong>Стоматологію родини Придатко</strong> заснував у 2008 році Ярослав Григорович Придатко. Сюди від початку приходили цілими родинами, і багато сімей лікуються тут досі.', '<strong>Prydatko Family Dentistry</strong> was founded in 2008 by Dr. Yaroslav Prydatko. Whole families have come here from the start, and many still do.')}</p>
        <p>{x('Клініка росла, і разом з нею зросла команда. Сьогодні з Ярославом Григоровичем працюють Юрій Ярославович і Світлана Карлівна Придатко, інші лікарі, ортодонт, асистенти, медсестри й адміністратори.', 'The clinic grew and so did the team. Today Dr. Yaroslav Prydatko works with Dr. Yurii Prydatko and Dr. Svitlana Prydatko, other dentists, an orthodontist, assistants, nurses and administrators.')}</p>
        <p>{x('<strong>Sladent</strong> — сучасна назва тієї самої родинної клініки. Ті самі люди, той самий підхід.', '<strong>Sladent</strong> is the modern name of the same family clinic. The same people and the same care.')}</p>
      </div>
    </div>
    {video(p, 'team', x('Команда Sladent у клініці', 'The Sladent team at the clinic'))}
  </div>
</section>
<section class="sec sec--tone" aria-labelledby="val-t">
  <div class="wrap">
    <h2 class="d2 rv" id="val-t" style="margin-bottom:clamp(1.75rem,3.5vw,3rem)">{x('Чому до нас повертаються', 'Why patients come back')}</h2>
    <div class="values">{v}</div>
  </div>
</section>
<section class="sec" aria-labelledby="q-t">
  <div class="wrap reviews-top" style="margin-bottom:0">
    <h2 class="d2 rv" id="q-t">{x('Що кажуть пацієнти', 'What patients say')}</h2>
    <blockquote class="quote rv"><p>{REVIEWS[1][2] if lang == 'uk' else REVIEWS[1][3]}</p><footer>{REVIEWS[1][0] if lang == 'uk' else REVIEWS[1][1]} · {x('відгук на Google', 'Google review, translated')} · <a class="arrow" href="reviews.html">{x('Усі відгуки', 'All reviews')}</a></footer></blockquote>
  </div>
</section>
{booking_panel(lang)}
{place(lang)}
</main>
"""
    return html + footer(lang)


# ------------------------------------------------------------------ team

def page_team(lang):
    x, p, page = x_for(lang), T[lang]["prefix"], "team.html"
    html = head(lang, page, x("Лікарі та команда · Sladent · Стоматологія родини Придатко · Тернопіль", "Doctors and team · Sladent · Prydatko Family Dentistry · Ternopil"),
                x("Лікарі Sladent: Ярослав Григорович Придатко, Юрій Ярославович Придатко, Світлана Карлівна Придатко, ортодонт Ірина Іванівна Глова, Ірина Василівна, Софія Романівна Гапій.",
                  "Sladent doctors: Yaroslav Prydatko, Yurii Prydatko, Svitlana Prydatko, orthodontist Iryna Hlova, Iryna Vasylivna and Sofiia Hapii."))
    html += header(lang, page)
    docs = "".join(person(p, f, x(n_uk, n_en), x(r_uk, r_en), doc_quote(lang, qi)) for f, n_uk, n_en, r_uk, r_en, qi in DOCTORS)
    staff = "".join(person(p, f, x(n_uk, n_en), x(r_uk, r_en)) for f, n_uk, n_en, r_uk, r_en in STAFF)
    html += f"""
<main id="main">
<section class="phero" aria-labelledby="t">
  <div class="wrap phero__row">
    <h1 class="d1 rv" id="t">{x('Лікарі та команда', 'Doctors and team')}</h1>
    <p class="lead rv">{x('Лікарі і команда, яка зустріне вас на рецепції, підготує кабінет і буде поруч під час прийому.', 'Our doctors and the team who will greet you at reception, prepare the room and stay with you during your visit.')}</p>
  </div>
</section>
<section class="sec" style="padding-top:0" aria-labelledby="d-t">
  <div class="wrap">
    <h2 class="d2 rv" id="d-t" style="margin-bottom:clamp(1.75rem,3.5vw,3rem)">{x('Лікарі', 'Doctors')}</h2>
    <div class="people">{docs}</div>
  </div>
</section>
<section class="sec sec--tone" aria-labelledby="s-t">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="d2 rv" id="s-t">{x('Команда клініки', 'Clinic team')}</h2>
      <p class="rv">{x('Асистенти, медсестри й адміністратори. Саме вони записують вас на прийом, готують інструменти і допомагають лікарю.', 'Assistants, nurses and administrators. They book your appointment, prepare the instruments and assist the doctor.')}</p>
    </div>
    <div class="people people--5">{staff}</div>
  </div>
</section>
<section class="sec" aria-labelledby="all-t">
  <div class="wrap split split--flip">
    {img(f'{p}images/photos/team-vertical.jpg', 1400, 2100, x('Уся команда Sladent разом', 'The whole Sladent team together'), style='aspect-ratio:4/5', small=(700,))}
    <div>
      <h2 class="d2 rv" id="all-t">{x('Уся команда разом', 'The whole team')}</h2>
      <p class="lead rv" style="margin-top:1.25rem">{x('Велика команда означає, що вас приймуть швидко, а лікар матиме поруч асистента на кожному прийомі.', 'A big team means you are seen quickly and your doctor has an assistant at every visit.')}</p>
      <div class="rv" style="margin-top:2rem"><a class="btn btn--red" href="{BOOK}">{ICON_CAL}{T[lang]['book_long']}</a></div>
    </div>
  </div>
</section>
{booking_panel(lang)}
</main>
"""
    return html + footer(lang)


# ------------------------------------------------------------------ reviews

def page_reviews(lang):
    x, p, page = x_for(lang), T[lang]["prefix"], "reviews.html"
    html = head(lang, page, x("Відгуки · Sladent · Стоматологія родини Придатко · Тернопіль", "Reviews · Sladent · Prydatko Family Dentistry · Ternopil"),
                x("Відгуки пацієнтів про Sladent, стоматологію родини Придатко в Тернополі: 4,8 на Google з 93 відгуків.", "Patient reviews of Sladent, the Prydatko family dental clinic in Ternopil: rated 4.8 on Google from 93 reviews."))
    html += header(lang, page)
    note = "" if lang == "uk" else '<p class="small muted rv" style="margin-top:1rem">Reviews are translated from Ukrainian. The originals are on Google.</p>'
    html += f"""
<main id="main">
<section class="phero" aria-labelledby="t">
  <div class="wrap phero__row">
    <div>
      <h1 class="d1 rv" id="t">{x('Відгуки пацієнтів', 'Patient reviews')}</h1>
      <div class="score rv"><b>{x('4,8', '4.8')}</b><div>{stars(96)}<small>{x('93 відгуки на Google', '93 Google reviews')}</small></div></div>
    </div>
    <blockquote class="quote rv"><p>{REVIEWS[0][2] if lang == 'uk' else REVIEWS[0][3]}</p><footer>{REVIEWS[0][0] if lang == 'uk' else REVIEWS[0][1]} · {x('відгук на Google', 'Google review')}</footer></blockquote>
  </div>
</section>
<section class="sec" style="padding-top:clamp(1rem,2vw,2rem)" aria-label="{x('Вибрані відгуки', 'Selected reviews')}">
  <div class="wrap">{reviews_grid(lang)}{note}</div>
</section>
<section class="sec sec--tone" aria-labelledby="g-t">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="d2 rv" id="g-t">{x('Усі відгуки з Google', 'All Google reviews')}</h2>
      <p class="rv">{x('Свіжі відгуки підтягуються з Google автоматично. Будемо вдячні, якщо залишите свій.', 'New reviews load from Google automatically. We would be grateful if you left one too.')}</p>
    </div>
    <div class="form-card form-card--reviews rv">
      <script src="https://static.elfsight.com/platform/platform.js" async></script>
      <div class="elfsight-app-948240cf-e926-4c1e-82aa-ef7c5c3e42bb" data-elfsight-app-lazy></div>
    </div>
  </div>
</section>
{booking_panel(lang)}
</main>
"""
    return html + footer(lang)


# ------------------------------------------------------------------ contact

def page_contact(lang):
    x, p, page, t = x_for(lang), T[lang]["prefix"], "contact.html", T[lang]
    html = head(lang, page, x("Контакти і запис · Sladent · Стоматологія родини Придатко · Тернопіль", "Contact and booking · Sladent · Prydatko Family Dentistry · Ternopil"),
                x("Запис у Sladent: +380 97 935 15 35. Просп. Злуки, 8, Тернопіль. Пн–Пт 09:00–20:00, Сб 10:00–15:00.", "Book at Sladent: +380 97 935 15 35. 8 Zluky Avenue, Ternopil. Mon–Fri 9:00–20:00, Sat 10:00–15:00."))
    html += header(lang, page)
    hrs = "".join(f'<span data-days="{d}">{a} · {b}</span>' for d, a, b in t["hours"])
    html += f"""
<main id="main">
<section class="phero" aria-labelledby="t">
  <div class="wrap phero__row">
    <h1 class="d1 rv" id="t">{x('Контакти і запис', 'Contact and booking')}</h1>
    <p class="lead rv">{x('Найшвидше записатися телефоном. Або залиште заявку нижче, і адміністратор передзвонить.', 'The fastest way to book is by phone. Or leave a request below and our administrator will call you back.')}</p>
  </div>
</section>
<section aria-label="{x('Контакти', 'Contact details')}">
  <div class="wrap contact-grid">
    <a class="rv" href="tel:{PHONE}"><span>{x('Телефон', 'Phone')}</span><b>{PHONE_UK}</b><span>{x('Запис і питання', 'Booking and questions')}</span></a>
    <a class="rv" href="mailto:{EMAIL}"><span>{x('Пошта', 'Email')}</span><b>{EMAIL}</b><span>{x('Для документів і довгих питань', 'For documents and longer questions')}</span></a>
    <a class="rv" href="https://www.google.com/maps/search/?api=1&amp;query=%D0%BF%D1%80%D0%BE%D1%81%D0%BF.+%D0%97%D0%BB%D1%83%D0%BA%D0%B8+8+%D0%A2%D0%B5%D1%80%D0%BD%D0%BE%D0%BF%D1%96%D0%BB%D1%8C" rel="noopener" target="_blank"><span>{x('Адреса', 'Address')}</span><b>{t['addr1']}</b><span>{t['addr2']}</span></a>
    <div class="rv"><span>{x('Графік', 'Hours')}</span><b data-status>{x('Пн–Пт 09:00–20:00', 'Mon–Fri 9:00–20:00')}</b><span class="hours-list">{hrs}</span></div>
  </div>
</section>
<section class="sec" id="booking-form" aria-labelledby="f-t" style="padding-top:clamp(2.5rem,5vw,4.5rem)">
  <div class="wrap book">
    <div class="book__head">
      <h2 class="d2 rv" id="f-t">{x('Заявка на прийом', 'Appointment request')}</h2>
      <p class="lead rv" style="margin-top:1rem">{x('Залиште імʼя і телефон. Адміністратор зателефонує і підбере зручний час.', 'Leave your name and phone number. Our administrator will call you to find a time.')}</p>
      <a class="btn btn--soft rv book__call" href="tel:{PHONE}">{ICON_PHONE}{x('Або подзвоніть:', 'Or call:')} {PHONE_UK}</a>
    </div>
    <div class="form-card rv book__form">
      <script src="https://static.elfsight.com/platform/platform.js" async></script>
      <div class="elfsight-app-18d024a3-e0f4-4038-9c6b-86ec1a5df6bb" data-elfsight-app-lazy></div>
    </div>
    <ul class="ticks rv book__notes">
      <li><span>{x('Можна записати одразу кілька членів родини', 'You can book for several family members at once')}</span></li>
      <li><span>{x('Для дитини вкажіть її вік', 'For a child, please add their age')}</span></li>
      <li><span>{x('Болить зараз? Телефонуйте, так швидше', 'In pain right now? Call us, it is faster')}</span></li>
    </ul>
  </div>
</section>
{place(lang)}
</main>
"""
    return html + footer(lang)


# ------------------------------------------------------------------ 404

def page_404(lang):
    x, p, page = x_for(lang), T[lang]["prefix"], "404.html"
    html = head(lang, page, x("Сторінку не знайдено · Sladent", "Page not found · Sladent"), x("Сторінку не знайдено.", "Page not found."), noindex=True)
    # 404 is served at any depth, so its links must be absolute
    html = html.replace(f'href="{p}site.css"', 'href="/site.css"').replace(f'href="{p}images/', 'href="/images/')
    hdr = header(lang, page)
    for h, _ in T[lang]["nav"] + [("index.html", ""), (BOOK, "")]:
        hdr = hdr.replace(f'href="{h}"', f'href="{("/en/" if lang == "en" else "/")}{h}"')
    hdr = hdr.replace(f'src="{p}images/', 'src="/images/').replace('href="en/404.html"', 'href="/en/"').replace('href="../404.html"', 'href="/"')
    html += hdr
    html += f"""
<main id="main">
<section class="wrap nf">
  <b aria-hidden="true">404</b>
  <h1 class="d2">{x('Такої сторінки немає', 'This page doesn’t exist')}</h1>
  <p class="lead">{x('Можливо, посилання застаріло. Почніть з головної або запишіться на прийом.', 'The link may be out of date. Start from the home page or book an appointment.')}</p>
  <div class="hero__cta"><a class="btn btn--dark" href="{'/en/' if lang == 'en' else '/'}">{x('На головну', 'Home')}</a><a class="btn btn--red" href="{'/en/' if lang == 'en' else '/'}{BOOK}">{T[lang]['book_long']}</a></div>
</section>
</main>
"""
    ftr = footer(lang)
    for h, _ in T[lang]["nav"]:
        ftr = ftr.replace(f'href="{h}"', f'href="{("/en/" if lang == "en" else "/")}{h}"')
    ftr = ftr.replace(f'href="{BOOK}"', f'href="{("/en/" if lang == "en" else "/")}{BOOK}"').replace(f'src="{p}', 'src="/').replace(f'href="{p}kids/"', 'href="/kids/"')
    return html + ftr


import re
from PIL import Image
_AVG = {}


def avg_colour(rel):
    """Average colour of an image in the site folder, used as its placeholder."""
    if rel not in _AVG:
        path = SITE / rel.replace("../", "").lstrip("/")
        try:
            r, g, b = Image.open(path).convert("RGB").resize((1, 1), Image.LANCZOS).getpixel((0, 0))
            _AVG[rel] = f"#{r:02x}{g:02x}{b:02x}"
        except OSError:
            _AVG[rel] = ""
    return _AVG[rel]


WRAP = re.compile(r'(<(?:div|a)\b[^>]*\bclass="(?:media|tile tile--photo)[^"]*"[^>]*?)(>\s*)(<(?:img|video)\b[^>]*?(?:src|poster)="([^"]+)")')


def finish(html):
    def wrap(m):
        tag, gap, media, src = m.groups()
        col = avg_colour(src)
        if col:
            tag = tag.replace('style="', f'style="background-color:{col};', 1) if 'style="' in tag else tag + f' style="background-color:{col}"'
        if media.startswith("<img"):
            media = media.replace("<img ", '<img onload="this.classList.add(\'ok\')" onerror="this.classList.add(\'ok\')" ', 1)
            media = media.replace('<img onload', '<img class="fade" onload', 1) if ' class="' not in media else media.replace(' class="', ' class="fade ', 1)
        return tag + gap + media
    html = WRAP.sub(wrap, html)
    # before/after: both photos sit in .ba, give it the "before" colour and fade both in
    html = re.sub(r'(<img )(class="ba__after" )?(src="[^"]*whitening-(?:before|after)\.jpg")', lambda m: m.group(1) + ('class="ba__after fade" ' if m.group(2) else 'class="fade" ') + 'onload="this.classList.add(\'ok\')" onerror="this.classList.add(\'ok\')" ' + m.group(3), html)
    html = html.replace(' rv"', '"').replace(' class="rv"', '').replace('class="rv ', 'class="')
    return html


PAGES = {}
for _lang in ("uk", "en"):
    _dir = "" if _lang == "uk" else "en/"
    for _name, _fn in (("index.html", page_home), ("services.html", page_services), ("about.html", page_about), ("team.html", page_team),
                       ("reviews.html", page_reviews), ("contact.html", page_contact), ("404.html", page_404)):
        PAGES[_dir + _name] = (lambda f=_fn, l=_lang: f(l))

if __name__ == "__main__":
    import sys
    only = sys.argv[1:]
    for name, fn in PAGES.items():
        if only and name not in only:
            continue
        out = SITE / name
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(finish(fn()), encoding="utf-8")
        print("wrote", out.relative_to(SITE.parent), out.stat().st_size, "bytes")
