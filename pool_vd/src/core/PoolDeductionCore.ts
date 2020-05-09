import { PoolState } from "./models/PoolState/PoolState";
import { Ball } from "./models/PoolState/Ball";
import { Vector2i } from "./models/PoolState/Vector2i";
import _ from "lodash";
import { Pocket } from "./models/Deduction/Pocket";
import { poolState } from "../../tests/testData/PoolState";
export class PoolDeductionCore {
  readonly pocketCatchRadius = 0.115;
  readonly pockets = [
    new Pocket("Top-left", new Vector2i(0.1, 0.08), this.pocketCatchRadius),
    new Pocket("Top-middle", new Vector2i(1.03, 0.04), this.pocketCatchRadius),
    new Pocket("Top-right", new Vector2i(1.97, 0.08), this.pocketCatchRadius),
    new Pocket(
      "Botton-right",
      new Vector2i(1.97, 0.99),
      this.pocketCatchRadius
    ),
    new Pocket(
      "Bottom-middle",
      new Vector2i(1.03, 1.03),
      this.pocketCatchRadius
    ),
    new Pocket("Bottom-left", new Vector2i(0.1, 0.99), this.pocketCatchRadius)
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

  public clearPockets() {
    this.pockets.forEach(p => p.clear());
    console.log("Cleared pockets");
  }

  public addPoolState(state: PoolState) {
    this.processPockets();
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
    lastState.pockets = _.cloneDeep(this.pockets);

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
    state.balls = state.balls.filter(
      ball => ballMap.get(ball.number)?.length === 1 || this.isBallValid(ball)
    );
  }

  private isBallValid(ball: Ball): boolean {
    const ballHistory: Ball[] = this.getBallHistory(
      ball.number,
      this.precision.velocityStates
    );

    const rangeCheck = this.ballRangeCheck(ball);
    if (!rangeCheck) return false;
    const inPocketCheck = this.inPocketCheck(ball);
    if (inPocketCheck) return false;
    const velocityCheck = this.ballVelocityCheck(ballHistory, ball);
    if (!velocityCheck) return false;

    return true;
  }

  private ballVelocityCheck(ballHistory: Ball[], ball: Ball) {
    if (ballHistory.length >= 2) {
      const start = _.first(ballHistory) as Ball;
      const stop = _.last(ballHistory) as Ball;
      const avgVelocity = this.getBallVelocity(start, stop);

      const stopCurrentDistance = ball.position.sub(stop.position).length();
      const velocityDistance = avgVelocity
        .multiply(ball.detectedAt - stop.detectedAt)
        .length();

      if (
        stopCurrentDistance > 0.1 &&
        Math.abs(stopCurrentDistance - velocityDistance) > 0.1
      )
        return false;
    }
    return true;
  }

  private ballRangeCheck(ball: Ball) {
    return _.inRange(ball.number, 0, 16);
  }

  private getBallVelocity(start: Ball, stop: Ball): Vector2i {
    const time = stop.detectedAt - start.detectedAt;
    return stop.position.sub(start.position).multiply(1 / time);
  }

  private getBallHistory(num: number, states: number): Ball[] {
    const ballHistory: Ball[] = [];

    this.ballsHistory.slice(-(states + 1)).forEach(balls => {
      const ballState = balls.get(num);
      if (ballState) ballHistory.push(...ballState);
    });
    return ballHistory;
  }

  private inPocketCheck(ball: Ball) {
    if (ball.number === 0) return false;
    for (const pocket of this.pockets) {
      const index = pocket.balls.findIndex(b => b.number === ball.number);
      if (index >= 0) return true;
    }
    return false;
  }

  private processPockets() {
    for (let n = 0; n < 16; n++) {
      const ballsStates: Array<Ball | null> = new Array(
        this.precision.inPocketStates + 1
      ).fill(null);
      this.ballsHistory
        .slice(-this.precision.inPocketStates - 1)
        .forEach((ballsHistory, i) => {
          const balls = ballsHistory.get(n) || [];
          if (balls.length > 0) ballsStates[i] = balls[0];
        });

      if (n == 13) console.log(ballsStates);

      if (
        ballsStates.slice(1).filter(x => x === null).length >=
        this.precision.inPocketStates
      ) {
        const b = ballsStates[0];
        if (b) {
          if (n == 13)
            console.log(_.cloneDeep(b.position), this.pockets[5].position);
          const pocket = this.pockets.find(p => p.isBallNear(b));
          pocket?.add(b);
        }
      }
    }
  }
}
