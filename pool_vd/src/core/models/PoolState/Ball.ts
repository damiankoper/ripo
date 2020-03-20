import { Vector2i } from "./Vector2i";

export enum BallType {
  SOLID = "SOLID",
  STRIPED = "STRIPED"
}

export class Ball {
  number = 0;
  position: Vector2i = { x: 0, y: 0 };
  type: BallType = BallType.SOLID;
}
