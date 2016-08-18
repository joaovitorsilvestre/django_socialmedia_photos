angular.module('index').controller('ownPageCtrl', ['$scope', 'servicesApi',
	function($scope, servicesApi){
		function getSelfImages(){
			servicesApi.getSelfImages().then(function successCallBack(response){
				$scope.selfImages = response.data
			})
		}

		getSelfImages()
	}
])