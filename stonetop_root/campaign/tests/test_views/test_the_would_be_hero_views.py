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
    TheWouldBeHero, FearAndAnger
)
from campaign.constants import (
    WOULD_BE_HERO_STARTING_MOVES,
)
from campaign.tests.base import (
    TEST_CAMPAIGN, TEST_USERNAME,
)
from campaign.tests.test_views.base_views import BaseViewsTestClass

User = get_user_model()


class CreateTheWouldBeHeroTests(BaseViewsTestClass):
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
        
        # Set marshal Character class 
        cls.the_would_be_hero = CharacterClass.objects.get(class_name="The Would-Be Hero")
        cls.starting_moves = WOULD_BE_HERO_STARTING_MOVES
        # Generate the form attributes unique to the Would-Be Hero
        fear = FearAndAnger.objects.filter(attribute_type="fear")[0:2]
        fear = [mw.pk for mw in fear]
        anger = FearAndAnger.objects.filter(attribute_type="anger")[0:3]
        anger = [p.pk for p in anger]
        # Generate the form attributes unique to the Marshal
        cls.would_be_hero_kwargs = {
            'fear': fear,
            'anger': anger,
            'trouble': 'Just yesterday.',
            'response': "I said, hey man with the beautiful muscles, don't hurt that patron.",
            'result': "He punched me.",
        }

    def test_create_the_would_be_hero_template_used(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)

        response = self.client.get(f'/campaigns/{test_campaign.pk}/create_the_would_be_hero/')

        self.assertTemplateUsed(response, 'campaign/create_the_would_be_hero.html')

    def test_create_the_would_be_hero_page_redirects_if_not_logged_in(self):
        test_campaign = Campaign.objects.get(name=TEST_CAMPAIGN)

        response = self.client.get(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}))

        self.assertRedirects(response, f'/login/?next=/campaigns/{test_campaign.pk}/create_the_would_be_hero/')

    @skip
    def test_create_the_would_be_hero_redirects_if_campaign_permission_not_met(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser2)
        # TODO: Create Permissions so that users without access to the specific campaign cannot access
        # any of the related pages

        response = self.client.get(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(response.status_code, 403)

    def test_create_the_would_be_hero_all_would_be_hero_backgrounds(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        would_be_hero_backgrounds = list(Background.objects.filter(character_class=self.the_would_be_hero).order_by('background'))
    
        response = self.client.get(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['background'].queryset), would_be_hero_backgrounds)

    def test_create_the_would_be_hero_all_would_be_hero_instincts(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        would_be_hero_instincts = list(Instinct.objects.filter(character_class=self.the_would_be_hero))
    
        response = self.client.get(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['instinct'].queryset), would_be_hero_instincts)

    def test_create_the_would_be_hero_would_be_hero_appearance1(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        would_be_hero_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_would_be_hero).filter(
                attribute_type='appearance1'
            ))
    
        response = self.client.get(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}))

        appearance1 = list(response.context['form'].fields['appearance1'].queryset)
        self.assertEqual(appearance1, would_be_hero_apperances)

    def test_create_the_would_be_hero_would_be_hero_appearance2(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        would_be_hero_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_would_be_hero).filter(
                attribute_type='appearance2'
            ))
    
        response = self.client.get(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}))

        appearance2 = list(response.context['form'].fields['appearance2'].queryset)
        self.assertEqual(appearance2, would_be_hero_apperances)

    def test_create_the_would_be_hero_would_be_hero_appearance3(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        would_be_hero_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_would_be_hero).filter(
                attribute_type='appearance3'
            ))
    
        response = self.client.get(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}))

        appearance3 = list(response.context['form'].fields['appearance3'].queryset)
        self.assertEqual(appearance3, would_be_hero_apperances)

    def test_create_the_would_be_hero_would_be_hero_appearance4(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        would_be_hero_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_would_be_hero).filter(
                attribute_type='appearance4'
            ))
    
        response = self.client.get(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}))

        appearance4 = list(response.context['form'].fields['appearance4'].queryset)
        self.assertEqual(appearance4, would_be_hero_apperances)

    def test_create_the_would_be_hero_all_would_be_hero_places_of_origin(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        would_be_hero_poo = list(PlaceOfOrigin.objects.filter(
            character_class=self.the_would_be_hero).order_by('location'))
    
        response = self.client.get(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}))

        poo = list(response.context['form'].fields['place_of_origin'].queryset)
        self.assertEqual(poo, would_be_hero_poo)

    def test_create_the_would_be_hero_all_would_be_hero_special_possessions(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        possessions = list(SpecialPossessions.objects.filter(
            character_class=self.the_would_be_hero).order_by('possession_name'))
    
        response = self.client.get(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}))

        form_possessions = list(response.context['form'].fields['special_possessions'].queryset)
        self.assertEqual(form_possessions, possessions)

    def test_create_the_would_be_hero_all_would_be_hero_moves(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = list(Moves.objects.filter(
            character_class__class_name=self.the_would_be_hero,
        ).filter(
            move_requirements__level_restricted=None,
        ).order_by(
                F('move_requirements__move_restricted').asc(nulls_first=True), 
                F('move_requirements__level_restricted').asc(nulls_first=True), 
                'name',
        ))
    
        response = self.client.get(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}))

        move_instances = list(response.context['form'].fields['move_instances'].queryset)
        self.assertEqual(moves, move_instances)

    def test_create_the_would_be_hero_actually_creates_a_would_be_hero_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # DRIVEN background (0)
        form_data = self.generate_create_character_form_data(self.the_would_be_hero, background=1, moves=moves_qs, kwargs=self.would_be_hero_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        self.assertEqual(TheWouldBeHero.objects.count(), 1)

    def test_create_the_would_be_hero_with_destined_background_redirects_to_update_background_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)

        # DESTINED background is the first one (0)
        form_data = self.generate_create_character_form_data(self.the_would_be_hero, background=0, moves=moves_qs, kwargs=self.would_be_hero_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheWouldBeHero.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'DESTINED')
        self.assertRedirects(response, reverse('update-background', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            'pk_background': char.background_instance.pk,
            }))
        
    def test_create_the_would_be_hero_with_driven_background_redirects_to_update_background_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # DRIVEN backgroud (1)
        form_data = self.generate_create_character_form_data(self.the_would_be_hero, background=1, moves=moves_qs, kwargs=self.would_be_hero_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}), data=form_data)
        
        char = TheWouldBeHero.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'DRIVEN')
        self.assertRedirects(response, reverse('update-background', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            'pk_background': char.background_instance.pk,
            }))
        
    def test_create_the_would_be_hero_with_impetuous_youth_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # IMPETUOUS YOUTH background (2)
        form_data = self.generate_create_character_form_data(self.the_would_be_hero, background=2, moves=moves_qs, kwargs=self.would_be_hero_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheWouldBeHero.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'IMPETUOUS YOUTH')
        self.assertRedirects(response, reverse('the-would-be-hero-detail', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))

    def test_create_the_would_be_hero_creates_special_possession_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        form_data = self.generate_create_character_form_data(self.the_would_be_hero, background=1, moves=moves_qs, kwargs=self.would_be_hero_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheWouldBeHero.objects.all()[0] # TODO: Find a less hacky way to get the character
        possession1 = SpecialPossessionInstance.objects.get(special_possession__possession_name="A good dog")
        self.assertEqual(list(char.special_possessions.all()), [possession1])
        
    def test_create_the_would_be_hero_creates_moves_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # DRIVEN background (1)
        form_data = self.generate_create_character_form_data(self.the_would_be_hero, background=1, moves=moves_qs, kwargs=self.would_be_hero_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}), data=form_data)

        char = TheWouldBeHero.objects.all()[0] # TODO: Find a less hacky way to get the character
        move_instance_1 = MoveInstance.objects.get(move__name='ANGER IS A GIFT')
        move_instance_2 = MoveInstance.objects.get(move__name='POTENTIAL FOR GREATNESS')
        self.assertEqual(list(char.move_instances.all()), [move_instance_1, move_instance_2])

    def test_create_the_would_be_hero_fear_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_would_be_hero, background=1, kwargs=self.would_be_hero_kwargs)
        form_data.pop('fear')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'fear', ['This field is required.'])
    
    def test_create_the_would_be_hero_anger_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_would_be_hero, background=1, kwargs=self.would_be_hero_kwargs)
        form_data.pop('anger')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'anger', ['This field is required.'])
    
    def test_create_the_would_be_hero_trouble_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_would_be_hero, background=1, kwargs=self.would_be_hero_kwargs)
        form_data.pop('trouble')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'trouble', ['This field is required.'])

    def test_create_the_would_be_hero_response_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_would_be_hero, background=1, kwargs=self.would_be_hero_kwargs)
        form_data.pop('response')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'response', ['This field is required.'])
    
    def test_create_the_would_be_hero_result_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_would_be_hero, background=1, kwargs=self.would_be_hero_kwargs)
        form_data.pop('result')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'result', ['This field is required.'])
    
    def test_create_the_would_be_hero_without_starting_moves_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_would_be_hero, background=0, kwargs=self.would_be_hero_kwargs)
        form_data.pop('move_instances')
        move = Moves.objects.filter(name='UNDERESTIMATED')
        form_data['move_instances'] = move
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', field=None, errors=['ANGER IS A GIFT is a required starting move.', 'POTENTIAL FOR GREATNESS is a required starting move.'])
    
    def test_create_the_would_be_hero_restricted_move_raises_error_if_selected(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('BUT I GET UP AGAIN')
        moves_qs = Moves.objects.filter(name__in=moves)
        # DRIVEN background (1)
        form_data = self.generate_create_character_form_data(self.the_would_be_hero, background=1, moves=moves_qs, kwargs=self.would_be_hero_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)
        response = self.client.post(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertFormError(response, 'form', field=None, errors=['BUT I GET UP AGAIN requires the I GET KNOCKED DOWN move.'])

    def test_create_would_be_hero_character_without_correct_stat_scores_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        form_data = self.generate_create_character_form_data(self.the_would_be_hero, 
            background=0, moves=moves_qs, stats=[1],
            kwargs=self.would_be_hero_kwargs)

        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-would-be-hero', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', field=None, 
            errors=['Stats should have the following scores (they can be in any order): +1, 0, 0, 0, 0, -1. Your stats are as follows: Strength: 2, Dexterity: 1, Intelligence: 1, Wisdom: 0, Constitution: 0, Charisma: -1.'])
