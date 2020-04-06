# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class vit_auto_int_transfer(models.Model):
	_inherit = 'stock.picking.type'

	picking_type_internal_id = fields.Many2one(string='Picking Type Internal',comodel_name='stock.picking.type')



class ValidateTranfer(models.Model):
	_inherit ='stock.picking'



	@api.multi
	def button_validate(self):
		res = super(ValidateTranfer, self).button_validate()
		# import pdb;pdb.set_trace()
		if self.picking_type_id.code == 'incoming':
			for picking in self:
				if self.origin:
					origin = self.origin
				else :
					origin = " "
				pass

				picking_copy = picking.create({
					'move_type' : picking.move_type,
					'state' : 'draft',
					'scheduled_date' : picking.scheduled_date,
					'date' : picking.date,
					'date_done' : picking.date_done,
					'printed' : picking.printed,
					'is_locked' : picking.is_locked,
					'immediate_transfer' : picking.immediate_transfer,
					'kode_cara_angkut' : picking.kode_cara_angkut,
					'has_export' : picking.has_export,
					'freight' : picking.freight,
					'is_bea_cukai' : picking.is_bea_cukai,
					'has_export_aju' : picking.has_export_aju,
					'is_subcontracting' : picking.is_subcontracting,


					'partner_id' : picking.partner_id.id,
					'department_id' : picking.department_id.id,
					'location_dest_id' : picking.location_dest_id.id,
					'no_sj_pengirim' : picking.no_sj_pengirim,
					'company_id' : picking.company_id.id,
					'invoice_id' : picking.invoice_id.id,
					'note' : picking.note,
					'nomor_aju_id' : picking.nomor_aju_id.id,
					'tgl_ttd' : picking.tgl_ttd,
					'tgl_dokumen' : picking.tgl_dokumen,

					'picking_type_id' : picking.picking_type_id.picking_type_internal_id.id,
					'origin' : origin + ' | ' + picking.name,
					'location_id' : picking.picking_type_id.picking_type_internal_id.default_location_src_id.id,
					'location_dest_id' : picking.picking_type_id.picking_type_internal_id.default_location_dest_id.id,
					'move_ids_without_package' : [(0,0,{
						'location_id' : obj.location_id.id,
						'location_dest_id' : obj.location_dest_id.id,
						'name' : obj.name,
						'product_id' : obj.product_id.id,
						'production_subcon_id' : obj.production_subcon_id.id,
						'product_uom_qty' : obj.quantity_done,
						# 'quantity_done' : obj.quantity_done,
						'product_uom' : obj.product_uom.id,
						'netto' : obj.netto,
						'brutto' : obj.brutto,
						'box' : obj.box,
						'reserved_availability' : obj.reserved_availability,
						})for obj in picking.move_ids_without_package],

				

				})
				
				picking_copy.action_confirm()
				picking_copy.write({ 'group_id' : picking.group_id.id})
				picking_copy.action_assign()

				for move in picking_copy.move_ids_without_package:
					move_data = move.search([('product_id','=',move.product_id.id),('picking_id','=',picking_copy.id)])
					move_line = move.move_line_ids.search([('product_id','=',move.product_id.id),('picking_id','=',move.picking_id.id)])
					move_self = self.move_line_ids.search([('picking_id','=',self.id),('product_id','=',move.product_id.id)])
					for data in move_self:
						move_line.create({
							'product_id' : move_data.product_id.id,
							'product_uom_id' : move_data.product_id.uom_id.id,
							'qty_done' : data.qty_done,
							'location_id' : move_data.location_id.id,
							'location_dest_id' : move.location_dest_id.id,
							'move_id' : move_data.id,
							'picking_id' : move_data.picking_id.id,
							'lot_id' : data.lot_id.id,
							'result_package_id' : data.result_package_id.id,
							'package_id' : data.package_id.id,

						})

				

				for x in picking_copy.move_line_ids:
					if x.product_uom_qty == 0 and x.qty_done == 0:
						x.unlink()

				if picking_copy.picking_type_id.code != 'incoming':
					picking_copy.button_validate()
				else :
					raise UserError(_('Code On Picking Type is Vendor!!!'))


		return res