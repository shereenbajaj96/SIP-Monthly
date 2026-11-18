"""Turn the SIP LTV sheet (CSV export) into data/lines.json for the Outlook tab.

Usage: python3 scripts/build_lines.py path/to/sip_ltv_export.csv data/lines.json
The CSV and the JSON it produces stay out of git (see .gitignore).
"""
import csv, json, sys

DEPTS = {'SIP Overall': 'All departments', 'Telecalling': 'Telecalling', 'DM + Comms': 'DM + Comms',
         'Platform + Ref + Upd + sh': 'Platform', 'NULL': 'Unattributed', 'SEO + SM + Oth': 'SEO / SM'}
ORDERS = {'Fresh subscriptions': 'Fresh', 'Upsell subscriptions': 'Upsell', 'Re-activation': 'Re-activation',
          'Cancelled Reonboard': 'Cancelled re-onboard', 'Lapsed Reonboard': 'Lapsed re-onboard', 'Recurring': 'Recurring'}
FIELDS = {'Subscriptions charged': 'subs', 'Total Revenue': 'revenue'}


def num(s):
    try:
        return float(s.replace(',', '').strip())
    except ValueError:
        return None


def main(src, dst):
    rows = list(csv.reader(open(src, encoding='utf8')))
    months = [m.replace(' - ', '-').strip() for m in rows[1][1:] if m.strip()]
    months = [m for m in months if '-' in m]
    n = len(months)
    dept = order = None
    got = {}
    for r in rows:
        k = r[0].strip()
        if k in DEPTS:
            dept, order = DEPTS[k], None
            continue
        if k in ORDERS:
            order = ORDERS[k]
            continue
        f = FIELDS.get(k)
        if dept and order and f and (dept, order, f) not in got:
            got[(dept, order, f)] = [num(x) for x in r[1:1 + n]]
    out = []
    for d, o in sorted({(d, o) for d, o, _ in got}):
        s, rv = got[(d, o, 'subs')], got[(d, o, 'revenue')]
        for i, m in enumerate(months):
            out.append({'dept': d, 'order': o, 'month': m, 'idx': i,
                        'subs': s[i] or 0, 'revenue_L': round((rv[i] or 0) / 1e5, 4)})
    json.dump(out, open(dst, 'w'))
    print(f'{len(out)} rows, {months[0]} to {months[-1]}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
