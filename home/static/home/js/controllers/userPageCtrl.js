angular.module('index').controller('userPageCtrl', ['$scope','$routeParams', 'servicesApi',
	function($scope,$routeParams, servicesApi){

		$scope.ownerPage = $routeParams.name

		servicesApi.isFriend($scope.ownerPage).then(function successCallBack(response){
			$scope.isFriend = response.data.isFriend
		})

		$scope.requestFriend = function(user){
			servicesApi.requestFriend(user).then(function successCallBack(response){
				console.log(response.data)
			})
		}
	}
])