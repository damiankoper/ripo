import { Vector2i } from "./PoolState/Vector2i";

export interface HSVA {
  a: number;
  h: number;
  s: number;
  v: number;
}

export class PoolOptions {
  public table = {
    color: {
      // CV2 HSV Color space
      from: {
        hsva: this.cvColor2HSVAPicker([70, 150, 50])
      },
      to: {
        hsva: this.cvColor2HSVAPicker([95, 255, 220])
      }
    },
    shift: new Vector2i(-3.4, -3.9),
    shrink: new Vector2i(106.7, 107)
  };

  public init = {
    duration: 120
  };

  public ball = {
    radiusLower: 15,
    radiusUpper: 30,
    threshold: 15,

    dp: 1,
    minDist: 22,
    param1: 90,
    param2: 9
  };

  public deduction = {
    precision: {
      historyStates: 15,
      inPocketStates: 5,
      velocityStates: 5
    }
  };

  public cvColor2HSVAPicker(cvColor: Array<number>): HSVA {
    return {
      h: cvColor[0] * 2,
      s: cvColor[1] / 255,
      v: cvColor[2] / 255,
      a: 1
    };
  }

  public hsvaColor2Cv(hsva: HSVA) {
    return [hsva.h / 2, Math.round(hsva.s * 255), Math.round(hsva.v * 255)];
  }
}
