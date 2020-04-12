import { PoolState } from "./models/PoolState/PoolState";
import BallDeduction from "./models/Deduction/BallDeduction";
import { Ball } from "./models/PoolState/Ball";
import { Vector2i } from "./models/PoolState/Vector2i";
import _ from "lodash";
import PolynomialRegression from "js-polynomial-regression";
export class PoolDeductionCore {
  /**
   * Contains history states limited to given precision
   */
  private poolStateHistory: PoolState[] = [];

  /**
   * //TODO: Pozdzielić precyzję dla:
   * 3. ilość stanów do wykrycia wpadnięcia
   * 4. ilość stanów do zniknięcia bili
   * 5. Ilość stanów do uznania bili za obecną
   */

  public precision = {
    regressionPolynomialDegree: 3,

    regressionStates: 1,
    inPocketStates: 1,
    appearedStates: 1
  };

  public addPoolState(state: PoolState) {
    this.poolStateHistory.push(state);
    const maxStates = this.getMaxStates();
    console.log(maxStates);
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
      if (ballStates.length > this.precision.appearedStates) {
        const deducedBall = this.deduceBall(
          ballStates.slice(-(this.precision.regressionStates + 1))
        );
        ballDeducedMap.set(number, deducedBall);
      }
    });

    const deductedState = _.cloneDeep(
      this.poolStateHistory[this.poolStateHistory.length - 1]
    );

    deductedState.balls = [];
    ballDeducedMap.forEach((ball, number) => {
      deductedState.balls.push(_.cloneDeep(ball));
    });

    return deductedState;
  }

  private getBallStatesMap(): Map<number, Ball[]> {
    const ballStatesMap = new Map<number, Ball[]>();
    this.poolStateHistory.forEach(poolState => {
      poolState.balls.forEach(ball => {
        const ballStates = ballStatesMap.get(ball.number) || [];
        ballStates.push(ball);
        ballStatesMap.set(ball.number, ballStates);
      });
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
