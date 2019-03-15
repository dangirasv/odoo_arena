# -*- coding: utf-8 -*-

from odoo import models, fields, api
from random import randint
from odoo.exceptions import Warning
from odoo import modules
import base64


def get_default_player_img():
    with open(modules.get_module_resource('odooarena', 'static/img', 'player.jpg'), 'rb') as f:
        return base64.b64encode(f.read())


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
    armor = fields.Integer("Armor Points", default=0)
    crit_chance = fields.Float("Critical Damage Chance", default=0.1)


class odooarena_player(models.Model):
    _name = 'odooarena.player'
    _inherit = 'odooarena.character'

    image = fields.Binary("Image", default=get_default_player_img())
    name = fields.Char("Character Name", default="Player")
    creator_id = fields.Many2one('res.users', ondelete='set null', string="Character Creator ID", index=True,
                                 default=lambda self: self.env.user)


class odooarena_fighter(models.Model):
    _name = 'odooarena.fighter'
    _inherit = 'odooarena.character'

    alive = fields.Boolean("Alive", default=True)
    fighting = fields.Boolean("Active Fighter", default=False)
    bio = fields.Text("Fighter Background")
    basic_skill = fields.Many2one('odooarena.skills', ondelete='set null', string="Primary Skill")
    ultimate_skill = fields.Many2one('odooarena.skills', ondelete='set null', string="Ultimate Skill")
    drops_item_1 = fields.Many2one('odooarena.items', ondelete='set null', string="Drops item 1")
    drops_item_2 = fields.Many2one('odooarena.items', ondelete='set null', string="Drops item 2")


class odooarena_skills(models.Model):
    _name = 'odooarena.skills'
    _description = 'stores skills used by players and fighters'

    SKILL_TYPE_LIST = [('a', 'Attack'),
                       ('d', 'Defense')]

    name = fields.Char("Skill Name")
    skill_type = fields.Selection(SKILL_TYPE_LIST, string="Skill Type", default='a')
    image = fields.Binary("Image")
    description = fields.Text("Skill Description")
    mana_cost = fields.Integer("Mana Cost")
    min_change_to_hp = fields.Integer("Minimum Changes to Target HP")
    max_change_to_hp = fields.Integer("Maximum Changes to Target HP")
    min_change_to_mana = fields.Integer("Minimum Change to Target Mana")
    max_change_to_mana = fields.Integer("Maximum Change to Target Mana")
    change_to_armor = fields.Integer("Change to Targets Armor")
    change_to_crit = fields.Float("Change to Targets Critical Chance")
    log_text = fields.Char("Skill Combat Log Text")


class odooarena_items(models.Model):
    _name = 'odooarena.items'
    _description = 'stores items that are rewarded after each win'

    name = fields.Char("Item Name")
    image = fields.Binary("Image")
    item_level = fields.Integer("Item Level")
    description = fields.Text("Item Description")
    change_to_hp = fields.Integer("Changes to HP")
    change_to_mana = fields.Integer("Change to Mana")
    change_to_armor = fields.Integer("Change to Armor")
    change_to_crit = fields.Float("Change to Critical Chance")
    change_to_damage = fields.Integer("Changes to Damage")


class odooarena_arena(models.Model):
    _name = 'odooarena.arena'
    _description = 'main class where the battle happens'

    name = fields.Char("The Fight", default="The Fight")
    combat_log = fields.Text("Combat Log")
    started = fields.Boolean("Has combat started?", default=False)
    lost = fields.Boolean("Has player lost?", default=False)
    won = fields.Boolean("Has player won?", default=False)

    fighter = fields.Many2one('odooarena.fighter', ondelete='set null', string="Active fighter")
    reward_name_1 = fields.Char(related='fighter.drops_item_1.name', string="First reward's name")
    reward_img_1 = fields.Binary(related='fighter.drops_item_1.image', string="First reward's image")
    reward_desc_1 = fields.Text(related='fighter.drops_item_1.description', string="First reward's description")
    reward_name_2 = fields.Char(related='fighter.drops_item_2.name', string="Second reward's name")
    reward_img_2 = fields.Binary(related='fighter.drops_item_2.image', string="Second reward's image")
    reward_desc_2 = fields.Text(related='fighter.drops_item_2.description', string="Second reward's description")

    fighter_name = fields.Char("Fighter Name")
    fighter_hp = fields.Integer("Fighter Health Points")
    fighter_mana = fields.Integer("Fighter Mana Points")
    fighter_image = fields.Binary("Fighter Image")
    fighter_mindamage = fields.Integer("Fighter Minimum Damage")
    fighter_maxdamage = fields.Integer("Fighter Max Damage")
    fighter_armor = fields.Integer("Fighter Armor Points")
    fighter_crit_chance = fields.Float("Critical Chance")

    player_name = fields.Char("Player Name")
    player_hp = fields.Integer("Player Health Points")
    player_mana = fields.Integer("Player Mana Points")
    player_image = fields.Binary("Player Image")
    player_mindamage = fields.Integer("Minimum Damage")
    player_maxdamage = fields.Integer("Max Damage")
    player_armor = fields.Integer("Player Armor Points")
    player_crit_chance = fields.Float("Critical Chance ")

    def prepare_fight(self):
        fighter = self.env['odooarena.fighter'].search([('fighting', '=', True)])
        player = self.env['odooarena.player'].search([('creator_id', '=', self.env.user.id)])
        self.fighter = fighter
        if not player:
            raise Warning("You're dead! Please go to Game Menu->Your Character to create a new character first.")
        else:
            self.write({
                'started': True,
                'lost': False,
                'fighter_name': fighter.name,
                'fighter_hp': fighter.maxhp,
                'fighter_mana': fighter.mana,
                'fighter_image': fighter.image,
                'fighter_mindamage': fighter.mindamage,
                'fighter_maxdamage': fighter.maxdamage,
                'fighter_armor': fighter.armor,
                'fighter_crit_chance': fighter.crit_chance,
                'player_name': player.name,
                'player_hp': player.maxhp,
                'player_mana': player.mana,
                'player_image': player.image,
                'player_mindamage': player.mindamage,
                'player_maxdamage': player.maxdamage,
                'player_armor': player.armor,
                'player_crit_chance': player.crit_chance,
                'combat_log': "",
            })

    """ PLAYER ACTIONS """

    def attack(self):
        if not self.env['odooarena.player'].search([('creator_id', '=', self.env.user.id)]) or self.player_hp <= 0:
            self.started = False
        else:
            player_damage = randint(self.player_mindamage, self.player_maxdamage) - self.fighter_armor
            combat_log = "Player has dealt %d damage to the fighter"
            player_damage, combat_log = self.update_if_player_crit(player_damage, combat_log)
            log = {
                'damage': player_damage,
                'combat_log': combat_log % player_damage,
            }
            self.fighter_reactions_and_log(log, 1)
            self.death_checks()

    def pistol_shot(self):
        if not self.env['odooarena.player'].search([('creator_id', '=', self.env.user.id)]) or self.player_hp <= 0:
            self.started = False
        elif self.player_mana < 30:
            raise Warning("You don't have enough mana to use this skill")
        else:
            self.player_mana -= 30
            skill = self.env['odooarena.skills'].search([('id', '=', 3)])
            player_damage = randint(skill.min_change_to_hp, skill.max_change_to_hp) - self.fighter_armor
            player_damage, combat_log = self.update_if_player_crit(player_damage, skill.log_text)
            log = {
                'damage': player_damage,
                'combat_log': "Player " + combat_log % player_damage,
            }
            self.fighter_reactions_and_log(log, 1)
            self.death_checks()

    def absorb(self):
        player = self.env['odooarena.player'].search([('creator_id', '=', self.env.user.id)])
        if not player or self.player_hp <= 0:
            self.started = False
        else:
            self.player_mana += 40
            log = {
                'damage': 0,
                'combat_log': "Player absorbs 50% of the damage received this turn and restores 40 mana",
            }
            self.fighter_reactions_and_log(log, 0.5)
            self.death_checks()

    def fighter_reactions_and_log(self, log, damage_modifier):
        info = {
            'player': log,
            'fighter': self.fighter_attack(damage_modifier),
        }
        self.normalise_stats()
        self.write({
            'fighter_hp': self.fighter_hp - info['player']['damage'],
            'player_hp': self.player_hp - info['fighter']['damage'],
            'combat_log': info['player']['combat_log'] + info['fighter']['combat_log'],
        })

    def update_if_player_crit(self, damage, log):
        chance = randint(1, 100)
        if chance <= self.player_crit_chance*100:
            # restoring original damage value since we want armor applied after critical hit, not before
            damage = (damage + self.fighter_armor) * 2 - self.fighter_armor
            log += " (critical damage!)"
        return damage, log

    def normalise_stats(self):
        player = self.env['odooarena.player'].search([('creator_id', '=', self.env.user.id)])
        fighter = self.env['odooarena.fighter'].search([('fighting', '=', True)])
        if self.player_mana > player.mana:
            self.player_mana = player.mana
        if self.player_mana < 0:
            self.player_mana = 0
        if self.player_crit_chance > 100:
            self.player_crit_chance = 100
        if self.player_crit_chance < 0:
            self.player_crit_chance = 0
        if self.player_armor < 0:
            self.player_armor = 0
        if self.fighter_mana > fighter.mana:
            self.fighter_mana = fighter.mana
        if self.fighter_mana < 0:
            self.fighter_mana = 0
        if self.fighter_crit_chance > 100:
            self.fighter_crit_chance = 100
        if self.fighter_crit_chance < 0:
            self.fighter_crit_chance = 0
        if self.fighter_armor < 0:
            self.fighter_armor = 0

    """ FIGHTER AI """

    def fighter_attack(self, damage_modifier):
        action_index = randint(1, 10)
        if action_index < 5:
            log = self.basic_fighter_attack(damage_modifier)
        elif action_index < 7:
            log = self.fighter_meditate()
        elif action_index < 10:
            if self.fighter_mana < self.env['odooarena.fighter'].search([('fighting', '=', True)]).basic_skill.mana_cost:
                log = self.fighter_attack(damage_modifier)
            else:
                log = self.fighter_basic_skill(damage_modifier)
        else:
            if self.fighter_mana < self.env['odooarena.fighter'].search([('fighting', '=', True)]).ultimate_skill.mana_cost:
                log = self.fighter_meditate()
            else:
                log = self.fighter_ultimate_skill(damage_modifier)
        return log

    def basic_fighter_attack(self, damage_modifier):
        fighter_damage = (randint(self.fighter_mindamage, self.fighter_maxdamage) - self.player_armor) * damage_modifier
        combat_log = "\nFighter has dealt %d damage back"
        fighter_damage, combat_log = self.update_if_fighter_crit(fighter_damage, combat_log)
        log = {
            'damage': fighter_damage,
            'combat_log': combat_log % fighter_damage,
        }
        return log

    def fighter_meditate(self):
        skill = self.env['odooarena.skills'].search([('id', '=', 1)])
        self.fighter_mana += 40
        heal = randint(skill.min_change_to_hp, skill.max_change_to_hp)
        self.fighter_hp += heal
        log = {
            'damage': 0,
            'combat_log': "\nFighter " + skill.log_text % heal
        }
        return log

    def fighter_basic_skill(self, damage_modifier):
        skill = self.env['odooarena.fighter'].search([('fighting', '=', True)]).basic_skill
        self.fighter_mana -= skill.mana_cost
        self.player_mana -= skill.min_change_to_mana
        log = self.create_log_and_crit_chance_check_for_skills(damage_modifier, skill)
        return log

    def fighter_ultimate_skill(self, damage_modifier):
        skill = self.env['odooarena.fighter'].search([('fighting', '=', True)]).ultimate_skill
        self.fighter_mana -= skill.mana_cost
        log = self.create_log_and_crit_chance_check_for_skills(damage_modifier, skill)
        return log

    def update_if_fighter_crit(self, damage, log):
        chance = randint(1, 100)
        if chance <= self.fighter_crit_chance*100:
            damage = (damage + self.player_armor) * 2 - self.player_armor
            log += " (critical damage!)"
        return damage, log

    def create_log_and_crit_chance_check_for_skills(self, damage_modifier, skill):
        fighter_damage = (randint(skill.min_change_to_hp, skill.max_change_to_hp) - self.player_armor) * damage_modifier
        combat_log = "\nFighter " + skill.log_text
        fighter_damage, combat_log = self.update_if_fighter_crit(fighter_damage, combat_log)
        log = {
            'damage': fighter_damage,
            'combat_log': combat_log % fighter_damage,
        }
        return log

    """ END GAME OPERATIONS """

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
        next_fighter = self.env['odooarena.fighter'].search([('id', '=', fighter.level+1)])
        try:
            next_fighter.fighting = True
        except ValueError:
            self.env['odooarena.fighter'].search([('level', '=', 1)]).fighting = True
        player.level += 1
        self.won = True

    def chose_item_1(self):
        item = self.fighter.drops_item_1
        self.item_stats_change(item)
        self.reset()

    def chose_item_2(self):
        item = self.fighter.drops_item_2
        self.item_stats_change(item)
        self.reset()

    def item_stats_change(self, item):
        player = self.env['odooarena.player'].search([('creator_id', '=', self.env.user.id)])
        player.write({
            'maxhp': player.maxhp + item.change_to_hp,
            'mana': player.mana + item.change_to_mana,
            'armor': player.armor + item.change_to_armor,
            'crit_chance': player.crit_chance + item.change_to_crit,
            'mindamage': player.mindamage + item.change_to_damage,
            'maxdamage': player.maxdamage + item.change_to_damage,
        })

    @api.multi
    def player_lost(self):
        self.env['odooarena.fighter'].search([('fighting', '=', True)]).fighting = False
        self.env['odooarena.fighter'].search([('level', '=', 1)]).fighting = True
        self.env['odooarena.player'].search([('creator_id', '=', self.env.user.id)]).unlink()
        self.lost = True

    def reset(self):
        self.started = False
        self.lost = False
        self.won = False

    # Only failures here

    def lost_window(self):
        print(1)
        # action = self.env.ref('odooarena.you_lost_form_view').read()[0]
        # return action
        action_id = self.env.ref('odooarena.you_lost_form_view')
        print(action_id)
        print(self.id)
        return {
            'name': "You Lost!",
            'type': 'ir.actions.act_window',
            'res_model': 'odooarena.arena',
            'view_mode': 'form',
            'view_id': action_id.id,
            'target': 'new',
            'domain': "[('creator_id', '=', 'self.env.user.id')]",
        }
