(function () {
  'use strict';

  angular
  .module('search.app')
  .config(RoutesConfig)

  RoutesConfig.$inject = ['$stateProvider', '$urlRouterProvider']

  function RoutesConfig($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/');

    $stateProvider
    .state('home', {
      url: '/home',
      templateUrl: 'static/src/templates/home.html',
      // templateUrl: 'home.html',
      controller: 'HomeController as home',
      resolve: {
        searchData: ['DataService', function (DataService) {
          return DataService.getData();
        }]
      }
    })
    .state('visualization', {
      url: '/visualization',
      templateUrl: 'static/src/templates/visual.html',
      controller: 'VisualController as visual',
    })
    .state('queryanalysis', {
      url: '/queryanalysis',
      templateUrl: 'static/src/templates/qanalysis.html',
      controller: 'QueryController as qctrl',
    })
    .state('search', {
      url: '/',
      // templateUrl: 'static/src/templates/search.html',
      controller: 'MainController as ctrl',
    });

  }

})();
