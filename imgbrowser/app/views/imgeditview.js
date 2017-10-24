var Marionette = require('backbone.marionette');
// var Cropper = require('cropperjs'); 
var lSendUrl = require('../js/comm/query.js');

var ImgEditView = Marionette.LayoutView.extend({  // 2
  template: require('../templates/imgeditview.html'),  // 4
  ui: {
  	'editimg': 'img',
    'checkcropbtn': '#check-crop-btn',
    'deleteimgbtn': '#delete-img-btn',
  },
  events:{
    'click @ui.checkcropbtn': 'checkCropped',
    'click @ui.deleteimgbtn': 'deleteImg',
  },
  initialize: function(options){
  	this.eventBus = options.eventBus;
    this.eventBus.on('chooseEditImg', this.chooseEditImg, this);
  },
  chooseEditImg: function(para){
  	console.log(' choose edit img ', para);
  	this.ui.editimg.attr('src', para['imgDir']);
    this.ui.editimg.attr('imgName', para['imgName']);
  },
  successCropImg: function(response, self){
    console.log(' successCropImg ', response['imgName']);
    self.eventBus.trigger('cropImg', response['imgName']);
  },
  checkCropped: function(){
    var self = this;
    var imgName = this.ui.editimg.attr('imgName');
    var imgSrc = this.ui.editimg.attr('src');
    console.log(' check cropped ', imgName, imgSrc);  
    var formData = new FormData();
    formData.append('imgName', imgName);
    formData.append('crop', true);
    lSendUrl('POST', 'http://localhost:20111/cropImg', formData, this.successCropImg, self); 
  },
  successDeleteImg: function(){
    console.log(" successDeleteImg ");
  },
  deleteImg: function(){
    var imgName = this.ui.editimg.attr('imgName');
    var imgSrc = this.ui.editimg.attr('src');
    console.log(' delete img ', imgName, imgSrc);
    var formData = new FormData();
    formData.append('imgName', imgName);
    lSendUrl('POST', 'http://localhost:20111/deleteImg', formData, this.successDeleteImg, self); 

  }
  // enableCrop: function(){
		// // console.log(' enable crop ');
		// $('#edit-img').on('load', function(){
		// 	console.log(" herhe ? ");
		// 	var image = document.getElementById('edit-img')
		// 	var cropper = new Cropper(image, {
		// 		crop: function(e){
		// 			console.log(e.detail.x);
		// 			console.log(e.detail);
		// 		}
		// 	});
		// });
		// // $('#edit-img').one('load', function(){
		// // 	var image = document.getElementById('edit-img');
		// // 	console.log(' loaded ');
		// // 	var cropper = new Cropper(image, {
		// // 		crop: function(e){
		// // 				console.log(e.detail.x);
		// // 		}
		// // 	});
		// // })
		// console.log(" croppp !! ");
		// // var cropper = new Cropper(image, {
		// // crop: function(e){
		// // 		console.log(e.detail.x);
		// // }
		// // });
  //         // ready: function () {
  //         //   var clone = this.cloneNode();
  //         //   clone.className = ''
  //         //   clone.style.cssText = (
  //         //     'display: block;' +
  //         //     'width: 100%;' +
  //         //     'min-width: 0;' +
  //         //     'min-height: 0;' +
  //         //     'max-width: none;' +
  //         //     'max-height: none;'
  //         //   );
  //         //   clone.id = 'previewimage';
  //         //   each(previews, function (elem) {	              
  //         //     elem.appendChild(clone.cloneNode());
  //         //   });
  //         // },

  //         // crop: function (e) {
  //         //   var data = e.detail;
  //         //   var cropper = this.cropper;
  //         //   var imageData = cropper.getImageData();
  //         //   var previewAspectRatio = data.width / data.height;

  //         //   each(previews, function (elem) {
  //         //     var previewImage = elem.getElementsByTagName('img').item(0);
  //         //     var previewWidth = elem.offsetWidth;
  //         //     var previewHeight = previewWidth / previewAspectRatio;
  //         //     var imageScaledRatio = data.width / previewWidth;

  //         //     elem.style.height = previewHeight + 'px';
  //         //     previewImage.style.width = imageData.naturalWidth / imageScaledRatio + 'px';
  //         //     previewImage.style.height = imageData.naturalHeight / imageScaledRatio + 'px';
  //         //     previewImage.style.marginLeft = -data.x / imageScaledRatio + 'px';
  //         //     previewImage.style.marginTop = -data.y / imageScaledRatio + 'px';
  //         //   });
  //         // },

  //         // cropend: function(e){
  //         //   var cropper = this.cropper;
  //         // }
  //       // });

		// // button.onclick = function(){
		// // 	var image = cropper.getCroppedCanvas().toDataURL("image/jpg").replace("image/png", "image/octet-stream");  // here is the most important part because if you dont replace you will get a DOM 18 exception.
		// // 	document.getElementById('saveA').href = image;
		// // 	document.getElementById('saveA').download = 'name.jpg'; 
		// // 	document.getElementById('saveA').click();
		// // 	// window.location.href=image; // it will save locally
		// // };
 	//  },
});

module.exports = ImgEditView;

  