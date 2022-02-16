from django.forms.widgets import ClearableFileInput

class SmallClearableFileInput(ClearableFileInput):
    template_name = 'users/widgets/small_clearable_file_input.html'
