var Marionette = require('backbone.marionette');
var lSendUrl = require('../js/comm/query.js');

var ImgBrowserView = Marionette.LayoutView.extend({  // 2
  // el: '#img-edit-div',
  template: require('../templates/imgbrowserview.html'),  // 4
  ui: {
  	'fetchbutton': '#img-browser-fetch-btn',
  },
  events: {
  	'click@fetchbutton': 'fetchImg',
  },
  initialize: function(){  	
  	this.fetchImg();
  },  
  successFetchFunc: function(response){
	console.log(" success fetch img ", response);
  },
  //fetch the imgs
  fetchImg: function(fetchNum){
  	console.log(" fetch image ");
  	if(fetchNum == undefined)
  		fetchNum = 10;
  	var formData = new FormData();
  	formData.append('fetchNum', fetchNum);
  	lSendUrl('POST', 'http://localhost:20111/fetchImgs', formData, this.successFetchFunc);
  },
});

module.exports = ImgBrowserView;