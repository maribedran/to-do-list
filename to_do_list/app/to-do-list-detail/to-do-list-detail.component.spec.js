'use strict';

describe('toDoListDetail', function() {

  // Load the module that contains the `toDoListDetail` component before each test
  beforeEach(module('toDoListDetail'));

  // Test the controller
  describe('ToDoListDetailController', function() {
    var $httpBackend, ctrl;
    var xyzToDoListData = {
      id: 1,
      name: 'toDoList xyz',
      tasks: [{'description': 'Do xyz'}]
    };

    beforeEach(inject(function($componentController, _$httpBackend_, $routeParams) {
      $httpBackend = _$httpBackend_;
      $httpBackend.expectGET('api/to_do_list/1').respond(xyzToDoListData);

      $routeParams.toDoListId = '1';

      ctrl = $componentController('toDoListDetail');
    }));

    it('should fetch the toDoList details', function() {
      jasmine.addCustomEqualityTester(angular.equals);

      expect(ctrl.toDoList).toEqual({});

      $httpBackend.flush();
      expect(ctrl.toDoList).toEqual(xyzToDoListData);
    });

  });

});
