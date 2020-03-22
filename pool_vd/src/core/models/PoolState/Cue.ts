import { Vector2i, IVector2i } from "./Vector2i";
import { Player, PlayerName, IPlayer } from "./Player";

export interface ICue {
  positionStart: IVector2i;
  positionEnd: IVector2i;
  player: IPlayer;
}

export class Cue implements ICue {
  constructor(object: ICue) {
    this.positionStart = new Vector2i(
      object.positionStart.x,
      object.positionStart.y
    );
    this.positionEnd = new Vector2i(object.positionEnd.x, object.positionEnd.y);
    this.player = new Player(object.player);
  }
  positionStart: Vector2i = new Vector2i(0, 0);
  positionEnd: Vector2i = new Vector2i(0, 0);
  player: Player = { color: [255, 0, 0], name: PlayerName.A };
}
