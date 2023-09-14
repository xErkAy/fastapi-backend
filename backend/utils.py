from tortoise.queryset import QuerySet


async def filter_city_street(queryset: QuerySet, **kwargs) -> QuerySet:
    city = kwargs.get('city')
    if city is not None:
        if city.isdigit():
            queryset = await queryset.filter(city_id=city)
        queryset = await queryset.filter(city__name__icontains=city)

    street = kwargs.get('street')
    if street is not None:
        if street.isdigit():
            queryset = await queryset.filter(street_id=street)
        queryset = await queryset.filter(street__name__icontains=street)
    return queryset
