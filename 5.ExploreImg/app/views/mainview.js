var Marionette = require('backbone.marionette')

var ImgSearchView = require('./imgsearchview.js')
var ImgShowView = require('./imgshowview.js')

var ImgCollection = require('../models/imgcollection.js')

require("css/viewstyle.css")

var MainView = Marionette.LayoutView.extend({  // 2
  el: '#app-hook',  // 3
  template: require('../templates/mainview.html'), // 4
  regions: {
  	'img-search-region': "#img-search-div",
  	'img-show-region': '#img-show-div',
  },
  onShow: function(){

    this.eventBus = _.extend({}, Backbone.Events); 
    imgCollection = new ImgCollection();

  	this.imgSearchView = new ImgSearchView({      
      eventBus: this.eventBus,
      collection: imgCollection,
    });
  	this.imgShowView = new ImgShowView({      
      eventBus: this.eventBus,      
      collection: imgCollection,
    });
  	this.showChildView('img-search-region', this.imgSearchView);
  	this.showChildView('img-show-region', this.imgShowView);
  }
});

module.exports = MainView;

// var MainView = Marionette.LayoutView.extend({  // 2
//   el: '#app-hook',  // 3
//   template: require('../templates/mainview.html'),  // 4
//   regions: {
//   	'img-edit-region': '#img-edit-div',
//   	'img-browser-region': '#img-browser-div'
//   },
//   onShow: function(){
//   	console.log(" on show ");

//     this.eventBus = _.extend({}, Backbone.Events);    

//   	this.imgEditView = new ImgEditView({
//   		model: this.editImgModel,
//       eventBus: this.eventBus
//   	});
//   	this.imgBrowserView = new ImgBrowserView({      
//       eventBus: this.eventBus
//     });
//   	this.showChildView('img-edit-region', this.imgEditView);
//   	// this.getRegion('img-edit-region').show(this.imgEditView);
//   	this.getRegion('img-browser-region').show(this.imgBrowserView);

//   },  
// });

// module.exports = MainView;