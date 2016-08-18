angular.module('index').controller('indexCtrl', ['$scope','accountsApi', 'servicesApi',
	function($scope, accountsApi,servicesApi){	
		function requestToMe(){
			servicesApi.requestToMe().then(
				function successCallBack(response){
					$scope.requestsToMe =  {
						'userRequest' : response.data['requestToMe'],
						'quantityRequests': response.data['requestToMe'].length
					}
			})
		}
		function getFriends(){
			servicesApi.getFriends().then(function successCallBack(response){
				$scope.friends = response.data["friends"]
			})
		}				
		function checkLogged(){
			accountsApi.checkLogged().then(
				function successCallBack(response){
					$scope.logged = response.data['active'];
					$scope.username = response.data['username'];
					$scope.errorLogin = null;
					if ($scope.logged){
						requestToMe()
						getFriends()
					};
				}
			)
		}

		$scope.showHideRequests = function(){
			if ($scope.showRequests){
				$scope.showRequests = !$scope.showRequests
			}else{
				if ($scope.requestsToMe['quantityRequests'] > 0){
					$scope.showRequests = true
				}
			}
		}

		$scope.logar = function(username, password){
			accountsApi.logar(username, password).then(
				function successCallBack(response){
					checkLogged()
				}, function errorCallBack(response){
					$scope.errorLogin = response.data
				});
		}

		$scope.search = function(searchString){
			servicesApi.doSearch(searchString).then(function successCallBack(response){
				$scope.searchResults = response.data
			},function errorCallBack(response){
				console.log(response)
			}
		)}

		$scope.showHideResuts = function(option){
			$scope.showResults = option
		}

		checkLogged()
}])