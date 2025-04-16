from django.urls import path
from .views import (
    home, requisition_list, view_requisition, search_candidates, delete_candidate, hr_metrics_view, get_hr_metrics_per_requisition,recruiter_view,
    add_requisition, add_candidates, get_funnel_data, edit_candidate, get_general_funnel_data, general_dashboard, requisition_detail, edit_requisition_redirect, edit_requisition
)

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", general_dashboard, name="dashboard"),
    path("requisitions/", requisition_list, name="requisitions"),
    path("requisition/<str:requisition_no>/", view_requisition, name="view_requisition"),
    path('recruiter-view/', recruiter_view, name='recruiter_view'),
    path("search/", search_candidates, name="search_candidates"),
    path("add-requisition/", add_requisition, name="add_requisition"),
    #path("add-candidate/", add_candidate, name="add_candidate"),
    path("add_candidates/", add_candidates, name="add_candidates"),
    path('edit-candidate/<int:pk>/', edit_candidate, name='edit_candidate'),
    #path('candidates/<str:requisition_no>/', candidate_detail, name='candidate_detail'),
    path("get-funnel-data/<int:requisition_no>/", get_funnel_data, name="get_funnel_data"),
    path("get-general-funnel-data/", get_general_funnel_data, name="get_general_funnel_data"),
    path('requisitions/<int:requisition_no>/', requisition_detail, name='requisition_detail'),
    path('delete-candidate/<int:pk>/', delete_candidate, name='delete_candidate'),
    path("hr-metrics/", hr_metrics_view, name="hr_metrics"),
    path('get-hr-metrics-per-requisition/', get_hr_metrics_per_requisition, name='hr_metrics_per_requisition'),
    path('edit-requisition/', edit_requisition_redirect, name='edit_requisition_redirect'),
    path('edit-requisition/<str:requisition_no>/', edit_requisition, name='edit_requisition'),

]
