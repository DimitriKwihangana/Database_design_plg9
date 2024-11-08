from mongoengine import Document, StringField, EmailField, IntField, DateTimeField, DecimalField, ListField, EmbeddedDocument, EmbeddedDocumentField, ReferenceField
from mongoengine import connect

# Connect to MongoDB (adjust parameters as necessary)
connect('my_database')

# Define the EmbeddedDocument for Address
class Address(EmbeddedDocument):
    street = StringField(max_length=100)
    city = StringField(max_length=50)
    state = StringField(max_length=50)
    zip_code = StringField(max_length=10)

# Define the Customer Document
class Customer(Document):
    customer_id = IntField(primary_key=True)
    first_name = StringField(max_length=50, required=True)
    last_name = StringField(max_length=50, required=True)
    phone = StringField(max_length=15)
    email = EmailField(max_length=100, unique=True, required=True)
    address = EmbeddedDocumentField(Address)

    meta = {
        'collection': 'customers',
        'indexes': ['email', 'customer_id'],  # Create indexes for efficient querying
        'ordering': ['last_name', 'first_name']
    }

# Define the Order Document
class Order(Document):
    order_id = IntField(primary_key=True)
    customer = ReferenceField(Customer, required=True)
    order_status = StringField(max_length=20)
    order_date = DateTimeField(required=True)
    required_date = DateTimeField()
    shipped_date = DateTimeField()

    meta = {
        'collection': 'orders',
        'indexes': ['order_id', 'customer'],  # Index on customer for faster lookups
        'ordering': ['-order_date']
    }

# Define the Product Document
class Product(Document):
    product_id = IntField(primary_key=True)
    name = StringField(max_length=100, required=True)
    quantity = IntField(min_value=0)

    meta = {
        'collection': 'products',
        'indexes': ['product_id', 'name'],
        'ordering': ['name']
    }

# Define the OrderItem Embedded Document for Order items
class OrderItem(EmbeddedDocument):
    item_id = IntField(required=True)
    product = ReferenceField(Product, required=True)
    quantity = IntField(min_value=1, required=True)
    list_price = DecimalField(precision=2, min_value=0, required=True)
    discount = DecimalField(precision=2, min_value=0)

# Modify the Order Document to include Order Items
class Order(Document):
    order_id = IntField(primary_key=True)
    customer = ReferenceField(Customer, required=True)
    order_status = StringField(max_length=20)
    order_date = DateTimeField(required=True)
    required_date = DateTimeField()
    shipped_date = DateTimeField()
    items = ListField(EmbeddedDocumentField(OrderItem))

    meta = {
        'collection': 'orders',
        'indexes': ['order_id', 'customer'],  # Index on customer for faster lookups
        'ordering': ['-order_date']
    }
