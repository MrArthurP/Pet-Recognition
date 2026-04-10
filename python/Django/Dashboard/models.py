from django.db import models
from django.utils.text import slugify
import os

def cachorro_directory_path(instance, filename):
    # Exemplo: imagens/cachorros/<id_do_cachorro>/<nome_da_imagem>
    return os.path.join('fotos_cachorros', instance.cachorro.nome, filename)


class Cachorro(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nome

class Foto(models.Model):
    cachorro = models.ForeignKey(Cachorro, related_name="fotos", on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to=cachorro_directory_path, null=True, blank=True)

    class Meta:
        db_table = 'Dashboard_foto'  # Nome da tabela no banco de dados

    def __str__(self):
        return f"Foto do {self.cachorro.nome}"



class EstadoBotao(models.Model):
    estado1 = models.BooleanField(default=False)  # ou True, dependendo do seu uso
    nivel = models.IntegerField(default=0)




# from django.db import models
# from django.utils.text import slugify
# import os

# def cachorro_directory_path(instance, filename):
#     nome_slug = slugify(instance.cachorro.nome)
#     return os.path.join('foto', nome_slug, filename)

# class Cachorro(models.Model):
#     nome = models.CharField(max_length=100)
#     data_nascimento = models.DateField()
#     peso = models.DecimalField(max_digits=5, decimal_places=2)
#     altura = models.DecimalField(max_digits=5, decimal_places=1)
#     foto = models.ImageField(upload_to='foto/', blank=True, null=True)

#     def __str__(self):
#         return self.nome

    


