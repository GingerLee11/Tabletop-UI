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
from django.urls import path, include

from campaign import views

urlpatterns = [
    path('stonetop/', views.CampaignListView.as_view(), name='campaign-list'),
    path('stonetop/create_campaign/', views.CreateCampaignView.as_view(), name='create-campaign'),
    path('stonetop/<int:pk>/', views.CampaignDetailView.as_view(), name='campaign-detail'), # TODO: Change so that the URL contains the name of the campaign
    path('stonetop/choose_character/', views.ChooseCharacterView.as_view(), name='choose-character'),
    path('stonetop/<int:pk>/create_the_blessed/', views.CreateTheBlessedView.as_view(), name='the-blessed'),
    path('stonetop/<int:pk>/create_the_fox/', views.CreateTheFoxView.as_view(), name='the-fox'),
    path('stonetop/<int:pk>/create_the_heavy/', views.CreateTheHeavyView.as_view(), name='the-heavy'),
    path('stonetop/<int:pk>/create_the_judge/', views.CreateTheJudgeView.as_view(), name='the-judge'),
    path('stonetop/<int:pk>/create_the_lightbearer/', views.CreateTheLightbearerView.as_view(), name='the-lightbearer'),
    path('stonetop/<int:pk>/create_the_marshal/', views.CreateTheMarshalView.as_view(), name='the-marshal'),
    path('stonetop/<int:pk>/create_the_ranger/', views.CreateTheRangerView.as_view(), name='the-ranger'),
    path('stonetop/<int:pk_>/the_blessed_home/<int:pk_blessed>/', views.TheBlessedDetailView.as_view(), name='the-blessed-detail'),
    path('stonetop/<int:pk_>/the_fox_home/<int:pk_fox>/', views.TheFoxDetailView.as_view(), name='the-fox-detail'),
    path('stonetop/<int:pk_>/the_heavy_home/<int:pk_char>/', views.TheHeavyDetailView.as_view(), name='the-heavy-detail'),
    path('stonetop/<int:pk_>/the_judge_home/<int:pk_char>/', views.TheJudgeDetailView.as_view(), name='the-judge-detail'),
    path('stonetop/<int:pk_>/the_lightbearer_home/<int:pk_char>/', views.TheLightbearerDetailView.as_view(), name='the-lightbearer-detail'),
    path('stonetop/<int:pk_>/the_marshal_home/<int:pk_char>/', views.TheMarshalDetailView.as_view(), name='the-marshal-detail'),
    path('stonetop/<int:pk_>/the_ranger_home/<int:pk_char>/', views.TheRangerDetailView.as_view(), name='the-ranger-detail'),

    # NPCs and followers:
    path('stonetop/<int:pk>/create_npc/', views.CreateNPCView.as_view(), name='create-npc'),
    path('stonetop/<int:pk>/gm_npc_instance/', views.GMCreateNPCInstanceView.as_view(), name='gm-npc-instance'),
    path('stonetop/<int:pk>/player_npc_instance/', views.PlayerCreateNPCInstanceView.as_view(), name='player-npc-instance'),
    
    
]
