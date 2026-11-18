#!/usr/bin/env python3
"""Builds every HandCut site page with one shared <head>: title, description,
canonical, Open Graph, Twitter card, SoftwareApplication JSON-LD (no
aggregateRating), the App Store smart banner and a visible App Store banner.
Run from the repo root. Copy is honest by construction: edit free, export with
Pro, price shown in the app; no prices or trials are quoted."""
import json, html, os, datetime
BASE = "https://shuhratjon1010.github.io/handcut/"
APP = "https://apps.apple.com/app/id6762062166"
ICON = BASE + "img/handcut-icon-512.jpg"
SHOT = BASE + "img/screenshot-1.jpg"
TODAY = "2026-11-18"
OFFER_LINE = "Edit free. Export with Pro, a monthly subscription. Price shown in the app."
CSS = ("body{max-width:46rem;margin:0 auto;padding:0 1.2rem 2rem;font:17px/1.6 -apple-system,system-ui,sans-serif;color:#111}"
       "a{color:#6d28d9}a.b{display:inline-block;padding:.75rem 1.25rem;border-radius:.75rem;background:#6d28d9;color:#fff;text-decoration:none;font-weight:600}"
       ".banner{display:flex;align-items:center;gap:.8rem;padding:.7rem 0;border-bottom:1px solid #8883;margin-bottom:1.2rem}"
       ".banner img{width:44px;height:44px;border-radius:10px}.banner span{flex:1;font-size:.95rem}"
       "td,th{border:1px solid #8884;padding:.45rem;vertical-align:top;text-align:left}table{border-collapse:collapse;width:100%}"
       "footer{margin-top:3rem;font-size:.9rem;border-top:1px solid #8883;padding-top:1rem}nav a{margin-right:.6rem}"
       "@media (prefers-color-scheme:dark){body{background:#111;color:#eee}a{color:#b794f6}}")
APP_LD = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "HandCut",
    "alternateName": "Handcut: Auto Captions Video",
    "applicationCategory": "MultimediaApplication",
    "applicationSubCategory": "Video editor",
    "operatingSystem": "iOS 17.0 or later",
    "installUrl": APP,
    "downloadUrl": APP,
    "url": BASE,
    "image": ICON,
    "screenshot": SHOT,
    "author": {"@type": "Person", "name": "Daler Soliev"},
    "publisher": {"@type": "Person", "name": "Daler Soliev"},
    "inLanguage": "en",
    "isAccessibleForFree": True,
    "description": ("Captions-first iPhone video editor. Word-by-word captions transcribed on your iPhone, "
                    "a real multi-clip timeline, 4K export and no watermark. Edit free; exporting needs a "
                    "HandCut Pro monthly subscription, priced in the app."),
    "featureList": ["Word-by-word auto captions transcribed on-device", "Karaoke-style word highlighting",
                    "Edit any caption word and restyle captions", "Burn captions into the video or export SRT",
                    "Multi-clip timeline with trim, split and reorder", "Picture-in-picture facecam bubble",
                    "Speed 0.25x to 4x", "Manual keyframes", "Export up to 4K, up to 60 fps", "No watermark",
                    "No account, no ads"],
    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD",
               "description": "Free to download and edit. Exporting needs a HandCut Pro monthly subscription; the price is shown in the app."},
}
PAGES = [
  ("index.html","HandCut: auto captions video editor for iPhone, no watermark","Word-by-word auto captions made on your iPhone, a real timeline and 4K export with no watermark. Edit free; export with Pro."),
  ("auto-captions-app.html","Auto captions app for iPhone: word-by-word, on-device | HandCut","An auto captions app for iPhone that transcribes on the device and times every caption to the word. No account, no watermark. Edit free; export with Pro."),
  ("add-subtitles-to-video-iphone.html","How to add subtitles to a video on iPhone | HandCut","Add subtitles to any video on iPhone in a few taps: import, generate word-by-word subtitles on-device, fix words, style, export. No watermark."),
  ("video-editor-no-watermark.html","Video editor with no watermark for iPhone | HandCut","HandCut never adds a watermark. Edit free on iPhone with captions, timeline, keyframes and 4K; exporting needs a HandCut Pro subscription."),
  ("how-to-add-captions-iphone.html","How to add captions to a video on iPhone (no watermark) | HandCut","Step by step: add word-by-word captions to a video on iPhone with HandCut and export with no watermark."),
  ("vs-capcut.html","HandCut vs CapCut for captions on iPhone","An honest, sourced comparison of HandCut and CapCut for adding captions on iPhone."),
  ("compare/index.html","HandCut compared with other auto captions apps","Public App Store facts for HandCut and other auto captions apps, with links to each listing."),
  ("app.html","HandCut app: features and plan","What HandCut does on iPhone, and how the plan works: edit free, export with Pro, price shown in the app."),
  ("styles.html","HandCut caption styles: Lantern, Silk and Spark","The caption styles in HandCut and the legibility rules behind them."),
  ("support.html","HandCut support and FAQ","Contact HandCut support and read answers about plans, captions, offline use, accounts and projects."),
  ("privacy.html","HandCut privacy policy","HandCut collects no data. Editing and captions run on your iPhone; nothing is sent to us."),
  ("terms.html","HandCut terms of use","The terms for using the HandCut iOS app, purchases and subscriptions."),
]
NAV = [("./","Home"),("auto-captions-app.html","Auto captions app"),("add-subtitles-to-video-iphone.html","Add subtitles on iPhone"),
       ("video-editor-no-watermark.html","No-watermark editor"),("how-to-add-captions-iphone.html","How to add captions"),
       ("styles.html","Caption styles"),("vs-capcut.html","HandCut vs CapCut"),("compare/","Compare apps"),("guides/","All guides"),
       ("support.html","Support"),("privacy.html","Privacy Policy"),("terms.html","Terms of Use")]

def head(path, title, desc, extra_ld=None):
    url = BASE + ("" if path == "index.html" else path.replace("index.html", ""))
    depth = path.count("/")
    pre = "../" * depth
    lds = [APP_LD] + ([extra_ld] if extra_ld else [])
    ld = "".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in lds)
    e = html.escape
    return pre, (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{e(title)}</title><meta name="description" content="{e(desc)}">'
        f'<link rel="canonical" href="{url}"><meta name="robots" content="index,follow">'
        f'<meta name="apple-itunes-app" content="app-id=6762062166">'
        f'<meta property="og:type" content="website"><meta property="og:site_name" content="HandCut">'
        f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">'
        f'<meta property="og:url" content="{url}"><meta property="og:image" content="{ICON}">'
        f'<meta property="og:image:width" content="512"><meta property="og:image:height" content="512">'
        f'<meta property="og:image:alt" content="HandCut app icon">'
        f'<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{e(title)}">'
        f'<meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{ICON}">'
        f'<link rel="icon" href="{pre}img/handcut-icon-512.jpg"><style>{CSS}</style>{ld}</head><body>'
        f'<div class="banner"><img src="{pre}img/handcut-icon-512.jpg" alt="" width="44" height="44">'
        f'<span><strong>HandCut</strong> for iPhone. {OFFER_LINE}</span>'
        f'<a class="b" href="{APP}">App Store</a></div>')

def foot(pre):
    links = " · ".join(f'<a href="{pre}{h if h!="./" else ""}">{t}</a>' if h!="./" else f'<a href="{pre or "./"}">{t}</a>' for h,t in NAV)
    return (f'<p><a class="b" href="{APP}">Download HandCut on the App Store</a></p>'
            f'<footer><nav>{links} · <a href="mailto:shuhrat.soliev@gmail.com">Contact</a></nav>'
            f'<p>HandCut is published by Daler Soliev. iPhone only, iOS 17 or later.</p></footer></body></html>')

def faq_ld(qas):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qas]}
def howto_ld(name, steps):
    return {"@context":"https://schema.org","@type":"HowTo","name":name,"tool":{"@type":"HowToTool","name":"HandCut for iPhone"},
            "step":[{"@type":"HowToStep","position":i+1,"text":s} for i,s in enumerate(steps)]}
def faq_html(qas): return "".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q,a in qas)
def steps_html(steps): return "<ol>" + "".join(f"<li>{html.escape(s)}</li>" for s in steps) + "</ol>"

FAQ = [
 ("Does HandCut add a watermark?", "No. HandCut never adds a watermark to any export."),
 ("Is HandCut free?", "HandCut is free to download and free to edit with. Exporting a video needs a HandCut Pro monthly subscription; the price is shown in the app before you buy. Existing purchases can be restored in the app."),
 ("Do I need an account?", "No. HandCut asks for no account and shows no ads."),
 ("How are captions made?", "Apple's on-device speech recognition transcribes your video on your iPhone, and HandCut times each caption to the spoken word. Audio is not uploaded."),
 ("Which languages are supported?", "Captions are built for English. Other languages work only where your iPhone's on-device speech model supports them; the export screen lists the ones your iPhone has. The app itself is in English."),
 ("Is HandCut on Android?", "No. HandCut is iPhone only, iOS 17 or later."),
]
STEPS = ["Install HandCut from the App Store and open it. No account is needed.",
         "Tap the button to pick a video from Photos.",
         "Open Captions and generate them. HandCut transcribes the speech on your iPhone and times each word.",
         "Tap any word to fix it, choose a caption style, and drag the captions where you want them.",
         "Tap Export. Captions are burned into the video, with no watermark. Exporting needs HandCut Pro; the price is shown in the app."]

BODY = {}
BODY["index.html"] = (None, f"""<h1>HandCut: auto captions that land on the word</h1>
<p>HandCut is a captions-first video editor for iPhone. It transcribes your video on the device and times every caption to the spoken word. No account, no ads, and never a watermark.</p>
<p><strong>{OFFER_LINE}</strong></p>
<h2>What you get</h2><ul>
<li>Word-by-word, karaoke-style auto captions; edit any word, restyle, move them anywhere on the frame</li>
<li>Burn captions into the video, or export an SRT file</li>
<li>Picture-in-picture: screen recording plus a facecam bubble plus captions</li>
<li>A real editor: multi-clip timeline, trim, split, reorder, 14 transitions, 0.25x to 4x speed, music and voiceover mixer, manual keyframes, reframe to vertical, square or widescreen</li>
<li>Export up to 4K, up to 60 fps, matching your footage</li></ul>
<h2>Free vs Pro</h2>
<p>Download and editing are free. Exporting needs HandCut Pro, a monthly subscription; the App Store price for your country is shown in the app before you buy. Pro also includes tools such as transcript editing (delete words to cut video), motion tracking, Smart Cutout, Auto-Reframe, denoise, Auto Match Look and version history. Existing purchases can be restored.</p>
<h2>Guides</h2><ul>
<li><a href="auto-captions-app.html">Auto captions app for iPhone</a></li>
<li><a href="add-subtitles-to-video-iphone.html">How to add subtitles to a video on iPhone</a></li>
<li><a href="video-editor-no-watermark.html">A video editor with no watermark</a></li>
<li><a href="how-to-add-captions-iphone.html">How to add captions on iPhone, step by step</a></li></ul>
<h2 id="faq">FAQ</h2>{faq_html(FAQ)}""", faq_ld(FAQ))

AUTO_FAQ = [
 ("Are the auto captions accurate?", "Accuracy depends on audio quality, accent and language. HandCut uses Apple's on-device recognition; you can tap any word to correct it before export."),
 ("Do auto captions work offline?", "Transcription runs on your iPhone with no network fallback. If a language is not available offline on your iPhone, HandCut tells you before you start."),
 ("Can I export the captions as a file?", "Yes. You can burn captions into the video or export an SRT file."),
] + FAQ[:2]
BODY["auto-captions-app.html"] = (None, f"""<h1>An auto captions app for iPhone that times every word</h1>
<p>Most people watch short video with the sound off. HandCut turns speech into captions on your iPhone, word by word, so the text appears exactly as each word is spoken.</p>
<p><strong>{OFFER_LINE}</strong></p>
<h2>How HandCut's auto captions work</h2><ul>
<li><strong>On-device transcription.</strong> Apple's speech recognition runs on your iPhone. Your audio is not uploaded.</li>
<li><strong>Word timing.</strong> Each caption follows the timing of the spoken words, with karaoke-style highlighting.</li>
<li><strong>Edit and style.</strong> Fix any word, change the look, and place captions anywhere on the frame.</li>
<li><strong>Export.</strong> Burn captions into the video with no watermark, or export SRT.</li></ul>
<h2>Who it is for</h2>
<p>Coaches, course creators, realtors, podcasters and anyone talking to camera who wants captions without a desktop editor.</p>
<h2>Languages</h2><p>Captions are built for English. Other languages work only where your iPhone's on-device speech model supports them, and the export screen lists the ones your iPhone has.</p>
<h2>FAQ</h2>{faq_html(AUTO_FAQ)}""", faq_ld(AUTO_FAQ))

SUB_STEPS = STEPS
BODY["add-subtitles-to-video-iphone.html"] = (None, f"""<h1>How to add subtitles to a video on iPhone</h1>
<p>You can add subtitles to a video on iPhone without a computer. With HandCut the subtitles are generated on the device and timed to each word.</p>
{steps_html(SUB_STEPS)}
<h2>Tips for better subtitles</h2><ul>
<li>Record close to the microphone and away from loud music; recognition is better with clean speech.</li>
<li>Keep two short lines on screen at most so viewers can read them at a glance.</li>
<li>Place subtitles above the bottom edge so app buttons on social platforms do not cover them.</li></ul>
<p><strong>{OFFER_LINE}</strong></p>""", howto_ld("How to add subtitles to a video on iPhone with HandCut", SUB_STEPS))

NW_FAQ = [
 ("Does HandCut ever add a watermark?", "No. There is no watermark on any export, and no branded end clip."),
 ("Is it a free video editor?", "Editing is free: import, captions, timeline, styles and keyframes. Exporting needs a HandCut Pro monthly subscription; the price is shown in the app before you buy."),
 ("What resolution can I export?", "Up to 4K, at up to 60 fps, following your footage."),
]
BODY["video-editor-no-watermark.html"] = (None, f"""<h1>A video editor for iPhone with no watermark</h1>
<p>HandCut never stamps your video. There is no logo in the corner and no branded clip at the end, whatever you make.</p>
<p><strong>{OFFER_LINE}</strong></p>
<h2>What you can do</h2><ul>
<li>Word-by-word auto captions made on your iPhone</li>
<li>Multi-clip timeline: trim, split, reorder, 14 transitions, speed 0.25x to 4x</li>
<li>Text, emoji and your own images; manual keyframes; mirror, crop and reframe</li>
<li>Music and voiceover tracks with a mixer; picture-in-picture facecam</li>
<li>Export up to 4K, up to 60 fps, with no watermark</li></ul>
<h2>Honest about the price</h2>
<p>You can download HandCut and edit for free. Exporting needs HandCut Pro, a monthly subscription. The App Store price for your country is shown in the app before you buy, and you can cancel anytime in your Apple Account settings.</p>
<h2>FAQ</h2>{faq_html(NW_FAQ)}""", faq_ld(NW_FAQ))

BODY["how-to-add-captions-iphone.html"] = (None, f"""<h1>How to add captions to a video on iPhone</h1>
{steps_html(STEPS)}
<p>See also: <a href="add-subtitles-to-video-iphone.html">how to add subtitles to a video on iPhone</a> and <a href="auto-captions-app.html">how HandCut's auto captions work</a>.</p>""", howto_ld("How to add captions to a video on iPhone with HandCut", STEPS))

BODY["vs-capcut.html"] = (None, """<h1>HandCut vs CapCut for captions</h1>
<p>For the full, regularly updated comparison see <a href="compare/handcut-vs-capcut/">HandCut vs CapCut: the detailed comparison</a>.</p>
<p>CapCut is the bigger editor, with templates and trending effects on more platforms. Pick CapCut if you build from templates. Pick HandCut if you mainly need word-by-word captions on talking-to-camera video on your iPhone, with no watermark and no account.</p>
<table><tr><th></th><th>HandCut</th><th>CapCut</th></tr>
<tr><td>Watermark</td><td>None on any export</td><td>CapCut says exports are usually watermark-free, but many templates add a branded ending clip you delete by hand, and Pro templates need CapCut Pro to export without a watermark</td></tr>
<tr><td>Captions</td><td>Word-by-word karaoke captions, transcribed on-device; burn in or export SRT</td><td>Auto captions built into a full editor</td></tr>
<tr><td>Price</td><td>Edit free; exporting needs HandCut Pro, a monthly subscription priced in the app</td><td>See CapCut's current pricing</td></tr>
<tr><td>Platforms</td><td>iPhone only (iOS 17+)</td><td>Mobile app, desktop and online editor</td></tr>
<tr><td>Account</td><td>None needed</td><td>See CapCut's current terms</td></tr></table>
<p><small>CapCut details from CapCut's own help pages (capcut.com/help: remove-watermark-when-exporting-video, download-template-video-without-watermark, paid-template), checked 11 October 2026. CapCut features change; check their site for the latest. CapCut is a trademark of its owner; HandCut is not affiliated with it.</small></p>""", None)

BODY["compare/index.html"] = (None, """<h1>HandCut compared with other “auto captions” apps</h1>
<p>Facts below are copied from Apple’s public iTunes Search API (US store) on 30 October 2026: the top results for “auto captions”. Ratings and sizes change; follow each link for the current listing. We make no claims about other apps’ features.</p>
<table><tr><th>App</th><th>Seller</th><th>Rating (count)</th><th>Price to download</th><th>Size</th></tr>
<tr><td><a href='https://apps.apple.com/us/app/id6762062166'>Handcut: Auto Captions Video</a></td><td>Daler Soliev</td><td>3.7 (3)</td><td>Free (export needs a subscription)</td><td>11 MB</td></tr>
<tr><td><a href='https://apps.apple.com/us/app/auto-caption-video-subtitles/id1659145800'>Auto Caption Video Subtitles</a></td><td>Take Agency, LLC</td><td>4.8 (920)</td><td>Free</td><td>323 MB</td></tr>
<tr><td><a href='https://apps.apple.com/us/app/auto-captions-video-subtitles/id655895351'>Auto Captions: Video Subtitles</a></td><td>Fitness Labs SRL</td><td>4.6 (1,494)</td><td>Free</td><td>113 MB</td></tr>
<tr><td><a href='https://apps.apple.com/us/app/captions-ai-edits-your-video/id1541407007'>Captions: AI Edits Your Video</a></td><td>Captions, LLC</td><td>4.7 (38,877)</td><td>Free</td><td>236 MB</td></tr>
<tr><td><a href='https://apps.apple.com/us/app/autocap-auto-video-captions/id1466743701'>AutoCap: Auto Video Captions</a></td><td>Zipo Apps Ltd.</td><td>4.7 (794)</td><td>Free</td><td>170 MB</td></tr>
<tr><td><a href='https://apps.apple.com/us/app/auto-captions-ai-teleprompter/id6776611961'>Auto Captions: AI Teleprompter</a></td><td>IDENTIQ INFOTECH</td><td>0 (0)</td><td>Free</td><td>25 MB</td></tr></table>
<p>“Price to download” is the App Store download price. Most of these apps sell in-app purchases or subscriptions; check each listing.</p>
<h2>What HandCut does</h2><ul>
<li>Per-word caption timing read from the audio, with karaoke highlighting</li>
<li>On-device transcription; no account and no ads</li>
<li>Picture-in-picture facecam bubble, multi-clip timeline, speed 0.25x to 4x, manual keyframes</li>
<li>Export up to 4K with no watermark</li></ul>
<h2>Price</h2><p>Free to download and to edit. Exporting needs HandCut Pro, a monthly subscription; the price is shown in the app. Existing purchases can be restored.</p>""", None)

BODY["app.html"] = (None, f"""<h1>HandCut: Auto Captions Video</h1>
<p>Word-by-word captions for iPhone. Transcription runs on your iPhone with no upload and no account. Karaoke highlighting, picture-in-picture, keyframes, 4K export, no watermark.</p>
<p><strong>{OFFER_LINE}</strong></p>
<h2>What it does</h2><ul>
<li>Per-word caption timing read from the audio, with karaoke highlighting</li>
<li>On-device transcription; no account, no ads</li>
<li>Picture-in-picture facecam bubble</li>
<li>Multi-clip timeline, speed 0.25x to 4x, manual keyframes</li>
<li>Export up to 4K, no watermark</li></ul>
<h2>Plan</h2><p>Free to download and to edit. Exporting needs HandCut Pro, a monthly subscription; the price is shown in the app before you buy. Existing purchases can be restored in the app.</p>""", None)

def frag(name):
    """Body of an old fragment page, with HTML comments removed."""
    import re
    # The fragments were replaced by generated pages in bd52c46; read the originals from ae24e59.
    import subprocess
    s = subprocess.run(["git", "show", "ae24e59:" + name], capture_output=True, text=True, check=True).stdout
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    return s

import re
styles = frag("styles.html")
styles = styles.replace("Handcut", "HandCut").replace("<h1>HandCut — Caption styles</h1>", "<h1>HandCut caption styles</h1>")
styles = re.sub(r"<li><strong>No watermark, ever.</strong> Free tier included\. There is no version of\s*HandCut that brands your video for you\.</li>",
                "<li><strong>No watermark, ever.</strong> There is no version of HandCut that brands your video for you.</li>", styles)
styles = styles.replace("Every export leaves HandCut with <strong>no watermark</strong>\non any tier", "Every export leaves HandCut with <strong>no watermark</strong>")
styles = styles.replace("Included free alongside Lantern and\nSilk.", "Available alongside Lantern and Silk.")
styles = styles.replace("It works, it ships, and it is free; it is just not finished.", "It works and it ships; it is just not finished.")
styles = styles.replace("<p>Full technical specification, including every contrast measurement and the rules that\nchoose the emphasised word: see the design notes shipped with the source.</p>", "")
styles += f"<p>Caption styles are part of editing, which is free. Exporting needs HandCut Pro; the price is shown in the app.</p>"
BODY["styles.html"] = (None, styles, None)

SUPPORT_FAQ = [
 ("What is free, and what needs Pro?", "Downloading and editing are free. Exporting needs HandCut Pro, a monthly subscription; the App Store price for your country is shown in the app before you buy. Pro also adds tools such as transcript editing, motion tracking, Smart Cutout, Auto-Reframe, denoise, Auto Match Look and version history. If you had HandCut before the 4.3 update, you keep the editor you already had."),
 ("I already paid. How do I get Pro back?", "Tap Restore purchases in the app. Earlier subscriptions and lifetime purchases stay valid. Manage subscriptions in Settings, your name, Subscriptions."),
 ("Does HandCut add a watermark?", "No. Never, on any export."),
 ("Do captions work offline?", "Transcription runs on your iPhone using Apple's on-device speech recognition, with no network fallback. Captions are built for English; other languages work only where your iPhone's on-device speech model supports them. The export screen lists the languages your iPhone has, and HandCut says so before you start if a language is missing."),
 ("Why is there no music library?", "Licensing one would mean a server, accounts and a very different app. You can add your own audio."),
 ("Do I need an account?", "No. There is no sign-up, login or password."),
 ("Where do my projects live? Do they sync?", "Your media never leaves your device. The small project file describing your cuts syncs through your own iCloud backup, which we cannot access. The media itself is excluded from that backup and can be re-imported from Photos."),
]
BODY["support.html"] = (None, f"""<h1>HandCut support</h1>
<p>Questions, bugs, or anything that looks wrong: <a href="mailto:shuhrat.soliev@gmail.com"><strong>shuhrat.soliev@gmail.com</strong></a>. We reply within 2 business days.</p>
<p><strong>{OFFER_LINE}</strong></p>
<h2>Frequently asked</h2>{faq_html(SUPPORT_FAQ)}""", faq_ld(SUPPORT_FAQ))

priv = frag("privacy.html").replace("Handcut", "HandCut")
priv = priv.replace("<h1>Privacy Policy — HandCut</h1>", "<h1>HandCut privacy policy</h1>")
priv = priv.replace("Effective 1 August 2026 (updated 12 November 2026).", "Effective 1 August 2026 (updated 18 November 2026).")
priv = priv.replace("There is no account, no analytics, no advertising identifier,", "There is no account, no analytics that leave your iPhone, no advertising identifier,")
priv = re.sub(r"<hr>\s*<p><em>Reviewed by counsel\? Not yet\.</em>.*?</p>", "", priv, flags=re.S)
priv = priv.replace("<h2>Purchases</h2>", "<h2>On-device counters</h2>\n<p>To improve the app, HandCut keeps a few simple counters on your iPhone, for example how many times the export subscription sheet was shown or dismissed. They are numbers stored in the app's own settings on this device only. They contain no identifier and are never sent to us or anyone else.</p>\n\n<h2>Purchases</h2>")
BODY["privacy.html"] = (None, priv, None)

terms = frag("terms.html").replace("Handcut", "HandCut")
terms = terms.replace("<h1>Terms of Use — HandCut</h1>", "<h1>HandCut terms of use</h1>")
terms = terms.replace("Effective 1 August 2026 (updated 12 November 2026).", "Effective 1 August 2026 (updated 18 November 2026).")
terms = terms.replace("""collect them, we cannot see them, and there is no account to create. Pay us or do not —
either way there is no watermark on your exports.</p>""", """collect them, we cannot see them, and there is no account to create. Editing is free;
exporting needs a HandCut Pro subscription. There is never a watermark on your exports.</p>""")
terms = terms.replace("""User License Agreement</a>. There is no project limit and no video-length limit on any
tier, including the free one.</p>""", """User License Agreement</a>.</p>""")
terms = re.sub(r"<p><strong>New users, existing users, and HandCut Pro\.</strong>.*?</p>", """<p><strong>Free editing and HandCut Pro.</strong> Downloading HandCut and editing are free.
Exporting a video needs HandCut Pro, a monthly subscription; the App Store price for your
country is shown in the app before you buy. Installs from before the 4.3 update keep the
editor they already had. Some additional tools shown in the app are part of HandCut Pro.</p>""", terms, flags=re.S)
terms = re.sub(r"<p>The current HandCut Pro offer for new customers is a monthly subscription from\s*US\$1/month in the US, or the local equivalent shown in the app before you buy\.", "<p>The current HandCut Pro offer for new customers is a monthly subscription. The price for\nyour country is shown in the app before you buy.", terms)
terms = re.sub(r"<hr>\s*<p><em>Reviewed by counsel\? Not yet\.</em>.*?</p>\s*<p><strong>This is not legal advice\.</strong>.*?</p>", "", terms, flags=re.S)
BODY["terms.html"] = (None, terms, None)

for path, title, desc in PAGES:
    _, body, ld = BODY[path]
    pre, h = head(path, title, desc, ld)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    open(path, "w").write(h + body.strip() + foot(pre))

# sitemap
urls = [BASE + ("" if p == "index.html" else p.replace("index.html", "")) for p, _, _ in PAGES]
# Keep every URL other workers added (guides, /for/, /features/, /compare/<name>/, /pt-br/, /es/).
if os.path.exists("sitemap.xml"):
    for u in re.findall(r"<loc>([^<]+)</loc>", open("sitemap.xml").read()):
        if u not in urls: urls.append(u)
open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
json.dump({"@context":"https://schema.org","@graph":[{k:v for k,v in APP_LD.items() if k!="@context"}]}, open("schema.jsonld","w"), ensure_ascii=False, indent=1)
json.dump(APP_LD, open("schema-app.jsonld","w"), ensure_ascii=False, indent=1)
print("built", len(PAGES), "pages")
