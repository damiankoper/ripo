export enum PlayerName {
  A,
  B
}
export interface IPlayer {
  name: PlayerName;
  color: [number, number, number];
}
export class Player {
  constructor(object: IPlayer) {
    this.name = object.name;
    this.color = object.color;
  }
  name: PlayerName = PlayerName.A;
  color: [number, number, number] = [0, 0, 0];
}
