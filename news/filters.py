from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter
from django.forms import DateTimeInput
from .models import *


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name="postcategory__categoryTrough",
        queryset=Category.objects.all(),
        label="Category",
        empty_label="Любая категория"
    )

    date_after = DateTimeFilter(
        field_name="dateCreation",
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'}
        )
    )

    class Meta:
        model = Post
        fields = {
            'title': ["icontains"],
        }

