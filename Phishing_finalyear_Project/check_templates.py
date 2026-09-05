import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phishing_project.settings')
django.setup()

from django.template.loader import get_template

templates = ['base.html', 'detector.html', 'index.html', 'analytics.html']

for tmpl_name in templates:
    try:
        tmpl = get_template(tmpl_name)
        print(f"✓ {tmpl_name}: OK")
    except Exception as e:
        print(f"✗ {tmpl_name}: {type(e).__name__}")
        print(f"  Error: {str(e)[:200]}")
