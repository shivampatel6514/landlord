import uuid
from django.db import models


class CustomUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role_type = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'  # Set the table name to 'users'
class PropertyType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.name    
    
class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)  # Add the slug field here
    name = models.CharField(max_length=100)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    images = models.JSONField(null=True)    
    status = models.CharField(max_length=100)
    category = models.CharField(max_length=100,null=True)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    bedrooms = models.IntegerField(null=True)
    bathrooms = models.IntegerField(null=True)
    reception = models.IntegerField(null=True)
    zipcode = models.CharField(max_length=20)
    city = models.CharField(max_length=100,null=True)
    description = models.TextField()
    address = models.TextField()
    features = models.JSONField()
    nearest_station = models.JSONField(null=True)
    is_land = models.BooleanField(default=False)

    def __str__(self):
        return self.name            

class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name
