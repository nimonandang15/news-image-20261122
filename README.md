# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/nimonandang15/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/nimonandang15/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image that sums up the world's news of Sunday 22 November 2026 — a newspaper front page, "The World in One Day", with the six stories that defined the day.

## The day's news

1. **Ukraine suffers its biggest attack of the year** — Russia fires 110 missiles and more than 400 drones in one night; President Zelenskyy calls Putin a "killer"; a Russian cruise missile violates Polish airspace. Trump, by contrast, calls Putin a friend who wants to end the war.
2. **Gulf on edge as tankers are hit** — Bahrain says Iran set fire to a civilian industrial site; two oil tankers are struck near the Strait of Hormuz; Iran claims it hit a US F-16 over the Gulf — US Central Command denies it.
3. **Russian cargo ship ablaze after drone strike** — the Sparta II, a military-linked cargo ship under US sanctions, catches fire in the Gulf of Finland and drifts into Finnish waters; all 16 crew are evacuated; Finland says Ukraine was likely behind it.
4. **Climate talks run into overtime** — negotiators at COP31 in Antalya, Turkey, extend the summit a second day, split over fossil fuels and funding for poorer nations; the EU says it wants a good deal or no deal.
5. **"El Chapo Isidro" captured** — Mexico seizes FBI most-wanted cartel boss Fausto Isidro Meza Flores in Guasave, Sinaloa; eleven people are killed in the firefight; he is flown to Mexico City.
6. **Quake shakes the Andes** — a magnitude 6.7–6.8 earthquake hits Peru's Junín region; 15 people are injured and no deaths are reported.

Sources: AP, CNN, TBS News, BBC, Reuters, EventGraph daily brief — 22 Nov 2026.

`main.ts` (Node 22, standard library only) copies `entry.png` byte for byte to `/output/entry.png`, refusing anything that is not a whole PNG within the gate limits (≤ 1 MiB, ≤ 1024×1024). Both runs write the same bytes. The poster is drawn by `render.py` (PIL + DejaVu only).

## Run it

```sh
python3 render.py            # rebuild entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=cydbk12s&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
