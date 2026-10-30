# Design notes: pixel art, the court and the panel

Deep Cut is one place, not a set of screens. A pixel-art basketball court is on screen from the first moment and stays mounted while the player moves between home, a prompt, the reveal, the results, the archive and how to play. The panel next to it carries every word and number; the court is decoration (`aria-hidden`) that makes each answer a shot.

The look is pixel art in black and orange, with chunky pixels, hard edges and scanlines. There are no smooth gradients, soft shadows, rounded corners or glow: edges are notched, shadows are hard offsets, dithering stands in for blending, and motion is stepped. How the pictures are made and shown is in [pixel-art.md](pixel-art.md).

## Layout

- **900 px and wider** (desktop, tablet landscape): a split screen. The panel (questions, controls, results) is on the left; the court fills the right half of the viewport and stays in place while the panel scrolls. `web/src/layout.ts` holds the 900 px breakpoint (`layoutForWidth`, `useLayout`); the CSS switches on the same width.
- **Below 900 px** (phones, narrow windows): the court is a strip at the top (288 px, two screen pixels per game pixel; 430 px from 520 px wide), and it stays at the top (sticky) while the panel scrolls under it, so a shot is never scrolled out of view. No horizontal scrolling at 360 px.
- The page order is the panel first and the court after it, so a screen reader reads the questions first and never meets the court.

## The court

A 172 x 215 game-pixel picture shown at a whole-number scale (`web/src/court/`): `court_bare.png` (stands, spotlight cones, LED ribbon, backboard, perspective hardwood, painted lane, three-point arc) with sprites on top: two crowd-sparkle frames and two spotlight beams, a jumbotron and a shot clock (real text in Press Start 2P over the stands), the rim in two halves with the ball between them, three net frames, the shooter in two poses, the dunker, the ball, a label and a burst of square particles. The court is a lazy-loaded chunk (15.4 KB gzipped JavaScript, 2.3 KB CSS, 33 KB for the court picture); the home screen does not wait for it.

The panel and the court talk through a tiny store (`courtStore.tsx`): the panel publishes what is on (a question, a result, the points, the seconds left, the shot, the skip) and the court draws it. The shot clock on the court is a copy: the timer in the prompt card is the accessible one.

- **Idle:** two spotlight beams sweep in steps, the crowd sparkles between two frames, and the ball bounces at centre court on a shadow that shrinks and grows.
- **A question is on:** the shooter waits at the top of the key dribbling; the shot clock counts down and flickers red in the last 5 seconds.
- **A result:** the shooter walks to a spot that depends on the tier, jumps, releases (his pose swaps), the ball hops to the hoop, the net swaps between its three frames, the jumbotron rolls the points up, and the tier label (with its number: "T5 Buzzer beater") pops in. A tap or Enter skips to the end.

| Points | Shot | From |
| --- | --- | --- |
| 0 | airball: the ball misses everything and drops off the bottom | the right wing |
| 10 | clank: the ball hits the front rim and bounces away; the rim shakes | close to the hoop, right |
| 20 | rim rattle: two hits on the rim and in | the left elbow |
| 35 | bank shot off the square | the left wing |
| 55 | swish, the net rings | the right, far wing |
| 75 | deep swish: a high arc, the net rings, a flicker of the crowd | far out on the left |
| 100 | slam dunk: a drive, the dunker hangs from the rim, 28 square particles, a flicker and a short shake | driving from the lane |

Only `transform` and `opacity` are animated. The ball's path is generated CSS keyframes (`geometry.ts`) with `steps()` timing that start from custom properties, so every shot starts at its own spot. With reduced motion there is a still court, and the shooter, the still ball at the end of the shot and the label (a plain fade) are all that change.

## Type and colour

Press Start 2P for headings, numbers, buttons and small labels; VT323 for prompt text, answers, the input and body copy. Both are self-hosted through `@fontsource`, imported in `main.tsx` (no font service is called).

| Token | Colour | Use |
| --- | --- | --- |
| ink | `#0a0a0a` | page, inputs, the court's frame |
| panel | `#141414` | cards |
| line | `#3a3a3a` | borders, dividers |
| orange | `#ff6a13` | buttons, the court frame, headings |
| amber | `#ffb347` | points, focus ring, links |
| cream | `#f4ead6` | text |
| muted | `#a8a8a8` | secondary text (never dimmer on dark) |
| deep | `#8a3c0a` | hard shadows |

Tier colours, the same on the court label, the reveal, the results squares, the archive strips and the chips: 1 `#6e6e6e`, 2 `#a8a8a8`, 3 `#ededed`, 4 `#ffb020`, 5 `#ff6a13`, 6 `#ff3b1f`. Text on tier 1 is white, on the rest ink, so every pair is at least 4.5 : 1 (`pixel.test.ts` computes them). A tier is never told by colour alone: every square, chip and label carries its number or its name. The share squares follow the same order: ⬛ miss, 🔲 1, 🔳 2, ⬜ 3, 🟨 4, 🟧 5, 🟥 6 (emoji have a limited palette, so the two greys are black and white buttons).

Pixel shapes without images: a **notched corner** is four box-shadow bars (`--notch`), so the corners are cut, a **hard shadow** is a zero-blur offset, the **scanlines** are two-pixel stripes behind the page and over the court, and the **timer bar** is a row of segments.

## Self-critique rounds

Screenshots at 360, 768, 1280 and 1920 px of the home screen, a prompt with the input focused, the reveal of a high-tier and a zero-point answer, the results and the archive (`docs/screenshots/pixel/`), judged against: a place, visual hierarchy, a readable left panel, anything cramped, flat, misaligned or generic, one product, and the krillion.io look (the site could not be opened from the build environment, so the direction was taken from the brief: chunky pixels, hard edges, scanlines, tight palette, notched corners, monospace pixel type, black and orange).

**Round 1 (first build).** Desktop worked at once: the court read as a place, and the wordmark, the dithered stands and the jumbotron gave a clear look. Problems: on a phone the court was drawn at one screen pixel per game pixel, tiny in a mostly black strip (the 4 px border took the height below the two-times threshold); at 1920 px the cards sat left of the header (a card margin overrode the centring); the secondary buttons vanished (dark on dark); the speaker was a smooth emoji in a pixel page; the zero-points label was a muddy grey with an orange shadow; the answer box was cramped beside its button on a phone and the prompt took seven lines; the shooter was clipped at the edge of the 640 px pane at the far spots; the tier 1 share square was tiny. Fixed: the strip is 288 px (and 430 px on tablets), the card margins, a pixel speaker drawn in 2 px squares, a grey shadow for a miss, a stacked answer row and smaller prompt text under 30 rem, shooting spots moved in from the edges, and new share squares.

**Round 2.** Secondary buttons were still faint on the page, so they take the panel grey on the page and ink inside a card; the phone home screen put the play button at the fold, so the type and spacing are tighter there; at 1600 px and wider the wordmark and tagline grow. Axe (home, prompt, reveal, results, archive: no violations), a keyboard-only dive (Tab to Play, type, arrow, Enter, no pointer), the console (no errors) and reduced motion (no running animation on the court) were checked.

**Round 3.** A contact sheet of all seven shots at three moments each (`all-seven-shots.png`) showed each shot distinct, the dunker on the rim, the flicker on the deep swish and the dunk, and the label legible; the final screenshots were retaken.

**Still weak, honestly.** The shooter is one sprite size at every spot, because a fractional scale would smear its pixels, so a deep shot does not look farther away, only farther along the floor. The waiting shooter faces away from the viewer. On tablets in portrait the court sits in black bars at three screen pixels per game pixel. At two screen pixels per game pixel the jumbotron's text is the 8 px minimum of the font. The two greys in the share squares are approximations. The ball does not spin. A next round would draw a second shooter facing the viewer and shorter jumbotron labels for small strips.
