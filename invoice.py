#!/usr/bin/env python3
"""Generate a clean HTML crypto invoice (USDT) from a JSON file. Zero dependencies."""
import argparse
import html
import json
import sys

NETWORKS = {"TRC20", "ERC20", "BEP20"}


def money(n):
    return f"${n:,.2f}"


def render(data):
    items = data["items"]
    subtotal = sum(i["qty"] * i["rate"] for i in items)
    total = subtotal

    network = data.get("network", "")
    if network not in NETWORKS:
        raise ValueError(f"network must be one of {sorted(NETWORKS)}, got {network!r}")
    address = data["address"]

    rows = "\n".join(
        f"<tr><td>{html.escape(i['description'])}</td>"
        f"<td style='text-align:right'>{html.escape(str(i['qty']))}</td>"
        f"<td style='text-align:right'>{money(i['rate'])}</td>"
        f"<td style='text-align:right'>{money(i['qty'] * i['rate'])}</td></tr>"
        for i in items
    )

    notes = html.escape(data.get("notes", ""))
    qr_url = (
        "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data="
        + html.escape(address)
    )

    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>Crypto Invoice {html.escape(data.get('invoice_number', ''))}</title>
<style>
body{{font-family:-apple-system,Arial,sans-serif;max-width:680px;margin:40px auto;color:#1a1a1a}}
table{{width:100%;border-collapse:collapse;margin-top:24px}}
th,td{{padding:8px;border-bottom:1px solid #ddd}}
th{{text-align:left;color:#666;font-size:13px;text-transform:uppercase}}
.total{{font-size:20px;font-weight:bold}}
.meta{{color:#666;font-size:14px}}
.pay{{margin-top:24px;padding:16px;border:1px solid #ddd;border-radius:8px;display:flex;gap:16px;align-items:center}}
.addr{{font-family:monospace;word-break:break-all;font-size:14px}}
.badge{{display:inline-block;background:#111;color:#fff;border-radius:4px;padding:2px 8px;font-size:12px}}
@media print{{body{{margin:0}}}}
</style></head><body>
<h1>Crypto Invoice {html.escape(data.get('invoice_number', ''))}</h1>
<p class="meta">From: {html.escape(data.get('from', ''))}<br>
To: {html.escape(data.get('to', ''))}<br>
Date: {html.escape(data.get('date', ''))} &middot; Due: {html.escape(data.get('due_date', ''))}</p>
<table>
<tr><th>Description</th><th style="text-align:right">Qty</th><th style="text-align:right">Rate</th><th style="text-align:right">Amount</th></tr>
{rows}
</table>
<p style="text-align:right;margin-top:16px">
<span class="total">Total: {money(total)}</span></p>
<div class="pay">
<img src="{qr_url}" alt="QR code for payment address" width="120" height="120">
<div>
<span class="badge">USDT &middot; {html.escape(network)}</span>
<p class="addr">{html.escape(address)}</p>
<p class="meta">Pay exactly in the <b>{html.escape(network)}</b> network. Sending on a different network may result in lost funds.</p>
</div>
</div>
{"<p class='meta'>" + notes + "</p>" if notes else ""}
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="JSON invoice file (see example.json)")
    ap.add_argument("-o", "--output", help="output HTML file (default: stdout)")
    args = ap.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    out = render(data)
    if args.output:
        with open(args.output, "w") as f:
            f.write(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    try:
        main()
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
