
var MainView = require('./views/mainview')

var mainview = new MainView();  // 5

mainview.render();  // 6
mainview.triggerMethod('show');

console.log('ssss')
