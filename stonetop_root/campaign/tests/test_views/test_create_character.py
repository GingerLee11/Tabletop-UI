from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import F

from unittest import skip

from campaign.models import (
    Campaign, 
    CharacterClass,
    Background, Instinct, 
    AppearanceAttribute, PlaceOfOrigin, 
    SpecialPossessions, SpecialPossessionInstance, 
    Moves, MoveInstance,
    RemarkableTraits, DanuOfferings,
    TheBlessed,
)
from campaign.constants import (
    POUCH_ORIGINS, POUCH_MATERIAL, POUCH_AESTHETICS, DANU_SHRINE
)
from campaign.tests.base import (
    TEST_CAMPAIGN, TEST_USERNAME,
)
from campaign.tests.test_views.base_views import BaseViewsTestClass


User = get_user_model()


class CreateCharacterTest(BaseViewsTestClass):
    fixtures = ['campaign_data.json']

    @classmethod
    def setUpTestData(cls):
        test_player1 = User.objects.create(
            username='testuser2',
            email='player1@test.com',
            password='109wdmgbowei8idj',
        )
        testuser = User.objects.get(username=TEST_USERNAME)
        cls.testuser = testuser
        test_player1.save()
        cls.testuser2 = test_player1
        
        # Set Blessed Character class 
        cls.the_blessed = CharacterClass.objects.get(class_name="The Blessed")
        cls.the_fox = CharacterClass.objects.get(class_name="The Fox")
        cls.the_would_be_hero = CharacterClass.objects.get(class_name="The Would-Be Hero")

        # Generate the form attributes unique to the blessed
        offerings = DanuOfferings.objects.all()[0:3]
        offering_pks = [offering.pk for offering in offerings]
        cls.blessed_kwargs = {
            'pouch_origin': POUCH_ORIGINS[0][0],
            'pouch_material': POUCH_MATERIAL[0][0],
            'pouch_aesthetics': POUCH_AESTHETICS[0][0],
            'remarkable_traits': RemarkableTraits.objects.filter(description__icontains='It cannot be cut,')[0].pk,
            'danus_shrine': DANU_SHRINE[0][0],
            'offerings': offering_pks
        }

    def test_create_character_background_field_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=0, kwargs=self.blessed_kwargs)
        form_data.pop('background')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'background', ['This field is required.'])

    def test_create_character_instinct_field_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=0, kwargs=self.blessed_kwargs)
        form_data.pop('instinct')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'instinct', ['This field is required.'])
    
    def test_create_character_appearance_fields_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=0, kwargs=self.blessed_kwargs)
        form_data.pop('appearance1')
        form_data.pop('appearance2')
        form_data.pop('appearance3')
        form_data.pop('appearance4')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'appearance1', ['This field is required.'])
        self.assertFormError(response, 'form', 'appearance2', ['This field is required.'])
        self.assertFormError(response, 'form', 'appearance3', ['This field is required.'])
        self.assertFormError(response, 'form', 'appearance4', ['This field is required.'])

    def test_create_character_place_of_origin_field_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=0, kwargs=self.blessed_kwargs)
        form_data.pop('place_of_origin')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'place_of_origin', ['This field is required.'])

    def test_create_character_character_name_field_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=0, kwargs=self.blessed_kwargs)
        form_data.pop('character_name')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'character_name', ['This field is required.'])

    def test_create_character_stat_fields_required_errors(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=0, kwargs=self.blessed_kwargs)
        form_data.pop('strength')
        form_data.pop('dexterity')
        form_data.pop('intelligence')
        form_data.pop('wisdom')
        form_data.pop('constitution')
        form_data.pop('charisma')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'strength', ['This field is required.'])
        self.assertFormError(response, 'form', 'dexterity', ['This field is required.'])
        self.assertFormError(response, 'form', 'intelligence', ['This field is required.'])
        self.assertFormError(response, 'form', 'wisdom', ['This field is required.'])
        self.assertFormError(response, 'form', 'constitution', ['This field is required.'])
        self.assertFormError(response, 'form', 'charisma', ['This field is required.'])

    def test_create_character_stat_fields_below_min_errors(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, 
            background=0, STR=-2, DEX=-2, INT=-2, WIS=-2, CON=-2, CHA=-2, 
            kwargs=self.blessed_kwargs)

        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'strength', ['Ensure this value is greater than or equal to -1.'])
        self.assertFormError(response, 'form', 'dexterity', ['Ensure this value is greater than or equal to -1.'])
        self.assertFormError(response, 'form', 'intelligence', ['Ensure this value is greater than or equal to -1.'])
        self.assertFormError(response, 'form', 'wisdom', ['Ensure this value is greater than or equal to -1.'])
        self.assertFormError(response, 'form', 'constitution', ['Ensure this value is greater than or equal to -1.'])
        self.assertFormError(response, 'form', 'charisma', ['Ensure this value is greater than or equal to -1.'])

    def test_create_character_stat_fields_above_max_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, 
            background=0, STR=4, DEX=5, INT=6, WIS=7, CON=8, CHA=9, 
            kwargs=self.blessed_kwargs)

        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'strength', ['Ensure this value is less than or equal to 3.'])
        self.assertFormError(response, 'form', 'dexterity', ['Ensure this value is less than or equal to 3.'])
        self.assertFormError(response, 'form', 'intelligence', ['Ensure this value is less than or equal to 3.'])
        self.assertFormError(response, 'form', 'wisdom', ['Ensure this value is less than or equal to 3.'])
        self.assertFormError(response, 'form', 'constitution', ['Ensure this value is less than or equal to 3.'])
        self.assertFormError(response, 'form', 'charisma', ['Ensure this value is less than or equal to 3.'])


    def test_create_character_non_would_be_hero_character_without_correct_stat_scores_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, 
            background=0, STR=-1, DEX=2, INT=1, WIS=2, CON=0, CHA=-1, 
            kwargs=self.blessed_kwargs)

        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', field=None, 
            errors=['Stats should have the following scores (they can be in any order): +2, +1, +1, 0, 0, -1. Your stats are as follows: Strength: -1, Dexterity: 2, Intelligence: 1, Wisdom: 2, Constitution: 0, Charisma: -1.'])

    def test_create_character_special_possessions_field_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=1, kwargs=self.blessed_kwargs)
        form_data.pop('special_possessions')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'special_possessions', ['This field is required.'])
  
    def test_create_character_move_instances_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=1, kwargs=self.blessed_kwargs)
        form_data.pop('move_instances')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'move_instances', ['This field is required.'])
    
    def test_move_cannot_be_taken_without_move_requirement_met(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        move_1 = Moves.objects.get(name="PARRY & RIPOSTE")
        move_2 = Moves.objects.get(name="AMBUSH")
        move_3 = Moves.objects.get(name="DANGER SENSE")
        move_list = [move_1.pk, move_2.pk, move_3.pk]

        form_data = self.generate_create_character_form_data(self.the_fox, background=0, moves=move_list)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-fox', kwargs={'pk': test_campaign.pk}), data=form_data)
        
        # self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 
            'form', field=None,
            errors=["PARRY & RIPOSTE requires the SKILL AT ARMS move."]
        )

    