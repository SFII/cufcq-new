from modules.base_module import BaseModule
import tornado.web


class FcqCardModule(BaseModule):

    def render(self, fcq_id):
        return '''
        <div class="card panel">
            <div class="card-head card-head-sm collapsed" data-toggle="collapse" data-parent="#{0}" data-target="#{0}" aria-expanded="false">
                <header id="header-{0}">{0}</header>
                <div class="tools">
                    <a class="btn btn-icon-toggle"><i class="fa fa-angle-down"></i></a>
                </div>
            </div>
            <div id="{0}" class="collapse" aria-expanded="false" style="height: 0px;">
              <div class="card-body"><p>{0}</p>
              </div>
            </div>
        </div>
        '''.format(fcq_id)

    def embedded_javascript(self):
        return '''
        '''
