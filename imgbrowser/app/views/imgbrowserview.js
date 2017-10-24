var Marionette = require('backbone.marionette');
var lSendUrl = require('../js/comm/query.js');
var ImgCollection = require('../models/imgmodelcollection.js');

var ImgView = Marionette.ItemView.extend({
  template: '#img-template',
  ui: {
    'img': '.thumbnail'
  },
  events: {
    'click @ui.img': 'clickImg'
  },
  triggers:{
    'selectImg': 'select:img',
  },
  onRender: function () {
      // Get rid of that pesky wrapping-div.
      // Assumes 1 child element present in template.
      this.$el = this.$el.children();
      // Unwrap the element to prevent infinitely 
      // nesting elements during re-render.
      this.$el.unwrap();
      this.setElement(this.$el);
  },
  clickImg: function(img){
    console.log(' click img ', img.target.getAttribute('src'), img.target.getAttribute('imgName'));
    this.trigger('selectImg');
  }  
});

var ImgBrowserView = Marionette.CompositeView.extend({  // 2
  // el: '#img-edit-div',
  template: require('../templates/imgbrowserview.html'),  // 4
  childViewContainer: '#img-browser-main-div', 
  collection: new ImgCollection(),
  childView: ImgView, 
  ui: {
  	'fetchbutton': '#img-browser-fetch-btn',
  },
  events: {
  	'click @ui.fetchbutton': 'fetchImg',
  },
  initialize: function(options){  	
  	// this.fetchImg(1);
    this.eventBus = options.eventBus;//保存eventBus  
    this.eventBus.on('cropImg', this.cropImg, this);
  },  
  successFetchFunc: function(response, self){
   var liImg = response['imgList'];
	 console.log(" success fetch img ", liImg); 
   if(liImg.length == 0){
    //no more img
     self.ui.fetchbutton.attr('disabled', true);
   }else{
     for (var i = 0; i < liImg.length; i ++) {
        var imgName = liImg[i]['imgName'];
        var imgDir = liImg[i]['imgDir'];
        var imgCrop = liImg[i]['crop'];
        console.log(imgName, imgDir, imgCrop);
        self.collection.add({
        'imgName': imgName,
        'imgDir': imgDir,
        'imgCrop': imgCrop
       }) 
      };  
      // console.log('!!! ', );
   }
  },
  //fetch the imgs
  fetchImg: function(fetchButton){
    var self = this;
    var fetchTimes = Number(fetchButton.target.getAttribute('fetchtimes'));
    var fetchNum = Number(fetchButton.target.getAttribute('fetcheverytime'));
  	var formData = new FormData();
  	formData.append('beginIndex', fetchTimes * fetchNum);
    formData.append('endIndex', (fetchTimes + 1) * fetchNum);
  	lSendUrl('POST', 'http://localhost:20111/fetchImgs', formData, this.successFetchFunc, self);
    fetchButton.target.setAttribute('fetchtimes', fetchTimes + 1);
  },
   onChildviewSelectImg: function(child){
    console.log(" parent select img ", child.ui.img.attr('src'), child.ui.img.attr('imgName') );
    var para = {
      'imgDir': child.ui.img.attr('src'),
      'imgName':  child.ui.img.attr('imgName'),
    }
    this.eventBus.trigger('chooseEditImg', para);
   },
   cropImg: function(imgName){
    console.log(' crop img ', imgName);
    this.children.each(function(view){
      //console.log(" highlight ", view, view.model.get('key'), paperkey);
      if(view.model.get('imgName') == imgName){
        view.ui.img.removeClass("img-crop-false");
        view.ui.img.addClass("img-crop-true");
      }
    });
   }
});

module.exports = ImgBrowserView;