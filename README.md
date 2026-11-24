# Get Real Integrative Health website

The site for getrealintegrative.com, built from Maria's approved design. Plain HTML and CSS, served by GitHub Pages from the `docs/` folder.

## Changing content

Edit files in `src/`, then run `python3 build.py`. It rewrites `docs/`.

| What | Where |
| --- | --- |
| Booking link (every "Book your consultation" button) | `src/data/site.json` → `booking_url` |
| Footer email, Instagram, site address | `src/data/site.json` |
| Free guides, in learning-path order | `src/data/guides.json` |
| Short reads (books) | `src/data/books.json` |
| Areas of study on About | `src/data/study-areas.json` |
| Page titles and search descriptions | `src/data/pages.json` |
| Page content | `src/pages/`, `src/guides/` |
| Shared menu and footer | `src/layout/` |

Adding a guide: add its page to `src/guides/<slug>.html` and an entry to `guides.json`. The Resources cards, "Step N of N" labels and "Next" cards update themselves.

## Before launch

- `booking_url` is still a placeholder. Set it to the Google Calendar booking page and set `booking_url_is_placeholder` to `false`.
- The portrait on Home and About is a placeholder until the photo shoot.
- The footer email stays getrealnut@gmail.com until maria@getrealintegrative.com exists.
- Custom domain: once the Namecheap DNS records are in, set `custom_domain` in `site.json` to `getrealintegrative.com` and rebuild. That writes `docs/CNAME`.

## Publishing

GitHub Pages → Deploy from a branch → `main`, folder `/docs`.

`src/assets/motion-ideas.css` holds optional motion and scroll ideas that are not used on the site yet.
