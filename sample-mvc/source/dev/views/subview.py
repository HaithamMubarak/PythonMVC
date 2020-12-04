from dev.views.appview import AppView


class SubView(AppView):
    def __init__(self, data):
        super(SubView, self).__init__(data=data)