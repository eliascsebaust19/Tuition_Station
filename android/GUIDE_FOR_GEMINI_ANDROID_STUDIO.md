# TuitionStation Android App — Complete Guide for Android Studio Gemini Assistant

This document provides everything Gemini in Android Studio needs to know to continue building the TuitionStation Android app. The app is a **location-based offline tuition marketplace** connecting students with home tutors in Bangladesh.

---

## 1. PROJECT OVERVIEW

| Item | Value |
|------|-------|
| **App Name** | TuitionStation |
| **Package** | `com.tuitionstation.app` |
| **Min SDK** | 26 (Android 8.0) |
| **Target SDK** | 34 (Android 14) |
| **Language** | Kotlin |
| **Architecture** | Activities + Fragments + Retrofit + Coroutines (MVVM-lite) |
| **Build** | Gradle 8.5, AGP 8.2.2, Kotlin 1.9.22 |
| **Backend** | Flask REST API at `http://192.168.137.1:5000/api/` (local dev) |

### Key Dependencies (already in build.gradle.kts)
- **Retrofit 2.9.0** + Gson + OkHttp logging interceptor
- **Glide 4.16.0** for image loading
- **Navigation** fragment-ktx & ui-ktx 2.7.7
- **AndroidX Security Crypto** 1.1.0 (EncryptedSharedPreferences)
- **Material 3** (com.google.android.material)

---

## 2. APP ARCHITECTURE & NAVIGATION FLOW

```
SplashActivity
  ├─ TokenManager.isLoggedIn() == false → LoginActivity / RegisterActivity
  └─ TokenManager.isLoggedIn() == true  → MainActivity

MainActivity (bottom nav host)
  ├─ Student role: StudentDashboardFragment + bottom nav (Home | Search | Messages | Logout)
  └─ Teacher role: TeacherDashboardFragment + bottom nav (Dashboard | Browse Posts | Messages | Logout)

Admin role → opens AdminDashboardActivity directly (separate Activity, no bottom nav)

Other Activities launched from MainActivity:
  SearchTutorsActivity → TeacherDetailActivity
  EditProfileActivity
  ChatActivity → MessageActivity
```

### Currently registered Activities (in AndroidManifest.xml):

| Activity | Class | Purpose |
|----------|-------|---------|
| SplashActivity | `.auth.SplashActivity` | **LAUNCHER** — checks login, routes |
| LoginActivity | `.auth.LoginActivity` | Email/password login |
| RegisterActivity | `.auth.RegisterActivity` | Registration with role selection |
| MainActivity | `.MainActivity` | Hub with bottom nav + fragment container |
| SearchTutorsActivity | `.student.SearchTutorsActivity` | Search/filter tutors + RecyclerView |
| TeacherDetailActivity | `.student.TeacherDetailActivity` | Full teacher profile view |
| EditProfileActivity | `.teacher.EditProfileActivity` | Teacher profile editing form |
| ChatActivity | `.chat.ChatActivity` | Conversation list |
| MessageActivity | `.chat.MessageActivity` | Individual chat with bubbles |
| AdminDashboardActivity | `.admin.AdminDashboardActivity` | Admin stats dashboard |

---

## 3. USER FLOWS (What the Web App Does — Android Should Match)

### 3.1 AUTHENTICATION
- **Login**: Email + password → POST `/api/auth/login` → returns `{token, user}` → save to TokenManager
- **Register**: Name, email, password, role (student/teacher) → POST `/api/auth/register` → returns `{token, user}`
- **Google Login**: Get Google access token via Credential Manager → POST `/api/auth/google` with `{access_token, role}`
- **Logout**: Clear TokenManager → navigate to LoginActivity

### 3.2 STUDENT FLOW
1. **Dashboard** → GET `/api/featured-teachers` (no auth needed) — show featured tutors
2. **Search Tutors** → GET `/api/students/search?q=&subject=&location=&min_fee=&max_fee=&page=&per_page=`
3. **Teacher Detail** → GET `/api/teachers/{teacher_id}` — shows profile, reviews, rating
4. **Save Tutor** → POST/DELETE `/api/students/saved-tutors` with `{teacher_id}`
5. **Saved Tutors List** → GET `/api/students/saved-tutors`
6. **Create Tuition Post** → POST `/api/students/tuition-posts` with `{title, subject, class_level, location, salary, description}`
7. **My Posts** → GET `/api/students/tuition-posts`
8. **Post Applications** → GET `/student/post/{id}/applications` (this is a server-rendered route — needs Android activity)
9. **Review Teacher** → POST `/api/reviews` with `{teacher_id, rating, comment}`
10. **My Reviews** → GET `/api/reviews` (query param teacher_id optional)

### 3.3 TEACHER FLOW
1. **Dashboard** → GET `/api/teacher/dashboard` → stats + recent applications
2. **Profile Management** → GET/PUT `/api/teacher/profile` (17 fields: subject, university, department, degree, experience, fee, hourly_fee, location, bio, availability, teaching_mode, qualification, subjects_expert_in, class_level, teaching_areas, languages, teaching_style, total_students_taught, intro_video_url)
3. **Browse Posts** → GET `/api/teacher/browse-posts?subject=&page=&per_page=`
4. **Apply to Post** → POST `/api/teacher/apply` with `{post_id, message}`
5. **My Applications** → GET `/api/teacher/applications?status=`
6. **Analytics** → GET `/api/teacher/analytics` → total/pending/accepted/rejected + rating
7. **Payment History** → GET `/api/payments`

### 3.4 ADMIN FLOW
1. **Dashboard** → GET `/api/admin/dashboard` → system-wide stats
2. **User List** → GET `/api/admin/users?role=&page=&per_page=`
3. **Approve User** → POST `/api/admin/users/{id}/approve`
4. **Toggle User Status** → POST `/api/admin/users/{id}/toggle-status`
5. **Payment List** → GET `/api/admin/payments?status=`
6. **Verify Payment** → POST `/api/admin/payments/{id}/verify`

### 3.5 CHAT (All authenticated users)
1. **Conversations** → GET `/api/chat/conversations`
2. **Messages** → GET `/api/chat/messages/{user_id}?page=&per_page=`
3. **Send Message** → POST `/api/chat/messages/{user_id}` with `{message}`
4. **Unread Count** → called via check (or GET `/api/auth/me` includes `unread_messages`)

### 3.6 NOTIFICATIONS (All logged-in users)
1. **List** → GET `/api/notifications`
2. **Mark Read** → POST `/api/notifications/{id}/read`
3. **Unread count** → included in GET `/api/auth/me` response as `unread_notifications`

### 3.7 SUBSCRIPTIONS & PAYMENTS (Teachers)
1. **Plans** → GET `/api/subscriptions/plans`
2. **My Subscription** → GET `/api/subscriptions/my`
3. **Submit Payment** → POST `/api/payments` with `{plan_id, method, sender_number, transaction_id}`

### 3.8 TO-DO (All users)
1. **List** → GET `/api/todos`
2. **Add** → POST `/api/todos` with `{title, description}`
3. **Update** → PUT `/api/todos/{id}` with `{title, description, is_completed}`
4. **Delete** → DELETE `/api/todos/{id}`

---

## 4. COMPLETE API REFERENCE

### Base URL: `http://192.168.137.1:5000/api/`
### Auth header: `Authorization: Bearer <jwt_token>`

### All endpoints return: `{"success": bool, "data": ..., "error": "..."}`

#### AUTH
| Method | Path | Auth | Body/Params | Response `data` |
|--------|------|------|-------------|-----------------|
| POST | `/auth/login` | No | `{email, password}` | `{token, user: {id, name, email, role, is_active, is_approved, profile_picture, created_at}}` |
| POST | `/auth/register` | No | `{name, email, password, role}` | `{token, user}` |
| POST | `/auth/google` | No | `{access_token, role}` | `{token, user}` |
| GET | `/auth/me` | Yes | — | `{id, name, email, role, ...profile, subscription, unread_messages, unread_notifications}` |

#### STUDENT
| Method | Path | Auth | Body/Params | Response `data` |
|--------|------|------|-------------|-----------------|
| GET | `/students/search` | Yes | `q, subject, location, min_fee, max_fee, page, per_page` | Array of `{user, profile, avg_rating, review_count, verified, featured}` + `total, page, per_page` |
| GET | `/teachers/{id}` | Yes | — | `{user, profile, avg_rating, review_count, verified, reviews: [{id, rating, comment, student_name, created_at}]}` |
| GET | `/students/tuition-posts` | Yes | — | Array of `{id, title, subject, class_level, location, salary, status, created_at, application_count}` |
| POST | `/students/tuition-posts` | Yes | `{title, subject, class_level, location, salary, description}` | `{id}` |
| GET | `/students/saved-tutors` | Yes | — | Array of `{id, teacher, profile, avg_rating, created_at}` |
| POST | `/students/saved-tutors` | Yes | `{teacher_id}` | `{id}` |
| DELETE | `/students/saved-tutors` | Yes | `{teacher_id}` | — |
| GET | `/reviews` | Yes | `?teacher_id=` | Array of `{id, rating, comment, student_name, teacher_id, created_at}` |
| POST | `/reviews` | Yes | `{teacher_id, rating, comment}` | `{id}` |

#### TEACHER
| Method | Path | Auth | Body/Params | Response `data` |
|--------|------|------|-------------|-----------------|
| GET | `/teacher/dashboard` | Yes | — | `{user, profile, stats: {total_applications, pending_applications, accepted_applications, open_posts, total_messages, avg_rating, review_count}, subscription, recent_applications}` |
| GET | `/teacher/profile` | Yes | — | `{user, profile}` |
| PUT | `/teacher/profile` | Yes | Any profile fields (subject, university, fee, location, bio, etc.) | Updated profile |
| GET | `/teacher/applications` | Yes | `?status=` | Array of `{id, post_id, post_title, post_subject, post_location, post_salary, student_name, message, status, created_at}` |
| GET | `/teacher/browse-posts` | Yes | `?subject=&page=&per_page=` | Array of `{id, title, subject, class_level, location, salary, description, student_name, has_applied, created_at}` + `total` |
| POST | `/teacher/apply` | Yes | `{post_id, message}` | `{id}` |
| GET | `/teacher/analytics` | Yes | — | `{total_applications, pending, accepted, rejected, avg_rating, review_count}` |

#### ADMIN
| Method | Path | Auth | Body/Params | Response `data` |
|--------|------|------|-------------|-----------------|
| GET | `/admin/dashboard` | Yes | — | `{total_users, total_teachers, total_students, pending_teachers, total_posts, open_posts, total_payments, pending_payments, total_revenue}` |
| GET | `/admin/users` | Yes | `?role=&page=&per_page=` | Array of user objects + `total, page` |
| POST | `/admin/users/{id}/approve` | Yes | — | — |
| POST | `/admin/users/{id}/toggle-status` | Yes | — | `{is_active}` |
| GET | `/admin/payments` | Yes | `?status=` | Array of `{id, user_name, amount, method, transaction_id, status, created_at}` |
| POST | `/admin/payments/{id}/verify` | Yes | — | — |

#### CHAT
| Method | Path | Auth | Body/Params | Response `data` |
|--------|------|------|-------------|-----------------|
| GET | `/chat/conversations` | Yes | — | Array of `{user, last_message, last_message_time, unread_count}` |
| GET | `/chat/messages/{user_id}` | Yes | `?page=&per_page=` | Array of `{id, sender_id, receiver_id, message, is_read, created_at}` |
| POST | `/chat/messages/{user_id}` | Yes | `{message}` | `{id, created_at}` |

#### NOTIFICATIONS
| Method | Path | Auth | Body/Params | Response `data` |
|--------|------|------|-------------|-----------------|
| GET | `/notifications` | Yes | — | Array of `{id, type, title, message, link, is_read, created_at}` |
| POST | `/notifications/{id}/read` | Yes | — | — |

#### SUBSCRIPTIONS
| Method | Path | Auth | Body/Params | Response `data` |
|--------|------|------|-------------|-----------------|
| GET | `/subscriptions/plans` | Yes | — | Array of `{id, name, price, duration_days, max_applications, is_featured, has_verified_badge, priority_ranking, description}` |
| GET | `/subscriptions/my` | Yes | — | `{id, plan_id, plan_name, price, start_date, end_date, days_remaining, is_active, auto_renew}` or `null` |

#### PAYMENTS
| Method | Path | Auth | Body/Params | Response `data` |
|--------|------|------|-------------|-----------------|
| GET | `/payments` | Yes | — | Array of `{id, plan_name, amount, method, transaction_id, status, created_at}` |
| POST | `/payments` | Yes | `{plan_id, method, sender_number, transaction_id}` | `{id}` |

#### TODOS
| Method | Path | Auth | Body/Params | Response `data` |
|--------|------|------|-------------|-----------------|
| GET | `/todos` | Yes | — | Array of `{id, title, description, is_completed, created_at}` |
| POST | `/todos` | Yes | `{title, description}` | `{id}` |
| PUT | `/todos/{id}` | Yes | `{title, description, is_completed}` | — |
| DELETE | `/todos/{id}` | Yes | — | — |

#### PUBLIC
| Method | Path | Auth | Body/Params | Response `data` |
|--------|------|------|-------------|-----------------|
| GET | `/featured-teachers` | No | — | Array of `{user, profile, avg_rating, review_count, verified}` |

---

## 5. DATABASE TABLES & KEY FIELDS (for Android-side understanding)

### User
| Field | Type | Notes |
|-------|------|-------|
| id | INT | PK |
| name | VARCHAR(100) | |
| email | VARCHAR(100) | Unique |
| role | VARCHAR(20) | 'student', 'teacher', 'admin' |
| is_active | BIT | Account blocked if false |
| is_approved | BIT | Teachers need admin approval |
| profile_picture | VARCHAR(500) | URL or path |
| created_at | DATETIME | |

### TeacherProfile
| Field | Type | Notes |
|-------|------|-------|
| id | INT | PK |
| user_id | INT | FK → users |
| university, department, degree | VARCHAR | |
| subject | VARCHAR | Main subject |
| experience | INT | Years |
| fee | FLOAT | Monthly fee (BDT) |
| hourly_fee | FLOAT | Per hour fee |
| location | VARCHAR | Teaching area |
| bio | TEXT | About me |
| availability | VARCHAR | 'Full-time', 'Part-time', 'Weekends' |
| teaching_mode | VARCHAR | 'Online', 'Offline', 'Both' |
| qualification | VARCHAR | |
| subjects_expert_in | TEXT | Comma-separated |
| class_level | VARCHAR | 'HSC', 'SSC', '1-5', '6-10', 'University' |
| teaching_areas | TEXT | |
| languages | TEXT | |
| teaching_style | VARCHAR | |
| total_students_taught | INT | |
| intro_video_url | VARCHAR | |
| cv | VARCHAR | File path |
| is_complete | BIT | True if subject AND fee set |

### SubscriptionPlan
| Field | Type |
|-------|------|
| id, name, price, duration_days, max_applications, has_verified_badge, is_featured, priority_ranking, description | |

### UserSubscription
| Field | Type |
|-------|------|
| id, user_id, plan_id, start_date, end_date, is_active, auto_renew | |

### Payment
| Field | Type |
|-------|------|
| id, user_id, plan_id, amount, method, sender_number, transaction_id, status ('Pending'/'Verified'/'Rejected'), verified_by, verified_at | |

### TuitionPost
| Field | Type |
|-------|------|
| id, student_id, title, subject, class_level, location, salary, description, status ('Open'/'Closed') | |

### Application
| Field | Type |
|-------|------|
| id, post_id, teacher_id, message, status ('Pending'/'Shortlisted'/'Accepted'/'Rejected') | |

### Message
| Field | Type |
|-------|------|
| id, sender_id, receiver_id, message, is_read, read_at, created_at | |

### Review
| Field | Type |
|-------|------|
| id, student_id, teacher_id, rating (1-5), comment, created_at | |

### Notification
| Field | Type |
|-------|------|
| id, user_id, type, title, message, link, is_read, created_at | |

### SavedTutor
| Field | Type |
|-------|------|
| id, student_id, teacher_id, created_at | |

### ToDo
| Field | Type |
|-------|------|
| id, user_id, title, description, is_completed, created_at | |

---

## 6. ALREADY IMPLEMENTED IN ANDROID APP

### ✅ Fully Working
- **Splash → Login/Register → Main flow** with role routing
- **JWT token management** via EncryptedSharedPreferences (TokenManager)
- **Retrofit API client** with auth interceptor and logging
- **All 30+ API endpoints** defined in `ApiService.kt`
- **All 20+ data models** defined in `Models.kt` with Gson annotations
- **Student Dashboard** — shows featured tutors from API
- **Search Tutors** — with query, subject, location, fee range filters + RecyclerView
- **Teacher Detail** — full profile view with save button
- **Teacher Profile Editing** — form with 8 fields (subject, fee, location, university, department, degree, experience, bio)
- **Teacher Dashboard** — stats grid (applications, rating, messages, subscription)
- **Admin Dashboard** — system-wide stats
- **Chat List** — conversation list with unread counts
- **Message Activity** — send/receive messages with chat bubbles
- **Utils** — Glide image loading, toast, keyboard hide helpers
- **Color scheme** — Material 3 purple (#6750A4) primary
- **Layouts** — 15 XML layouts for all screens
- **Menu** — 2 bottom nav menus (student & teacher)

### 🚧 NOT YET IMPLEMENTED (Needs Work)

| Feature | What's Needed |
|---------|---------------|
| **Google Login** | ApiService has `googleLogin()` — needs UI integration with Credential Manager API |
| **Student: Browse Posts (tuition posts)** | API exists — needs Activity/Fragment + RecyclerView |
| **Student: Create Post** | API exists — needs form Activity |
| **Student: Post Applications** | API exists — needs Activity showing applications per post |
| **Student: Saved Tutors List** | API exists — needs Activity with RecyclerView |
| **Student: Review Teacher** | API exists — needs rating UI (stars) in TeacherDetailActivity |
| **Teacher: Browse Posts** | API exists, fragment has button — no click handler or Activity |
| **Teacher: Applications List** | API exists — needs Activity/RecyclerView with filter by status |
| **Teacher: Analytics** | API exists — needs charts/graphs |
| **Teacher: Payment History** | API exists — needs RecyclerView |
| **Admin: User Management** | API exists — needs RecyclerView + approve/toggle actions |
| **Admin: Payment Verification** | API exists — needs RecyclerView + verify button |
| **Admin: Post Management** | API exists — needs Activity |
| **Notifications** | API exists — needs Activity + RecyclerView |
| **Subscriptions** | API exists — needs plan cards + payment form |
| **Todo List** | Full CRUD API exists — needs Activity |
| **Profile Picture Upload** | Model has field but no image picker |
| **Real-time Chat** | Currently manual refresh — needs polling or WebSocket |
| **Pagination** | API supports but UI doesn't implement infinite scroll |
| **Logout from all screens** | Bottom nav has logout but no confirmation dialog |
| **Error handling UX** | Toasts only — needs Snackbar/dialog patterns |

---

## 7. DESIGN SYSTEM & THEME

### Color Palette (from `colors.xml`)

```xml
<!-- Already defined -->
<color name="primary">#6750A4</color>
<color name="primary_dark">#4F378B</color>
<color name="primary_light">#EADDFF</color>
<color name="secondary">#625B71</color>
<color name="tertiary">#7D5260</color>
<color name="surface">#FFFBFE</color>
<color name="success">#4CAF50</color>
<color name="warning">#FF9800</color>
<color name="error">#B3261E</color>
<color name="verified_badge">#4CAF50</color>
```

### Web App Design Reference
The web app uses an "Atelier" design system with:
- **Glassmorphism** — blurred backgrounds with `rgba(255,255,255,0.7)` glass effect
- **Inter font** (Google Fonts)
- **Material Symbols** for icons
- **Editorial sophistication** — clean, premium look with subtle shadows
- **Verified badges** — green checkmark on Premium/Standard tutor cards
- **Featured tutor cards** — elevated cards with priority ranking
- **Hero section** — blue gradient (`#1e3a8a`) with search CTA
- **Responsive grid** columns for tutor cards

### Android UI Guidelines
- Use **Material 3** components throughout (MaterialCardView, TextInputLayout, BottomNavigationView)
- Use **Glide** for all image loading with `loadProfilePicture()` extension (circular crop)
- Verified badge: green dot/icon on tutor cards
- Chat bubble colors:
  - Sent: `@color/primary` (purple) with right alignment
  - Received: `@color/surface_container` (gray) with left alignment

---

## 8. HELPER UTILITIES (in `Utils.kt`)

```kotlin
// Load profile picture with Glide (circular, placeholder on error)
ImageView.loadProfilePicture(url: String?)

// Show/hide views
View.show()
View.hide()

// Toast
Context.showToast(message: String)

// Hide keyboard
Activity.hideKeyboard()

// Capitalize words
String.capitalizeWords(): String
```

---

## 9. TOKEN MANAGER API (in `TokenManager.kt`)

```kotlin
TokenManager.saveToken(token: String)
TokenManager.getToken(): String?
TokenManager.saveUserInfo(id: Int, role: String, name: String, email: String)
TokenManager.getUserId(): Int?
TokenManager.getUserRole(): String?
TokenManager.getUserName(): String?
TokenManager.getUserEmail(): String?
TokenManager.isLoggedIn(): Boolean
TokenManager.logout()
```

---

## 10. TEST CREDENTIALS

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@tuition.com | admin123 |
| Teacher | ahmed@tutor.com | password123 |
| Teacher | sarah@tutor.com | password123 |
| Student | rahim@student.com | password123 |
| Student | karim@student.com | password123 |

---

## 11. IMPLEMENTATION ORDER (Recommended)

### Phase 1: Complete Core Features (Immediate)
1. **Google Login** — integrate Credential Manager → `api/auth/google`
2. **Student: Create Post** — form Activity → POST `/api/students/tuition-posts`
3. **Student: My Posts + Applications** — RecyclerView + status management
4. **Teacher: Browse & Apply to Posts** — RecyclerView + apply dialog
5. **Teacher: Applications List** — RecyclerView with status filter

### Phase 2: Secondary Features
6. **Notifications** — Activity with RecyclerView + mark-as-read
7. **Subscriptions** — Plan cards → payment form → POST `/api/payments`
8. **Todo List** — Full CRUD UI
9. **Saved Tutors** — Activity with RecyclerView
10. **Teacher Analytics** — Charts (MPAndroidChart or similar)

### Phase 3: Admin Panel
11. **Admin: User Management** — RecyclerView + approve/toggle
12. **Admin: Payments** — List + verify button
13. **Admin: Posts** — List + close posts

### Phase 4: Polish
14. **Profile Picture Upload** — Image picker → multipart upload
15. **Pagination** — Add scroll listeners for infinite loading
16. **Real-time Chat** — Polling every 5s or WebSocket
17. **Error Handling** — Consistent Snackbar/dialog patterns
18. **Pull-to-refresh** — SwipeRefreshLayout on all lists

---

## 12. API SERVICE ENDPOINTS (already defined — use as reference)

The `ApiService.kt` interface already has all endpoints defined. Key method names:

```kotlin
// Auth
fun login(@Body body) → Call<ApiResponse<AuthData>>
fun register(@Body body) → Call<ApiResponse<AuthData>>
fun googleLogin(@Body body) → Call<ApiResponse<AuthData>>
fun getMe() → Call<ApiResponse<UserData>>

// Student
fun searchTutors(@QueryMap) → Call<ApiResponse<List<TeacherListItem>>>
fun getTeacherDetail(@Path("teacher_id") id) → Call<ApiResponse<TeacherDetailData>>
fun getTuitionPosts() → Call<ApiResponse<List<TuitionPostData>>>
fun createTuitionPost(@Body body) → Call<ApiResponse<TuitionPostData>>
fun getSavedTutors() → Call<ApiResponse<List<SavedTutorData>>>
fun saveTutor(@Body body) → Call<ApiResponse<Any>>
fun deleteSavedTutor(@Body body) → Call<ApiResponse<Any>>
fun submitReview(@Body body) → Call<ApiResponse<Any>>

// Teacher
fun getTeacherDashboard() → Call<ApiResponse<TeacherDashboardData>>
fun getTeacherProfile() → Call<ApiResponse<TeacherProfileData>>
fun updateTeacherProfile(@Body body) → Call<ApiResponse<TeacherProfileData>>
fun getTeacherApplications(@Query("status") status) → Call<ApiResponse<List<ApplicationData>>>
fun browsePosts(@QueryMap) → Call<ApiResponse<List<TuitionPostData>>>
fun applyToPost(@Body body) → Call<ApiResponse<Any>>
fun getTeacherAnalytics() → Call<ApiResponse<TeacherStats>>

// Admin
fun getAdminDashboard() → Call<ApiResponse<AdminDashboardData>>
fun getAdminUsers(@QueryMap) → Call<ApiResponse<List<UserData>>>
fun approveUser(@Path("id") id) → Call<ApiResponse<Any>>
fun toggleUserStatus(@Path("id") id) → Call<ApiResponse<Any>>
fun getAdminPayments(@Query("status") status) → Call<ApiResponse<List<PaymentData>>>
fun verifyPayment(@Path("id") id) → Call<ApiResponse<Any>>

// Chat
fun getConversations() → Call<ApiResponse<List<ConversationData>>>
fun getMessages(@Path("user_id") id, @QueryMap) → Call<ApiResponse<List<MessageData>>>
fun sendMessage(@Path("user_id") id, @Body body) → Call<ApiResponse<MessageData>>

// Notifications
fun getNotifications() → Call<ApiResponse<List<NotificationData>>>
fun markNotificationRead(@Path("id") id) → Call<ApiResponse<Any>>

// Subscriptions & Payments
fun getSubscriptionPlans() → Call<ApiResponse<List<SubscriptionPlanData>>>
fun getMySubscription() → Call<ApiResponse<SubscriptionInfo>>
fun getPayments() → Call<ApiResponse<List<PaymentData>>>
fun submitPayment(@Body body) → Call<ApiResponse<Any>>

// Todos
fun getTodos() → Call<ApiResponse<List<TodoData>>>
fun createTodo(@Body body) → Call<ApiResponse<TodoData>>
fun updateTodo(@Path("id") id, @Body body) → Call<ApiResponse<Any>>
fun deleteTodo(@Path("id") id) → Call<ApiResponse<Any>>

// Public
fun getFeaturedTeachers() → Call<ApiResponse<List<TeacherListItem>>>
```

---

## 13. DATA MODELS (already defined in `Models.kt`)

```kotlin
data class ApiResponse<T>(val success: Boolean, val data: T?, val error: String?, val total: Int?, val page: Int?, val perPage: Int?)
data class AuthData(val token: String, val user: UserData)
data class UserData(val id: Int, val name: String, val email: String, val role: String, ...)
data class TeacherListItem(val user: UserData, val profile: TeacherProfileData?, val avgRating: Double?, ...)
data class TeacherDetailData(val user: UserData, val profile: TeacherProfileData?, ...)
data class TeacherProfileData(val id: Int, val userId: Int, val university: String?, ...)
data class TeacherDashboardData(val user: UserData, val profile: TeacherProfileData?, val stats: TeacherStats?, ...)
data class TeacherStats(val totalApplications: Int, val pendingApplications: Int, ...)
data class AdminDashboardData(val totalUsers: Int, val totalTeachers: Int, ...)
data class TuitionPostData(val id: Int, val title: String, val subject: String, ...)
data class ApplicationData(val id: Int, val postId: Int, val postTitle: String, ...)
data class MessageData(val id: Int, val senderId: Int, val receiverId: Int, val message: String, ...)
data class ConversationData(val user: UserData, val lastMessage: String?, val lastMessageTime: String?, val unreadCount: Int)
data class NotificationData(val id: Int, val type: String, val title: String, ...)
data class SubscriptionPlanData(val id: Int, val name: String, val price: Double, ...)
data class SubscriptionInfo(val id: Int, val planId: Int, val planName: String, ...)
data class PaymentData(val id: Int, val planName: String?, val amount: Double, ...)
data class SavedTutorData(val id: Int, val teacher: UserData, val profile: TeacherProfileData?, ...)
data class TodoData(val id: Int, val title: String, val description: String?, val isCompleted: Boolean, ...)
```

---

## 14. IMPORTANT NOTES

- **Server IP**: The API base URL is currently `http://192.168.137.1:5000/api/` — change in `BuildConfig` or `ApiClient.kt` for production
- **Cleartext traffic**: Enabled in `network_security_config.xml` for local dev (remove for production HTTPS)
- **Role handling**: `TokenManager.getUserRole()` returns "student", "teacher", or "admin" — use this for all role-based navigation
- **Fragment reuse**: `StudentDashboardFragment` and `TeacherDashboardFragment` are swapped via `FragmentManager.replace()` in `MainActivity`
- **Coroutines**: Each activity creates its own `CoroutineScope(Dispatchers.Main + SupervisorJob())` — cancel in `onDestroy()`
- **No DI**: Currently no Hilt/Dagger — consider adding Hilt for production
- **No Room**: No local cache — all data from network
