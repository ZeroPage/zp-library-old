var app = angular.module('LibraryApp', ['ngMaterial']).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

app.controller('LibraryControl', function($scope, $timeout, $mdSidenav, $mdToast, $window, $mdBottomSheet, messageService) {
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
                .hideDelay(0)
                .position('bottom right')
        );
    };

    $scope.addMessage = function(type, message) {
        messageService.addMessage(type, message);
    };

    $scope.openBottomSheet = function() {
        $mdBottomSheet.show({
            templateUrl: '/static/html/bottom-sheet-list-template.html',
            controller: 'MessageControl'
        });
    };

    $scope.toURL = function(url) {
        $scope.closeLeft();
        $window.location.href = url;
    }
}).controller('MessageControl', function($scope, messageService) {
    $scope.messages = messageService.getMessages();
}).service('messageService', function() {
    var messages = [];

    var addMessage = function(type, message) {
        messages.push({type: type, message: message});
    };

    var getMessages = function() {
        return messages;
    };

    return {
        addMessage: addMessage,
        getMessages: getMessages
    }
});