"""Pack the dashboard data files into one string for the DASH_DATA environment variable.

Usage: python3 scripts/pack_data.py data/ > packed.txt
Then paste packed.txt into Vercel > Project > Settings > Environment Variables as DASH_DATA
(type Sensitive), and redeploy. Never commit packed.txt or the data folder.
"""
import base64, gzip, json, os, sys

NAMES = ['monthly', 'depts', 'order_overall', 'dept_order', 'bridge', 'notes', 'lines']

folder = sys.argv[1] if len(sys.argv) > 1 else 'data'
data = {n: json.load(open(os.path.join(folder, n + '.json'), encoding='utf8')) for n in NAMES}
raw = json.dumps(data, separators=(',', ':')).encode()
packed = base64.b64encode(gzip.compress(raw, 9)).decode()
if len(packed) > 60000:
    sys.exit('Packed data is %d characters; Vercel allows about 64 KB of environment variables.' % len(packed))
print(packed)
