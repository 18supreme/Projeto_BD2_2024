from djongo import models

class UnidadeCurricular(models.Model):
    id = models.IntegerField(primary_key=True)
    des = models.CharField(max_length=255)
    sem = models.IntegerField()
    ano = models.IntegerField()
    ht = models.IntegerField()

    class Meta:
        verbose_name_plural = "Unidades Curriculares"

class Curso(models.Model):
    nome = models.CharField(max_length=255)
    tipo_curso = models.IntegerField()
    apresent = models.TextField()
    said_prof = models.TextField()
    planocur = models.JSONField()  # JSONField para armazenar o plano curricular
    avqual = models.JSONField(default=list)  # Usando JSONField para armazenar uma lista de avaliações
    outr_inf = models.JSONField(default=dict)  # Outras informações como dicionário

    def __str__(self):
        return self.nome