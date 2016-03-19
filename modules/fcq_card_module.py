from modules.base_module import BaseModule
import tornado.web


class FcqCardModule(BaseModule):
    fcq_ids = []

    def render(self, fcq_ids):
        self.fcq_ids = fcq_ids
        return self.render_string('modules/fcqcard.html', fcq_ids=fcq_ids, fcq_title=self.fcq_title)

    def embedded_javascript(self):
        javascript = ""
        for fcq_id in self.fcq_ids:
            javascript += '''
            $("#header-{0}").one( "click", function(){{
                $( "#body-{0}" ).load( "/ajax/fcqcard/{0}");
            }});
            '''.format(fcq_id)
        return javascript
