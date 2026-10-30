# Design notes: the panel and the shot chart

Deep Cut is one place, not a set of screens. A flat shot chart is on screen from the first moment and stays mounted while the player moves between home, a prompt, the reveal, the results, the archive and how to play. The panel next to it carries every word and number; the chart is decoration (its SVG is `aria-hidden`) that turns each answer into a shot.

The look is flat and hard-edged, in black and orange: no gradients that blend, no blur, no glow, no raster images. The panel keeps its notched borders and hard shadows; the chart is plain SVG shapes.

## Layout

- **900 px and wider:** a split screen. The panel (questions, controls, results) is on the left; the chart fills the right half of the viewport (background `#060606`) and stays in place while the panel scrolls. `web/src/layout.ts` holds the breakpoint; the CSS switches on the same width.
- **Below 900 px:** the chart is above the panel, at most 60% of the screen height (its shape is 688 : 860). When a result or the results screen appears, the page scrolls back to the top so the shot is never played out of sight.
- The page order is the panel first and the chart after it, so a screen reader reads the questions first.

## The shot chart (`web/src/chart/`)

One inline SVG, `viewBox="0 0 688 860"`, 11.2 units per foot, the basket at the top.

- **Court:** a rectangle at (96, 104), 560 x 526.4; the lane; the free-throw circle (top half solid, bottom half dashed); the restricted-area arc; the three-point line (straight sides to y = 263, then a 266-unit arc about the hoop); the half-court arc at the bottom; the backboard line and the rim (radius 8.4) at (376, 162.8). Lines are cream, 3 wide, square caps.
- **Rarity zones:** concentric filled circles about the hoop, clipped to the court, in very dark warm tones (warmest nearest the basket), with dashed grey rings at the boundaries: T1 under 112 units from the hoop, T2 to 190.4, T3 to 266, T4 to 358.4, T5 to 440, T6 to 467.
- **Depth gauge:** left of the court, a line at x = 84 with a tick at every boundary, and for each tier a square with its number and the points beside it (10, 20, 35, 55, 75, 100), in the middle of its band.
- **Markers:** one 22-unit square per answer in the tier colour, with the tier number, a hard black offset shadow and a dashed line from the hoop. The latest answer has a dashed cream ring (radius 26). A wrong or late answer is a grey square with an X in the **airball zone** (a dashed rectangle under the court, three slots across and two deep; more misses wrap round, a little to the right).
- **Placement** (`placement.ts`): the angle and the distance come from a hash of the prompt id and the dive number (the dive number stands for the dive's date), so a dive always looks the same. The distance is inside the tier's band and off its edges, the angle is 20 to 160 degrees below the hoop, the marker and its ring stay on the court, and no two markers (or a marker and the waiting ball) are closer than 34 units. Markers are placed in prompt order, so an earlier one never moves when a later answer is added.
- **Header and readouts:** "SHOT CHART" in Press Start 2P, the tagline "Rarer answer = deeper shot." in VT323, and the clock and points from the same store the panel publishes (no second timer). Under the airball zone, three boxes: SHOTS (made / total), POINTS and BEST SHOT (tier and points).
- **Home:** no markers, the ball at the bottom, and a "TODAY'S DIVE #N / 7 PROMPTS" box over the court. Other idle screens show their name in the same box.

The panel and the chart talk through a tiny store (`chartStore.tsx`): the panel publishes what is on (the question number, the points, the seconds left, the answers so far, the shot, the skip) and the chart draws it.

## Animation

CSS only, and only `transform` and `opacity`.

- **A correct answer:** a ball (orange, black seams) flies in an arc from the bottom centre to its marker (x moves with ease-out, y rises and falls); the marker pops in when it lands (scale 0.6 to a peak to 1), the target band pulses once, and the tier colour flashes behind the points readout. A rarer tier flies longer (590 ms for T1 to 940 ms for T6), arcs higher and pops bigger. **T6** also gets a brief white flash over the court and a short "DEEP CUT" stamp.
- **A wrong or late answer:** the ball falls short into the airball zone, bounces, and the X appears.
- **Replay:** the results screen shows all seven markers, popping in one after another (480 ms apart, in step with the squares on the left).
- **Skip:** a tap or Enter jumps to the end state. **Reduced motion:** no flight, pulse, flash or stamp; the marker only fades in.
- The existing sound effects are called as before.

## Type and colour

Press Start 2P for headings, numbers and buttons; VT323 for prompt text, answers, the input and body copy. Both are self-hosted through `@fontsource`.

Palette: ink `#0a0a0a`, panel `#141414`, line `#3a3a3a`, orange `#ff6a13`, amber `#ffb347`, danger red `#ff3b1f`, cream `#f4ead6`, muted `#a8a8a8`, deep orange `#8a3c0a`. Tier colours, the same on the chart, the reveal, the results squares, the archive strips and the chips: 1 `#6e6e6e`, 2 `#a8a8a8`, 3 `#ededed`, 4 `#ffb020`, 5 `#ff6a13`, 6 `#ff3b1f`. Text on tier 1 is white, on the rest ink, so every pair is at least 4.5 : 1. A tier is never told by colour alone: every square, chip and marker has its number.

## Accessibility

The SVG is `aria-hidden`. A visually hidden `aria-live="polite"` line next to it says each result ("Tier 3, 35 points, 55 total", or "Airball, 0 points, 55 total"). Everything on the chart is also in the panel. On a phone the small text is made larger in CSS, because the picture is about 0.55 of its size.

## Self-critique rounds

Screenshots of home, prompt 1 and 7, a correct answer, an airball, the T6 flash and the results, at 1440 x 860 and 390 x 844 (`docs/screenshots/chart/`).

**Round 1.** Found: on a phone the page scrolled to the result heading and the chart left the screen, so the shot was missed; a tier-4 marker sat on the court line with its ring outside it; the "100" of the gauge touched the axis; five tier-1 markers on the results screen carried a ring over the cluster; the pulse of a zone was a strong tan band; the zone tones were too close to tell apart. Fixed: the chart scrolls back into view on a phone, markers keep their ring on the court, the gauge text is smaller, the ring is only for the live shot, the pulse is lighter, and the zone tones are further apart.

**Round 2.** Rechecked every state at both sizes: no horizontal scroll, no overlapping labels, no marker outside the court, the gauge ticks on the band rings, the left panel unchanged except the capital on the question. Nothing more failed.

**Limits, honestly.** On a phone the picture is about 0.55 of its size, so the gauge and the stats are small even after being enlarged; five or more tier-1 markers sit close together near the basket because that zone is small; the page is 9 px taller than a 860 px window (a margin in the panel, as before), so the whole page can scroll by that much; focus goes to the result heading after an answer (as before) and to the next question's input, not to the same input.
