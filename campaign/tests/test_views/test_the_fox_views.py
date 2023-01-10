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
    TheFox, TallTales,
)
from campaign.constants import (
    TALE_OPENING, TALE_ENDINGS, 
)
from campaign.tests.base import (
    TEST_CAMPAIGN, TEST_USERNAME,
)
from campaign.tests.test_views.base_views import BaseViewsTestClass


User = get_user_model()


class CreateTheFoxTests(BaseViewsTestClass):
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
        
        # Set fox Character class 
        cls.the_fox = CharacterClass.objects.get(class_name="The Fox")

    def test_create_the_fox_template_used(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)

        response = self.client.get(f'/campaigns/{test_campaign.pk}/create_the_fox/')

        self.assertTemplateUsed(response, 'campaign/create_the_fox.html')

    def test_create_the_fox_page_redirects_if_not_logged_in(self):
        test_campaign = Campaign.objects.get(name=TEST_CAMPAIGN)

        response = self.client.get(reverse('the-fox', kwargs={'pk': test_campaign.pk}))

        self.assertRedirects(response, f'/login/?next=/campaigns/{test_campaign.pk}/create_the_fox/')

    @skip
    def test_create_the_fox_redirects_if_campaign_permission_not_met(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser2)
        # TODO: Create Permissions so that users without access to the specific campaign cannot access
        # any of the related pages

        response = self.client.get(reverse('the-fox', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(response.status_code, 403)

    def test_create_the_fox_all_fox_backgrounds(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        fox_backgrounds = list(Background.objects.filter(character_class=self.the_fox).order_by('background'))
    
        response = self.client.get(reverse('the-fox', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['background'].queryset), fox_backgrounds)

    def test_create_the_fox_all_fox_instincts(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        fox_instincts = list(Instinct.objects.filter(character_class=self.the_fox))
    
        response = self.client.get(reverse('the-fox', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['instinct'].queryset), fox_instincts)

    def test_create_the_fox_fox_appearance1(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        fox_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_fox).filter(
                attribute_type='appearance1'
            ))
    
        response = self.client.get(reverse('the-fox', kwargs={'pk': test_campaign.pk}))

        appearance1 = list(response.context['form'].fields['appearance1'].queryset)
        self.assertEqual(appearance1, fox_apperances)

    def test_create_the_fox_fox_appearance2(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        fox_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_fox).filter(
                attribute_type='appearance2'
            ))
    
        response = self.client.get(reverse('the-fox', kwargs={'pk': test_campaign.pk}))

        appearance2 = list(response.context['form'].fields['appearance2'].queryset)
        self.assertEqual(appearance2, fox_apperances)

    def test_create_the_fox_fox_appearance3(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        fox_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_fox).filter(
                attribute_type='appearance3'
            ))
    
        response = self.client.get(reverse('the-fox', kwargs={'pk': test_campaign.pk}))

        appearance3 = list(response.context['form'].fields['appearance3'].queryset)
        self.assertEqual(appearance3, fox_apperances)

    def test_create_the_fox_fox_appearance4(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        fox_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_fox).filter(
                attribute_type='appearance4'
            ))
    
        response = self.client.get(reverse('the-fox', kwargs={'pk': test_campaign.pk}))

        appearance4 = list(response.context['form'].fields['appearance4'].queryset)
        self.assertEqual(appearance4, fox_apperances)

    def test_create_the_fox_all_fox_places_of_origin(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        fox_poo = list(PlaceOfOrigin.objects.filter(
            character_class=self.the_fox).order_by('location'))
    
        response = self.client.get(reverse('the-fox', kwargs={'pk': test_campaign.pk}))

        poo = list(response.context['form'].fields['place_of_origin'].queryset)
        self.assertEqual(poo, fox_poo)

    def test_create_the_fox_all_fox_special_possessions(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        possessions = list(SpecialPossessions.objects.filter(
            character_class=self.the_fox).order_by('possession_name'))
    
        response = self.client.get(reverse('the-fox', kwargs={'pk': test_campaign.pk}))

        form_possessions = list(response.context['form'].fields['special_possessions'].queryset)
        self.assertEqual(form_possessions, possessions)

    def test_create_the_fox_all_fox_moves(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = list(Moves.objects.filter(
            character_class__class_name=self.the_fox,
        ).filter(
            move_requirements__level_restricted=None,
        ).order_by(
                F('move_requirements__move_restricted').asc(nulls_first=True), 
                F('move_requirements__level_restricted').asc(nulls_first=True), 
                'name',
        ))
    
        response = self.client.get(reverse('the-fox', kwargs={'pk': test_campaign.pk}))
        move_instances = list(response.context['form'].fields['move_instances'].queryset)
        self.assertEqual(moves, move_instances)

    def test_create_the_fox_actually_creates_a_fox_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = ['ALL IN THE WRIST', 'AMBUSH', 'DANGER SENSE']
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # The Natural background (1)
        form_data = self.generate_create_character_form_data(self.the_fox, moves=moves_qs, background=1)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-fox', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        self.assertEqual(TheFox.objects.count(), 1)

    def test_create_the_fox_with_the_natural_background_redirects_to_tall_tales_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = ['ALL IN THE WRIST', 'AMBUSH', 'DANGER SENSE']
        moves_qs = Moves.objects.filter(name__in=moves)

        # The Natural background is the first one (0)
        form_data = self.generate_create_character_form_data(self.the_fox, moves=moves_qs, background=1)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-fox', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheFox.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'THE NATURAL')
        self.assertRedirects(response, reverse('add-tall-tale', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))
        
    def test_create_the_fox_with_a_life_of_crime_background_redirects_to_tall_tales_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = ['ALL IN THE WRIST', 'AMBUSH', 'DANGER SENSE', 'BURGLE']
        moves_qs = Moves.objects.filter(name__in=moves)

        # Raised by wolves should be the second one
        form_data = self.generate_create_character_form_data(self.the_fox, moves=moves_qs, background=0)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-fox', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        
        char = TheFox.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'A LIFE OF CRIME')
        self.assertRedirects(response, reverse('add-tall-tale', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))
        
    def test_create_the_fox_with_the_prodigal_returned_background_redirects_to_tall_tales_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = ['ALL IN THE WRIST', 'AMBUSH', 'DANGER SENSE']
        moves_qs = Moves.objects.filter(name__in=moves)

        # THE PRODIGAL RETURNED background (2)
        form_data = self.generate_create_character_form_data(self.the_fox, moves=moves_qs, background=2)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-fox', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheFox.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'THE PRODIGAL RETURNED')
        self.assertRedirects(response, reverse('add-tall-tale', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))

    def test_create_the_fox_creates_special_possession_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = ['ALL IN THE WRIST', 'AMBUSH', 'DANGER SENSE']
        moves_qs = Moves.objects.filter(name__in=moves)

        form_data = self.generate_create_character_form_data(self.the_fox, moves=moves_qs, background=1)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-fox', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheFox.objects.all()[0] # TODO: Find a less hacky way to get the character
        burglary_kit = SpecialPossessionInstance.objects.get(special_possession__possession_name='Burglary Kit')
        self.assertEqual(list(char.special_possessions.all()), [burglary_kit])
        
    def test_create_the_fox_creates_moves_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = ['ALL IN THE WRIST', 'AMBUSH', 'DANGER SENSE']
        moves_qs = Moves.objects.filter(name__in=moves)

        form_data = self.generate_create_character_form_data(self.the_fox, moves=moves_qs, background=1)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-fox', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheFox.objects.all()[0] # TODO: Find a less hacky way to get the character
        all_in_the_wrist = MoveInstance.objects.get(move__name='ALL IN THE WRIST')
        ambush = MoveInstance.objects.get(move__name='AMBUSH')
        danger_sense = MoveInstance.objects.get(move__name='DANGER SENSE')
        self.assertEqual(list(char.move_instances.all()), [all_in_the_wrist, ambush, danger_sense])

    def test_fox_without_ambush_or_skill_at_arms_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = ['ALL IN THE WRIST', 'DANGER SENSE']
        moves_qs = Moves.objects.filter(name__in=moves)
                
        # THE NATURAL background (1)
        form_data = self.generate_create_character_form_data(self.the_fox, background=1, moves=moves_qs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-fox', kwargs={'pk': test_campaign.pk}), data=form_data)
        
        self.assertFormError(response, 'form', field=None, errors=['AMBUSH or SKILL AT ARMS move is required.'])

    def test_fox_without_danger_sense_or_perceptive_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = ['ALL IN THE WRIST', 'AMBUSH']
        moves_qs = Moves.objects.filter(name__in=moves)
                
        # THE NATURAL background (1)
        form_data = self.generate_create_character_form_data(self.the_fox, background=1, moves=moves_qs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-fox', kwargs={'pk': test_campaign.pk}), data=form_data)
        
        self.assertFormError(response, 'form', field=None, errors=['DANGER SENSE or PERCEPTIVE move is required.'])

    def test_fox_with_a_life_of_crime_background_without_burgle_or_light_fingers_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = ['ALL IN THE WRIST', 'AMBUSH', 'DANGER SENSE']
        moves_qs = Moves.objects.filter(name__in=moves)
                
        # A LIFE OF CRIME background (0)
        form_data = self.generate_create_character_form_data(self.the_fox, background=0, moves=moves_qs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-fox', kwargs={'pk': test_campaign.pk}), data=form_data)
        
        self.assertFormError(response, 'form', field=None, errors=['BURGLE or LIGHT FINGERS move is required with A LIFE OF CRIME background.'])

    def test_create_the_fox_parry_and_riposte_without_skill_at_arms_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = ['AMBUSH', 'DANGER SENSE', 'PARRY & RIPOSTE']
        moves_qs = Moves.objects.filter(name__in=moves)

        form_data = self.generate_create_character_form_data(self.the_fox, background=1, moves=moves_qs)
        form_data = self.convert_data_to_foreign_keys(form_data)
        response = self.client.post(reverse('the-fox', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertFormError(response, 'form', field=None, errors=['PARRY & RIPOSTE requires the SKILL AT ARMS move.'])



class TallTalesTest(BaseViewsTestClass):
    """
    This test suite will test the fox creating tall tales after creating a character.
    """
    # TODO: Test Tall Tales



class TheFoxDetailTests(BaseViewsTestClass):
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
        
        # Set Fox Character class 
        cls.the_fox = CharacterClass.objects.get(class_name="The Fox")

    def create_the_natural_background_fox(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = ['AMBUSH', 'CATLIKE', 'DANGER SENSE']
        moves_qs = Moves.objects.filter(name__in=moves)
        possessions = ['Hidden stash', 'Tannery']
        sp_qs = SpecialPossessions.objects.filter(possession_name__in=possessions)
        
        form_data = self.generate_create_character_form_data(
            self.the_fox, background=1, STR=0, DEX=2, INT=1, WIS=0, CON=-1, CHA=1, 
            moves=moves_qs, special_possessions=sp_qs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-fox', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheFox.objects.all()[0] 
        return test_campaign, char        

    def test_the_fox_detail_page_uses_correct_template(self):
        campaign, fox = self.create_the_natural_background_fox()

        response = self.client.get(f'/campaigns/{campaign.pk}/{fox.pk}/the_fox_home/')

        self.assertTemplateUsed(response, 'campaign/the_fox_detail.html')

    def test_the_fox_update_moves_uses_correct_template(self):
        campaign, fox = self.create_the_natural_background_fox()

        response = self.client.get(f'/campaigns/{campaign.pk}/{fox.pk}/moves/update/')

        self.assertTemplateUsed(response, 'campaign/update_moves.html')

    def test_the_fox_update_moves_doesnt_show_any_initial_moves(self):
        campaign, fox = self.create_the_natural_background_fox()

        response = self.client.get(f'/campaigns/{campaign.pk}/{fox.pk}/moves/update/')

        initial_moves = response.context['form'].fields['move_instances'].initial
        self.assertEqual(initial_moves, None)

    def test_the_fox_all_fox_moves(self):
        campaign, fox = self.create_the_natural_background_fox()
        starting_moves = ['AMBUSH', 'CATLIKE', 'DANGER SENSE']
        moves = list(Moves.objects.filter(
            character_class=self.the_fox).exclude(
                name__in=starting_moves
            ).order_by(
                F('move_requirements__level_restricted').asc(nulls_first=True), 
                F('move_requirements__move_restricted').asc(nulls_first=True), 
                'name'
                ))

        response = self.client.get(f'/campaigns/{campaign.pk}/{fox.pk}/moves/update/')

        move_instances = list(response.context['form'].fields['move_instances'].queryset)
        self.assertEqual(moves, move_instances)

