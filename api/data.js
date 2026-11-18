// Returns the dashboard data, only to a caller who sends the right password.
// The data lives in the DASH_DATA environment variable (gzip + base64 JSON),
// set in Vercel project settings. It is never stored in this repo.
const zlib = require('zlib');
const crypto = require('crypto');

function same(a, b) {
  const x = Buffer.from(String(a || ''));
  const y = Buffer.from(String(b || ''));
  return x.length === y.length && crypto.timingSafeEqual(x, y);
}

module.exports = (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  const pass = process.env.DASH_PASSWORD;
  const packed = process.env.DASH_DATA;
  if (!pass || !packed) {
    res.status(503).json({ error: 'Dashboard is not configured yet.' });
    return;
  }
  if (!same(req.headers['x-dash-key'], pass)) {
    res.status(401).json({ error: 'Wrong password.' });
    return;
  }
  try {
    const json = zlib.gunzipSync(Buffer.from(packed, 'base64')).toString('utf8');
    res.setHeader('Content-Type', 'application/json');
    res.status(200).send(json);
  } catch (e) {
    res.status(500).json({ error: 'Stored data could not be read.' });
  }
};
