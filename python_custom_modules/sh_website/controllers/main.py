from odoo import models,fields,api,_ #type:ignore
from odoo.http import request, Controller, route #type:ignore


class WebFormController(Controller):
    @route('/webform', auth='public', website=True)
    def web_form(self, **kwargs):
        salesperson_recs = request.env['res.users'].search([("share","=",False)])
        return request.render('sh_website.web_form_template',{'salesperson_recs':salesperson_recs})
    
    
    @route('/webform/submit', type='http', auth='public', website=True, methods=['GET','POST'])
    def web_form_submit(self, **post):
        request.env['res.partner'].sudo().create({
                    'name': post.get('name'),
                    'phone': post.get('phone'),
                    'email': post.get('email'),  
                    'user_id':post.get('user_id')              
                })
        return request.redirect('/thank-you-page')
