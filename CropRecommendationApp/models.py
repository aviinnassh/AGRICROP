from django.db import models

class crop(models.Model):
    crop_id = models.AutoField('Crop ID', primary_key=True)
    crop_name = models.CharField('Crop Name', max_length=100, unique=True)
    crop_details = models.TextField('Crop Details', max_length=400)
    crop_category = models.CharField('Crop Category', max_length=20)
    crop_image = models.ImageField('Crop Image', upload_to='upload_images/crop/')

    def __str__(self):
        return self.crop_name

class Fertilizer(models.Model):
    name = models.CharField('Fertilizer Name', max_length=100, unique=True)
    description = models.TextField('Fertilizer Details', max_length=500)

    def __str__(self):
        return self.name

class crop_recommed(models.Model):
    cr_id = models.AutoField('Crop Recommend ID', primary_key=True)
    cr_farmername = models.CharField('Farmer Name', max_length=100)
    cr_nitrogen = models.PositiveIntegerField('Soil Nitrogen')
    cr_phosphorous = models.PositiveIntegerField('Soil Phosphorous')
    cr_potassium = models.PositiveIntegerField('Soil Potassium')
    cr_ph = models.FloatField('Soil pH')
    cr_temperature = models.FloatField('Soil Temperature')
    cr_humidity = models.FloatField('Relative Humidity')
    cr_rainfall = models.FloatField('Rainfall')
    cr_crop = models.CharField('Recommended Crop', max_length=100)

class fertilizer_recommed(models.Model):
    fr_id = models.AutoField('Fertilizer Recommend ID', primary_key=True)
    fr_farmername = models.CharField('Farmer Name', max_length=100)
    fr_crop = models.CharField('Crop Type', max_length=100)
    fr_soil = models.CharField('Soil Type', max_length=100)
    fr_nitrogen = models.PositiveIntegerField('Soil Nitrogen')
    fr_phosphorous = models.PositiveIntegerField('Soil Phosphorous')
    fr_potassium = models.PositiveIntegerField('Soil Potassium')
    fr_temperature = models.FloatField('Soil Temperature')
    fr_humidity = models.FloatField('Relative Humidity')
    fr_moisture = models.FloatField('Soil Moisture')
    fr_fertilizer = models.CharField('Recommended Fertilizer', max_length=100)

class CropModel:
    def __init__(self, clf, encoder):
        self.clf = clf
        self.encoder = encoder

    def predict(self, X):
        pred = self.clf.predict(X)
        return self.encoder.inverse_transform(pred)