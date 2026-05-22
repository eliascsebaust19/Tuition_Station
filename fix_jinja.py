from jinja2 import Template

# Minimal, clean base.html
template_str = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Tuition Station{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/atelier.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% block nav %}
    <nav>
        <div>
            <a href="{{ url_for('auth.index') }}">Tuition Station</a>
            <ul>
                {% if current_user.is_authenticated %}
                    {% if current_user.role == 'student' %}
                    <li><a href="{{ url_for('student.dashboard') }}">Dashboard</a></li>
                    {% elif current_user.role == 'teacher' %}
                    <li><a href="{{ url_for('teacher.dashboard') }}">Dashboard</a></li>
                    {% elif current_user.role == 'admin' %}
                    <li><a href="{{ url_for('admin.dashboard') }}">Dashboard</a></li>
                    {% endif %}
                    <li><a href="{{ url_for('auth.logout') }}">Logout</a></li>
                {% else %}
                    <li><a href="{{ url_for('auth.login') }}">Sign In</a></li>
                    <li><a href="{{ url_for('auth.register') }}">Register</a></li>
                {% endif %}
            </ul>
        </div>
    </nav>
    {% endblock %}

    {% block content %}{% endblock %}

    {% block footer %}
    <footer>
        <p>&copy; 2026 Tuition Station</p>
    </footer>
    {% endblock %}

    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>"""

# Test Jinja2 syntax
try:
    t = Template(template_str)
    print("Jinja2 syntax OK")
    # Write to file
    with open(r'E:\Level 2 term II\DBMS\tuition_system\templates\base.html', 'w') as f:
        f.write(template_str)
    print("base.html written successfully")
except Exception as e:
    print(f"Error: {e}")
