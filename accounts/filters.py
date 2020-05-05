import django_filters
from django_filters import DateFilter
from .models import *

class ProgressFilter(django_filters.FilterSet):
	end_date = DateFilter(field_name="date_created", lookup_expr='lte')

	class Meta:
		model = Progress
		fields = '__all__'
		exclude = ['student', 'date_created']