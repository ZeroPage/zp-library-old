var app = angular.module('LibraryApp', ['ngMaterial']);

app.controller('LibraryControl', function($scope, $timeout, $mdSidenav, $mdToast) {
    $scope.openLeft = function() {
        $mdSidenav('left').open();
    };

    $scope.closeLeft = function() {

        $mdSidenav('left').close();
    };

    $scope.showToast = function(message) {
        $mdToast.show(
            $mdToast.simple()
                .content(message)
                .action('OK')
                .hideDelay(6000)
                .position('bottom right')
        );
    };
});