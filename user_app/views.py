import time

from rest_framework.viewsets import ModelViewSet
# from rest_framework_role_filters.viewsets import RoleFilterModelViewSet
from rest_framework.decorators import action

from core_app.utils import success_response, error_response, specific_error_response, success_response_message
from user_app.models import UserProfile, FavouritePlayers, UserBetPaymentInfo, ReportType, ReportUser
from user_app.serializers import UserProfileSerializer, FavouritePlayersSerializer, UserBetPaymentInfoSerializer, ReportTypeSerializer, ReportSerializer, MyBetsSerializer, UserNotificationsSerializer, GamePlayerProfileSerializer, MyProfileSerializer
# from user_app.role_filters import SuperAdminRoleFilter, RegulerUserRoleFilter
from core_app.mixins import APIResponseGenericViewMixin, SoftDeleteDestroyViewMixin, DeleteResponseMixin
# from user_app.permissions import UserProfileUpdatePermission
from django.http.response import Http404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
# from game_app.models import PlaceBet, GamePlayers, Leaderboard, Game, GamePlayerScorecard
# from game_app.serializers import LeaderboardSerializer
from core_app.pagination import MetaPageNumberPagination
from django.db.models import Q, Sum
from core_app.pagination import MetaPageNumberPagination
# from feeds_app.models import Video
# from game_app.serializers import GameScorecardDetailSerializer, GameScorecardListingSerializer
# from feeds_app.serializers import FeedVideoSerializer
# from feeds_app.models import Video
from django_filters.rest_framework import DjangoFilterBackend
from user_app.filters import HomiesNameFilter
from rest_framework.authtoken.models import Token
from auth_app.tasks import send_account_deletion_email


class UserProfileViewSet(APIResponseGenericViewMixin, ModelViewSet):
    queryset = UserProfile.objects.filter(active=True).order_by('pk')
    serializer_class = UserProfileSerializer
    # main methods: Post and Get
    # me methods: Put, Delete, Get


    def list(self, request, *args, **kwargs):
        user = request.user.userprofile.pk
        # queryset = self.queryset
        # FIXME: excluded emtpy DOB users as per the request of FE dev
        queryset = self.queryset.filter(~Q(id=user)).exclude(dob__isnull=True)
        pagination = MetaPageNumberPagination()
        qs = pagination.paginate_queryset(queryset, request)
        serializer = self.serializer_class(qs, many=True)
        return pagination.get_paginated_response(serializer.data)

    @action(detail=True, methods=['get'])
    def scorecards(self, request, *args, **kwargs):
        # user = request.user.userprofile
        # if we get the user pk in url, it will help us in using this API for match histories of other app users as well and not only the logged in one
        user = self.get_object()
        queryset = Game.objects.filter(gameplayers__player=user,game_status__in=('S','E')).order_by('-id')
        pagination = MetaPageNumberPagination()
        qs = pagination.paginate_queryset(queryset, request)
        # serializer_class = GameScorecardDetailSerializer
        serializer_class = GameScorecardListingSerializer
        serializer = serializer_class(qs, many=True)
        return pagination.get_paginated_response(serializer.data)


    @action(detail=False, methods=['get', 'put', 'patch','delete'])
    def me(self, request, *args, **kwargs):
        profile = request.user.userprofile

        if profile.active == False:
            return specific_error_response(message="record not found")

        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return success_response(serializer, message="Profile fetched successfully")

        elif request.method == 'DELETE':
            user = request.user
            instance = user.userprofile

            email = user.email
            full_name = instance.full_name

            instance.active = False
            instance.save()
            user.email = "deleted_" + str(int(time.time())) + "_" + user.email
            user.is_active = False
            user_fcm = user.fcmdevice_set.all()
            if user_fcm:
                user_fcm.delete()

            user_token = Token.objects.filter(user=user)
            if user_token:
                user_token.delete()

            user_videos = instance.video_set.all()
            if user_videos:
                user_videos.update(active=False)

            homies = FavouritePlayers.objects.filter(Q(favourite_player=instance) | Q(followed_by=instance))
            if homies:
                homies.delete()

            try:
                instance.leaderboard.delete()
            except:
                pass

            try:
                instance.toptenplayers.delete()
            except:
                pass

            user.save()
            send_account_deletion_email.delay(full_name, email)
            return success_response_message(data={},message="Record successfully deleted",status_code=200)

        instance = request.user.userprofile
        serializer = UserProfileSerializer(instance, data=request.data, partial=True,context={'request': request})
        if not serializer.is_valid():
            return error_response(serializer)

        serializer.save()
        return success_response(serializer, message="User Profile Updated Successfully")
        # return success_response_message(data=serializer.validated_data, message="User Profile Updated Successfully")


    @action(detail=False, methods=['post'])
    def notification_settings(self, request, *args, **kwargs):
        user = request.user.userprofile
        allow_notifications = request.data.get('allow_notifications')
        if allow_notifications:
            user.allow_notifications = allow_notifications
            user.save()

        return success_response_message(data={}, message='Notifications status updated successfully')


    @action(detail=True, methods=['get'])
    def videos(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = FeedVideoSerializer
        queryset = object.video_set.filter(active=True)
        serializer = serializer(queryset, many=True,context={'request': request})
        return success_response(serializer, message="Videos fetched successfully")

    @action(detail=True, methods=['delete'])
    def unfollow(self, request,pk=None):
        user = request.user.userprofile
        fav_player_obj = user.favourite_player.filter(favourite_player=pk)
        if fav_player_obj:
            fav_player_obj.delete()
            return Response({"success": True, 'data':{}, "message": "Unfollowed successfully", "status_code": 200},
                            status=status.HTTP_200_OK)
        else:
            return Response({"success": False, 'data':{}, "message": "Detail not found", "status_code": 404},
                            status=status.HTTP_404_NOT_FOUND)




# class UserVideosViewSet(viewsets.ViewSet):
#     serializer = FeedVideoSerializer
#     def retrieve(self, request, pk=None):
#         user = UserProfile.objects.get(pk=pk)
#         queryset = user.video_set.filter(active=True)
#         pagination = MetaPageNumberPagination()
#         qs = pagination.paginate_queryset(queryset, request)
#
#         serializer = self.serializer(qs, many=True)
#         return success_response(serializer, message="Videos fetched successfully")
#         # return pagination.get_paginated_response(serializer.data)    # def ret  (self, request, *args, **kwargs):
#

class FavouritePlayersViewSet(APIResponseGenericViewMixin,ModelViewSet):

    serializer_class = FavouritePlayersSerializer
    queryset = FavouritePlayers.objects.all()

    filter_backends = (DjangoFilterBackend,)
    filterset_class = HomiesNameFilter
    # http_method_names = ['get','post','delete']
    # User should be able to see his/her favourite players using /me endpoint
    # so that he can delete only his/her

    # This was deleted as separate endpoint was made via user/ to unfollow a homie
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     # user can only unfollow someone he follows
    #     if instance.followed_by != request.user.userprofile:
    #         return specific_error_response(message="You donot follow this player")
    #     instance.delete()
    #     return Response({"success": True, 'data':{}, "message": "Record deleted successfully", "status_code": 200},
    #                     status=status.HTTP_200_OK)

        # return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        profile = request.user.userprofile
        pagination = MetaPageNumberPagination()
        queryset = self.filter_queryset(self.queryset.filter(followed_by=profile))
        qs = pagination.paginate_queryset(queryset, request)
        serializer = self.serializer_class(qs, many=True)
        return pagination.get_paginated_response(serializer.data)

        # profile = request.user.userprofile
        # # qs = self.filter_queryset(self.get_queryset())
        # qs = self.filter_queryset(self.queryset.filter(followed_by=profile))
        # serializer = self.get_serializer(qs, many=True)
        # return success_response(serializer, message='Records successfully fetched')


class UserBetPaymentInfoViewSet(APIResponseGenericViewMixin,DeleteResponseMixin,ModelViewSet):
    serializer_class = UserBetPaymentInfoSerializer
    queryset = UserBetPaymentInfo.objects.all().order_by('-pk')

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        profile = request.user.userprofile

        if request.method == 'GET':
            serializer = self.get_serializer(self.queryset.filter(user=profile), many=True)
            return success_response(serializer, message='Records successfully fetched')


class ReportTypeViewSet(APIResponseGenericViewMixin,ModelViewSet):
    queryset = ReportType.objects.filter(active=True)
    serializer_class = ReportTypeSerializer


class ReportViewSet(APIResponseGenericViewMixin,ModelViewSet):
    queryset = ReportUser.objects.all()
    serializer_class = ReportSerializer
    http_method_names = ['post']


class MyBetsView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user.userprofile
            user_bets = user.user_bet_by

            bets_count = user_bets.count()
            bets_won = user_bets.filter(bet_status='W').count()
            bets_lost = user_bets.filter(bet_status='L').count()

            bets_summary = []
            all_bets = user_bets.all()
            for each in all_bets:
                bones = each.bones
                placed_on_fullname = each.placed_on.full_name
                bet_status = each.bet_status
                game_players = each.game.gameplayers_set.all()

                players_info = []
                for i in game_players:
                    player = i.player
                    players_info.append({'full_name':player.full_name,'image':player.image})

                bets_summary.append({
                    'bones':bones
                    ,'placed_on':placed_on_fullname
                    ,'bet_status':bet_status
                    ,'players_info':players_info
                })
            data = {'bets_count':bets_count
                    ,'bets_won':bets_won
                    ,'bets_lost':bets_lost
                    ,'bets_summary':bets_summary}

            return success_response_message(data=data,message='Success')
        except Exception as e:
            return specific_error_response(message=repr(e))


class MyProfileViewSet(viewsets.ViewSet):
    serializer_class = MyProfileSerializer

    def retrieve(self, request, pk=None):
        user = UserProfile.objects.get(pk=pk)
        # user = UserProfile.objects.prefetch_related('gameplayers_set__player','video_set','bet_payments_info','video_set__videolikes_set').get(pk=pk)
        # print("user : ", user)
        serializer = self.serializer_class(user, context={'request': request})
        return success_response(serializer=serializer, message="Profile fetched successfully")