from modules.base_module import BaseModule


class FcqCardModule(BaseModule):
    fcq_ids = []

    def render(self, fcq_ids, color):
        self.fcq_ids = fcq_ids
        self.fcq_ids.reverse()
        chunks = [self.fcq_ids[x:x + 6]
                  for x in range(0, len(self.fcq_ids), 6)]
        return self.render_string(
            'modules/FcqCollection.html', chunks=chunks, fcq_ids=fcq_ids, fcq_title=self.fcq_title, convert_date=self.convert_date, color=color)

    def embedded_javascript(self):
        javascript = ""
        for fcq_id in self.fcq_ids:
            javascript += '''
            $("#card-{0}").one( "click", function(){{
                $( "#body-{0}" ).load( "/ajax/fcqcard/{0}", function(){{
                    $( "#nav-{0} :not(.disabled) a").click(function (e) {{
                        e.preventDefault();
                        $(this).tab('show');
                        console.log(e);
                    }});
                }});
            }});
            '''.format(fcq_id)
        return javascript
