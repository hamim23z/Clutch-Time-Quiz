# Pixel art

Every picture on the site is drawn by one script, `tools/pixel/gen_pixel.py`, so the art is reproducible: change a colour or a pose, run the script, commit the PNGs.

## Run it

```
pip install pillow                     # once
cd web && npm install && cd ..          # once: the share image uses the site's two fonts
python3 tools/pixel/gen_pixel.py        # from the repo root
python3 tools/pixel/gen_pixel.py OUTDIR # or write everything to another folder
```

By default it writes into `web/src/assets/pixel/` (the pictures the court uses) and `web/public/` (`favicon.png`, `apple-touch-icon.png`, `social.png`). It is deterministic (a fixed random seed): running it twice gives identical files, and `court.png`, `ball.png` and `dunker.png` are byte for byte the starter pictures it grew from. If the fonts are missing (no `npm install`) it skips `social.png` and says so.

## How a picture is made

1. A small canvas is drawn with aliased primitives (lines, polygons, ellipses with no smoothing). The court is **172 x 215** pixels; the ball is 13 x 13; a player is 56 x 76. These are "game pixels".
2. Shading is **Bayer ordered dithering** (a fixed 4 x 4 pattern between two colours), never a smooth blend, so the art keeps its hard edges.
3. The canvas is enlarged **4x with nearest neighbour** (`Image.NEAREST`), so every game pixel is a 4 x 4 block in the PNG (`court.png` is 688 x 860).
4. The same palette everywhere: ink `#0a0a0a`, orange `#ff6a13`, amber `#ffb347`, cream `#f4ead6`, deep orange `#8a3c0a`, and the wood and skin tones in the script.

| File | What it is |
| --- | --- |
| `court.png` | the half court with its hoop baked in (the reference picture; the site does not show it) |
| `court_bare.png` | the same court with no rim and no net, which the site draws and animates on top |
| `rim_back.png`, `rim_front.png` | the two halves of the rim, so the ball passes between them |
| `net_0.png`, `net_1.png`, `net_2.png` | the net at rest, stretched by the ball, and snapped back |
| `ball.png` | the ball |
| `dunker.png` | the mid-dunk pose (hand on the rim) |
| `shooter_stand.png`, `shooter_shoot.png` | the shooter waiting with the ball, and at the release |
| `beam.png` | a spotlight beam (dithered, so it stays pixels) |
| `crowd_a.png`, `crowd_b.png` | two frames of sparkle for the stands |
| `favicon.png`, `apple-touch-icon.png`, `social.png` | the browser icon (64 x 64), the touch icon (180 x 180) and the share image (1200 x 630, from a 400 x 210 canvas at 3x) |

## How the site shows them

- **Integer scale only.** The court is placed on a stage of 172 x 215 game pixels, each shown as `k x k` screen pixels, where `k` is a whole number: `stageScale(paneWidth, paneHeight)` in `web/src/court/geometry.ts` is the width of the pane divided by 172, rounded, and never bigger than what lets the 142 rows every shot needs fit in the height. A 360 px phone strip gets k = 2, a tablet strip 3, the desktop pane 4 (1920 px wide: 6). The stage is centred in whole pixels; a pane wider than the stage shows black bars, a narrower one crops evenly.
- **Always `image-rendering: pixelated`.** Every picture has it (CSS and a test). Because the PNGs are 4x, showing them at `k` x 56 x 76 is a clean nearest-neighbour step for any whole `k`.
- **Placed in game pixels.** Everything on the stage (jumbotron, shot clock, hoop pieces, shooter, ball, label) is positioned with `--x`, `--y`, `--w`, `--h` in game pixels multiplied by `--u` (= `k` px), so it lines up with the baked court at every scale. The rim centre is at (86, 70), about 50% across and 32.6% down.
- **Stepped motion.** The ball and the shooter move with `steps()` timing (a hop about every 7 game pixels), the net and the poses are plain swaps between frames, the flash is a flickering checkerboard, the shake is a few whole-pixel jumps. No sprite is rotated or scaled by a fraction, because that would smear its pixels.
- **Scanlines** are a hard-edged stripe pattern over the court and behind the page.

## Adding a sprite

Draw it in `gen_pixel.py` with the same helpers (`sprite()` for a figure with an outline and a highlight, `net()` and `rim_halves()` for the hoop), save it with `save(image, "name.png")`, run the script, import the PNG in `web/src/court/CourtScene.tsx`, and show it with the `Sprite` component (a width and height in game pixels). `web/src/pixel.test.ts` checks that every picture is a whole multiple of the game size and that none is left unused.
