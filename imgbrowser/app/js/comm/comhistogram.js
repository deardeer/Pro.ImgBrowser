var _ = require('underscore')
var d3 = require('d3')

function histogram(){

	var Info = new Object;

	Info.computeDisConfigure = function(liValue, bColor){
		var self = this;
		var disConfig =	{'valueList': []}; 
		var bNumber = this.isNumber(liValue[0]);
		if(bNumber == true){
			var defaultBinNum = 50;
			// var propertyType = self.getPropertyTypebyId(iPropertyId); //, 'value ', m_mapPropertyIdValueList[iPropertyId]);
			var maxProValue = _.max(liValue);
			var minProValue = _.min(liValue);
			var binValue;
			if(maxProValue == minProValue){
				defaultBinNum = 1;
				binValue = 0;
			}else{
			 	binValue = (maxProValue - minProValue)/(defaultBinNum-1);					
			}
			//number
			disConfig['minValue'] = minProValue, disConfig['maxValue'] = maxProValue;
			disConfig['binNum'] = defaultBinNum;
			disConfig['binValueRange'] = binValue;
			disConfig['getBinIndex'] = function(value){
				if(this.minValue == this.maxValue){
					return 0;
				}
				var binIndex = parseInt((value - this.minValue)/(this.binValueRange));
				// //console.log('value', value, ' number binindex ', binIndex);
				return binIndex;
			};
			disConfig['getBinValue'] = function(iBinIndex){
				var thisBinValue = this.minValue + (iBinIndex * this.binValueRange);
				return thisBinValue;
			}
		}else{
			var valueSet = new Set(liValue);
			if(bColor == false){						
				valueSet.forEach(function(value){
					disConfig['valueList'].push(value);
				});				
			}else{
				var tempHSVRGBList = [];
				var bHex = false;
				var bUpCase = false;
				valueSet.forEach(function(value){							
					//convert value to RGB
					var rgb = JSON.parse(value);
					var tempRGB = d3.rgb(rgb[0], rgb[1], rgb[2]);
					var tempHSV = self.rgb2hsv(tempRGB);
					console.log(" TEMP HSV ", tempHSV, ' value ', tempRGB, rgb);
					tempHSVRGBList.push({h: tempHSV.h, s: tempHSV.s, v: tempHSV.v, rgb: tempRGB});
				});		

				//sort the HSVList
				function hsvcompare(hsv1, hsv2){
					if(parseInt(hsv1.h) > parseInt(hsv2.h))
						return 1;
					else if(parseInt(hsv1.h) < parseInt(hsv2.h))
						return -1;
					else{
						if(parseInt(hsv1.s) > parseInt(hsv2.s))
							return 1;
						else if(parseInt(hsv1.s) < parseInt(hsv2.s))
							return -1;
						else{
							if(parseInt(hsv1.v) > parseInt(hsv2.v))
								return 1;
							else if(parseInt(hsv1.v) <= parseInt(hsv2.v))
								return -1;
							else
								return 0;
						}
					}
				}		

				tempHSVRGBList.sort(hsvcompare);

				$.each(tempHSVRGBList, function(i, HSVRGB){
					// //console.log(" HSVRGB ", i, ' H ', HSVRGB.h, ' S ', HSVRGB.s, ' V ', HSVRGB.v);
					var tempRGB = HSVRGB.rgb;
					var tempRGB_str = "[" +  tempRGB.r + ', ' + tempRGB.g + ', ' + tempRGB.b + "]";
					disConfig['valueList'].push(tempRGB_str);
				});
			}
			disConfig['binNum'] = disConfig.valueList.length;
			disConfig['getBinIndex'] = function(value){
				return this.valueList.indexOf(value);
			}
			disConfig['getBinValue'] = function(iBinIndex){
				return this.valueList[iBinIndex];
			}			
		}
		return disConfig;
	}

	Info.drawCateogricalHistogram = function(gId, liValue, bColor, title){

		var valueSet = new Set(liValue);
		var disConfig = this.computeDisConfigure(liValue, bColor)

		console.log(' disConfig ', title, disConfig);

		var liCount = [];
		var iBinNum = disConfig.binNum;
		for (var i = 0; i < iBinNum; i++) {
			liCount.push(0);
		};

		for (var i = liValue.length - 1; i >= 0; i--) {
			var value = liValue[i];
			var binIndex = disConfig.getBinIndex(value);
			liCount[binIndex] += 1;
		};

		var histogramG = d3.select('#' + gId);

		histogramG.append('text')
		.attr('x', '0')
		.attr('y', '-2')
		.text(title);
	
		var histWidth = +histogramG.attr('width'), histHeight = +histogramG.attr('height');
		var margin = {top: 0, right: 10, bottom: 0, left: 10};
		var width = histWidth - margin.left - margin.right;
		var height = histHeight - margin.top - margin.bottom;

		var x = d3.scaleLinear()
			  .domain([0, disConfig['valueList'].length])
			  .range([0, width]);
		var y = d3.scaleLinear()
			  .domain([0, _.max(liCount)])
			  .rangeRound([height, 0]);

	    var bar = histogramG.selectAll(".bar")
	    				  .data(liCount)
						  .enter().append("g")
					      .attr("class", "bar")
					      .attr("transform", function(d, i) { return "translate(" + x(i) + "," + y(d) + ")"; });

	    bar.append("rect")
		    .attr("x", 1)
		    .attr("width", function(d, i){return ((x(i + 1) - x(i))) * 0.9;})
		    .attr("height", function(d) { return height - y(d); })
		    .style('fill', function(d, i){
		    	if(!bColor)
		    		return 'black';
		    	else{
		    		var rgb = JSON.parse(disConfig.getBinValue(i));
		    		return 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')';
		    	}
		    });

		var formatCount = d3.format(",.0f");

		if(!bColor){
			bar.append("text")
	    	.style('fill', 'white')
		    .attr("dy", ".45em")
		    .attr("y", 6)
		    .attr("x", function(d, i){return (x(i + 1) - x(i)) / 2;})
		    .attr("text-anchor", "middle")
		    .text(function(d, i){ 
		    	var text = (disConfig.getBinValue(i)) + ': ' + d; 
		    	return text;
		    });
		}	    
	}

	Info.drawColorHistogram = function(gId, liValue){

	}
	//draw the histogram
	Info.drawHistogram = function(gId, liValue, title){

		var histogramG = d3.select('#' + gId);

		var liNormalValue= [];
		var maxValue = _.max(liValue);
		for (var i = liValue.length - 1; i >= 0; i--) {
			liNormalValue.push(liValue[i]/maxValue);
		};

		// liCount = d3.range(100).map(d3.randomBates(10));
		histogramG.append('text')
		.attr('x', '0')
		.attr('y', '-2')
		.text(title);

		var histWidth = +histogramG.attr('width'), histHeight = +histogramG.attr('height');
		var margin = {top: 0, right: 10, bottom: 0, left: 10};
		var width = histWidth - margin.left - margin.right;
		var height = histHeight - margin.top - margin.bottom;

		console.log(' height ', height);
		//x-axis
		var x;
		var bins;
		
		x = d3.scaleLinear()
			  .rangeRound([0, width]);

		bins = d3.histogram()
			    .domain(x.domain())
			    .thresholds(x.ticks(50))
			    (liNormalValue);
		

		console.log(" bins ", bins);

		var y = d3.scaleLinear()
		    .domain([0, d3.max(bins, function(d) { return d.length; })])
		    .range([height, 0]);

		var bar = histogramG.selectAll(".bar")
						  .data(bins)
						  .enter().append("g")
					      .attr("class", "bar")
					      .attr("transform", function(d) { return "translate(" + x(d.x0) + "," + y(d.length) + ")"; });

	    bar.append("rect")
		    .attr("x", 1)
		    .attr("width", x(bins[0].x1) - x(bins[0].x0) - 1)
		    .attr("height", function(d) { return height - y(d.length); })
		    .style('fill', 'black');

		var formatCount = d3.format(",.0f");

	    bar.append("text")
	    	.style('fill', 'white')
		    .attr("dy", ".45em")
		    .attr("y", 6)
		    .attr("x", (x(bins[0].x1) - x(bins[0].x0)) / 2)
		    .attr("text-anchor", "middle")
		    .text(function(d) { 
		    	var text = formatCount(d.length); 
		    	if(text == 0) 
		    		return ""; 
		    	else 
		    		return text;
		    });
	}

	Info.rgb2hsv = function(color) {
	    var rr, gg, bb,
	        r = color.r / 255,
	        g = color.g / 255,
	        b = color.b / 255,
	        h, s,
	        v = Math.max(r, g, b),
	        diff = v - Math.min(r, g, b),
	        diffc = function(c){
	            return (v - c) / 6 / diff + 1 / 2;
	        };

	    if (diff == 0) {
	        h = s = 0;
	    } else {
	        s = diff / v;
	        rr = diffc(r);
	        gg = diffc(g);
	        bb = diffc(b);

	        if (r === v) {
	            h = bb - gg;
	        }else if (g === v) {
	            h = (1 / 3) + rr - bb;
	        }else if (b === v) {
	            h = (2 / 3) + gg - rr;
	        }
	        if (h < 0) {
	            h += 1;
	        }else if (h > 1) {
	            h -= 1;
	        }
	    }
	    return {
	        h: Math.round(h * 360),
	        s: Math.round(s * 100),
	        v: Math.round(v * 100)
	    };
	}


	Info.isNumber = function(value){
		var isNum = _.isNumber(value);
		// var isString = _.isString(exampleProValue);
		return (isNum);
	}

	return Info;
}

var Histogram = new histogram;
module.exports = Histogram;