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
    TheMarshal, Tags
)
from campaign.constants import (
    MARSHAL_STARTING_MOVES,
    WAR_STORIES, MARSHAL_CREW_TAGS,
)
from campaign.tests.base import (
    TEST_CAMPAIGN, TEST_USERNAME,
)
from campaign.tests.test_views.base_views import BaseViewsTestClass

User = get_user_model()


class CreateTheMarshalTests(BaseViewsTestClass):
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
        cls.the_marshal = CharacterClass.objects.get(class_name="The Marshal")
        cls.starting_moves = MARSHAL_STARTING_MOVES
        # Generate the form attributes unique to the Marshal
        cls.marshal_kwargs = {
            'war_story': WAR_STORIES[0][0],
            'war_detail_1': 'Four score, 25 years in the past.',
            'war_detail_3': 'I saved the union with my beard.',
            'war_detail_7': "Those dang corrupted crinwin, so now I'm back to kick some ass.",
        }

    def test_create_the_marshal_template_used(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)

        response = self.client.get(f'/campaigns/{test_campaign.pk}/create_the_marshal/')

        self.assertTemplateUsed(response, 'campaign/create_the_marshal.html')

    def test_create_the_marshal_page_redirects_if_not_logged_in(self):
        test_campaign = Campaign.objects.get(name=TEST_CAMPAIGN)

        response = self.client.get(reverse('the-marshal', kwargs={'pk': test_campaign.pk}))

        self.assertRedirects(response, f'/login/?next=/campaigns/{test_campaign.pk}/create_the_marshal/')

    @skip
    def test_create_the_marshal_redirects_if_campaign_permission_not_met(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser2)
        # TODO: Create Permissions so that users without access to the specific campaign cannot access
        # any of the related pages

        response = self.client.get(reverse('the-marshal', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(response.status_code, 403)

    def test_create_the_marshal_all_marshal_backgrounds(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        marshal_backgrounds = list(Background.objects.filter(character_class=self.the_marshal).order_by('background'))
    
        response = self.client.get(reverse('the-marshal', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['background'].queryset), marshal_backgrounds)

    def test_create_the_marshal_all_marshal_instincts(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        marshal_instincts = list(Instinct.objects.filter(character_class=self.the_marshal))
    
        response = self.client.get(reverse('the-marshal', kwargs={'pk': test_campaign.pk}))

        self.assertEqual(list(response.context['form'].fields['instinct'].queryset), marshal_instincts)

    def test_create_the_marshal_marshal_appearance1(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        marshal_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_marshal).filter(
                attribute_type='appearance1'
            ))
    
        response = self.client.get(reverse('the-marshal', kwargs={'pk': test_campaign.pk}))

        appearance1 = list(response.context['form'].fields['appearance1'].queryset)
        self.assertEqual(appearance1, marshal_apperances)

    def test_create_the_marshal_marshal_appearance2(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        marshal_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_marshal).filter(
                attribute_type='appearance2'
            ))
    
        response = self.client.get(reverse('the-marshal', kwargs={'pk': test_campaign.pk}))

        appearance2 = list(response.context['form'].fields['appearance2'].queryset)
        self.assertEqual(appearance2, marshal_apperances)

    def test_create_the_marshal_marshal_appearance3(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        marshal_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_marshal).filter(
                attribute_type='appearance3'
            ))
    
        response = self.client.get(reverse('the-marshal', kwargs={'pk': test_campaign.pk}))

        appearance3 = list(response.context['form'].fields['appearance3'].queryset)
        self.assertEqual(appearance3, marshal_apperances)

    def test_create_the_marshal_marshal_appearance4(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        marshal_apperances = list(AppearanceAttribute.objects.filter(
            character_class=self.the_marshal).filter(
                attribute_type='appearance4'
            ))
    
        response = self.client.get(reverse('the-marshal', kwargs={'pk': test_campaign.pk}))

        appearance4 = list(response.context['form'].fields['appearance4'].queryset)
        self.assertEqual(appearance4, marshal_apperances)

    def test_create_the_marshal_all_marshal_places_of_origin(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        marshal_poo = list(PlaceOfOrigin.objects.filter(
            character_class=self.the_marshal).order_by('location'))
    
        response = self.client.get(reverse('the-marshal', kwargs={'pk': test_campaign.pk}))

        poo = list(response.context['form'].fields['place_of_origin'].queryset)
        self.assertEqual(poo, marshal_poo)

    def test_create_the_marshal_all_marshal_special_possessions(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        possessions = list(SpecialPossessions.objects.filter(
            character_class=self.the_marshal).order_by('possession_name'))
    
        response = self.client.get(reverse('the-marshal', kwargs={'pk': test_campaign.pk}))

        form_possessions = list(response.context['form'].fields['special_possessions'].queryset)
        self.assertEqual(form_possessions, possessions)

    def test_create_the_marshal_all_marshal_moves(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = list(Moves.objects.filter(
            character_class__class_name=self.the_marshal,
        ).filter(
            move_requirements__level_restricted=None,
        ).order_by(
                F('move_requirements__move_restricted').asc(nulls_first=True), 
                F('move_requirements__level_restricted').asc(nulls_first=True), 
                'name',
        ))
    
        response = self.client.get(reverse('the-marshal', kwargs={'pk': test_campaign.pk}))

        move_instances = list(response.context['form'].fields['move_instances'].queryset)
        self.assertEqual(moves, move_instances)

    def test_create_the_marshal_actually_creates_a_marshal_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # PENITENT background (0)
        form_data = self.generate_create_character_form_data(self.the_marshal, background=1, moves=moves_qs, kwargs=self.marshal_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-marshal', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        self.assertEqual(TheMarshal.objects.count(), 1)

    def test_create_the_marshal_with_luminary_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('WE HAPPY FEW')
        moves_qs = Moves.objects.filter(name__in=moves)

        # LUMINARY background is the first one (0)
        form_data = self.generate_create_character_form_data(self.the_marshal, background=0, moves=moves_qs, kwargs=self.marshal_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-marshal', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheMarshal.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'LUMINARY')
        self.assertRedirects(response, reverse('character-create-crew', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))
        
    def test_create_the_marshal_with_penitent_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # PENITENT backgroud (1)
        form_data = self.generate_create_character_form_data(self.the_marshal, background=1, moves=moves_qs, kwargs=self.marshal_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-marshal', kwargs={'pk': test_campaign.pk}), data=form_data)
        
        char = TheMarshal.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'PENITENT')
        self.assertRedirects(response, reverse('character-create-crew', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))
        
    def test_create_the_marshal_with_scion_background_redirects_to_home_page(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('VETERAN CREW')
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # SCION background (2)
        form_data = self.generate_create_character_form_data(self.the_marshal, background=2, moves=moves_qs, kwargs=self.marshal_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-marshal', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheMarshal.objects.all()[0] # TODO: Find a less hacky way to get the character
        self.assertEqual(char.background_instance.background.background, 'SCION')
        self.assertRedirects(response, reverse('character-create-crew', kwargs={
            'pk': test_campaign.pk, 
            'pk_char': char.pk,
            }))

    def test_create_the_marshal_creates_special_possession_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        form_data = self.generate_create_character_form_data(self.the_marshal, background=1, moves=moves_qs, kwargs=self.marshal_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-marshal', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheMarshal.objects.all()[0] # TODO: Find a less hacky way to get the character
        possession1 = SpecialPossessionInstance.objects.get(special_possession__possession_name="Chirurgeon's tools")
        self.assertEqual(list(char.special_possessions.all()), [possession1])
        
    def test_create_the_marshal_creates_moves_instance(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # PENITENT background (1)
        form_data = self.generate_create_character_form_data(self.the_marshal, background=1, moves=moves_qs, kwargs=self.marshal_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-marshal', kwargs={'pk': test_campaign.pk}), data=form_data)

        char = TheMarshal.objects.all()[0] # TODO: Find a less hacky way to get the character
        move_instance_1 = MoveInstance.objects.get(move__name='CREW')
        move_instance_2 = MoveInstance.objects.get(move__name='LOGISTICS')
        self.assertEqual(list(char.move_instances.all()), [move_instance_1, move_instance_2])

    def test_create_the_marshal_at_least_three_war_details_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)

        form_data = self.generate_create_character_form_data(self.the_marshal, background=1, kwargs=self.marshal_kwargs)
        form_data.pop('war_detail_1')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-marshal', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', field=None, errors=['You have answered 2 questions. Please answer at least 3 questions about the war story.'])
          
    def test_create_the_marshal_war_story_required_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_marshal, background=1, kwargs=self.marshal_kwargs)
        form_data.pop('war_story')
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-marshal', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'war_story', ['This field is required.'])
    
    def test_create_the_marshal_without_starting_moves_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        
        form_data = self.generate_create_character_form_data(self.the_marshal, background=0, kwargs=self.marshal_kwargs)
        form_data.pop('move_instances')
        move = Moves.objects.filter(name='ARMORED')
        form_data['move_instances'] = move
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-marshal', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', field=None, errors=['CREW is a required starting move.', 'LOGISTICS is a required starting move.'])
    
    def test_create_the_marshal_restricted_move_raises_error_if_selected(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('PREPARE A WELCOME')
        moves_qs = Moves.objects.filter(name__in=moves)
        # PENITENT background (1)
        form_data = self.generate_create_character_form_data(self.the_marshal, background=1, moves=moves_qs, kwargs=self.marshal_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)
        response = self.client.post(reverse('the-marshal', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertFormError(response, 'form', field=None, errors=['PREPARE A WELCOME requires the READ THE LAND move.'])

    def test_create_the_marshal_luminary_background_without_we_happy_few_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # LUMINARY background (0)
        form_data = self.generate_create_character_form_data(self.the_marshal, background=0, moves=moves_qs, kwargs=self.marshal_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)
        response = self.client.post(reverse('the-marshal', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertFormError(response, 'form', field=None, errors=['WE HAPPY FEW move is required for LUMINARY background.'])

    def test_create_the_marshal_scion_background_without_veteran_crew_raises_error(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves_qs = Moves.objects.filter(name__in=moves)
        
        # SCION background (2)
        form_data = self.generate_create_character_form_data(self.the_marshal, background=2, moves=moves_qs, kwargs=self.marshal_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)
        response = self.client.post(reverse('the-marshal', kwargs={'pk': test_campaign.pk}), data=form_data)

        self.assertFormError(response, 'form', field=None, errors=['VETERAN CREW move is required for SCION background.'])


class CreateCrewTests(BaseViewsTestClass):
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
        cls.the_marshal = CharacterClass.objects.get(class_name="The Marshal")
        cls.starting_moves = MARSHAL_STARTING_MOVES
        # Generate the form attributes unique to the Marshal
        cls.marshal_kwargs = {
            'war_story': WAR_STORIES[0][0],
            'war_detail_1': 'Four score, 25 years in the past.',
            'war_detail_3': 'I saved the union with my beard.',
            'war_detail_7': "Those dang corrupted crinwin, so now I'm back to kick some ass.",
        }

    def create_luminary_background_marshal(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('WE HAPPY FEW')
        moves_qs = Moves.objects.filter(name__in=moves)

        # LUMINARY background is the first one (0)
        form_data = self.generate_create_character_form_data(self.the_marshal, background=0, moves=moves_qs, kwargs=self.marshal_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-marshal', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheMarshal.objects.all()[0] # TODO: Find a less hacky way to get the character
        return test_campaign, char

    def test_create_crew_uses_correct_template(self):
        campaign, marshal = self.create_luminary_background_marshal()

        response = self.client.get(f'/campaigns/{campaign.pk}/{marshal.pk}/add_crew/')

        self.assertTemplateUsed(response, 'campaign/create_crew.html')

    def test_create_crew_queryset_contains_only_relevant_tags(self):
        campaign, marshal = self.create_luminary_background_marshal()

        response = self.client.get(f'/campaigns/{campaign.pk}/{marshal.pk}/add_crew/')
        tags = list(response.context['form'].fields['crew_tags'].queryset)
        tags = [tag.name for tag in tags]
        self.assertEqual(tags, MARSHAL_CREW_TAGS)
    
    def test_create_crew_group_tag_already_selected(self):
        campaign, marshal = self.create_luminary_background_marshal()
        group_tag = Tags.objects.get(name='group')

        response = self.client.get(f'/campaigns/{campaign.pk}/{marshal.pk}/add_crew/')
        self.assertEqual(list(response.context['form'].fields['crew_tags'].initial), [group_tag])

    @skip
    def test_create_crew_with_luminary_background_without_devoted_tag_raises_error(self):
        pass
    
    @skip
    def test_create_crew_character_attribute_set_to_current_character(self):
        campaign, marshal = self.create_luminary_background_marshal()

        response = self.client.get(f'/campaigns/{campaign.pk}/{marshal.pk}/add_crew/')



class TheMarshalDetailTests(BaseViewsTestClass):
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
        cls.the_marshal = CharacterClass.objects.get(class_name="The Marshal")
        cls.starting_moves = MARSHAL_STARTING_MOVES
        cls.starting_moves.append('ARMORED')
        # Generate the form attributes unique to the Marshal
        cls.marshal_kwargs = {
            'war_story': WAR_STORIES[0][0],
            'war_detail_1': 'Four score, 25 years in the past.',
            'war_detail_3': 'I saved the union with my beard.',
            'war_detail_7': "Those dang corrupted crinwin, so now I'm back to kick some ass.",
        }

    def create_luminary_background_marshal(self):
        test_campaign = self.join_campaign_and_login_user(TEST_CAMPAIGN, self.testuser)
        moves = self.starting_moves
        moves.append('WE HAPPY FEW')
        moves_qs = Moves.objects.filter(name__in=moves)
        possessions = ["Engineer's tools", 'Personal symbol']
        sp_qs = SpecialPossessions.objects.filter(possession_name__in=possessions)
        
        form_data = self.generate_create_character_form_data(
            self.the_marshal, background=0, STR=-1, DEX=0, INT=1, WIS=2, CON=0, CHA=1, 
            moves=moves_qs, special_possessions=sp_qs, kwargs=self.marshal_kwargs)
        form_data = self.convert_data_to_foreign_keys(form_data)

        response = self.client.post(reverse('the-marshal', kwargs={'pk': test_campaign.pk}), data=form_data)
    
        char = TheMarshal.objects.all()[0] 
        return test_campaign, char        

    def test_the_marshal_detail_page_uses_correct_template(self):
        campaign, marshal = self.create_luminary_background_marshal()

        response = self.client.get(f'/campaigns/{campaign.pk}/{marshal.pk}/the_marshal_home/')

        self.assertTemplateUsed(response, 'campaign/the_marshal_detail.html')

    def test_the_marshal_update_moves_uses_correct_template(self):
        campaign, marshal = self.create_luminary_background_marshal()

        response = self.client.get(f'/campaigns/{campaign.pk}/{marshal.pk}/moves/update/')

        self.assertTemplateUsed(response, 'campaign/update_moves.html')

    def test_the_marshal_update_moves_form_shows_no_initial_moves(self):
        campaign, marshal = self.create_luminary_background_marshal()

        response = self.client.get(f'/campaigns/{campaign.pk}/{marshal.pk}/moves/update/')

        initial_moves = response.context['form'].fields['move_instances'].initial
        self.assertEqual(initial_moves, None)
    
    def test_the_marshal_all_marshal_moves(self):
        campaign, marshal = self.create_luminary_background_marshal()
        starting_moves = self.starting_moves
        moves = list(Moves.objects.filter(
            character_class=self.the_marshal).exclude(
                name__in=starting_moves
            ).order_by(
                F('move_requirements__level_restricted').asc(nulls_first=True), 
                F('move_requirements__move_restricted').asc(nulls_first=True), 
                'name'
                ))

        response = self.client.get(f'/campaigns/{campaign.pk}/{marshal.pk}/moves/update/')

        move_instances = list(response.context['form'].fields['move_instances'].queryset)
        self.assertEqual(moves, move_instances)
