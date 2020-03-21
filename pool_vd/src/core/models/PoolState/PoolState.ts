import { Ball, IBall } from "./Ball";
import { Cue, ICue } from "./Cue";

export interface IPoolState {
  balls: IBall[];
  cues: ICue[];
}

export class PoolState implements IPoolState {
  constructor(object: IPoolState) {
    this.balls = object.balls.map(b => new Ball(b));
    this.cues = object.cues.map(c => new Cue(c));
  }
  balls: Ball[] = [];
  cues: Cue[] = [];
}
