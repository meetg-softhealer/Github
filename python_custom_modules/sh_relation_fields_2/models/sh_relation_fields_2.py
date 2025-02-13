# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import models,fields,api # type: ignore

class Partner(models.Model):
    _name = "sh.res.partner"
    _decription = "Partner Table"

    name = fields.Char("Partner Name")
    city = fields.Char("City")

class Product(models.Model):
    _name = "sh.product.product"
    _decription = "Product Table"

    name = fields.Char("Product Name")

class Account(models.Model):
    _name = "sh.account.tax"
    _decription = "Account Table"

    name = fields.Char("Tax Name")

class Sale_Order(models.Model):
    _name = "sh.sale.order"
    _decription = "Sale Order Table"

    name = fields.Char("Order Reference")
    date = fields.Date("Date")
    partner_id = fields.Many2one("sh.res.partner", string="Partner")
    order_line_ids = fields.One2many("sh.sale.order.line", "order_line_id", string="Order Lines")

class Sale_Order_Line(models.Model):
    _name = "sh.sale.order.line"
    _decription = "Sale Order Line Table"

    name = fields.Char("Sale Order Line Name")
    product_id = fields.Many2one("sh.product.product", string="Product")
    qty = fields.Integer("Quantity")
    price = fields.Float("Price")
    tax_ids = fields.Many2many("sh.account.tax", string="Taxes")
    order_line_id = fields.Many2one("sh.sale.order", string="Order Line")


