"""block_vote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from block_vote_app.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$',display_login),
    url(r'^display_login', display_login, name="display_login"),
    url(r'^logout', logout, name="logout"),
    url(r'^check_login', check_login, name="check_login"),
    url(r'^show_home_admin', show_home_admin, name="show_home_admin"),
    url(r'^register', register, name="register"),
    url(r'^view_requests', view_requests, name="view_requests"),
    url(r'^show_home_voter', show_home_voter, name="show_home_voter"),
    url(r'^show_home_candidate', show_home_candidate, name="show_home_candidate"),
    url(r'^show_home_election_committee', show_home_election_committee, name="show_home_election_committee"),
    url(r'^approve1', approve1, name="approve1"),
    url(r'^reject1', reject1, name="reject1"),
    url(r'^view_vote_result', view_vote_result, name="view_vote_result"),

    url(r'^display_nomination', display_nomination, name="display_nomination"),
    url(r'^nomination_submission', nomination_submission, name="nomination_submission"),
    url(r'^show_first_nomination', show_first_nomination, name="show_first_nomination"),
    url(r'^view_second_nomination', view_second_nomination, name="view_second_nomination"),
    url(r'^for_third_nomination', for_third_nomination, name="for_third_nomination"),
    url(r'^principal_forth_nomination', principal_forth_nomination, name="principal_forth_nomination"),

    url(r'^accept', accept, name="accept"),
    url(r'^drop', drop, name="drop"),
    url(r'^sd_accept', sd_accept, name="sd_accept"),
    url(r'^sd_drop', sd_drop, name="sd_drop"),
    url(r'^eic_accept', eic_accept, name="eic_accept"),
    url(r'^eic_drop', eic_drop, name="eic_drop"),
    url(r'^principal_accept', principal_accept, name="principal_accept"),
    url(r'^principal_drop', principal_drop, name="principal_drop"),
    url(r'^delete_data',delete_data,name="delete_data"),
    url(r'^view_candidates',view_candidates,name="view_candidates"),
    url(r'^show_candidates_list',show_candidates_list,name="show_candidates_list"),
    url(r'^preview_candidates_list_candidate',preview_candidates_list_candidate,name="preview_candidates_list_candidate"),
    url(r'^voter_view_candidates',voter_view_candidates,name="voter_view_candidates"),
    url(r'^render_set_vote_time',render_set_vote_time,name="render_set_vote_time"),
    url(r'^submit_vote_time',submit_vote_time,name="submit_vote_time"),
    url(r'^dis_vote_page_voter',dis_vote_page_voter,name="dis_vote_page_voter"),
    url(r'^do_vote',do_vote,name="do_vote"),
    url(r'^perform_do_vote',perform_do_vote,name="perform_do_vote"),
    url(r'^visible_vote_page_candidate',visible_vote_page_candidate,name="visible_vote_page_candidate"),
    url(r'^publish_vote_result',publish_vote_result,name="publish_vote_result"),
    url(r'^get_vote_result',get_vote_result,name="get_vote_result"),
    url(r'^reveal_result_voter',reveal_result_voter,name="reveal_result_voter"),
    url(r'^exhibit_result_candidate',exhibit_result_candidate,name="exhibit_result_candidate"),
]
