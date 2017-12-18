var webpack = require('webpack');
var path = require('path');
module.exports = {
  entry: './app/driver.js', //entry js
  devtool: 'source-map' ,
  module: {
    loaders: [
      { test: /\.json$/, 
        loader: "json-loader" 
      },
      {
          test: /\.js$/,
          loader: 'ify-loader'
      },
      {
        test: /\.html$/,
        loader: 'underscore-template-loader'
      },
      {
        test: /\.css$/,
        loaders: ['style', 'css'],
      },
      // the file-loader emits files. 
      { test: /\.(woff|woff2)$/,  loader: "url-loader?limit=10000&mimetype=application/font-woff" },
      { test: /\.ttf$/,    loader: "file-loader" },
      { test: /\.eot$/,    loader: "file-loader" },
      { test: /\.svg$/,    loader: "file-loader" }
    ]
  },
  output: {
    path: path.join(__dirname,'static/js'), 
    filename: 'bundle.js'
  },
  plugins: [
    new webpack.ProvidePlugin({
      _: 'underscore',
      $: "jquery",
      jQuery: "jquery"
    }),
  ],
  resolve: {
    modulesDirectories: [__dirname + '/node_modules'],
    root: path.join(__dirname ,'app')
  },
  resolveLoader: {
    root: path.join(__dirname ,'node_modules')
  }
};