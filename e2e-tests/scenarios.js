'use strict';

// Angular E2E Testing Guide:
// https://docs.angularjs.org/guide/e2e-testing

describe('ToDoList Application', function() {

  it('should redirect `index.html` to `index.html#!/to-do-lists', function() {
    browser.get('index.html');
    expect(browser.getLocationAbsUrl()).toBe('/to-do-lists');
  });

  describe('View: ToDoList list', function() {

    beforeEach(function() {
      browser.get('index.html#!/to-do-lists');
    });

    it('should filter the toDoList list as a user types into the search box', function() {
      var toDoListList = element.all(by.repeater('toDoList in $ctrl.to-do-lists'));
      var query = element(by.model('$ctrl.query'));

      expect(toDoListList.count()).toBe(20);

      query.sendKeys('nexus');
      expect(toDoListList.count()).toBe(1);

      query.clear();
      query.sendKeys('motorola');
      expect(toDoListList.count()).toBe(8);
    });

    it('should be possible to control toDoList order via the drop-down menu', function() {
      var queryField = element(by.model('$ctrl.query'));
      var orderSelect = element(by.model('$ctrl.orderProp'));
      var nameOption = orderSelect.element(by.css('option[value="name"]'));
      var toDoListNameColumn = element.all(by.repeater('toDoList in $ctrl.to-do-lists').column('toDoList.name'));

      function getNames() {
        return toDoListNameColumn.map(function(elem) {
          return elem.getText();
        });
      }

      queryField.sendKeys('tablet');   // Let's narrow the dataset to make the assertions shorter

      expect(getNames()).toEqual([
        'Motorola XOOM\u2122 with Wi-Fi',
        'MOTOROLA XOOM\u2122'
      ]);

      nameOption.click();

      expect(getNames()).toEqual([
        'MOTOROLA XOOM\u2122',
        'Motorola XOOM\u2122 with Wi-Fi'
      ]);
    });

    it('should render toDoList specific links', function() {
      var query = element(by.model('$ctrl.query'));
      query.sendKeys('nexus');

      element.all(by.css('.to-do-lists li a')).first().click();
      expect(browser.getLocationAbsUrl()).toBe('/to-do-lists/nexus-s');
    });

  });

  describe('View: ToDoList detail', function() {

    beforeEach(function() {
      browser.get('index.html#!/to-do-lists/1');
    });

    it('should display the to-do list 1 page', function() {
      expect(element(by.binding('$ctrl.toDoList.name')).getText()).toBe('Nexus S');
    });

  });

});
