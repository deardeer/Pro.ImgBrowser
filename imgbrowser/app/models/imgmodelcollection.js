var Backbone = require('backbone')
var ImgModel = require('./imgmodel.js');

var ImgCollection = Backbone.Collection.extend({
	model: ImgModel,
});

module.exports = ImgCollection;