from django.test.runner import DiscoverRunner
from colour_runner.django_runner import ColourRunnerMixin

class ColourRunner(ColourRunnerMixin, DiscoverRunner):
    pass

