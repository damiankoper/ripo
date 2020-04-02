import Color from "color";
export class PoolOptions {
  public table = {
    color: {
      // CV2 HSV Color space
      from: [70, 150, 50] as any,
      to: [95, 255, 220] as any
    }
  };

  public init = {
    time: 120
  };

  constructor() {
    this.table.color.from = {
      hsva: this.cvColor2HSVAPicker(this.table.color.from)
    };
    this.table.color.to = {
      hsva: this.cvColor2HSVAPicker(this.table.color.to)
    };
  }

  private cvColor2HSVAPicker(cvColor: Array<number>) {
    return {
      h: cvColor[0] * 2,
      s: cvColor[1] / 255,
      v: cvColor[2] / 255,
      a: 1
    };
  }
}
