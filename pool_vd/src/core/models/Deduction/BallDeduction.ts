import { Ball } from "../PoolState/Ball";
import { Vector2i } from "../PoolState/Vector2i";

export default class BallDeduction extends Ball {
  public velocity?: Vector2i;
  public acceleration?: Vector2i;
}
