import { poolState } from "./testData/PoolState";
const server = require("http").createServer();
var socketio = require("socket.io")(server);
let timer: any;
socketio.on("connection", function(socket: any) {
  timer = setInterval(() => {
    socket.emit("poolState", poolState);
    poolState.balls.forEach(ball => {
      ball.position.x += 0.001;
    });
  }, 1000 / 60);
  socket.on("disconnect", () => {
    clearInterval(timer);
  });
});
server.listen(8888);
