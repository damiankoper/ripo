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
    shrink: new Vector2i(106.7, 105.7)
  };

  public init = {
    duration: 120
  };

  public ball = {
    radiusLower: 15,
    radiusUpper: 30,
    threshold: 15
  };

  public deduction = {
    precision: {
      regressionPolynomialDegree: 3,
      regressionStates: 1,
  
      inPocketStates: 1,
      appearedStates: 1
    }
  }

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
