# freelance-crypto-invoice-cli

Generate a clean, print-ready HTML invoice for a USDT payment — with the
network, wallet address, and a scannable QR code baked right in. Zero
dependencies, single file.

Why: a plain invoice that just says "pay in USDT" is how clients send funds
on the wrong network and lose them. This CLI forces you to name the network
explicitly and puts the address in front of the client as both text and a
QR code, so there's no ambiguity at payment time.

## Usage

```
python3 invoice.py example.json
python3 invoice.py my-invoice.json -o invoice.html
```

## Input format

```json
{
  "invoice_number": "INV-CRYPTO-0001",
  "from": "Acme Freelancer",
  "to": "Client Co.",
  "date": "2026-10-21",
  "due_date": "2026-10-28",
  "network": "TRC20",
  "address": "T...",
  "items": [
    {"description": "Website redesign", "qty": 1, "rate": 1200}
  ],
  "notes": "optional"
}
```

`network` must be one of `TRC20`, `ERC20`, `BEP20` — anything else is
rejected with a clear error instead of silently generating an invoice with
no network label (a common cause of client payments going to the wrong
chain and getting lost).

Not sure which network to use? See [Какую сеть USDT выбрать](https://kleogeos.github.io/freelancer-tools/kakuyu-set-usdt-vybrat-frilanseru.html?src=cli-cryptoinvoice).

## Wrong network? Second tool in this repo

If a client already sent USDT on the wrong network (e.g. your invoice said
TRC20 but it landed as ERC20), `swap-helper.py` prints a ready-to-send
client message plus a non-custodial swap link — no account needed on
either side, and no need to ask the client to resend anything.

```
python3 swap-helper.py 150 erc20 trc20
```

(The swap link is a SimpleSwap affiliate link — disclosed here plainly:
using it costs the client nothing extra and sends a small referral
commission this project's way.)

## Related

Part of the [Freelancer Toolbox](https://kleogeos.github.io/freelancer-tools/kit.html?src=cli-cryptoinvoice) —
free tools for freelancer paperwork (invoices, contracts, rates, taxes,
crypto payments).

## License

MIT
