import { PoolState } from "../../src/core/models/PoolState/PoolState";
import { BallType } from "../../src/core/models/PoolState/Ball";
import { Vector2i } from "../../src/core/models/PoolState/Vector2i";
import { Pocket } from '@/core/models/Deduction/Pocket';

export const poolState: PoolState = {
  cues: [
    {
      positionStart: new Vector2i(0.4, 1.18),
      positionEnd: new Vector2i(0.6, 0.6)
    }
  ],
  balls: [
    {
      number: 15,
      position: new Vector2i(0.45, 0.6),
      type: BallType.STRIPED,
      detectedAt: performance.now()
    },
    {
      number: 8,
      position: new Vector2i(0, 0),
      type: BallType.SOLID,
      detectedAt: performance.now()
    },
    {
      number: 2,
      position: new Vector2i(0.3, 0.5),
      type: BallType.SOLID,
      detectedAt: performance.now()
    },
    {
      number: 3,
      position: new Vector2i(0.7, 0.2),
      type: BallType.SOLID,
      detectedAt: performance.now()
    },
    {
      number: 11,
      position: new Vector2i(1, 1),
      type: BallType.STRIPED,
      detectedAt: performance.now()
    }
  ],
  pockets: [
    {
      position: new Vector2i(0, 0),
      balls: [
        {
          position: new Vector2i(0.7, 0.2),
          number: 11,
          type: BallType.STRIPED,
          detectedAt: performance.now()
        },
        {
          position: new Vector2i(0.7, 0.2),
          number: 12,
          type: BallType.STRIPED,
          detectedAt: performance.now()
        },
        {
          position: new Vector2i(0.7, 0.2),
          number: 7,
          type: BallType.SOLID,
          detectedAt: performance.now()
        }
      ]
    } as Pocket,
    {
      position: new Vector2i(0, 0),
      balls: [
        {
          position: new Vector2i(0.7, 0.2),
          number: 9,
          type: BallType.STRIPED,
          detectedAt: performance.now()
        },
        {
          position: new Vector2i(0.7, 0.2),
          number: 10,
          type: BallType.STRIPED,
          detectedAt: performance.now()
        },
        {
          position: new Vector2i(0.7, 0.2),
          number: 15,
          type: BallType.STRIPED,
          detectedAt: performance.now()
        },
        {
          position: new Vector2i(0.7, 0.2),
          number: 4,
          type: BallType.SOLID,
          detectedAt: performance.now()
        },
        {
          position: new Vector2i(0.7, 0.2),
          number: 3,
          type: BallType.SOLID,
          detectedAt: performance.now()
        }
      ]
    } as Pocket,
    {
      position: new Vector2i(0, 0),
      balls: [
        {
          position: new Vector2i(0.7, 0.2),
          number: 14,
          type: BallType.STRIPED,
          detectedAt: performance.now()
        },
        {
          position: new Vector2i(0.7, 0.2),
          number: 2,
          type: BallType.SOLID,
          detectedAt: performance.now()
        },
        {
          position: new Vector2i(0.7, 0.2),
          number: 5,
          type: BallType.SOLID,
          detectedAt: performance.now()
        }
      ]
    } as Pocket,
    {
      position: new Vector2i(0, 0),
      balls: [
        {
          position: new Vector2i(0.7, 0.2),
          number: 14,
          type: BallType.STRIPED,
          detectedAt: performance.now()
        },
        {
          position: new Vector2i(0.7, 0.2),
          number: 2,
          type: BallType.SOLID,
          detectedAt: performance.now()
        },
        {
          position: new Vector2i(0.7, 0.2),
          number: 5,
          type: BallType.SOLID,
          detectedAt: performance.now()
        }
      ]
    } as Pocket,
    {
      position: new Vector2i(0, 0),
      balls: [
        {
          position: new Vector2i(0.7, 0.2),
          number: 14,
          type: BallType.STRIPED,
          detectedAt: performance.now()
        },
        {
          position: new Vector2i(0.7, 0.2),
          number: 2,
          type: BallType.SOLID,
          detectedAt: performance.now()
        },
        {
          position: new Vector2i(0.7, 0.2),
          number: 5,
          type: BallType.SOLID,
          detectedAt: performance.now()
        }
      ]
    } as Pocket,
    {
      position: new Vector2i(0, 0),
      balls: [
        {
          position: new Vector2i(0.7, 0.2),
          number: 14,
          type: BallType.STRIPED,
          detectedAt: performance.now()
        },
        {
          position: new Vector2i(0.7, 0.2),
          number: 2,
          type: BallType.SOLID,
          detectedAt: performance.now()
        },
        {
          position: new Vector2i(0.7, 0.2),
          number: 5,
          type: BallType.SOLID,
          detectedAt: performance.now()
        }
      ]
    } as Pocket
  ]
};
