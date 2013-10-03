$(function(){

	var app = new Object();

	$("#homebtn").click(function(){

		//alert("home");
		loadDocuments();

	});

	$("#btn-tokenize").click(function(){


		function loadTokenizedData(text){
			$("#tokenized-text-area").html("")
			$("#tokenized-text-area").html(text);
		}

		function failedTokenizedData(xhr){
			console.log(xhr);
		}


		$.ajax({
			type:"POST",
			url:"/tokenizeData",
			data:{"text":app.currentDocument},
			success:loadTokenizedData,
			failure:failedTokenizedData
		});
	});

	$("#btn-pos").click(function(){

		function loadPosTags(tags){
			$("#POS-text-area").html("");
			$("#POS-text-area").html(tags);
		}

			function failedPosTags(xhr){
			console.log(xhr);
		}

		$.ajax({
			type:"GET",
			url:"/postags",
			success:loadPosTags,
			failure:failedPosTags
		});

	});

	$("#btn-chunk").click(function(){

		function loadChunkedData(chunks){
			$("#chunked-text-area").html("");
			$("#chunked-text-area").html(chunks);
		}

		function failedChunking(xhr){
			console.log(xhr);
		}

		$.ajax({
			type:"GET",
			url:"/chunk",
			success:loadChunkedData,
			failure:failedChunking

		});

	});

	$("#btn-entity").click(function(){

		function loadEntities(entities){
			$("#entity-text-area").html("");
			$("#entity-text-area").html(entities);
		}

		function failedEntities(xhr){
			console.log(xhr);
		}

		$.ajax({
			type:"GET",
			url:"/entities",
			success:loadEntities,
			failure:failedEntities

		});

	});




	$(document.body).on('click','.document-name' , function(event){
		
		loadDocument(event.target.text);
		app.currentDocument = event.target.text;

	});


	function loadDocument(document) {

		function loadDocumentSuccess(text){
			$("#plain-text-area").html("");
			$("#plain-text-area").html(text);
		}

		function loadDocumentFailure(){
			$("#Documents li.active").removeClass("active");
		}

		$.ajax({
			type:"GET",
			url:"/getContent/"+document,
			dataType:"text",
			success:loadDocumentSuccess,
			failure:loadDocumentFailure
		});		

	}

	function loadDocuments(){

		function loadDocumentsSuccess(json){
			$("#plain-text-area").html("");
			$("#tokenized-text-area").html("");
			$("#POS-text-area").html("");
			$("chunked-text-area").html("");
			$("entity-text-area").html("");

			$.each(json.data,function(key,value){
				$("#dropdown-area").append("<li><a class=document-name>"+value.name+"</a></li>");
			});		
		}

		$.ajax({
			type:"GET",
			url:"/loadFileNames",
			dataType:"json",
			success:loadDocumentsSuccess
		});

	}

	loadDocuments();

});