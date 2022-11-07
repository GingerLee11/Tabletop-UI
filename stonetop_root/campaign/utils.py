from django.forms import MultiWidget 
from django import forms 
from django.core.exceptions import ValidationError


class OptionalChoiceWidget(MultiWidget):

    def decompress(self, value):
        if value:
            if value in [x[0] for x in self.widgets[0].choices]:
                return [value, ""] # make it set the pull down to chioce
            else:
                return ["", value] # Keep pulldown to blank, set freetext
        return ["", ""]


class OptionalChoiceField(forms.MultiValueField):
    def __init__(self, choices, max_length=150, *args, **kwargs):
        """
        Sets the two fields as not required 
        but will enforce that (at least) one is set in compress
        """
        fields = (forms.ChoiceField(choices=choices, required=False), forms.CharField(required=False))
        self.widget = OptionalChoiceWidget(widgets=[f.widget for f in fields])
        super(OptionalChoiceField, self).__init__(required=False, fields=fields, *args, **kwargs)

    def compress(self, data_list):
        """
        return the choicefield value if selected or charfield value
        (if both empty, will throw exception)
        """
        if not data_list:
            raise ValidationError("Need to select an option or enter text for this field")
        if data_list[1]:
            return data_list[1]
        else:
            return data_list[0]

