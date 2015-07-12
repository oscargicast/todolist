/*
 Copyright 2011 The Go Authors.  All rights reserved.
 Use of this source code is governed by a BSD-style
 license that can be found in the LICENSE file.
*/

function TaskCtrl($scope, $http) {
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
}
