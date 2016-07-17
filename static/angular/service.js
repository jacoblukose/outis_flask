angular.module('es-app')
    .factory('searchService', searchService);

searchService.$inject = ["$http"]


function searchService($http){
	return {
		search_fn : search_fn,
		aggr_fn   : aggr_fn,
		upload_fn : upload_fn,
    export_fn:export_fn
	};


	function search_fn(dataval){
	
		return $http({
   			url: "http://localhost:5000/api/v1/data/search",
   	 		method: "POST",
   	 		headers: { 'Content-Type': 'application/json' },
    		data: dataval

    		});
		
	}

	function aggr_fn(dataval){
	
		return $http({
   			url: "http://localhost:5000/api/v1/data/estimate",
   	 		method: "POST",
   	 		headers: { 'Content-Type': 'application/json' },
    		data: dataval

    		});
	}


	
	function upload_fn(file){
              var fd = new FormData();
              fd.append('file', file);
              return $http.post("http://localhost:5000/api/v1/data/upload", fd, {
                  transformRequest: angular.identity,
                  headers: {'Content-Type': undefined}
               });
            
        
            }

  function export_fn(dataval){
    return $http({
        url: "http://localhost:5000/api/v1/data/export",
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        data: dataval

        });

  }


}

