import { BallType } from "./PoolState/Ball";

const colors = ["yellow", "blue", "red", "purple", "orange", "green", "maroon"];
function generateBalls(colors: string[], type: BallType) {
  return colors.map(color => ({
    color,
    type
  }));
}

export const poolData = {
  table: {
    ratio: 0.5
  },
  ball: {
    size: 49,
    stripeSize: 0.2,
    textSize: 0.24
  },
  balls: [
    ...generateBalls(["white"], BallType.SOLID),
    ...generateBalls(colors, BallType.SOLID),
    ...generateBalls(["black"], BallType.SOLID),
    ...generateBalls(colors, BallType.STRIPED)
  ]
};
