{% extends "mail_templated/base.tpl" %}

{% block subject %}
Password Reset Email
{% endblock %}

{% block html %}
<h1>Hello There</h1>
<p>
It seems like you've forgotten your password. Worry no worry. Here's a link to help you reset it:
</p>
<p>
    <a href="http://127.0.0.1:8000/accounts/api/v1/forget-password/confirm/{{ token }}">Reset your password</a>
</p>
{% endblock %}
