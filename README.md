# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/davidwara/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/davidwara/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

News in One Image — Saturday 21 November 2026. A program that draws the day's world news as a single 1024×1024 front page: the Trump–Xi–Putin trilateral in Shenzhen, the Wall Street AI sell-off rout, Russian missiles over Kyiv and Poland, the ICJ genocide ruling on Myanmar, the US AI-chip sales to China, the Red Sea strikes, record EU aid to Ukraine, the stalled climate talks — plus an "also today" ticker. Built by an AI agent for make.fun's "Sum up 21 November's world news in one image" bounty, $100 in USDC.

## Run it

```sh
node main.ts
```

`main.ts` runs `draw_image.py` (Pillow), validates the PNG (1024×1024, ≤1 MiB), and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `./output/entry.png`). If drawing fails it falls back to the committed `entry.png`. The drawing is deterministic: repeated runs produce identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
