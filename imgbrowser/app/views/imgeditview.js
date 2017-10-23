var Marionette = require('backbone.marionette');

var ImgEditView = Marionette.LayoutView.extend({  // 2
  template: require('../templates/imgeditview.html'),  // 4
  ui: {
  	'editimg': 'img'
  },
  initialize: function(options){
  	this.eventBus = options.eventBus;
    this.eventBus.on('chooseEditImg', this.chooseEditImg, this);
  },
  chooseEditImg: function(src){
  	console.log(' choose edit img ', src);
  	this.ui.editimg.attr('src', src);
  }
});

module.exports = ImgEditView;