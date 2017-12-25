var Marionette = require('backbone.marionette');
var d3 = require('d3');
require('../css/viewstyle.css');
var rgb2hsv = require('../js/comm/rgb2hsv.js')

var ImgEntityView = Marionette.ItemView.extend({
	template: require('../templates/imgitem.html'),	
	// el: '.imgitem',
	initialize: function(){		
		// var rect = d3.select('#img-info-' + this.model.get('imgName'))
		// .append('rect')
		// .attr('class', 'testrect')
		// .attr('width', 10)
		// .attr('height', 10)
		// .attr('x', '10')
		// .attr('y', '10')
		// .style('fill', 'black');
		// console.log("  init img ", '#img-info-' + this.model.get('imgName'), rect);
	},
	onRender: function () {
        // Get rid of that pesky wrapping-div.
        // Assumes 1 child element present in template.
        this.$el = this.$el.children();
        // Unwrap the element to prevent infinitely 
        // nesting elements during re-render.
        this.$el.unwrap();
        this.setElement(this.$el);
    }
});

var ImgListView = Marionette.CollectionView.extend({ 
	tagName: 'ul',
	childView: ImgEntityView,  
 	reorderOnSort : true,
	showImg: function(){
	}
});

var ImgShowView = Marionette.LayoutView.extend({
	template: require('../templates/imgshowview.html'),	
	regions:{
		imglist: '#img-show-div'
	},
	initialize: function(options){  
		this.eventBus = options.eventBus;//保存eventBus  
		this.eventBus.on('loadImgs', this.loadImgs, this);
		this.eventBus.on('queryImgs', this.queryImgs, this);
	},
	onShow: function(){
		this.imgListView = new ImgListView({
			collection: this.collection,
		});
		this.showChildView('imglist', this.imgListView);
	},
	loadImgs: function(para){
		var liImg = para['imgList'];
		for (var i = 0; i < liImg.length; i++) {
			var imgInfo = liImg[i];	
			if(this.collection.where({'imgName': imgInfo['imgName']}).length > 0)
				continue;
			this.collection.add({
				'imgName': imgInfo['imgName'],
				'imgDir': imgInfo['imgDir'],
				'mainColor': imgInfo['mainColor'],
			})
		};
		console.log(' collection size ', this.collection.length);
	},
	queryImgs: function(queryConstraint){
		console.log("queryImgs!");
		switch(queryConstraint['object']){
			case 'image':
				this.queryImgs_Image(queryConstraint);
				break;
			default:
				break;
		}
	},
	queryImgs_Image: function(queryConstraint){
		console.log('queryImgs_Image');
		switch(queryConstraint['query']){
			case 'color':
				this.computeHSLColorDis(queryConstraint['constraint']);
				break;
		}
	},
	computeHSLColorDis: function(liHSL){
		console.log("computeHSLColorDis ", liHSL);
		this.collection.forEach(function(model){
			var liMainColor = model.get('mainColor');
			var length = liHSL.length;
			if(liHSL.length > liMainColor.length)
				length = liMainColor.length
			var queryDis = 0.;
			for (var index = 0; index < length; index ++){
				var DC = liMainColor[index];
				var density = DC[0];
				var referHSL = liHSL[index];
				var mainHSL = DC[1].slice(3, 6);		
				var diff = (referHSL[0] - mainHSL[0]) * (referHSL[0] - mainHSL[0]) + (referHSL[1] - mainHSL[1]) * (referHSL[1] - mainHSL[1]) + (referHSL[2]/255. - mainHSL[2]/255.) * (referHSL[2]/255. - mainHSL[2]/255.);
				diff = Math.sqrt(diff);
				// console.log(' referHSL ', referHSL, ' mainHSL ', mainHSL, ' diff ', diff);
				queryDis += density * diff; //Math.sqrt((referHSL - mainHSL)*(referHSL - mainHSL))
				// queryDis += (density * Math.sqrt((referHSL - mainHSL)*(referHSL - mainHSL)))
				// console.log(' query dis ', referHSL, mainHSL);
			};
			model.set('queryDis', queryDis);
			// console.log('queryDis ', queryDis);
		})
		this.collection.sort();
		// console.log(' collection attribute ', this.collection.attributes)
	},
	showImg: function(para){
		console.log('show img!', para);		
	},
});


module.exports = ImgShowView;