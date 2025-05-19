# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_ #type:ignore
from odoo.exceptions import UserError, ValidationError #type:ignore


class ShCalendarEventInherit(models.Model):
    _inherit = "calendar.event"

    sh_presenter = fields.Many2one("res.users", string="Presenter")
    sh_facilitator = fields.Many2one("res.partner", string="Facilitator")
    sh_note_taker = fields.Many2one("res.users", string="Note Taker")
    sh_time_keeper = fields.Many2one("res.users", string="Time Keeper")

    sh_agenda_topics = fields.Text("Agenda Topic")
    sh_action_items = fields.Text("Action Items")
    sh_conclusion = fields.Text("Conclusion")

    
