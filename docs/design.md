# Design notes: the court and the panel

Deep Cut is one place, not a set of screens. A basketball court is on screen from the first moment and stays mounted while the player moves between home, a prompt, the reveal, the results, the archive and how to play. The panel next to it carries every word and number; the court is decoration (`aria-hidden`) that makes each answer a shot.

## Layout

- **900 px and wider** (desktop, tablet landscape): a split screen. The panel (questions, controls, results) is on the left; the court fills the right half of the viewport and stays in place while the panel scrolls. `web/src/layout.ts` holds the 900 px breakpoint (`layoutForWidth`, `useLayout`); the CSS switches on the same width.
- **Below 900 px** (phones, narrow windows): the court is a strip at the top, about 36% of the screen height, and it stays at the top (sticky) while the panel scrolls under it, so a shot is never scrolled out of view. No horizontal scrolling at 360 px.
- The page order is the panel first and the court after it, so a screen reader reads the questions first and never meets the court.

## The court

Drawn in SVG, in layers that all use one picture (`web/src/court/`): arena and stands, crowd, spotlights, the hardwood floor with its boards, painted lane, free-throw circle, three-point line and centre circle, a floor glow, the HUD (a hanging jumbotron and the shot clock above the backboard), and the action layer (backboard, rim, net, shooter, ball). The picture is drawn 400 units wider than the court on each side, so a wide, short strip (a tablet in portrait) shows more arena instead of cutting the hoop off. The court is a lazy-loaded chunk of about 5 KB gzipped (JavaScript) plus 2.3 KB (CSS); the home screen does not wait for it.

The panel and the court talk through a tiny store (`courtStore.tsx`): the panel publishes what is on (a question, a result, the points, the seconds left, the shot, the skip) and the court draws it. The shot clock on the court is a copy: the timer in the prompt card is the accessible one.

- **Idle:** spotlights sweep, the crowd shimmers in three bands, the floor glows and a ball bounces at centre court.
- **A question is on:** a silhouette shooter waits at the top of the key with the ball; the shot clock counts down and turns red and pulses in the last 5 seconds.
- **A result:** the shooter shoots from a spot that depends on the tier, the ball travels to the hoop, and the jumbotron rolls the points up, then the tier name pops. A tap or Enter skips to the end.

| Points | Shot | From |
| --- | --- | --- |
| 0 | airball, the ball misses everything and drops off the bottom | the right wing |
| 10 | clank off the top of the backboard | close to the hoop |
| 20 | rim rattle, around the rim twice and in | the left elbow |
| 35 | bank shot off the square | the left wing |
| 55 | swish, with a net ripple | the top of the key |
| 75 | deep swish: higher arc, bigger net snap, a crowd flash | far outside the three-point line |
| 100 | slam dunk: a drive and a hang, rim shake, a short screen shake, 28 particles | driving from the lane |

Only `transform` and `opacity` are animated; the ball's path is generated CSS keyframes (`geometry.ts`) that start from custom properties, so every shot starts at its own spot. With reduced motion there is a still court, and the ball at the end of the shot and the label fade in.

## Type and colour

Barlow Condensed (800 and 700) for the wordmark, headings and numbers, Barlow for text, both self-hosted through `@fontsource`. A night-navy arena, hardwood amber, white court lines, and one strong accent, ball orange (buttons, the rim, the wordmark's "NBA"). One colour per tier everywhere (white, blue, green, yellow, orange, purple; a miss is a muted grey): on the court label, the reveal, the results squares, the archive strips and the share squares, and a tier is never told by colour alone (every square has its number).

## Self-critique rounds

Screenshots at 360, 768, 1280 and 1920 px of the home screen, a prompt with the input focused, the reveal of a high-tier and a zero-point answer, the results and the archive, judged against: a place or a diagram, visual hierarchy, a readable left panel, anything cramped, flat, misaligned or generic, one product.

**Round 1 (first build).** The court read as a place (stands, boards, painted lane, a hoop with a net), the wordmark and the big play button gave the home screen a clear order, and the split worked at 1280 and 1920. Problems: the shot was cut short, because the Enter that submits an answer was still bubbling when the result screen mounted and counted as "skip" (found because the mid-flight frame looked the same as the last one); the three home buttons sat in one cramped row and "How to play" wrapped; the painted lane looked grey under the spotlight beams; on a phone the wordmark appeared three times (header, hero, jumbotron); the ball and shooter were too small to follow. Fixed: the skip listener now waits 120 ms; one column of actions; stronger lane paint and shorter beams; no header brand on the home screen; a bigger ball and shooter.

**Round 2.** At 768 px the strip cut off the jumbotron and the deep shooting spots; on a phone the court scrolled away when the result's heading took focus, so the shot was missed; the archive was a wall of solid orange buttons; the 34 rem panel looked small at 1920. Fixed: the picture is drawn wider (see above) and the strip shows the whole court at every width; the strip is sticky on phones and the headings have a scroll margin under it; archive Play buttons are outlined (only a hover fills them); the panel is wider and the wordmark larger from 1600 px.

**Round 3.** The crowd, drawn as hundreds of random dots, looked like television static. It is now three bands of tiled rows that shimmer out of step. The three-width screenshots, the contact sheet of all seven shots (`docs/screenshots/court/all-seven-shots.jpg`) and the checks (axe, keyboard only, reduced motion) were rerun.

**Still weak, honestly.** The shooter is a small flat silhouette with no sense of weight; the hoop is small beside the court at 1920; on a phone the ball in flight is a few pixels across; the net's motion is subtle; the crowd is dots, not people. A next round would give the shooter a better pose and a short run-up for every shot and enlarge the hoop and ball on small screens.
