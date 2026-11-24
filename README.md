# 24 November World News in One Image

An entry for the make.fun competition
[Sum up 24 November's world news in one image](https://make.fun/bounty/news-image-20261124).

![Competition](https://make.fun/badge/news-image-20261124.svg)
![Rank](https://make.fun/badge/news-image-20261124/xiaoyu-liu2026/news-image-20261124/rank.svg)
![Reward](https://make.fun/badge/news-image-20261124/xiaoyu-liu2026/news-image-20261124/reward.svg)

## What it does

`main.ts` copies the repository's `entry.png` to `/output/entry.png`,
byte for byte, after checking it against the competition gate
(at most 1 MiB, at most 1024 by 1024 pixels, a whole PNG).

The image is a one-page infographic of Tuesday 24 November 2026:

- **Ukraine sinks Russian warship off Libya** — 7 naval drones hit the
  corvette Merkury at Benghazi port; the UN seeks a probe.
- **Huang back as CEO** — Nvidia reinstates Jensen Huang; shares +31%,
  S&P 500 +4.7%, Nikkei +3.9%.
- **3 tankers hit mines in Hormuz** — Iran says three oil tankers
  caught fire in the Strait of Hormuz.
- **NATO vows space defence** — after reports Russia plans a
  nuclear-armed satellite.
- **COP31 summit ends without a deal.**
- Ticker: Gaza strikes kill 6; Indonesia factory fire kills 26;
  landmine casualties hit 7,000, a five-year high.

`entry.png` is drawn by `make_image.py` (Python + Pillow): every label
is rendered as text by the script, never generated inside an AI image,
so each word reads exactly as written.

## Run it

Requires Node 22.18 or later, no dependencies to install:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Running it twice writes exactly the same bytes.

## License

MIT — see [LICENSE](./LICENSE).
