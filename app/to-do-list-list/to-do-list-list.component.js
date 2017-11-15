'use strict';

// Register `toDoListList` component, along with its associated controller and template
angular.
  module('toDoListList').
  component('toDoListList', {
    templateUrl: 'app/to-do-list-list/to-do-list-list.template.html',
    controller: ['ToDoList', '$scope',
      function ToDoListListController(ToDoList, $scope) {
        self = this;
        self.orderProp = 'earlyest_task';

        // Load Page
        updateList();
        setEmptyList();

        // Resource service
        function updateList () {
          self.toDoLists = ToDoList.query({});
        }

        // Create To-Do List
        function setEmptyList () {
          self.newList = {
            tasks: []
          };
        }

        self.addTask = function() {
          self.newList.tasks.push({
            description: null,
            due_at: null
          })
        }

        self.create = function () {
          ToDoList.post(self.newList).$promise
          .then(function(response){
            $scope.createFormColapsed = true;
            createAlert('success', 'To-Do List successfuly created!');
            setTimeout(self.closeAlert, 1000);
            updateList();
            setEmptyList();
          })
          .catch(function(reason) {
            createAlert('danger', formatErrorMsg(reason.data))
          })
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
