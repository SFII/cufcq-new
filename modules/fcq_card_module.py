from modules.base_module import BaseModule
import tornado.web


class FcqCardModule(BaseModule):
    fcq_ids = []

    def render(self, fcq_ids):
        self.fcq_ids = fcq_ids
        chunks = [self.fcq_ids[x:x+7] for x in range(0, len(self.fcq_ids), 7)]
        return self.render_string('modules/fcqcard.html', chunks=chunks, fcq_ids=fcq_ids, fcq_title=self.fcq_title)

    def embedded_javascript(self):
        javascript = ""
        for fcq_id in self.fcq_ids:
            javascript += '''
            $("#card-{0}").one( "click", function(){{
                $.ajax({{
                    type: "GET",
                    url: "/ajax/fcqcard/{0}",
                    success: function(data, status) {{
                        $("#body-{0}").html(data);
                    }},
                    error: function() {{
                        console.log("AJAX ERROR: {0} could not be loaded.");
                    }}
                }})
            }});
            '''.format(fcq_id)
        return javascript
