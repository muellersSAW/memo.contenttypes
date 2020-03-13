from Products.Five.browser import BrowserView

class ManuscriptView(BrowserView):

    def the_title(self):
        return u'Lets see'