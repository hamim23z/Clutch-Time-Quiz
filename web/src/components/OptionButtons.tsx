import type { ScenarioOption } from '../types';

interface Props {
  options: readonly ScenarioOption[];
  onPick: (key: string) => void;
}

export function OptionButtons({ options, onPick }: Props) {
  return (
    <div className="options" role="group" aria-label="Your options">
      {options.map((option) => (
        <button key={option.key} type="button" className="option" onClick={() => onPick(option.key)}>
          {option.label}
        </button>
      ))}
    </div>
  );
}
