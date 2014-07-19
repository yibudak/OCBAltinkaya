# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2008 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _

class product_pricelist(osv.osv):
    _inherit = 'product.pricelist'

    _columns ={
        'visible_discount': fields.boolean('Visible Discount'),
    }
    _defaults = {
         'visible_discount': True,
    }

product_pricelist()

class sale_order_line(osv.osv):
    _inherit = "sale.order.line"

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False, context=None):

        def get_real_price(res_dict, product_id, qty, uom, pricelist):
            product_obj = self.pool.get('product.product')
            currency_obj = self.pool.get('res.currency')
            item_obj = self.pool.get('product.pricelist.item')
            price_type_obj = self.pool.get('product.price.type')
            pricelist_obj = self.pool.get('product.pricelist')
            price = res_dict.get(pricelist, False)
            
            if res_dict.get('item_id',False) and res_dict['item_id'].get(pricelist,False):
                item = res_dict['item_id'].get(pricelist,False)
                item_base = item_obj.browse(cr, uid, item, context=context)
                pricelist_currency = pricelist_obj.browse(cr, uid, pricelist, context=context).currency_id
                if item_base.base == -1:
                    base_pricelist = item_base.base_pricelist_id.id
                    if not base_pricelist:
                        price = 0.0
                    else:
                         price_tmp = pricelist_obj.price_get(cr, uid,
                                     [base_pricelist], product_id,
                                     qty, context=context)[base_pricelist]
                         ptype_src = pricelist_obj.browse(cr, uid, base_pricelist, context=context).currency_id.id
                         price = currency_obj.compute(cr, uid,
                                 ptype_src, pricelist_currency.id,
                                 price_tmp, round=False, context=context)
            elif item_base.base > 0:
                price_type = price_type_obj.browse(cr, uid, item_base.base)
                price = currency_obj.compute(cr, uid,
                        price_type.currency_id.id, pricelist_currency.id,
                        product_obj.price_get(cr, uid, [product_id],price_type.field, context=context)[product_id],
                        round=False, context=context)
            factor = 1.0
            if uom and uom != product.uom_id.id:
                product_uom_obj = self.pool.get('product.uom')
                uom_data = product_uom_obj.browse(cr, uid,  product.uom_id.id)
                factor = uom_data.factor

            return price * factor
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty, uom, qty_uos, uos,
                                                             name, partner_id, lang, update_tax, date_order, packaging=packaging, 
                                                             fiscal_position=fiscal_position, flag=flag, context=context)
        context = {'lang': lang, 'partner_id': partner_id}
        result = res['value']
        pricelist_obj = self.pool.get('product.pricelist')
        product_obj = self.pool.get('product.product')
        if product:
            if result.get('price_unit',False):
                price = result['price_unit']
            else:
                return res

            product = product_obj.browse(cr, uid, product, context=context)
            list_price = pricelist_obj.price_get(cr, uid, [pricelist],
                    product.id, qty or 1.0, partner_id, {'uom': uom,'date': date_order })

            pricelists = pricelist_obj.read(cr, uid, [pricelist], ['visible_discount'], context=context)

            new_list_price = get_real_price(list_price, product.id, qty, uom, pricelist)
            if len(pricelists)>0 and pricelists[0]['visible_discount'] and list_price[pricelist] != 0 and new_list_price != 0:
                discount = (new_list_price - price) / new_list_price * 100
                if discount > 0:
                    result['price_unit'] = new_list_price
                    result['discount'] = discount
                else:
                    result['discount'] = 0.0
            else:
                result['discount'] = 0.0
        return res
