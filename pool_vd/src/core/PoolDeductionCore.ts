import { PoolState } from "./models/PoolState/PoolState";
import BallDeduction from "./models/Deduction/BallDeduction";
import { Ball } from "./models/PoolState/Ball";
import { Vector2i } from "./models/PoolState/Vector2i";
import _ from "lodash";
import PolynomialRegression from "js-polynomial-regression";
import { Pocket } from "./models/Deduction/Pocket";
export class PoolDeductionCore {
  readonly pocketCatchRadius = 0.1;
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

  public precision = {
    regressionPolynomialDegree: 3,

    regressionStates: 1,
    inPocketStates: 1,
    appearedStates: 1
  };

  public clearPoolStates() {
    this.poolStateHistory = [];
    this.pockets.forEach(p => p.clear());
  }

  public addPoolState(state: PoolState) {
    this.poolStateHistory.push(state);
    const maxStates = this.getMaxStates();
    if (this.poolStateHistory.length > maxStates)
      this.poolStateHistory = this.poolStateHistory.slice(-(maxStates + 1));
  }

  private getMaxStates() {
    return Math.max(
      this.precision.regressionStates,
      this.precision.inPocketStates,
      this.precision.appearedStates
    );
  }

  public getDeductedPoolState() {
    const ballStatesMap = this.getBallStatesMap();
    const ballDeducedMap = new Map<number, BallDeduction>();

    ballStatesMap.forEach((ballStates, number) => {
      const filteredBallStates: Ball[] = ballStates.filter(x => x) as Ball[];
      const pocket: Pocket | undefined = this.getFallenPocket(
        ballStates,
        filteredBallStates
      );
      if (pocket) {
        pocket.add(filteredBallStates[filteredBallStates.length - 1]);
      } else if (filteredBallStates.length >= this.precision.appearedStates) {
        const deducedBall = this.deduceBall(
          filteredBallStates.slice(-(this.precision.regressionStates + 1))
        );
        ballDeducedMap.set(number, deducedBall);
      }
    });

    const deductedState = _.cloneDeep(
      this.poolStateHistory[this.poolStateHistory.length - 1]
    );

    deductedState.balls = [];
    ballDeducedMap.forEach(ball => {
      deductedState.balls.push(_.cloneDeep(ball));
    });
    deductedState.pockets = this.pockets

    return deductedState;
  }

  private getFallenPocket(
    ballStates: (Ball | undefined)[],
    filteredBallStates: Ball[]
  ): Pocket | undefined {
    const inPocketStates = this.precision.inPocketStates;
    const ball = filteredBallStates[filteredBallStates.length - 1];
    for (const pocket of this.pockets) {
      if (
        pocket.isBallNear(ball) &&
        ballStates.slice(-inPocketStates).filter(x => x).length === 0
      ) {
        return pocket;
      }
    }

    return undefined;
  }

  private getBallStatesMap(): Map<number, (Ball | undefined)[]> {
    const ballStatesMap = new Map<number, (Ball | undefined)[]>();

    this.poolStateHistory.forEach((poolState, i) => {
      poolState.balls.forEach(ball => {
        const ballStates = ballStatesMap.get(ball.number) || [];
        ballStates.push(ball);
        ballStatesMap.set(ball.number, ballStates);
      });

      for (let number = 0; number < 16; number++) {
        const ballStates = ballStatesMap.get(number) || [];
        if (ballStates.length <= i) {
          ballStates.push(undefined);
        }
      }
    });

    return ballStatesMap;
  }

  private deduceBall(ballStates: Ball[]): BallDeduction {
    const uncertainState = ballStates.pop() as Ball;
    const ballDeduction = new BallDeduction(uncertainState);

    const dataX: { x: number; y: number }[] = [];
    const dataY: { x: number; y: number }[] = [];
    ballStates.forEach(ball => {
      dataX.push({ x: ball.detectedAt, y: ball.position.x });
      dataY.push({ x: ball.detectedAt, y: ball.position.y });
    });

    if (ballStates.length > 1) {
      const predictionX = this.predictValue(dataX, uncertainState);
      const predictionY = this.predictValue(dataY, uncertainState);

      if (!isNaN(predictionX) && !isNaN(predictionY)) {
        const predictedPosition = new Vector2i(predictionX, predictionY);
        ballDeduction.position = predictedPosition;
      }
    }
    return ballDeduction;
  }

  private predictValue(data: { x: number; y: number }[], uncertainState: Ball) {
    const model = PolynomialRegression.read(
      data,
      this.precision.regressionPolynomialDegree
    );
    const terms = model.getTerms();
    const prediction = model.predictY(terms, uncertainState.detectedAt);
    return prediction;
  }
}
