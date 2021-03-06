// Create a file that will configure your custom bundle - e.g. lean_plotly.js 
var Plotly = require('plotly.js/lib/core');

// Load in the trace types you need e.g. pie, and choropleth
Plotly.register([
    require('plotly.js/lib/histogram'),
    // require('plotly.js/lib/choropleth')
]);

// Export the custom build
module.exports = Plotly;