from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Literal, Sequence

Mode = Literal["bid", "on-demand"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--max-price", required=True)
    parser.add_argument("--disk-gb", required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--ssh-public-key", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=20)
    return parser.parse_args()


def run(command: Sequence[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, check=check, text=True)


def json_or_none(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def print_output(stdout: str, stderr: str) -> None:
    output = "\n".join(part for part in [stdout.strip(), stderr.strip()] if part)
    payload = json_or_none(output)
    print(json.dumps(payload, indent=2) if payload is not None else output)


def offer_id(offer: dict[str, Any]) -> str:
    return str(offer.get("id") or offer.get("ask_contract_id") or "")


def offer_price(offer: dict[str, Any], mode: Mode) -> str:
    price = (
        offer.get("min_bid")
        if mode == "bid"
        else offer.get("dph_total") or offer.get("dph")
    )
    return str(price) if price is not None else ""


def search_offers(
    *,
    mode: Mode,
    query: str,
    disk_gb: str,
    limit: int,
) -> list[dict[str, Any]]:
    order = "min_bid" if mode == "bid" else "dph"
    result = run(
        [
            "vastai",
            "--raw",
            "search",
            "offers",
            "--type",
            mode,
            query,
            "--storage",
            disk_gb,
            "--limit",
            str(limit),
            "-o",
            order,
        ]
    )
    offers = json.loads(result.stdout)
    if not isinstance(offers, list):
        raise TypeError(f"Expected offer list, got {type(offers).__name__}")
    return offers


def summarize_offers(mode: Mode, offers: list[dict[str, Any]]) -> None:
    print(f"Found {len(offers)} {mode} offers")
    price_name = "min_bid" if mode == "bid" else "dph"
    for offer in offers[:5]:
        print(
            f"- {offer_id(offer)}: "
            f"{offer.get('gpu_name', 'unknown GPU')}, "
            f"{price_name}={offer_price(offer, mode)}"
        )


def create_instance(args: argparse.Namespace, mode: Mode, offer: dict[str, Any]) -> str | None:
    current_offer_id = offer_id(offer)
    current_price = offer_price(offer, mode)
    if not current_offer_id or not current_price:
        return None

    command = [
        "vastai",
        "--raw",
        "create",
        "instance",
        current_offer_id,
        "--image",
        args.image,
        "--disk",
        args.disk_gb,
        "--ssh",
        "--direct",
        "--cancel-unavail",
        "--label",
        args.label,
    ]
    if mode == "bid":
        command.extend(["--bid_price", current_price])

    print(
        f"Trying {mode} offer {current_offer_id}: "
        f"{offer.get('gpu_name', 'unknown GPU')}, price={current_price}"
    )
    result = run(command, check=False)
    print_output(result.stdout, result.stderr)
    if result.returncode != 0:
        print(f"Offer {current_offer_id} failed with status {result.returncode}")
        return None

    payload = json_or_none(result.stdout)
    if not isinstance(payload, dict):
        return None

    instance_id = payload.get("new_contract")
    return str(instance_id) if instance_id else None


def rent_mode(args: argparse.Namespace, mode: Mode, query: str) -> str | None:
    offers = search_offers(mode=mode, query=query, disk_gb=args.disk_gb, limit=args.limit)
    summarize_offers(mode, offers)

    for offer in offers:
        if instance_id := create_instance(args, mode, offer):
            print(f"Selected {mode} offer {offer_id(offer)}")
            return instance_id

    return None


def write_github_output(instance_id: str) -> None:
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output is None:
        print(instance_id)
        return

    with Path(github_output).open("a", encoding="utf-8") as output:
        output.write(f"instance_id={instance_id}\n")


def register_ssh_key(public_key_path: Path) -> None:
    public_key = public_key_path.read_text(encoding="utf-8").strip()
    result = run(["vastai", "create", "ssh-key", public_key, "-y"])
    print_output(result.stdout, result.stderr)


def main() -> int:
    args = parse_args()
    register_ssh_key(args.ssh_public_key)

    instance_id = rent_mode(args, "bid", f"{args.query} min_bid<={args.max_price}")

    if instance_id is None:
        print(f"No interruptible offer rented; trying on-demand under ${args.max_price}/hr")
        instance_id = rent_mode(args, "on-demand", f"{args.query} dph<={args.max_price}")

    if instance_id is None:
        print("No Vast offer could be rented", file=sys.stderr)
        return 1

    write_github_output(instance_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
