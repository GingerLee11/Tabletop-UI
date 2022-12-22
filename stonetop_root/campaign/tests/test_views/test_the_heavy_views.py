from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Q

from unittest import skip

from campaign.models import (
    Campaign, 
    CharacterClass,
    Background, Instinct, 
    AppearanceAttribute, PlaceOfOrigin, 
    SpecialPossessions, SpecialPossessionInstance, 
    Moves, MoveInstance,
    TheHeavy, HistoryOfViolence,
    MajorArcanaInstance,
)
from campaign.constants import HEAVY_STARTING_MOVES
from campaign.tests.base import (
    TEST_CAMPAIGN, TEST_USERNAME,
)
from campaign.tests.test_views.base_views import BaseViewsTestClass


User = get_user_model()


class CreateTheHeavyTests(BaseViewsTestClass):
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
        
        # Set heavy Character class 
        cls.the_heavy = CharacterClass.objects.get(class_name="The Heavy")
        cls.starting_moves = HEAVY_STARTING_MOVES
        # Generate the form attributes unique to the Heavy
        stories_of_glory = HistoryOfViolence.objects.filter(history_theme="stories of glory")[0:2]
        terrible_stories = HistoryOfViolence.objects.filter(history_theme="terrible stories")[0:2]
        fears = HistoryOfViolence.objects.filter(history_theme="fears")[0:2]
        stories_of_glory = [offering.pk for offering in stories_of_glory]
        terrible_stories = [offering.pk for offering in terrible_stories]
        fears = [offering.pk for offering in fears]
        cls.heavy_kwargs = {
            'stories_of_glory': stories_of_glory,
            'terrible_stories': terrible_stories,
            'fears': fears,
        }

    def test_create_the_heavy_template_used(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)

        response = self.client.get(f'/campaigns/{test_campaign.pk}/create_the_heavy/')

        self.assertTemplateUsed(response, 'campaign/create_the_heavy.html')

    def test_create_the_heavy_page_redirects_if_not_logged_in(self):
        test_campaign = Campaign.objects.get(name=TEST_CAMPAIGN)

        response = self.client.get(reverse('the-heavy', kwargs={'pk': test_campaign.pk}))

        self.assertRedirects(response, f'/login/?next=/campaigns/{test_campaign.pk}/create_the_heavy/')

    @skip
    def test_create_the_heavy_redirects_if_campaign_permission_not_met(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser2)
        # TODO: Create Permissions so that users without access to the specific campaign cannot access
        # any of the related pages

        response = self.client.get(reverse('the-heavy', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(response.status_code, 403)

    def test_create_the_heavy_all_heavy_backgrounds(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        heavy_backgrounds = list(Background.objects.filter(character_class=self.the_heavy).order_by('background'))
    
        response = self.client.get(reverse('the-heavy', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['background'].queryset), heavy_backgrounds)

    def test_create_the_heavy_all_heavy_instincts(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        heavy_instincts = list(Instinct.objects.filter(character_class=self.the_heavy))
    
        response = self.client.get(reverse('the-heavy', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['instinct'].queryset), heavy_instincts)

    def test_create_the_heavy_heavy_appearance1(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        heavy_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_heavy).filter(
                attribute_type='appearance1'
            ))
    
        response = self.client.get(reverse('the-heavy', kwargs={'pk': test_campaign.pk}))

        appearance1 = list(response.context['form'].fields['appearance1'].queryset)
        self.assertEqual(appearance1, heavy_apperances)

    def test_create_the_heavy_heavy_appearance2(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        heavy_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_heavy).filter(
                attribute_type='appearance2'
            ))
    
        response = self.client.get(reverse('the-heavy', kwargs={'pk': test_campaign.pk}))

        appearance2 = list(response.context['form'].fields['appearance2'].queryset)
        self.assertEqual(appearance2, heavy_apperances)

    def test_create_the_heavy_heavy_appearance3(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        heavy_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_heavy).filter(
                attribute_type='appearance3'
            ))
    
        response = self.client.get(reverse('the-heavy', kwargs={'pk': test_campaign.pk}))

        appearance3 = list(response.context['form'].fields['appearance3'].queryset)
        self.assertEqual(appearance3, heavy_apperances)

    def test_create_the_heavy_heavy_appearance4(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        heavy_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_heavy).filter(
                attribute_type='appearance4'
            ))
    
        response = self.client.get(reverse('the-heavy', kwargs={'pk': test_campaign.pk}))

        appearance4 = list(response.context['form'].fields['appearance4'].queryset)
        self.assertEqual(appearance4, heavy_apperances)

    def test_create_the_heavy_all_heavy_places_of_origin(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        heavy_poo = list(PlaceOfOrigin.objects.filter(
            character_class=self.the_heavy).order_by('location'))
    
        response = self.client.get(reverse('the-heavy', kwargs={'pk': test_campaign.pk}))

        poo = list(response.context['form'].fields['place_of_origin'].queryset)
        self.assertEqual(poo, heavy_poo)

    def test_create_the_heavy_all_heavy_special_possessions(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        possessions = list(SpecialPossessions.objects.filter(
            character_class=self.the_heavy).order_by('possession_name'))
    
        response = self.client.get(reverse('the-heavy', kwargs={'pk': test_campaign.pk}))

        form_possessions = list(response.context['form'].fields['special_possessions'].queryset)
        self.assertEqual(form_possessions, possessions)

    def test_create_the_heavy_all_heavy_moves(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = list(Moves.objects.filter(
            character_class__class_name=self.the_heavy
            ).filter(
                move_requirements__level_restricted__isnull=True
                ).order_by('name'))
    
        response = self.client.get(reverse('the-heavy', kwargs={'pk': test_campaign.pk}))

        move_instances = list(response.context['form'].fields['move_instances'].queryset)
        self.assertEqual(moves, move_instances)

    def test_create_the_heavy_actually_creates_a_heavy_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('ARMORED')
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # SHERIFF background is the first one (0)
        form_data = self.generate_create_character_form_data(self.the_heavy, background=0, moves=moves_qs, kwargs=self.heavy_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-heavy', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        self.assertEqual(TheHeavy.objects.count(), 1)

    def test_create_the_heavy_with_sheriff_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('ARMORED')
        moves_qs = Moves.objects.filter(name__in=moves)

        # SHERIFF background is the first one (0)
        form_data = self.generate_create_character_form_data(self.the_heavy, background=0, moves=moves_qs, kwargs=self.heavy_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-heavy', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheHeavy.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'SHERIFF')
        self.assertRedirects(response, reverse('the-heavy-detail', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))
        
    def test_create_the_heavy_with_blood_soaked_past_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('UNCANNY REFLEXES')
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # BLOOD-SOAKED PAST backgroud (1)
        form_data = self.generate_create_character_form_data(self.the_heavy, background=1, moves=moves_qs, kwargs=self.heavy_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-heavy', kwargs={'pk': test_campaign.pk}), data=form_data)
        
        char = TheHeavy.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'BLOOD-SOAKED PAST')
        self.assertRedirects(response, reverse('the-heavy-detail', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))
        
    def test_create_the_heavy_with_storm_marked_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('ARMORED')
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # STORM-MARKED background (2)
        form_data = self.generate_create_character_form_data(self.the_heavy, background=2, moves=moves_qs, kwargs=self.heavy_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-heavy', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheHeavy.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'STORM-MARKED')
        self.assertRedirects(response, reverse('the-heavy-detail', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))

    def test_create_the_heavy_creates_special_possession_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('ARMORED')
        moves_qs = Moves.objects.filter(name__in=moves)
        
        form_data = self.generate_create_character_form_data(self.the_heavy, background=0, moves=moves_qs, kwargs=self.heavy_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-heavy', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheHeavy.objects.all()[0] # TODO: Find a less hacky way to get the character
        possession = SpecialPossessionInstance.objects.get(special_possession__possession_name="Chirurgeon's tools")
        self.assertEqual(list(char.special_possessions.all()), [possession])
        
    def test_create_the_heavy_creates_moves_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('ARMORED')
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # SHERIFF background (0)
        form_data = self.generate_create_character_form_data(self.the_heavy, background=0, moves=moves_qs, kwargs=self.heavy_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-heavy', kwargs={'pk': test_campaign.pk}), data=form_data)

        char = TheHeavy.objects.all()[0] # TODO: Find a less hacky way to get the character
        move_instance_1 = MoveInstance.objects.get(move__name='ARMORED')
        move_instance_2 = MoveInstance.objects.get(move__name='DANGEROUS')
        move_instance_3 = MoveInstance.objects.get(move__name='HARD TO KILL')
        self.assertEqual(list(char.move_instances.all()), [move_instance_1, move_instance_2, move_instance_3])

    def test_create_the_heavy_stories_of_glory_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_heavy, background=0, kwargs=self.heavy_kwargs)
        form_data.pop('stories_of_glory')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-heavy', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'stories_of_glory', ['This field is required.'])
          
    def test_create_the_heavy_terrible_stories_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_heavy, background=0, kwargs=self.heavy_kwargs)
        form_data.pop('terrible_stories')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-heavy', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'terrible_stories', ['This field is required.'])
          
    def test_create_the_heavy_fears_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_heavy, background=0, kwargs=self.heavy_kwargs)
        form_data.pop('fears')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-heavy', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'fears', ['This field is required.'])
        
    def test_create_the_heavy_storm_marked_background_creates_storm_markings_arcanum_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('ARMORED')
        moves_qs = Moves.objects.filter(name__in=moves)
            
        form_data = self.generate_create_character_form_data(self.the_heavy, background=2, moves=moves_qs, kwargs=self.heavy_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-heavy', kwargs={'pk': test_campaign.pk}), data=form_data)

        char = TheHeavy.objects.all()[0] # TODO: Find a less hacky way to get the character
        storm_markings = MajorArcanaInstance.objects.get(arcana__name="Storm Markings")
        self.assertEqual(list(char.major_arcana.all()), [storm_markings])

    def test_create_the_heavy_without_either_armored_or_uncanny_reflexes_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        form_data = self.generate_create_character_form_data(self.the_heavy, background=0, moves=moves_qs, kwargs=self.heavy_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-heavy', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertFormError(response, 'form', field=None, errors=['ARMORED or UNCANNY REFLEXES move is required for The Heavy.'])
        