# Tests

Run on 2026-11-18 (local VM, Python 3.12.3, Pillow 10.2.0; `main.py` targets
Python 3.13 and uses only the standard library plus Pillow).

## Determinism — run twice, byte-identical

```sh
python3 main.py && sha256sum out/entry.png
python3 main.py && sha256sum out/entry.png
```

| Run | SHA-256 | Size | Dimensions |
| --- | ------- | ---- | ---------- |
| 1 | `126538f1c00a910b3d636c57d733ef935e627bf1e7c54cde314ef9722ade6605` | 143,842 bytes | 1024 × 1024 PNG |
| 2 | `126538f1c00a910b3d636c57d733ef935e627bf1e7c54cde314ef9722ade6605` | 143,842 bytes | 1024 × 1024 PNG |

Both runs also wrote `/output/entry.png` with the identical SHA-256.
Size 143,842 bytes < 1 MiB limit. Dimensions exactly 1024 × 1024.

## Visual check

Rendered `out/entry.png` and inspected it: header, six numbered story
blocks (tag, headline, one-line summary), and footer with sources are all
legible, high contrast, with no overlapping or clipped text. (An earlier
draft overflowed story 1 into story 2 and clipped the footer; headlines
were shortened and the layout rebalanced to fix it.)

## program/v1 harness check

With `MAKEFUN_ENV_URL` pointed at a local fake harness server:

- Program POSTed `{"port": <free port>}` to `$MAKEFUN_ENV_URL/register`
  (ports observed: 32903, 46519 — never 8080).
- `GET /healthz` on the registered port returned `200 ok` while running.
- Program exited with code 0 once `GET $MAKEFUN_ENV_URL/done` returned
  `{"done": true}`.
- Without `MAKEFUN_ENV_URL`, the program writes the image and exits
  immediately (no harness behaviour).
