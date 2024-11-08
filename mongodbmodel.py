from mongoengine import Document, fields, EmbeddedDocument
from mongoengine import connect

MONGODB_URL ="mongodb+srv://dimitrikwihangana:<db_password>@waterpotability.lb4ag.mongodb.net/?retryWrites=true&w=majority&appName=waterpotability"

connect(host=MONGODB_URL)

class WaterQuality(Document):
    sample_id = fields.IntField(primary_key=True, auto_increment=True)
    potability = fields.BooleanField()
    chemical_properties = fields.EmbeddedDocumentListField('ChemicalProperties')
    physical_properties = fields.EmbeddedDocumentListField('PhysicalProperties')

class ChemicalProperties(EmbeddedDocument):
    ph = fields.FloatField()
    chloramines = fields.FloatField()
    sulfate = fields.FloatField()
    conductivity = fields.FloatField()
    organic_carbon = fields.FloatField()
    trihalomethanes = fields.FloatField()

class PhysicalProperties(EmbeddedDocument):
    hardness = fields.FloatField()
    solids = fields.FloatField()
    turbidity = fields.FloatField()
