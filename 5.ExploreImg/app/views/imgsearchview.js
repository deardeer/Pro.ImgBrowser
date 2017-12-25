var Marionette = require('backbone.marionette');
require('jscolor-picker');
var d3 = require('d3');
var $ = require('jquery');
var lSendUrl = require('../js/comm/query.js')
var rgb2hsv = require('../js/comm/rgb2hsv.js')
// var json = require('json-loader');
// var JSON = require('json');

var ImgSearchView = Marionette.LayoutView.extend({ 
	template: require('../templates/imgsearchview.html'),
	ui: {
		'image-color-ok-button': '#image-color-select-ok',
		'image-color-query-button': '#image-color-query',
	},
	events: {
		'click @ui.image-color-ok-button': 'okImageColorSelect',
		'click @ui.image-color-query-button': 'okImageColorQuery',
	},	
	bFetch: false,	
	sQueryConstraint: {},
	initialize: function(options){  
		this.eventBus = options.eventBus;//保存eventBus  
	},
	okImageColorSelect: function(){
		console.log('image color select!', $('.image-jscolor')[0]);
		var selectColor = $('.image-jscolor')[0].style['background-color'];
		
		var rectCount = d3.selectAll('#image-color-div .image-color-rect').size();

		//get the color
		d3.select('#image-color-div .image-color-svg')
		.append('rect')
		.attr('class', 'image-color-rect')
		.attr('x', function(){
			return rectCount > 0? rectCount * (20 + 5): 0;
		})
		.attr('y', 0)
		.attr('width', 20)
		.attr('height', 20)
		.attr('fill', selectColor);
	},
	okImageColorQuery: function(){
		var liColor = [];
		d3.selectAll('#image-color-div .image-color-rect')
		.each(function(d){
			var rgb = d3.rgb(d3.select(this).attr('fill'));
			var hsv = rgb2hsv(rgb.r,rgb.g,rgb.b)
			liColor.push([hsv.h, hsv.s, hsv.v]);
		});
		console.log('image color query!', liColor);
		this.queryImage('image','color',liColor);
	},

	//query
	queryImage: function(objectType, attrType, constraint){
		var self = this;
		this.sQueryConstraint = {
				'object': 'image',
				'query': 'color',
				'constraint': constraint,
		}
		if(!self.bFetch){
			var formData = new FormData();
			var url = 'http://localhost:20111/loadProImgs';//query_' + objectType + '_' + attrType;
			self.eventBus.trigger('set')
	    	lSendUrl('POST', url, formData, this.successQueryFun, self);	
		}else{
			self.eventBus.trigger('queryImgs', this.sQueryConstraint);
		}
	  	
	},

	successQueryFun: function(response, self){
		console.log(' success image query ', response);		
   		self.eventBus.trigger('loadImgs', response);
   		self.eventBus.trigger('queryImgs', self.sQueryConstraint); 
	},
});

module.exports = ImgSearchView;