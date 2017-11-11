'use strict';

// Register `toDoListDetail` component, along with its associated controller and template
angular.
  module('toDoListDetail').
  component('toDoListDetail', {
    templateUrl: 'app/to-do-list-detail/to-do-list-detail.template.html',
    controller: ['$routeParams', 'ToDoList',
      function ToDoListDetailController($routeParams, ToDoList) {
        var self = this;
        self.toDoList = ToDoList.get({toDoListId: $routeParams.toDoListId});
        this.orderProp = 'due_at';
      }
    ]
  });
