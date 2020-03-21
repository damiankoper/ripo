import { PlayerName } from "../../src/core/models/PoolState/Player";
import { PoolState } from "../../src/core/models/PoolState/PoolState";
import { BallType } from "../../src/core/models/PoolState/Ball";

export const poolState: PoolState = {
  cues: [
    {
      player: {
        color: [60, 100, 100],
        name: PlayerName.A
      },
      positionStart: {
        x: 0,
        y: 400
      },
      positionEnd: {
        x: 0,
        y: 600
      }
    }
  ],
  balls: [
    {
      number: 15,
      position: {
        x: 0.45,
        y: 0.6
      },
      type: BallType.STRIPED
    },
    {
      number: 8,
      position: {
        x: 0.0,
        y: 0.0
      },
      type: BallType.SOLID
    },
    {
      number: 2,
      position: {
        x: 0.3,
        y: 0.5
      },
      type: BallType.SOLID
    },
    {
      number: 3,
      position: {
        x: 0.7,
        y: 0.2
      },
      type: BallType.STRIPED
    },
    {
      number: 11,
      position: {
        x: 1,
        y: 1
      },
      type: BallType.STRIPED
    }
  ]
};
