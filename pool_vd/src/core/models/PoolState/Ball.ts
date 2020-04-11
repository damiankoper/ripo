import { Vector2i, IVector2i } from "./Vector2i";

export enum BallType {
  SOLID = "SOLID",
  STRIPED = "STRIPED"
}

export interface IBall {
  number: number;
  position: IVector2i;
  type: BallType;
  detectedAt: number;
}
export class Ball implements IBall {
  constructor(object: IBall) {
    this.number = object.number;
    this.type = object.type;
    this.position = new Vector2i(object.position.x, object.position.y);
    this.detectedAt = object.detectedAt;
  }
  number = 0;
  position: Vector2i = new Vector2i(0, 0);
  type: BallType = BallType.SOLID;
  detectedAt: number;
}
