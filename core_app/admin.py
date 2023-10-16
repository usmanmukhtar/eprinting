import datetime

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import F

from user_app.models import UserProfile
# from game_app.models import Leaderboard, GameType, Game
from django.db.models import Sum, Window
from django.db.models.functions import DenseRank
from django.shortcuts import render

@staff_member_required
def admin_dashboard(request):
    new_signups = UserProfile.objects.filter(created_at__date=datetime.date.today()).count()
    games = GameType.objects.all().count()
    total_users = UserProfile.objects.count()
    leader_board = Leaderboard.objects.all().annotate(profile_picture = F('player__image'), full_name = F('player__full_name')).order_by('-matches_won')[0:10]

    labels = []
    data = []

    most_played_games = Game.objects.values('game_type').annotate(
                top_5 = Sum('game_type'),
                place=Window(
                    expression=DenseRank(),
                    order_by=[
                        F('top_5').desc(),
                    ])
                ).values('game_type__title', 'top_5', 'place').order_by('-top_5')[:5]

    for city in most_played_games:
        labels.append(city['game_type__title'])
        data.append(city['place'])

    context = {
        'available_apps': admin.site.get_app_list(request),
        'leader_board': leader_board,
        'cards': [
            {"title": "New Signups", "value": new_signups, "icon": "fa fa-user-plus"},
            {"title": "Games", "value": games, "icon": "fa fa-trophy"},
            {"title": "Total Users", "value": total_users, "icon": "fa fa-users"},
            {"title": "Total Income", "value": total_users, "icon": "fa fa-dollar-sign"},
        ],
        'chart': {
            'labels': labels,
            'data': data,
        }
    }
    return render(request, 'admin/admin_dashboard.html', context)
