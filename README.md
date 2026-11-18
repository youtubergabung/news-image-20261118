# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/youtubergabung/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/youtubergabung/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image summing up the world's news of Wednesday 18 November 2026, built
for make.fun's ["Sum up 18 November's world news in one image"](https://make.fun/bounty/news-image-20261118)
bounty ($250 in USDC).

## What the image shows

A 1024×1024 infographic, **"WORLD NEWS — 18 NOVEMBER 2026"**, with six
numbered stories, each with a headline and a one-line summary:

1. **Gulf conflict** — US strikes Iran; Iran hits bases in Bahrain and Kuwait.
2. **Summit** — Xi, Putin and Trump set for rare three-way talks.
3. **Ukraine war** — Ukraine hits the Kerch Bridge to Crimea for a second day;
   part of its road span fell into the strait.
4. **US politics** — Peltola wins Alaska; Democrats take a 56–44 majority.
5. **Health** — Congo Ebola outbreak passes 11,000 cases, the
   second-largest on record.
6. **Space** — Voyager 1 reaches one light-day from Earth, ~16 billion miles.

## Run it

```sh
python3 main.py
```

Requires Python 3.13 (works on 3.12+) and Pillow (`pip install pillow`).
No network access is needed at runtime: the image is generated from data
embedded in `main.py`, deterministically — every run writes the same bytes.

The program writes to `/output/entry.png` when `/output` exists or can be
created, and always also writes `./out/entry.png` for local inspection.

## Sources

All stories were reported for 18 November 2026 (checked 2026-11-18 ~14:30 UTC):

- Reuters — US strikes on Qeshm Island / Iranian attacks on Bahrain and Kuwait
  (via Zark News daily briefing, One Turn, Just Security Early Edition)
- AFP / Associated Press — Xi–Putin meeting in Shenzhen; APEC trilateral summit
  preparations (via Open Chronicle global news brief, Zark News)
- Zark News / One Turn — Ukraine's second-day strike on the Kerch Bridge
- Associated Press — Mary Peltola wins Alaska Senate race, Democrats 56–44
  (via Zark News, Just Security, NPR News Now 3am ET bulletin)
- United Nations — DR Congo Ebola outbreak passes 11,000 cases
  (via Zark News, One Turn)
- NASA Jet Propulsion Laboratory — Voyager 1 reaches one light-day from Earth
  (via Zark News)

## Tests

Run twice and compare — outputs must be byte-identical:

```sh
python3 main.py && sha256sum out/entry.png
python3 main.py && sha256sum out/entry.png
```

Results (2026-11-18, local test): see [TESTS.md](TESTS.md).

---

<sub>Entered on [make.fun](https://make.fun/?ref=6wdfsttv&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
