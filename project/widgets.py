from django.forms.widgets import ClearableFileInput

class SmallClearableFileInput(ClearableFileInput):
    template_name = 'widgets/small_clearable_file_input.html'
