from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import *
from datetime import datetime

from order_service.util import generate_token

db = SqliteDatabase('order_service/data.db')


class BaseModel(Model):
    updated_at = DateTimeField(default=datetime.now)
    created_at = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)

    def serialize(self):
        return model_to_dict(self, backrefs=True, recurse=True)

    class Meta:
        database = db


class Order(BaseModel):
    unique_id = CharField(default=generate_token)
    cust_id = IntegerField()
    emp_id = IntegerField()
    from_lat = FloatField()
    from_lng = FloatField()
    additional_detail = TextField(default='')

    class Meta:
        db_table = 'order'


class OrderPoint(BaseModel):
    order = ForeignKeyField(Order, backref='points')
    receiver_name = CharField()
    to_lat = FloatField()
    to_lng = FloatField()
    status = IntegerField(default=0)
    weight = FloatField()

    class Meta:
        table_name = 'order_point'
