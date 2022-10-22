"""stonetop_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path

from campaign import views

from django.views.generic import TemplateView

urlpatterns = [
    path('', views.CampaignListView.as_view(), name='campaign-list'),
    path('create_campaign/', views.CreateCampaignView.as_view(), name='create-campaign'),
    path('<int:pk>/', views.CampaignDetailView.as_view(), name='campaign-detail'), 
    path('choose_character/', views.ChooseCharacterView.as_view(), name='choose-character'),
    
    # Create Character:
    path('<int:pk>/create_the_blessed/', views.CreateTheBlessedView.as_view(), name='the-blessed'),
    path('<int:pk>/create_the_fox/', views.CreateTheFoxView.as_view(), name='the-fox'),
    path('<int:pk>/create_the_heavy/', views.CreateTheHeavyView.as_view(), name='the-heavy'),
    path('<int:pk>/create_the_judge/', views.CreateTheJudgeView.as_view(), name='the-judge'),
    path('<int:pk>/create_the_lightbearer/', views.CreateTheLightbearerView.as_view(), name='the-lightbearer'),
    path('<int:pk>/create_the_marshal/', views.CreateTheMarshalView.as_view(), name='the-marshal'),
    path('<int:pk>/create_the_ranger/', views.CreateTheRangerView.as_view(), name='the-ranger'),
    path('<int:pk>/create_the_seeker/', views.CreateTheSeekerView.as_view(), name='the-seeker'),
    
    # Character Detail View:
    path('<int:pk>/<int:pk_char>/the_blessed_home/', views.TheBlessedDetailView.as_view(), name='the-blessed-detail'),
    path('<int:pk>/<int:pk_char>/the_fox_home/', views.TheFoxDetailView.as_view(), name='the-fox-detail'),
    path('<int:pk>/<int:pk_char>/the_heavy_home/', views.TheHeavyDetailView.as_view(), name='the-heavy-detail'),
    path('<int:pk>/<int:pk_char>/the_judge_home/', views.TheJudgeDetailView.as_view(), name='the-judge-detail'),
    path('<int:pk>/<int:pk_char>/the_lightbearer_home/', views.TheLightbearerDetailView.as_view(), name='the-lightbearer-detail'),
    path('<int:pk>/<int:pk_char>/the_marshal_home/', views.TheMarshalDetailView.as_view(), name='the-marshal-detail'),
    path('<int:pk>/<int:pk_char>/the_ranger_home/', views.TheRangerDetailView.as_view(), name='the-ranger-detail'),
    path('<int:pk>/<int:pk_char>/the_seeker_home/', views.TheSeekerDetailView.as_view(), name='the-seeker-detail'),

    # NPCs and followers:
    path('<int:pk>/create_npc/', views.CreateNPCView.as_view(), name='create-npc'),
    path('<int:pk>/gm_npc_instance/', views.GMCreateNPCInstanceView.as_view(), name='gm-npc-instance'),
    path('<int:pk>/<int:pk_char>/player_create_npc/', views.PlayerCreateNPCInstanceView.as_view(), name='player-create-npc'),
    path('<int:pk>/<int:pk_char>/add_follower/', views.CreateFollowerInstanceView.as_view(), name='create-follower'),
    path('<int:pk>/<int:pk_char>/<int:pk_follower>/', views.FollowerDetailView.as_view(), name='follower-detail'),
    # Animal Companions:
    path('<int:pk>/<int:pk_char>/add_animal_companion/', views.CreateAnimalCompanionView.as_view(), name='create-animal-companion'),
    path('<int:pk>/<int:pk_char>/animal_companion/<int:pk_animal>', views.UpdateAnimalCompanionView.as_view(), name='update-animal-companion'),

    # Update Views
    # Background
    path('<int:pk>/<int:pk_char>/background/<int:pk_background>/', views.UpdateBackgroundInstanceView.as_view(), name='update-background'),
    # Inventory:
    path('<int:pk>/<int:pk_char>/inventory/', views.UpdateCharacterInventoryView.as_view(), name='character-inventory'),
    path('<int:pk>/<int:pk_char>/create_item/', views.CreateItemView.as_view(), name='create-item'),
    path('<int:pk>/<int:pk_char>/create_small_item/', views.CreateSmallItemView.as_view(), name='create-small-item'),
    path('<int:pk>/<int:pk_char>/item/<int:pk_item>', views.UpdateItemInstanceView.as_view(), name='update-item'),
    path('<int:pk>/<int:pk_char>/small_item/<int:pk_small_item>/', views.UpdateSmallItemInstanceView.as_view(), name='update-small-item'),
    path('<int:pk>/<int:pk_char>/item/<int:pk_item>/delete/', views.DeleteItemInstanceView.as_view(), name='delete-item'),
    path('<int:pk>/<int:pk_char>/small_item/<int:pk_small_item>/delete/', views.DeleteSmallItemInstanceView.as_view(), name='delete-small-item'),

    # Stats:
    path('<int:pk>/<int:pk_char>/stats/', views.CharacterUpdateStatsView.as_view(), name='character-stats'),
    # Special Possessions:
    path('<int:pk>/<int:pk_char>/special_possession/<int:pk_special_possession>/', views.UpdateSpecialPossessionView.as_view(), name='update-special-possession'),
    # Moves:
    path('<int:pk>/<int:pk_char>/move/<int:pk_move>/', views.UpdateMoveInstanceView.as_view(), name='update-move'),
    path('<int:pk>/<int:pk_char>/moves/', views.UpdateCharacterMovesView.as_view(), name='update-moves'),
    # path('<int:pk>/the_blessed_home/<int:pk_char>/moves/', views.UpdateTheBlessedMovesView.as_view(), name='the-blessed-moves'),
    # path('<int:pk>/the_fox_home/<int:pk_char>/moves/', views.UpdateTheFoxMovesView.as_view(), name='the-fox-moves'),
    # path('<int:pk>/the_heavy_home/<int:pk_char>/moves/', views.UpdateTheHeavyMovesView.as_view(), name='the-heavy-moves'),
    # path('<int:pk>/the_judge_home/<int:pk_char>/moves/', views.UpdateTheJudgeMovesView.as_view(), name='the-judge-moves'),
    # path('<int:pk>/the_lightbearer_home/<int:pk_char>/moves/', views.UpdateTheLightbearerMovesView.as_view(), name='the-lightbearer-moves'),
    # path('<int:pk>/the_marshal_home/<int:pk_char>/moves/', views.UpdateTheMarshalMovesView.as_view(), name='the-marshal-moves'),
    # path('<int:pk>/the_ranger_home/<int:pk_char>/moves/', views.UpdateTheRangerMovesView.as_view(), name='the-ranger-moves'),
    # path('<int:pk>/the_seeker_home/<int:pk_char>/moves/', views.UpdateTheSeekerMovesView.as_view(), name='the-seeker-moves'),
    # Arcana:
    path('<int:pk>/<int:pk_char>/major_arcana/<int:pk_arcana>', views.UpdateMajorArcanaInstancesView.as_view(), name='update-major-arcana'),
    path('<int:pk>/<int:pk_char>/minor_arcana/<int:pk_arcana>', views.UpdateMinorArcanaInstancesView.as_view(), name='update-minor-arcana'),
    path('<int:pk>/<int:pk_char>/arcana_moves/<int:pk_arcana_move>', views.UpdateArcanaMovesView.as_view(), name='update-arcana-move'), # TODO: Maybe change this so that it also correlates to the arcana in the URL

    # The Seeker Arcana
    path('<int:pk>/the_seeker_home/<int:pk_char>/inital_arcana/', views.TheSeekerInitialArcanaView.as_view(), name='the-seeker-initial-arcana'),
    
]

# Autocomplete URLS:

urlpatterns += [
    re_path(
        r'^tags-autocomplete/$', 
        views.TagsAutoCompleteView.as_view(create_field='name'), 
        name='tags-autocomplete',
        ),
    re_path(
        r'^npc_instance-autocomplete/$', 
        views.NPCInstanceAutoCompleteView.as_view(), 
        name='npc-autocomplete',
        ),
]
