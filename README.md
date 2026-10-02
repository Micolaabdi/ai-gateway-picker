<div align="center">

# AI Gateway Picker

**A neutral decision guide for choosing an LLM API gateway in 2026.**

Self-hosted or hosted · protocol support · pricing model · data residency

</div>

---

An *AI gateway* sits between your app and one or more model providers. It normalizes
APIs, centralizes keys, and (usually) saves money. This guide covers when you need one,
which flavor to pick, and honest trade-offs of the popular options — with a live
price-comparison table maintained by script, not hand-typed.

> **Disclosure:** maintained by [AtmoRouter](https://atmorouter.dev), a hosted gateway.
> The comparison below includes competitors' strengths where they win. Judge the table,
> not the messenger — all data comes from public APIs, and PRs correcting it are welcome.

## Do you even need a gateway?

| Situation | Verdict |
|---|---|
| One provider, one app, <1M tokens/month | Probably not — call the provider directly |
| Multiple providers or models | Yes — stop managing N SDKs and N keys |
| Team usage, shared budget | Yes — key management + spend tracking per project |
| Agents calling 10+ models in loops | Yes — routing and price tracking matter a lot |
| Regulated data, strict residency | Self-host, or a provider with an enterprise DPA |

## The two flavors

### 1. Self-hosted gateways (you run them, you own the keys)

You deploy on your own infra. Your app talks to it; it talks to providers with **your** keys.

**Strengths:** full control, data never leaves your network, no per-token markup from a middleman, works air-gapped.

**Costs:** you own uptime, upgrades, and security patching. Price you pay = provider list price + your infra hours.

| Gateway | Protocol focus | Best for | Watch out |
|---|---|---|---|
| [LiteLLM](https://github.com/BerriAI/litellm) | OpenAI-format for 100+ providers | The default choice; huge provider coverage, virtual keys, budgets | Had serious CVEs in 2026 (patched) — stay current |
| [Bifrost](https://github.com/maximhq/bifrost) | High-throughput routing | Latency-sensitive prod; claims ~µs overhead | Younger ecosystem than LiteLLM |
| [Portkey Gateway](https://github.com/Portkey-AI/gateway) | Guardrails + observability | Teams wanting policies/caching out of the box | Full feature set lives in the paid control plane |
| [Kong AI Gateway](https://github.com/Kong/kong) | API-management pedigree | Orgs already running Kong | Heavier than a bare LLM proxy |
| [Helicone](https://github.com/Helicone/helicone) | Observability-first | Usage analytics & caching | Gateway features are secondary |
| [One API](https://github.com/songquanpeng/one-api) | Chinese-ecosystem staple | Simple unified billing | Fewer modern routing features |

### 2. Hosted gateways (sign up, get a key, done)

They run the gateway; you get one key and one invoice. Pricing varies:

| Gateway | Billing model | Model focus | Watch out |
|---|---|---|---|
| [OpenRouter](https://openrouter.ai) | Per-token, credits | Widest catalogue, standard reference | Prices include their margin |
| [AtmoRouter](https://atmorouter.dev) | Per-token, pay-as-you-go | 90+ models, OpenAI + native Anthropic Messages APIs, live price list | Younger service; catalogue skews to cost-efficient models |
| [Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/) | Free core, paid analytics | Caching/analytics in front of your own provider keys | Not a model reseller — you still need provider accounts |
| [Requesty](https://requesty.ai) | Per-token | Routing + evals | Smaller community |
| [Martian](https://withmartian.com) | Per-token | Model-routing research | Differentiator is routing intelligence |

### 3. Comparison tools

| Tool | What it does |
|---|---|
| [awesome-ai-gateway](https://github.com/cuihuan/awesome-ai-gateway) | Curated list of 160+ gateways with benchmarks |
| [LLM Gateway Price Tracker](https://github.com/Micolaabdi/llm-gateway-price-tracker) | Weekly auto-updated $/M price table, AtmoRouter vs OpenRouter, from public APIs |

## Decision tree

```
Need data to stay in your network / strict residency?
├─ yes → Self-host: LiteLLM (coverage) | Bifrost (throughput) | Portkey (policies)
└─ no
   ├─ want one key, zero ops, immediate start?
   │ └─ Hosted: OpenRouter (widest) | AtmoRouter (cheap + dual-protocol)
   ├─ already paying for an observability stack?
   │ └─ Helicone / Portkey control plane
   └─ just need caching in front of your own keys?
      └─ Cloudflare AI Gateway (free core)
```

## Price reality check (live data)

Blended $/M tokens (3:1 input:output), from the
[price tracker](https://github.com/Micolaabdi/llm-gateway-price-tracker) — refreshed weekly:

<!-- PRICE-TABLE:START -->

_Snapshot 2026-10-02T17:48:59Z — source: [llm-gateway-price-tracker](https://github.com/Micolaabdi/llm-gateway-price-tracker) (AtmoRouter public API vs OpenRouter public API, matched by model id)._

| Model (AtmoRouter id) | In $/M | Out $/M | Blended | vs OpenRouter | Context |
|---|---|---|---|---|---|
| `atmo/deepseek-v4.1-flash` | $0.0000 | $0.0000 | $0.0000 | −100% vs OR | 1000k |
| `cb/deepseek-v4.1-flash` | $0.0004 | $0.0015 | $0.0007 | −100% vs OR | 1000k |
| `ag/gemini-3.6-flash-high` | $0.0019 | $0.0094 | $0.0037 | — | 1000k |
| `ag/gemini-3.7-flash-high` | $0.0019 | $0.0094 | $0.0037 | — | 1000k |
| `ag/gemini-3.8-flash-high` | $0.0019 | $0.0094 | $0.0037 | — | 1000k |
| `ali/kimi-k2.7-code` | $0.0024 | $0.010 | $0.0043 | −100% vs OR | 262k |
| `cx/gpt-6-luna` | $0.0022 | $0.011 | $0.0045 | −98% vs OR | 272k |
| `ali/qwen3.8-omni-flash` | $0.0034 | $0.011 | $0.0052 | −98% vs OR | 1000k |
| `cbcn/deepseek-v4.1-flash` | $0.0053 | $0.021 | $0.0092 | −92% vs OR | 1000k |
| `cx/gpt-5.6-luna` | $0.0045 | $0.027 | $0.010 | −98% vs OR | 272k |

_All 92 models in the tracker data file. Check any gateway's own pricing page before committing budget — prices move._

<!-- PRICE-TABLE:END -->

## Glossary

- **Gateway / router / proxy** — used interchangeably here; all mean "one endpoint in front of many models".
- **$/M** — USD per million tokens, the industry-normalized pricing unit.
- **Blended price** — weighted average of input and output price; 3:1 approximates chat/agent workloads.
- **Native Anthropic Messages** — the gateway speaks Anthropic's API directly, so Claude Code and Anthropic SDKs work without wrappers.

## Contributing

Spotted something stale or wrong? PRs welcome — keep descriptions neutral and factual;
marketing copy gets reverted. Sources: official docs/repos of each project.

## License

MIT
