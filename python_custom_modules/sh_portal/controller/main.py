from odoo import models,fields,api,_,http #type:ignore
from odoo.http import request, Controller, route #type:ignore
from odoo.addons.portal.controllers import portal

class ShPortalController(portal.CustomerPortal):
    
    
    def _prepare_home_portal_values(self, counters):
        vals = super(ShPortalController, self)._prepare_home_portal_values(counters)
        vals["sh_portal_count"] = request.env['sh.portal'].search_count([('sh_partner_id','=',request.env.user.partner_id.id)])
        print("\n\n\n vals", vals)
        return vals
        

    @http.route("/my/sh_portal", type="http", auth="user", website=True)
    def sh_portal(self, page=1):
        documents = request.env['sh.portal'].search([('sh_partner_id','=',request.env.user.partner_id.id)])

        url = "/my/sh_portal"
        pager_values = portal.pager(
            url = url,
            total = len(documents),
            page = page,
            step = self._items_per_page,
            url_args = {}
        )

        return request.render("sh_portal.sh_portal_documents", {
            'page_name':'MyPortal',
            'pager':pager_values,
            'default_url':url,
            'documents':documents
        })