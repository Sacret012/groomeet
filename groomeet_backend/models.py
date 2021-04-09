from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel, SoftDeletableModel
from dateutil.relativedelta import relativedelta
from enum import Enum

# Create your models here.

class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre

class Instrumento(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    familia = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.nombre

#Método auxiliar para guardar la imagen como la id del usuario seguida de un punto
def rename_avatar_image(instance, filename):
        filesplits = filename.split('.')
        return 'media/images/avatars/%s.%s' % (instance.usuario.id, filesplits[-1])

#Añadir ubicaciones para mejora del filtro de búsqueda
class Musico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    instrumentos = models.ManyToManyField(Instrumento)
    generos = models.ManyToManyField(Genero,verbose_name="Géneros")
    fechaNacimiento = models.DateField(verbose_name="Fecha de nacimiento", null=True)
    descripcion = models.TextField(verbose_name="Descripción")
    enlaceVideo = models.CharField(max_length=150, verbose_name="Enlace de vídeo", blank=True)
    avatar = models.ImageField(upload_to=rename_avatar_image, blank=True, null=True)
    #Sección de likes de Músico a Músico
    likesRecibidos = models.ManyToManyField(User, related_name="likesDados", blank=True) #Tabla que relaciona con los usuarios que te han dado like
    noLikesRecibidos = models.ManyToManyField(User, related_name="noLikesDados", blank=True) #Tabla que relaciona con los usuarios que te han dado "no me gusta"
    #Sección de likes de Músico a Banda
    likesRecibidosBanda = models.ManyToManyField('Banda', related_name="likesDadosMusico", blank=True)
    noLikesRecibidosBanda = models.ManyToManyField('Banda', related_name="noLikesDadosMusico", blank=True)

    def __str__(self):
        return self.usuario.username

    @property
    def numLikes(self):
        return self.likesRecibidos.all().count()

    @property
    def edad(self):
        return relativedelta(date.today(), self.fechaNacimiento).years

#Añadir ubicaciones para mejora del filtro de búsqueda
class Banda(models.Model):
    nombre = models.CharField(max_length=50)
    administrador = models.ForeignKey(Musico, on_delete = models.DO_NOTHING, related_name="bandasAdministradas") #Si desaparece el administrador, la banda puede seguir creada
    miembros = models.ManyToManyField(Musico, through='MiembroDe', blank=True)
    generos = models.ManyToManyField(Genero, blank=True)
    instrumentos = models.ManyToManyField(Instrumento, blank=True)
    #Sección de likes de Banda a Músico
    likesRecibidosMusico = models.ManyToManyField(User, related_name="likesDadosBanda", blank=True)
    noLikesRecibidosMusico = models.ManyToManyField(User, related_name="noLikesDadosBanda", blank=True)
    #Sección de likes de Banda a Banda
    likesRecibidosBanda = models.ManyToManyField('Banda', related_name="likesDadosBanda", blank=True)
    noLikesRecibidosBanda = models.ManyToManyField('Banda', related_name="noLikesDadosBanda", blank=True)

    def __str__(self):
        return self.nombre

class MiembroNoRegistrado(models.Model):
    banda = models.ForeignKey(Banda, on_delete = models.CASCADE, related_name="miembrosNoRegistrados")
    nombre = models.CharField(max_length=500)
    descripcion = models.CharField(max_length=500)
    instrumentos = models.ManyToManyField(Instrumento, blank=True)
    #foto?

    def __str__(self):
        return self.nombre

class MiembroDe(models.Model):
    musico = models.ForeignKey(Musico, on_delete = models.CASCADE) #Si se borra el músico, esta relación se elimina, igual con la banda
    banda = models.ForeignKey(Banda, on_delete = models.CASCADE)
    fechaUnion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de unión")



#TimeStampedModel tiene campos de created y modified, que almacenan las horas de creación y modificación
#SoftDeletableModel en lugar de borrar una entrada de la tabla, le activa un campo llamado "is_removed"
class Chat(TimeStampedModel, SoftDeletableModel):
    participante1 = models.ForeignKey(Musico, verbose_name="Participante 1", on_delete=models.CASCADE, related_name="chats1")
    participante2 = models.ForeignKey(Musico, verbose_name="Participante 2", on_delete=models.CASCADE, related_name="chats2")

    def __str__(self):
        return "Chat de " + self.participante1.usuario.username + " con " + self.participante2.usuario.username


class Mensaje(TimeStampedModel, SoftDeletableModel):
    chat = models.ForeignKey(Chat, verbose_name="Chat", on_delete=models.CASCADE, related_name="mensajes")
    autor = models.ForeignKey(Musico, verbose_name="Autor", on_delete=models.CASCADE, related_name="mensajes")
    cuerpo = models.TextField(verbose_name="Cuerpo del mensaje")
    #leido = models.BooleanField(verbose_name=_("Leido"), default=False)   #A tener en cuenta para posible mejora del chat, "doble check azul"

    def __str__(self):
        return self.autor.usuario.username + "(" + self.created + ") - '" + self.cuerpo + "'"

#Estado de las invitaciones a una banda
class EstadoInvitacion(Enum):
    Rechazada = "Rechazada"
    Pendiente = "Pendiente"
    Aceptada = "Aceptada"

class Invitacion(TimeStampedModel):
    emisor = models.ForeignKey(Musico, on_delete=models.CASCADE, related_name="invitacionesEnviadas")
    receptor = models.ForeignKey(Musico, on_delete=models.CASCADE, related_name="invitacionesRecibidas")
    banda = models.ForeignKey(Banda, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=40,
        choices=[(estado, estado.value) for estado in EstadoInvitacion]
    )