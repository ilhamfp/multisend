from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import *
from datetime import datetime

db = SqliteDatabase('order_service/data.db')

class BaseModel(Model):
    updated_at = DateTimeField(default=datetime.now)
    created_at = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)

    def serialize(self):
        return model_to_dict(self, backrefs=True, recurse=False)

    class Meta:
        database = db


class Order(BaseModel):
    id = IntegerField()
    cust_id = IntegerField()
    emp_id = IntegerField()

    class Meta:
        db_table = 'order'
