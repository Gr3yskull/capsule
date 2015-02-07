// Credits: http://stackoverflow.com/questions/68485/how-to-show-loading-spinner-in-jquery
// Last Accessed: 2-Mar-2013
$(document).ajaxStart(function() {
	$('#progress-nav').show();
}).ajaxStop(function() {
	$('#progress-nav').hide();
});

function State() {
	this.total_pages  = 0;
	this.total_records  = 0;
	this.current_page = 0; // last fetched
	this.initial_run  = true;
	this.total_records_in_last_fetched = 0;

	this.request = {'kind': 'H'}
	this.base = 'highlights';
	this.url_slice = 'page'

	this.fetchRequired = function () {
		if (this.initial_run)
			this.current_page = 0;
		// Account for zero based index and return if all pages are fetched
		return (this.total_pages > (this.current_page - 1));
	};
	
	this.resetState = function() {
		this.initial_run = true;
	};
	this.kind = function(kind) {
		this.request['kind'] = kind
	};
}

function fetchState(state) {
	if(state.fetchRequired()) {
		requestServce("/api/notes/"+state.url_slice+"/"+state.current_page+"/", state.request, function (response){
			state.total_pages = response['total_pages'];
			state.total_records = response['total_records'];
			state.total_records_in_last_fetched = response['total_records_this'];
			addTableRows(response['rolls'], state.base);
			
			// Correct bug and trace when each needs to be triggered.
			refreshResultStatus('highlights');
			refreshResultStatus('stackups');
			refreshResultStatus('images');
			refreshResultStatus('search');
		});
		state.current_page += 1;
		state.initial_run = false;
	}
}

h_state = new State();
h_state.kind('H');
h_state.base = 'highlights';

s_state = new State(); // Stackups
s_state.kind('S');
s_state.base = 'stackups';

i_state = new State(); // Images
i_state.kind('I');
i_state.base = 'images';

search_state = new State(); // Search
search_state.kind = '';
search_state.base = 'search';
search_state.url_slice = 'search';

function Tags() {
	this.initial_run = true;

	this.resetState = function() {
		this.initial_run = true;
	};
}

function fetchTags(tags) {
	if (tags.initial_run) {
		$.get('/api/notes/tags_frequency', '', function(response) {
			if (response['success']) {
				tags.search_term = true;
				tags.total_tags = response['total_tags'];
				tags.items = response['tags'];
				addTagsToCloud(tags);
		} else
			tags.success = false;
		});
		tags.initial_run = false;
	};
}

tags = new Tags();
function addTagsToCloud(tags) {
	for (var i = 0; i < tags.total_tags; i++) {
		var $tag = getTagFrequencyTemplate();
		$tag.find('#tag_name').text(tags.items[i]['tag']);
		$tag.find('#tag_frequency').text(tags.items[i]['frequency']);
		$tag.appendTo('#tag-cloud');
		$('#tag-cloud').append(' ');
	};
}

function tagClick($this, event) {
	var search_term = $($this).find('#tag_name').text();
	$('#search-text').val(search_term);
	$('#search-text-btn').click();
	$('#close-tag-cloud-modal').click();
}

function validateChangePasswordForm() {
	var $form = $('#change-password-form');
	var uname = document.forms["change-password-form"]["username"].value;
	var pwd = $form.find("input[name=password]").val();
	var new_pwd = document.forms["change-password-form"]["new_password"].value;
	var confirm_pwd = document.forms["change-password-form"]["new_password_confirm"].value;

	if (new_pwd.length < 6) {
		$form.markErrors(dummyResponseForPasswordLength());
		return false;
	};

	if (pwd == new_pwd) {
		$form.markErrors(dummyResponseForPasswordSameAsOld());
		return false;
	};

	if (uname == new_pwd) {
		$form.markErrors(dummyResponseForUsernameInvalidSameAsPassword());
		return false;
	};

	if (new_pwd != confirm_pwd) {
		$form.markErrors(dummyResponseForPasswordsDontMatch());
		return false;
	};

	return true;
}

function validateChangeUsernameForm() {
	var $form = $('#change-username-form');
	var uname = document.forms["change-username-form"]["username"].value;
	var pwd = $form.find("#password").val();
	var new_uname = document.forms["change-username-form"]["new_username"].value;

	if (pwd.length < 6) {
		$form.markErrors(dummyResponseForPasswordLength());
		return false;
	};

	if (new_uname.length < 4 ) {
		$form.markErrors(dummyResponseForUsernameInvalid());
		return false;
	};

	if (uname == new_uname) {
		$form.markErrors(dummyResponseForUsernameSameAsOld());
		return false;
	};
	
	return true;
}

$(document).ready(function() {
	$('#progress-nav').hide();
	window.onhashchange = hashBind;
	// Cope for any changes
	hashBind();
	// Fade In body effect
	// $("body").css("display", "none");
	// $("body").fadeIn(2000);
	
	$("#change-username-form").submit(function(e) {
		e.preventDefault();
		var data = $(this).serializeObject();

		$('#change-username-form').removeErrors();
		if(validateChangeUsernameForm()) {
			requestServce("/api/user/modify/", data, function(response){
				if(response['success']) {
					location.reload();
				} else {
					$("#change-username-form").markErrors(response);
				}
			});
		}
	});
	$("#change-password-form").submit(function(e) {
		e.preventDefault();
		var data = $(this).serializeObject();
		
		// var dummy_response = dummyResponseForPasswordsDontMatch();
		// if (!validateConfirmPassword($("#change-password-form"))) {
		// 	$('#change-password-form').markErrors(dummy_response);
		// 	return false;
		// }
		$('#change-password-form').removeErrors()
		if(validateChangePasswordForm()) {
			requestServce("/api/user/modify/", data, function(response){
				if(response['success']) {
					location.reload();
				} else {
					$("#change-password-form").markErrors(response);
				}
			});
		}
	});

	console.log("Fetching notes (initial bunch)");
	fetchState(h_state);
	fetchState(s_state);
	fetchState(i_state);
	fetchTags(tags);

	// For Infinite Scroll
	// Credits: http://stackoverflow.com/questions/5059526/infinite-scroll-jquery-plugin
	// Last Access: 6-Apr-2013
	$(window).scroll(function () { 
		if ($(window).scrollTop() >= $(document).height() - $(window).height() - 10) {
			switch(getActiveId()) {
				case "highlights":
					fetchState(h_state);
					break;
				case "stackups":
					fetchState(s_state);
					break;
				case "images":
					fetchState(i_state);
					break;
				case "search":
					searchForResults();
					break;
			}
		}
	});

	// Fancy Search
	$('#search-text').focus(function() {
		$(this).animate({
			width: '+=110'
		}, 'fast')
	}).blur(function() {
		$(this).animate({
			width: '-=110'
		}, 'fast')
	});
	// Minimalistic view
	// var brand_active = false;
	// var brand_width = $('#navigation').width();
	// // var brand_left = $('#navigation').css('left');
	// $('#brand').click(function() {
	// 	console.log("Branding clicked...");
		
	// 	var move = brand_width + 40;
	// 	if (brand_active) { // brand is active
	// 		$('#navigation').animate({
	// 				left: 20
	// 			}, 'fast');
	// 		$('#app-main-screen').animate({
	// 				left: 20
	// 			}, 'fast');
	// 		brand_active = !brand_active;
	// 	} else {
	// 		$('#navigation').animate({
	// 				left: -move
	// 				// width: 'toggle'
	// 			}, 'fast');
	// 		brand_active = !brand_active;
	// 	}
	// });
});

function search() {
	// Remove all content for a new search
	$('#search-content').children().remove();
	document.location.hash = '/search/';
	search_state.resetState();

	var search_term = document.getElementById('search-text').value;
	search_state.request['search'] = search_term;

	searchForResults();
}

function searchForResults() {
	if (search_state.request['search']) {
		fetchState(search_state);
	}
}

function addTableRows(rolls, where) {
	refreshResultStatus(where);

	if (!rolls.length) {
		return;
	}
	for (var i =  0; i < rolls.length; i++) {
		// Initializing templates
		var kind = rolls[i]['kind']
		var $row = getRowTemplate();
		if(kind == 'I')
			var $row_slave = getRowSlaveTemplateImage();
		else
			var $row_slave = getRowSlaveTemplate();
		// Date manipulations
		var date = Date.parseTimestamp(rolls[i]['timestamp']);
		$row.find('#date').text(date.toShortString());

		// Juggling the title
		$row.find('#title').html(rolls[i]['title']);
		$row_slave.find('#title').html(rolls[i]['title']);
		$row_slave.find('#title').attr('href', rolls[i]['url'])

		$row.find('#description').html(rolls[i]['description']);
		$row.find('#kind').html(rolls[i]['kind']);
		$row.find('#colour').html(rolls[i]['colour']);
		
		// Adding tags
		addTags(rolls[i]['tags'], $row.find('#tags'));
		
		
		if (kind == 'I') {
			$row_slave.find('#image').attr('src', rolls[i]['url'])
		} else {
			$row_slave.find('#content').text(rolls[i]['content']);
		// Adding the content as html might distort the functionality of the web app
		// $row_slave.find('#content').html(rolls[i]['content'].replace(/\n/g, '<br />')
		// 													.replace(/\t/g, '    '));
			addTags(rolls[i]['tags'], $row_slave.find('#tags'));
		}

		// Linking controls
		$row.find('#control-url').attr('href', rolls[i]['url'])
		// Activating tooltips
		$row.find('#control-url').tooltip();
		$row.find('#control-edit').tooltip();
		$row.find('#control-delete').tooltip();

		$add_to = $('#'+where+'-tbl');
		// To cope up with deletes
		removeDatasheetById(rolls[i]['id'], $add_to);

		// Row set ID and append
		$row.attr('id', rolls[i]['id']);
		$row.appendTo('#'+where+'-tbl');
		// Row-Slave set ID and append
		$row_slave.attr('id', rolls[i]['id']+'-slave');
		$row_slave.appendTo('#'+where+'-tbl');
	};
}

function updateIdInPlace(section, roll) {
	$row = $('#'+section).find('#'+roll['id']);
	$row_slave = $('#'+section).find('#'+roll['id']+'-slave');

	$row.find('#title').text(roll['title']);
	$row_slave.find('#title').text(roll['title']);
	$row_slave.find('#title').attr('href', roll['url'])

	updateHandlingUndefinedAsText($row.find('#description'), roll['description']);
	updateHandlingUndefinedAsText($row.find('#kind'), roll['kind']);

	$row.find('#colour').text(roll['colour']);
	updateHandlingUndefinedAsText($row_slave.find('#content'), roll['content']);

	// Removing existing tags
	$row.find('#tags span').remove();
	$row_slave.find('#tags span').remove();
	addTags(roll['tags'], $row.find('#tags'));
	addTags(roll['tags'], $row_slave.find('#tags'));
}

function updateHandlingUndefinedAsText($node, value) {
	if (value == undefined)
		$node.text("");
	else
		$node.text(value);
}

function getRowTemplate() {
	return $('#template-tbl-tr').clone()
}
function getRowSlaveTemplate() {
	return $('#template-tbl-tr-slave').clone()
}
function getRowSlaveTemplateImage() {
	return $('#template-tbl-tr-image-slave').clone()
}
function getTagFrequencyTemplate() {
	return $('#template-tag-cloud-tag').clone()
}
// Inputs -
// $from: A list of tags
function addTags($from, $to) {
	for (tag_no in $from) {
		var $tag = $('#template-tag').clone();
		$tag.html($from[tag_no])
			.appendTo($to)
			.after(' ');
	};
}
// Input: Javascript object
function toggleSlave($master) {
	var $slave = $('#'+$($master).parent().attr('id')+'-slave');
	$slave.fadeToggle();
}

// Handle errors properly.
function editDatasheet($ref, event) {
	event.preventDefault();
	var $master = $($ref).parent() // div
					 .parent() // td
					 .parent(); // tr
	var id = $master.attr('id');
	var $slave = $('#'+id+'-slave');
	var $modal = $('#edit-ds-box');
	// var $modal = $('#edit-modal');

	var title = $master.find('#title').text();
	var description = $master.find('#description').text();
	var url = $master.find('#control-url').attr('href');
	var kind = $master.find('#kind').text();

	var $tags = $('#'+id).find('#tags span');
	var tags = "";
	for (var i = 0; i < $tags.length; i++) {
		tags += $tags[i].innerText;
		if (i != $tags.length-1)
			tags += ", ";
	};

	// Keeping for future versions
	// var colour = $master.find('#colour').text();

	$modal.find('#clear-form').click();
	// Adding it to the modal
	$modal.find('input[name="_id"]').val(id);
	$modal.find('input[name="url"]').val(url);
	$modal.find('input[name="title"]').val(title);
	$modal.find('input[name="description"]').val(description);
	$modal.find('input[name="tags"]').val(tags);
	
	if(kind == "H") {
		var content = $slave.find('#content').text();
		$modal.find('#content').val(content);
		$modal.find('#content-section').css('display', '');
	} else
		$modal.find('#content-section').css('display', 'none');

	$('#edit-ds').removeErrors();
	$('#goto-edit-modal-btn').click();
}

function confirmEditDatasheet($this) {
	$('#edit-ds').removeErrors();
	var $modal = $($this).parent() // div
						 .parent(); // div
	var id = $modal.find('#_id').val();
	var request = {
		'_id': id,
		'url': $modal.find('#url').val(),
		'title': $modal.find('#title').val(),
		'description': $modal.find('#description').val(),
		'content': $modal.find('#content').val(),
		'tags': $modal.find('#tags').val()
	};
	requestServce("/api/notes/modify/", request, function(response){
		if(response['success']) {
			correctEditedData(response['roll']);
			$modal.find('#cancel').click();
		} else {
			$('#edit-ds').markErrors(response);
			return false
			// alert("Modification failed due to unknown reasons.")
		}
	});
}

function correctEditedData(roll) {
	updateIdInPlace('highlights', roll);
	updateIdInPlace('stackups', roll);
	updateIdInPlace('images', roll);
	updateIdInPlace('search', roll);
}

function correctEditedDataForSection(id, roll) {
	var $master = $('#'+id).find(roll['_id']).attr('id');
	var $slave = $('#'+id+'-slave');
	var $modal = $('#edit-ds-box');

	var title = $master.find('#title').text();
	var description = $master.find('#description').text();
	var content = $slave.find('#content').text();
	var url = $master.find('#control-url').attr('href');
}

function removeDatasheet($ref, event) {
	event.preventDefault();
	var id = $($ref).parent() // div
					.parent() // td
					.parent() // tr
					.attr('id');
	var title = $($ref)	.parent() // div
						.parent() // td
						.parent() // tr
						.find('#title')
						.text();
	$('#delete-modal').find('#_id').text(id);
	$('#delete-modal').find('#title').text(title);
	$('#goto-delete-modal-btn').click();
}

function confirmDeleteDatasheet($ref, event) {
	var $modal = $($ref).parent() // div
					 .parent() // div
					 .parent() // div modal
	var id = $modal.find('#_id').text();
	var request = {'_id': id};
	requestServce("/api/notes/delete/", request, function(response){
		if(response['success']) {
			removeDatasheetById(id, null);
			$modal.find('#cancel').click();
		} else {
			alert("Deletion failed due to unknown reasons.")
		}
	});
}

function removeDatasheetById(id, $remove_from) {
	if (!$remove_from) {
		$remove_from  = $(document);
	};

	var $self = $remove_from.find('#'+id);
	var $slave = $remove_from.find('#'+id+'-slave');

	$slave.remove();
	$self.fadeOut();
	$self.remove();

	refreshResultStatus('highlights');
	refreshResultStatus('stackups');
	refreshResultStatus('images');
}

function refreshResultStatus(for_section) {
	if ($('#'+for_section+'-content').children().length == 0)
		$('#no-results-'+for_section).show();
	else
		$('#no-results-'+for_section).hide();
}

function closeSlave($slave_row) {
	$($slave_row)
	.parent()	// div
	.parent()	// td
	.parent()	// tr
	.fadeToggle();
}

function showSearchSideBar() {
	$('#search-side-bar').fadeIn();
}

// Credits: http://stackoverflow.com/questions/6504914/how-can-i-capture-keyboard-events-are-from-which-keys
// Last accessed on: 6-Apr-2013
function handleShortcuts(e) {
	e = e || window.event;
	var charCode = (typeof e.which == "number") ? e.which : e.keyCode;
	if (charCode > 0) {
		// console.log("Code: "+ charCode +", Typed character: " + String.fromCharCode(charCode));
		// If return key is pressed, then,
		if (charCode == 13) {
			var parent = e.target.parentElement;
			// console.log("'return' pressed");
			// Quick Search
			if ($(e.target).attr('id') == "search-text") {
				console.log('Quick Search');
				$('#search-text-btn').click();
			};
		};
		// Shortcuts
		// `: Perform Logout
		if (charCode == 96) {
			console.log('Logging out');
			window.location.assign('/logout/')
		};
	}
}

// Toggling the display of addon buttons
function displayToolkit(target) {
	$(target).find('#controls').css('visibility','');
}
function hideToolkit(target) {
	$(target).find('#controls').css('visibility','hidden');
}

function hashBind() {
	switch(document.location.hash) {
		case "":
			document.location.hash = '/highlights/';
			break;
		case "#/":
			document.location.hash = '/highlights/';
			break;
		case "#/highlights/":
			make_active('highlights');
			break;
		case "#/stackups/":
			make_active('stackups');
			break;
		case "#/images/":
			make_active('images');
			break;
		// case "#/filter/":
		// 	make_active('filter');
			break;
		case "#/search/":
			showSearchSideBar();
			make_active('search');
			break;
		case "#/change-username/":
			make_active('change-username');
			break;
		case "#/change-password/":
			make_active('change-password');
			break;
		// case "#/change-details/":
		// 	make_active('change-details');
			break;
		default:
			document.location.hash = '/highlights/';
			break;
	}
}

function make_active(active) {
	var $old_active = $('#app-content div:first');
	var old_id = $old_active.attr('id')
	var old_href = '#/' + old_id + '/'

	var $new_active = $('#'+active)
	var new_id = $new_active.attr('id')
	var new_href = '#/' + new_id + '/'

	// Correcting active selection
	$('#navigation [href="'+old_href+'"]').parent().removeClass('active')
	$('#navigation [href="'+new_href+'"]').parent().addClass('active')

	// Moving the old pane
	$old_active.appendTo('#app-storage');

	// Making the new pane active
	$new_active.appendTo('#app-content');
}

function getActiveId() {
	var $active = $('#app-content div:first');
	return $active.attr('id');
}
