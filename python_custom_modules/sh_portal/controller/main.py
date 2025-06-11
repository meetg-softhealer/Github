from odoo import models,fields,api,_,http #type:ignore
from odoo.http import request, Controller, route #type:ignore
from odoo.addons.portal.controllers import portal #type:ignore
from odoo.exceptions import AccessError, MissingError #type:ignore

class ShPortalController(portal.CustomerPortal):
    
    
    def _prepare_home_portal_values(self, counters):
        vals = super(ShPortalController, self)._prepare_home_portal_values(counters)
        vals["sh_portal_count"] = request.env['sh.portal'].search_count([('sh_partner_id','=',request.env.user.partner_id.id)])
        print("\n\n\n vals", vals)
        return vals
        

    @http.route("/my/sh_portal", type="http", auth="user", website=True)
    def sh_portal_documents(self, page=1):
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
            'page_name':'ShPortal',
            'pager':pager_values,
            'default_url':url,
            'documents':documents
        })
    
    @http.route("/my/sh_portal/<int:doc_id>", type="http", auth="user", website=True)
    def sh_portal_document(self, doc_id, access_token=None):

        try:
            order_sudo = self._document_check_access('sh.portal', doc_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        return request.render("sh_portal.sh_portal_document", {'document':order_sudo})