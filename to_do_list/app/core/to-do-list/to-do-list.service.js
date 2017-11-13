'use strict';

angular.
  module('core.to-do-list').
  factory('ToDoList', ['$resource',
    function($resource) {
      return $resource('api/to_do_list/:toDoListId/', {}, {
        query: {
          method: 'GET',
          params: {},
          isArray: true
        },
        post: {
          method: 'POST',
          params: {},
          isArray: false
        }
      });
    }
  ]);
