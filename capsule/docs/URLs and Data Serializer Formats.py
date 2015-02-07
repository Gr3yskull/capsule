# TODO List
- Make 404 page and not authorized page

# URL Listings
urlpatterns = patterns('',
	# API
	# (r'^api/$', ),

	(r'^api/user/signup/$', ),
	(r'^api/user/login/$', ),
	(r'^api/user/login_no_redirect/$', ),
	(r'^api/user/login_status/$', ),
	(r'^api/user/logout/$', ),
	(r'^api/user/logout_no_redirect/$', ),
	(r'^api/user/modify/$', ),
	(r'^api/user/username_available/$', ),
	(r'^api/user/delete_account/$', ),
	(r'^api/user/get_profile/$', ),

	# (r'^api/notes/', ),
	(r'^api/notes/page/$', ),
	(r'^api/notes/page/70/$', ),
	(r'^api/notes/add/$', ),
	(r'^api/notes/modify/$', ),
	(r'^api/notes/filter/$', ),
	(r'^api/notes/filter/page/70$', ),
	(r'^api/notes/misc/colour_codes/$', ),

	# Deprecated
	(r'^api/misc/login_status/$', ),
)



# Filtering Query (Highlights)
{
	url: "",
	title:	[
		"The Title",
		...
	],
	desc:	[
		"description",
		...
	],
	content:	[
		"is a lover",
		...
	],
	date:	[
		{start:"", end:""},
		...
	],
	tags: [
		"Just Now!",
		"Personal",
		"News",
		...
	],
	color: [
		"red",
		"blue",
		...
	]
}


# JSON for filters (Highlight), v1
{
	title:	[
		"The Title",
		...
	],
	desc:	[
		"description",
		...
	],
	content:	[
		"is a lover",
		...
	],
	date:	[
		{start:"", end:""},
		...
	],
	tags: [
		"Just Now!",
		"Personal",
		"News",
		...
	],
	color: [
		"red",
		"blue",
		...
	],
	ctype: [
		"plain",
		"image",
		"jotters",
		"stacks",
		"all"
	]
}
