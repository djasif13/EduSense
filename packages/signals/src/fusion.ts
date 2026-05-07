export type LearnerState =
  | 'focused' | 'engaged' | 'distracted' | 'idle'
  | 'confused' | 'bored' | 'fatigued' | 'note_taking'
  | 'replaying' | 'hesitating' | 'overloaded' | 'unknown';

export interface BehaviorSignals {
  tab_hidden?: boolean;
  idle?: boolean;
  scroll_depth?: number;
  scroll_velocity?: number;
  mouse_entropy?: number;
}

export interface FusionResult {
  state: LearnerState;
  confidence: number;
}

export function fuseSignals(signals: BehaviorSignals): FusionResult {
  if (signals.tab_hidden) return { state: 'distracted', confidence: 0.9 };
  if (signals.idle) return { state: 'idle', confidence: 0.85 };
  if (signals.scroll_depth !== undefined) {
    if (signals.scroll_depth > 0.8) return { state: 'engaged', confidence: 0.75 };
    if (signals.scroll_depth < 0.1) return { state: 'focused', confidence: 0.6 };
  }
  return { state: 'focused', confidence: 0.5 };
}
