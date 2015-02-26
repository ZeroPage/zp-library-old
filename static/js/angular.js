var app = angular.module('LibraryApp', ['ngMaterial']);

app.controller('LibraryControl', function($scope, $timeout, $mdSidenav, $mdToast) {
    $scope.toggleLeft = function() {
        $mdSidenav('left').toggle();
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