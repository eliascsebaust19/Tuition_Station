from jinja2 import Environment, FileSystemLoader
import os

# Write a minimal, clean base.html
content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Tuition Station{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/atelier.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% block nav %}{% endblock %}

    {% block content %}{% endblock %}

    {% block footer %}{% endblock %}

    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
"""

# Test Jinja2 syntax
try:
    env = Environment()
    env.parse(content)
    print('Jinja2 syntax OK')
    # Write to file
    with open(r'E:\Level 2 term II\DBMS\tuition_system\templates\base.html', 'w') as f:
        f.write(content)
    print('base.html written successfully')
except Exception as e:
    print(f'Error: {e}')
