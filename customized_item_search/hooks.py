from . import __version__ as app_version

app_name = "customized_item_search"
app_title = "Customized Item Search"
app_publisher = "hafeesk@gmail.com"
app_description = "Search Item"
app_email = "hafeesk@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/customized_item_search/css/customized_item_search.css"
# app_include_js = "/assets/customized_item_search/js/customized_item_search.js"
app_include_js = "customized_item_search.bundle.js"

# include js, css files in header of web template
# web_include_css = "/assets/customized_item_search/css/customized_item_search.css"
# web_include_js = "/assets/customized_item_search/js/customized_item_search.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "customized_item_search/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "customized_item_search.utils.jinja_methods",
#	"filters": "customized_item_search.utils.jinja_filters"
# }

jinja = {
	"methods": "customized_item_search.custom_script.jinja.convert_number_to_given_language"
}

# Installation
# ------------

# before_install = "customized_item_search.install.before_install"
# after_install = "customized_item_search.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "customized_item_search.uninstall.before_uninstall"
# after_uninstall = "customized_item_search.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "customized_item_search.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"customized_item_search.tasks.all"
#	],
#	"daily": [
#		"customized_item_search.tasks.daily"
#	],
#	"hourly": [
#		"customized_item_search.tasks.hourly"
#	],
#	"weekly": [
#		"customized_item_search.tasks.weekly"
#	],
#	"monthly": [
#		"customized_item_search.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "customized_item_search.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "customized_item_search.event.get_events"
# }
override_whitelisted_methods = {
	"frappe.desk.search.search_widget": "customized_item_search.custom_script.search.custom_search_widget"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "customized_item_search.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"customized_item_search.auth.validate"
# ]

fixtures = [
		{
			"dt":"Print Format",
			"filters":[
				["module","=","Customized Item Search"]
			]
		}
	]
