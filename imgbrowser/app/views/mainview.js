var Marionette = require('backbone.marionette')

var ImgCollection = require('../models/imgmodelcollection.js');
var ImgModel = require('../models/imgmodel.js')

var ImgEditView = require('./imgeditview.js')
var ImgBrowserView = require('./imgbrowserview.js')

require('../css/viewstyle.css');

var MainView = Marionette.LayoutView.extend({  // 2
  el: '#app-hook',  // 3
  template: require('../templates/mainview.html'),  // 4
  regions: {
  	'img-edit-region': '#img-edit-div',
  	'img-browser-region': '#img-browser-div'
  },
  onShow: function(){
  	console.log(" on show ");

    this.eventBus = _.extend({}, Backbone.Events);    

  	this.imgEditView = new ImgEditView({
  		model: this.editImgModel,
      eventBus: this.eventBus
  	});
  	this.imgBrowserView = new ImgBrowserView({      
      eventBus: this.eventBus
    });
  	this.showChildView('img-edit-region', this.imgEditView);
  	// this.getRegion('img-edit-region').show(this.imgEditView);
  	this.getRegion('img-browser-region').show(this.imgBrowserView);

  },  
});

module.exports = MainView;