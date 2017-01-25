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

from jinja2 import Template
import json
import subprocess
import os
import signal
import sys

from django.core.management.base import BaseCommand
from django.db import connection

from taiga.users.models import User
from taiga.auth.tokens import get_token_for_user

from ._requests_data import USER_ID, reqs as _reqs


class Command(BaseCommand):
    help = 'Generate json files for documentation'

    def add_arguments(self, parser):
        parser.add_argument('requests', nargs='*')

    def _build_curl_cmd(self, host, req):
        data = {
            "method": req['method'],
            "url": req['url'],
            "host": host,
            "body": req.get('body', None),
            "fields": None,
            "admin_needed": req.get('admin_needed', False)
        }

        if data['method'] == "MULTIPART-POST":
            data['method'] = "POST"
            data['fields'] = data['body']
            data['body'] = None

        if data['body'] is not None:
            data['body'] = json.dumps(data['body'], sort_keys=True, indent=4)
            data['body'] = "\n".join(["    "+line for line in data['body'].split("\n")])[4:]

        template = Template("""curl -X {{method}} \\
{% if fields %}-H "Content-Type: multipart/form-data"{% else %}-H "Content-Type: application/json"{% endif %} \\
{% if admin_needed %}-H "Authorization: Bearer ${ADMIN_AUTH_TOKEN}"{% else %}-H "Authorization: Bearer ${AUTH_TOKEN}"{% endif %} \\
{% if fields %}{% for (key,value) in sorted(fields.items()) %}-F {{key}}={{value}} \\
{% endfor %}{% endif %}{% if body %}-d '{{body}}' \\
{% endif %}-s {{host}}{{url}}
""")
        return template.render(**data, sorted=sorted)

    def _execute_requests(self, reqs):
        admin = User.objects.get(username="admin")
        user = User.objects.get(id=USER_ID)
        user.token = "password-token"
        user.email_token = "email-token"
        user.new_email = "test@sample-email.com"
        user.save()

        user_token = get_token_for_user(user, "authentication")
        admin_token = get_token_for_user(admin, "authentication")
        os.environ["AUTH_TOKEN"] = user_token
        os.environ["ADMIN_AUTH_TOKEN"] = admin_token

        host = "http://localhost:8000"

        for (key, req) in reqs.items():
            print("Generate", key)

            cmd_path = os.path.join("output", key + "-cmd.adoc")
            os.makedirs("output", exist_ok=True)
            curl_cmd = self._build_curl_cmd(host, req)
            with open(cmd_path, "w") as fd:
                fd.write("[source,bash]\n")
                fd.write("----\n")
                fd.write(curl_cmd.replace("$$INCLUDE_FILE$$", "@"))
                fd.write("\n----\n")

            if req['method'] == "DELETE":
                continue

            curl_cmd = curl_cmd.replace("$$INCLUDE_FILE$$", "@{}/".format(os.path.dirname(__file__)))

            output_path = os.path.join("output", key + "-output.adoc")
            if "response" in req:
                response_data = req['response']
            else:
                result = subprocess.run(curl_cmd + " -f", shell=True, stdout=subprocess.PIPE)

                if result.returncode != 0:
                    result = subprocess.run(curl_cmd, shell=True, stdout=subprocess.PIPE)
                    print("ERROR on key: ", key)
                    print(result)

                if result.stdout == b'':
                    response_data = None
                else:
                    response_data = json.loads(result.stdout.decode('utf-8'))
                    if req.get('index', None) is not None:
                        response_data = response_data[req['index']]

            if not response_data:
                continue

            with open(output_path, "w") as fd:
                fd.write("[source,json]\n")
                fd.write("----\n")
                json.dump(response_data, fd, sort_keys=True, indent=4)
                fd.write("\n----\n")

    def run_webhook_server(self):
        import http.server
        import socketserver

        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_POST(self):
                return "Ok"

        httpd = socketserver.TCPServer(("", 3000), Handler)
        httpd.serve_forever()

    def handle(self, *args, **options):
        reqs = {}
        if options.get('requests'):
            for request in options.get('requests'):
                reqs[request] = _reqs[request]
        else:
            reqs = _reqs
        connection.close()
        child_pid = os.fork()
        if child_pid == 0:
            self.run_webhook_server()
        else:
            try:
                self._execute_requests(reqs)
            except Exception as e:
                os.kill(child_pid, signal.SIGTERM)
                raise e
        os.kill(child_pid, signal.SIGTERM)
