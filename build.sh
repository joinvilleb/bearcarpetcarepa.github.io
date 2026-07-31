#!/usr/bin/env bash
#
# Builds the production assets: css/site.min.css plus the minified JS.
#
#   css/style.css   Bootstrap 4.5.3 + the original template theme.
#                   Purged against the HTML, because the pages use a small
#                   fraction of Bootstrap and it was shipping ~196KB.
#   css/icons.css   Generated icon set that replaced the Font Awesome CDN.
#   css/revamp.css  Mobile-first layer. Must load last so it wins.
#
# Re-run this after editing any of the three sources:
#   ./build.sh
#
set -euo pipefail
cd "$(dirname "$0")"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Classes that only ever appear at runtime, so PurgeCSS cannot see them
# in the markup: JS toggles the first group, the form renders the alerts.
SAFELIST=(
  show collapsing is-visible is-invalid
  alert alert-success alert-danger
  fade active disabled
)

echo "→ purging css/style.css against the HTML"
npx --yes purgecss \
  --css css/style.css \
  --content '*.html' 'js/*.js' \
  --safelist "${SAFELIST[@]}" \
  --output "$TMP/"

echo "→ concatenating purged base + icons + revamp"
cat "$TMP/style.css" css/icons.css css/revamp.css > "$TMP/bundle.css"

echo "→ minifying"
# Level 1 only: level 2 merges and reorders rules, which breaks the
# deliberate source order these three files depend on.
npx --yes clean-css-cli -O1 -o css/site.min.css "$TMP/bundle.css"

echo "→ minifying JavaScript"
for f in main contact; do
  npx --yes terser "js/$f.js" --compress --mangle --output "js/$f.min.js" 2>/dev/null
done

printf '\n%-22s %s\n' "style.css (source):" "$(wc -c < css/style.css | tr -d ' ') bytes"
printf '%-22s %s\n'   "purged base:"        "$(wc -c < "$TMP/style.css" | tr -d ' ') bytes"
printf '%-22s %s\n'   "site.min.css:"       "$(wc -c < css/site.min.css | tr -d ' ') bytes"
printf '%-22s %s\n'   "site.min.css (gzip):" "$(gzip -c css/site.min.css | wc -c | tr -d ' ') bytes"
printf '%-22s %s\n'   "main.min.js:"        "$(wc -c < js/main.min.js | tr -d ' ') bytes"
printf '%-22s %s\n'   "contact.min.js:"     "$(wc -c < js/contact.min.js | tr -d ' ') bytes"
