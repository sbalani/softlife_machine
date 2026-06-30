# softlife_machine

Custom **Odoo 18** module — the SoftLife soft-serve **machine fleet** record.

The central business object that `softlife_huaxin` and `softlife_haccp` depend on:

- Machine record: name, internal ref, Huaxin device IMEI/ID.
- Assignment: customer (partner), current location, serving warehouse
  (one warehouse → many machines; one customer → many machines).
- Product / hopper config: base product + per-position topping/sauce lines
  (portion size, loaded capacity, cycles) — maps to Huaxin product positions.
- HACCP maintenance dates (last full clean) — written by `softlife_haccp`.
- Numbered transfer / delivery documents (`MTR/YYYY/#####`) so machines can be
  reassigned or relocated with an audit trail.

## Depends on
`base`, `stock`, `product`, `mail` — all standard Odoo. No OCA dependencies.

## Install
Clone into your Odoo addons path named `softlife_machine`:

```bash
git clone https://github.com/sbalani/softlife_machine.git softlife_machine
```

Then in Odoo: **Apps → Update Apps List → install "SoftLife Machine Fleet"**.
