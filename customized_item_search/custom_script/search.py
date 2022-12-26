

import json
import re

import frappe
from frappe import _, is_whitelisted
from frappe.permissions import has_permission
from frappe.utils import cint, cstr

from frappe.desk.search import sanitize_searchfield, get_std_fields_list, relevance_sorter

@frappe.whitelist()
def custom_search_widget(
	doctype,
	txt,
	query=None,
	searchfield=None,
	start=0,
	page_length=20,
	filters=None,
	filter_fields=None,
	as_dict=False,
	reference_doctype=None,
	ignore_user_permissions=False,
):

	start = cint(start)

	if isinstance(filters, str):
		filters = json.loads(filters)

	if searchfield:
		sanitize_searchfield(searchfield)

	if not searchfield:
		searchfield = "name"

	standard_queries = frappe.get_hooks().standard_queries or {}

	if query and query.split()[0].lower() != "select":
		# by method
		try:
			is_whitelisted(frappe.get_attr(query))
			if query == "erpnext.controllers.queries.item_query":
				query = "customized_item_search.custom_script.queries.custom_item_query"
			frappe.response["values"] = frappe.call(
				query, doctype, txt, searchfield, start, page_length, filters, as_dict=as_dict
			)
		except frappe.exceptions.PermissionError as e:
			if frappe.local.conf.developer_mode:
				raise e
			else:
				frappe.respond_as_web_page(
					title="Invalid Method",
					html="Method not found",
					indicator_color="red",
					http_status_code=404,
				)
			return
		except Exception as e:
			raise e
	elif not query and doctype in standard_queries:
		# from standard queries
		custom_search_widget(
			doctype, txt, standard_queries[doctype][0], searchfield, start, page_length, filters
		)
	else:
		meta = frappe.get_meta(doctype)

		if query:
			frappe.throw(_("This query style is discontinued"))
			# custom query
			# frappe.response["values"] = frappe.db.sql(scrub_custom_query(query, searchfield, txt))
		else:
			if isinstance(filters, dict):
				filters_items = filters.items()
				filters = []
				for f in filters_items:
					if isinstance(f[1], (list, tuple)):
						filters.append([doctype, f[0], f[1][0], f[1][1]])
					else:
						filters.append([doctype, f[0], "=", f[1]])

			if filters is None:
				filters = []
			or_filters = []

			# build from doctype
			if txt:
				field_types = [
					"Data",
					"Text",
					"Small Text",
					"Long Text",
					"Link",
					"Select",
					"Read Only",
					"Text Editor",
				]
				search_fields = ["name"]
				if meta.title_field:
					search_fields.append(meta.title_field)

				if meta.search_fields:
					search_fields.extend(meta.get_search_fields())

				for f in search_fields:
					fmeta = meta.get_field(f.strip())
					if not meta.translated_doctype and (
						f == "name" or (fmeta and fmeta.fieldtype in field_types)
					):
						or_filters.append([doctype, f.strip(), "like", f"%{txt}%"])

			if meta.get("fields", {"fieldname": "enabled", "fieldtype": "Check"}):
				filters.append([doctype, "enabled", "=", 1])
			if meta.get("fields", {"fieldname": "disabled", "fieldtype": "Check"}):
				filters.append([doctype, "disabled", "!=", 1])

			# format a list of fields combining search fields and filter fields
			fields = get_std_fields_list(meta, searchfield or "name")
			if filter_fields:
				fields = list(set(fields + json.loads(filter_fields)))
			formatted_fields = [f"`tab{meta.name}`.`{f.strip()}`" for f in fields]

			# Insert title field query after name
			if meta.show_title_field_in_link:
				formatted_fields.insert(1, f"`tab{meta.name}`.{meta.title_field} as `label`")

			# In order_by, `idx` gets second priority, because it stores link count
			from frappe.model.db_query import get_order_by

			order_by_based_on_meta = get_order_by(doctype, meta)
			# 2 is the index of _relevance column
			order_by = f"{order_by_based_on_meta}, `tab{doctype}`.idx desc"

			if not meta.translated_doctype:
				formatted_fields.append(
					"""locate({_txt}, `tab{doctype}`.`name`) as `_relevance`""".format(
						_txt=frappe.db.escape((txt or "").replace("%", "").replace("@", "")),
						doctype=doctype,
					)
				)
				order_by = f"_relevance, {order_by}"

			ignore_permissions = (
				True
				if doctype == "DocType"
				else (
					cint(ignore_user_permissions)
					and has_permission(
						doctype,
						ptype="select" if frappe.only_has_select_perm(doctype) else "read",
					)
				)
			)

			values = frappe.get_list(
				doctype,
				filters=filters,
				fields=formatted_fields,
				or_filters=or_filters,
				limit_start=start,
				limit_page_length=None if meta.translated_doctype else page_length,
				order_by=order_by,
				ignore_permissions=ignore_permissions,
				reference_doctype=reference_doctype,
				as_list=not as_dict,
				strict=False,
			)

			if meta.translated_doctype:
				# Filtering the values array so that query is included in very element
				values = (
					result
					for result in values
					if any(
						re.search(f"{re.escape(txt)}.*", _(cstr(value)) or "", re.IGNORECASE)
						for value in (result.values() if as_dict else result)
					)
				)

			# Sorting the values array so that relevant results always come first
			# This will first bring elements on top in which query is a prefix of element
			# Then it will bring the rest of the elements and sort them in lexicographical order
			values = sorted(values, key=lambda x: relevance_sorter(x, txt, as_dict))

			# remove _relevance from results
			if not meta.translated_doctype:
				if as_dict:
					for r in values:
						r.pop("_relevance")
				else:
					values = [r[:-1] for r in values]

			frappe.response["values"] = values