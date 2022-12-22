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
    TheJudge, SymbolOfAuthority, 
    TheChronical, DemandsOfAratis
)
from campaign.constants import (
    JUDGE_STARTING_MOVES, SHRINE_OF_ARATIS,
)
from campaign.tests.base import (
    TEST_CAMPAIGN, TEST_USERNAME,
)
from campaign.tests.test_views.base_views import BaseViewsTestClass

User = get_user_model()


class CreateTheJudgeTests(BaseViewsTestClass):
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
        
        # Set judge Character class 
        cls.the_judge = CharacterClass.objects.get(class_name="The Judge")
        cls.starting_moves = JUDGE_STARTING_MOVES
        cls.starting_possessions = ["Scribe's tools"]
        # Generate the form attributes unique to the Judge
        chronical_positives = TheChronical.objects.filter(attribute_type__iexact="positive")[0:3]
        chronical_positives = [cp.pk for cp in chronical_positives]
        chronical_negatives = TheChronical.objects.filter(attribute_type__iexact="negative")[0:3]
        chronical_negatives = [cn.pk for cn in chronical_negatives]
        demands = DemandsOfAratis.objects.all()[0:3]
        demands = [d.pk for d in demands]
        cls.judge_kwargs = {
            'symbol_of_authority': SymbolOfAuthority.objects.get(symbol__icontains="Makerglass").pk,
            'chronical_positives': chronical_positives,
            'chronical_negatives': chronical_negatives,
            'shrine_of_aratis': SHRINE_OF_ARATIS[0][0],
            'demands_of_aratis': demands,
        }

    def test_create_the_judge_template_used(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)

        response = self.client.get(f'/campaigns/{test_campaign.pk}/create_the_judge/')

        self.assertTemplateUsed(response, 'campaign/create_the_judge.html')

    def test_create_the_judge_page_redirects_if_not_logged_in(self):
        test_campaign = Campaign.objects.get(name=TEST_CAMPAIGN)

        response = self.client.get(reverse('the-judge', kwargs={'pk': test_campaign.pk}))

        self.assertRedirects(response, f'/login/?next=/campaigns/{test_campaign.pk}/create_the_judge/')

    @skip
    def test_create_the_judge_redirects_if_campaign_permission_not_met(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser2)
        # TODO: Create Permissions so that users without access to the specific campaign cannot access
        # any of the related pages

        response = self.client.get(reverse('the-judge', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(response.status_code, 403)

    def test_create_the_judge_all_judge_backgrounds(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        judge_backgrounds = list(Background.objects.filter(character_class=self.the_judge))
    
        response = self.client.get(reverse('the-judge', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['background'].queryset), judge_backgrounds)

    def test_create_the_judge_all_judge_instincts(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        judge_instincts = list(Instinct.objects.filter(character_class=self.the_judge))
    
        response = self.client.get(reverse('the-judge', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['instinct'].queryset), judge_instincts)

    def test_create_the_judge_judge_appearance1(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        judge_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_judge).filter(
                attribute_type='appearance1'
            ))
    
        response = self.client.get(reverse('the-judge', kwargs={'pk': test_campaign.pk}))

        appearance1 = list(response.context['form'].fields['appearance1'].queryset)
        self.assertEqual(appearance1, judge_apperances)

    def test_create_the_judge_judge_appearance2(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        judge_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_judge).filter(
                attribute_type='appearance2'
            ))
    
        response = self.client.get(reverse('the-judge', kwargs={'pk': test_campaign.pk}))

        appearance2 = list(response.context['form'].fields['appearance2'].queryset)
        self.assertEqual(appearance2, judge_apperances)

    def test_create_the_judge_judge_appearance3(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        judge_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_judge).filter(
                attribute_type='appearance3'
            ))
    
        response = self.client.get(reverse('the-judge', kwargs={'pk': test_campaign.pk}))

        appearance3 = list(response.context['form'].fields['appearance3'].queryset)
        self.assertEqual(appearance3, judge_apperances)

    def test_create_the_judge_judge_appearance4(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        judge_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_judge).filter(
                attribute_type='appearance4'
            ))
    
        response = self.client.get(reverse('the-judge', kwargs={'pk': test_campaign.pk}))

        appearance4 = list(response.context['form'].fields['appearance4'].queryset)
        self.assertEqual(appearance4, judge_apperances)

    def test_create_the_judge_all_judge_places_of_origin(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        judge_poo = list(PlaceOfOrigin.objects.filter(
            character_class=self.the_judge).order_by('location'))
    
        response = self.client.get(reverse('the-judge', kwargs={'pk': test_campaign.pk}))

        poo = list(response.context['form'].fields['place_of_origin'].queryset)
        self.assertEqual(poo, judge_poo)

    def test_create_the_judge_all_judge_special_possessions(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        possessions = list(SpecialPossessions.objects.filter(
            character_class=self.the_judge).order_by('possession_name'))
    
        response = self.client.get(reverse('the-judge', kwargs={'pk': test_campaign.pk}))

        form_possessions = list(response.context['form'].fields['special_possessions'].queryset)
        self.assertEqual(form_possessions, possessions)

    def test_create_the_judge_all_judge_moves(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = list(Moves.objects.filter(
            character_class__class_name=self.the_judge,
        ).filter(
            move_requirements__level_restricted=None,
        ).order_by(
                F('move_requirements__move_restricted').asc(nulls_first=True), 
                F('move_requirements__level_restricted').asc(nulls_first=True), 
                'name',
        ))
    
        response = self.client.get(reverse('the-judge', kwargs={'pk': test_campaign.pk}))

        move_instances = list(response.context['form'].fields['move_instances'].queryset)
        self.assertEqual(moves, move_instances)

    def test_create_the_judge_actually_creates_a_judge_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # LEGACY background is the first one (0)
        form_data = self.generate_create_character_form_data(self.the_judge, background=0, moves=moves_qs, kwargs=self.judge_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-judge', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        self.assertEqual(TheJudge.objects.count(), 1)

    def test_create_the_judge_with_legacy_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)

        # LEGACY background is the first one (0)
        form_data = self.generate_create_character_form_data(self.the_judge, background=0, moves=moves_qs, kwargs=self.judge_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-judge', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheJudge.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'LEGACY')
        self.assertRedirects(response, reverse('the-judge-detail', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))
        
    def test_create_the_judge_with_missionary_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # MISSIONARY backgroud (1)
        form_data = self.generate_create_character_form_data(self.the_judge, background=1, moves=moves_qs, kwargs=self.judge_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-judge', kwargs={'pk': test_campaign.pk}), data=form_data)
        
        char = TheJudge.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'MISSIONARY')
        self.assertRedirects(response, reverse('the-judge-detail', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))
        
    def test_create_the_judge_with_prophet_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # PROPHET background (2)
        form_data = self.generate_create_character_form_data(self.the_judge, background=2, moves=moves_qs, kwargs=self.judge_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-judge', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheJudge.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'PROPHET')
        self.assertRedirects(response, reverse('the-judge-detail', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))

    def test_create_the_judge_creates_special_possession_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        special_possessions = self.starting_possessions
        special_possessions.append('Aviary')
        sp_qs = SpecialPossessions.objects.filter(possession_name__in=special_possessions)
        moves_qs = Moves.objects.filter(name__in=moves)
        
        form_data = self.generate_create_character_form_data(self.the_judge, background=0, moves=moves_qs, special_possessions=sp_qs, kwargs=self.judge_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-judge', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheJudge.objects.all()[0] # TODO: Find a less hacky way to get the character
        possession1 = SpecialPossessionInstance.objects.get(special_possession__possession_name="Aviary")
        possession2 = SpecialPossessionInstance.objects.get(special_possession__possession_name="Scribe's tools")
        self.assertEqual(list(char.special_possessions.all()), [possession1, possession2])
        
    def test_create_the_judge_creates_moves_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # LEGACY background (0)
        form_data = self.generate_create_character_form_data(self.the_judge, background=0, moves=moves_qs, kwargs=self.judge_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-judge', kwargs={'pk': test_campaign.pk}), data=form_data)

        char = TheJudge.objects.all()[0] # TODO: Find a less hacky way to get the character
        move_instance_1 = MoveInstance.objects.get(move__name='CENSURE')
        move_instance_2 = MoveInstance.objects.get(move__name='CHRONICLER OF STONETOP')
        self.assertEqual(list(char.move_instances.all()), [move_instance_1, move_instance_2])

    def test_create_the_judge_symbol_of_authority_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_judge, background=0, kwargs=self.judge_kwargs)
        form_data.pop('symbol_of_authority')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-judge', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'symbol_of_authority', ['This field is required.'])
          
    def test_create_the_judge_chronical_positives_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_judge, background=0, kwargs=self.judge_kwargs)
        form_data.pop('chronical_positives')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-judge', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'chronical_positives', ['This field is required.'])
    
    def test_create_the_judge_chronical_negatives_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_judge, background=0, kwargs=self.judge_kwargs)
        form_data.pop('chronical_negatives')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-judge', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'chronical_negatives', ['This field is required.'])    
    
    def test_create_the_judge_shrine_of_aratis_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_judge, background=0, kwargs=self.judge_kwargs)
        form_data.pop('shrine_of_aratis')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-judge', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'shrine_of_aratis', ['This field is required.'])
    
    def test_create_the_judge_demands_of_aratis_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_judge, background=0, kwargs=self.judge_kwargs)
        form_data.pop('demands_of_aratis')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-judge', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'demands_of_aratis', ['This field is required.'])
    
    def test_create_the_judge_without_starting_moves_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_judge, background=0, kwargs=self.judge_kwargs)
        form_data.pop('move_instances')
        move = Moves.objects.filter(name='ARMORED')
        form_data['move_instances'] = move
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-judge', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', field=None, errors=['CENSURE is a required starting move.', 'CHRONICLER OF STONETOP is a required starting move.'])
    
    def test_create_the_judge_restricted_moves_raise_errors_if_selected(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('LIKE A DOG WITH A BONE')
        moves.append('A BUNDLE OF STICKS UNBROKEN')
        moves.append('BINDING ARBITRATION')
        moves_qs = Moves.objects.filter(name__in=moves)

        form_data = self.generate_create_character_form_data(self.the_judge, background=0, moves=moves_qs, kwargs=self.judge_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)
        response = self.client.post(reverse('the-judge', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertFormError(response, 'form', field=None, 
            errors=[
                'LIKE A DOG WITH A BONE requires the HOUND OF ARATIS move.',
                'A BUNDLE OF STICKS UNBROKEN requires the MANY HANDS MAKE LIGHT WORK move.',
                'BINDING ARBITRATION requires the TRUTH OR CONSEQUENCES move.',
            ])
