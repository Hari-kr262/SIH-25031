# CivicResolve API Documentation

Base URL: `http://localhost:8000/api/v1`
Interactive Docs: `http://localhost:8000/docs`

## Authentication

All protected endpoints require `Authorization: Bearer <token>` header.

### Endpoints

#### POST /auth/register
Register a new user.
```json
{
  "full_name": "string",
  "email": "string",
  "password": "string",
  "phone": "string (optional)",
  "role": "citizen|volunteer|field_worker"
}
```

#### POST /auth/login
```json
{ "email": "string", "password": "string" }
```
Returns: `{ access_token, refresh_token, user_id, role, full_name }`

#### POST /auth/refresh
```json
{ "refresh_token": "string" }
```

#### GET /auth/me
Returns current user profile.

---

## Issues

#### POST /issues/
Create a new issue report.

#### GET /issues/
List issues with filters: `?status=pending&category=pothole&page=1&page_size=20`

#### GET /issues/my
Current user's issues.

#### GET /issues/trending
Top upvoted issues.

#### GET /issues/nearby
`?lat=23.3&lng=85.3&radius_km=2.0`

#### GET /issues/{id}
Get specific issue.

#### PUT /issues/{id}
Update issue (author or admin).

#### DELETE /issues/{id}
Delete issue (admin only).

#### POST /issues/{id}/assign
```json
{ "assigned_to": 5, "department_id": 2 }
```

#### POST /issues/{id}/status
```json
{ "status": "in_progress", "comment": "optional note" }
```

#### GET /issues/{id}/timeline
Get audit trail for issue.

---

## Votes

#### POST /votes/upvote/{issue_id}
#### POST /votes/downvote/{issue_id}
#### DELETE /votes/remove/{issue_id}
#### GET /votes/count/{issue_id}

---

## Resolutions

#### POST /resolutions/
Submit fix proof (field workers only).

#### GET /resolutions/{issue_id}
Get resolution for an issue.

#### POST /resolutions/{issue_id}/verify
```json
{ "citizen_verified": true, "citizen_rating": 5, "citizen_feedback": "string" }
```

---

## Comments

#### POST /comments/
#### GET /comments/issue/{issue_id}
#### PUT /comments/{id}
#### DELETE /comments/{id}

---

## Notifications

#### GET /notifications/
#### POST /notifications/{id}/read
#### POST /notifications/read-all
#### GET /notifications/unread-count

---

## Dashboard

#### GET /dashboard/public — No auth required
#### GET /dashboard/admin — Admin+
#### GET /dashboard/department — Department head+

---

## Analytics

#### GET /analytics/trends?days=30
#### GET /analytics/heatmap
#### GET /analytics/performance — Admin+
#### GET /analytics/sla — Admin+
#### GET /analytics/export/pdf — Admin+
#### GET /analytics/export/excel — Admin+

---

## Gamification

#### GET /gamification/stats — Current user stats
#### GET /gamification/leaderboard
#### GET /gamification/badges — All badges
#### GET /gamification/badges/mine — User's earned badges

---

## Admin

#### GET /admin/users
#### PUT /admin/users/{id}/toggle-active
#### GET /admin/departments
#### POST /admin/departments
#### POST /admin/announcements
#### GET /admin/announcements
#### GET /admin/audit-logs

---

## Budgets

#### GET /budgets/
#### POST /budgets/allocate
#### POST /budgets/expense

---

## Map

#### GET /map/issues
#### GET /map/heatmap
#### GET /map/clusters

---

## Chatbot

#### POST /chatbot/chat
```json
{ "message": "How do I report a pothole?", "context": "general" }
```

---

## Response Format

All responses follow:
```json
{
  "success": true,
  "message": "Success",
  "data": { ... }
}
```

Error responses:
```json
{
  "success": false,
  "message": "Error description",
  "details": null
}
```
