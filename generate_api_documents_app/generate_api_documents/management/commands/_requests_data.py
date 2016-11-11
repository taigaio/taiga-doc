# -*- coding: utf-8 -*-
# Copyright (C) 2014-2016 Andrey Antukh <niwi@niwi.nz>
# Copyright (C) 2014-2016 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014-2016 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014-2016 Alejandro Alonso <alejandro.alonso@kaleidos.net>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import OrderedDict

from taiga.external_apps.models import Application, ApplicationToken
from taiga.webhooks.models import Webhook
from taiga.users.models import User
from taiga.auth.tokens import get_token_for_user
from taiga.projects.epics.models import RelatedUserStory
from taiga.projects.models import Project, Membership
from taiga.projects.notifications.models import NotifyPolicy
from taiga.projects.history.models import HistoryEntry
from taiga.projects.history.choices import HistoryType
from taiga.projects.services import transfer as transfer_service

USER_ID = 6
user = User.objects.get(id=USER_ID)

(membership, _) = Membership.objects.get_or_create(
    token="00000000-0000-0000-0000-000000000000",
    defaults={
        "user_id": None,
        "project_id": 1,
        "role_id": 3,
        "is_admin": False,
        "email": "test@test.com",
        "invited_by_id": 1,
        "invitation_extra_text": "",
        "user_order": 1,
    }
)
membership.user_id = None
membership.save()


(app, _) = Application.objects.get_or_create(
    id="00000000-0000-0000-0000-000000000000",
    defaults={
        "name": "example application",
        "icon_url": None,
        "web": "http://example.com",
        "description": "description paragraph",
        "next_url": "http://example.com",
    }
)

(app2, _) = Application.objects.get_or_create(
    id="00000000-0000-0000-0000-000000000001",
    defaults={
        "name": "example application 2",
        "icon_url": None,
        "web": "http://example.com",
        "description": "description paragraph",
        "next_url": "http://example.com",
    }
)

(app_token, _) = ApplicationToken.objects.get_or_create(
    user_id=USER_ID,
    application=app,
    defaults={
        "auth_code": "00000000-0000-0000-0000-000000000002",
        "token": "00000000-0000-0000-0000-000000000001",
        "state": "random-state",
    }
)

(app_token2, _) = ApplicationToken.objects.get_or_create(
    user_id=USER_ID,
    application=app2,
    defaults={
        "auth_code": "00000000-0000-0000-0000-000000000004",
        "token": "00000000-0000-0000-0000-000000000003",
        "state": "random-state",
    }
)

entry = HistoryEntry.objects.filter(project_id=1, key="userstories.userstory:2", type=HistoryType.change).first()
entry.id = "00000000-0000-0000-0000-000000000000"
entry.save()

Webhook.objects.create(project_id=1, name="Webhook", url="http://localhost:3000/htbin/test.py", key="test-key")

test_file = "$$INCLUDE_FILE$$test.png"
dump_file = "$$INCLUDE_FILE$$dump.json"

project1 = Project.objects.get(id=1)
project1.owner_id = USER_ID
project1.save()
transfer_service.start_project_transfer(project1, user, "test")

project2 = Project.objects.get(id=3)
project1.owner_id = USER_ID
project1.save()
transfer_service.start_project_transfer(project2, user, "test")
related_user_story = RelatedUserStory.objects.filter(epic__project_id=project2.id).first()
related_user_story_id = related_user_story.user_story.id
epic = related_user_story.epic
epics_attachment = epic.attachments.all().first().id
epic_ref = epic.ref
epic_id = epic.id
epic_custom_attribute_id = project2.epiccustomattributes.all().first().id
epic_custom_attribute_id2 = project2.epiccustomattributes.all()[2].id
user_stories_attachment = project2.user_stories.first().attachments.all().first().id
user_story_ref = project1.user_stories.first().ref
user_story_id = project1.user_stories.first().id
user_story_custom_attribute_id = project1.userstorycustomattributes.all().first().id
user_story_custom_attribute_id2 = project1.userstorycustomattributes.all()[2].id
issues_attachment = project2.issues.first().attachments.all().first().id
issue_ref = project1.issues.first().ref
issue_id = project1.issues.first().id
issue_custom_attribute_id = project1.issuecustomattributes.all().first().id
issue_custom_attribute_id2 = project1.issuecustomattributes.all()[2].id
tasks_attachment = project2.tasks.first().attachments.all().first().id
task_ref = project1.tasks.first().ref
task_id = project1.tasks.first().id
task_custom_attribute_id = project1.taskcustomattributes.all().first().id
task_custom_attribute_id2 = project1.taskcustomattributes.all()[2].id
wiki_id = project1.wiki_pages.first().id
wiki_link_id = project1.wiki_links.first().id
wiki_attachment = project2.wiki_pages.first().attachments.all().first().id
milestone_id = project1.milestones.first().id
milestone_slug = project1.milestones.first().slug

notify_policy_id = NotifyPolicy.objects.filter(user_id=USER_ID).first().id
owned_project = Project.objects.filter(owner_id=USER_ID).first()

tags = [t[0] for t in project1.tags_colors[0:4]]

reqs = OrderedDict([
    ("projects-tags-colors", {
        "method": "GET",
        "url": "/api/v1/projects/1/tags_colors",
    }),

    ("projects-create-tag", {
        "method": "POST",
        "url": "/api/v1/projects/1/create_tag",
        "body": {
            "tag": "testing-tag",
            "color": "#FC8EAC"
        }
    }),
    ("projects-edit-tag", {
        "method": "POST",
        "url": "/api/v1/projects/1/edit_tag",
        "body": {
            "from_tag": "testing-tag",
            "to_tag": "testing-tag-updated",
            "color": "#FFF8E7"
        }
    }),
    ("projects-delete-tag", {
        "method": "POST",
        "url": "/api/v1/projects/1/delete_tag",
        "body": {
            "tag": "testing-tag-updated",
        }
    }),
    ("projects-mix-tags", {
        "method": "POST",
        "url": "/api/v1/projects/1/mix_tags",
        "body": {
            "from_tags": tags,
            "to_tag": tags[0]
        }
    }),
    ("memberships-bulk-create", {
        "method": "POST",
        "url": "/api/v1/memberships/bulk_create",
        "body": {
            "project_id": 1,
            "bulk_memberships": [
                {"role_id": 3, "username": "test@test.com"},
                {"role_id": 4, "username": "john@doe.com"}
            ]
        }
    }),
    ("invitations-get", {
        "method": "GET",
        "url": "/api/v1/invitations/00000000-0000-0000-0000-000000000000"
    }),
    ("memberships-create", {
        "method": "POST",
        "url": "/api/v1/memberships",
        "body": {
            "project": 1,
            "role": 3,
            "username": "test-user@test.com"
        }
    }),
    ("memberships-get", {
        "method": "GET",
        "url": "/api/v1/memberships/1",
    }),
    ("memberships-resend-invitation", {
        "method": "POST",
        "url": "/api/v1/memberships/1/resend_invitation",
    }),
    ("memberships-list", {
        "method": "GET",
        "url": "/api/v1/memberships",
    }),
    ("memberships-filtered-list", {
        "method": "GET",
        "url": "/api/v1/memberships?project=1",
    }),
    ("register-user", {
        "method": "POST",
        "url": "/api/v1/auth/register",
        "body": {
            "type": "private",
            "existing": False,
            "token": "00000000-0000-0000-0000-000000000000",
            "username": "test-username",
            "password": "password",
            "email": "test-register@email.com",
            "full_name": "test"
        }
    }),
    ("normal-register", {
        "method": "POST",
        "url": "/api/v1/auth/register",
        "body": {
            "type": "public",
            "username": "test-username2",
            "password": "password",
            "email": "test-register2@email.com",
            "full_name": "test"
        }
    }),
    ("normal-login", {
        "method": "POST",
        "url": "/api/v1/auth",
        "body": {
            "type": "normal",
            "username": "test-username",
            "password": "password"
        }
    }),
    ("epics-list", {
        "method": "GET",
        "url": "/api/v1/epics",
        "index": 0,
    }),
    ("epics-filtered-list", {
        "method": "GET",
        "url": "/api/v1/epics?project=1",
    }),
    ("epics-create", {
        "method": "POST",
        "url": "/api/v1/epics",
        "body": {
            "assigned_to": None,
            "blocked_note": "blocking reason",
            "client_requirement": False,
            "description": "New epic description",
            "is_blocked": True,
            "project": 1,
            "epics_order": 2,
            "status": 2,
            "color": "#ABCABC",
            "subject": "New epic",
            "tags": [
                "service catalog",
                "customer"
            ],
            "team_requirement": False,
            "watchers": []
        }
    }),
    ("epics-simple-create", {
        "method": "POST",
        "url": "/api/v1/epics",
        "body": {
            "project": 1,
            "subject": "New epic"
        }
    }),
    ("epics-get", {
        "method": "GET",
        "url": "/api/v1/epics/1",
    }),
    ("epics-get-by-ref", {
        "method": "GET",
        "url": "/api/v1/epics/by_ref?ref={}\&project={}".format(epic_ref, epic.project_id),
    }),
    ("epics-patch", {
        "method": "PATCH",
        "url": "/api/v1/epics/{}".format(epic_id),
        "body": {
            "subject": "Patching subject",
            "version": 1
        }
    }),
    ("epics-bulk-create", {
        "method": "POST",
        "url": "/api/v1/epics/bulk_create",
        "body": {
            "project_id": 1,
            "bulk_epics": "EPIC 1 \n EPIC 2 \n EPIC 3"
        }
    }),
    ("epics-filters-data-get", {
        "method": "GET",
        "url": "/api/v1/epics/filters_data?project=1",
    }),
    ("epics-upvote", {
        "method": "POST",
        "url": "/api/v1/epics/3/upvote",
    }),
    ("epics-voters", {
        "method": "GET",
        "url": "/api/v1/epics/{}/voters".format(task_id),
        "index": 0,
    }),
    ("epics-downvote", {
        "method": "POST",
        "url": "/api/v1/epics/3/downvote",
    }),
    ("epics-attachments-list", {
        "method": "GET",
        "url": "/api/v1/epics/attachments?object_id={}\&project=1".format(epics_attachment),
    }),
    ("epics-attachments-create", {
        "method": "MULTIPART-POST",
        "url": "/api/v1/epics/attachments",
        "body": {
            "object_id": epic_id,
            "project": epic.project.id,
            "attached_file": test_file
        }
    }),
    ("epics-watch", {
        "method": "POST",
        "url": "/api/v1/epics/{}/watch".format(epic_id),
    }),
    ("epics-watchers", {
        "method": "GET",
        "url": "/api/v1/epics/{}/watchers".format(epic_id),
        "index": 0,
    }),
    ("epics-unwatch", {
        "method": "POST",
        "url": "/api/v1/epics/{}/unwatch".format(epic_id),
    }),
    ("epics-attachments-get", {
        "method": "GET",
        "url": "/api/v1/epics/attachments/{}".format(epics_attachment),
    }),
    ("epics-attachments-patch", {
        "method": "PATCH",
        "url": "/api/v1/epics/attachments/{}".format(epics_attachment),
        "body": {
            "description": "Updated description",
        }
    }),
    ("epics-attachments-delete", {
        "method": "DELETE",
        "url": "/api/v1/epics/attachments/{}".format(epics_attachment),
    }),
    ("epic-statuses-patch", {
          "method": "PATCH",
          "url": "/api/v1/epic-statuses/1",
          "body": {
              "name": "Patch status name"
          }
      }),
    ("epic-statuses-create", {
          "method": "POST",
          "url": "/api/v1/epic-statuses",
          "body": {
              "color": "#AAAAAA",
              "is_closed": True,
              "name": "New status",
              "order": 8,
              "project": 1
          }
      }),
    ("epic-statuses-patch", {
        "method": "PATCH",
        "url": "/api/v1/epic-statuses/1",
        "body": {
            "name": "Patch status name"
        }
    }),
    ("epic-statuses-create", {
        "method": "POST",
        "url": "/api/v1/epic-statuses",
        "body": {
            "color": "#AAAAAA",
            "is_closed": True,
            "name": "New status",
            "order": 8,
            "project": 1
        }
    }),
    ("epic-statuses-simple-create", {
        "method": "POST",
        "url": "/api/v1/epic-statuses",
        "body": {
            "project": 1,
            "name": "New status name"
        }
    }),
    ("epic-statuses-get", {
        "method": "GET",
        "url": "/api/v1/epic-statuses/1",
    }),
    ("epic-statuses-bulk-update-order", {
        "method": "POST",
        "url": "/api/v1/epic-statuses/bulk_update_order",
        "body": {
            "project": 1,
            "bulk_epic_statuses": [[1, 10], [2, 5]]
        }
    }),
    ("epic-statuses-list", {
        "method": "GET",
        "url": "/api/v1/epic-statuses",
    }),
    ("epic-statuses-filtered-list", {
        "method": "GET",
        "url": "/api/v1/epic-statuses?project=1",
    }),
    ("epic-statuses-delete", {
        "method": "DELETE",
        "url": "/api/v1/epic-statuses/1",
    }),
    ("epics-custom-attributes-values-patch", {
        "method": "PATCH",
        "url": "/api/v1/epics/custom-attributes-values/{}".format(epic_id),
        "body": {
            "attributes_values": {"{}".format(epic_custom_attribute_id): "240 min"},
            "version": 1
        }
    }),
    ("epics-custom-attributes-values-get", {
        "method": "GET",
        "url": "/api/v1/epics/custom-attributes-values/{}".format(epic_id),
    }),
    ("epics-custom-attributes-patch", {
        "method": "PATCH",
        "url": "/api/v1/epic-custom-attributes/{}".format(epic_custom_attribute_id),
        "body": {
          "name": "Duration 1"
        }
    }),
    ("epics-custom-attributes-create", {
        "method": "POST",
        "url": "/api/v1/epic-custom-attributes",
        "body": {
            "name": "Duration 2",
            "description": "Duration in minutes",
            "order": 8,
            "project": 1
        }
    }),
    ("epics-custom-attributes-simple-create", {
        "method": "POST",
        "url": "/api/v1/epic-custom-attributes",
        "body": {
            "name": "Duration 3",
            "project": 1
        }
    }),
    ("epics-custom-attributes-get", {
        "method": "GET",
        "url": "/api/v1/epic-custom-attributes/{}".format(epic_custom_attribute_id),
    }),
    ("epics-custom-attributes-bulk-update-order", {
        "method": "POST",
        "url": "/api/v1/epic-custom-attributes/bulk_update_order",
        "body": {
            "project": 1,
            "bulk_epic_custom_attributes": [[epic_custom_attribute_id, 10], [epic_custom_attribute_id2, 15]]
        }
    }),
    ("epics-custom-attributes-list", {
        "method": "GET",
        "url": "/api/v1/epic-custom-attributes",
    }),
    ("epics-custom-attributes-filtered-list", {
        "method": "GET",
        "url": "/api/v1/epic-custom-attributes?project=1",
    }),
    ("epics-custom-attributes-delete", {
        "method": "DELETE",
        "url": "/api/v1/epic-custom-attributes/{}".format(epic_custom_attribute_id),
    }),

    ("epics-related-user-stories-bulk-create", {
        "method": "POST",
        "url": "/api/v1/epics/{}/related_userstories/bulk_create".format(epic_id),
        "body": {
            "project_id": epic.project.id,
            "bulk_userstories": "epic 1 \n epic 2 \n epic 3"
        }
    }),
    ("epics-related-user-story-create", {
        "method": "POST",
        "url": "/api/v1/epics/{}/related_userstories".format(epic_id),
        "body": {
            "user_story": user_story_id,
            "epic": epic_id
        }
    }),
    ("epics-related-user-story-patch", {
        "method": "PATCH",
        "url": "/api/v1/epics/{}/related_userstories/{}".format(epic_id, related_user_story_id),
        "body": {
            "order": 100,
        }
    }),
    ("epics-related-user-story-get", {
        "method": "GET",
        "url": "/api/v1/epics/{}/related_userstories/{}".format(epic_id, related_user_story_id),
    }),
    ("epics-related-user-stories-list", {
        "method": "GET",
        "url": "/api/v1/epics/{}/related_userstories".format(epic_id),
        "index": 0,
    }),
    ("epics-related-user-story-delete", {
        "method": "DELETE",
        "url": "/api/v1/epics/{}/related_userstories/{}".format(epic_id, related_user_story_id),
    }),
    ("epics-delete", {
        "method": "DELETE",
        "url": "/api/v1/epics/{}".format(epic_id),
    }),
    ("add-attachment-to-us", {
        "method": "MULTIPART-POST",
        "url": "/api/v1/userstories/attachments",
        "body": {
            "object_id": 1,
            "project": 1,
            "attached_file": test_file
        }
    }),
    ("unwatch", {
        "method": "POST",
        "url": "/api/v1/userstories/1/unwatch"
    }),
    ("user-stories-bulk-update-sprint-order", {
        "method": "POST",
        "url": "/api/v1/userstories/bulk_update_sprint_order",
        "body": {
            "project_id": 1,
            "bulk_stories": [
                {
                    "us_id": 1,
                    "order": 10
                },
                {
                    "us_id": 2,
                    "order": 15
                }
            ]
        }
    }),
    ("user-stories-bulk-create", {
        "method": "POST",
        "url": "/api/v1/userstories/bulk_create",
        "body": {
            "project_id": 1,
            "bulk_stories": "US 1 \n US 2 \n US 3"
        }
    }),
    ("user-stories-bulk-update-milestone", {
        "method": "POST",
        "url": "/api/v1/userstories/bulk_update_milestone",
        "body": {
            "project_id": 1,
            "milestone_id": 1,
            "bulk_stories": [
                {
                    "us_id": 1,
                    "order": 10
                },
                {
                    "us_id": 2,
                    "order": 15
                }
            ]
        }
    }),
    ("user-stories-patch", {
        "method": "PATCH",
        "url": "/api/v1/userstories/1",
        "body": {
            "subject": "Patching subject",
            "version": 1
        }
    }),
    ("user-stories-create", {
        "method": "POST",
        "url": "/api/v1/userstories",
        "body": {
            "assigned_to": None,
            "backlog_order": 2,
            "blocked_note": "blocking reason",
            "client_requirement": False,
            "description": "Implement API CALL",
            "is_blocked": False,
            "is_closed": True,
            "kanban_order": 37,
            "milestone": None,
            "points": {
                "1": 4,
                "2": 3,
                "3": 2,
                "4": 1
            },
            "project": 1,
            "sprint_order": 2,
            "status": 2,
            "subject": "Customer personal data",
            "tags": [
                "service catalog",
                "customer"
            ],
            "team_requirement": False,
            "watchers": []
        }
    }),
    ("user-stories-simple-create", {
        "method": "POST",
        "url": "/api/v1/userstories",
        "body": {
            "project": 1,
            "subject": "Customer personal data"
        }
    }),
    ("user-stories-get", {
        "method": "GET",
        "url": "/api/v1/userstories/1",
    }),
    ("user-stories-filter-data", {
        "method": "GET",
        "url": "/api/v1/userstories/filters_data?project=1",
    }),
    ("user-stories-watch", {
        "method": "POST",
        "url": "/api/v1/userstories/1/watch",
    }),
    ("user-stories-get-voters", {
        "method": "GET",
        "url": "/api/v1/userstories/2/voters",
        "index": 0,
    }),
    ("user-stories-attachments-list", {
        "method": "GET",
        "url": "/api/v1/userstories/attachments?object_id=1\&project=1",
    }),
    ("user-stories-attachment-patch", {
        "method": "PATCH",
        "url": "/api/v1/userstories/attachments/1",
        "body": {"description": "patching description"}
    }),
    ("user-stories-upvote", {
        "method": "POST",
        "url": "/api/v1/userstories/1/upvote",
    }),
    ("user-stories-list", {
        "method": "GET",
        "url": "/api/v1/userstories",
        "index": 0,
    }),
    ("user-stories-filtered-list", {
        "method": "GET",
        "url": "/api/v1/userstories?project=1",
    }),
    ("user-stories-downvote", {
        "method": "POST",
        "url": "/api/v1/userstories/1/downvote",
    }),
    ("user-stories-get-by-ref", {
        "method": "GET",
        "url": "/api/v1/userstories/by_ref?ref={}\&project=1".format(user_story_ref),
    }),
    ("user-stories-get-watchers", {
        "method": "GET",
        "url": "/api/v1/userstories/1/watchers",
        "index": 0,
    }),
    ("user-stories-attachments-get", {
        "method": "GET",
        "url": "/api/v1/userstories/attachments/415",
    }),
    ("user-stories-bulk-update-backlog-order", {
        "method": "POST",
        "url": "/api/v1/userstories/bulk_update_backlog_order",
        "body": {
            "project_id": 1,
            "bulk_stories": [
                {
                    "us_id": 1,
                    "order": 10
                },
                {
                    "us_id": 2,
                    "order": 15
                }
            ]
        }
    }),
    ("user-stories-bulk-update-kanban-order", {
        "method": "POST",
        "url": "/api/v1/userstories/bulk_update_kanban_order",
        "body": {
            "project_id": 1,
            "bulk_stories": [
                {
                    "us_id": 1,
                    "order": 10
                },
                {
                    "us_id": 2,
                    "order": 15
                }
            ]
        }
    }),
    ("projects-timeline-get", {
        "method": "GET",
        "url": "/api/v1/timeline/project/1",
        "index": 0,
    }),
    ("users-timeline-get", {
        "method": "GET",
        "url": "/api/v1/timeline/user/1",
    }),
    ("profile-timeline-get", {
        "method": "GET",
        "url": "/api/v1/timeline/profile/1",
    }),
    ("issue-statues-patch", {
        "method": "PATCH",
        "url": "/api/v1/issue-statuses/1",
        "body": {
            "name": "Patch status name"
        }
    }),
    ("issue-statuses-create", {
        "method": "POST",
        "url": "/api/v1/issue-statuses",
        "body": {
            "color": "#AAAAAA",
            "is_closed": True,
            "name": "New status",
            "order": 8,
            "project": 1
        }
    }),
    ("issue-statuses-simple-create", {
        "method": "POST",
        "url": "/api/v1/issue-statuses",
        "body": {
            "project": 1,
            "name": "New status name"
        }
    }),
    ("issue-statuses-get", {
        "method": "GET",
        "url": "/api/v1/issue-statuses/1",
    }),
    ("issue-statuses-bulk-update-order", {
        "method": "POST",
        "url": "/api/v1/issue-statuses/bulk_update_order",
        "body": {
            "project": 1,
            "bulk_issue_statuses": [[1, 10], [2, 5]]
        }
    }),
    ("issue-statuses-list", {
        "method": "GET",
        "url": "/api/v1/issue-statuses",
    }),
    ("issue-statuses-filtered-list", {
        "method": "GET",
        "url": "/api/v1/issue-statuses?project=1",
    }),
    ("user-stories-custom-attributes-patch", {
        "method": "PATCH",
        "url": "/api/v1/userstory-custom-attributes/1",
        "body": {
            "name": "Duration 1"
        }
    }),
    ("user-stories-custom-attributes-create", {
        "method": "POST",
        "url": "/api/v1/userstory-custom-attributes",
        "body": {
            "name": "Duration 2",
            "description": "Duration in minutes",
            "order": 8,
            "project": 1
        }
    }),
    ("user-stories-custom-attributes-simple-create", {
        "method": "POST",
        "url": "/api/v1/userstory-custom-attributes",
        "body": {
            "name": "Duration 3",
            "project": 1
        }
    }),
    ("user-stories-custom-attributes-get", {
        "method": "GET",
        "url": "/api/v1/userstory-custom-attributes/1",
    }),
    ("user-stories-custom-attributes-bulk-update-order", {
        "method": "POST",
        "url": "/api/v1/userstory-custom-attributes/bulk_update_order",
        "body": {
            "project": 1,
            "bulk_userstory_custom_attributes": [[1, 10], [2, 5]]
        }
    }),
    ("user-stories-custom-attributes-list", {
        "method": "GET",
        "url": "/api/v1/userstory-custom-attributes",
    }),
    ("user-stories-custom-attributes-filtered-list", {
        "method": "GET",
        "url": "/api/v1/userstory-custom-attributes?project=1",
    }),
    ("tasks-custom-attributes-values-patch", {
        "method": "PATCH",
        "url": "/api/v1/tasks/custom-attributes-values/{}".format(task_id),
        "body": {
            "attributes_values": {"{}".format(task_custom_attribute_id): "240 min"},
            "version": 1
        }
    }),
    ("tasks-custom-attributes-values-get", {
        "method": "GET",
        "url": "/api/v1/tasks/custom-attributes-values/{}".format(task_id),
    }),
    ("projects-export", {
        "method": "GET",
        "url": "/api/v1/exporter/1",
    }),
    ("projects-import", {
        "method": "MULTIPART-POST",
        "url": "/api/v1/importer/load_dump",
        "body": {
            "dump": dump_file
        }
    }),
    ("severities-patch", {
        "method": "PATCH",
        "url": "/api/v1/severities/1",
        "body": {
            "name": "Patch name"
        }
    }),
    ("severities-create", {
        "method": "POST",
        "url": "/api/v1/severities",
        "body": {
            "color": "#AAAAAA",
            "name": "New severity",
            "order": 8,
            "project": 1
        }
    }),
    ("severities-simple-create", {
        "method": "POST",
        "url": "/api/v1/severities",
        "body": {
            "project": 1,
            "name": "New severity name"
        }
    }),
    ("severities-get", {
        "method": "GET",
        "url": "/api/v1/severities/1",
    }),
    ("severities-bulk-update-order", {
        "method": "POST",
        "url": "/api/v1/severities/bulk_update_order",
        "body": {
            "project": 1,
            "bulk_severities": [[1, 10], [2, 5]]
        }
    }),
    ("severities-list", {
        "method": "GET",
        "url": "/api/v1/severities",
    }),
    ("severities-filtered-list", {
        "method": "GET",
        "url": "/api/v1/severities?project=1",
    }),
    ("user-stories-edit-comment", {
        "method": "POST",
        "url": "/api/v1/history/userstory/2/edit_comment?id=00000000-0000-0000-0000-000000000000",
        "body": {
            "comment": "comment edition"
        }
    }),
    ("user-stories-get-comment-versions", {
        "method": "GET",
        "url": "/api/v1/history/userstory/2/comment_versions?id=00000000-0000-0000-0000-000000000000",
        "index": 0,
    }),
    ("user-story-delete-comment", {
        "method": "POST",
        "url": "/api/v1/history/userstory/2/delete_comment?id=00000000-0000-0000-0000-000000000000",
    }),
    ("user-stories-get-history", {
        "method": "GET",
        "url": "/api/v1/history/userstory/2",
        "index": 0,
    }),
    ("user-stories-undelete-comment", {
        "method": "POST",
        "url": "/api/v1/history/userstory/2/undelete_comment?id=00000000-0000-0000-0000-000000000000",
    }),
    ("task-statuses-patch", {
        "method": "PATCH",
        "url": "/api/v1/task-statuses/1",
        "body": {
            "name": "Patch status name"
        }
    }),
    ("task-statuses-create", {
        "method": "POST",
        "url": "/api/v1/task-statuses",
        "body": {
            "color": "#AAAAAA",
            "is_closed": True,
            "name": "New status",
            "order": 8,
            "project": 1
        }
    }),
    ("task-statuses-simple-create", {
        "method": "POST",
        "url": "/api/v1/task-statuses",
        "body": {
            "project": 1,
            "name": "New status name"
        }
    }),
    ("task-statuses-get", {
        "method": "GET",
        "url": "/api/v1/task-statuses/1",
    }),
    ("task-statuses-bulk-update-order", {
        "method": "POST",
        "url": "/api/v1/task-statuses/bulk_update_order",
        "body": {
            "project": 1,
            "bulk_task_statuses": [[1, 10], [2, 5]]
        }
    }),
    ("task-statuses-list", {
        "method": "GET",
        "url": "/api/v1/task-statuses",
    }),
    ("task-statuses-filtered-list", {
        "method": "GET",
        "url": "/api/v1/task-statuses?project=1",
    }),
    ("issues-attachments-create", {
        "method": "MULTIPART-POST",
        "url": "/api/v1/issues/attachments",
        "body": {
            "object_id": issue_id,
            "project": 1,
            "attached_file": test_file
        }
    }),
    ("issues-unwatch", {
        "method": "POST",
        "url": "/api/v1/issues/3/unwatch",
    }),
    ("issues-bulk-create", {
        "method": "POST",
        "url": "/api/v1/issues/bulk_create",
        "body": {
            "project_id": 1,
            "bulk_issues": "Issue 1 \n Issue 2 \n Issue 3"
        }
    }),
    ("issues-patch", {
        "method": "PATCH",
        "url": "/api/v1/issues/3",
        "body": {
            "version": 1,
            "subject": "Patching subject"
        }
    }),
    ("issues-create", {
        "method": "POST",
        "url": "/api/v1/issues",
        "body": {
            "assigned_to": None,
            "blocked_note": "blocking reason",
            "description": "Implement API CALL",
            "is_blocked": False,
            "is_closed": True,
            "milestone": None,
            "project": 1,
            "status": 3,
            "severity": 2,
            "priority": 3,
            "type": 1,
            "subject": "Customer personal data",
            "tags": [
                "service catalog",
                "customer"
            ],
            "watchers": []
        }
    }),
    ("issues-simple-create", {
        "method": "POST",
        "url": "/api/v1/issues",
        "body": {
            "project": 1,
            "subject": "Customer personal data"
        }
    }),
    ("issues-get", {
        "method": "GET",
        "url": "/api/v1/issues/3",
    }),
    ("issues-filters-data-get", {
        "method": "GET",
        "url": "/api/v1/issues/filters_data?project=1",
    }),
    ("issues-watch", {
        "method": "POST",
        "url": "/api/v1/issues/3/watch",
    }),
    ("issues-voters", {
        "method": "GET",
        "url": "/api/v1/issues/3/voters",
        "index": 0,
    }),
    ("issues-attachments-list", {
        "method": "GET",
        "url": "/api/v1/issues/attachments?object_id={}\&project=1".format(issues_attachment),
    }),
    ("issues-attachment-patch", {
        "method": "PATCH",
        "url": "/api/v1/issues/attachments/{}".format(issues_attachment),
    }),
    ("issues-attachment-get", {
        "method": "GET",
        "url": "/api/v1/issues/attachments/{}".format(issues_attachment),
    }),
    ("issues-upvote", {
        "method": "POST",
        "url": "/api/v1/issues/3/upvote",
    }),
    ("issues-list", {
        "method": "GET",
        "url": "/api/v1/issues",
        "index": 0,
    }),
    ("issues-filtered-list", {
        "method": "GET",
        "url": "/api/v1/issues?project=1",
    }),
    ("issues-filtered-and-ordered-list", {
        "method": "GET",
        "url": "/api/v1/issues?project=1\&order_by=priority",
    }),
    ("issues-downvote", {
        "method": "POST",
        "url": "/api/v1/issues/3/downvote",
    }),
    ("issues-get-by-ref", {
        "method": "GET",
        "url": "/api/v1/issues/by_ref?ref={}\&project=1".format(issue_ref),
    }),
    ("issues-watchers", {
        "method": "GET",
        "url": "/api/v1/issues/3/watchers",
        "index": 0,
    }),
    ("priorities-patch", {
        "method": "PATCH",
        "url": "/api/v1/priorities/1",
        "body": {
            "name": "Patch name"
        }
    }),
    ("priorities-create", {
        "method": "POST",
        "url": "/api/v1/priorities",
        "body": {
            "color": "#AAAAAA",
            "name": "New priority",
            "order": 8,
            "project": 1
        }
    }),
    ("priorities-simple-create", {
        "method": "POST",
        "url": "/api/v1/priorities",
        "body": {
            "project": 1,
            "name": "New priority name"
        }
    }),
    ("priorities-get", {
        "method": "GET",
        "url": "/api/v1/priorities/1",
    }),
    ("priorities-bulk-update-order", {
        "method": "POST",
        "url": "/api/v1/priorities/bulk_update_order",
        "body": {
            "project": 1,
            "bulk_priorities": [[1, 10], [2, 5]]
        }
    }),
    ("priorities-list", {
        "method": "GET",
        "url": "/api/v1/priorities",
    }),
    ("priorities-filtered-list", {
        "method": "GET",
        "url": "/api/v1/priorities?project=1",
    }),
    ("webhooklogs-list", {
        "method": "GET",
        "url": "/api/v1/webhooklogs",
    }),
    ("webhooklogs-filtered-list", {
        "method": "GET",
        "url": "/api/v1/webhooklogs?webhook=1",
    }),
    ("webhooks-test", {
        "method": "POST",
        "url": "/api/v1/webhooks/1/test",
    }),
    ("webhooks-patch", {
        "method": "PATCH",
        "url": "/api/v1/webhooks/1",
        "body": {
            "name": "My service name"
        }
    }),
    ("webhooks-create", {
        "method": "POST",
        "url": "/api/v1/webhooks",
        "body": {
            "project": 1,
            "name": "My service webhook",
            "url": "http://myservice.com/webhooks",
            "key": "my-very-secret-key"
        }
    }),
    ("webhooks-get", {
        "method": "GET",
        "url": "/api/v1/webhooks/1",
    }),
    ("webhooklogs-get", {
        "method": "GET",
        "url": "/api/v1/webhooklogs/1",
    }),
    ("webhooks-list", {
        "method": "GET",
        "url": "/api/v1/webhooks",
    }),
    ("webhooks-filtered-list", {
        "method": "GET",
        "url": "/api/v1/webhooks?project=1",
    }),
    ("webhooklogs-resend", {
        "method": "POST",
        "url": "/api/v1/webhooklogs/1/resend",
    }),
    ("notify-policies-patch", {
        "method": "PATCH",
        "url": "/api/v1/notify-policies/{}".format(notify_policy_id),
        "body": {
          "notify_level": 2
        }
    }),
    ("notify-policies-get", {
        "method": "GET",
        "url": "/api/v1/notify-policies/{}".format(notify_policy_id),
    }),
    ("notify-policies-list", {
        "method": "GET",
        "url": "/api/v1/notify-policies",
    }),
    ("issues-custom-attributes-values-patch", {
        "method": "PATCH",
        "url": "/api/v1/issues/custom-attributes-values/{}".format(issue_id),
        "body": {
            "attributes_values": {"{}".format(issue_custom_attribute_id): "240 min"},
            "version": 1
        }
    }),
    ("issues-custom-attributes-values-get", {
        "method": "GET",
        "url": "/api/v1/issues/custom-attributes-values/{}".format(issue_id),
    }),
    ("stats-discover", {
        "method": "GET",
        "url": "/api/v1/stats/discover",
    }),
    ("stats-system", {
        "method": "GET",
        "url": "/api/v1/stats/system",
    }),
    ("user-storage-create", {
        "method": "POST",
        "url": "/api/v1/user-storage",
        "body": {
            "key": "favorite-forest",
            "value": "Taiga"
        }
    }),
    ("user-storage-patch", {
        "method": "PATCH",
        "url": "/api/v1/user-storage/favorite-forest",
        "body": {
            "value": "Russian Taiga"
        }
    }),
    ("user-storage-get", {
        "method": "GET",
        "url": "/api/v1/user-storage/favorite-forest",
    }),
    ("user-storage-list", {
        "method": "GET",
        "url": "/api/v1/user-storage",
    }),
    ("projects-unwatch", {
        "method": "POST",
        "url": "/api/v1/projects/1/unwatch",
    }),
    ("projects-create-template", {
        "method": "POST",
        "admin_needed": True,
        "url": "/api/v1/projects/1/create_template",
        "body": {
            "template_name": "Beta template",
            "template_description": "Beta template description"
        }
    }),
    ("projects-stats", {
        "method": "GET",
        "url": "/api/v1/projects/1/stats",
    }),
    ("projects-change-logo", {
        "method": "MULTIPART-POST",
        "url": "/api/v1/projects/1/change_logo",
        "body": {
            "logo": test_file
        }
    }),
    ("projects-issues-stats", {
        "method": "GET",
        "url": "/api/v1/projects/1/issues_stats",
    }),
    ("projects-update", {
        "method": "PUT",
        "url": "/api/v1/projects/1",
        "body": {
            "name": "Beta project put",
            "description": "Beta description"
        }
    }),
    ("projects-patch", {
        "method": "PATCH",
        "url": "/api/v1/projects/1",
        "body": {
            "name": "Beta project patch"
        }
    }),
    ("projects-simple-create", {
        "method": "POST",
        "url": "/api/v1/projects",
        "body": {
            "name": "Beta project",
            "description": "Beta description"
        }
    }),
    ("projects-create", {
        "method": "POST",
        "url": "/api/v1/projects",
        "body": {
            "name": "Beta project",
            "description": "Taiga",
            "creation_template": 1,
            "is_backlog_activated": False,
            "is_issues_activated": True,
            "is_kanban_activated": True,
            "is_private": False,
            "is_wiki_activated": True,
            "videoconferences": "appear-in",
            "videoconferences_extra_data": None,
            "total_milestones": 3,
            "total_story_points": 20.0
        }
    }),
    ("projects-get", {
        "method": "GET",
        "url": "/api/v1/projects/1",
    }),
    ("projects-watch", {
        "method": "POST",
        "url": "/api/v1/projects/1/watch",
        "body": {
            "notify_level": 3
        }
    }),
    ("projects-bulk-update-order", {
        "method": "POST",
        "url": "/api/v1/projects/bulk_update_order",
        "body": [
            {
                "project_id": 1,
                "order": 10
            },
            {
                "project_id": 2,
                "order": 15
            }
        ]
    }),
    ("projects-unlike", {
        "method": "POST",
        "url": "/api/v1/projects/1/unlike",
    }),
    ("projects-get-by-slug", {
        "method": "GET",
        "url": "/api/v1/projects/by_slug?slug=project-0",
    }),
    ("projects-modules-get", {
        "method": "GET",
        "url": "/api/v1/projects/1/modules",
    }),
    ("projects-fans", {
        "method": "GET",
        "url": "/api/v1/projects/1/fans",
        "index": 0,
    }),
    ("projects-transfer-request", {
        "method": "POST",
        "url": "/api/v1/projects/1/transfer_request",
    }),
    ("projects-transfer-validate-token", {
        "method": "POST",
        "url": "/api/v1/projects/1/transfer_validate_token",
        "body": {
            "token": project1.transfer_token,
        }
    }),
    ("projects-transfer-accept", {
        "method": "POST",
        "url": "/api/v1/projects/{}/transfer_accept".format(project2.id),
        "body": {
            "token": project2.transfer_token,
            "reason": "testing"
        }
    }),
    ("projects-transfer-reject", {
        "method": "POST",
        "url": "/api/v1/projects/1/transfer_reject",
        "body": {
            "token": project1.transfer_token,
            "reason": "testing"
        }
    }),
    ("projects-list", {
        "method": "GET",
        "url": "/api/v1/projects",
        "index": 0,
    }),
    ("projects-filtered-list", {
        "method": "GET",
        "url": "/api/v1/projects?member=1",
    }),
    ("projects-filtered-and-ordered-list", {
        "method": "GET",
        "url": "/api/v1/projects?member=1\&order_by=memberships__user_order",
    }),
    ("projects-modules-patch", {
        "method": "PATCH",
        "url": "/api/v1/projects/1/modules",
        "body": {
            "github": {
                "secret": "new_secret"
            }
        }
    }),
    ("projects-start-tranfer", {
        "method": "POST",
        "url": "/api/v1/projects/{}/transfer_start".format(owned_project.id),
        "body": {
            "user": owned_project.memberships.exclude(user_id__isnull=True, user_id=USER_ID).first().user_id,
        }
    }),
    ("projects-like", {
        "method": "POST",
        "url": "/api/v1/projects/1/like",
    }),
    ("projects-watchers", {
        "method": "GET",
        "url": "/api/v1/projects/1/watchers",
        "index": 0
    }),
    ("projects-remove-logo", {
        "method": "POST",
        "url": "/api/v1/projects/1/remove_logo",
    }),
    ("issue-types-patch", {
        "method": "PATCH",
        "url": "/api/v1/issue-types/1",
        "body": {
          "name": "Patch type name"
        }
    }),
    ("issue-types-create", {
        "method": "POST",
        "url": "/api/v1/issue-types",
        "body": {
            "color": "#AAAAAA",
            "name": "New type",
            "order": 8,
            "project": 1
        }
    }),
    ("issue-types-simple-create", {
        "method": "POST",
        "url": "/api/v1/issue-types",
        "body": {
            "project": 1,
            "name": "New type name"
        }
    }),
    ("issue-types-get", {
        "method": "GET",
        "url": "/api/v1/issue-types/1",
    }),
    ("issue-types-bulk-update-order", {
        "method": "POST",
        "url": "/api/v1/issue-types/bulk_update_order",
        "body": {
            "project": 1,
            "bulk_issue_types": [[1, 10], [2, 5]]
        }
    }),
    ("issue-types-list", {
        "method": "GET",
        "url": "/api/v1/issue-types",
    }),
    ("issue-types-filtered-list", {
        "method": "GET",
        "url": "/api/v1/issue-types?project=1",
    }),
    ("wiki-attachments-create", {
        "method": "MULTIPART-POST",
        "url": "/api/v1/wiki/attachments",
        "body": {
            "object_id": wiki_id,
            "project": 1,
            "attached_file": test_file
        }
    }),
    ("wiki-unwatch", {
        "method": "POST",
        "url": "/api/v1/wiki/{}/unwatch".format(wiki_id),
    }),
    ("wiki-patch", {
        "method": "PATCH",
        "url": "/api/v1/wiki/{}".format(wiki_id),
        "body": {
          "subject": "Patching subject",
          "version": 1
        }
    }),
    ("wiki-create", {
        "method": "POST",
        "url": "/api/v1/wiki",
        "body": {
            "project": 1,
            "slug": "new-page",
            "content": "Lorem ipsum dolor.",
            "watchers": []
        }
    }),
    ("wiki-simple-create", {
        "method": "POST",
        "url": "/api/v1/wiki",
        "body": {
            "project": 1,
            "slug": "new-simple-page",
            "content": "Lorem ipsum dolor."
        }
    }),
    ("wiki-get", {
        "method": "GET",
        "url": "/api/v1/wiki/{}".format(wiki_id),
    }),
    ("wiki-watch", {
        "method": "POST",
        "url": "/api/v1/wiki/{}/watch".format(wiki_id),
    }),
    ("wiki-get-by-slug", {
        "method": "GET",
        "url": "/api/v1/wiki/by_slug?slug=home\&project=1",
    }),
    ("wiki-attachments-list", {
        "method": "GET",
        "url": "/api/v1/wiki/attachments?object_id={}\&project=1".format(wiki_id),
    }),
    ("wiki-attachments-patch", {
        "method": "PATCH",
        "url": "/api/v1/wiki/attachments/{}".format(wiki_attachment),
        "body": {
            "description": "Updated description",
        }
    }),
    ("wiki-list", {
        "method": "GET",
        "url": "/api/v1/wiki",
    }),
    ("wiki-filtered-list", {
        "method": "GET",
        "url": "/api/v1/wiki?project=1",
    }),
    ("wiki-watchers", {
        "method": "GET",
        "url": "/api/v1/wiki/{}/watchers".format(wiki_id),
        "index": 0,
    }),
    ("wiki-attachments-get", {
        "method": "GET",
        "url": "/api/v1/wiki/attachments/{}".format(wiki_attachment),
    }),
    ("feedback", {
        "method": "POST",
        "url": "/api/v1/feedback",
        "body": {
            "comment": "Testing feedback"
        }
    }),
    ("wiki-links-patch", {
        "method": "PATCH",
        "url": "/api/v1/wiki-links/{}".format(wiki_link_id),
        "body": {
            "subject": "Patching subject"
        }
    }),
    ("wiki-links-create", {
        "method": "POST",
        "url": "/api/v1/wiki-links",
        "body": {
            "project": 1,
            "title": "Home page",
            "href": "home",
            "order": 1
        }
    }),
    ("wiki-links-simple-create", {
        "method": "POST",
        "url": "/api/v1/wiki-links",
        "body": {
            "project": 1,
            "title": "Home page",
            "href": "home"
        }
    }),
    ("wiki-links-get", {
        "method": "GET",
        "url": "/api/v1/wiki-links/{}".format(wiki_link_id),
    }),
    ("wiki-links-list", {
        "method": "GET",
        "url": "/api/v1/wiki-links",
    }),
    ("wiki-links-filtered-list", {
        "method": "GET",
        "url": "/api/v1/wiki-links?project=1",
    }),
    ("issues-custom-attributes-patch", {
        "method": "PATCH",
        "url": "/api/v1/issue-custom-attributes/{}".format(issue_custom_attribute_id),
        "body": {
            "name": "Duration 1"
        }
    }),
    ("issues-custom-attributes-create", {
        "method": "POST",
        "url": "/api/v1/issue-custom-attributes",
        "body": {
            "name": "Duration 2",
            "description": "Duration in minutes",
            "order": 8,
            "project": 1
        }
    }),
    ("issues-custom-attributes-simple-create", {
        "method": "POST",
        "url": "/api/v1/issue-custom-attributes",
        "body": {
            "name": "Duration 3",
            "project": 1
        }
    }),
    ("issues-custom-attributes-get", {
        "method": "GET",
        "url": "/api/v1/issue-custom-attributes/{}".format(issue_custom_attribute_id),
    }),
    ("issues-custom-attributes-bulk-update-order", {
        "method": "POST",
        "url": "/api/v1/issue-custom-attributes/bulk_update_order",
        "body": {
            "project": 1,
            "bulk_issue_custom_attributes": [[issue_custom_attribute_id, 10], [issue_custom_attribute_id2, 5]]
        }
    }),
    ("issues-custom-attributes-list", {
        "method": "GET",
        "url": "/api/v1/issue-custom-attributes",
    }),
    ("issues-custom-attributes-filtered-list", {
        "method": "GET",
        "url": "/api/v1/issue-custom-attributes?project=1",
    }),
    ("user-story-statuses-patch", {
        "method": "PATCH",
        "url": "/api/v1/userstory-statuses/1",
        "body": {
            "name": "Patch status name"
        }
    }),
    ("user-story-statuses-create", {
        "method": "POST",
        "url": "/api/v1/userstory-statuses",
        "body": {
            "color": "#AAAAAA",
            "is_closed": True,
            "name": "New status",
            "order": 8,
            "project": 1,
            "wip_limit": 6
        }
    }),
    ("user-story-statuses-simple-create", {
        "method": "POST",
        "url": "/api/v1/userstory-statuses",
        "body": {
            "project": 1,
            "name": "New status name"
        }
    }),
    ("user-story-statuses-get", {
        "method": "GET",
        "url": "/api/v1/userstory-statuses/1",
    }),
    ("user-story-statuses-bulk-update-order", {
        "method": "POST",
        "url": "/api/v1/userstory-statuses/bulk_update_order",
        "body": {
            "project": 1,
            "bulk_userstory_statuses": [[1, 10], [2, 5]]
        }
    }),
    ("user-story-statuses-list", {
        "method": "GET",
        "url": "/api/v1/userstory-statuses",
    }),
    ("user-story-statuses-filtered-list", {
        "method": "GET",
        "url": "/api/v1/userstory-statuses?project=1",
    }),
    ("tasks-attachments-create", {
        "method": "MULTIPART-POST",
        "url": "/api/v1/tasks/attachments",
        "body": {
            "object_id": task_id,
            "project": 1,
            "attached_file": test_file
        }
    }),
    ("tasks-unwatch", {
        "method": "POST",
        "url": "/api/v1/tasks/{}/unwatch".format(task_id),
    }),
    ("tasks-bulk-create", {
        "method": "POST",
        "url": "/api/v1/tasks/bulk_create",
        "body": {
            "project_id": 1,
            "milestone_id": milestone_id,
            "bulk_tasks": "Task 1 \n Task 2 \n Task 3"
        }
    }),
    ("tasks-patch", {
        "method": "PATCH",
        "url": "/api/v1/tasks/{}".format(task_id),
        "body": {
            "subject": "Patching subject",
            "version": 1
        }
    }),
    ("tasks-create", {
        "method": "POST",
        "url": "/api/v1/tasks",
        "body": {
            "assigned_to": None,
            "blocked_note": "blocking reason",
            "description": "Implement API CALL",
            "is_blocked": False,
            "is_closed": True,
            "milestone": None,
            "project": 1,
            "user_story": 17,
            "status": 1,
            "subject": "Customer personal data",
            "tags": [
                "service catalog",
                "customer"
            ],
            "us_order": 1,
            "taskboard_order": 1,
            "is_iocaine": False,
            "external_reference": None,
            "watchers": []
        }
    }),
    ("tasks-simple-create", {
        "method": "POST",
        "url": "/api/v1/tasks",
        "body": {
            "project": 1,
            "subject": "Customer personal data"
        }
    }),
    ("tasks-get", {
        "method": "GET",
        "url": "/api/v1/tasks/{}".format(task_id),
    }),
    ("tasks-filters-data", {
        "method": "GET",
        "url": "/api/v1/tasks/filters_data?project=1",
    }),
    ("tasks-watch", {
        "method": "POST",
        "url": "/api/v1/tasks/{}/watch".format(task_id),
    }),
    ("tasks-voters", {
        "method": "GET",
        "url": "/api/v1/tasks/{}/voters".format(task_id),
        "index": 0,
    }),
    ("tasks-attachments-list", {
        "method": "GET",
        "url": "/api/v1/tasks/attachments?object_id={}\&project=1".format(task_id),
    }),
    ("tasks-attachments-patch", {
        "method": "PATCH",
        "url": "/api/v1/tasks/attachments/{}".format(tasks_attachment),
        "body": {
            "description": "Updated description",
        }
    }),
    ("tasks-upvote", {
        "method": "POST",
        "url": "/api/v1/tasks/{}/upvote".format(task_id),
    }),
    ("tasks-list", {
        "method": "GET",
        "url": "/api/v1/tasks",
        "index": 0,
    }),
    ("tasks-filtered-list", {
        "method": "GET",
        "url": "/api/v1/tasks?project=1",
    }),
    ("tasks-downvote", {
        "method": "POST",
        "url": "/api/v1/tasks/{}/downvote".format(task_id),
    }),
    ("tasks-by-ref", {
        "method": "GET",
        "url": "/api/v1/tasks/by_ref?ref={}\&project=1".format(task_ref),
    }),
    ("tasks-watchers", {
        "method": "GET",
        "url": "/api/v1/tasks/{}/watchers".format(task_id),
        "index": 0,
    }),
    ("tasks-attachments-get", {
        "method": "GET",
        "url": "/api/v1/tasks/attachments/{}".format(tasks_attachment),
    }),
    ("application-tokens-validate", {
        "method": "POST",
        "url": "/api/v1/application-tokens/validate",
        "body": {
            "application": app.id,
            "auth_code": app_token.auth_code,
            "state": app_token.state
        }
    }),
    ("applications-get", {
        "method": "GET",
        "url": "/api/v1/applications/{}".format(app.id),
    }),
    ("applications-get-token", {
        "method": "GET",
        "url": "/api/v1/applications/{}/token".format(app.id),
    }),
    ("application-tokens-authorize", {
        "method": "POST",
        "url": "/api/v1/application-tokens/authorize",
        "body": {
            "application": app.id,
            "state": "random-state"
        }
    }),
    ("project-templates-patch", {
        "method": "PATCH",
        "admin_needed": True,
        "url": "/api/v1/project-templates/1",
        "body": {
            "description": "New description"
        }
    }),
    ("project-templates-create", {
        "method": "POST",
        "admin_needed": True,
        "url": "/api/v1/project-templates",
        "body": {
            "default_options": {
                "us_status": "New",
                "points": "?",
                "priority": "Normal",
                "severity": "Normal",
                "task_status": "New",
                "issue_type": "Bug",
                "issue_status": "New"
            },
            "us_statuses": [
                {
                    "wip_limit": None,
                    "color": "#999999",
                    "name": "New",
                    "order": 1,
                    "is_closed": False
                },
                {
                    "wip_limit": None,
                    "color": "#f57900",
                    "name": "Ready",
                    "order": 2,
                    "is_closed": False
                },
                {
                    "wip_limit": None,
                    "color": "#729fcf",
                    "name": "In progress",
                    "order": 3,
                    "is_closed": False
                },
                {
                    "wip_limit": None,
                    "color": "#4e9a06",
                    "name": "Ready for test",
                    "order": 4,
                    "is_closed": False
                },
                {
                    "wip_limit": None,
                    "color": "#cc0000",
                    "name": "Done",
                    "order": 5,
                    "is_closed": True
                }
            ],
            "points": [
                {
                    "value": None,
                    "name": "?",
                    "order": 1
                },
                {
                    "value": 0.0,
                    "name": "0",
                    "order": 2
                },
                {
                    "value": 0.5,
                    "name": "1/2",
                    "order": 3
                },
                {
                    "value": 1.0,
                    "name": "1",
                    "order": 4
                },
                {
                    "value": 2.0,
                    "name": "2",
                    "order": 5
                },
                {
                    "value": 3.0,
                    "name": "3",
                    "order": 6
                },
                {
                    "value": 5.0,
                    "name": "5",
                    "order": 7
                },
                {
                    "value": 8.0,
                    "name": "8",
                    "order": 8
                },
                {
                    "value": 10.0,
                    "name": "10",
                    "order": 9
                },
                {
                    "value": 15.0,
                    "name": "15",
                    "order": 10
                },
                {
                    "value": 20.0,
                    "name": "20",
                    "order": 11
                },
                {
                    "value": 40.0,
                    "name": "40",
                    "order": 12
                }
            ],
            "task_statuses": [
                {
                    "color": "#999999",
                    "name": "New",
                    "order": 1,
                    "is_closed": False
                },
                {
                    "color": "#729fcf",
                    "name": "In progress",
                    "order": 2,
                    "is_closed": False
                },
                {
                    "color": "#f57900",
                    "name": "Ready for test",
                    "order": 3,
                    "is_closed": True
                },
                {
                    "color": "#4e9a06",
                    "name": "Closed",
                    "order": 4,
                    "is_closed": True
                },
                {
                    "color": "#cc0000",
                    "name": "Needs Info",
                    "order": 5,
                    "is_closed": False
                }
            ],
            "issue_statuses": [
                {
                    "color": "#999999",
                    "name": "New",
                    "order": 1,
                    "is_closed": False
                },
                {
                    "color": "#729fcf",
                    "name": "In progress",
                    "order": 2,
                    "is_closed": False
                },
                {
                    "color": "#f57900",
                    "name": "Ready for test",
                    "order": 3,
                    "is_closed": True
                },
                {
                    "color": "#4e9a06",
                    "name": "Closed",
                    "order": 4,
                    "is_closed": True
                },
                {
                    "color": "#cc0000",
                    "name": "Needs Info",
                    "order": 5,
                    "is_closed": False
                },
                {
                    "color": "#d3d7cf",
                    "name": "Rejected",
                    "order": 6,
                    "is_closed": True
                },
                {
                    "color": "#75507b",
                    "name": "Postponed",
                    "order": 7,
                    "is_closed": False
                }
            ],
            "issue_types": [
                {
                    "color": "#cc0000",
                    "name": "Bug",
                    "order": 1
                },
                {
                    "color": "#729fcf",
                    "name": "Question",
                    "order": 2
                },
                {
                    "color": "#4e9a06",
                    "name": "Enhancement",
                    "order": 3
                }
            ],
            "priorities": [
                {
                    "color": "#999999",
                    "name": "Low",
                    "order": 1
                },
                {
                    "color": "#4e9a06",
                    "name": "Normal",
                    "order": 3
                },
                {
                    "color": "#CC0000",
                    "name": "High",
                    "order": 5
                }
            ],
            "severities": [
                {
                    "color": "#999999",
                    "name": "Wishlist",
                    "order": 1
                },
                {
                    "color": "#729fcf",
                    "name": "Minor",
                    "order": 2
                },
                {
                    "color": "#4e9a06",
                    "name": "Normal",
                    "order": 3
                },
                {
                    "color": "#f57900",
                    "name": "Important",
                    "order": 4
                },
                {
                    "color": "#CC0000",
                    "name": "Critical",
                    "order": 5
                }
            ],
            "roles": [
                {
                    "permissions": [
                        "add_issue", "modify_issue", "comment_issue", "delete_issue",
                        "view_issues", "add_milestone", "modify_milestone",
                        "delete_milestone", "view_milestones", "view_project",
                        "add_task", "modify_task", "comment_task", "delete_task", "view_tasks",
                        "add_us", "modify_us", "comment_us", "delete_us", "view_us",
                        "add_wiki_page", "modify_wiki_page", "comment_wiki_page", "delete_wiki_page",
                        "view_wiki_pages", "add_wiki_link", "delete_wiki_link",
                        "view_wiki_links"
                    ],
                    "order": 10,
                    "computable": True,
                    "slug": "ux",
                    "name": "UX"
                },
                {
                    "permissions": [
                        "add_issue", "modify_issue", "comment_issue", "delete_issue",
                        "view_issues", "add_milestone", "modify_milestone",
                        "delete_milestone", "view_milestones", "view_project",
                        "add_task", "modify_task", "comment_task", "delete_task", "view_tasks",
                        "add_us", "modify_us", "comment_us", "delete_us", "view_us",
                        "add_wiki_page", "modify_wiki_page", "comment_wiki_page", "delete_wiki_page",
                        "view_wiki_pages", "add_wiki_link", "delete_wiki_link",
                        "view_wiki_links"
                    ],
                    "order": 20,
                    "computable": True,
                    "slug": "design",
                    "name": "Design"
                },
                {
                    "permissions": [
                        "add_issue", "modify_issue", "comment_issue", "delete_issue",
                        "view_issues", "add_milestone", "modify_milestone",
                        "delete_milestone", "view_milestones", "view_project",
                        "add_task", "modify_task", "comment_task", "delete_task", "view_tasks",
                        "add_us", "modify_us", "comment_us", "delete_us", "view_us",
                        "add_wiki_page", "modify_wiki_page", "comment_wiki_page", "delete_wiki_page",
                        "view_wiki_pages", "add_wiki_link", "delete_wiki_link",
                        "view_wiki_links"
                    ],
                    "order": 30,
                    "computable": True,
                    "slug": "front",
                    "name": "Front"
                },
                {
                    "permissions": [
                        "add_issue", "modify_issue", "comment_issue", "delete_issue",
                        "view_issues", "add_milestone", "modify_milestone",
                        "delete_milestone", "view_milestones", "view_project",
                        "add_task", "modify_task", "comment_task", "delete_task", "view_tasks",
                        "add_us", "modify_us", "comment_us", "delete_us", "view_us",
                        "add_wiki_page", "modify_wiki_page", "comment_wiki_page", "delete_wiki_page",
                        "view_wiki_pages", "add_wiki_link", "delete_wiki_link",
                        "view_wiki_links"
                    ],
                    "order": 40,
                    "computable": True,
                    "slug": "back",
                    "name": "Back"
                },
                {
                    "permissions": [
                        "add_issue", "modify_issue", "comment_issue", "delete_issue",
                        "view_issues", "add_milestone", "modify_milestone",
                        "delete_milestone", "view_milestones", "view_project",
                        "add_task", "modify_task", "comment_task", "delete_task", "view_tasks",
                        "add_us", "modify_us", "comment_us", "delete_us", "view_us",
                        "add_wiki_page", "modify_wiki_page", "comment_wiki_page", "delete_wiki_page",
                        "view_wiki_pages", "add_wiki_link", "delete_wiki_link",
                        "view_wiki_links"
                    ],
                    "order": 50,
                    "computable": False,
                    "slug": "product-owner",
                    "name": "Product Owner"
                },
                {
                    "permissions": [
                        "add_issue", "modify_issue", "comment_issue", "delete_issue",
                        "view_issues", "view_milestones", "view_project",
                        "view_tasks", "view_us", "modify_wiki_page", "comment_wiki_page",
                        "view_wiki_pages", "add_wiki_link", "delete_wiki_link",
                        "view_wiki_links"
                    ],
                    "order": 60,
                    "computable": False,
                    "slug": "stakeholder",
                    "name": "Stakeholder"
                }
            ],
            "id": 2,
            "name": "New Template",
            "slug": "new-template",
            "description": "Sample description",
            "default_owner_role": "product-owner",
            "is_backlog_activated": False,
            "is_kanban_activated": True,
            "is_wiki_activated": False,
            "is_issues_activated": False,
            "videoconferences": None,
            "videoconferences_extra_data": ""
        }
    }),
    ("project-templates-simple-create", {
        "method": "POST",
        "admin_needed": True,
        "url": "/api/v1/project-templates",
        "body": {
            "name": "New simple template",
            "description": "Sample description",
            "default_owner_role": "product-owner"
        }
    }),
    ("project-templates-get", {
        "method": "GET",
        "url": "/api/v1/project-templates/1",
    }),
    ("project-templates-list", {
        "method": "GET",
        "url": "/api/v1/project-templates",
    }),
    ("search", {
        "method": "GET",
        "url": "/api/v1/search?project=1\&text=quas",
    }),
    ("points-patch", {
        "method": "PATCH",
        "url": "/api/v1/points/1",
        "body": {
            "name": "Patch name"
        }
    }),
    ("points-create", {
        "method": "POST",
        "url": "/api/v1/points",
        "body": {
            "color": "#AAAAAA",
            "name": "Huge",
            "order": 8,
            "value": 40,
            "project": 1
        }
    }),
    ("points-simple-create", {
        "method": "POST",
        "url": "/api/v1/points",
        "body": {
            "project": 1,
            "name": "Very huge"
        }
    }),
    ("points-get", {
        "method": "GET",
        "url": "/api/v1/points/1",
    }),
    ("points-bulk-update-order", {
        "method": "POST",
        "url": "/api/v1/points/bulk_update_order",
        "body": {
            "project": 1,
            "bulk_points": [[1, 10], [2, 5]]
        }
    }),
    ("points-list", {
        "method": "GET",
        "url": "/api/v1/points",
    }),
    ("points-filtered-list", {
        "method": "GET",
        "url": "/api/v1/points?project=1",
    }),
    ("application-tokens-get", {
        "method": "GET",
        "url": "/api/v1/application-tokens/{}".format(app_token.id),
    }),
    ("application-tokens-list", {
        "method": "GET",
        "url": "/api/v1/application-tokens",
    }),
    ("application-tokens-authorize", {
        "method": "POST",
        "url": "/api/v1/application-tokens/authorize",
        "body": {
            "application": "00000000-0000-0000-0000-000000000000",
            "state": "random-state"
        }
    }),
    ("tasks-custom-attributes-patch", {
        "method": "PATCH",
        "url": "/api/v1/task-custom-attributes/{}".format(task_custom_attribute_id),
        "body": {
          "name": "Duration 1"
        }
    }),
    ("tasks-custom-attributes-create", {
        "method": "POST",
        "url": "/api/v1/task-custom-attributes",
        "body": {
            "name": "Duration 2",
            "description": "Duration in minutes",
            "order": 8,
            "project": 1
        }
    }),
    ("tasks-custom-attributes-simple-create", {
        "method": "POST",
        "url": "/api/v1/task-custom-attributes",
        "body": {
            "name": "Duration 3",
            "project": 1
        }
    }),
    ("tasks-custom-attributes-get", {
        "method": "GET",
        "url": "/api/v1/task-custom-attributes/{}".format(task_custom_attribute_id),
    }),
    ("tasks-custom-attributes-bulk-update-order", {
        "method": "POST",
        "url": "/api/v1/task-custom-attributes/bulk_update_order",
        "body": {
            "project": 1,
            "bulk_task_custom_attributes": [[task_custom_attribute_id, 10], [task_custom_attribute_id2, 15]]
        }
    }),
    ("tasks-custom-attributes-list", {
        "method": "GET",
        "url": "/api/v1/task-custom-attributes",
    }),
    ("tasks-custom-attributes-filtered-list", {
        "method": "GET",
        "url": "/api/v1/task-custom-attributes?project=1",
    }),
    ("locales", {
        "method": "GET",
        "url": "/api/v1/locales",
    }),
    ("milestones-unwatch", {
        "method": "POST",
        "url": "/api/v1/milestones/1/unwatch",
    }),
    ("milestones-stats", {
        "method": "GET",
        "url": "/api/v1/milestones/1/stats",
    }),
    ("milestones-patch", {
        "method": "PATCH",
        "url": "/api/v1/milestones/1",
        "body": {
            "name": "Sprint 2"
        }
    }),
    ("milestones-create", {
        "method": "POST",
        "url": "/api/v1/milestones",
        "body": {
            "project": 1,
            "name": "Sprint 1",
            "estimated_start": "2014-10-20",
            "estimated_finish": "2014-11-04",
            "disponibility": 30,
            "slug": "sprint-1",
            "order": 1,
            "watchers": []
        }
    }),
    ("milestones-simple-create", {
        "method": "POST",
        "url": "/api/v1/milestones",
        "body": {
          "project": 1,
          "name": "Sprint 3",
          "estimated_start": "2014-10-20",
          "estimated_finish": "2014-11-04"
        }
    }),
    ("milestones-get", {
        "method": "GET",
        "url": "/api/v1/milestones/1",
    }),
    ("milestones-watch", {
        "method": "POST",
        "url": "/api/v1/milestones/1/watch",
    }),
    ("milestones-list", {
        "method": "GET",
        "url": "/api/v1/milestones",
    }),
    ("milestones-filtered-list", {
        "method": "GET",
        "url": "/api/v1/milestones?project=1",
    }),
    ("milestones-watchers", {
        "method": "GET",
        "url": "/api/v1/milestones/1/watchers",
        "index": 0,
    }),
    ("users-stats", {
        "method": "GET",
        "url": "/api/v1/users/{}/stats".format(USER_ID),
    }),
    ("users-voted", {
        "method": "GET",
        "url": "/api/v1/users/{}/voted".format(USER_ID),
        "index": 0,
    }),
    ("users-liked", {
        "method": "GET",
        "url": "/api/v1/users/{}/liked?type=userstory\&q=test".format(USER_ID),
        "index": 0,
    }),
    ("users-remove-avatar", {
        "method": "POST",
        "url": "/api/v1/users/remove_avatar",
    }),
    ("users-patch", {
        "method": "PATCH",
        "url": "/api/v1/users/{}".format(USER_ID),
        "body": {
            "username": "patchedusername"
        }
    }),
    ("users-get", {
        "method": "GET",
        "url": "/api/v1/users/{}".format(USER_ID),
    }),
    ("users-liked", {
        "method": "GET",
        "url": "/api/v1/users/{}/liked".format(USER_ID),
    }),
    ("users-filtered-liked", {
        "method": "GET",
        "url": "/api/v1/users/{}/liked?q=test".format(USER_ID),
    }),
    ("users-contacts", {
        "method": "GET",
        "url": "/api/v1/users/{}/contacts".format(USER_ID),
        "index": 1,
    }),
    ("users-change-password", {
        "method": "POST",
        "url": "/api/v1/users/change_password",
        "body": {
            "current_password": "123123",
            "password": "new-password"
        }
    }),
    ("users-change-password-from-recovery", {
        "method": "POST",
        "url": "/api/v1/users/change_password_from_recovery",
        "body": {
          "token": "password-token",
          "password": "new-password"
        }
    }),
    ("users-change-avatar", {
        "method": "MULTIPART-POST",
        "url": "/api/v1/users/change_avatar",
        "body": {"avatar": test_file}
    }),
    ("users-list", {
        "method": "GET",
        "url": "/api/v1/users",
    }),
    ("users-filtered-list", {
        "method": "GET",
        "url": "/api/v1/users?project=1",
    }),
    ("users-change-email", {
        "method": "POST",
        "url": "/api/v1/users/change_email",
        "body": {
            "email_token": "email-token"
        }
    }),
    ("users-watched", {
        "method": "GET",
        "url": "/api/v1/users/1/watched",
        "index": 0,
    }),
    ("users-filtered-watched", {
        "method": "GET",
        "url": "/api/v1/users/1/watched?type=project\&q=test",
    }),
    ("users-password-recovery", {
        "method": "POST",
        "url": "/api/v1/users/password_recovery",
        "body": {
            "username": "user1"
        }
    }),
    ("users-me", {
        "method": "GET",
        "url": "/api/v1/users/me",
    }),
    ("user-stories-custom-attributes-values-patch", {
        "method": "PATCH",
        "url": "/api/v1/userstories/custom-attributes-values/{}".format(user_story_id),
        "body": {
            "attributes_values": {"{}".format(user_story_custom_attribute_id): "240 min"},
            "version": 1
        }
    }),
    ("user-stories-custom-attributes-values-get", {
        "method": "GET",
        "url": "/api/v1/userstories/custom-attributes-values/{}".format(user_story_id),
    }),
    ("resolver-milestone", {
        "method": "GET",
        "url": "/api/v1/resolver?project=project-0\&milestone={}".format(milestone_slug),
    }),
    ("resolver-user-story", {
        "method": "GET",
        "url": "/api/v1/resolver?project=project-0\&us={}".format(user_story_ref),
    }),
    ("resolver-wiki-page", {
        "method": "GET",
        "url": "/api/v1/resolver?project=project-0\&wikipage=home",
    }),
    ("resolver-issue", {
        "method": "GET",
        "url": "/api/v1/resolver?project=project-0\&issue={}".format(issue_ref),
    }),
    ("resolver-project", {
        "method": "GET",
        "url": "/api/v1/resolver?project=project-0",
    }),
    ("resolver-task", {
        "method": "GET",
        "url": "/api/v1/resolver?project=project-0\&task={}".format(task_ref),
    }),
    ("resolver-ref", {
        "method": "GET",
        "url": "/api/v1/resolver?project=project-0\&ref={}".format(task_ref),
    }),
    ("resolver-multiple", {
        "method": "GET",
        "url": "/api/v1/resolver?project=project-0\&task={}\&us={}\&wikipage=home".format(task_ref, user_story_ref),
    }),
    ("memberships-patch", {
        "method": "PATCH",
        "url": "/api/v1/memberships/1",
        "body": {
            "role": 3
        }
    }),
    ("issues-delete", {
        "method": "DELETE",
        "url": "/api/v1/issues/{}".format(issue_id),
    }),
    ("user-stories-attachment-delete", {
        "method": "DELETE",
        "url": "/api/v1/userstories/attachments/{}".format(user_stories_attachment),
    }),
    ("user-stories-custom-attributes-delete", {
        "method": "DELETE",
        "url": "/api/v1/userstory-custom-attributes/1",
    }),
    ("wiki-attachments-delete", {
        "method": "DELETE",
        "url": "/api/v1/wiki/attachments/{}".format(wiki_attachment),
    }),
    ("wiki-delete", {
        "method": "DELETE",
        "url": "/api/v1/wiki/{}".format(wiki_id),
    }),
    ("wiki-links-delete", {
        "method": "DELETE",
        "url": "/api/v1/wiki-links/{}".format(wiki_link_id),
    }),
    ("issues-custom-attributes-delete", {
        "method": "DELETE",
        "url": "/api/v1/issue-custom-attributes/{}".format(issue_custom_attribute_id),
    }),
    ("tasks-attachments-delete", {
        "method": "DELETE",
        "url": "/api/v1/tasks/attachments/{}".format(tasks_attachment),
    }),
    ("tasks-delete", {
        "method": "DELETE",
        "url": "/api/v1/tasks/{}".format(task_id),
    }),
    ("user-stories-delete", {
        "method": "DELETE",
        "url": "/api/v1/userstories/{}".format(user_story_id),
    }),
    ("project-templates-delete", {
        "method": "DELETE",
        "admin_needed": True,
        "url": "/api/v1/project-templates/1",
    }),
    ("points-delete", {
        "method": "DELETE",
        "url": "/api/v1/points/1",
    }),
    ("application-tokens-delete", {
        "method": "DELETE",
        "url": "/api/v1/application-tokens/{}".format(app_token2.id),
    }),
    ("tasks-custom-attributes-delete", {
        "method": "DELETE",
        "url": "/api/v1/task-custom-attributes/{}".format(task_custom_attribute_id),
    }),
    ("milestones-delete", {
        "method": "DELETE",
        "url": "/api/v1/milestones/1",
    }),
    ("users-delete", {
        "method": "DELETE",
        "admin_needed": True,
        "url": "/api/v1/users/10",
    }),
    ("user-story-statuses-delete", {
        "method": "DELETE",
        "url": "/api/v1/userstory-statuses/1",
    }),
    ("memberships-delete", {
        "method": "DELETE",
        "url": "/api/v1/memberships/2",
    }),
    ("issue-statuses-delete", {
        "method": "DELETE",
        "url": "/api/v1/issue-statuses/1",
    }),
    ("severities-delete", {
        "method": "DELETE",
        "url": "/api/v1/severities/1",
    }),
    ("task-statuses-delete", {
        "method": "DELETE",
        "url": "/api/v1/task-statuses/1",
    }),
    ("issues-attachment-delete", {
        "method": "DELETE",
        "url": "/api/v1/issues/attachments/{}".format(issues_attachment),
    }),
    ("priorities-delete", {
        "method": "DELETE",
        "url": "/api/v1/priorities/1",
    }),
    ("webhooks-delete", {
        "method": "DELETE",
        "url": "/api/v1/webhooks/1",
    }),
    ("user-storage-delete", {
        "method": "DELETE",
        "url": "/api/v1/user-storage/favorite-forest",
    }),
    ("issue-types-delete", {
        "method": "DELETE",
        "url": "/api/v1/issue-types/1",
    }),
    ("projects-leave", {
        "method": "POST",
        "url": "/api/v1/projects/2/leave",
    }),
    ("projects-delete", {
        "method": "DELETE",
        "url": "/api/v1/projects/1",
    }),
    ("users-cancel", {
        "method": "POST",
        "url": "/api/v1/users/cancel",
        "body": {
          "cancel_token": get_token_for_user(user, "cancel_account")
        }
    }),
    ("importers-trello-auth-url", {
        "method": "GET",
        "url": "/api/v1/importers/trello/auth_url",
    }),
    ("importers-trello-authorize", {
        "method": "POST",
        "url": "/api/v1/importers/trello/authorize",
        "body": {
          "code": "00000000000000000000000000000000"
        },
        "response": {
          "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        },
    }),
    ("importers-trello-list-users", {
        "method": "POST",
        "url": "/api/v1/importers/trello/list_users",
        "body": {
          "project": "123ABC",
          "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        },
        "response": [
            {
                "id": "trello-user",
                "full_name": "Trello user",
                "email": None,
                "user": None,
            },
            {
                "id": "other-trello-user",
                "full_name": "Other Trello user",
                "email": "other-trello-user@email.com",
                "user": {
                    "id": 12345,
                    "full_name": "Taiga user",
                    "gravatar_id": "64e1b8d34f425d19e1ee2ea7236d3028",
                    "photo": "/user-photo-url"
                }
            },
        ],
    }),
    ("importers-trello-list-projects", {
        "method": "POST",
        "url": "/api/v1/importers/trello/list_projects",
        "body": {
          "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        },
        "response": [
          {
              "id": "123ABC",
              "name": "Trello project",
              "description": "My trello project",
              "is_private": False,
          },
          {
              "id": "ABC123",
              "name": "Other trello project",
              "description": "My other trello project",
              "is_private": True,
          }
        ],
    }),
    ("importers-trello-import-project", {
        "method": "POST",
        "url": "/api/v1/importers/trello/import",
        "body": {
          "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
          "project": "123ABC",
          "name": "New project name",
          "description": "New project description",
          "template": "kanban",
          "users_bindings": {
              "user-1": "123",
              "user-2": "321",
          },
          "keep_external_reference": False,
          "is_private": False,
        },
        "response": {
          "slug": "my-username-new-project-name",
          "my_permissions": ["view_us"],
          "is_backlog_activated": False,
          "is_kanban_activated": True,
        }
    }),
    ("importers-github-auth-url", {
        "method": "GET",
        "url": "/api/v1/importers/github/auth_url",
    }),
    ("importers-github-authorize", {
        "method": "POST",
        "url": "/api/v1/importers/github/authorize",
        "body": {
          "code": "00000000000000000000"
        },
        "response": {
          "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        },
    }),
    ("importers-github-list-users", {
        "method": "POST",
        "url": "/api/v1/importers/github/list_users",
        "body": {
          "project": "user/project",
          "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        },
        "response": [
            {
                "id": 12345,
                "username": "github-user",
                "full_name": "Github user",
                "user": None,
            },
            {
                "id": 12345,
                "username": "other-github-user",
                "full_name": "Other Github user",
                "user": {
                    "id": 54321,
                    "full_name": "Taiga user",
                    "gravatar_id": "64e1b8d34f425d19e1ee2ea7236d3028",
                    "photo": "/user-photo-url"
                }
            },
        ],
    }),
    ("importers-github-list-projects", {
        "method": "POST",
        "url": "/api/v1/importers/github/list_projects",
        "body": {
          "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        },
        "response": [
          {
              "id": "user/project",
              "name": "Github project",
              "description": "My github project",
              "is_private": False,
          },
          {
              "id": "user/other-project",
              "name": "Other github project",
              "description": "My other github project",
              "is_private": True,
          }
        ],
    }),
    ("importers-github-import-project", {
        "method": "POST",
        "url": "/api/v1/importers/github/import",
        "body": {
          "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
          "project": "user/project",
          "name": "New project name",
          "description": "New project description",
          "template": "kanban",
          "users_bindings": {
              "user-1": "123",
              "user-2": "321",
          },
          "keep_external_reference": False,
          "is_private": False,
        },
        "response": {
          "slug": "my-username-new-project-name",
          "my_permissions": ["view_us"],
          "is_backlog_activated": False,
          "is_kanban_activated": True,
        }
    }),
    ("importers-jira-auth-url", {
        "method": "GET",
        "url": "/api/v1/importers/jira/auth_url?url=http://your.jira.server",
        "response": {
            "url": "http://your.jira.server/plugins/servlet/oauth/authorize?oauth_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        },
    }),
    ("importers-jira-authorize", {
        "method": "POST",
        "url": "/api/v1/importers/jira/authorize",
        "body": {},
        "response": {
          "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
          "url": "http://your.jira.server",
        },
    }),
    ("importers-jira-list-users", {
        "method": "POST",
        "url": "/api/v1/importers/jira/list_users",
        "body": {
          "project": "12345",
          "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
          "url": "http://your.jira.server",
        },
        "response": [
            {
                "id": "jira-user",
                "full_name": "Jira user",
                "email": None,
                "user": None,
            },
            {
                "id": "other-jira-user",
                "full_name": "Other Jira user",
                "email": "other-jira-user@email.com",
                "user": {
                    "id": 12345,
                    "full_name": "Taiga user",
                    "gravatar_id": "64e1b8d34f425d19e1ee2ea7236d3028",
                    "photo": "/user-photo-url"
                }
            },
        ],
    }),
    ("importers-jira-list-projects", {
        "method": "POST",
        "url": "/api/v1/importers/jira/list_projects",
        "body": {
          "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
          "url": "http://your.jira.server",
        },
        "response": [
          {
              "id": "123",
              "name": "Jira project",
              "type": "project",
              "description": "My jira project",
              "is_private": False,
          },
          {
              "id": "456",
              "name": "Other jira project",
              "type": "board",
              "description": "My other jira project",
              "is_private": True,
          }
        ],
    }),
    ("importers-jira-import-project", {
        "method": "POST",
        "url": "/api/v1/importers/jira/import",
        "body": {
          "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
          "url": "http://your.jira.server",
          "project": "123",
          "name": "New project name",
          "description": "New project description",
          "project_type": "kanban",
          "users_bindings": {
              "user-1": "123",
              "user-2": "321",
          },
          "keep_external_reference": False,
          "is_private": False,
        },
        "response": {
          "slug": "my-username-new-project-name",
          "my_permissions": ["view_us"],
          "is_backlog_activated": False,
          "is_kanban_activated": True,
        }
    }),
    ("importers-asana-auth-url", {
        "method": "GET",
        "url": "/api/v1/importers/asana/auth_url",
    }),
    ("importers-asana-authorize", {
        "method": "POST",
        "url": "/api/v1/importers/asana/authorize",
        "body": {},
        "response": {
          "token": {
            "access_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "token_type": "bearer",
            "expires_in": 3600,
            "data": {
              "id": 123,
              "name": "User",
              "email": "user-email@email.com"
            },
            "refresh_token": "0/000000000000000000000000000000000"
          }
        },
    }),
    ("importers-asana-list-users", {
        "method": "POST",
        "url": "/api/v1/importers/asana/list_users",
        "body": {
          "project": 12345,
          "token": {
            "access_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "token_type": "bearer",
            "expires_in": 3600,
            "data": {
              "id": 123,
              "name": "User",
              "email": "user-email@email.com"
            },
            "refresh_token": "0/000000000000000000000000000000000"
          },
        },
        "response": [
            {
                "id": 123,
                "full_name": "Asana user",
                "user": None,
            },
            {
                "id": 456,
                "full_name": "Other Asana user",
                "user": {
                    "id": 12345,
                    "full_name": "Taiga user",
                    "gravatar_id": "64e1b8d34f425d19e1ee2ea7236d3028",
                    "photo": "/user-photo-url"
                }
            },
        ],
    }),
    ("importers-asana-list-projects", {
        "method": "POST",
        "url": "/api/v1/importers/asana/list_projects",
        "body": {
          "token": {
            "access_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "token_type": "bearer",
            "expires_in": 3600,
            "data": {
              "id": 123,
              "name": "User",
              "email": "user-email@email.com"
            },
            "refresh_token": "0/000000000000000000000000000000000"
          },
        },
        "response": [
          {
              "id": "123",
              "name": "Asana project",
              "description": "My asana project",
              "is_private": False,
          },
          {
              "id": "456",
              "name": "Other asana project",
              "description": "My other asana project",
              "is_private": True,
          }
        ],
    }),
    ("importers-asana-import-project", {
        "method": "POST",
        "url": "/api/v1/importers/asana/import",
        "body": {
          "token": {
            "access_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "token_type": "bearer",
            "expires_in": 3600,
            "data": {
              "id": 123,
              "name": "User",
              "email": "user-email@email.com"
            },
            "refresh_token": "0/000000000000000000000000000000000"
          },
          "project": 123,
          "name": "New project name",
          "description": "New project description",
          "template": "kanban",
          "users_bindings": {
              "user-1": "123",
              "user-2": "321",
          },
          "keep_external_reference": False,
          "is_private": False,
        },
        "response": {
          "slug": "my-username-new-project-name",
          "my_permissions": ["view_us"],
          "is_backlog_activated": False,
          "is_kanban_activated": True,
        }
    }),
])
