$(function(){

	$("#homebtn").click(function(){

		alert("home");
		loadDocuments();

	});

	$(document.body).on('click','.document',function(){

		loadDocument($(this).text());

	});

	function loadDocument(document) {

		function loadDocumentSuccess(text){

			$("#Documents li.active").removeClass("active");
			$(this).parent().addClass("active");

			$("#Content").html("");
			$("#Content").html(text);

		}

		$.ajax({
			type:"GET",
			url:"/getContent/"+document,
			dataType:"text",
			success:loadDocumentSuccess
		});		

	}

	function loadDocuments(){

		function loadDocumentsSuccess(json){
			$("#Documents").html("");
			$("#Content").html("");

			$.each(json.data,function(key,value){
				$("#Documents").append("<li><a class='document' href='#'>"+value.name+"</a></li>")
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