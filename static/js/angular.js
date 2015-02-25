var app = angular.module('LibraryApp', ['ngMaterial']);

app.controller('LibraryControl', function($scope, $timeout, $mdSidenav, $log) {
    $scope.toggleLeft = function() {
        $mdSidenav('left').toggle();
    };
});