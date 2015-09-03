var actions = {
  'forward': [],
  'backward': [],
  'left': [],
  'right': [],
  'look_left': [],
  'look_right': [],
  'chop': []
};

// create charts
actionCharts = {}
for (var action in actions) {
  actionCharts[action] = new Morris.Line({
    element: action + '_chart',
    data: actions[action],
    xkey: action + '_id',
    ykeys: ['q_value'],
    labels: ['Q-value for ' + action],
    parseTime: false
  });
};

// connect to websocket server
var ws = new WebSocket("ws://localhost:8081");

// when message is received..
ws.onmessage = function(event) {
  //console.log("received: ", JSON.parse(event.data))
  var data = JSON.parse(event.data);

  var action = data['action'];
  var value = data['q_value'];
  var step = data['step'];
  var episode = data['episode'];

  var x_axis = episode * 1000 + step // assume max 999 actions per episode

  var data_point = {};
  data_point[action + '_id'] = x_axis;
  data_point["q_value"] = value;
  actions[action].push(data_point);

  //console.log("pushed: ", data_point);

  actionCharts[action].setData(actions[action]);
};





//  var q_values = [
//    { year: '2008', value: 20 },
//    { year: '2009', value: 10 },
//    { year: '2010', value: 5 },
//    { year: '2011', value: 5 }
//  ];
