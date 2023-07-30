from marshmallow import Schema, fields


class IdeaSchema(Schema):
    idea = fields.Str(required=True, validate=fields.Length(128))
    user_id = fields.Int(required=True)