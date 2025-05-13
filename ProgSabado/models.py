from django.db import models
from django.contrib.auth.models import User  # Importa o modelo padrão de usuário do Django


class Programacao(models.Model):
    data = models.DateField()
    anciao_do_dia = models.ForeignKey(
        User,  # Modelo de usuário
        on_delete=models.SET_NULL,  # Se o usuário for excluído, o campo ficará como NULL
        null=True,  # Permite que o valor seja NULL no banco de dados
        blank=True,  # Permite que o campo seja deixado vazio no formulário
        related_name='programacoes',  # Relacionamento reverso
        verbose_name='Ancião do Dia'  # Nome visível no admin
    )

    def __str__(self):
        return self.data.strftime('%d/%m/%Y')  # Formato brasileiro de data


class ProgDetail(models.Model):
    ordem = models.PositiveIntegerField()  # Ordem gerada automaticamente
    momento = models.CharField(max_length=100)  # Limita 'momento' para 30 caracteres
    detalhe = models.CharField(max_length=50, blank=True, null=True)  # Limita 'detalhe' para 30 caracteres
    obs = models.CharField(max_length=50, blank=True, null=True)  # Observação opcional, limitada a 30 caracteres
    programacao = models.ForeignKey(Programacao, on_delete=models.CASCADE, related_name="detalhes")

    def save(self, *args, **kwargs):
        if not self.pk:  # Apenas se for um novo registro
            if not self.ordem:  # Garante que a ordem seja preenchida automaticamente
                max_ordem = ProgDetail.objects.filter(programacao=self.programacao).aggregate(models.Max('ordem'))[
                    'ordem__max']
                self.ordem = 1 if max_ordem is None else max_ordem + 1
        super().save(*args, **kwargs)

        return f"Ordem {self.ordem} - {self.momento} - {self.detalhe}"
