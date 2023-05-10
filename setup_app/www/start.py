import frappe

def get_context(context):
    context["no_header"] = True
    return context