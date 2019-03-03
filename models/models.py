# -*- coding: utf-8 -*-

from odoo import models, fields, api


class odooarena_character(models.Model):
    _name = 'odooarena.character'
    _description = 'basic class to hold character info'

    name = fields.Char("Character Name")
    maxhp = fields.Integer("Max Health Points", default=100)
    currenthp = fields.Integer("Current Health Points", default=100)
    mindamage = fields.Integer("Minimum Damage", default=8)
    maxdamage = fields.Integer("Max Damage", default=12)
    image = fields.Binary("Image")
    level = fields.Integer("Character Level")


class odooarena_player(models.Model):
    _name = 'odooarena.player'
    _inherit = 'odooarena.character'


class odooarena_fighter(models.Model):
    _name = 'odooarena.fighter'
    _inherit = 'odooarena.character'

    alive = fields.Boolean("Alive", default=True)
    fighting = fields.Boolean("Active Fighter", default=False)
    bio = fields.Text("Fighter Background")


class odooarena_arena(models.Model):
    _name = 'odooarena.arena'
    _description = 'main class where the battle happens'

    combat_log = fields.Text("Combat Log")
    fighter_name = fields.Char("Fighter Name")
    fighter_hp = fields.Integer("Fighter Health Points", default=100)
    fighter_image = fields.Binary("Fighter Image")

    def prepare_fight(self):
        fighter = self.env['odooarena.fighter'].search([('fighting', '=', True)])
        self.fighter_name = fighter.name
        self.fighter_hp = fighter.maxhp
        self.fighter_image = fighter.image



