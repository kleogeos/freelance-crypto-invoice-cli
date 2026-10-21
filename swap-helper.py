#!/usr/bin/env python3
"""Prints a ready-to-send message + swap link for the 'client paid USDT in the
wrong network' scenario. No network calls — just formats text and a link."""
import argparse
import sys

NETWORKS = {"trc20", "erc20", "bep20"}

REFERRAL_LINK = "https://simpleswap.io/?ref=9aabfd28302b"


def build_message(amount: float, got_network: str, want_network: str) -> str:
    return (
        f"Looks like the {amount} USDT arrived on {got_network.upper()}, but this wallet "
        f"expects {want_network.upper()}. No need to resend anything on your side — "
        f"I'll convert it myself using a non-custodial swap service (no account needed): "
        f"{REFERRAL_LINK}"
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("amount", type=float, help="Amount received, e.g. 150")
    p.add_argument("got_network", help="Network it actually arrived on: trc20/erc20/bep20")
    p.add_argument("want_network", help="Network your wallet needs: trc20/erc20/bep20")
    args = p.parse_args()

    got = args.got_network.lower()
    want = args.want_network.lower()
    for n in (got, want):
        if n not in NETWORKS:
            print(f"error: unknown network '{n}' (expected one of trc20, erc20, bep20)", file=sys.stderr)
            return 1
    if got == want:
        print("error: got_network and want_network are the same — nothing to swap", file=sys.stderr)
        return 1

    print(build_message(args.amount, got, want))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
