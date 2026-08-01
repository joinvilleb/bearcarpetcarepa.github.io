#!/usr/bin/env bash
#
# Builds the production assets and regenerates every page.
#
#   css/site.css      hand-written, no framework. Minified to site.min.css.
#   js/*.js           minified to *.min.js, which is what the pages load.
#   build-pages.py    renders the nine HTML pages from one set of facts.
#
# Run after editing any source file:  ./build.sh
#
set -euo pipefail
cd "$(dirname "$0")"

echo "→ minifying CSS"
npx --yes clean-css-cli -O1 -o css/site.min.css css/site.css

echo "→ minifying JavaScript"
for f in main contact; do
  npx --yes terser "js/$f.js" --compress --mangle --output "js/$f.min.js"
done

echo "→ generating pages"
python3 build-pages.py

printf '\n%-22s %s bytes\n' "site.css:"       "$(wc -c < css/site.css | tr -d ' ')"
printf '%-22s %s bytes\n'   "site.min.css:"   "$(wc -c < css/site.min.css | tr -d ' ')"
printf '%-22s %s bytes\n'   "  gzipped:"      "$(gzip -c css/site.min.css | wc -c | tr -d ' ')"
printf '%-22s %s bytes\n'   "main.min.js:"    "$(wc -c < js/main.min.js | tr -d ' ')"
printf '%-22s %s bytes\n'   "contact.min.js:" "$(wc -c < js/contact.min.js | tr -d ' ')"
