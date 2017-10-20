var Backbone = require('backbone')

var ImgModel = Backbone.Model.extend({
	'imgName': '',
	'cropped': '',
})

module.exports = ImgModel;