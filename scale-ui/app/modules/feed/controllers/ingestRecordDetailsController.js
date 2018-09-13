(function () {
    'use strict';

    angular.module('scaleApp').controller('ingestRecordDetailsController', function ($scope, $routeParams, scaleConfig, scaleService, navService, subnavService, feedService) {
        var vm = this;

        vm.loading = false;
        vm.subnavLinks = scaleConfig.subnavLinks.feed;
        vm.scaleService = scaleService;
        vm.moment = moment;
        vm.ingestRecord = null;

        var getIngestRecordDetails = function () {
            vm.loading = true;
            feedService.getIngestDetails($routeParams.id).then(function (data) {
                vm.ingestRecord = data;
                feedService.getSourceDetails(vm.ingestRecord.source_file.id).then(function (sourceData) {
                    vm.ingestRecord.products = sourceData.products;
                });
            }).catch(function (error) {
                console.log(error);
            }).finally(function () {
                vm.loading = false;
            });
        };

        var initialize = function () {
            navService.updateLocation('feed');
            subnavService.setCurrentPath('feed/ingests');
            getIngestRecordDetails();
        };

        vm.calculateFileSize = function (size) {
            return scaleService.calculateFileSizeFromBytes(size);
        };

        initialize();
    });
})();
