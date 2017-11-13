'use strict';

// Register `toDoListList` component, along with its associated controller and template
angular.
  module('toDoListList').
  component('toDoListList', {
    templateUrl: 'app/to-do-list-list/to-do-list-list.template.html',
    controller: ['ToDoList', '$scope',
      function ToDoListListController(ToDoList, $scope) {
        this.orderProp = 'earlyest_task';

        this.updateList = function () {
          this.toDoLists = ToDoList.query({});
        }

        // Create To-Do List
        this.newList = {
          tasks: []
        };

        this.addTask = function() {
          this.newList.tasks.push({
            description: null,
            due_at: null
          })
        }

        this.create = function () {
          ToDoList.post(this.newList).$promise
          .then(function(response){
            $scope.createFormColapsed = true;
            createAlert('success', 'To-Do List successfuly created!');
            this.updateList();
            setTimeout(this.closeAlert.bind(this), 1000);
          }.bind(this))
          .catch(function(reason) {
            createAlert('danger', formatErrorMsg(reason.data))
          }.bind(this))
        }

        // Feedback
        function createAlert(type, msg) {
          $scope.alerts.push({type: type, msg: msg})
        }

        function formatErrorMsg(msg) {
          var messages = [];
          angular.forEach(msg, function(value, key){
            key = key.charAt(0).toUpperCase() + key.slice(1)
            var formatedValue = [];
            angular.forEach(value, function(item) {
              var val = angular.isString(item) ? item : formatErrorMsg(item);
              formatedValue.push(val);
            })
            messages.push([key, formatedValue.join('. ')].join(': '))
          })
          return messages.join(' ')
        }

        // Load Page
        this.updateList();

        // ui-bootstrap

        // Alerts
        $scope.alerts = [];
        $scope.closeAlert = function(index) {
          $scope.alerts.splice(index, 1);
        };

        // Datepicker
        $scope.datepickers = [];
        $scope.openDatepicker = function(index) {
          var datepicker = $scope.datepickers[index] || {open: false};
          datepicker.open = true
          $scope.datepickers[index] = datepicker;
        }

        // Collapse
        $scope.createFormColapsed = true;

    }]});
