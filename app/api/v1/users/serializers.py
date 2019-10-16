from marshmallow import fields, ValidationError, pre_load, post_dump
from marshmallow_enum import EnumField

from app import ma
from app.models.app_models import User, ParkingSlots, UserParkingSlots


class UserModelSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name')
        model = User

    @post_dump(pass_many=True)
    def wrap(self, data, many):
        key = 'users' if many else 'user'
        return {
            key: data,
        }


class ParkingSlotsModelSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'is_reserved')
        model = ParkingSlots


# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Field can\'t be blank!')


class UserSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(
        required=True,
        validate=must_not_be_blank
    )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=must_not_be_blank
    )
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    parking_slots = ma.Nested(ParkingSlotsModelSchema, many=True)

    # Clean up data
    @pre_load
    def process_input(self, data):
        data['username'] = data['username'].lower().strip()
        data['first_name'] = data['first_name'].strip()
        data['last_name'] = data['last_name'].strip()
        return data

    # We add a post_dump hook to add an envelope to responses
    @post_dump(pass_many=True)
    def wrap(self, data, many):
        key = 'users' if many else 'user'
        return {
            key: data,
        }
