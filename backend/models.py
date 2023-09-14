from tortoise import Model, fields


class City(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)

    def __str__(self):
        return self.name


class Street(Model):
    name = fields.CharField(max_length=100)
    city = fields.ForeignKeyField('models.City', null=True, on_delete=fields.SET_NULL)

    def __str__(self):
        return f'st. {self.name}, {self.city}'


class Shop(Model):
    name = fields.CharField(max_length=30)
    city = fields.ForeignKeyField('models.City', null=True, on_delete=fields.SET_NULL)
    street = fields.ForeignKeyField('models.Street', null=True, on_delete=fields.SET_NULL)
    building = fields.CharField(max_length=10)
    open_time = fields.TimeField()
    close_time = fields.TimeField()

    def __str__(self):
        return f'{self.name}: {self.street}, building: {self.building}'

    @property
    def address(self):
        return f'st. {self.street}, {self.city}, building {self.building}'
