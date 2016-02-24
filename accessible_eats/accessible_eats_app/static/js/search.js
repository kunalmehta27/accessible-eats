var placeSearch, autocomplete;

function initAutocomplete() {
	console.log('initAutocomplete')
  	autocomplete = new google.maps.places.Autocomplete(
      	(document.getElementById('filter-geography')),
      	{types: ['geocode']});
  	autocomplete.addListener('place_changed', setCoordinates);
}

function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      var circle = new google.maps.Circle({
        center: geolocation,
        radius: position.coords.accuracy
      });
      autocomplete.setBounds(circle.getBounds());
    });
  }
}

function setCoordinates() {
  var place = autocomplete.getPlace();
  var lat = place.geometry.location.lat()
  var lng = place.geometry.location.lng()
  $("#geo-lat").html(lat)
  $("#geo-lng").html(lng)
  reload_data()
}


function reload_data() {
	page_num = $("#page-num").html()
	if($("#mini-searchbar").height() > 0) {
		lat = 0
		lng = 0
		category = 0
		for(field in filter_values) {
			filter_values[field] = false
		}
		filter_string = encodeURIComponent(JSON.stringify(filter_values))
		if($(".search-by").html() == 'Name') {
			name = $("#small-search-val").val()
			name = encodeURIComponent(name)
		}
		else {
			name = ''
		}
		if(name == '') {
			name = 0
		}
		if($(".search-by").html() == 'Location') {
			location_name = $("#small-search-val").val()
			location_name = encodeURIComponent(location_name)
		}
		else {
			location_name = ''
		}
		if(location_name == '') {
			location_name = 0
		}
		yelp_rating = 0
		ae_rating = 0
	}
	else {
		name = $("#filter-name").typeahead('val')
		category = $("#filter-category").typeahead('val')
		yelp_rating = $("#filter-yelp").val()
		ae_rating = $("#filter-ae").val()
		lat = $("#geo-lat").html()
		lng = $("#geo-lng").html()
		if(lat == '') {
			lat = 0
		}
		if(lng == '') {
			lng = 0
		}

		for(field in filter_values) {
			if($("#" + field).parent().hasClass('active')) {
				filter_values[field] = true
			}
			else {
				filter_values[field] = false
			}
		}

		filter_string = encodeURIComponent(JSON.stringify(filter_values))

		if(name == '') {
			name = 0
		}
		name = encodeURIComponent(name)

		if(category == '') {
			category = 0
		}
		category = encodeURIComponent(category)

		if(yelp_rating == '') {
			yelp_rating = 0
		}

		if(ae_rating == '') {
			ae_rating = 0
		}

		location_name = 0
	}

	console.log(location_name)
	url = "/searchresults/" + page_num + '/' + name + '/' + category + '/' + yelp_rating + '/' + ae_rating + '/' + filter_string + '/' + lat + '/' + lng + '/' + location_name + '/'
	$("#results").load(url, function() {
		$("#page-num").html($("#results_page_num").html())
		$("#num-pages").html($("#results_num_pages").html())
	})
}

filter_values = {}

filter_fields = JSON.parse($("#filter-fields").html())
for(key in filter_fields) {
	filter_values[key] = false
}

$("#previous-page").click(function() {
	page_num = $("#page-num").html()
	new_page_num = Math.max(1, parseInt(page_num) - 1)
	$("#page-num").html(new_page_num)
	if(page_num != new_page_num) {
		reload_data()
	}
})

$("#next-page").click(function() {
	num_pages = parseInt($("#num-pages").html())
	page_num = $("#page-num").html()
	new_page_num = Math.min(num_pages, parseInt(page_num) + 1)
	$("#page-num").html(new_page_num)
	if(page_num != new_page_num) {
		reload_data()
	}
})

function showMore(app_id) {
	$("#extended" + app_id).show()
	$("#showmore" + app_id).hide()
	$("#showless" + app_id).show()
}

function showLess(app_id) {
	$("#extended" + app_id).hide()
	$("#showmore" + app_id).show()
	$("#showless" + app_id).hide()
}

function expand(review_id) {
	if($("#review" + review_id).hasClass('limitHeight')) {
		$("#review" + review_id).removeClass('limitHeight')
	}
	else {
		$("#review" + review_id).addClass('limitHeight')
	}
}

$("#search-button").click(function() {
	reload_data()
})

$(".clear-name").click(function() {
	$("#filter-name").typeahead('val', '')
	reload_data()
})

var restaurants = JSON.parse($("#restaurants-vals").html())

var restaurants = new Bloodhound({
	datumTokenizer: Bloodhound.tokenizers.whitespace,
	queryTokenizer: Bloodhound.tokenizers.whitespace,
	local: restaurants,
});

$("#filter-name").typeahead({
	hint: true,
	highlight: true,
	minLength: 1
},
{
	name: 'restaurants',
	source: restaurants,
})

$("#filter-name").bind('typeahead:select', function(ev, suggestion) {
	reload_data()
})

$(".clear-category").click(function() {
	$("#filter-category").typeahead('val', '')
	reload_data()
})

var categories = JSON.parse($("#categories-vals").html())

var categories = new Bloodhound({
	datumTokenizer: Bloodhound.tokenizers.whitespace,
	queryTokenizer: Bloodhound.tokenizers.whitespace,
	local: categories,
});

$("#filter-category").typeahead({
	hint: true,
	highlight: true,
	minLength: 1
},
{
	name: 'categories',
	source: categories,
})

$("#filter-category").bind('typeahead:select', function(ev, suggestion) {
	reload_data()
})

$("#filter-yelp").select2({
	placeholder:'Yelp rating higher than...',
	allowClear: true,
	minimumResultsForSearch: Infinity,
})

$("#filter-yelp").on("change", function(e) {
	reload_data()
})

$("#filter-ae").select2({
	placeholder:'Accessibility higher than...',
	allowClear: true,
	minimumResultsForSearch: Infinity,
})

$("#filter-ae").on("change", function(e) {
	reload_data()
})

$(".nav-stacked>li>a").click(function() {
	li = $(this).parent()
	if(li.hasClass('active')) {
		li.removeClass('active')
	}
	else {
		li.addClass('active')
	}
	reload_data()
})

$(".clear-geography").click(function() {
	$("#filter-geography").val('')
	$("#geo-lat").html('')
	$("#geo-lng").html('')
	reload_data()
})

$("#small-search").click(function() {
	reload_data()
})

$("#small-clear").click(function() {
	$("#small-search-val").val('')
	reload_data()
})

$("#search-by-menu li a").click(function() {
	val = $(this).html()
	$(".search-by").html(val)
})

reload_data()