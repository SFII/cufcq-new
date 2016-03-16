from modules.base_module import BaseModule
import tornado.web


class FcqCardModule(BaseModule):
    fcq_ids = []

    def render(self, fcq_id):
        self.fcq_ids.append(fcq_id)

        return '''
        <div class="card panel">
            <div class="card-head card-head-sm collapsed" data-toggle="collapse" data-parent="#{0}" data-target="#{0}" aria-expanded="false">
                <header id="header-{0}">{1}</header>
                <div class="tools">
                    <a class="btn btn-icon-toggle"><i class="fa fa-angle-down"></i></a>
                </div>
            </div>
            <div id="{0}" class="collapse" aria-expanded="false" style="height: 0px;">
              <div id="body-{0}" class="card-body"><p><i>loading...</i></p>
              </div>
            </div>
        </div>
        '''.format(fcq_id, self.fcq_title(fcq_id))

    def embedded_javascript(self):
        javascript = ""
        for fcq_id in self.fcq_ids:
            javascript += '''
            $("#header-{0}").one( "click", function(){{
                $.ajax({{
                    type: "GET",
                    url: "/api/fcq/{0}",
                    success: function(data, status) {{
                        $("#body-{0}").html(JSON.stringify(data));
                    }},
                    error: function() {{
                        console.log("AJAX ERROR: {0} could not be loaded.");
                    }}
                }})
            }});
            '''.format(fcq_id)
        return javascript
