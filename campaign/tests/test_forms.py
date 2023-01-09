from django.test import TestCase

from unittest import skip

from campaign.forms import (
    CreateCharacterForm,  CreateTheBlessedForm
)
from campaign.models import (
    CharacterClass,
    Background, Instinct, AppearanceAttribute, 
    PlaceOfOrigin, SpecialPossessions, Moves,
    RemarkableTraits, DanuOfferings
)
from campaign.constants import (
    POUCH_ORIGINS, POUCH_MATERIAL, POUCH_AESTHETICS, DANU_SHRINE
)
from campaign.tests.base import BaseTestClass


class BaseFormsTestClass(BaseTestClass):
    """
    This inherits from the BaseTestClass and then changes it 
    to fit the needs of the forms.
    """  
    

class CreateCharacterFormTest(BaseFormsTestClass):
    fixtures = ['campaign_data.json']

    @classmethod
    def setUpTestData(cls):
        cls.the_blessed = CharacterClass.objects.get(class_name='The Blessed')
        cls.blessed_form = CreateTheBlessedForm

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
        form_data = self.generate_create_character_form_data(character_class=self.the_blessed)
        form = CreateCharacterForm(character_class=self.the_blessed, data=form_data)
        self.assertTrue(form.is_valid)

    def test_create_character_str_below_min_invalid(self):
        form_data = self.generate_create_character_form_data(character_class=self.the_blessed, STR=-2)
        form = CreateCharacterForm(character_class=self.the_blessed, data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_character_str_above_max_invalid(self):
        form_data = self.generate_create_character_form_data(character_class=self.the_blessed, STR=4)
        form = CreateCharacterForm(character_class=self.the_blessed, data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_character_dex_below_max_invalid(self):
        form_data = self.generate_create_character_form_data(character_class=self.the_blessed, DEX=-2)
        form = CreateCharacterForm(character_class=self.the_blessed, data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_character_dex_above_max_invalid(self):
        form_data = self.generate_create_character_form_data(character_class=self.the_blessed, DEX=4)
        form = CreateCharacterForm(character_class=self.the_blessed, data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_character_int_below_max_invalid(self):
        form_data = self.generate_create_character_form_data(character_class=self.the_blessed, INT=-2)
        form = CreateCharacterForm(character_class=self.the_blessed, data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_character_int_above_max_invalid(self):
        form_data = self.generate_create_character_form_data(character_class=self.the_blessed, INT=4)
        form = CreateCharacterForm(character_class=self.the_blessed, data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_character_wis_below_max_invalid(self):
        form_data = self.generate_create_character_form_data(character_class=self.the_blessed, WIS=-2)
        form = CreateCharacterForm(character_class=self.the_blessed, data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_character_wis_above_max_invalid(self):
        form_data = self.generate_create_character_form_data(character_class=self.the_blessed, WIS=4)
        form = CreateCharacterForm(character_class=self.the_blessed, data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_character_con_below_max_invalid(self):
        form_data = self.generate_create_character_form_data(character_class=self.the_blessed, CON=-2)
        form = CreateCharacterForm(character_class=self.the_blessed, data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_character_con_above_max_invalid(self):
        form_data = self.generate_create_character_form_data(character_class=self.the_blessed, CON=4)
        form = CreateCharacterForm(character_class=self.the_blessed, data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_character_cha_below_max_invalid(self):
        form_data = self.generate_create_character_form_data(character_class=self.the_blessed, CHA=-2)
        form = CreateCharacterForm(character_class=self.the_blessed, data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_character_cha_above_max_invalid(self):
        form_data = self.generate_create_character_form_data(character_class=self.the_blessed, CHA=4)
        form = CreateCharacterForm(character_class=self.the_blessed, data=form_data)
        self.assertFalse(form.is_valid())

class CreateTheBlessedTest(BaseFormsTestClass):
    fixtures = ['campaign_data.json']

    @classmethod
    def setUpTestData(cls):
        cls.the_blessed = CharacterClass.objects.get(class_name='The Blessed')
        cls.blessed_form = CreateTheBlessedForm
        cls.starting_moves = ['SPIRIT TONGUE', 'CALL THE SPIRITS']

    def test_blank_create_blessed_form_not_valid(self):
        form = self.blessed_form()
        self.assertFalse(form.is_valid())
    
    def test_create_blessed_form_with_correct_inputs_is_valid(self):
        moves = self.starting_moves
        moves.append('TRACKLESS STEP')
        moves.append('AMULETS & TALISMANS')
        moves_qs = Moves.objects.filter(name__in=moves)
        blessed_kwargs = {
            'pouch_origin': POUCH_ORIGINS[0][0],
            'pouch_material': POUCH_MATERIAL[0][0],
            'pouch_aesthetics': POUCH_AESTHETICS[0][0],
            'remarkable_traits': RemarkableTraits.objects.filter(description__icontains='It cannot be cut,'),
            'danus_shrine': DANU_SHRINE[0][0],
            'offerings': DanuOfferings.objects.all()[0:3],
        }
        form_data = self.generate_create_character_form_data(character_class=self.the_blessed,background=1, moves=moves_qs, kwargs=blessed_kwargs)
        form = CreateTheBlessedForm(self.the_blessed, data=form_data)
        self.assertTrue(form.is_valid())
