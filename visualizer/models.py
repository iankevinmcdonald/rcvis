from django.contrib import admin
from django.db import models
from django.utils.text import slugify
from django.db import models

class JsonConfig(models.Model):
    detail_views = ('visualizer.views.Visualize',)

    jsonFile = models.FileField()
    slug = models.SlugField(unique=True)
    uploadedAt = models.DateTimeField(auto_now_add=True)

    # Options modifiable at upload or runtime
    rotateNames = models.BooleanField(default=True)
    horizontalSankey = models.BooleanField(default=False)
    onlyShowWinnersTabular = models.BooleanField(default=True)
    doHideOverflowAndEliminated = models.BooleanField(default=False)
    doUseHorizontalBarGraph = models.BooleanField(default=False)
    hideSankey = models.BooleanField(default=False)
    hideTabular = models.BooleanField(default=False)

    # Options only modifiable at upload time
    excludeFinalWinnerAndEliminatedCandidate = models.BooleanField(default=False)
    hideDecimals = models.BooleanField(default=False)

    def _get_unique_slug(self):
        slug = slugify(self.jsonFile)
        unique_slug = slug
        num = 1
        while JsonConfig.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

@admin.register(JsonConfig)
class JsonAdmin(admin.ModelAdmin):
  list_display = ('slug', 'uploadedAt')
