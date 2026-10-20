// Verifex frontend runtime configuration.
//
// The UI is hosted as static files (Vercel) while the Python inference API runs
// on a separate origin (a Hugging Face Space), so the frontend has to be told
// where to send its requests. This value is not a secret: the Space is public and
// the API requires no credentials.
(function () {
  // Set to the deployed backend once the Hugging Face Space exists, e.g.
  // "https://synthetica-pj-verifex.hf.space"
  var PRODUCTION_API_BASE = "";

  // "" means same origin, which is what local development and the bundled
  // fallback UI (the Python server serving this same folder) rely on.
  var host = window.location.hostname;
  var isLocalHost = host === "localhost" || host === "127.0.0.1" || host === "";

  window.__VERIFEX_API_BASE__ = isLocalHost ? "" : PRODUCTION_API_BASE;
})();
