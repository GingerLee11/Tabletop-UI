from django.urls import reverse
from django.contrib.auth import get_user_model

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
        
    def test_create_the_blessed_with_vessel_background_redirects_to_home_page(self):
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
    
