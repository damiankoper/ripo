import { Vector2i } from "./Vector2i";
import { Player, PlayerName } from "./Player";

export class Cue {
  positionStart: Vector2i = { x: 0, y: 0 };
  positionEnd: Vector2i = { x: 0, y: 0 };
  player: Player = { color: [255, 0, 0], name: PlayerName.A };
}
