export interface IVector2i {
  x: number;
  y: number;
}

export class Vector2i implements IVector2i {
  x = 0;
  y = 0;

  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
  }

  public add(v: Vector2i) {
    return new Vector2i(this.x + v.x, this.y + v.y);
  }

  public multiply(a: number | Vector2i) {
    if (a instanceof Vector2i) {
      return new Vector2i(this.x * a.x, this.y * a.y);
    }
    return new Vector2i(this.x * a, this.y * a);
  }

  public length() {
    return Math.sqrt(this.x ** 2 + this.y ** 2);
  }

  public clone() {
    return new Vector2i(this.x, this.y);
  }
}
