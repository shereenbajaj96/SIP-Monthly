# Data files

No business data is kept in this repo. Every figure the dashboard shows is loaded at runtime from the files below, and `.gitignore` blocks anything else placed in this folder.

Each file is a JSON array of objects. The fields each file needs:

| File | One row per | Fields |
|---|---|---|
| `monthly.json` | Month (Aug, Sep, Oct) | `month`, `revenue_L`, `subs_charged`, `avg_value`, `cancellations`, `churn_pct`, `active_subs`, `rev_delta_prev_L` |
| `depts.json` | Department | `dept`, `full_name`, `share_pct`, `rev_sep_L`, `rev_oct_L`, `rev_delta_L`, `rev_pct`, `subs_sep`, `subs_oct`, `subs_delta`, `active_sep`, `active_oct`, `cancels_sep`, `cancels_oct`, `cancel_churn_sep`, `cancel_churn_oct` |
| `order_overall.json` | Order type | `order`, `rank`, `subs_pct`, `rev_pct`, `vps_sep`, `vps_oct`, `subs_delta`, `contrib_L` |
| `dept_order.json` | Department × order type | `dept`, `order`, `status` (`ok`, `too_small` or `not_in_review`), and any of `subs_sep`, `subs_oct`, `subs_delta`, `subs_pct`, `rev_sep_L`, `rev_oct_L`, `rev_delta_L`, `rev_pct`, `note` |
| `bridge.json` | Step of the Sep → Oct revenue bridge | `step`, `group` (`added` or `removed`), `delta_L`, optional `label` and `detail` to override the plain-language bar text |
| `notes.json` | Finding | `scope` (`Overall`, a department or an order type), `bucket` (`working`, `not` or `steady`), `text` |
| `lines.json` | Department × order type × month | `dept`, `order`, `month`, `idx`, `subs`, `revenue_L` |

Units: `_L` fields are ₹ lakh. `_pct` fields are percentages (for example `-0.4`, not `-0.004`).

`lines.json` is built from the SIP LTV sheet with `scripts/build_lines.py`. The Outlook tab expects `idx` 0 to be Jan 2025, so that 16–21 are May–Oct 2026.
