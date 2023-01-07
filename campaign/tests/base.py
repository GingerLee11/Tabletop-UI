from django.test import TestCase
from django.db.models import F

from campaign.models import (
    TheWouldBeHero,
    Background, Instinct, AppearanceAttribute, 
    PlaceOfOrigin, SpecialPossessions, Moves,
)

TEST_USERNAME = 'testuser'
TEST_EMAIL = 'testing@example.com'
TEST_CAMPAIGN = 'Open campaign for functional tests'


class BaseTestClass(TestCase):

    def generate_create_character_form_data(self, 
        character_class=None, background=0, 
        STR=2, DEX=1, INT=1, WIS=0, CON=0, CHA=-1, stats=[],
        moves=[], special_possessions=[], **kwargs):
        background_pk = Background.objects.filter(
            character_class=character_class).order_by(
                'background')[background].pk
        instinct_pk = Instinct.objects.filter(character_class=character_class)[0].pk
        appearance1_pk = AppearanceAttribute.objects.filter(
            character_class=character_class).filter(
                attribute_type='appearance1'
        )[0].pk
        appearance2_pk = AppearanceAttribute.objects.filter(
            character_class=character_class).filter(
                attribute_type='appearance2'
        )[0].pk
        appearance3_pk = AppearanceAttribute.objects.filter(
            character_class=character_class).filter(
                attribute_type='appearance3'
        )[0].pk
        appearance4_pk = AppearanceAttribute.objects.filter(
            character_class=character_class).filter(
                attribute_type='appearance4'
        )[0].pk
        place_of_origin_pk = PlaceOfOrigin.objects.filter(character_class=character_class)[0].pk
        if special_possessions == []:
            special_possession_list = SpecialPossessions.objects.filter(
                character_class__class_name=character_class
                ).order_by('possession_name')[:1]
        else:
            special_possession_list = special_possessions
        if moves == []:
            move_list = Moves.objects.filter(
            character_class__class_name=character_class,
            ).filter(
                move_requirements__level_restricted=None,
            ).order_by(
                F('move_requirements__move_restricted').asc(nulls_first=True), 
                F('move_requirements__level_restricted').asc(nulls_first=True), 
                'name',
            )
        else:
            move_list = moves

        # TODO: Fix this, this is very hacky
        if str(character_class) == 'The Would-Be Hero' and stats == []:
            STR = -1
            DEX = 0
            INT = 0
            WIS = 0
            CON = 0
            CHA = 1
        
        form_data = {
            'background': background_pk, 
            'instinct': instinct_pk, 
            'appearance1': appearance1_pk, 
            'appearance2': appearance2_pk, 
            'appearance3': appearance3_pk, 
            'appearance4': appearance4_pk,
            'place_of_origin': place_of_origin_pk,
            'character_name': 'test',
            'strength': STR,
            'dexterity': DEX,
            'intelligence': INT,
            'wisdom': WIS,
            'constitution': CON,
            'charisma': CHA,
            'special_possessions': special_possession_list,
            'move_instances': move_list,
        }
        # Adds addtional form items for other character classes
        if kwargs:
            # print(f"\nkwargs: {kwargs}\n")
            form_kwargs = kwargs['kwargs']
            # print(f"form kwargs: {form_kwargs}\n")
            for k, v in form_kwargs.items():
                form_data[k] = v
            # print(f"form data: {form_data}\n")
        return form_data
