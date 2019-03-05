# -*- coding: utf-8 -*-

from odoo import models, fields, api
from random import randint
from odoo.exceptions import Warning


class odooarena_character(models.Model):
    _name = 'odooarena.character'
    _description = 'basic class to hold character info'

    name = fields.Char("Character Name")
    maxhp = fields.Integer("Max Health Points", default=100)
    currenthp = fields.Integer("Current Health Points", default=100)
    mindamage = fields.Integer("Minimum Damage", default=8)
    maxdamage = fields.Integer("Max Damage", default=12)
    image = fields.Binary("Image")
    level = fields.Integer("Character Level", default=1)


class odooarena_player(models.Model):
    _name = 'odooarena.player'
    _inherit = 'odooarena.character'

    image = fields.Binary("Image")


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
    fighter_mindamage = fields.Integer("Fighter Minimum Damage")
    fighter_maxdamage = fields.Integer("Fighter Max Damage")
    started = fields.Boolean("Has combat started?", default=False)

    player_name = fields.Char("Player Name")
    player_hp = fields.Integer("Player Health Points", default=100)
    player_image = fields.Binary("Player Image")
    player_mindamage = fields.Integer("Minimum Damage")
    player_maxdamage = fields.Integer("Max Damage")

    def prepare_fight(self):
        fighter = self.env['odooarena.fighter'].search([('fighting', '=', True)])
        player = self.env['odooarena.player'].search([('id', '=', 1)])
        self.fighter_name = fighter.name
        self.fighter_hp = fighter.maxhp
        self.fighter_image = fighter.image
        self.started = True
        self.fighter_mindamage = fighter.mindamage
        self.fighter_maxdamage = fighter.maxdamage
        self.player_name = player.name
        self.player_hp = player.maxhp
        self.player_image = player.image
        self.player_mindamage = player.mindamage
        self.player_maxdamage = player.maxdamage

        self.write({'fighter_name': self.fighter_name, 'fighter_hp': self.fighter_hp,
                    'fighter_image': self.fighter_image, 'started': self.started,
                    'fighter_mindamage': self.fighter_mindamage, 'fighter_maxdamage': self.fighter_maxdamage,
                    'player_name': self.player_name, 'player_hp': self.player_hp, 'player_image': self.player_image,
                    'player_mindamage': self.player_mindamage, 'player_maxdamage': self.player_maxdamage})

    def attack(self):
        player_damage = randint(self.player_mindamage, self.player_maxdamage)
        self.fighter_hp -= player_damage
        log = "Player has dealt %d damage to the fighter." % player_damage
        log = self.fighter_attack(log)
        self.write({'fighter_hp': self.fighter_hp, 'player_hp': self.player_hp, 'combat_log': log})
        self.death_checks()

    def fighter_attack(self, log):
        fighter_damage = randint(self.fighter_mindamage, self.fighter_maxdamage)
        self.player_hp -= fighter_damage
        log += "\nFighter has dealt %d damage back." % fighter_damage
        return log

    def death_checks(self):
        if self.fighter_hp <= 0:
            self.player_won()
        elif self.player_hp <= 0:
            self.player_lost()

    def player_won(self):
        fighter = self.env['odooarena.fighter'].search([('fighting', '=', True)])
        fighter.fighting = False
        next_fighter = self.env['odooarena.fighter'].search([('id', '=', fighter.id+1)])
        try:
            next_fighter.fighting = True
        except ValueError:
            self.env['odooarena.fighter'].search([('id', '=', 1)]).fighting = True
            raise Warning("Congratulations! You've beaten all Arena fighters! You can run the gauntlet again with your"
                          " overpowered character or create a new character")
        self.search([('fighter_hp', '<=', 0)]).unlink()

    def player_lost(self):
        fighter = self.env['odooarena.fighter'].search([('fighting', '=', True)])
        fighter.fighting = False
        self.env['odooarena.fighter'].search([('id', '=', 1)]).fighting = True
        self.env['odooarena.player'].search([('id', '=', 1)]).unlink()
        self.search([('player_hp', '<=', 0)]).unlink()

