import { poolState } from "./testData/PoolState";
const server = require("http").createServer();
var socketio = require("socket.io")(server);
let timer: any;
socketio.on("connection", function(socket: any) {
  timer = setInterval(() => {
    socket.emit("poolState", poolState);
    poolState.balls.forEach(ball => {
      ball.position.x += (Math.random() - 0.5) / 100;
      ball.position.y += (Math.random() - 0.5) / 100;
    });
  }, 1000 / 30);
  socket.on("disconnect", () => {
    clearInterval(timer);
  });
});
server.listen(8888);
