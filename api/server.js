var WebSocketServer = require('ws').Server;
var fs = require('fs');
var wsPy = new WebSocketServer({port:8080});
var wsJs = new WebSocketServer({port:8081});
var wsJsSocket = {send: function() { console.log("warning, no js client connected") }};

var qtrons = {
    'chop':0, 'forward':0, 'left':0, 'right':0, 'backward':0, 'look_left':0, 'look_right':0
}

var filename = '../data/datastream_' + new Date().getTime() + '.csv';

fs.appendFile(filename, 'q_chop,q_forward,q_left,q_right,q_backward,q_look_left,q_look_right,actioncount,episode', function (err) {
    if (err) {
        throw err;
    }
});

console.log('streaming websocket data server started')

wsPy.on('connection', function (ws) {
  ws.on('message', function (message) {
    wsJsSocket.send(message);
    pms = JSON.parse(message)
    qtrons[pms.action] = pms.q_value
    fs.appendFile(filename, '\n' + qtrons['chop'] + ',' + qtrons['forward'] + ',' + qtrons['left'] + ',' + qtrons['right'] + ',' + qtrons['backward'] + ',' + qtrons['look_left'] + ',' + qtrons['look_right'] + ',' + pms.step + ',' + pms.episode, function (err) {
        if (err) {
            throw err;
        }
    });
  });
});

wsJs.on('connection', function (ws) {
  wsJsSocket = ws;
});
