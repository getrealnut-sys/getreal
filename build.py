#!/usr/bin/env python3
"""Builds the Get Real Integrative Health site into docs/ (served by GitHub Pages).

Edit content in src/, then run:  python3 build.py
- src/data/site.json         booking link, email, Instagram, site address
- src/data/guides.json       the free guides, in learning-path order (Resources cards, guide headers, "Next" cards)
- src/data/books.json        the short reads shown on Resources
- src/data/study-areas.json  the "Areas of study" list on About
- src/data/pages.json        page titles and search descriptions
- src/pages/, src/guides/    page content;  src/layout/ shared header and footer
"""
import html, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(ROOT, 'src'), os.path.join(ROOT, 'docs')


def rd(*p):
    with open(os.path.join(SRC, *p), encoding='utf-8') as f:
        return f.read()


def data(name):
    return json.loads(rd('data', name))


def esc(v):
    return html.escape(str(v), quote=True)


def fill(tpl, values):
    """Replace {{key}} with escaped values; unknown placeholders are an error."""
    def rep(m):
        k = m.group(1)
        if k not in values:
            raise KeyError(f'no value for {{{{{k}}}}}')
        v = values[k]
        return str(v) if isinstance(v, Raw) else esc(v)
    return re.sub(r'\{\{([a-z_:.\-]+)\}\}', rep, tpl)


class Raw(str):
    """Already-built HTML, inserted as is."""


site = data('site.json')
layout = data('layout.json')
guides = data('guides.json')
books = data('books.json')
areas = data('study-areas.json')
end_card = data('guide-end-card.json')
pages = data('pages.json')

NAV_ACTIVE = 'color: #7C5E26; text-decoration: none; border-bottom: 1px solid #B8924A; padding-bottom: 2px'
NAV_PLAIN = 'color: #1B2F47; text-decoration: none; '
NAV_KEYS = {'about.html': 'about', 'work-with-me.html': 'work', 'integrative-health.html': 'integrative', 'resources.html': 'resources'}

FAVICON = ("data:image/svg+xml," + "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Ccircle cx='32' cy='32' r='30' fill='%23F7F4EE' stroke='%23B8924A' stroke-width='2'/%3E"
           "%3Ctext x='32' y='38' text-anchor='middle' font-family='sans-serif' font-size='18' letter-spacing='1' fill='%23B8924A'%3EGR%3C/text%3E%3C/svg%3E")

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{page_title}}</title>
<meta name="description" content="{{description}}">
<link rel="canonical" href="{{canonical}}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Get Real Integrative Health">
<meta property="og:title" content="{{page_title}}">
<meta property="og:description" content="{{description}}">
<meta property="og:url" content="{{canonical}}">
<meta name="theme-color" content="#14304F">
<link rel="icon" href="{{favicon}}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Jost:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{root}}assets/site.css">
</head>
<body>
<div style="{{wrapper_style}}">
'''
TAIL = '\n</div>\n</body>\n</html>\n'


def render(body, out, title, description, extra=None):
    root = '../' * out.count('/')
    section = 'resources' if out.startswith('guides/') else NAV_KEYS.get(out)  # guides sit under Resources
    nav = {f'nav_style:{k}': (NAV_ACTIVE if section == k else NAV_PLAIN) for k in NAV_KEYS.values()}
    common = {'root': root, 'booking_url': site['booking_url'], 'email': site['email'],
              'instagram_url': site['instagram_url'], **nav}
    vals = dict(common)
    vals['header'] = Raw(fill(rd('layout', 'header.html'), common))
    vals['footer'] = Raw(fill(rd('layout', 'footer.html'), common))
    vals.update(extra or {})
    canonical = site['site_url'].rstrip('/') + '/' + ('' if out == 'index.html' else out)
    head = fill(HEAD, {'page_title': title, 'description': description, 'canonical': canonical,
                       'favicon': FAVICON, 'root': root, 'wrapper_style': layout['wrapper_style']})
    html_out = head + fill(body, vals).strip() + TAIL
    path = os.path.join(OUT, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html_out)


def items(tpl_name, rows, extra=lambda i, r: {}):
    tpl = rd('templates', tpl_name)
    return ''.join(fill(tpl, {**r, **extra(i, r)}) for i, r in enumerate(rows))


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, 'assets'))
    shutil.copy(os.path.join(SRC, 'assets', 'site.css'), os.path.join(OUT, 'assets', 'site.css'))
    open(os.path.join(OUT, '.nojekyll'), 'w').close()

    guide_cards = Raw(''.join(
        fill(rd('templates', 'guide-card-featured.html' if i == 0 else 'guide-card.html'),
             {**g, 'root': '', 'card_label': ('Start here · ' if i == 0 else '') + f'Step {i + 1}'})
        for i, g in enumerate(guides)))
    lists = {'list:study-areas': Raw(items('study-area.html', areas)),
             'list:guides': guide_cards,
             'list:books': Raw(items('book.html', books))}

    for p in pages:
        render(rd('pages', p['file']), p['file'], p['title'], p['description'], lists)

    for i, g in enumerate(guides):
        out = f"guides/{g['slug']}.html"
        root = '../'
        if i + 1 < len(guides):
            n = guides[i + 1]
            nxt = {'href': f"guides/{n['slug']}.html", 'label': f'Next · Step {i + 2}', 'title': n['title'], 'subtitle': n['subtitle']}
        else:
            nxt = {'href': 'resources.html', **end_card}
        nxt_html = fill(rd('templates', 'guide-next.html'), {**nxt, 'root': root})
        extra = {'guide.step': i + 1, 'guide.total': len(guides), 'guide.title': g['title'],
                 'guide.subtitle': g['subtitle'], 'guide.time': g['time'], 'guide_next': Raw(nxt_html)}
        render(rd('guides', g['slug'] + '.html'), out, f"{g['title']} — Get Real Integrative Health",
               f"{g['subtitle']}. {g['blurb']}", extra)

    if site.get('booking_url_is_placeholder'):
        print('NOTE: booking_url in src/data/site.json is still a placeholder. Set the real booking link before launch.')
    if site.get('custom_domain'):
        with open(os.path.join(OUT, 'CNAME'), 'w') as f:
            f.write(site['custom_domain'] + '\n')
    print(f'Built {len(pages) + len(guides)} pages into docs/')


if __name__ == '__main__':
    try:
        build()
    except KeyError as e:
        sys.exit(f'Build failed: {e}')
