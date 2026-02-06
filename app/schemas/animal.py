from marshmallow import Schema, fields, validate

class AnimalSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    type = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    breed = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    age_months = fields.Int(required=True, validate=validate.Range(min=1))
    price_per_unit = fields.Decimal(required=True, validate=validate.Range(min=0))
    quantity_available = fields.Int(required=True, validate=validate.Range(min=1))
    images = fields.List(fields.Str(), missing=list)
    county = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    status = fields.Str(validate=validate.OneOf(['available', 'sold', 'pending']), missing='available')
    farmer_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class AnimalUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=100))
    type = fields.Str(validate=validate.Length(min=1, max=50))
    breed = fields.Str(validate=validate.Length(min=1, max=50))
    age_months = fields.Int(validate=validate.Range(min=1))
    price_per_unit = fields.Decimal(validate=validate.Range(min=0))
    quantity_available = fields.Int(validate=validate.Range(min=1))
    county = fields.Str(validate=validate.Length(min=1, max=50))
    status = fields.Str(validate=validate.OneOf(['available', 'sold', 'pending']))

animal_schema = AnimalSchema()
animals_schema = AnimalSchema(many=True)
animal_update_schema = AnimalUpdateSchema()