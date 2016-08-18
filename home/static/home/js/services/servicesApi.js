angular.module('index').service('servicesApi', ['$http', function($http){
	this.doSearch = function(searchString){
		return (
			$http({
				url:'/services/search/'.concat(searchString),
				method:'GET'
			})
		)	
	}
	this.isFriend = function(user){
		return (
			$http({
				url:'/services/isfriend/'.concat(user),
				method:'GET'
			})
		) 
	}
	this.requestFriend = function(user){
		return (
			$http({
				url:'/services/requestfriend/'.concat(user),
				method:'GET'
			})
		) 
	}
	this.requestToMe = function(){
		return (
			$http({
				url:'/services/requesttome/',
				method:'GET'
			})
		) 
	}
	this.getSelfImages = function(){
		return (
			$http({
				url:'/services/getselfimages/',
				method:'GET'
			})
		) 
	}
	this.getFriends = function(){
		return(
			$http({
				url:'/services/getfriends/',
				method: 'GET'
			})
		)
	}
}])