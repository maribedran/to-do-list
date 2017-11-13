'use strict';

angular.
  module('toDoListApp').
  config([
    '$locationProvider',
    '$routeProvider',
    '$resourceProvider',
    '$httpProvider',
    function config($locationProvider, $routeProvider, $resourceProvider, $httpProvider) {
      $locationProvider.hashPrefix('!');

      $resourceProvider.defaults.stripTrailingSlashes = false;

      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

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
