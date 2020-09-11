$(document).ready(function(){
			
	$('#searchfield').autocomplete({
		source: "fetch",
		minLength: 1,
		select: function(event, ui){
			$('#searchfield').val(ui.item.value);
		}
	}).data('ui-autocomplete')._renderItem = function(ul, item){
		return $("<li class='ui-autocomplete-row'></li>")
				.data("item.autocomplete", item)
				.append(item.label)
				.appendTo(ul);
		};

});