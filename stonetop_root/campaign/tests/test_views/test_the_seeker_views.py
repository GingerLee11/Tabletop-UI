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
    TheSeeker, 
)
from campaign.constants import (
    SEEKER_STARTING_MOVES,
)
from campaign.tests.base import (
    TEST_CAMPAIGN, TEST_USERNAME,
)
from campaign.tests.test_views.base_views import BaseViewsTestClass

User = get_user_model()


class CreateTheSeekerTests(BaseViewsTestClass):
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
        
        # Set seeker Character class 
        cls.the_seeker = CharacterClass.objects.get(class_name="The Seeker")
        cls.starting_moves = SEEKER_STARTING_MOVES
        # Generate the form attributes unique to the Seeker


    def test_create_the_seeker_template_used(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)

        response = self.client.get(f'/campaigns/{test_campaign.pk}/create_the_seeker/')

        self.assertTemplateUsed(response, 'campaign/create_the_seeker.html')

    def test_create_the_seeker_page_redirects_if_not_logged_in(self):
        test_campaign = Campaign.objects.get(name=TEST_CAMPAIGN)

        response = self.client.get(reverse('the-seeker', kwargs={'pk': test_campaign.pk}))

        self.assertRedirects(response, f'/login/?next=/campaigns/{test_campaign.pk}/create_the_seeker/')

    @skip
    def test_create_the_seeker_redirects_if_campaign_permission_not_met(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser2)
        # TODO: Create Permissions so that users without access to the specific campaign cannot access
        # any of the related pages

        response = self.client.get(reverse('the-seeker', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(response.status_code, 403)

    def test_create_the_seeker_all_seeker_backgrounds(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        seeker_backgrounds = list(Background.objects.filter(character_class=self.the_seeker).order_by('background'))
    
        response = self.client.get(reverse('the-seeker', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['background'].queryset), seeker_backgrounds)

    def test_create_the_seeker_all_seeker_instincts(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        seeker_instincts = list(Instinct.objects.filter(character_class=self.the_seeker))
    
        response = self.client.get(reverse('the-seeker', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['instinct'].queryset), seeker_instincts)

    def test_create_the_seeker_seeker_appearance1(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        seeker_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_seeker).filter(
                attribute_type='appearance1'
            ))
    
        response = self.client.get(reverse('the-seeker', kwargs={'pk': test_campaign.pk}))

        appearance1 = list(response.context['form'].fields['appearance1'].queryset)
        self.assertEqual(appearance1, seeker_apperances)

    def test_create_the_seeker_seeker_appearance2(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        seeker_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_seeker).filter(
                attribute_type='appearance2'
            ))
    
        response = self.client.get(reverse('the-seeker', kwargs={'pk': test_campaign.pk}))

        appearance2 = list(response.context['form'].fields['appearance2'].queryset)
        self.assertEqual(appearance2, seeker_apperances)

    def test_create_the_seeker_seeker_appearance3(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        seeker_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_seeker).filter(
                attribute_type='appearance3'
            ))
    
        response = self.client.get(reverse('the-seeker', kwargs={'pk': test_campaign.pk}))

        appearance3 = list(response.context['form'].fields['appearance3'].queryset)
        self.assertEqual(appearance3, seeker_apperances)

    def test_create_the_seeker_seeker_appearance4(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        seeker_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_seeker).filter(
                attribute_type='appearance4'
            ))
    
        response = self.client.get(reverse('the-seeker', kwargs={'pk': test_campaign.pk}))

        appearance4 = list(response.context['form'].fields['appearance4'].queryset)
        self.assertEqual(appearance4, seeker_apperances)

    def test_create_the_seeker_all_seeker_places_of_origin(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        seeker_poo = list(PlaceOfOrigin.objects.filter(
            character_class=self.the_seeker).order_by('location'))
    
        response = self.client.get(reverse('the-seeker', kwargs={'pk': test_campaign.pk}))

        poo = list(response.context['form'].fields['place_of_origin'].queryset)
        self.assertEqual(poo, seeker_poo)

    def test_create_the_seeker_all_seeker_special_possessions(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        possessions = list(SpecialPossessions.objects.filter(
            character_class=self.the_seeker).order_by('possession_name'))
    
        response = self.client.get(reverse('the-seeker', kwargs={'pk': test_campaign.pk}))

        form_possessions = list(response.context['form'].fields['special_possessions'].queryset)
        self.assertEqual(form_possessions, possessions)

    def test_create_the_seeker_all_seeker_moves(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = list(Moves.objects.filter(
            character_class__class_name=self.the_seeker,
        ).filter(
            move_requirements__level_restricted=None,
        ).order_by(
            F('move_requirements__move_restricted').asc(nulls_first=True), 
            F('move_requirements__level_restricted').asc(nulls_first=True), 
            'name',
        ))
    
        response = self.client.get(reverse('the-seeker', kwargs={'pk': test_campaign.pk}))

        move_instances = list(response.context['form'].fields['move_instances'].queryset)
        self.assertEqual(moves, move_instances)

    def test_create_the_seeker_actually_creates_a_seeker_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('POLYGLOT')
        moves_qs = Moves.objects.filter(name__in=moves)
        # ANTIQUARIAN background (0)
        form_data = self.generate_create_character_form_data(self.the_seeker, background=0, moves=moves_qs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-seeker', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        self.assertEqual(TheSeeker.objects.count(), 1)

    def test_create_the_seeker_with_antiquarian_background_redirects_to_initial_arcana_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('POLYGLOT')
        moves_qs = Moves.objects.filter(name__in=moves)

        # ANTIQUARIAN background is the first one (0)
        form_data = self.generate_create_character_form_data(self.the_seeker, background=0, moves=moves_qs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-seeker', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheSeeker.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'ANTIQUARIAN')
        self.assertRedirects(response, reverse('the-seeker-initial-arcana', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))
        
    def test_create_the_seeker_with_patriot_background_redirects_to_initial_arcana_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append("LET'S MAKE A DEAL")
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # PATRIOT backgroud (1)
        form_data = self.generate_create_character_form_data(self.the_seeker, background=1, moves=moves_qs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-seeker', kwargs={'pk': test_campaign.pk}), data=form_data)
        
        char = TheSeeker.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'PATRIOT')
        self.assertRedirects(response, reverse('the-seeker-initial-arcana', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))
        
    def test_create_the_seeker_with_witch_hunter_background_redirects_to_initial_arcana_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append("EVERYTHING BLEEDS")
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # WITCH HUNTER background (2)
        form_data = self.generate_create_character_form_data(self.the_seeker, background=2, moves=moves_qs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-seeker', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheSeeker.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'WITCH HUNTER')
        self.assertRedirects(response, reverse('the-seeker-initial-arcana', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))

    def test_create_the_seeker_creates_special_possession_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('POLYGLOT')
        moves_qs = Moves.objects.filter(name__in=moves)
        special_qs = SpecialPossessions.objects.filter(possession_name="Scribe's tools")
        
        form_data = self.generate_create_character_form_data(self.the_seeker, background=0, moves=moves_qs, special_possessions=special_qs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-seeker', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheSeeker.objects.all()[0] # TODO: Find a less hacky way to get the character
        possession1 = SpecialPossessionInstance.objects.get(special_possession__possession_name="Scribe's tools")
        self.assertEqual(list(char.special_possessions.all()), [possession1])
        
    def test_create_the_seeker_creates_moves_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('POLYGLOT')
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # ANITQUARIAN background (0)
        form_data = self.generate_create_character_form_data(self.the_seeker, background=0, moves=moves_qs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-seeker', kwargs={'pk': test_campaign.pk}), data=form_data)

        char = TheSeeker.objects.all()[0] # TODO: Find a less hacky way to get the character
        move_instance_1 = MoveInstance.objects.get(move__name='POLYGLOT')
        move_instance_2 = MoveInstance.objects.get(move__name='WELL VERSED')
        move_instance_3 = MoveInstance.objects.get(move__name="WORK WITH WHAT YOU'VE GOT")
        self.assertEqual(list(char.move_instances.all()), [move_instance_1, move_instance_2, move_instance_3])

    def test_create_the_seeker_without_starting_moves_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_seeker, background=0)
        form_data.pop('move_instances')
        move = Moves.objects.filter(name='ATTUNED')
        form_data['move_instances'] = move
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-seeker', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', field=None, errors=['WELL VERSED is a required starting move.', "WORK WITH WHAT YOU'VE GOT is a required starting move."])
    
    def test_create_the_seeker_restricted_move_raises_error_if_selected(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('CRYPTOLOGIST')
        moves_qs = Moves.objects.filter(name__in=moves)
        # PATRIOT background (1)
        form_data = self.generate_create_character_form_data(self.the_seeker, background=1, moves=moves_qs)
        form_data = self.convert_data_to_foreign_keys(form_data)
        response = self.client.post(reverse('the-seeker', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertFormError(response, 'form', field=None, errors=['CRYPTOLOGIST requires the POLYGLOT move.'])

    def test_create_the_seeker_patriot_background_without_lets_make_a_deal_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # PATRIOT background (1)
        form_data = self.generate_create_character_form_data(self.the_seeker, background=1, moves=moves_qs)
        form_data = self.convert_data_to_foreign_keys(form_data)
        response = self.client.post(reverse('the-seeker', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertFormError(response, 'form', field=None, errors=["LET'S MAKE A DEAL move is required for PATRIOT background."])

    def test_create_the_seeker_antiquarian_background_without_polyglot_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # ANTIQUARIAN background (0)
        form_data = self.generate_create_character_form_data(self.the_seeker, background=0, moves=moves_qs)
        form_data = self.convert_data_to_foreign_keys(form_data)
        response = self.client.post(reverse('the-seeker', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', field=None, errors=['POLYGLOT move is required for ANTIQUARIAN background.'])

    def test_create_the_seeker_witch_hunter_background_without_mental_map_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # WITCH HUNTER background (2)
        form_data = self.generate_create_character_form_data(self.the_seeker, background=2, moves=moves_qs)
        form_data = self.convert_data_to_foreign_keys(form_data)
        response = self.client.post(reverse('the-seeker', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertFormError(response, 'form', field=None, errors=['EVERYTHING BLEEDS move is required for WITCH HUNTER background.'])
