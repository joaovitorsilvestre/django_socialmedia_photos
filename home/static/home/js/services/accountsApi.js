angular.module('index').service('accountsApi', ['$http', '$httpParamSerializerJQLike',
	function($http, $httpParamSerializerJQLike){
		this.logar = function(username,password){
			var data = $httpParamSerializerJQLike({
				username: username,
				password: password
			})
			return (
				$http({
					url:'/accounts/login_ajax/',
					method:'POST',
					data: data,
					headers: {'Content-Type': 'application/x-www-form-urlencoded'},	
				})
			)	
		}
		this.checkLogged = function(){
			return(
				$http({
					url:'/accounts/login_ajax/',
					method: 'GET',
				})
			)
		}
	}
])