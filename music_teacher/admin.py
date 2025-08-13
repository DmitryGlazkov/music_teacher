from datetime import datetime

from flask import redirect, request, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms.fields import TextAreaField


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class TextDataAdmin(ModelView):
    column_labels = {
        'title': 'Title',
        'text': 'Content',
        'added_by': 'Added By',
        'timestamp': 'Date Added'
    }
    form_columns = ['title', 'text', 'added_by']
    form_overrides = {
        'text': TextAreaField
    }
    form_args = {
        'text': {
            'render_kw': {'rows': 10}
        }
    }

    column_default_sort = ('id', True)

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.timestamp = datetime.utcnow()
        return super().on_model_change(form, model, is_created)


class CustomModelView(ModelView):
    column_default_sort = ('id', True)


admin = Admin(
    name='Music Teacher Admin',
    template_mode='bootstrap3',
    index_view=MyAdminIndexView()
)
