var Marionette = require('backbone.marionette');

var ImgEditView = Marionette.LayoutView.extend({  // 2
  template: require('../templates/imgeditview.html'),  // 4
  initialize: function(){
  	console.log(" init ", this.model.get('imgName'));
  }
});

module.exports = ImgEditView;