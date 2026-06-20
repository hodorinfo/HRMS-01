"""Email template helpers."""

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATES_DIR = Path(__file__).parent / "templates"


def render_email_template(template_name: str, context: dict[str, Any]) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(template_name)
    return template.render(**context)


DEFAULT_TEMPLATES = {
    "welcome": "welcome.html",
    "password_reset": "password_reset.html",
    "leave_approved": "leave_approved.html",
    "payslip_ready": "payslip_ready.html",
}
