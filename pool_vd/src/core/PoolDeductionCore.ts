import { PoolState } from "./models/PoolState/PoolState";

export class PoolDeductionCore {
  /**
   * Contains history states limited to given precision
   */
  private poolStateHistory: PoolState[] = [];

  /**
   * How many history stated are user to determine real pool state
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
    /**
     * For tests pool state is based on last given state
     */
    return this.poolStateHistory[this.poolStateHistory.length - 1];
  }
}
