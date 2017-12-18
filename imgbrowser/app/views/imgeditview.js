var Marionette = require('backbone.marionette');
var d3 = require('d3');
var Histogram = require('../js/comm/comhistogram.js');
// var Plotly = require('./customplotly.js');
// var Plotly = require('./customplotly.js');
// var Cropper = require('cropperjs'); 
var lSendUrl = require('../js/comm/query.js');

var ImgEditView = Marionette.LayoutView.extend({  // 2
  template: require('../templates/imgeditview.html'),  // 4
  ui: {
  	'editimg': 'img',
    'checkcropbtn': '#check-crop-btn',
    'deleteimgbtn': '#delete-img-btn',
    'showcontour': '#show-contour-input',
  },

  events:{
    'click @ui.checkcropbtn': 'checkCropped',
    'click @ui.deleteimgbtn': 'deleteImg',
    'click @ui.showcontour': 'setContourVisible'
  },

  liContourIndex: [],
  liPropertyInfo: [],
  proInfoMap: {
  },

  initialize: function(options){
  	this.eventBus = options.eventBus;
    this.eventBus.on('chooseEditImg', this.chooseEditImg, this);
  },
  chooseEditImg: function(para){
  	console.log(' choose edit img ', para);
  	this.ui.editimg.attr('src', para['imgDir']);
    this.ui.editimg.attr('imgName', para['imgName']);
    var imgPro = para['imgPro'];
    if(imgPro){
      //fetch the meta info of img
      this.getImgProInfo(para['imgName']);
    }
  },
  //get teh img processed info
  getImgProInfo: function(imgName){
    var self = this;
    var formData = new FormData();
    var url = 'http://localhost:20111/getProInfo';    
    formData.append('imgName', imgName);
    lSendUrl('POST', url, formData, this.successGetProInfo, self);
  },

  successGetProInfo: function(response, self){

    //default the check button checked
    self.ui.showcontour.prop('checked', true);

    //get the contours
    console.log('Contours ', response['contours']);

    var offsetTop = document.getElementById('edit-img').offsetTop;
    var offsetLeft = document.getElementById('edit-img').offsetLeft;

    var imgHeight = document.getElementById('edit-img').getBoundingClientRect().height;
    var imgWidth = document.getElementById('edit-img').getBoundingClientRect().width;

    //adjust edit-cover-svg
    d3.select('#edit-cover-svg')
    .style('visibility', 'visible')
    .style('left', offsetLeft)
    .style('width', imgWidth)
    .style('height', imgHeight)
    .style('top', offsetTop);

    //adjust property-cover-svg
    var viewHeight = window.visualViewport.height, viewWidth = window.visualViewport.width;
    d3.select('#pro-info-svg')
    .style('visibility', 'visible')
    .style('left', 0)
    .style('top', document.getElementById('edit-cover-svg').getBoundingClientRect().height + document.getElementById('edit-cover-svg').getBoundingClientRect().top)
    .style('width', viewWidth)
    .style('height', viewHeight - document.getElementById('edit-cover-svg').getBoundingClientRect().height - document.getElementById('edit-cover-svg').getBoundingClientRect().top);

    //clear contours
    d3.selectAll('.contour-path')
    .remove();

    self.liContourIndex = [];
    self.liPropertyInfo = [];
    self.proInfoMap = {};

    for (var i = response['contours'].length - 1; i >= 0; i--) {

      var contour_str = response['contours'][i];
      var contour = JSON.parse(contour_str);

      if(i == response['contours'].length - 1){
        self.liPropertyInfo = Object.keys(contour);
        self.liPropertyInfo.splice(self.liPropertyInfo.indexOf('c_points'), 1);
        console.log(" liPropertyInfo ", self.liPropertyInfo);
      }

      var mapContourAttr = {};
      var licontour_attr = Object.keys(contour);
      for(var j = 0; j < licontour_attr.length; j ++){
        var contour_attr = licontour_attr[j];
        if(contour_attr != 'c_points')
          mapContourAttr[contour_attr] = contour[contour_attr];
      }

      self.proInfoMap[i] = mapContourAttr;
      self.liContourIndex.push(i);

      liPoint = JSON.parse(contour['c_points']);
      liXY = [];
      for(var j = 0; j < liPoint.length/2; j ++){
        liXY.push({
          'x': liPoint[j * 2],
          'y': liPoint[j * 2 + 1],
        });
      }
      liXY.push(liXY[0]);

      console.log(' lipoint ', liXY);
      var lineFunction = d3.line()
                          .x(function(d){return d.x;})
                          .y(function(d){return d.y;});
      d3.select('#edit-cover-svg')
      .append('path')
      .attr('class', 'contour-path')
      .data([liXY])
      .attr('contourindex', i)
      .attr('d', lineFunction)
      .style('stroke', 'blue')
      .style('stroke-width', '2px')
      .style('fill', 'none')
      .on('mouseover', function(){
        d3.select(this).style('stroke', 'red');
      })
      .on('mousedown', function(){
        var contourIndex = d3.select(this).attr('contourindex');
        console.log('click', self.proInfoMap[contourIndex]);
        // var bbox = d3.select(this).node().getBBox();
        // var temp_left = bbox.x + bbox.width;
        // var temp_top = bbox.y + bbox.height;
        // d3.select("#pro-info-g").remove();
        // g = d3.select('#edit-cover-svg')
        // .append('g')
        // .attr('id', 'pro-info-g');
        // // .attr('transform', 'translate(' + + ',' + this.offsetTop + ')');
        // g.append('rect')
        // .data
        // .attr('x', temp_left)
        // .attr('y', temp_top)
        // .attr('width', 100)
        // .attr('height', 100)
        // .style('fill', 'white')
        // .style('stroke', 'black');
      })
      .on('mouseout', function(){
        d3.select(this).style('stroke', 'blue');
      });

    };

    //draw pro info panel
    self.drawProInfoPanel();
    self.addProInfos();

    console.log('success get pro info ');
  },

  addProInfos: function(){

      proInfoG = d3.select('#pro-info-svg');

      var proPanelBox = document.getElementById('pro-info-svg').getBoundingClientRect();

      //clear the histograms
      d3.selectAll('.his-g')
      .remove();

      //add the XX-hist-svg
      var iColumnNum = 2, columnWidthPad = 20;
      var iRowNum = Math.ceil(this.liPropertyInfo.length / iColumnNum), rowHeightPad = 20;
      var histWidth = (proPanelBox.width - columnWidthPad * (iColumnNum + 1))/iColumnNum;
      var histHeight = (proPanelBox.height - rowHeightPad * (iRowNum + 1))/iRowNum;
      for (var i = 0; i < this.liPropertyInfo.length; i++) {

        var iColumnIndex = i % iColumnNum;
        var iRowIndex = Math.floor(i / iColumnNum);
        var propertyName = this.liPropertyInfo[i];

        var histG = proInfoG.append('g')
        .attr('id', propertyName + '-his-g')
        .attr('class', 'his-g')
        .attr('transform', 'translate(' + ((iColumnIndex + 1) * columnWidthPad + iColumnIndex * histWidth) + ',' + ((iRowIndex + 1) * rowHeightPad + iRowIndex * histHeight) + ')')
        .attr('width', histWidth)
        .attr('height', histHeight);

        histG.append('rect')
        .style('width', histWidth)
        .style('height', histHeight)
        .style('left', 0)
        .style('top', 0)
        .style('fill','none')
        .style('stroke', '#03a9f4');
      };
     
      //draw attributes
      for(var p = 0; p < this.liPropertyInfo.length; p ++){
        var propertyName = this.liPropertyInfo[p];
        var bNumber = true;
        var liValue = [];
        for (var i = this.liContourIndex.length - 1; i >= 0; i--) {
            var iContourIndex = this.liContourIndex[i];
            var proInfo = this.proInfoMap[iContourIndex];
            if(Histogram.isNumber(proInfo[propertyName]) == false){
              bNumber = false;
              liValue.push(proInfo[propertyName]);
            }else
              liValue.push(+proInfo[propertyName]);
        };
        // if(bNumber == false){
        //   console.log(propertyName, liValue.length, liValue);
        //   continue;
        // }
        if(bNumber)       
          Histogram.drawHistogram(propertyName + '-his-g', liValue, propertyName);
        else{
          if(propertyName == 'mean_color'){
            console.log(' color !!! ', liValue);
            Histogram.drawCateogricalHistogram(propertyName + '-his-g', liValue, true, propertyName);
          }
          else
            Histogram.drawCateogricalHistogram(propertyName + '-his-g', liValue, false, propertyName);
        }
      }    
  },

  drawProInfoPanel: function(){

    // d3.selectAll('.panel-bbox')
    // .remove();

    // var svgBBox = document.getElementById('edit-cover-svg').getBoundingClientRect();
    // var imgBBox = document.getElementById('edit-img').getBoundingClientRect();
    // var imgInfoTop = imgBBox.top, imgInfoLeft = imgBBox.left;
    // var imgInfoHeight = imgBBox.height, imgInfoWidth = imgBBox.width;

    // d3.select('#edit-cover-svg')
    // .append('rect')
    // .attr('class', 'panel-bbox')
    // .attr('width', imgInfoWidth)
    // .attr('height', imgInfoHeight)
    // .attr('x', imgInfoLeft)
    // .attr('y', imgInfoTop)
    // .style('stroke', 'black')
    // .style('fill', 'none');

    // var padHeight = 10;
    // var proInfoTop = imgBBox.top + imgBBox.height + padHeight;
    // d3.select('#edit-cover-svg')
    // .append('svg')
    // .attr('id', 'pro-panel-bbox')
    // .attr('class', 'panel-bbox')
    // .attr('x', imgInfoLeft)
    // .attr('y', proInfoTop)
    // .attr('width', svgBBox.width - 10)
    // .attr('height', svgBBox.top + svgBBox.height - imgInfoTop - imgInfoHeight - padHeight)
    // .style('border', 'black')
    // .style('background', 'yellow');

    // proInfoG = d3.select('#edit-cover-svg')
    // .append('g')
    // .attr('id', 'proinfo-g')
    // .attr('transform', 'translate(' + imgInfoLeft + ',' + proInfoTop + ')');
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

  setContourVisible: function(){
    var visible = this.ui.showcontour.is(':checked');   
    d3.selectAll('.contour-path')
    .style('visibility', visible==true?'visible':'hidden');
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

  