from django_filters import widgets, FilterSet, DateFromToRangeFilter, RangeFilter, DateFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):
    pub_time__gt = DateFilter(
        field_name='pub_time',
        label = 'Start date',
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        ),
        lookup_expr='date__gte'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
        }