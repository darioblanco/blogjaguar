from django.conf.urls.defaults import patterns

urlpatterns = patterns(
    'pygmentize',
    (r'^static/css/pygments.css$', 'pygmentizer.get_css'),
)
