// Returns the dashboard data. Access is controlled by Vercel's own login protection on the project.
// The data lives in the DASH_DATA environment variable (gzip + base64 JSON),
// set in Vercel project settings. It is never stored in this repo.
const zlib = require('zlib');

module.exports = (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  const packed = process.env.DASH_DATA;
  if (!packed) {
    res.status(503).json({ error: 'Dashboard is not configured yet.' });
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
