var app = angular.module('LibraryApp', ['ngMaterial']);

app.controller('LibraryControl', function($scope, $timeout, $mdSidenav, $mdToast) {
    $scope.openLeft = function() {
        $mdSidenav('left').open();
    };

    $scope.closeLeft = function() {

        $mdSidenav('left').close();
    };

    $scope.showToast = function() {
        $mdToast.show(
            $mdToast.simple()
                .content('NOTICE - Under Development!')
                .action('OK')
                .hideDelay(0)
        );
    };
});