from django.test import TestCase
from django.urls import reverse, resolve
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models

from unittest import skip

from stonetop_site.views import HomePageView

from campaign.models import (
    Campaign, 
    CharacterClass, Character, 
    Background, Instinct, 
    AppearanceAttribute, PlaceOfOrigin, 
    SpecialPossessions, SpecialPossessionInstance, 
    Moves, MoveInstance,
    RemarkableTraits, DanuOfferings,
    TheBlessed,
)
from campaign.constants import (
    CAMPAIGN_STATUS,
    POUCH_ORIGINS, POUCH_MATERIAL, POUCH_AESTHETICS, DANU_SHRINE
)
from campaign.tests.base import BaseTestClass


User = get_user_model()
TEST_USERNAME = 'testuser'
TEST_EMAIL = 'testing@example.com'
TEST_CAMPAIGN = 'Open campaign for functional tests'


class BaseViewsTestClass(BaseTestClass):
    def login_user(self, user):
        self.client.force_login(user, settings.AUTHENTICATION_BACKENDS[0])

    def set_campaign_session_data(self, campaign):
        session = self.client.session
        session['current_campaign_id'] = campaign.pk
        session['current_campaign_name'] = campaign.name
        session.save()

    def convert_data_to_foreign_keys(self, data):
        for k, o in data.items():
            if isinstance(o, models.query.QuerySet):
                o = list(o)
                o = [i.pk for i in o]
                data[k] = o
        return data

class HomePageTests(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    
class CampaignListPageTests(TestCase):

    def test_uses_campaign_list_template(self):
        response = self.client.get('/campaigns/')
        self.assertTemplateUsed(response, 'campaign/campaign_list.html')


class CampaignCreationAndPlayerAdditionTests(BaseViewsTestClass):

    @classmethod
    def setUpTestData(cls):
        # Create three users
        test_gm1 = User.objects.create(
            username='test_gm1',
            email='gm@test.com',
            password='29874v2398vrn83',
        )
        test_player1 = User.objects.create(
            username='test_player1',
            email='player1@test.com',
            password='109wdmgbowei8idj',
        )
        test_player2 = User.objects.create(
            username='test_player2',
            email='player2@test.com',
            password='sldifj2932938f238f',
        )

        test_gm1.save()
        test_player1.save()
        test_player2.save()

        cls.gm = test_gm1
        cls.player1 = test_player1
        cls.player2 = test_player2

        # test_gm1 will create a campaign
        test_campaign = Campaign.objects.create(
            gm=test_gm1,
            name='Test Campaign',
            code='superdupersecret1234',
            status=CAMPAIGN_STATUS[0][0],
        )
        test_campaign.players.set([test_player1])
        test_campaign.save()
        cls.campaign1 = test_campaign

    def login_user(self, user):
        self.client.force_login(user, settings.AUTHENTICATION_BACKENDS[0])

    def set_campaign_session_data(self, campaign):
        session = self.client.session
        session['current_campaign_id'] = campaign.pk
        session['current_campaign_name'] = campaign.name
        session.save()

    def test_campaign_present_in_database(self):
        self.assertEqual(Campaign.objects.count(), 1)

    def test_three_users_present_in_database(self):
        self.assertEqual(User.objects.count(), 3)

    def test_campaign_detail_page_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('campaign-detail', kwargs={'pk': self.campaign1.pk}))
        self.assertRedirects(response, f'/login/?next=/campaigns/{self.campaign1.pk}/')

    def test_campaign_detail_page_status_code(self):
        self.login_user(self.gm)
        response = self.client.get(f'/campaigns/{self.campaign1.id}/')
        # response = self.client.get(reverse('campaign-detail', args=[self.campaign1.id]))
        self.assertTrue(response.status_code, 200)

    def test_correct_template_campaign_detail_template_used(self):
        self.login_user(self.gm)
        response = self.client.get(f'/campaigns/{self.campaign1.id}/')
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'campaign/campaign_detail.html')
        
    def test_gm_can_view_campaign_detail_page(self):
        self.login_user(self.gm)
        response = self.client.get(reverse('campaign-detail', kwargs={'pk': self.campaign1.pk}))
        self.assertEqual(response.context['user'], self.gm)
        self.assertEqual(str(response.context['user']), 'test_gm1')

    def test_gm_can_see_campaign_code(self):
        self.login_user(self.gm)
        response = self.client.get(reverse('campaign-detail', kwargs={'pk': self.campaign1.pk}))
        self.assertContains(response, f'Campaign code: {self.campaign1.code}')

    def test_player1_can_see_campaign_information(self):
        # This is the user that the GM added when creating the campaign
        self.login_user(self.player1)

        response = self.client.get(reverse('campaign-detail', kwargs={'pk': self.campaign1.pk}))

        # Ensures that the player can see the basic campaign information, 
        # but not the campaign code (only the GM should be able to see this)
        self.assertNotContains(response, f'Campaign code: {self.campaign1.code}')
        self.assertContains(response, f'GM: {self.campaign1.gm}')
        self.assertContains(response, f'Campaign Status: {self.campaign1.status}')

    
    def test_player2_cannot_see_campaign_information(self):
        # This is a user that has not been given permission to view any of the 
        # campaign information
        self.login_user(self.player2)

        response = self.client.get(reverse('campaign-detail', kwargs={'pk': self.campaign1.pk}))

        # Ensures that the player can't see any of the campaign information
        self.assertNotContains(response, f'Campaign code: {self.campaign1.code}')
        self.assertNotContains(response, f'GM: {self.campaign1.gm}')
        self.assertNotContains(response, f'Campaign Status: {self.campaign1.status}')

    def test_check_code_redirects_to_campaign_detail_page_with_correct_code(self):
        # This is testing the campaign check code view
        self.login_user(self.player2)
        # This adds the id and name of the campaign to the sesions
        self.set_campaign_session_data(self.campaign1)

        response = self.client.post(f'/campaigns/{self.campaign1.pk}/check_code/', data={
            'code': self.campaign1.code
        })

        self.assertRedirects(response, f'/campaigns/{self.campaign1.pk}/')
        
    def test_player2_can_see_campaign_information_after_submitting_correct_code(self):
        # This is testing the campaign check code view
        self.login_user(self.player2)
        # This adds the id and name of the campaign to the sesions
        self.set_campaign_session_data(self.campaign1)

        response = self.client.post(f'/campaigns/{self.campaign1.pk}/check_code/', data={
            'code': self.campaign1.code
        })

        response = self.client.get(f'/campaigns/{self.campaign1.pk}/')

        # Ensures that the player can see the basic campaign information, 
        # but not the campaign code (only the GM should be able to see this)
        self.assertNotContains(response, f'Campaign code: {self.campaign1.code}')
        self.assertContains(response, f'GM: {self.campaign1.gm}')
        self.assertContains(response, f'Campaign Status: {self.campaign1.status}')


class CreateTheBlessedTests(BaseViewsTestClass):
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

    def join_campaign_and_login_user(self, campaign, user):
        test_campaign = Campaign.objects.get(name=campaign)
        self.login_user(user)
        self.set_campaign_session_data(test_campaign)
        return test_campaign

    def test_create_the_blessed_template_used(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)

        response = self.client.get(f'/campaigns/{test_campaign.pk}/create_the_blessed/')

        self.assertTemplateUsed(response, 'campaign/create_the_blessed.html')

    def test_create_the_blessed_page_redirects_if_not_logged_in(self):
        test_campaign = Campaign.objects.get(name=TEST_CAMPAIGN)

        response = self.client.get(reverse('the-blessed', kwargs={'pk': test_campaign.pk}))

        self.assertRedirects(response, f'/login/?next=/campaigns/{test_campaign.pk}/create_the_blessed/')

    @skip
    def test_create_the_blessed_redirects_if_campaign_permission_not_met(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser2)
        # TODO: Create Permissions so that users without access to the specific campaign cannot access
        # any of the related pages

        response = self.client.get(reverse('the-blessed', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(response.status_code, 403)

    def test_create_the_blessed_all_blessed_backgrounds(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        blessed_backgrounds = list(Background.objects.filter(character_class=self.the_blessed))
    
        response = self.client.get(reverse('the-blessed', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['background'].queryset), blessed_backgrounds)

    def test_create_the_blessed_all_blessed_instincts(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        blessed_instincts = list(Instinct.objects.filter(character_class=self.the_blessed))
    
        response = self.client.get(reverse('the-blessed', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['instinct'].queryset), blessed_instincts)

    def test_create_the_blessed_blessed_appearance1(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        blessed_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_blessed).filter(
                attribute_type='appearance1'
            ))
    
        response = self.client.get(reverse('the-blessed', kwargs={'pk': test_campaign.pk}))

        appearance1 = list(response.context['form'].fields['appearance1'].queryset)
        self.assertEqual(appearance1, blessed_apperances)

    def test_create_the_blessed_blessed_appearance2(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        blessed_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_blessed).filter(
                attribute_type='appearance2'
            ))
    
        response = self.client.get(reverse('the-blessed', kwargs={'pk': test_campaign.pk}))

        appearance2 = list(response.context['form'].fields['appearance2'].queryset)
        self.assertEqual(appearance2, blessed_apperances)

    def test_create_the_blessed_blessed_appearance3(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        blessed_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_blessed).filter(
                attribute_type='appearance3'
            ))
    
        response = self.client.get(reverse('the-blessed', kwargs={'pk': test_campaign.pk}))

        appearance3 = list(response.context['form'].fields['appearance3'].queryset)
        self.assertEqual(appearance3, blessed_apperances)

    def test_create_the_blessed_blessed_appearance4(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        blessed_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_blessed).filter(
                attribute_type='appearance4'
            ))
    
        response = self.client.get(reverse('the-blessed', kwargs={'pk': test_campaign.pk}))

        appearance4 = list(response.context['form'].fields['appearance4'].queryset)
        self.assertEqual(appearance4, blessed_apperances)

    def test_create_the_blessed_all_blesed_places_of_origin(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        blessed_poo = list(PlaceOfOrigin.objects.filter(
            character_class=self.the_blessed).order_by('location'))
    
        response = self.client.get(reverse('the-blessed', kwargs={'pk': test_campaign.pk}))

        poo = list(response.context['form'].fields['place_of_origin'].queryset)
        self.assertEqual(poo, blessed_poo)

    def test_create_the_blessed_all_blessed_special_possessions(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        possessions = list(SpecialPossessions.objects.filter(
            character_class=self.the_blessed).order_by('possession_name'))
    
        response = self.client.get(reverse('the-blessed', kwargs={'pk': test_campaign.pk}))

        form_possessions = list(response.context['form'].fields['special_possessions'].queryset)
        self.assertEqual(form_possessions, possessions)

    def test_create_the_blessed_all_blesed_moves(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = list(Moves.objects.filter(
            character_class=self.the_blessed).exclude(
                name__icontains='SPIRIT'
                ).filter(
                    move_requirements__level_restricted__isnull=True
                    ).order_by('name'))
    
        response = self.client.get(reverse('the-blessed', kwargs={'pk': test_campaign.pk}))

        move_instances = list(response.context['form'].fields['move_instances'].queryset)
        self.assertEqual(moves, move_instances)

    def test_create_the_blessed_actually_creates_a_blessed_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        # Initiate background is the first one (0)
        form_data = self.generate_create_character_form_data(self.the_blessed, background=0, kwargs=self.blessed_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        self.assertEqual(TheBlessed.objects.count(), 1)

    def test_create_the_blessed_with_initiate_background_redirects_to_initiate_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        # Initiate background is the first one (0)
        form_data = self.generate_create_character_form_data(self.the_blessed, background=0, kwargs=self.blessed_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheBlessed.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'INITIATE')
        self.assertRedirects(response, reverse('the-blessed-add-initiates', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))
        
    def test_create_the_blessed_with_raised_by_wolves_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        # Raised by wolves should be the second one
        form_data = self.generate_create_character_form_data(self.the_blessed, background=1, kwargs=self.blessed_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        
        char = TheBlessed.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'RAISED BY WOLVES')
        self.assertRedirects(response, reverse('the-blessed-detail', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))
        
    def test_create_the_blessed_with_raised_by_wolves_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        # VESSEL background (2)
        form_data = self.generate_create_character_form_data(self.the_blessed, background=2, kwargs=self.blessed_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheBlessed.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'VESSEL')
        self.assertRedirects(response, reverse('the-blessed-detail', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))

    def test_create_the_blessed_creates_special_possession_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        # RAISED BY WOLVES background (1)
        form_data = self.generate_create_character_form_data(self.the_blessed, background=1, kwargs=self.blessed_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheBlessed.objects.all()[0] # TODO: Find a less hacky way to get the character
        apiary = SpecialPossessionInstance.objects.get(special_possession__possession_name='Apiary')
        self.assertEqual(list(char.special_possessions.all()), [apiary])
        
    def test_create_the_blessed_creates_moves_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        # RAISED BY WOLVES background (1)
        form_data = self.generate_create_character_form_data(self.the_blessed, background=1, kwargs=self.blessed_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheBlessed.objects.all()[0] # TODO: Find a less hacky way to get the character
        amulets_and_talis = MoveInstance.objects.get(move__name='AMULETS & TALISMANS')
        call_the_spirits = MoveInstance.objects.get(move__name='CALL THE SPIRITS')
        spirit_tongue = MoveInstance.objects.get(move__name='SPIRIT TONGUE')
        self.assertEqual(list(char.move_instances.all()), [amulets_and_talis, call_the_spirits, spirit_tongue])

    def test_create_the_blessed_background_field_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=0, kwargs=self.blessed_kwargs)
        form_data.pop('background')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'background', ['This field is required.'])

    def test_create_the_blessed_instinct_field_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=0, kwargs=self.blessed_kwargs)
        form_data.pop('instinct')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'instinct', ['This field is required.'])
    
    def test_create_the_blessed_appearance_fields_required_error(self):
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

    def test_create_the_blessed_place_of_origin_field_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=0, kwargs=self.blessed_kwargs)
        form_data.pop('place_of_origin')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'place_of_origin', ['This field is required.'])

    def test_create_the_blessed_character_name_field_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=0, kwargs=self.blessed_kwargs)
        form_data.pop('character_name')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'character_name', ['This field is required.'])

    def test_create_the_blessed_stat_fields_required_errors(self):
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

    def test_create_the_blessed_stat_fields_below_min_errors(self):
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

    def test_create_the_blessed_stat_fields_above_max_error(self):
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

    def test_create_the_blessed_special_possessions_field_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=1, kwargs=self.blessed_kwargs)
        form_data.pop('special_possessions')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'special_possessions', ['This field is required.'])
  
    def test_create_the_blessed_move_instances_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=1, kwargs=self.blessed_kwargs)
        form_data.pop('move_instances')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'move_instances', ['This field is required.'])
      
    def test_create_the_blessed_pouch_origin_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=1, kwargs=self.blessed_kwargs)
        form_data.pop('pouch_origin')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'pouch_origin', ['This field is required.'])
          
    def test_create_the_blessed_pouch_material_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=1, kwargs=self.blessed_kwargs)
        form_data.pop('pouch_material')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'pouch_material', ['This field is required.'])
          
    def test_create_the_blessed_pouch_aesthetics_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=1, kwargs=self.blessed_kwargs)
        form_data.pop('pouch_aesthetics')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'pouch_aesthetics', ['This field is required.'])
              
    def test_create_the_blessed_remarkable_traits_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=1, kwargs=self.blessed_kwargs)
        form_data.pop('remarkable_traits')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'remarkable_traits', ['This field is required.'])
              
    def test_create_the_blessed_danus_shrine_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=1, kwargs=self.blessed_kwargs)
        form_data.pop('danus_shrine')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'danus_shrine', ['This field is required.'])
              
    def test_create_the_blessed_offerings_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_blessed, background=1, kwargs=self.blessed_kwargs)
        form_data.pop('offerings')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-blessed', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'offerings', ['This field is required.'])
    
