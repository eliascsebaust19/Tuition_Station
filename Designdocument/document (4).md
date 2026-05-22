# Landing Page with Hero Section, Search Bar, and Featured Tutors

## Overview
Create a public-facing landing page that serves as the marketplace entry point. The page features a hero section with headline and role-based signup CTAs, a search bar for discovering tutors by location and subject, and a featured tutors grid showcasing top tutors. The design is mobile-first responsive with Font Awesome icons and a cohesive color scheme. No authentication is required to view the page.

## Problem Statement
New visitors need an intuitive, visually engaging entry point to understand the platform's value and begin their tutor discovery journey. Without a compelling hero section and easy search access, users may not understand the platform's purpose or know how to get started.

## Solution
Build a single-page landing experience with three key sections: (1) Hero with headline, value proposition, and role-specific signup buttons; (2) Search bar for filtering tutors by location and subject; (3) Featured tutors grid displaying tutor cards with profile information, ratings, and hourly rates. Design mobile-first with responsive breakpoints, Font Awesome icons for visual clarity, and hover effects for interactivity.

## UI Layout Description

### Hero Section (Epicenter)
The hero section is the visual anchor of the page. It occupies full viewport height on desktop, stacking vertically on mobile. The primary content is a headline ("Find Your Perfect Tutor" or similar) paired with a subheadline explaining the value proposition in 1-2 sentences. Below the text are two prominent CTA buttons side-by-side on desktop (stacked on mobile): "Sign Up as Student" (primary color #2563EB) and "Sign Up as Teacher" (secondary color #10B981). Both buttons use Font Awesome icons (e.g., `fa-user-graduate` for student, `fa-chalkboard-user` for teacher) to the left of the text. The hero background is a subtle gradient or solid light color to ensure text readability.

### Search Section (Supporting)
Below the hero, a search bar section allows visitors to explore tutors without signing up. The search bar is a horizontal form with two input fields side-by-side on desktop (stacked on mobile): "Location" (text input with `fa-map-marker-alt` icon) and "Subject" (dropdown or text input with `fa-book` icon). A "Search" button (primary color #2563EB) with `fa-search` icon triggers the search. This section includes a brief label ("Search for tutors near you") above the form. On mobile, the search bar takes full width with inputs stacking vertically.

### Featured Tutors Grid (Supporting)
Below the search section, a "Featured Tutors" heading introduces a grid of tutor cards. The grid is 4 columns on desktop (1200px+), 3 columns on tablet (768px-1199px), 2 columns on mobile landscape (480px-767px), and 1 column on mobile portrait (<480px). Each card displays:
- **Tutor photo** (top, square aspect ratio, placeholder if unavailable)
- **Name** (bold, primary color #2563EB)
- **Subjects** (secondary text, comma-separated list)
- **Hourly rate** (bold, secondary color #10B981, e.g., "$25/hr")
- **Rating** (star icon `fa-star` in secondary color, followed by numeric rating, e.g., "4.8 (24 reviews)")
- **"View Profile" button** (outline style, primary color #2563EB, small)

Cards have a subtle shadow and rounded corners (8px). On hover, cards lift slightly (box-shadow increase) and the "View Profile" button background fills with primary color. No authentication required; clicking "View Profile" navigates to a public tutor profile page (or shows a modal if profile viewing is gated).

## User Stories

- As a prospective student, I want to see a clear headline and signup button so I can quickly understand the platform and register as a student.
- As a prospective teacher, I want to see a clear headline and signup button so I can quickly understand the platform and register as a teacher.
- As a visitor, I want to search for tutors by location and subject without signing up so I can explore available options before committing.
- As a visitor, I want to see featured tutors with their rates and ratings so I can get a sense of the tutor quality and pricing on the platform.

## Functional Requirements

### Hero Section
- Display a headline (e.g., "Find Your Perfect Tutor") and subheadline (e.g., "Connect with qualified tutors in your area")
- Provide two CTA buttons: "Sign Up as Student" and "Sign Up as Teacher"
- Each button includes a Font Awesome icon (student: `fa-user-graduate`, teacher: `fa-chalkboard-user`)
- Buttons link to `/auth/register?role=student` and `/auth/register?role=teacher` respectively
- Hero section spans full viewport height on desktop, adapts to content height on mobile
- Background uses a subtle gradient or solid light color (#F9FAFB or similar)

### Search Bar
- Two input fields: "Location" (text input) and "Subject" (dropdown or text input)
- Each field has a Font Awesome icon (location: `fa-map-marker-alt`, subject: `fa-book`)
- "Search" button with `fa-search` icon triggers a GET request to `/student/search?location=X&subject=Y`
- Search bar is responsive: side-by-side on desktop, stacked on mobile
- Search is optional (both fields can be empty for a general search)

### Featured Tutors Grid
- Display 6-8 featured tutors (fetched from backend or hardcoded for MVP)
- Grid layout: 4 columns (desktop), 3 columns (tablet), 2 columns (mobile landscape), 1 column (mobile portrait)
- Each card displays: photo, name, subjects, hourly rate, rating, and "View Profile" button
- Card hover effect: lift (increase box-shadow) and button background fill
- "View Profile" button links to `/tutor/<teacher_id>` (public profile page)
- Cards have 8px border-radius and subtle shadow (e.g., `box-shadow: 0 1px 3px rgba(0,0,0,0.1)`)

### Responsive Design
- Mobile-first approach: base styles for mobile, media queries for larger screens
- Breakpoints: 480px (mobile landscape), 768px (tablet), 1200px (desktop)
- Hero section: full viewport height on desktop, auto height on mobile
- Search bar: full width, inputs stack vertically on mobile
- Featured tutors grid: responsive column count per breakpoint
- All text is readable on mobile (minimum 16px font size for body text)
- Touch-friendly button sizes (minimum 44px height on mobile)

### Color Scheme & Typography
- Primary color: #2563EB (buttons, headings, accents)
- Secondary color: #10B981 (rates, secondary CTAs, accents)
- Neutral colors: #F9FAFB (light background), #6B7280 (secondary text), #111827 (dark text)
- Font: System font stack or web-safe font (e.g., -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto)
- Heading: 2.5rem (desktop), 1.875rem (mobile)
- Body text: 1rem (desktop), 0.875rem (mobile)
- Font Awesome icons: 1.25rem for buttons, 1rem for form labels

### No Authentication Required
- Landing page is publicly accessible at `/` (no login required)
- Search functionality is public (no login required to search)
- "View Profile" links may redirect to login if profile viewing is gated (handled in separate requirement)

## Technical Requirements

### Frontend
- Use HTML5 semantic markup (header, main, section, article)
- CSS Grid for featured tutors layout (responsive via media queries)
- Flexbox for hero section and search bar alignment
- Font Awesome 6+ for icons (CDN or local installation)
- Responsive images for tutor photos (srcset for different resolutions)
- No JavaScript required for basic layout; optional JS for search form submission and hover effects

### Backend Integration
- Fetch featured tutors from `/api/tutors?featured=true` endpoint (returns JSON list of tutors)
- Search form submits to `/student/search?location=X&subject=Y` (backend handles filtering)
- Tutor profile links point to `/tutor/<teacher_id>` (backend serves public profile page)

### Data Requirements
- Featured tutors list: teacher_id, name, subjects, hourly_rate, rating, photo_url
- Search filters: location (string), subject (string)

## Acceptance Criteria

- [] Given the landing page is loaded, When the page renders, Then the hero section displays a headline, subheadline, and two CTA buttons (Student and Teacher signup)
- [] Given a visitor views the hero section on desktop, When the page renders, Then the hero section spans full viewport height with centered text and buttons
- [] Given a visitor views the hero section on mobile, When the page renders, Then the hero section adapts to content height with stacked buttons and readable text (minimum 16px)
- [] Given a visitor clicks "Sign Up as Student", When the button is clicked, Then the user is redirected to `/auth/register?role=student`
- [] Given a visitor clicks "Sign Up as Teacher", When the button is clicked, Then the user is redirected to `/auth/register?role=teacher`
- [] Given the search bar is visible, When a visitor enters a location and subject, Then clicking "Search" submits a GET request to `/student/search?location=X&subject=Y`
- [] Given the search bar is visible on mobile, When the page renders, Then the location and subject inputs stack vertically and take full width
- [] Given the featured tutors section is visible, When the page renders, Then 6-8 tutor cards are displayed in a responsive grid (4 columns on desktop, 3 on tablet, 2 on mobile landscape, 1 on mobile portrait)
- [] Given a tutor card is visible, When the card renders, Then it displays the tutor's photo, name, subjects, hourly rate, and rating
- [] Given a tutor card is hovered on desktop, When the mouse hovers over the card, Then the card lifts (box-shadow increases) and the "View Profile" button background fills with primary color #2563EB
- [] Given a tutor card is visible, When "View Profile" is clicked, Then the user is redirected to `/tutor/<teacher_id>`
- [] Given the page is viewed on mobile, When the page renders, Then all text is readable (minimum 16px font size) and buttons are touch-friendly (minimum 44px height)
- [] Given the page is viewed on desktop, When the page renders, Then the primary color (#2563EB) is used for headings and primary buttons, and secondary color (#10B981) is used for rates and secondary accents
- [] Given Font Awesome icons are used, When the page renders, Then icons appear correctly for buttons (student: fa-user-graduate, teacher: fa-chalkboard-user, search: fa-search, location: fa-map-marker-alt, subject: fa-book, rating: fa-star)
- [] Given the landing page is accessed, When the page loads, Then no authentication is required and the page is publicly accessible