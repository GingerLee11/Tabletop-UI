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
    TheRanger, 
)
from campaign.constants import (
    RANGER_STARTING_MOVES, RANGER_STARTING_POSSESSIONS,
    SOMETHING_WICKED, 
)
from campaign.tests.base import (
    TEST_CAMPAIGN, TEST_USERNAME,
)
from campaign.tests.test_views.base_views import BaseViewsTestClass

User = get_user_model()


class CreateTheRangerTests(BaseViewsTestClass):
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
        
        # Set ranger Character class 
        cls.the_ranger = CharacterClass.objects.get(class_name="The Ranger")
        cls.starting_moves = RANGER_STARTING_MOVES
        cls.starting_possessions = RANGER_STARTING_POSSESSIONS
        # Generate the form attributes unique to the Ranger
        cls.ranger_kwargs = {
            'something_wicked': SOMETHING_WICKED[0][0],
            'wicked_detail_1': 'A monster!!!.',
            'wicked_detail_3': 'Everyone and everything.',
            'wicked_detail_7': "The spirits of the Forest Folk.",
        }

    def test_create_the_ranger_template_used(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)

        response = self.client.get(f'/campaigns/{test_campaign.pk}/create_the_ranger/')

        self.assertTemplateUsed(response, 'campaign/create_the_ranger.html')

    def test_create_the_ranger_page_redirects_if_not_logged_in(self):
        test_campaign = Campaign.objects.get(name=TEST_CAMPAIGN)

        response = self.client.get(reverse('the-ranger', kwargs={'pk': test_campaign.pk}))

        self.assertRedirects(response, f'/login/?next=/campaigns/{test_campaign.pk}/create_the_ranger/')

    @skip
    def test_create_the_ranger_redirects_if_campaign_permission_not_met(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser2)
        # TODO: Create Permissions so that users without access to the specific campaign cannot access
        # any of the related pages

        response = self.client.get(reverse('the-ranger', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(response.status_code, 403)

    def test_create_the_ranger_all_ranger_backgrounds(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        ranger_backgrounds = list(Background.objects.filter(character_class=self.the_ranger).order_by('background'))
    
        response = self.client.get(reverse('the-ranger', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['background'].queryset), ranger_backgrounds)

    def test_create_the_ranger_all_ranger_instincts(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        ranger_instincts = list(Instinct.objects.filter(character_class=self.the_ranger))
    
        response = self.client.get(reverse('the-ranger', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['instinct'].queryset), ranger_instincts)

    def test_create_the_ranger_ranger_appearance1(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        ranger_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_ranger).filter(
                attribute_type='appearance1'
            ))
    
        response = self.client.get(reverse('the-ranger', kwargs={'pk': test_campaign.pk}))

        appearance1 = list(response.context['form'].fields['appearance1'].queryset)
        self.assertEqual(appearance1, ranger_apperances)

    def test_create_the_ranger_ranger_appearance2(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        ranger_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_ranger).filter(
                attribute_type='appearance2'
            ))
    
        response = self.client.get(reverse('the-ranger', kwargs={'pk': test_campaign.pk}))

        appearance2 = list(response.context['form'].fields['appearance2'].queryset)
        self.assertEqual(appearance2, ranger_apperances)

    def test_create_the_ranger_ranger_appearance3(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        ranger_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_ranger).filter(
                attribute_type='appearance3'
            ))
    
        response = self.client.get(reverse('the-ranger', kwargs={'pk': test_campaign.pk}))

        appearance3 = list(response.context['form'].fields['appearance3'].queryset)
        self.assertEqual(appearance3, ranger_apperances)

    def test_create_the_ranger_ranger_appearance4(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        ranger_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_ranger).filter(
                attribute_type='appearance4'
            ))
    
        response = self.client.get(reverse('the-ranger', kwargs={'pk': test_campaign.pk}))

        appearance4 = list(response.context['form'].fields['appearance4'].queryset)
        self.assertEqual(appearance4, ranger_apperances)

    def test_create_the_ranger_all_ranger_places_of_origin(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        ranger_poo = list(PlaceOfOrigin.objects.filter(
            character_class=self.the_ranger).order_by('location'))
    
        response = self.client.get(reverse('the-ranger', kwargs={'pk': test_campaign.pk}))

        poo = list(response.context['form'].fields['place_of_origin'].queryset)
        self.assertEqual(poo, ranger_poo)

    def test_create_the_ranger_all_ranger_special_possessions(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        possessions = list(SpecialPossessions.objects.filter(
            character_class=self.the_ranger).order_by('possession_name'))
    
        response = self.client.get(reverse('the-ranger', kwargs={'pk': test_campaign.pk}))

        form_possessions = list(response.context['form'].fields['special_possessions'].queryset)
        self.assertEqual(form_possessions, possessions)

    def test_create_the_ranger_all_ranger_moves(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = list(Moves.objects.filter(
            character_class__class_name=self.the_ranger,
        ).filter(
            move_requirements__level_restricted=None,
        ).order_by(
            F('move_requirements__move_restricted').asc(nulls_first=True), 
            F('move_requirements__level_restricted').asc(nulls_first=True), 
            'name',
        ))
    
        response = self.client.get(reverse('the-ranger', kwargs={'pk': test_campaign.pk}))

        move_instances = list(response.context['form'].fields['move_instances'].queryset)
        self.assertEqual(moves, move_instances)

    def test_create_the_ranger_actually_creates_a_ranger_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('EXPERT TRACKER')
        moves.append('STALKER')
        moves_qs = Moves.objects.filter(name__in=moves)
        possessions = self.starting_possessions
        sp_qs = SpecialPossessions.objects.filter(possession_name__in=possessions)
        
        # MIGHTY HUNTER background (1)
        form_data = self.generate_create_character_form_data(
            self.the_ranger, background=1, moves=moves_qs, special_possessions=sp_qs, kwargs=self.ranger_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-ranger', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        self.assertEqual(TheRanger.objects.count(), 1)

    def test_create_the_ranger_with_beast_bonded_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('ANIMAL COMPANION')
        moves_qs = Moves.objects.filter(name__in=moves)
        possessions = self.starting_possessions
        sp_qs = SpecialPossessions.objects.filter(possession_name__in=possessions)
        
        # BEAST-BONDED background is the first one (0)
        form_data = self.generate_create_character_form_data(
            self.the_ranger, background=0, moves=moves_qs, special_possessions=sp_qs, kwargs=self.ranger_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-ranger', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheRanger.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'BEAST-BONDED')
        self.assertRedirects(response, reverse('create-animal-companion', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))
        
    def test_create_the_ranger_with_mighty_hunter_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('EXPERT TRACKER')
        moves.append('STALKER')
        moves_qs = Moves.objects.filter(name__in=moves)
        possessions = self.starting_possessions
        sp_qs = SpecialPossessions.objects.filter(possession_name__in=possessions)
        
        # MIGHTY HUNTER backgroud (1)
        form_data = self.generate_create_character_form_data(
            self.the_ranger, background=1, moves=moves_qs, special_possessions=sp_qs, kwargs=self.ranger_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-ranger', kwargs={'pk': test_campaign.pk}), data=form_data)
        
        char = TheRanger.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'MIGHTY HUNTER')
        self.assertRedirects(response, reverse('the-ranger-detail', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))
        
    def test_create_the_ranger_with_wide_wanderer_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('MENTAL MAP')
        moves_qs = Moves.objects.filter(name__in=moves)
        possessions = self.starting_possessions
        sp_qs = SpecialPossessions.objects.filter(possession_name__in=possessions)
        
        # WIDE WANDERER background (2)
        form_data = self.generate_create_character_form_data(
            self.the_ranger, background=2, moves=moves_qs, special_possessions=sp_qs, kwargs=self.ranger_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-ranger', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheRanger.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'WIDE WANDERER')
        self.assertRedirects(response, reverse('the-ranger-detail', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))

    def test_create_the_ranger_creates_special_possession_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('EXPERT TRACKER')
        moves.append('STALKER')
        moves_qs = Moves.objects.filter(name__in=moves)
        possessions = self.starting_possessions
        possessions.append('Distillery')
        sp_qs = SpecialPossessions.objects.filter(possession_name__in=possessions)
        
        form_data = self.generate_create_character_form_data(
            self.the_ranger, background=1, moves=moves_qs, special_possessions=sp_qs, kwargs=self.ranger_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-ranger', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheRanger.objects.all()[0] # TODO: Find a less hacky way to get the character
        possession1 = SpecialPossessionInstance.objects.get(special_possession__possession_name="Compound bow")
        possession2 = SpecialPossessionInstance.objects.get(special_possession__possession_name="Distillery")
        self.assertEqual(list(char.special_possessions.all()), [possession1, possession2])
        
    def test_create_the_ranger_creates_moves_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('EXPERT TRACKER')
        moves.append('STALKER')
        moves_qs = Moves.objects.filter(name__in=moves)
        possessions = self.starting_possessions
        sp_qs = SpecialPossessions.objects.filter(possession_name__in=possessions)
                
        # MIGHTY HUNTER background (1)
        form_data = self.generate_create_character_form_data(
            self.the_ranger, background=1, moves=moves_qs, special_possessions=sp_qs, kwargs=self.ranger_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-ranger', kwargs={'pk': test_campaign.pk}), data=form_data)

        char = TheRanger.objects.all()[0] # TODO: Find a less hacky way to get the character
        move_instance_1 = MoveInstance.objects.get(move__name='EXPERT TRACKER')
        move_instance_2 = MoveInstance.objects.get(move__name='HOME ON THE RANGE')
        move_instance_3 = MoveInstance.objects.get(move__name='STALKER')
        self.assertEqual(list(char.move_instances.all()), [move_instance_1, move_instance_2, move_instance_3])

    def test_create_the_ranger_at_least_three_something_wicked_details_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('EXPERT TRACKER')
        moves.append('STALKER')
        moves_qs = Moves.objects.filter(name__in=moves)

        form_data = self.generate_create_character_form_data(self.the_ranger, background=1, moves=moves_qs, kwargs=self.ranger_kwargs)
        form_data.pop('wicked_detail_1')
        form_data.pop('wicked_detail_3')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-ranger', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', field=None, errors=['You have answered 1 question(s). Please answer at least 3 questions about something wicked.'])
          
    def test_create_the_ranger_something_wicked_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_ranger, background=1, kwargs=self.ranger_kwargs)
        form_data.pop('something_wicked')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-ranger', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'something_wicked', ['This field is required.'])
    
    def test_create_the_ranger_without_starting_moves_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_ranger, background=0, kwargs=self.ranger_kwargs)
        form_data.pop('move_instances')
        move = Moves.objects.filter(name='A SAFE PLACE')
        form_data['move_instances'] = move
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-ranger', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', field=None, errors=['HOME ON THE RANGE is a required starting move.'])
    
    def test_create_the_ranger_restricted_move_raises_error_if_selected(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('ALPHA')
        moves_qs = Moves.objects.filter(name__in=moves)
        # MIGHTY HUNTER background (1)
        form_data = self.generate_create_character_form_data(self.the_ranger, background=1, moves=moves_qs, kwargs=self.ranger_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)
        response = self.client.post(reverse('the-ranger', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertFormError(response, 'form', field=None, errors=['ALPHA requires the WILD SPEECH move.'])

    def test_create_the_ranger_mighty_hunter_background_without_expert_tracker_and_stalker_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # MIGHTY HUNTER background (1)
        form_data = self.generate_create_character_form_data(self.the_ranger, background=1, moves=moves_qs, kwargs=self.ranger_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)
        response = self.client.post(reverse('the-ranger', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertFormError(response, 'form', field=None, errors=['EXPERT TRACKER move is required for MIGHTY HUNTER background.', 'STALKER move is required for MIGHTY HUNTER background.'])

    def test_create_the_ranger_beast_bonded_background_without_animal_companion_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # BEAST-BONDED background (0)
        form_data = self.generate_create_character_form_data(self.the_ranger, background=0, moves=moves_qs, kwargs=self.ranger_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)
        response = self.client.post(reverse('the-ranger', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertFormError(response, 'form', field=None, errors=['ANIMAL COMPANION move is required for BEAST-BONDED background.'])

    def test_create_the_ranger_wide_wanderer_background_without_mental_map_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # WIDE WANDERER background (2)
        form_data = self.generate_create_character_form_data(self.the_ranger, background=2, moves=moves_qs, kwargs=self.ranger_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)
        response = self.client.post(reverse('the-ranger', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertFormError(response, 'form', field=None, errors=['MENTAL MAP move is required for WIDE WANDERER background.'])

    def test_create_the_ranger_without_compound_bow_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_ranger, background=0, kwargs=self.ranger_kwargs)
        form_data.pop('special_possessions')
        possession = SpecialPossessions.objects.filter(possession_name='Distillery')
        form_data['special_possessions'] = possession
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-ranger', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', field=None, errors=['Compound bow is a required starting special possession.'])
    