from django.forms import widgets
from django.utils.safestring import mark_safe


class CustomImageWidget(widgets.FileInput):
    
    def render(self, name, value, attrs=None, **kwargs):
        default_html = super().render(name, value, attrs, **kwargs)
        print(value.url)
        img_html = mark_safe(f'<img src="{value.url}" width="200">')
        print("done")
        return f"{img_html}" 
    