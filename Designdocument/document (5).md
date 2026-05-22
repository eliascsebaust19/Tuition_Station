# Student Dashboard & Tutor Search with Filters

## Overview
Build a student dashboard with sidebar navigation, tutor search and filtering capabilities, tutor discovery grid, tuition request modal, and saved tutors list. The dashboard is role-protected (student only) and responsive across desktop and mobile devices.

## Problem Statement
Students need a centralized place to discover tutors by location, subject, and budget, save favorites for later, and send tuition requests. Without a dedicated dashboard, the search experience is fragmented and inefficient.

## Solution
Create a student dashboard with persistent sidebar navigation, advanced search filters, tutor cards in a grid layout, a modal for sending requests, and a saved tutors section. Implement responsive design with collapsible sidebar on mobile.

## UI/UX Layout

### Dashboard Structure
The dashboard uses a two-column layout: a persistent sidebar on the left (collapsible on mobile) and main content area on the right. The sidebar contains navigation links (Dashboard, Saved Tutors, Profile, Logout) and is branded with the app logo/name at the top. The main content area displays the tutor search section at the top, followed by a grid of tutor cards below.

### Search & Filter Section
The search section sits at the top of the main content area and includes:
- **Search Bar** (primary): Text input for tutor name or keyword search
- **Filter Controls** (secondary): Collapsible filter panel with three filter groups:
  - Location (text input or dropdown)
  - Subject (multi-select dropdown or checkboxes)
  - Hourly Rate (range slider: min-max or two number inputs)
- **Apply Filters Button** (tertiary): Triggers search/filter
- **Clear Filters Link** (tertiary): Resets all filters to defaults

### Tutor Grid Cards
Tutor results display in a responsive grid (3 columns on desktop, 2 on tablet, 1 on mobile). Each card contains:
- **Tutor Name** (primary): Bold, top-left
- **Subjects** (secondary): Comma-separated list below name
- **Hourly Rate** (secondary): Displayed prominently (e.g., "$25/hr")
- **Rating** (secondary): Star rating or numeric score (e.g., "4.5/5")
- **Location** (tertiary): Small text, bottom-left
- **Save Button** (interactive): Heart icon or "Save" button, top-right; toggles filled/unfilled state
- **View Profile / Send Request Button** (primary action): Button at bottom-right of card

### Send Tuition Request Modal
When user clicks "Send Request" on a card, a modal appears with:
- **Modal Title** (primary): "Send Tuition Request to [Tutor Name]"
- **Tutor Summary** (secondary): Small card showing tutor name, subject, rate
- **Message Input** (primary): Text area for student to write a message (optional)
- **Preferred Schedule** (secondary): Optional fields for preferred days/times (if applicable in v1)
- **Send Button** (primary action): Submits request
- **Cancel Button** (secondary action): Closes modal without sending

### Saved Tutors Section
A dedicated page/tab showing saved tutors in a similar grid format to the main search results. Includes a message if no tutors are saved ("No saved tutors yet. Start exploring!").

### Responsive Sidebar (Mobile)
On mobile (< 768px):
- Sidebar collapses to a hamburger menu icon in the top-left
- Clicking hamburger toggles sidebar visibility (slides in from left, overlays content)
- Sidebar closes when a navigation link is clicked
- Main content area expands to full width when sidebar is closed

## User Stories

- As a student, I want to search for tutors by name or keyword so I can find tutors matching my interests
- As a student, I want to filter tutors by location so I can find tutors near me
- As a student, I want to filter tutors by subject so I can find tutors who teach what I need
- As a student, I want to filter tutors by hourly rate so I can find tutors within my budget
- As a student, I want to see tutor cards with name, subjects, rate, and rating so I can quickly evaluate options
- As a student, I want to save tutors to a favorites list so I can revisit them later
- As a student, I want to unsave tutors from my favorites so I can manage my saved list
- As a student, I want to send a tuition request to a tutor with an optional message so I can express my interest
- As a student, I want to view my saved tutors in a dedicated list so I can easily access my favorites
- As a student on mobile, I want the sidebar to collapse so I have more screen space for browsing tutors
- As a non-student user, I want to be redirected away from the student dashboard so I cannot access student-only features

## Functional Requirements

### Dashboard Access & Authentication
- **Route**: `/student/dashboard`
- **Access Control**: Require user to be logged in with role = "student"; redirect to login if not authenticated, redirect to appropriate dashboard if wrong role
- **Session Check**: Verify session contains user_id and role = "student" on page load

### Search & Filter Functionality
- **Search Bar**: Accept text input; search against tutor name and bio fields (case-insensitive)
- **Location Filter**: Filter TeacherProfile records by location field (exact match or contains)
- **Subject Filter**: Filter TeacherProfile records by subjects field (multi-select; match if any selected subject is in tutor's subjects list)
- **Rate Filter**: Filter TeacherProfile records by hourly_rate field (range: min ≤ rate ≤ max)
- **Apply Filters**: Combine all active filters with AND logic (location AND subject AND rate AND search)
- **Clear Filters**: Reset all filters to defaults and reload tutor list
- **Pagination** (optional for v1): If result set is large, implement offset/limit pagination (e.g., 12 tutors per page)

### Tutor Grid Display
- **Data Source**: Query TeacherProfile and User tables; join on user_id
- **Grid Layout**: CSS Grid or Flexbox; responsive columns (3 desktop, 2 tablet, 1 mobile)
- **Card Content**: Display tutor name, subjects, hourly_rate, rating (if available), location
- **Card Interaction**: Clicking card or "View Profile" button navigates to tutor profile page (or opens modal with details)
- **Empty State**: If no tutors match filters, display message "No tutors found. Try adjusting your filters."

### Save Tutor Functionality
- **Save Button**: Heart icon or "Save" button on each card; toggles between saved/unsaved state
- **Save Action**: POST to `/student/saved-tutors` with tutor_id; creates SavedTutor record
- **Unsave Action**: DELETE to `/student/saved-tutors/{tutor_id}`; removes SavedTutor record
- **Visual Feedback**: Button changes appearance (filled heart vs outline) to indicate saved state
- **Persistence**: Saved state persists across page reloads (stored in database)

### Send Tuition Request Modal
- **Trigger**: Clicking "Send Request" button on tutor card
- **Modal Content**: Display tutor name, subject, rate; text area for optional message
- **Submit Action**: POST to `/student/requests` with tutor_id, message (optional); creates TuitionRequest record
- **Success Feedback**: Show success message ("Request sent!") and close modal
- **Error Handling**: Display error message if request fails (e.g., "Failed to send request. Please try again.")
- **Cancel**: Close modal without sending

### Saved Tutors Page
- **Route**: `/student/saved-tutors`
- **Access Control**: Require student role
- **Display**: Show saved tutors in grid format (same as search results)
- **Empty State**: If no saved tutors, display "No saved tutors yet. Start exploring!" with link to search
- **Remove from Saved**: Clicking unsave button removes tutor from saved list and updates display

### Responsive Sidebar Navigation
- **Desktop (≥ 768px)**: Sidebar is always visible on left; main content takes remaining space
- **Mobile (< 768px)**: Sidebar collapses to hamburger menu; clicking hamburger toggles sidebar visibility
- **Sidebar Content**: Logo/app name at top; navigation links (Dashboard, Saved Tutors, Profile, Logout)
- **Mobile Behavior**: Sidebar slides in from left, overlays content; clicking a link closes sidebar; clicking outside sidebar closes it
- **Hamburger Icon**: Three horizontal lines; positioned in top-left of header

## Technical Requirements

### Backend Routes

| Endpoint                               | Method   | Purpose                   | Auth    | Request Body                                                                               | Response                                                                             |
| -------------------------------------- | -------- | ------------------------- | ------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| `/student/dashboard`                   | GET      | Display dashboard         | Student | —                                                                                          | HTML page with search form and tutor grid                                            |
| `/api/tutors`                          | GET      | Search and filter tutors  | Student | Query params: `search`, `location`, `subject[]`, `rate_min`, `rate_max`, `limit`, `offset` | JSON: `{tutors: [{id, name, subjects, rate, rating, location, saved}], total, page}` |
| `/student/saved-tutors`                | GET      | Display saved tutors page | Student | —                                                                                          | HTML page with saved tutors grid                                                     |
| `/api/student/saved-tutors`            | POST     | Save a tutor              | Student | `{tutor_id}`                                                                               | JSON: `{success: true, message: "Tutor saved"}` or error                             |
| `/api/student/saved-tutors/{tutor_id}` | DELETE   | Unsave a tutor            | Student | —                                                                                          | JSON: `{success: true, message: "Tutor removed from saved"}` or error                |
| `/api/student/requests`                | POST     | Send tuition request      | Student | `{tutor_id, message}`                                                                      | JSON: `{success: true, request_id, message: "Request sent"}` or error                |

### Frontend Components

| Component            | Purpose                         | Props/State                                                  | Events                                |
| -------------------- | ------------------------------- | ------------------------------------------------------------ | ------------------------------------- |
| **Sidebar**          | Navigation and branding         | `isOpen` (mobile), `currentPage`                             | `onToggle`, `onNavigate`              |
| **SearchBar**        | Text search input               | `value`, `onChange`                                          | `onSearch`                            |
| **FilterPanel**      | Location, subject, rate filters | `filters` (location, subjects, rateMin, rateMax), `onChange` | `onApply`, `onClear`                  |
| **TutorCard**        | Individual tutor display        | `tutor` (id, name, subjects, rate, rating, location, saved)  | `onSave`, `onUnsave`, `onSendRequest` |
| **TutorGrid**        | Grid of tutor cards             | `tutors[]`, `loading`, `empty`                               | `onCardAction`                        |
| **SendRequestModal** | Tuition request form            | `tutor`, `isOpen`                                            | `onSend`, `onCancel`                  |
| **SavedTutorsList**  | Saved tutors page               | `tutors[]`, `loading`, `empty`                               | `onUnsave`                            |

### Data Requirements

**SavedTutor** (new entity)
- saved_tutor_id (integer, primary key)
- student_id (integer, foreign key → User.user_id, not null)
- tutor_id (integer, foreign key → User.user_id, not null)
- created_at (datetime, default now)
- Unique constraint: (student_id, tutor_id)

**TuitionRequest** (new entity, used by this and REQ-6)
- request_id (integer, primary key)
- student_id (integer, foreign key → User.user_id, not null)
- tutor_id (integer, foreign key → User.user_id, not null)
- message (text, nullable)
- status (enum: pending/accepted/rejected, default pending)
- created_at (datetime, default now)
- updated_at (datetime, default now, on update)

### Error Handling

| Scenario                      | Status Code   | Response                                                     |
| ----------------------------- | ------------- | ------------------------------------------------------------ |
| User not authenticated        | 401           | Redirect to login                                            |
| User is not student           | 403           | Redirect to appropriate dashboard                            |
| Tutor not found               | 404           | JSON: `{error: "Tutor not found"}`                           |
| Save/unsave fails (DB error)  | 500           | JSON: `{error: "An error occurred. Please try again."}`      |
| Send request fails (DB error) | 500           | JSON: `{error: "Failed to send request. Please try again."}` |
| Invalid filter parameters     | 400           | JSON: `{error: "Invalid filter parameters"}`                 |

### API Response Format (Matching Existing Patterns)

**GET /api/tutors Success (200):**
```json
{
  "tutors": [
    {
      "id": 2,
      "name": "Jane Smith",
      "subjects": "Math, Physics",
      "hourly_rate": 25,
      "rating": 4.5,
      "location": "Downtown",
      "saved": true
    }
  ],
  "total": 42,
  "page": 1,
  "limit": 12
}
```

**POST /api/student/saved-tutors Success (201):**
```json
{
  "success": true,
  "message": "Tutor saved"
}
```

**POST /api/student/requests Success (201):**
```json
{
  "success": true,
  "request_id": 5,
  "message": "Request sent"
}
```

## Acceptance Criteria

- [] Given a student is logged in, When they navigate to `/student/dashboard`, Then the dashboard loads with sidebar, search bar, and tutor grid
- [] Given a student is not logged in, When they try to access `/student/dashboard`, Then they are redirected to the login page
- [] Given a non-student user is logged in, When they try to access `/student/dashboard`, Then they are redirected to their role-specific dashboard
- [] Given the dashboard is loaded, When the student enters text in the search bar and clicks search, Then tutors matching the search term are displayed in the grid
- [] Given the dashboard is loaded, When the student selects a location filter and clicks apply, Then only tutors in that location are displayed
- [] Given the dashboard is loaded, When the student selects one or more subjects and clicks apply, Then only tutors teaching those subjects are displayed
- [] Given the dashboard is loaded, When the student sets a rate range and clicks apply, Then only tutors within that rate range are displayed
- [] Given filters are applied, When the student clicks clear filters, Then all filters are reset and all tutors are displayed
- [] Given multiple filters are active, When the student applies them, Then tutors matching ALL filters are displayed (AND logic)
- [] Given no tutors match the filters, When the search is executed, Then a message "No tutors found. Try adjusting your filters." is displayed
- [] Given a tutor card is displayed, When the student clicks the save button, Then the tutor is added to their saved list and the button changes appearance
- [] Given a tutor is saved, When the student clicks the unsave button, Then the tutor is removed from their saved list and the button changes appearance
- [] Given a tutor card is displayed, When the student clicks "Send Request", Then a modal opens with the tutor's name, subject, and rate
- [] Given the send request modal is open, When the student enters a message and clicks send, Then a POST request is made to `/api/student/requests` with tutor_id and message
- [] Given a request is sent successfully, When the modal closes, Then a success message is displayed
- [] Given a request fails to send, When the error occurs, Then an error message is displayed in the modal
- [] Given the send request modal is open, When the student clicks cancel, Then the modal closes without sending a request
- [] Given a student has saved tutors, When they navigate to `/student/saved-tutors`, Then their saved tutors are displayed in a grid
- [] Given a student has no saved tutors, When they navigate to `/student/saved-tutors`, Then a message "No saved tutors yet. Start exploring!" is displayed
- [] Given a tutor is displayed on the saved tutors page, When the student clicks unsave, Then the tutor is removed from the saved list
- [] Given the dashboard is viewed on desktop (≥ 768px), When the page loads, Then the sidebar is visible and the main content takes the remaining space
- [] Given the dashboard is viewed on mobile (< 768px), When the page loads, Then the sidebar is collapsed and a hamburger menu is visible
- [] Given the sidebar is collapsed on mobile, When the student clicks the hamburger menu, Then the sidebar slides in from the left and overlays the content
- [] Given the sidebar is open on mobile, When the student clicks a navigation link, Then the sidebar closes
- [] Given the sidebar is open on mobile, When the student clicks outside the sidebar, Then the sidebar closes
- [] Given a tutor card displays name, subjects, rate, rating, and location, When the card is rendered, Then all fields are visible and properly formatted