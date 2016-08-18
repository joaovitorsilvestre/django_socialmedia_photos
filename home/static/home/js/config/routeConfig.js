angular.module('index').config(['$routeProvider',function($routeProvider) {
	$routeProvider.when("/own", {
		templateUrl: "/home/ownpage",
		controller:"ownPageCtrl"
	})

	$routeProvider.when("/userpage/:name",{
		templateUrl: "/home/userpage",
		controller: "userPageCtrl"
	})

	$routeProvider.otherwise({redirectTo:"/own"})
}])