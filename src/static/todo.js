var app = angular.module('myapp', []).config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

app.controller('TaskCtrl', function($scope, $http) {
  $scope.tasks = [];
  $scope.working = false;

  var logError = function(data, status) {
    console.log('code ' + status + ': ' + data);
    $scope.working = false;
  };

  var refresh = function() {
    return $http.get('/task/').
    success(function(data) {
      $scope.tasks = data.Tasks;
    }).
    error(logError);
  };

  $scope.addTodo = function() {
    $scope.working = true;
    $http({
      url: '/task/',
      method: 'POST',
      data: "Title=" + $scope.todoText,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }).
    error(logError).
    success(function() {
      refresh().then(function() {
        $scope.working = false;
        $scope.todoText = '';
      })
    });
  };

  $scope.removeTodo = function(task) {
    data = {
      ID: task._id["$oid"],
    }
    $http.delete('/task/' + task._id["$oid"] + '/').
    error(logError).
    success(function() {
      refresh()
    });
  };

  $scope.toggleDone = function(task) {
    data = {
      ID: task._id["$oid"],
      Title: task.Title,
      Done: !task.Done
    }
    $http.put('/task/' + task._id["$oid"] + '/', data).
    error(logError).
    success(function() {
      task.Done = !task.Done
    });
  };

  refresh().then(function() {
    $scope.working = false;
  });
});
