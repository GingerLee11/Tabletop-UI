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
    TheLightbearer, HeliorWorship,
    LightbearerPredecessor,
)
from campaign.constants import (
    LIGHTBEARER_STARTING_MOVES, WORSHIP_OF_HELIOR, 
    HELIORS_SHRINE, LIGHTBEARER_POWER_ORIGINS
)
from campaign.tests.base import (
    TEST_CAMPAIGN, TEST_USERNAME,
)
from campaign.tests.test_views.base_views import BaseViewsTestClass

User = get_user_model()


class CreateTheLightbearerTests(BaseViewsTestClass):
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
        
        # Set lightbearer Character class 
        cls.the_lightbearer = CharacterClass.objects.get(class_name="The Lightbearer")
        cls.starting_moves = LIGHTBEARER_STARTING_MOVES
        # Generate the form attributes unique to the Lightbearer
        methods_of_worship = HeliorWorship.objects.all()[0:2]
        methods_of_worship = [mw.pk for mw in methods_of_worship]
        predecessor = LightbearerPredecessor.objects.all()[0:3]
        predecessor = [p.pk for p in predecessor]
        cls.lightbearer_kwargs = {
            'worship_of_helior': WORSHIP_OF_HELIOR[0][0],
            'methods_of_worship': methods_of_worship,
            'heliors_shrine': HELIORS_SHRINE[0][0],
            'predecessor': predecessor,
            'origin_of_powers': LIGHTBEARER_POWER_ORIGINS[0][0],
        }

    def test_create_the_lightbearer_template_used(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)

        response = self.client.get(f'/campaigns/{test_campaign.pk}/create_the_lightbearer/')

        self.assertTemplateUsed(response, 'campaign/create_the_lightbearer.html')

    def test_create_the_lightbearer_page_redirects_if_not_logged_in(self):
        test_campaign = Campaign.objects.get(name=TEST_CAMPAIGN)

        response = self.client.get(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}))

        self.assertRedirects(response, f'/login/?next=/campaigns/{test_campaign.pk}/create_the_lightbearer/')

    @skip
    def test_create_the_lightbearer_redirects_if_campaign_permission_not_met(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser2)
        # TODO: Create Permissions so that users without access to the specific campaign cannot access
        # any of the related pages

        response = self.client.get(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(response.status_code, 403)

    def test_create_the_lightbearer_all_lightbearer_backgrounds(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        lightbearer_backgrounds = list(Background.objects.filter(character_class=self.the_lightbearer))
    
        response = self.client.get(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['background'].queryset), lightbearer_backgrounds)

    def test_create_the_lightbearer_all_lightbearer_instincts(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        lightbearer_instincts = list(Instinct.objects.filter(character_class=self.the_lightbearer))
    
        response = self.client.get(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['instinct'].queryset), lightbearer_instincts)

    def test_create_the_lightbearer_lightbearer_appearance1(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        lightbearer_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_lightbearer).filter(
                attribute_type='appearance1'
            ))
    
        response = self.client.get(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}))

        appearance1 = list(response.context['form'].fields['appearance1'].queryset)
        self.assertEqual(appearance1, lightbearer_apperances)

    def test_create_the_lightbearer_lightbearer_appearance2(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        lightbearer_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_lightbearer).filter(
                attribute_type='appearance2'
            ))
    
        response = self.client.get(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}))

        appearance2 = list(response.context['form'].fields['appearance2'].queryset)
        self.assertEqual(appearance2, lightbearer_apperances)

    def test_create_the_lightbearer_lightbearer_appearance3(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        lightbearer_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_lightbearer).filter(
                attribute_type='appearance3'
            ))
    
        response = self.client.get(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}))

        appearance3 = list(response.context['form'].fields['appearance3'].queryset)
        self.assertEqual(appearance3, lightbearer_apperances)

    def test_create_the_lightbearer_lightbearer_appearance4(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        lightbearer_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_lightbearer).filter(
                attribute_type='appearance4'
            ))
    
        response = self.client.get(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}))

        appearance4 = list(response.context['form'].fields['appearance4'].queryset)
        self.assertEqual(appearance4, lightbearer_apperances)

    def test_create_the_lightbearer_all_lightbearer_places_of_origin(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        lightbearer_poo = list(PlaceOfOrigin.objects.filter(
            character_class=self.the_lightbearer).order_by('location'))
    
        response = self.client.get(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}))

        poo = list(response.context['form'].fields['place_of_origin'].queryset)
        self.assertEqual(poo, lightbearer_poo)

    def test_create_the_lightbearer_all_lightbearer_special_possessions(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        possessions = list(SpecialPossessions.objects.filter(
            character_class=self.the_lightbearer).order_by('possession_name'))
    
        response = self.client.get(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}))

        form_possessions = list(response.context['form'].fields['special_possessions'].queryset)
        self.assertEqual(form_possessions, possessions)

    def test_create_the_lightbearer_all_lightbearer_moves(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = list(Moves.objects.filter(
            character_class__class_name=self.the_lightbearer,
        ).filter(
            move_requirements__level_restricted=None,
        ).order_by(
                F('move_requirements__move_restricted').asc(nulls_first=True), 
                F('move_requirements__level_restricted').asc(nulls_first=True), 
                'name',
        ))
    
        response = self.client.get(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}))

        move_instances = list(response.context['form'].fields['move_instances'].queryset)
        self.assertEqual(moves, move_instances)

    def test_create_the_lightbearer_actually_creates_a_lightbearer_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # AUSPICIOUS BIRTH background is the first one (0)
        form_data = self.generate_create_character_form_data(self.the_lightbearer, background=0, moves=moves_qs, kwargs=self.lightbearer_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        self.assertEqual(TheLightbearer.objects.count(), 1)

    def test_create_the_lightbearer_with_auspicious_birth_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)

        # AUSPICIOUS BIRTH background is the first one (0)
        form_data = self.generate_create_character_form_data(self.the_lightbearer, background=0, moves=moves_qs, kwargs=self.lightbearer_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheLightbearer.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'AUSPICIOUS BIRTH')
        self.assertRedirects(response, reverse('character-update-invocations', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))
        
    def test_create_the_lightbearer_with_itinerant_mystic_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # ITINERANT MYSTIC backgroud (1)
        form_data = self.generate_create_character_form_data(self.the_lightbearer, background=1, moves=moves_qs, kwargs=self.lightbearer_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}), data=form_data)
        
        char = TheLightbearer.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'ITINERANT MYSTIC')
        self.assertRedirects(response, reverse('character-update-invocations', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))
        
    def test_create_the_lightbearer_with_soul_on_fire_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # SOUL ON FIRE background (2)
        form_data = self.generate_create_character_form_data(self.the_lightbearer, background=2, moves=moves_qs, kwargs=self.lightbearer_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheLightbearer.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'SOUL ON FIRE')
        self.assertRedirects(response, reverse('character-update-invocations', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))

    def test_create_the_lightbearer_creates_special_possession_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        form_data = self.generate_create_character_form_data(self.the_lightbearer, background=0, moves=moves_qs, kwargs=self.lightbearer_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheLightbearer.objects.all()[0] # TODO: Find a less hacky way to get the character
        possession1 = SpecialPossessionInstance.objects.get(special_possession__possession_name="Apiary")
        self.assertEqual(list(char.special_possessions.all()), [possession1])
        
    def test_create_the_lightbearer_creates_moves_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # AUSPICIOUS BIRTH background (0)
        form_data = self.generate_create_character_form_data(self.the_lightbearer, background=0, moves=moves_qs, kwargs=self.lightbearer_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}), data=form_data)

        char = TheLightbearer.objects.all()[0] # TODO: Find a less hacky way to get the character
        move_instance_1 = MoveInstance.objects.get(move__name='CONSECRATED FLAME')
        move_instance_2 = MoveInstance.objects.get(move__name='INVOKE THE SUN GOD')
        self.assertEqual(list(char.move_instances.all()), [move_instance_1, move_instance_2])

    def test_create_the_lightbearer_worship_of_helior_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_lightbearer, background=0, kwargs=self.lightbearer_kwargs)
        form_data.pop('worship_of_helior')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'worship_of_helior', ['This field is required.'])
          
    def test_create_the_lightbearer_methods_of_worship_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_lightbearer, background=0, kwargs=self.lightbearer_kwargs)
        form_data.pop('methods_of_worship')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'methods_of_worship', ['This field is required.'])
    
    def test_create_the_lightbearer_heliors_shrine_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_lightbearer, background=0, kwargs=self.lightbearer_kwargs)
        form_data.pop('heliors_shrine')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'heliors_shrine', ['This field is required.'])    
    
    def test_create_the_lightbearer_predecessor_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_lightbearer, background=0, kwargs=self.lightbearer_kwargs)
        form_data.pop('predecessor')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'predecessor', ['This field is required.'])
    
    def test_create_the_lightbearer_origin_of_powers_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_lightbearer, background=0, kwargs=self.lightbearer_kwargs)
        form_data.pop('origin_of_powers')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'origin_of_powers', ['This field is required.'])
    
    def test_create_the_lightbearer_without_starting_moves_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_lightbearer, background=0, kwargs=self.lightbearer_kwargs)
        form_data.pop('move_instances')
        move = Moves.objects.filter(name='PIETY')
        form_data['move_instances'] = move
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', field=None, errors=['CONSECRATED FLAME is a required starting move.', 'INVOKE THE SUN GOD is a required starting move.'])
    
    def test_create_the_lightbearer_restricted_move_raises_error_if_selected(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('LUMINOUS SHIELD')
        moves_qs = Moves.objects.filter(name__in=moves)
        # AUSPICIOUS BIRTH background (0)
        form_data = self.generate_create_character_form_data(self.the_lightbearer, background=0, moves=moves_qs, kwargs=self.lightbearer_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)
        response = self.client.post(reverse('the-lightbearer', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertFormError(response, 'form', field=None, errors=['LUMINOUS SHIELD requires the A CANDLE AGAINST THE DARK move.'])
