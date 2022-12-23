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

urlpatterns = [
    path('', views.CampaignListView.as_view(), name='campaign-list'),
    path('create_campaign/', views.CreateCampaignView.as_view(), name='create-campaign'),
    path('<int:pk>/', views.CampaignDetailView.as_view(), name='campaign-detail'), 
    path('<int:pk>/update/', views.CampaignUpdateView.as_view(), name='update-campaign'), 
    path('<int:pk>/check_code/', views.CheckCampaignCodeView.as_view(), name='check-campaign-code'), 
    path('<int:pk>/choose_character/', views.ChooseCharacterView.as_view(), name='choose-character'),
    # Create Character:
    path('<int:pk>/create_the_blessed/', views.CreateTheBlessedView.as_view(), name='the-blessed'),
    path('<int:pk>/create_the_fox/', views.CreateTheFoxView.as_view(), name='the-fox'),
    path('<int:pk>/create_the_heavy/', views.CreateTheHeavyView.as_view(), name='the-heavy'),
    path('<int:pk>/create_the_judge/', views.CreateTheJudgeView.as_view(), name='the-judge'),
    path('<int:pk>/create_the_lightbearer/', views.CreateTheLightbearerView.as_view(), name='the-lightbearer'),
    path('<int:pk>/create_the_marshal/', views.CreateTheMarshalView.as_view(), name='the-marshal'),
    path('<int:pk>/create_the_ranger/', views.CreateTheRangerView.as_view(), name='the-ranger'),
    path('<int:pk>/create_the_seeker/', views.CreateTheSeekerView.as_view(), name='the-seeker'),
    path('<int:pk>/create_the_would_be_hero/', views.CreateTheWouldBeHeroView.as_view(), name='the-would-be-hero'),
    # Character Detail View:
    path('<int:pk>/<int:pk_char>/the_blessed_home/', views.TheBlessedDetailView.as_view(), name='the-blessed-detail'),
    path('<int:pk>/<int:pk_char>/the_fox_home/', views.TheFoxDetailView.as_view(), name='the-fox-detail'),
    path('<int:pk>/<int:pk_char>/the_heavy_home/', views.TheHeavyDetailView.as_view(), name='the-heavy-detail'),
    path('<int:pk>/<int:pk_char>/the_judge_home/', views.TheJudgeDetailView.as_view(), name='the-judge-detail'),
    path('<int:pk>/<int:pk_char>/the_lightbearer_home/', views.TheLightbearerDetailView.as_view(), name='the-lightbearer-detail'),
    path('<int:pk>/<int:pk_char>/the_marshal_home/', views.TheMarshalDetailView.as_view(), name='the-marshal-detail'),
    path('<int:pk>/<int:pk_char>/the_ranger_home/', views.TheRangerDetailView.as_view(), name='the-ranger-detail'),
    path('<int:pk>/<int:pk_char>/the_seeker_home/', views.TheSeekerDetailView.as_view(), name='the-seeker-detail'),
    path('<int:pk>/<int:pk_char>/the_would_be_hero_home/', views.TheWouldBeHeroDetailView.as_view(), name='the-would-be-hero-detail'),
    # NPCs and followers:
    path('<int:pk>/create_npc/', views.CreateNPCView.as_view(), name='create-npc'),
    path('<int:pk>/gm_npc_instance/', views.GMCreateNPCInstanceView.as_view(), name='gm-npc-instance'),
    path('<int:pk>/<int:pk_char>/player_create_npc/', views.PlayerCreateNPCInstanceView.as_view(), name='player-create-npc'),
    path('<int:pk>/<int:pk_char>/add_follower/', views.CreateFollowerInstanceView.as_view(), name='create-follower'),
    path('<int:pk>/<int:pk_char>/followers/', views.CharacterFollowersListView.as_view(), name='character-followers'),
    path('<int:pk>/<int:pk_char>/followers/<int:pk_follower>/', views.FollowerDetailView.as_view(), name='follower-detail'),
    path('<int:pk>/<int:pk_char>/followers/<int:pk_follower>/update/', views.UpdateNPCInstanceAndFollowerView.as_view(), name='update-follower'),
    path('<int:pk>/<int:pk_char>/followers/<int:pk_follower>/items/<int:pk_item>/update/', views.UpdateFollowerItemView.as_view(), name='update-follower-item'),
    path('<int:pk>/<int:pk_char>/followers/<int:pk_follower>/small_items/<int:pk_small_item>/update/', views.UpdateFollowerSmallItemView.as_view(), name='update-follower-small-item'),
    path('<int:pk>/<int:pk_char>/followers/<int:pk_follower>/items/<int:pk_item>/delete/', views.DeleteFollowerItemInstanceView.as_view(), name='delete-follower-item'),
    path('<int:pk>/<int:pk_char>/followers/<int:pk_follower>/small_items/<int:pk_small_item>/delete/', views.DeleteFollowerSmallItemInstanceView.as_view(), name='delete-follower-small-item'),

    # Animal Companions:
    path('<int:pk>/<int:pk_char>/add_animal_companion/', views.CreateAnimalCompanionView.as_view(), name='create-animal-companion'),
    path('<int:pk>/<int:pk_char>/animal_companion/<int:pk_animal>', views.UpdateAnimalCompanionView.as_view(), name='update-animal-companion'),
    # Background
    path('<int:pk>/<int:pk_char>/background/<int:pk_background>/', views.UpdateBackgroundInstanceView.as_view(), name='update-background'),
    # Inventory:
    path('<int:pk>/<int:pk_char>/inventory/', views.CharacterInventoryListView.as_view(), name='character-inventory'),
    path('<int:pk>/<int:pk_char>/inventory/update/', views.UpdateCharacterInventoryView.as_view(), name='update-character-inventory'),
    path('<int:pk>/<int:pk_char>/create_item/', views.CreateItemView.as_view(), name='create-item'),
    path('<int:pk>/<int:pk_char>/create_small_item/', views.CreateSmallItemView.as_view(), name='create-small-item'),
    path('<int:pk>/<int:pk_char>/items/<int:pk_item>/update/', views.UpdateItemInstanceView.as_view(), name='update-item'),
    path('<int:pk>/<int:pk_char>/small_items/<int:pk_small_item>/update/', views.UpdateSmallItemInstanceView.as_view(), name='update-small-item'),
    path('<int:pk>/<int:pk_char>/items/<int:pk_item>/delete/', views.DeleteItemInstanceView.as_view(), name='delete-item'),
    path('<int:pk>/<int:pk_char>/small_items/<int:pk_small_item>/delete/', views.DeleteSmallItemInstanceView.as_view(), name='delete-small-item'),
    # Stats:
    path('<int:pk>/<int:pk_char>/stats/', views.CharacterUpdateStatsView.as_view(), name='character-stats'),
    # Special Possessions:
    path('<int:pk>/<int:pk_char>/special_possession/', views.CharacterSpecialPossessionsListView.as_view(), name='character-special-possessions'),
    path('<int:pk>/<int:pk_char>/special_possession/<int:pk_special_possession>/', views.UpdateSpecialPossessionView.as_view(), name='update-special-possession'),
    # Moves:
    path('<int:pk>/<int:pk_char>/moves/', views.CharacterMovesListView.as_view(), name='character-moves'),
    path('<int:pk>/<int:pk_char>/moves/<int:pk_move>/', views.UpdateMoveInstanceView.as_view(), name='update-move'),
    path('<int:pk>/<int:pk_char>/moves/update/', views.UpdateCharacterMovesView.as_view(), name='update-moves'),
    # Arcana:
    path('<int:pk>/<int:pk_char>/arcana/', views.CharacterArcanaListView.as_view(), name='character-arcana'),
    path('<int:pk>/<int:pk_char>/major_arcana/<int:pk_arcana>/', views.UpdateMajorArcanaInstancesView.as_view(), name='update-major-arcana'),
    path('<int:pk>/<int:pk_char>/minor_arcana/<int:pk_arcana>/', views.UpdateMinorArcanaInstancesView.as_view(), name='update-minor-arcana'),
    path('<int:pk>/<int:pk_char>/arcana_moves/<int:pk_arcana_move>/', views.UpdateArcanaMovesView.as_view(), name='update-arcana-move'), # TODO: Maybe change this so that it also correlates to the arcana in the URL
    
    # The Blessed special views
    path('<int:pk>/<int:pk_char>/sacred_pouch/', views.TheBlessedSacredPouchDetailView.as_view(), name='character-sacred-pouch'),
    path('<int:pk>/<int:pk_char>/update_sacred_pouch/', views.TheBlessedSacredPouchUpdateView.as_view(), name='character-update-sacred-pouch'),
    path('<int:pk>/<int:pk_char>/add_initiates_of_danu/', views.TheBlessedAddInitatesOfDanuView.as_view(), name='the-blessed-add-initiates'),
    path('<int:pk>/<int:pk_char>/initiates_of_danu/', views.TheBlessedInitiatesOfDanuView.as_view(), name='character-initiates-of-danu'),
    # The Fox special Views
    path('<int:pk>/<int:pk_char>/tall_tales/', views.TheFoxTallTalesListView.as_view(), name='character-tall-tales'),
    path('<int:pk>/<int:pk_char>/tall_tales/<int:pk_tale>/update/', views.TheFoxTallTalesUpdateView.as_view(), name='update-tall-tale'),
    path('<int:pk>/<int:pk_char>/create_tall_tale/', views.TheFoxTallTalesCreateView.as_view(), name='add-tall-tale'),
    # The Lighbearer special views:
    path('<int:pk>/<int:pk_char>/invocations/', views.TheLightbearerInvocationsListView.as_view(), name='character-invocations'),
    path('<int:pk>/<int:pk_char>/invocations/update/', views.TheLightBearerInvocationUpdateView.as_view(), name='character-update-invocations'),
    # The Marshal special views:
    path('<int:pk>/<int:pk_char>/add_crew/', views.CreateCrewView.as_view(), name='character-create-crew'),

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
