// ---------------------------------------------------------------------------
// SITE CONFIG - the single source of truth for this site.
// Every name, contact and colour on the page reads from here. Nothing is
// hardcoded in index.html or style.css. Same rule as the repo: the brand
// lives in one place (BRAND.md decides the values; this file carries them
// to the site). All values below are PLACEHOLDERS until the handles exist.
// ---------------------------------------------------------------------------

window.SITE_CONFIG = {
  COMPANY_NAME: "<COMPANY NAME - from BRAND.md, under review>",
  TAGLINE: "<TAGLINE - from BRAND.md>",
  EMAIL: "<EMAIL>",
  MOBILE: "<MOBILE>",
  ABN: "<ABN>",
  ACCENT_COLOUR: "#1462A0",   // Chalk Blue per BRAND.md - change here, nowhere else
  FORM_ENDPOINT: ""           // e.g. a Formspree/Basin URL. Empty = form disabled,
                              // the page says to text the plans instead.
};
