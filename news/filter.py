


from django_filters import FilterSet, DateFilter
from .models import News
from django.forms import DateInput

class NewsFilter(FilterSet):
    date = DateFilter(
        field_name='dates',
        label='time',
        widget=DateInput(
            attrs={
                'type':'date',
            }

        ),
    )


    class Meta:
       model = News
       fields = {

           'name': ['icontains'],
           'quantity': ['gt'],

       }

