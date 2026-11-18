# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/keyyzoo/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/keyyzoo/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A program that writes one image summing up the world's news of Tuesday 17 November 2026.

## What it is

A newspaper front page in one image (`image.png`, 1024×1024): the masthead
names the day — **TUESDAY, 17 NOVEMBER 2026** — and the page sums up the
day's most consequential stories: Ukraine's strike on the Kerch Bridge,
Trump's arrival in Asia for APEC, the Strait of Hormuz tanker attacks,
the five-nation Rwanda return hub, US chip curbs and Nvidia's earnings,
Japan scrambling jets, plus a ticker of four more stories from the day.
All facts are events of 17 November 2026 as reported that day; the
illustration is drawn from simple geometric shapes, no photos.

## Run it

```sh
# Re-render the image (needs Pillow; build time only)
python3 render.py

# Write the entry image (standard library only)
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
# or, with the default output directory:
python3 main.py
```

`main.py` copies the pre-rendered `image.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png` by default),
verifies the copy byte-for-byte, and prints the output path and size.
Running it twice produces identical bytes.

## Files

- `main.py` — the entry program (standard library only).
- `render.py` — the deterministic Pillow renderer that draws `image.png`.
- `image.png` — the rendered infographic, 1024×1024 PNG.
- `LICENSE` — MIT.

Built with [make.fun](https://make.fun/r/8cr10cb2) — enter the bounty yourself with referral code `8cr10cb2`.
