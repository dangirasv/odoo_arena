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
    mana = fields.Integer("Mana Points", default=100)
    mindamage = fields.Integer("Minimum Damage", default=8)
    maxdamage = fields.Integer("Max Damage", default=12)
    image = fields.Binary("Image")
    level = fields.Integer("Character Level", default=1)


class odooarena_player(models.Model):
    _name = 'odooarena.player'
    _inherit = 'odooarena.character'

    image = fields.Binary("Image")
    name = fields.Char("Character Name", default="Player")
    creator_id = fields.Many2one('res.users', ondelete='set null', string="Character Creator ID", index=True,
                                 default=lambda self: self.env.user)


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
    fighter_hp = fields.Integer("Fighter Health Points")
    fighter_mana = fields.Integer("Fighter Mana Points")
    fighter_image = fields.Binary("Fighter Image")
    fighter_mindamage = fields.Integer("Fighter Minimum Damage")
    fighter_maxdamage = fields.Integer("Fighter Max Damage")
    started = fields.Boolean("Has combat started?", default=False)

    player_name = fields.Char("Player Name")
    player_hp = fields.Integer("Player Health Points")
    player_mana = fields.Integer("Player Mana Points")
    player_image = fields.Binary("Player Image")
    player_mindamage = fields.Integer("Minimum Damage")
    player_maxdamage = fields.Integer("Max Damage")

    def prepare_fight(self):
        fighter = self.env['odooarena.fighter'].search([('fighting', '=', True)])
        player = self.env['odooarena.player'].search([('creator_id', '=', self.env.user.id)])
        if not player:
            raise Warning("You're dead! Please go to menu Game->Your Character to create a new character first.")
        else:
            self.write({'fighter_name': fighter.name, 'fighter_hp': fighter.maxhp, 'fighter_mana': fighter.mana,
                        'fighter_image': fighter.image, 'started': True, 'fighter_mindamage': fighter.mindamage,
                        'fighter_maxdamage': fighter.maxdamage, 'player_name': player.name, 'player_hp': player.maxhp,
                        'player_mana': player.mana, 'player_image': player.image, 'player_mindamage': player.mindamage,
                        'player_maxdamage': player.maxdamage, 'combat_log': ""})

    def attack(self):
        if not self.env['odooarena.player'].search([('creator_id', '=', self.env.user.id)]):
            self.started = False
            # raise Warning("Please create a new character to fight first.")
        else:
            player_damage = randint(self.player_mindamage, self.player_maxdamage)
            log = (player_damage, "Player has dealt %d damage to the fighter." % player_damage)
            self.fighter_reactions_and_log(log)
            self.death_checks()

    def fighter_reactions_and_log(self, log):
        info_list = [log, self.fighter_attack()]
        self.write({'fighter_hp': self.fighter_hp - info_list[0][0], 'player_hp': self.player_hp - info_list[1][0],
                    'combat_log': info_list[0][1] + info_list[1][1]})

    def fighter_attack(self):
        fighter_damage = randint(self.fighter_mindamage, self.fighter_maxdamage)
        log = (fighter_damage, "\nFighter has dealt %d damage back." % fighter_damage)
        return log

    @api.multi
    def death_checks(self):
        if self.fighter_hp <= 0:
            self.player_won()
        elif self.player_hp <= 0:
            self.player_lost()

    def player_won(self):
        player = self.env['odooarena.player'].search([('creator_id', '=', self.env.user.id)])
        fighter = self.env['odooarena.fighter'].search([('fighting', '=', True)])
        fighter.fighting = False
        next_fighter = self.env['odooarena.fighter'].search([('id', '=', fighter.id+1)])
        try:
            next_fighter.fighting = True
        except ValueError:
            self.env['odooarena.fighter'].search([('id', '=', 1)]).fighting = True
            raise Warning("Congratulations! You've beaten all Arena fighters! You can run the gauntlet again with your"
                          " overpowered character or create a new character")
        # self.search([('fighter_hp', '<=', 0)]).unlink()
        player.level += 1
        self.started = False

    @api.multi
    def player_lost(self):
        fighter = self.env['odooarena.fighter'].search([('fighting', '=', True)])
        fighter.fighting = False
        self.env['odooarena.fighter'].search([('id', '=', 1)]).fighting = True
        self.env['odooarena.player'].search([('creator_id', '=', self.env.user.id)]).unlink()
        # self.search([('player_hp', '<=', 0)]).unlink()
        # self.started = False

    @api.multi
    def return_to_title(self):
        # action = self.env.ref('odooarena.action_player').read()[0]
        # return action
        # action_id = self.env.ref('odooarena.player_lost')
        return {
            'name': "Create Another Character",
            # 'type': 'ir.actions.act_window',
            'res_model': 'odooarena.player',
            'view_mode': 'list,form',
            'domain': "[('creator_id', '=', uid)]",
        }
