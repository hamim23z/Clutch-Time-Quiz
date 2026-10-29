import { act, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { SHOT_NAMES } from './shots';
import { createSoundPlayer, loadSoundSetting, saveSoundSetting, SHOT_TONES, SOUND_KEY, SoundProvider, useSound } from './sound';
import type { StorageLike } from './storage';

const memory = (): StorageLike & { data: Map<string, string> } => {
  const data = new Map<string, string>();
  return { data, getItem: (k) => data.get(k) ?? null, setItem: (k, v) => void data.set(k, v) };
};

/** A fake AudioContext that counts the oscillators started. */
function fakeAudio() {
  const started: number[] = [];
  class Fake {
    state = 'running';
    currentTime = 0;
    destination = {};
    resume = () => Promise.resolve();
    createOscillator() {
      const node = { type: '', frequency: { setValueAtTime: () => undefined, exponentialRampToValueAtTime: () => undefined }, connect: (n: unknown) => n, start: (t: number) => void started.push(t), stop: () => undefined };
      return node;
    }
    createGain() {
      return { gain: { setValueAtTime: () => undefined, exponentialRampToValueAtTime: () => undefined }, connect: (n: unknown) => n };
    }
  }
  return { Ctor: Fake as unknown as new () => AudioContext, started };
}

describe('the sound setting', () => {
  it('is off by default and remembers on/off', () => {
    const store = memory();
    expect(loadSoundSetting(store)).toBe(false);
    saveSoundSetting(store, true);
    expect(store.data.get(SOUND_KEY)).toBe('on');
    expect(loadSoundSetting(store)).toBe(true);
    saveSoundSetting(store, false);
    expect(loadSoundSetting(store)).toBe(false);
  });

  it('survives storage that throws or does not exist', () => {
    const broken: StorageLike = { getItem: () => { throw new Error('blocked'); }, setItem: () => { throw new Error('full'); } };
    expect(loadSoundSetting(broken)).toBe(false);
    expect(() => saveSoundSetting(broken, true)).not.toThrow();
    expect(loadSoundSetting(null)).toBe(false);
    expect(() => saveSoundSetting(null, true)).not.toThrow();
  });
});

describe('the sound player', () => {
  it('has tones for every shot and needs no audio files', () => {
    for (const name of SHOT_NAMES) expect(SHOT_TONES[name].length).toBeGreaterThan(0);
  });

  it('plays nothing before the visitor has interacted, then plays when enabled', () => {
    const { Ctor, started } = fakeAudio();
    const player = createSoundPlayer(() => true, Ctor);
    player.play('dunk');
    expect(started).toHaveLength(0);
    player.arm();
    player.play('dunk');
    expect(started).toHaveLength(SHOT_TONES.dunk.length);
  });

  it('plays nothing while the setting is off, even after an interaction', () => {
    const { Ctor, started } = fakeAudio();
    const player = createSoundPlayer(() => false, Ctor);
    player.arm();
    player.play('swish');
    expect(started).toHaveLength(0);
  });

  it('stays silent, without throwing, when Web Audio is missing or fails', () => {
    const none = createSoundPlayer(() => true, null);
    none.arm();
    expect(() => none.play('swish')).not.toThrow();
    const Broken = class { constructor() { throw new Error('no audio'); } } as unknown as new () => AudioContext;
    const failing = createSoundPlayer(() => true, Broken);
    failing.arm();
    expect(() => failing.play('swish')).not.toThrow();
  });
});

function Harness() {
  const { enabled, toggle, play } = useSound();
  return (
    <>
      <button onClick={toggle}>toggle {enabled ? 'on' : 'off'}</button>
      <button onClick={() => play('swish')}>play</button>
    </>
  );
}

describe('SoundProvider', () => {
  it('starts off, and stays silent until the first interaction', async () => {
    const { Ctor, started } = fakeAudio();
    const store = memory();
    store.data.set(SOUND_KEY, 'on'); // enabled from a previous visit
    render(<SoundProvider storage={store} ctor={Ctor}><Harness /></SoundProvider>);
    expect(screen.getByRole('button', { name: 'toggle on' })).toBeInTheDocument();
    act(() => screen.getByRole('button', { name: 'play' }).click()); // a programmatic click is not a user interaction
    expect(started).toHaveLength(0);
    const user = userEvent.setup();
    await user.click(screen.getByRole('button', { name: 'play' })); // a real pointer interaction arms it
    await user.click(screen.getByRole('button', { name: 'play' }));
    expect(started.length).toBeGreaterThan(0);
  });

  it('toggles, remembers the choice, and works with no storage', async () => {
    const user = userEvent.setup();
    const store = memory();
    const { unmount } = render(<SoundProvider storage={store} ctor={null}><Harness /></SoundProvider>);
    expect(screen.getByRole('button', { name: 'toggle off' })).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'toggle off' }));
    expect(store.data.get(SOUND_KEY)).toBe('on');
    unmount();
    const second = render(<SoundProvider storage={store} ctor={null}><Harness /></SoundProvider>);
    expect(screen.getByRole('button', { name: 'toggle on' })).toBeInTheDocument();
    second.unmount();
    render(<SoundProvider storage={null} ctor={null}><Harness /></SoundProvider>);
    await user.click(screen.getByRole('button', { name: 'toggle off' }));
    expect(screen.getByRole('button', { name: 'toggle on' })).toBeInTheDocument();
    vi.restoreAllMocks();
  });
});
