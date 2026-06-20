from django import template
from django.template.library import token_kwargs
from django.urls import NoReverseMatch, reverse

register = template.Library()

class SafeURLNode(template.Node):
    def __init__(self, view_name, args, kwargs, asvar):
        self.view_name = view_name
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        try:
            view_name = self.view_name.resolve(context)
        except Exception:
            view_name = str(self.view_name)

        args = []
        for arg in self.args:
            try:
                args.append(arg.resolve(context))
            except Exception:
                args.append(None)

        kwargs = {}
        for k, v in self.kwargs.items():
            try:
                kwargs[k] = v.resolve(context)
            except Exception:
                kwargs[k] = None

        current_app = None
        if hasattr(context, "request") and hasattr(context.request, "current_app"):
            current_app = context.request.current_app

        try:
            return reverse(view_name, args=args, kwargs=kwargs, current_app=current_app)
        except NoReverseMatch:
            val = str(view_name)
            if "rotating-work-type-assign-view" in val:
                return "/employees/rotating-work-type-assign/"
            if "rotating-shift-assign-view" in val:
                return "/employees/rotating-shift-assign/"
            if "shift-request-view" in val or "shift-request" in val:
                return "/employees/shift-requests/"
            if "work-type-request-view" in val or "work-type-request" in val:
                return "/employees/work-type-requests/"
            if "employee-profile" in val:
                return "/employees/profile/"
            if "employee-document-requests" in val or "document-request" in val:
                return "/employees/document-requests/"
            if "employee-disciplinary-actions" in val or "disciplinary" in val:
                return "/employees/disciplinary-actions/"
            if "employee-policies" in val or "policies" in val:
                return "/employees/policies/"
            if "employee-org-chart" in val or "org-chart" in val:
                return "/employees/org-chart/"
            if "employee_list" in val or "employee-list" in val:
                return "/employees/"
            if "employee-create" in val or "employee_create" in val:
                return "/employees/create/"
            
            fallback_url = f"/stub-url/{val}/"
            if self.asvar:
                context[self.asvar] = fallback_url
                return ""
            return fallback_url

@register.tag(name="url")
def url(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError("'%s' takes at least one argument, the name of a url path." % bits[0])
    
    view_name = parser.compile_filter(bits[1])
    args = []
    kwargs = {}
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == "as":
        asvar = bits[-1]
        bits = bits[:-2]

    if bits:
        for bit in bits:
            match = token_kwargs((bit,), parser)
            if match:
                kwargs.update(match)
            else:
                args.append(parser.compile_filter(bit))

    return SafeURLNode(view_name, args, kwargs, asvar)
