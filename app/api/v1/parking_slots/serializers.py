from marshmallow import fields, ValidationError, pre_load, post_dump

from app import ma
from app.models.app_models import ParkingSlots


class ParkingSlotModelSchema(ma.ModelSchema):

    class Meta:
        fields = ('id', 'is_reserved')
        model = ParkingSlots


# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Field cannot be blank!')


# Schema for getting UserParkingSlots List
class UserParkingSlotsSchema(ma.Schema):
    parking_slot_id = fields.Int(dump_only=True)


# Schema for getting Parking Slots list
class ParkingSlotsSchema(ma.Schema):
    id = fields.Int(required=True)
    lat = fields.Float(dump_only=True)
    long = fields.Float(dump_only=True)
    is_reserved = fields.Bool(required=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many):
        key = 'parking_slots' if many else 'parking_slot'
        return {
            key: data,
        }
