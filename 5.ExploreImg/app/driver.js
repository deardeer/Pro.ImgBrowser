
var Marionette = require('backbone.marionette');  // 1
var MainView = require("./views/mainview")
require("bootstrap-webpack");

var App = new Marionette.Application({

  onStart: function(){
    //console.log(" options ", options);

    var mainview = new MainView();  // 5

	mainview.render();  // 6
	mainview.triggerMethod('show');
    // console.log('mystring','chenshuai') 
  }  

});

App.start();
console.log(" app ");

