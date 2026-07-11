import json
import re
from datetime import datetime
from email.utils import parseaddr
from pathlib import Path


def load_config(path):
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def ensure_folder(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def format_timestamp(value=None):
    value = value or datetime.now()
    return value.strftime("%Y-%m-%d %H:%M:%S")


def render_template(template, context):
    pattern = re.compile(r"\{\{(\w+)\}\}")

    def replace(match):
        return str(context.get(match.group(1), ""))

    return pattern.sub(replace, template)


def load_text_file(path):
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        return handle.read()


def validate_email(address):
    if not address:
        return False
    _, email = parseaddr(address)
    return bool(email and "@" in email)


def normalize_header(value):
    if value is None:
        return ""
    return str(value).strip().title().replace(" ", " ")
