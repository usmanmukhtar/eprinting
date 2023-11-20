from user_app import views
from rest_framework.routers import DefaultRouter
from django.urls import path


router = DefaultRouter()

router.register(r'user',views.UserProfileViewSet, basename='user')
router.register(r'favourite_user',views.FavouritePlayersViewSet, basename='favourite-user')
router.register(r'user_bet_paymentinfo',views.UserBetPaymentInfoViewSet, basename='user-bet-paymentinfo')
router.register(r'report_type', views.ReportTypeViewSet, basename='report-type')
router.register(r'report', views.ReportViewSet, basename='report')
router.register(r'myprofile', views.MyProfileViewSet, basename='myprofile')
# router.register(r'videos', views.UserVideosViewSet, basename='videos')

urlpatterns = router.urls

urlpatterns += [
    path("my_bets/", views.MyBetsView.as_view(), name="my-bets"),
    # path("leaderboard/", views.LeaderboardViewSet().as_view(), name="leaderboard"),

]