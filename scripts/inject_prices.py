#!/usr/bin/env python3
"""Inject the live top-10 price table from the llm-gateway-price-tracker data
into ai-gateway-picker's README between the PRICE-TABLE markers."""
import json
import urllib.request

SRC = "https://raw.githubusercontent.com/Micolaabdi/llm-gateway-price-tracker/main/data/data.json"
README = "README.md"
START = "<!-- PRICE-TABLE:START -->"
END = "<!-- PRICE-TABLE:END -->"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ai-gateway-picker/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def fmt(x):
    if x >= 1:
        return f"${x:.2f}"
    if x >= 0.01:
        return f"${x:.3f}"
    return f"${x:.4f}"


def main():
    data = fetch_json(SRC)
    rows = []
    for m in data["models"][:10]:
        a = m["atmorouter"]
        vs = m.get("vs_openrouter_pct")
        vs_s = f"−{vs:.0f}% vs OR" if vs is not None and vs > 0 else "—"
        ctx = a.get("context_length")
        ctx_s = f"{ctx // 1000}k" if ctx else "—"
        rows.append(
            f"| `{m['id']}` | {fmt(a['input_per_m'])} | {fmt(a['output_per_m'])} | "
            f"{fmt(a['blended_per_m'])} | {vs_s} | {ctx_s} |"
        )

    table = "\n".join(
        [
            f"_Snapshot {data['generated_at']} — source: [llm-gateway-price-tracker](https://github.com/Micolaabdi/llm-gateway-price-tracker) (AtmoRouter public API vs OpenRouter public API, matched by model id)._",
            "",
            "| Model (AtmoRouter id) | In $/M | Out $/M | Blended | vs OpenRouter | Context |",
            "|---|---|---|---|---|---|",
            *rows,
            "",
            f"_All {len(data['models'])} models in the tracker data file. Check any gateway's own pricing page before committing budget — prices move._",
        ]
    )

    src = open(README).read()
    i, j = src.index(START) + len(START), src.index(END)
    out = src[:i] + "\n\n" + table + "\n\n" + src[j:]
    with open(README, "w") as f:
        f.write(out)
    print(f"injected {len(rows)} rows into {README}")


if __name__ == "__main__":
    main()
