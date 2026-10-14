{% extends "mail_templated/base.tpl" %}

{% block subject %}
Activation Email
{% endblock %}

{% block html %}
<h1>Hello There</h1>

<p>
    <a href="http://127.0.0.1:8000/accounts/api/v1/verification/confirm/{{ token }}">Activate your account</a>
</p>
{% endblock %}