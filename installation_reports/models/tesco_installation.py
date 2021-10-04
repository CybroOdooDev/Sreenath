# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class TescoInstallation(models.Model):
    _name = 'tesco.installation'

    issue_date = fields.Date(string='Date')
    install_type = fields.Char(string='Install Type')

    company_name = fields.Many2one('res.partner', string='Company Name')
    company_sector = fields.Char(string='Company Sector')
    company_no = fields.Char(string='Company Number', related='company_name.phone')
    company_email = fields.Char(string='Company Number', related='company_name.email')

    vrn = fields.Char('VRN')
    odometer_reading = fields.Char('Odometer Reading')
    vehicle_type = fields.Char('Vehicle Type')
    make = fields.Char('Make')
    vehicle_model = fields.Char('Vehicle Model')
    vehicle_year = fields.Char('Vehicle Year')
    full_vin_no = fields.Char('Fill VIN NO')
    trailer_make = fields.Char('Trailer Make')
    trailer_no = fields.Char('Trailer No')

    installation_address = fields.Char('Installation Address')
    time_started = fields.Char('Time Started')
    time_finished = fields.Char('Time Finished')
    commissioning_number = fields.Char('Commissioning Number')
    serial_number = fields.Char('Serial Number')

    vehicle_headlights = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], 'Vehicle Headlights')
    post_vehicle_headlights = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], 'Vehicle Headlights')
    eml_light = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], 'EML Light')

    post_eml_light = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], 'EML Light')

    damage_to_vehicle = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], 'Damage to vehicle')
    post_damage_to_vehicle = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], 'Damage to vehicle')

    cigarette_lighter = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], 'Cigarette Lighter')
    post_cigarette_lighter = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], 'Cigarette Lighter')

    photos_taken = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], 'Photo Taken')
    post_photos_taken = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], 'Photo Taken')

    is_kit_warranty = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], 'Is kit in Warranty?')

    job_description = fields.Char('Job Description')
    comments = fields.Char('Comments')
    post_comments = fields.Char('Comments')
    additional_installation_notes = fields.Html('Additional Installation notes')

    length = fields.Char('Length')
    height = fields.Char('Height')
    width = fields.Char('Width')

    had_devices_tampered = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], default='no', string='Had devices been tampered with?')

    if_yes_devices_tampered = fields.Text('If Yes, please describe')

    were_devices_faulty = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], default='no', string='Were devices faulty? ')

    warning_sticker = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], default='no', string='Did you fit a VisionTrack Warning Sticker? ')

    if_yes_devices_faulty = fields.Text('If Yes, please describe')

    equipment_used = fields.One2many('equipment.used', 'tesco_id', string='Equipment Used')

    attachment_ids = fields.Many2many(
        'ir.attachment', 'survey_mail_compose_message_ir_attachments_rel', 'wizard_id', 'attachment_id',
        string='Attachments')


class EquipmentUsed(models.Model):
    _name = 'equipment.used'

    tesco_id = fields.Many2one('tesco.installation')

    model_no = fields.Char('Model Number')
    description = fields.Char('Description')
    serial_no = fields.Char('DRID or Serial Number')
    quantity = fields.Float('Quantity')
    bootstock = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], default='no', string='Bootstock?')
    chargeable =fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], default='no', string='Chargeable?')