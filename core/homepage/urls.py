from django.urls import path
from core.homepage.views.services.views import *
from core.homepage.views.departments.views import *
from core.homepage.views.social_networks.views import *
from core.homepage.views.statistics.views import *
from core.homepage.views.mainpage.views import *
from core.homepage.views.frequent_questions.views import *
from core.homepage.views.testimonials.views import *
from core.homepage.views.gallery.views import *
from core.homepage.views.team.views import *
from core.homepage.views.comments.views import *
from core.homepage.views.qualities.views import *
from core.homepage.views.news.views import *
from core.homepage.views.videos.views import *

urlpatterns = [
    # mainpage
    path('', IndexView.as_view(), name='index'),
    path('sign/in/', SignInView.as_view(), name='sign_in'),
    # services
    path('services/', ServicesListView.as_view(), name='services_list'),
    path('services/add/', ServicesCreateView.as_view(), name='services_create'),
    path('services/update/<int:pk>/', ServicesUpdateView.as_view(), name='services_update'),
    path('services/delete/<int:pk>/', ServicesDeleteView.as_view(), name='services_delete'),
    # departments
    path('departments/', DepartmentsListView.as_view(), name='departments_list'),
    path('departments/add/', DepartmentsCreateView.as_view(), name='departments_create'),
    path('departments/update/<int:pk>/', DepartmentsUpdateView.as_view(), name='departments_update'),
    path('departments/delete/<int:pk>/', DepartmentsDeleteView.as_view(), name='departments_delete'),
    # socialnetworks
    path('social/networks/', SocialNetworksListView.as_view(), name='social_networks_list'),
    path('social/networks/add/', SocialNetworksCreateView.as_view(), name='social_networks_create'),
    path('social/networks/update/<int:pk>/', SocialNetworksUpdateView.as_view(), name='social_networks_update'),
    path('social/networks/delete/<int:pk>/', SocialNetworksDeleteView.as_view(), name='social_networks_delete'),
    # statistics
    path('statistics/', StatisticsListView.as_view(), name='statistics_list'),
    path('statistics/add/', StatisticsCreateView.as_view(), name='statistics_create'),
    path('statistics/update/<int:pk>/', StatisticsUpdateView.as_view(), name='statistics_update'),
    path('statistics/delete/<int:pk>/', StatisticsDeleteView.as_view(), name='statistics_delete'),
    # freqquestions
    path('frequent/questions/', FrequentQuestionsListView.as_view(), name='frequent_questions_list'),
    path('frequent/questions/add/', FrequentQuestionsCreateView.as_view(), name='frequent_questions_create'),
    path('frequent/questions/update/<int:pk>/', FrequentQuestionsUpdateView.as_view(), name='frequent_questions_update'),
    path('frequent/questions/delete/<int:pk>/', FrequentQuestionsDeleteView.as_view(), name='frequent_questions_delete'),
    # testimonials
    path('testimonials/', TestimonialsListView.as_view(), name='testimonials_list'),
    path('testimonials/add/', TestimonialsCreateView.as_view(), name='testimonials_create'),
    path('testimonials/update/<int:pk>/', TestimonialsUpdateView.as_view(), name='testimonials_update'),
    path('testimonials/delete/<int:pk>/', TestimonialsDeleteView.as_view(), name='testimonials_delete'),
    # galery
    path('gallery/', GalleryListView.as_view(), name='gallery_list'),
    path('gallery/add/', GalleryCreateView.as_view(), name='gallery_create'),
    path('gallery/update/<int:pk>/', GalleryUpdateView.as_view(), name='gallery_update'),
    path('gallery/delete/<int:pk>/', GalleryDeleteView.as_view(), name='gallery_delete'),
    # team
    path('team/', TeamListView.as_view(), name='team_list'),
    path('team/add/', TeamCreateView.as_view(), name='team_create'),
    path('team/update/<int:pk>/', TeamUpdateView.as_view(), name='team_update'),
    path('team/delete/<int:pk>/', TeamDeleteView.as_view(), name='team_delete'),
    # qualities
    path('qualities/', QualitiesListView.as_view(), name='qualities_list'),
    path('qualities/add/', QualitiesCreateView.as_view(), name='qualities_create'),
    path('qualities/update/<int:pk>/', QualitiesUpdateView.as_view(), name='qualities_update'),
    path('qualities/delete/<int:pk>/', QualitiesDeleteView.as_view(), name='qualities_delete'),
    #  videos
    path('videos/', VideosListView.as_view(), name='videos_list'),
    path('videos/add/', VideosCreateView.as_view(), name='videos_create'),
    path('videos/update/<int:pk>/', VideosUpdateView.as_view(), name='videos_update'),
    path('videos/delete/<int:pk>/', VideosDeleteView.as_view(), name='videos_delete'),
    #  news
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/add/', NewsCreateView.as_view(), name='news_create'),
    path('news/update/<int:pk>/', NewsUpdateView.as_view(), name='news_update'),
    path('news/delete/<int:pk>/', NewsDeleteView.as_view(), name='news_delete'),
    # comments
    path('comments/', CommentsListView.as_view(), name='comments_list'),
    path('comments/delete/<int:pk>/', CommentsDeleteView.as_view(), name='comments_delete'),
]
