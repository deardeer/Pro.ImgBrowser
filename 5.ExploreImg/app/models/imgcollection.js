var ImgModel = require('./imgmodel.js');

var ImgCollection = Backbone.Collection.extend({
    
    model: ImgModel,

    sortBy: "queryDis",
    sortA: function(value){
        this.sortBy = value;
        this.sort();
    },
    //define compare function
    comparator : function(item1, item2){
        //console.log("this sort ", this.sortBy, item1, item2);
        if(this.sortBy == 'hsl'){
            return this.sortByHSL(item1, item2);
        }else if(this.sortBy == "queryDis")
            return this.sortbyQueryDis(item1, item2); //item1.get('year').localeCompare(item2.get('year'));  
            //return this.sortbyYear(item1, item2);
        else if(this.sortBy == "imgName")
            return this.sortbyImgName(item1, item2);//item1.get('key').localeCompare(item2.get('key'));  
            ////return this.sortbyKey(item1, item2);
    },

    sortByHSL: function(item1, item2){

    },

    sortbyQueryDis: function(item1, item2){
        // console.log('comp ', item1.get('queryDis'), item2.get('queryDis'));
        return item1.get('queryDis') - (item2.get('queryDis'));        
    },
    
    sortbyImgName: function(item1, item2){
        return item1.get('imgName').localeCompare(item2.get('imgName'));  
    }
    
    // sortBy: "author",
    
    //set_sortBy: function (value) {
    //},
       
    // sortA: function(value){
    //     this.sortBy = value;
    //     this.sort();
    // },
    
    // updateFilterTags: function(tagList){
    //     console.log(" update filter tags!!!!! ", tagList);    
    // },
    
    // //define compare function
    // comparator : function(item1, item2){
    //     //console.log("this sort ", this.sortBy, item1, item2);
        
    //     if(this.sortBy == "year")
    //         return this.sortbyYear(item1, item2); //item1.get('year').localeCompare(item2.get('year'));  
    //         //return this.sortbyYear(item1, item2);
    //     else if(this.sortBy == "author")
    //         return this.sortbyAuthor(item1, item2);//item1.get('key').localeCompare(item2.get('key'));  
    //         ////return this.sortbyKey(item1, item2);
    // },
    
    // sortbyYear: function(item1, item2){
    //     return item1.get('year').localeCompare(item2.get('year'));        
    // },
    
    // sortbyAuthor: function(item1, item2){
    //     return item1.get('key').localeCompare(item2.get('key'));  
    // }
});

module.exports = ImgCollection;
