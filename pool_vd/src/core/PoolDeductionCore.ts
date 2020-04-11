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
   * 1. stopień wielomianu
   * 2. ilość stanów w interpolacji >= 2
   * ---
   * 3. ilość stanów do wykrycia wpadnięcia
   * 4. ilość stanów do zniknięcia bili
   * 5. Ilość stanów do uznania bili za obecną
   * 
   * 
   * OSZAR 
   */

  private precision = 1;

  public setPrecision(i: number) {
    this.precision = i;
  }
  public getPrecision() {
    return this.precision;
  }

  public addPoolState(state: PoolState) {
    this.poolStateHistory.push(state);
    if (this.poolStateHistory.length > this.precision)
      this.poolStateHistory.shift();
  }

  public getDeductedPoolState() {
    const ballStatesMap = this.getBallStatesMap();
    const ballDeducedMap = new Map<number, BallDeduction>();

    ballStatesMap.forEach((ballStates, number) => {
      ballDeducedMap.set(number, this.deduceBall(ballStates));
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
        const ballState = ballStatesMap.get(ball.number) || [];
        ballState.push(ball);
        ballStatesMap.set(ball.number, ballState);
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

    if (this.precision >= 3) {
      const degree = this.precision - 1;

      const modelX = PolynomialRegression.read(dataX, degree);
      const termsX = modelX.getTerms();
      const predictionX = modelX.predictY(termsX, uncertainState.detectedAt);

      const modelY = PolynomialRegression.read(dataY, degree);
      const termsY = modelY.getTerms();
      const predictionY = modelY.predictY(termsY, uncertainState.detectedAt);

      if (!isNaN(predictionX) && !isNaN(predictionY)) {
        const predictedPosition = new Vector2i(predictionX, predictionY);
        ballDeduction.position = predictedPosition;
      }
    }
    return ballDeduction;
  }
}
