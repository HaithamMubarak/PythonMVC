from mvc.view.base import DefaultView
import os


class AppView(DefaultView):

    TEMPLATES_DIR = '%s/%s' % (os.path.dirname(os.path.realpath(__file__)), 'templates')

    def __init__(self, templateName=None, data={}):
        if templateName is None or len(str(templateName)) == 0:
            templateName = self.__class__.__name__
        super().__init__('%s/%s.html' % (self.TEMPLATES_DIR, templateName), data)

    """
    This method will be called to evaluate the template files into string contents.
    So changing the methid impl, will customize the template processing
    """
    def process(self, templatestring):
        return super(AppView, self).process(templatestring)