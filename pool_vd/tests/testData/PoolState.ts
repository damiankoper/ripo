import { PlayerName } from "../../src/core/models/PoolState/Player";
import { PoolState } from "../../src/core/models/PoolState/PoolState";
import { BallType } from "../../src/core/models/PoolState/Ball";
import { Vector2i } from "../../src/core/models/PoolState/Vector2i";

export const poolState: PoolState = {
  cues: [
    {
      player: {
        color: [0, 100, 100],
        name: PlayerName.A
      },
      positionStart: new Vector2i(0.4, 1.18),
      positionEnd: new Vector2i(0.6, 0.6)
    }
  ],
  balls: [
    {
      number: 15,
      position: new Vector2i(0.45, 0.6),

      type: BallType.STRIPED
    },
    {
      number: 8,
      position: new Vector2i(0, 0),
      type: BallType.SOLID
    },
    {
      number: 2,
      position: new Vector2i(0.3, 0.5),

      type: BallType.SOLID
    },
    {
      number: 3,
      position: new Vector2i(0.7, 0.2),
      type: BallType.SOLID
    },
    {
      number: 11,
      position: new Vector2i(1, 1),
      type: BallType.STRIPED
    }
  ]
};