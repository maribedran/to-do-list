'use strict';

describe('ToDoList', function() {
  var $httpBackend;
  var ToDoList;
  var toDoListsData = [
    {name: 'ToDoList X'},
    {name: 'ToDoList Y'},
    {name: 'ToDoList Z'}
  ];

  // Add a custom equality tester before each test
  beforeEach(function() {
    jasmine.addCustomEqualityTester(angular.equals);
  });

  // Load the module that contains the `ToDoList` service before each test
  beforeEach(module('core.to-do-list'));

  // Instantiate the service and "train" `$httpBackend` before each test
  beforeEach(inject(function(_$httpBackend_, _ToDoList_) {
    $httpBackend = _$httpBackend_;
    $httpBackend.expectGET('api/to_do_list').respond(toDoListsData);

    ToDoList = _ToDoList_;
  }));

  // Verify that there are no outstanding expectations or requests after each test
  afterEach(function () {
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  it('should fetch the toDoLists data from `api/to_do_list`', function() {
    var toDoLists = ToDoList.query();

    expect(toDoLists).toEqual([]);

    $httpBackend.flush();
    expect(toDoLists).toEqual(toDoListsData);
  });

});
