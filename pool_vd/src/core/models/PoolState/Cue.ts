import { Vector2i, IVector2i } from "./Vector2i";

export interface ICue {
  positionStart: IVector2i;
  positionEnd: IVector2i;
}

export class Cue implements ICue {
  constructor(object: ICue) {
    this.positionStart = new Vector2i(
      object.positionStart.x,
      object.positionStart.y
    );
    this.positionEnd = new Vector2i(object.positionEnd.x, object.positionEnd.y);
  }
  positionStart: Vector2i = new Vector2i(0, 0);
  positionEnd: Vector2i = new Vector2i(0, 0);
}
