from django.test import TestCase

from unittest import skip

from campaign.forms import (
    CreateCharacterForm,  CreateTheBlessedForm
)
from campaign.models import (
    CharacterClass,
    Background, Instinct, AppearanceAttribute, 
    PlaceOfOrigin, SpecialPossessions, Moves,
)


class CharacterFormBaseTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.the_blessed = CharacterClass.objects.get(class_name='The Blessed')
        cls.blessed_form = CreateTheBlessedForm
        
    def fill_out_create_character_form(self, character_class=None, STR=0, DEX=0, INT=0, WIS=0, CON=0, CHA=0):
        background_pk = Background.objects.filter(character_class=character_class)[0].pk
        instinct_pk = Instinct.objects.filter(character_class=character_class)[0].pk
        appearance1_pk = AppearanceAttribute.objects.filter(
            character_class=character_class).filter(
                attribute_type='appearance1'
        )[0].pk
        appearance2_pk = AppearanceAttribute.objects.filter(
            character_class=character_class).filter(
                attribute_type='appearance2'
        )[0].pk
        appearance3_pk = AppearanceAttribute.objects.filter(
            character_class=character_class).filter(
                attribute_type='appearance3'
        )[0].pk
        appearance4_pk = AppearanceAttribute.objects.filter(
            character_class=character_class).filter(
                attribute_type='appearance4'
        )[0].pk
        place_of_origin_pk = PlaceOfOrigin.objects.filter(character_class=character_class)[0].pk
        special_possession_list = SpecialPossessions.objects.filter(character_class=character_class)[:2]
        move_list = Moves.objects.filter(character_class=character_class)[:2]
        form = CreateCharacterForm(data={
            'background': background_pk, 
            'instinct': instinct_pk, 
            'appearance1': appearance1_pk, 
            'appearance2': appearance2_pk, 
            'appearance3': appearance3_pk, 
            'appearance4': appearance4_pk,
            'place_of_origin': place_of_origin_pk,
            'character_name': 'test',
            'strength': STR,
            'dexterity': DEX,
            'intelligence': INT,
            'wisdom': WIS,
            'constitution': CON,
            'charisma': CHA,
            'special_possessions': special_possession_list,
            'move_instances': move_list,
        })
        return form
        

class CreateCharacterFormTest(CharacterFormBaseTest):
    fixtures = ['campaign_data.json']

    def test_blank_form_not_valid(self):
        form = CreateCharacterForm()
        self.assertFalse(form.is_valid())

    def test_create_character_background_label_is_blank(self):
        form = CreateCharacterForm()
        self.assertTrue(form.fields['background'].label == '')

    def test_create_character_instinct_label_is_blank(self):
        form = CreateCharacterForm()
        self.assertTrue(form.fields['instinct'].label == '')

    def test_create_character_appearance_labels_are_blank(self):
        form = CreateCharacterForm()
        self.assertTrue(form.fields['appearance1'].label == '')
        self.assertTrue(form.fields['appearance2'].label == '')
        self.assertTrue(form.fields['appearance3'].label == '')
        self.assertTrue(form.fields['appearance4'].label == '')
        
    def test_create_character_place_of_origin_label_is_blank(self):
        form = CreateCharacterForm()
        self.assertTrue(form.fields['place_of_origin'].label == '')
        
    def test_create_character_character_name_label_is_blank(self):
        form = CreateCharacterForm()
        self.assertTrue(form.fields['character_name'].label == '')
        
    def test_create_character_special_possessions_label_is_blank(self):
        form = CreateCharacterForm()
        self.assertTrue(form.fields['special_possessions'].label == '')
        
    def test_create_character_move_instances_label_is_blank(self):
        form = CreateCharacterForm()
        self.assertTrue(form.fields['move_instances'].label == '')

    def test_form_valid_with_correct_inputs(self):
        form = self.fill_out_create_character_form(character_class=self.the_blessed)
        self.assertTrue(form.is_valid)

    def test_create_character_str_below_min_invalid(self):
        form = self.fill_out_create_character_form(character_class=self.the_blessed, STR=-2)
        self.assertFalse(form.is_valid())

    def test_create_character_str_above_max_invalid(self):
        form = self.fill_out_create_character_form(character_class=self.the_blessed, STR=4)
        self.assertFalse(form.is_valid())

    def test_create_character_dex_below_max_invalid(self):
        form = self.fill_out_create_character_form(character_class=self.the_blessed, DEX=-2)
        self.assertFalse(form.is_valid())

    def test_create_character_dex_above_max_invalid(self):
        form = self.fill_out_create_character_form(character_class=self.the_blessed, DEX=4)
        self.assertFalse(form.is_valid())

    def test_create_character_int_below_max_invalid(self):
        form = self.fill_out_create_character_form(character_class=self.the_blessed, INT=-2)
        self.assertFalse(form.is_valid())

    def test_create_character_int_above_max_invalid(self):
        form = self.fill_out_create_character_form(character_class=self.the_blessed, INT=4)
        self.assertFalse(form.is_valid())

    def test_create_character_wis_below_max_invalid(self):
        form = self.fill_out_create_character_form(character_class=self.the_blessed, WIS=-2)
        self.assertFalse(form.is_valid())

    def test_create_character_wis_above_max_invalid(self):
        form = self.fill_out_create_character_form(character_class=self.the_blessed, WIS=4)
        self.assertFalse(form.is_valid())

    def test_create_character_con_below_max_invalid(self):
        form = self.fill_out_create_character_form(character_class=self.the_blessed, CON=-2)
        self.assertFalse(form.is_valid())

    def test_create_character_con_above_max_invalid(self):
        form = self.fill_out_create_character_form(character_class=self.the_blessed, CON=4)
        self.assertFalse(form.is_valid())

    def test_create_character_cha_below_max_invalid(self):
        form = self.fill_out_create_character_form(character_class=self.the_blessed, CHA=-2)
        self.assertFalse(form.is_valid())

    def test_create_character_cha_above_max_invalid(self):
        form = self.fill_out_create_character_form(character_class=self.the_blessed, CHA=4)
        self.assertFalse(form.is_valid())


class CreateTheBlessedTest(CharacterFormBaseTest):
    fixtures = ['campaign_data.json']

    def test_blank_create_blessed_form_not_valid(self):
        form = self.blessed_form()
        self.assertFalse(form.is_valid())
