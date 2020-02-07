(function () {
  'use strict';

  angular
   .module('search.app')
   .controller('MainController', MainController)
   .service('DataService', DataService)
   .controller('HomeController', HomeController)
   .controller('VisualController', VisualController)
   .service('ConfigService', ConfigService)
   .controller('QueryController', QueryController)
   .service('APIService', APIService)

   DataService.$inject = ['$http', '$q', '$timeout', '$state']
   function DataService($http, $q, $timeout, $state) {

     var service = this;
     service.search_string = '';
     service.showVisual = true;

     service.setParam = function (value) {
       service.search_string = value;
     }
     service.getParam = function () {
       return service.search_string;
     }
     service.getData = function () {
       var response = [];
       if (!service.search_string || service.search_string.length == 0){
         // console.log('changestate');
         $state.go('search', {}, {reload: true});
       }
       else {
         var response = $http({
           method: 'GET',
           url: 'basic/search_result',
           params: {search: service.search_string}
         })
       }
       return response;
     }

     service.setVisual = function (value) {
       service.showVisual = value;
     }
     service.getVisual = function () {
       return service.showVisual;
     }

   }

   function APIService() {
     this.positive = 0;
     this.negative = 0;
     this.neutral = 0;
     this.category = {};
     this.setSentimentData = function (value1, value2, value3) {
       this.positive = value1;
       this.negative = value2;
       this.neutral = value3;
     }
     this.getSentimentData = function () {
       return {
         pos: this.positive,
         neg: this.negative,
         neu: this.neutral
       };
     }
     this.setCategoryData = function (value) {
       this.category = value;
     }
     this.getCategoryData = function () {
       return this.category;
     }
   }

   function ConfigService() {
     var config = this;
     config.queryVisual = false;
     config.setVisual = function (value) {
       config.queryVisual = value;
     }
     config.getVisual = function () {
       return config.queryVisual;
     }

   }

   QueryController.$inject = ['APIService', 'DataService', '$state']
   function QueryController(APIService, DataService, $state) {
     var qctrl = this;
     if (!DataService.search_string || DataService.search_string.length == 0){
       // console.log('changestate');
       $state.go('search', {}, {reload: true});
     }
     var sentimentData = APIService.getSentimentData();
     // console.log(sentimentData.pos);
     // console.log(sentimentData.neg);
     // console.log(sentimentData.neu);
     if (sentimentData.pos == 0 && sentimentData.neg == 0 && sentimentData.neu == 0 ){
       var nodata = {text: 'No Results', bold:true, fontSize:20}
       var series = [{values:[]}]
     } else {
       var series = [
         {
           'values':[sentimentData.pos],
           'text': 'Positive'
         },
         {
           "values":[sentimentData.neg],
           'text': 'Negative'
         },
         {
           "values": [sentimentData.neu],
           'text': 'Neutral'
          }
       ]
     }
     qctrl.sentiment = {
       "graphset": [{
         "type":"pie3d",
         "title":{
           "text":"Sentiment Analysis"
         },
         "noData": nodata,
         "series": series
       }]
     };

     var categoryData = APIService.getCategoryData();

     if (Object.keys(categoryData).length == 0) {
       var nodata = {text: 'No Results', bold:true, fontSize:20}
       var series = [{values:[]}]
     } else {
       var series = [
         {
           'values':[categoryData[0]],
           'text': 'Healthcare/Achievement/Address'
         },
         {
           "values":[categoryData[1]],
           'text': 'Power/Violence/Love'
         },
         {
           "values":[categoryData[2]],
           'text': 'President/Leader/Community'
          },
         {
           "values":[categoryData[3]],
           'text': 'Elections'
          },
         {
           "values":[categoryData[4]],
           'text': 'Youth/Life'
          },
         {
           "values":[categoryData[5]],
           'text': 'Climate/News'
         },
         {
           "values":[categoryData[6]],
           'text': 'Women Empowerment/Nation/Job/Debate'
         },
         {
           "values":[categoryData[7]],
           'text': 'Indian Politics'
          },
         {
           "values":[categoryData[8]],
           'text': 'Economy/History'
          },
         {
           "values":[categoryData[9]],
           'text': 'Campaign/Support/Gratitude'
         },
         {
           "values":[categoryData[10]],
           'text': 'Others'
         }
       ]
     }

     qctrl.category = {
       "graphset": [{
         "type":"pie3d",
         "title":{
           "text":"Topic Categorization"
         },
         "noData": nodata,
         "series": series
       }]
     };

   }


   VisualController.$inject = ['DataService', '$state'];
   function VisualController(DataService, $state) {
     var visual = this;
     if (DataService.getVisual() == true) {
       // console.log('changestate');
       $state.go('search', {}, {reload: true});
     }
     // console.log('visual');
     visual.sent = false;
     visual.cat = false;

     visual.sentimentClicked = function () {
       visual.sent = true;
       visual.cat = false;
        visual.myConfig = {
        type: "bar3d",
        series: [
        {
          values:[50,47,46,37,38,50,56,59,48,38,52,58,33,57,31]
        },
        {
          values:[7,11,14,13,11,8,11,14,5,19,15,12,16,10,20]  //negative
        },
        {
          values:[43,42,40,50,51,42,33,27,47,43,33,30,51,33,49] //positive
        }
        ]
        };
     }
     visual.categoryClicked = function () {
       visual.sent = false;
       visual.cat = true;
       visual.pieChart = {
         "graphset": [{
           "type":"pie3d",
           // "plotarea": {
           //   'margin': 'dynamic dynamic dynamic dynamic',
           //   'marginLeftOffset': 1000},
           "title":{
             "text":"Categorization"
           },
           // 'legend': {
           //   'max-items': 10,
           //   "highlight-plot":true,
           //   'draggable': true
           // },
           "series":[
             {
               'values':[14806],
               'text': 'Healthcare/Achievement/Address'
             },
             {
               "values":[6974],
               'text': 'Power/Violence/Love'
             },
             {
               "values":[10688],
               'text': 'President/Leader/Community'
              },
             {
               "values":[5558],
               'text': 'Elections'
              },
             {
               "values":[5886],
               'text': 'Youth/Life'
              },
             {
               "values":[3527],
               'text': 'Climate/News'
             },
             {
               "values":[3624],
               'text': 'Women Empowerment/Nation/Job/Debate'
             },
             {
               "values":[6501],
               'text': 'Indian Politics'
              },
             {
               "values":[3768],
               'text': 'Economy/History'
              },
             {
               "values":[4393],
               'text': 'Campaign/Support/Gratitude'
             }
           ]
         }]
      };
     }
   }

 //   stateChange.$inject = ['$rootScope', '$state']
 //   function stateChange($rootScope, $state) {
 //     $rootScope.$on("$locationChangeStart", function(event, next, current) {
 //
 //     if(next==current && next=='/home')
 //       event.preventDefault();
 //       $state.go('search');
 //   })
 // }

  MainController.$inject = ['$state', 'DataService', 'ConfigService']
  function MainController($state, DataService, ConfigService) {
    var ctrl = this;
    ctrl.hide_search = false;
    ctrl.showQueryVisual = false;
    ctrl.showVisual = true;
    // console.log("hello");
    ctrl.search = function () {
      // console.log('clicked');
      if (!ctrl.search_string || ctrl.search_string.length == 0){
        $state.go('search', {}, {reload: true});
      } else {
        DataService.setParam(ctrl.search_string);
        ConfigService.setVisual(true);
        ctrl.showQueryVisual = true;
        ctrl.showVisual = false;
        $state.go('home', {}, {reload: true});
      }
    }
    ctrl.clicked = function () {
      // console.log('visual clicked');
      ctrl.showQueryVisual = false;
      ctrl.hide_search = true;
      ctrl.showVisual = false;
      DataService.setVisual(false);
    }
    ctrl.clearData = function () {
      ctrl.search_string = null;
      ctrl.hide_search = false;
      ctrl.showQueryVisual = false;
      ctrl.showVisual = true;
      DataService.setVisual(true);
    }

  }

  HomeController.$inject = ['searchData', '$http', '$interval', '$scope', 'DataService', '$state', 'APIService']
  function HomeController(searchData, $http, $interval, $scope, DataService, $state, APIService) {

    var home = this;
    var begin = 0;
    var end = 0;
    var positive = 0;
    var negative = 0;
    var topic;
    var category = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0};
    var search_string = DataService.getParam();
    if (!search_string || search_string.length == 0){
      home.show_str = false;
      // console.log(home.show_str);
      $state.go('search');
    } else {
      home.show_str = true;
    }
    home.count = 1;
    home.searchData = searchData.data;
    home.currentpage = 1;
    home.itemsperpage = 10;
    home.maxsize = 10;
    home.showPagination = true;
    home.showNoData = false;

    for (var data in home.searchData) {
      home.searchData[data].url = "https://twitter.com/" + home.searchData[data].name + "/status/" + home.searchData[data].id;
      home.searchData[data].open = false;
      if (home.searchData[data].tweet_sentiment == "positive") {
        positive += 1;
      }
      if (home.searchData[data].tweet_sentiment == "negative") {
        negative += 1;
      }

      topic = home.searchData[data].topic;
      category[topic[0]] += 1
    }
    home.actualData = home.searchData;
    // console.log(category);

    if (home.searchData && home.searchData.length > 0) {
      home.noofpages = home.searchData.length / home.itemsperpage;
      APIService.setSentimentData(positive, negative, home.searchData.length - positive - negative);
      APIService.setCategoryData(category);
    } else {
      home.noofpages = 0;
      home.showPagination = false;
      home.showNoData = true;
      home.show_str = false;
      APIService.setSentimentData(0, 0, 0);
      APIService.setCategoryData({});
    }

    $scope.$watch('home.currentpage', function () {
      begin = (home.currentpage - 1) * home.itemsperpage;
      end = begin + home.itemsperpage;

      home.paged = {results: home.searchData.slice(begin, end)}
      // console.log(home.paged.results);

    });

    home.clearCountryList = function () {
      home.selected.country = [];
      home.paged.results = [];
      home.searchData = home.actualData;
      home.currentpage = 1;
      begin = (home.currentpage - 1) * home.itemsperpage;
      end = begin + home.itemsperpage;

      home.paged = {results: home.searchData.slice(begin, end)}
    }

    home.clearLanguageList = function () {
      home.selected.language = [];
      home.paged.results = [];
      home.searchData = home.actualData;
      home.currentpage = 1;
      // console.log(home.searchData);
      begin = (home.currentpage - 1) * home.itemsperpage;
      end = begin + home.itemsperpage;

      home.paged = {results: home.searchData.slice(begin, end)}
    }

    home.applyCountryFilter = function () {
      var country_list = [];
      home.searchData = [];
      home.paged.results = [];
      for (var i in home.selected.country) {
        country_list.push(home.selected.country[i].name);
      }
      for (var i in home.actualData) {
        if (country_list.indexOf(home.actualData[i].country[0]) >= 0) {
          home.searchData.push(home.actualData[i]);
        }
      }
      // console.log(home.searchData);
      home.currentpage = 1;
      begin = (home.currentpage - 1) * home.itemsperpage;
      end = begin + home.itemsperpage;

      home.paged = {results: home.searchData.slice(begin, end)}

    }

    home.applyLanguageFilter = function () {
      var language_list = [];
      home.searchData = [];
      home.paged.results = [];
      // console.log(home.searchData);
      // console.log(home.actualData);
      // console.log(home.selected.language);
      for (var i in home.selected.language) {
        language_list.push(home.selected.language[i].value);
      }
      // console.log(language_list);
      for (var i in home.actualData) {
        if (language_list.indexOf(home.actualData[i].language) >= 0) {
          home.searchData.push(home.actualData[i]);
        }
      }
      // console.log(home.searchData);
      home.currentpage = 1;
      begin = (home.currentpage - 1) * home.itemsperpage;
      end = begin + home.itemsperpage;

      home.paged = {results: home.searchData.slice(begin, end)}
    }

    home.applyFilter = function () {
      var language_list = [];
      var country_list = [];
      home.searchData_lang = [];
      home.searchData_country = [];
      home.searchData_verified = [];
      home.paged.results = [];

      if (home.selected.language.length > 0) {
        for (var i in home.selected.language) {
          language_list.push(home.selected.language[i].value);
        }
        for (var i in home.actualData) {
          if (language_list.indexOf(home.actualData[i].language) >= 0) {
            home.searchData_lang.push(home.actualData[i]);
          }
        }
      }
      else{
        home.searchData_lang = home.actualData
      }
      console.log(home.searchData_lang);

      if (home.selected.country.length > 0) {
        for (var i in home.selected.country) {
          country_list.push(home.selected.country[i].name);
        }
        for (var i in home.searchData_lang) {
          if (country_list.indexOf(home.searchData_lang[i].country[0]) >= 0) {
            home.searchData_country.push(home.searchData_lang[i]);
          }
        }
      }
      else {
        home.searchData_country = home.searchData_lang
      }
      console.log(home.searchData_country);

      if (home.selected.verified.length > 0){
        for (var i in home.searchData_country) {
          if (home.searchData_country[i].verified) {
            home.searchData_verified.push(home.searchData_country[i]);
          }
        }
      }
      else {
        home.searchData_verified = home.searchData_country
      }
      console.log(home.searchData_verified);

      home.searchData = home.searchData_verified;
      home.currentpage = 1;
      begin = (home.currentpage - 1) * home.itemsperpage;
      end = begin + home.itemsperpage;

      home.paged = {results: home.searchData.slice(begin, end)}
    }

    home.clearFilter = function () {
      home.selected.language = [];
      home.selected.country = [];
      home.selected.verified = [];
      home.paged.results = [];
      home.searchData = home.actualData;
      home.currentpage = 1;
      // console.log(home.searchData);
      begin = (home.currentpage - 1) * home.itemsperpage;
      end = begin + home.itemsperpage;

      home.paged = {results: home.searchData.slice(begin, end)}
    }

    home.countrylist = [
         {name: 'India'},
         {name: 'USA'},
         {name: 'Brazil'}
    ];

    home.selected = {
        country: [],
        language: [],
        verified: []
    };
    home.languagelist = [
         {name: 'English', value:'en'},
         {name: 'Hindi', value:'hi'},
         {name: 'Portugese', value:'pt'}
    ];

  }

})();
