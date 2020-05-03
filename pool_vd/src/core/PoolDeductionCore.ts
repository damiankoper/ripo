import { PoolState } from "./models/PoolState/PoolState";
import { Ball } from "./models/PoolState/Ball";
import { Vector2i } from "./models/PoolState/Vector2i";
import _ from "lodash";
import { Pocket } from "./models/Deduction/Pocket";
import { poolState } from "../../tests/testData/PoolState";
export class PoolDeductionCore {
  readonly pocketCatchRadius = 0.05;
  readonly pockets = [
    new Pocket("Top-left", new Vector2i(0, 0), this.pocketCatchRadius),
    new Pocket("Top-middle", new Vector2i(0.5, 0), this.pocketCatchRadius),
    new Pocket("Top-right", new Vector2i(1, 0), this.pocketCatchRadius),
    new Pocket("Botton-right", new Vector2i(1, 1), this.pocketCatchRadius),
    new Pocket("Bottom-middle", new Vector2i(0.5, 1), this.pocketCatchRadius),
    new Pocket("Bottom-left", new Vector2i(0, 1), this.pocketCatchRadius)
  ];

  /**
   * Contains history states limited to given precision
   */
  private poolStateHistory: PoolState[] = [];
  private ballsHistory: Map<number, Ball[]>[] = [];

  public precision = {
    historyStates: 1,
    inPocketStates: 1,
    velocityStates: 1
  };

  public clearPoolStates() {
    this.poolStateHistory = [];
    this.pockets.forEach(p => p.clear());
  }

  public addPoolState(state: PoolState) {
    this.processState(state);

    this.poolStateHistory.push(state);
    this.addBallHistory(state);

    const maxStates = this.getMaxStates();
    if (this.poolStateHistory.length > maxStates)
      this.poolStateHistory = this.poolStateHistory.slice(-(maxStates + 1));
    if (this.ballsHistory.length > maxStates)
      this.ballsHistory = this.ballsHistory.slice(-(maxStates + 1));
  }

  public addBallHistory(state: PoolState) {
    const ballsState = new Map<number, Ball[]>();

    state.balls.forEach(b => {
      const balls = ballsState.get(b.number) || [];
      balls.push(b);
      ballsState.set(b.number, balls);
    });

    this.ballsHistory.push(ballsState);
  }

  private getMaxStates() {
    return Math.max(
      this.precision.historyStates,
      this.precision.inPocketStates,
      this.precision.velocityStates
    );
  }

  public getDeductedPoolState() {
    const lastState =
      _.cloneDeep(_.last(this.poolStateHistory)) || new PoolState(poolState);
    lastState.pockets = this.pockets;

    lastState.balls = [];
    for (let n = 0; n < 16; n++) {
      const last = _.last(this.getBallHistory(n, this.precision.historyStates));
      if (last) lastState.balls.push(_.cloneDeep(last));
    }
    return lastState;
  }

  private processState(state: PoolState) {
    const ballMap = new Map<number, Ball[]>();
    state.balls.forEach(ball => {
      const ballStates = ballMap.get(ball.number) || [];
      ballStates.push(ball);
      ballMap.set(ball.number, ballStates);
    });
    const balls = [];
    state.balls = state.balls.filter(
      ball => ballMap.get(ball.number)?.length === 1 || this.isBallValid(ball)
    );
  }

  private isBallValid(ball: Ball): boolean {
    const ballHistory: Ball[] = this.getBallHistory(
      ball.number,
      this.precision.velocityStates
    );
    let ballValid = true;
    if (ballHistory.length >= 2) {
      const start = _.first(ballHistory) as Ball;
      const stop = _.last(ballHistory) as Ball;
      const time = stop.detectedAt - start.detectedAt;
      const avgVelocity = stop.position.sub(start.position).multiply(1 / time);

      const stopCurrentDistance = ball.position.sub(stop.position).length();
      const velocityDistance = avgVelocity
        .multiply(ball.detectedAt - stop.detectedAt)
        .length();

      if (
        stopCurrentDistance > 0.05 &&
        Math.abs(stopCurrentDistance - velocityDistance) > 0.05
      )
        ballValid = false;
    }

    return ballValid && _.inRange(ball.number, 0, 16);
  }

  private getBallHistory(num: number, states: number): Ball[] {
    const ballHistory: Ball[] = [];

    this.ballsHistory.slice(-(states + 1)).forEach(balls => {
      const ballState = balls.get(num);
      if (ballState) ballHistory.push(...ballState);
    });
    return ballHistory;
  }
}
