from django.db import models


EDL_TYPE_CHOICES = [
    ('url', 'URL'),
    ('fqdn', 'FQDN'),
    ('ip_address', 'IP Address')
]


class Edl(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    edl_type = models.CharField(max_length=20, choices=EDL_TYPE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "External Dynamic List"
        verbose_name_plural = "External Dynamic Lists"

    def __str__(self):
        return f'{self.name}'.lower()


class EdlEntry(models.Model):
    edl = models.ForeignKey(Edl, on_delete=models.CASCADE, related_name='entries')
    entry_value = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(default=None)

    class Meta:
        verbose_name = "External Dynamic List Entry"
        verbose_name_plural = "External Dynamic Entries"


    def __str__(self):
        return f'{self.edl.name} {self.entry_value}'.lower()

class EdlLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    performed_by = models.CharField(max_length=50)
    edl_name =  models.CharField(max_length=50, unique=False)
    edl_entry =  models.CharField(max_length=200, unique=False, null=True)
    action = models.CharField(max_length=20)
    log_message = models.CharField(max_length=200, unique=False, null=True)


    class Meta:
        verbose_name = "External Dynamic List Log"
        verbose_name_plural = "External Dynamic Logs"

    # def __str__(self):
    #     return f'{self.edl.name} {self.entry_value}'.lower()