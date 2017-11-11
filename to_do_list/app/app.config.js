'use strict';

angular.
  module('toDoListApp').
  config(['$locationProvider', '$routeProvider', '$resourceProvider',
    function config($locationProvider, $routeProvider, $resourceProvider) {
      $locationProvider.hashPrefix('!');

      $routeProvider.
        when('/to-do-lists', {
          template: '<to-do-list-list></to-do-list-list>'
        }).
        when('/to-do-lists/:toDoListId', {
          template: '<to-do-list-detail></to-do-list-detail>'
        }).
        otherwise('/to-do-lists');
    }
  ]);
