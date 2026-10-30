import { HOOP, VIEWBOX } from './geometry';

/** The static pieces of the arena, drawn once. Everything here is decoration. */

const FLOOR = '150,296 650,296 880,640 -80,640';

/** Lines of the floor boards, fanning from a vanishing point above the hoop. */
function boardLines(): string[] {
  const lines: string[] = [];
  for (let i = -9; i <= 9; i++) {
    const bottomX = 400 + i * 62;
    const topX = 400 + (bottomX - 400) * 0.66;
    lines.push(`M${topX.toFixed(1)} 296 L${bottomX} 640`);
  }
  return lines;
}

export function Arena() {
  return (
    <svg className="court__layer" viewBox={VIEWBOX} preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">
      <defs>
        <linearGradient id="c-sky" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0" stopColor="#04060c" />
          <stop offset="0.5" stopColor="#0b1324" />
          <stop offset="1" stopColor="#16223b" />
        </linearGradient>
        <linearGradient id="c-tier" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0" stopColor="#101a2e" />
          <stop offset="1" stopColor="#1d2d4c" />
        </linearGradient>
        <clipPath id="c-stands-clip">
          <polygon points="-400,64 1200,64 1200,292 -400,292" />
        </clipPath>
      </defs>
      <rect x="-400" width="1600" height="640" fill="url(#c-sky)" />
      <g clipPath="url(#c-stands-clip)">
        <polygon points="-400,64 1200,64 1200,292 -400,292" fill="url(#c-tier)" />
        {[0, 1, 2].map((tier) => (
          <polygon key={tier} points={`-400,${100 + tier * 62} 1200,${100 + tier * 62} 1200,${108 + tier * 62} -400,${108 + tier * 62}`} fill="#2b3f66" opacity={0.7} />
        ))}
        {Array.from({ length: 33 }, (_, i) => (
          <line key={i} x1={400 + (i - 16) * 36} y1="64" x2={400 + (i - 16) * 68} y2="292" stroke="#0a1120" strokeWidth="3" opacity="0.8" />
        ))}
      </g>
      <rect x="-400" y="278" width="1600" height="18" fill="#080c16" />
      <rect x="-400" y="284" width="1600" height="5" fill="#ff7a1a" opacity="0.85" />
      <polygon points="-400,0 1200,0 1200,64 -400,64" fill="#05070c" opacity="0.75" />
      {/* the apron beside the court, dark wood out to the edges of a wide picture */}
      <rect x="-400" y="296" width="1600" height="344" fill="#0c1222" />
      <rect x="-400" y="296" width="1600" height="344" fill="#2a1a0e" opacity="0.5" />
    </svg>
  );
}

/** The crowd: rows of fans in the stands, in three bands that shimmer out of step. */
export function Crowd() {
  const colors = ['#5b6fa0', '#a5648c', '#c58b4b', '#6aa3c9', '#8e7fd0', '#d7d3c8'];
  const patterns = [0, 1, 2].map((s) => (
    <pattern key={s} id={`c-fans-${s}`} width="48" height="24" patternUnits="userSpaceOnUse">
      {[0, 1, 2].map((k) => (
        <circle key={`a${k}`} cx={6 + k * 16} cy={7} r={2.4} fill={colors[(k * 2 + s) % colors.length]} />
      ))}
      {[0, 1, 2].map((k) => (
        <circle key={`b${k}`} cx={14 + k * 16} cy={19} r={2.4} fill={colors[(k * 2 + s + 3) % colors.length]} />
      ))}
    </pattern>
  ));
  return (
    <svg className="court__layer court__crowd" viewBox={VIEWBOX} preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">
      <defs>{patterns}</defs>
      {[0, 1, 2].map((s) => (
        <rect key={s} x="-400" y={72 + s * 72} width="1600" height="70" fill={`url(#c-fans-${s})`} className={`court__fans court__fans--${s}`} />
      ))}
    </svg>
  );
}

export function Lights() {
  return (
    <svg className="court__layer court__lights" viewBox={VIEWBOX} preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">
      <defs>
        <linearGradient id="c-beam" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0" stopColor="#fff6dc" stopOpacity="0.5" />
          <stop offset="1" stopColor="#fff6dc" stopOpacity="0" />
        </linearGradient>
      </defs>
      {[-130, 120, 400, 680, 930].map((x, i) => (
        <polygon key={x} points={`${x - 14},0 ${x + 14},0 ${x + 150 - (i % 3) * 20},330 ${x - 170 + (i % 3) * 20},330`} fill="url(#c-beam)" opacity={i === 2 ? 0.32 : 0.3} />
      ))}
    </svg>
  );
}

export function Floor() {
  return (
    <svg className="court__layer" viewBox={VIEWBOX} preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">
      <defs>
        <linearGradient id="c-wood" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0" stopColor="#6b4120" />
          <stop offset="0.5" stopColor="#a8703a" />
          <stop offset="1" stopColor="#cf9855" />
        </linearGradient>
        <radialGradient id="c-sheen" cx="0.5" cy="0.35" r="0.6">
          <stop offset="0" stopColor="#ffe3b0" stopOpacity="0.45" />
          <stop offset="1" stopColor="#ffe3b0" stopOpacity="0" />
        </radialGradient>
        <clipPath id="c-floor-clip">
          <polygon points={FLOOR} />
        </clipPath>
      </defs>
      <polygon points={FLOOR} fill="url(#c-wood)" />
      <g clipPath="url(#c-floor-clip)">
        <path d={boardLines().join(' ')} stroke="#2a1708" strokeWidth="1.3" opacity="0.38" fill="none" />
        <path d="M0 330 H800 M0 372 H800 M0 424 H800 M0 488 H800 M0 566 H800" stroke="#2a1708" strokeWidth="0.8" opacity="0.18" fill="none" />
        {/* the painted lane */}
        <polygon points="345,296 455,296 481,468 319,468" fill="#143a8f" opacity="0.88" />
        <polygon points="345,296 455,296 481,468 319,468" fill="none" stroke="#f5f7fb" strokeWidth="3" />
        <ellipse cx="400" cy="468" rx="62" ry="21" fill="none" stroke="#f5f7fb" strokeWidth="3" />
        <path d="M338 468 A62 21 0 0 0 462 468" fill="none" stroke="#f5f7fb" strokeWidth="3" strokeDasharray="9 7" />
        <ellipse cx="400" cy="296" rx="32" ry="6" fill="none" stroke="#f5f7fb" strokeWidth="2" opacity="0.7" />
        {/* the three-point line and the centre circle */}
        <path d="M205 296 L205 352 A195 190 0 0 0 595 352 L595 296" fill="none" stroke="#f5f7fb" strokeWidth="3.5" />
        <ellipse cx="400" cy="640" rx="150" ry="56" fill="none" stroke="#f5f7fb" strokeWidth="3.5" />
        <ellipse cx="400" cy="640" rx="40" ry="15" fill="#ff7a1a" opacity="0.28" />
        <rect x="0" y="0" width="800" height="640" fill="url(#c-sheen)" />
      </g>
      <polyline points="150,296 -80,640" stroke="#f5f7fb" strokeWidth="3" fill="none" opacity="0.9" />
      <polyline points="650,296 880,640" stroke="#f5f7fb" strokeWidth="3" fill="none" opacity="0.9" />
      <line x1="150" y1="296" x2="650" y2="296" stroke="#f5f7fb" strokeWidth="3.5" />
    </svg>
  );
}

export function FloorGlow() {
  return (
    <svg className="court__layer court__glow" viewBox={VIEWBOX} preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">
      <defs>
        <radialGradient id="c-glow" cx="0.5" cy="0.5" r="0.5">
          <stop offset="0" stopColor="#ffb23f" stopOpacity="0.55" />
          <stop offset="1" stopColor="#ff7a1a" stopOpacity="0" />
        </radialGradient>
      </defs>
      <ellipse cx={HOOP.x} cy="545" rx="420" ry="130" fill="url(#c-glow)" />
    </svg>
  );
}
