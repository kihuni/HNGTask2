from django.urls import path
from .views import RegisterView, LoginView, UserDetailView, OrganisationListView, OrganisationDetailView, OrganisationCreateView, AddUserToOrganisationView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('api/users/<str:pk>', UserDetailView.as_view(), name='user-detail'),
    path('api/organisations', OrganisationListView.as_view(), name='organisation-list'),
    path('api/organisations/create', OrganisationCreateView.as_view(), name='organisation-create'),
    path('api/organisations/<str:orgId>', OrganisationDetailView.as_view(), name='organisation-detail'),
    path('api/organisations/<str:orgId>/add-user', AddUserToOrganisationView.as_view(), name='add-user-to-organisation')
]
