from modules.base_module import BaseModule


class FcqCardModule(BaseModule):
    fcq_ids = []

    def render(self, fcq_ids):
        self.fcq_ids = fcq_ids
        chunks = [self.fcq_ids[x:x + 7]
                  for x in range(0, len(self.fcq_ids), 7)]
        return self.render_string(
            'modules/FcqCollection.html', chunks=chunks, fcq_ids=fcq_ids, fcq_title=self.fcq_title)

    def embedded_javascript(self):
        javascript = ""
        for fcq_id in self.fcq_ids:
            javascript += '''
            $("#card-{0}").one( "click", function(){{
                $( "#body-{0}" ).load( "/ajax/fcqcard/{0}");
                $(document).ready(function(){{
                    $('ul.tabs').tabs();
                    console.log("{0}");
                }});
            }});
            '''.format(fcq_id)
        return javascript
