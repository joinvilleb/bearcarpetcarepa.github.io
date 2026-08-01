# Pointing carpetcleanerharrisburg.com at bearcarpetcare.com

`carpetcleanerharrisburg.com` is not part of this repository. It is hosted on a
separate site builder, so the redirect has to be set up **there or at your DNS
provider**, not here. Everything below is for you or whoever manages that domain.

## What to do

Use a **301 (permanent) redirect**, not a 302 and not a forwarding frame. A 301
passes the accumulated ranking signals to bearcarpetcare.com; a 302 does not,
and a frame keeps the old domain in the address bar and hides the new site from
search engines entirely.

Redirect **page to matching page**, not everything to the home page. Google
treats a mass redirect to one URL as a soft 404 and drops the value.

| carpetcleanerharrisburg.com | bearcarpetcare.com |
|---|---|
| `/` | `/` |
| `/about_us` | `/about.html` |
| `/carpet-cleaning` | `/carpet-cleaning.html` |
| `/stain-removal` | `/carpet-cleaning.html` |
| `/pet-stain-removal` | `/carpet-cleaning.html` |
| `/area-rug-cleaning` | `/oriental-rug-cleaning.html` |
| `/oriental-rug-cleaning` | `/oriental-rug-cleaning.html` |
| `/testimonials` | `/reviews.html` |
| `/gallery` | `/gallery.html` |
| `/contact` | `/contact.html` |
| anything else | `/` |

There is no upholstery page on the old site, so nothing maps to
`/upholstery-cleaning.html`.

## Where to set it

**If the domain stays on its current builder** (Wix, Squarespace, GoDaddy
Website Builder and similar all have this): look for *Settings → Domains → 
Forwarding* or *URL redirects*. Add one rule per row above, type "permanent /
301". Some builders only offer whole-domain forwarding, in which case forward
everything to `https://bearcarpetcare.com/` and accept the loss of the
page-level mapping.

**If you move the domain to a host that serves files**, drop this in the root:

```
# _redirects  (Netlify / Cloudflare Pages)
/about_us              https://bearcarpetcare.com/about.html            301!
/carpet-cleaning       https://bearcarpetcare.com/carpet-cleaning.html  301!
/stain-removal         https://bearcarpetcare.com/carpet-cleaning.html  301!
/pet-stain-removal     https://bearcarpetcare.com/carpet-cleaning.html  301!
/area-rug-cleaning     https://bearcarpetcare.com/oriental-rug-cleaning.html 301!
/oriental-rug-cleaning https://bearcarpetcare.com/oriental-rug-cleaning.html 301!
/testimonials          https://bearcarpetcare.com/reviews.html          301!
/gallery               https://bearcarpetcare.com/gallery.html          301!
/contact               https://bearcarpetcare.com/contact.html          301!
/*                     https://bearcarpetcare.com/:splat                301!
```

**Cloudflare** (if DNS is there): Rules → Redirect Rules → *Create*, matching
`hostname eq "carpetcleanerharrisburg.com"`, dynamic target
`concat("https://bearcarpetcare.com", http.request.uri.path)`, status 301.

## Do these at the same time

1. **Update the Google Business Profile website link** to
   `https://bearcarpetcare.com/`. This is the important one. The profile
   currently points at the old domain, and that link is where a lot of the
   traffic comes from.
2. Update the website link on **Yelp, Facebook, Instagram, TikTok and YouTube**
   for the same reason.
3. Keep the old domain **registered and renewing**. If it lapses, every link
   pointing at it dies, including any the redirect was passing value through.
4. In **Google Search Console**, add both properties and use *Settings →
   Change of address* on the old one once the redirects are live.
5. Leave the redirects in place permanently. There is no point at which
   removing them helps.

## Checking it worked

```bash
curl -sI https://carpetcleanerharrisburg.com/carpet-cleaning | head -5
```

You want `HTTP/2 301` and a `location:` header pointing at the
bearcarpetcare.com equivalent. If you see `200`, it is serving the old page
rather than redirecting. If you see `302`, change it to permanent.
