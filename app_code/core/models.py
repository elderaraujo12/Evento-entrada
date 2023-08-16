from django.db import models
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class CodigoPulseira(models.Model): 
    codigo = models.IntegerField(unique=True)
    status = models.BooleanField(default=False)
    qrcode = models.ImageField(upload_to='media/qrcodes/', blank=True, null=True)

    def __str__(self):
        return f'Código: {self.codigo}, Status: {"Liberado" if self.status else "Bloqueado"}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.qrcode:  # Gera o QR code apenas se não estiver presente
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(str(self.codigo))
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img_io = BytesIO()
            img.save(img_io, format='PNG')
            filename = f'qrcode_{self.codigo}.png'
            self.qrcode.save(filename, ContentFile(img_io.getvalue()), save=True)

class Pulseira(models.Model):
    codigo_pulseira = models.OneToOneField(CodigoPulseira, on_delete=models.CASCADE)


@receiver(post_save, sender=CodigoPulseira)
def criar_pulseira(sender, instance, created, **kwargs):
    if created:
        Pulseira.objects.create(codigo_pulseira=instance)
