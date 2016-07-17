angular.module('es-app')
    .controller('searchCtrl', searchCtrl);


/* Inject Dependencies */
searchCtrl.$inject = [
    '$scope', 'searchService'
];



function searchCtrl($scope, searchService)
{

	$scope.vale = null;
	$scope.search={};
	$scope.search.query='*';
	$scope.search.toggle=1;

	$scope.aggr={};
	$scope.val=90;
	$scope.array = [{ "value":   "5y", "text": "Last 5 years" }
				    , { "value": "2y", "text": "Last 2 years  " }
				    , { "value": "1y", "text": "This year" }
				    , { "value": "1M", "text": "This month" }
				    , { "value": "7d", "text": "This week" }
				    , { "value": "10d", "text": "Past 10 days" }];
	$scope.array1 = [
				    { "value": "sum", "text": "SUM" }
				    , { "value": "value_count", "text": "COUNT" }
				    , { "value": "avg", "text": "AVERAGE" },
				    { "value":   "terms", "text": "TERMS" }];
	$scope.searchData=searchData;
	$scope.aggrData=aggrData;
	$scope.uploadFile=uploadFile;
	$scope.reset=reset;
	$scope.resetAggr=resetAggr;
	$scope.exportData=exportData;


	toastr.options = {
	  "debug": false,
	  "positionClass": "toast-bottom-right",
	  "onclick": null,
	  "fadeIn": 300,
	  "fadeOut": 1000,
	  "timeOut": 5000,
	  "extendedTimeOut": 1000
	}

	toastr.options.closeButton = true;
	toastr.warning('Please upload your log file');


	$(document).ready(function(){
    $('#myTable').DataTable();
    searchData($scope.search);
		});


	
	function exportData(data){


		searchService.export_fn(data)
		.then(function(data)
		{
		
		var hiddenElement = document.createElement('a');

	    hiddenElement.href = 'data:text/csv;charset=UTF-8,' + encodeURI(data.data);
    	hiddenElement.target = '_blank';
    	hiddenElement.download = 'myFile.csv';
    	hiddenElement.click();
     	
			
			});
		
	}

	function searchData(data){
		
		searchService.search_fn(data)
		.then(function(data)
		{
			
		if($scope.search.toggle == 1){	
			key_list=[];
			doc_list=[];

			$scope.temp=data.data;
			
			if($scope.temp){
				toastr.info('Search performed on query');
			}
			else{
				toastr.warning('Please upload your log file');

			}
			hello=data.data;
			$scope.last=hello[hello.length - 1 ];
		
		
		
   
	for (x in $scope.last) 
			{
    			txt = JSON.stringify($scope.last[x].key_as_string);
    			txt=txt.replace(/['"]+/g, '');
    			txt1 = JSON.stringify($scope.last[x].doc_count);
    			key_list.push(txt1);
    			doc_list.push(txt);
			}

		
			var ctx = document.getElementById("myChart");
			var randomColorGenerator = function () { 
			    return '#' + (Math.random().toString(16) + '0000000').slice(2, 8); 
			};
			var myChart = new Chart(ctx, {
			    type: 'bar',
			    data :{
			    labels:  doc_list ,
			    datasets: [
			        { 
			            label: "Document count ",
			            fill: true,
			            lineTension: 0.1,
			            backgroundColor: "rgba(75,192,192,1)",
			            borderColor: "rgba(75,192,192,1)",
			            borderCapStyle: 'butt',
			            borderDash: [],
			            borderDashOffset: 0.0,
			            borderJoinStyle: 'miter',
			            
			            pointRadius: 1,
			            pointHitRadius: 10,
			            data: key_list,
			        }
			    ]
				},
				options:{
					title: {
         	   			display: true,
            			text: 'Search results'
       						 
				},
				tooltips:{
					mode: 'label',

				}
			}
			    
			});
			if(myChart)
		    {		
		            myChart.destroy();
		    }	
		}

		});


	}

	function reset(){

			$scope.temp={};
			doc_list=[];
			key_list=[];
			
		
	}

	function resetAggr(){

			$scope.temp2={};
			
		
	}

	function aggrData(data){

		searchService.aggr_fn(data)
		.then(function(data)
		{
			doc_list=[];
			key_list=[];
			
			$scope.temp2=data.data;
			var txt="";
			var txt1="";
			var x;
			
			for (x in $scope.temp2) 
			{
    			txt = JSON.stringify($scope.temp2[x].doc_count);
    			txt1 = JSON.stringify($scope.temp2[x].key);
    			key_list.push(txt);
    			doc_list.push(txt1);
			}
			
			$scope.doc=doc_list;
			$scope.key=key_list;

			console.log(key_list);
			var ctx = document.getElementById("myChart");
			var myChart = new Chart(ctx, {
			    type: 'bar',
			    data :{
			    labels:  doc_list ,
			    datasets: [
			        { 
			           
			            fill: false,
			            lineTension: 0.1,
			            backgroundColor: "rgba(75,192,192,1)",
			            borderColor: "rgba(75,192,192,1)",
			            borderCapStyle: 'butt',
			            borderDash: [],
			            borderDashOffset: 0.0,
			            borderJoinStyle: 'miter',
			            pointBorderColor: "rgba(75,192,192,1)",
			            pointBackgroundColor: "#fff",
			            pointBorderWidth: 1,
			            pointHoverRadius: 5,
			            pointHoverBackgroundColor: "rgba(75,192,192,1)",
			            pointHoverBorderColor: "rgba(220,220,220,1)",
			            pointHoverBorderWidth: 2,
			            pointRadius: 1,
			            pointHitRadius: 10,
			            data: key_list,
			        }
			    ]
			}

			    
			});
			if(myChart)
		    {		
		            myChart.destroy();
		    }

			console.log(key_list);
			console.log(doc_list);
		});

	}

function uploadFile(data){


	var file = $scope.myFile;        
   

	searchService.upload_fn(data)
	.then(function(data)
	{    
	
	toastr.info('File is uploaded');
	location.reload();

	});
	
}


}