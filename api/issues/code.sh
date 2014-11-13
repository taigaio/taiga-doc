curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
          "type": "normal",
          "username": "admin",
          "password": "123123"
      }' \
  http://localhost:8000/api/v1/auth

echo ""
echo -n "INSERT AUTH TOKEN: "
read AUTH_TOKEN

echo "1. -------------------------------"
curl -s -o /dev/null -w "%{http_code}" -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  -d '{
          "project_id": 3,
          "bulk_issues": "Issue 1 \n Issue 2 \n Issue 3"
      }' \
  http://localhost:8000/api/v1/issues/bulk_create
echo ""
echo "2. -------------------------------"
curl -s -o /dev/null -w "%{http_code}" -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  -d '{
          "assigned_to": null,
          "blocked_note": "blocking reason",
          "description": "Implement API CALL",
          "is_blocked": false,
          "is_closed": true,
          "milestone": null,
          "project": 3,
          "status": 13,
          "severity": 2,
          "priority": 3,
          "type": 1,
          "subject": "Customer personal data",
          "tags": [
              "service catalog",
              "customer"
          ],
          "watchers": []
      }' \
  http://localhost:8000/api/v1/issues
echo ""
echo "3. -------------------------------"
curl -s -o /dev/null -w "%{http_code}" -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  -d '{
          "project": 3,
          "subject": "Customer personal data"
      }' \
  http://localhost:8000/api/v1/issues
echo ""
echo "4. -------------------------------"
curl -s -o /dev/null -w "%{http_code}" -X POST \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  -F "object_id=81" \
  -F "project=3" \
  -F "attached_file=@/tmp/test.png" \
  http://localhost:8000/api/v1/issues/attachments
echo ""
echo "5. -------------------------------"
curl -s -o /dev/null -w "%{http_code}" -X DELETE \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  http://localhost:8000/api/v1/issues/1
echo ""
echo "6. -------------------------------"
curl -s -o /dev/null -w "%{http_code}" -X DELETE \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  http://localhost:8000/api/v1/issues/attachments/415
echo ""
echo "7. -------------------------------"
curl -s -o /dev/null -w "%{http_code}" -X POST \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  http://localhost:8000/api/v1/issues/1/downvote
echo ""
echo "8. -------------------------------"
curl -s -o /dev/null -w "%{http_code}" -X PATCH \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  -F "description=patching description" \
  http://localhost:8000/api/v1/issues/attachments/417
echo ""
echo "9. -------------------------------"
curl -s -o /dev/null -w "%{http_code}" -X PATCH \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  -d '{
          "subject": "Patching subject"
      }' \
  http://localhost:8000/api/v1/issues/1
echo ""
echo "10. -------------------------------"
curl -s -o /dev/null -w "%{http_code}" -X GET \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  http://localhost:8000/api/v1/issues/1
echo ""
echo "11. -------------------------------"
curl -s -o /dev/null -w "%{http_code}" -X GET \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  http://localhost:8000/api/v1/issues/attachments/415
echo ""
echo "12. -------------------------------"
curl -s -o /dev/null -w "%{http_code}" -X GET \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  http://localhost:8000/api/v1/issues
echo ""
echo "13. -------------------------------"
curl -s -o /dev/null -w "%{http_code}" -X GET \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  http://localhost:8000/api/v1/issues?project=1
echo ""
echo "14. -------------------------------"
curl -s -o /dev/null -w "%{http_code}" -X GET \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  http://localhost:8000/api/v1/issues?project=1&order_by=priority
echo ""
echo "15. -------------------------------"
curl -s -o /dev/null -w "%{http_code}" -X GET \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  http://localhost:8000/api/v1/issues/attachments?object_id=81&project=3
echo ""
echo "16. -------------------------------"
curl -s -o /dev/null -w "%{http_code}" -X POST \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  http://localhost:8000/api/v1/issues/1/upvote
