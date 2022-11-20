from django.db import models

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)


def image_path(instance, filename):
    return '/'.join(['sensorImages', f'sensor_id_{instance.sensor.id}', filename])


class Sensor(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=image_path, null=True, blank=True)
