from .utils import render_template


def render_email(template, stakeholder):
    context = {k: v for k, v in stakeholder.items()}
    return render_template(template, context)


def render_subject(subject_template, stakeholder):
    return render_template(subject_template, stakeholder)
