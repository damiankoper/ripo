import { Vector2i } from "../PoolState/Vector2i";
import { Ball } from "../PoolState/Ball";

export class Pocket {
  public position: Vector2i;
  public catchRadius: number;
  public name: string;
  public balls: Ball[] = [];
  constructor(name: string, position: Vector2i, catchRadius = 0.01) {
    this.name = name;
    this.position = position;
    this.catchRadius = catchRadius;
  }

  public isBallNear(ball: Ball) {
    return this.position.sub(ball.position).length() <= this.catchRadius;
  }

  public add(ball: Ball) {
    console.log(this.balls.every(b => b.number !== ball.number));

    if (this.balls.every(b => b.number !== ball.number)) {
      this.balls.push(ball);
    }
  }

  public clear() {
    this.balls = [];
  }
}
