# SIP Monthly

The monthly SIP revenue dashboard. It has five tabs:

- **Insights:** the headline net change, department cards, the revenue bridge, the biggest movers and the review's findings.
- **Overview:** KPI tiles, an "Aug = 100" index chart and the subs-vs-value-per-sub map.
- **Departments:** a scorecard, plus a drill-down per department.
- **Order types:** a scorecard and a department × order-type heatmap, plus a drill-down per order type.
- **Outlook:** a 12-month trend for any department and order type, projected at the current rate and 1.5× faster, with months to critical and a watchlist.

## What's here

- `dashboard/page.html` is the dashboard page. It runs inside a Claude Data artifact, which supplies the `dash` runtime, d3 and the design tokens. It contains no business figures.
- `data/README.md` lists the data files the page reads and their fields. The data itself is never committed.
- `scripts/build_lines.py` converts the SIP LTV sheet export into `data/lines.json` for the Outlook tab.

## Outlook rules

- Baseline: the average of the last 6 months.
- Trend: a straight-line fit over those 6 months.
- Critical: 10% below the baseline for Recurring and All order types, 30% below for every other order type. Warning is halfway to critical.
- Lines averaging under 50 subs a month are not projected.

## Hosting on Vercel

- `public/index.html` is the standalone site, built from `dashboard/page.html` with `python3 scripts/build_site.py`. It loads the data from `/api/data`.
- `api/data.js` serves the data from the `DASH_DATA` Vercel environment variable (all data files packed into one string with `python3 scripts/pack_data.py data/`). The data never goes in this repo.
- There is no dashboard password. Access is controlled by Vercel's login protection on the project, so keep it on: anyone who gets past it can see the numbers.
- To refresh the numbers each month: rebuild the data files, re-pack them, paste the result into `DASH_DATA` in Vercel, and redeploy.
