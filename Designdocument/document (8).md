# Teacher Data Model & Database Schema

## Overview
This requirement defines the complete data model for teacher profiles in the tuition marketplace. The schema supports teacher discovery, profile management, scheduling, and student reviews while maintaining data integrity through proper normalization and relationships.

## Problem Statement
The tuition marketplace needs a robust data structure to store and retrieve teacher information efficiently. Without a well-designed schema, the system cannot support core features like teacher discovery, availability management, pricing flexibility, and student reviews.

## Solution
Create a normalized relational data model with seven core entities: Teachers, Subjects, Qualifications, TeacherQualifications, Pricing, Availability, and Reviews. This structure supports flexible teacher profiles while maintaining referential integrity and query performance.

---

## Data Model Specification

### Entity: Teacher (new)
Core teacher profile entity containing personal and professional information.

**Fields:**
- teacher_id (UUID, primary key): Unique identifier for each teacher
- first_name (string, max 100): Teacher's first name
- last_name (string, max 100): Teacher's last name
- email (string, unique, max 255): Teacher's email address
- phone (string, max 20): Contact phone number
- bio (text): Professional biography and teaching philosophy
- profile_image_url (string, max 500): URL to teacher's profile photo
- years_of_experience (integer, min 0): Total years teaching experience
- is_verified (boolean, default false): Verification status for credentials
- verification_date (timestamp, nullable): When teacher was verified
- hourly_rate_min (decimal, precision 10,2, min 0): Minimum hourly rate in USD
- hourly_rate_max (decimal, precision 10,2, min 0): Maximum hourly rate in USD
- monthly_rate (decimal, precision 10,2, min 0, nullable): Monthly subscription rate if offered
- service_radius_km (integer, min 0): Radius of service area in kilometers
- latitude (decimal, precision 10,8, nullable): Service area center latitude
- longitude (decimal, precision 10,8, nullable): Service area center longitude
- address_line1 (string, max 255, nullable): Street address
- address_line2 (string, max 255, nullable): Apartment/suite number
- city (string, max 100, nullable): City name
- state_province (string, max 100, nullable): State or province
- postal_code (string, max 20, nullable): Postal code
- country (string, max 100, nullable): Country name
- average_rating (decimal, precision 3,2, default 0, range 0-5): Average student rating
- total_reviews (integer, default 0): Total number of reviews
- total_students_taught (integer, default 0): Cumulative student count
- is_active (boolean, default true): Account active status
- created_at (timestamp): Account creation timestamp
- updated_at (timestamp): Last profile update timestamp

---

### Entity: Subject (new)
Subjects and specializations offered by teachers.

**Fields:**
- subject_id (UUID, primary key): Unique identifier for subject
- name (string, unique, max 100): Subject name (e.g., "Mathematics", "English Literature")
- category (string, max 50): Subject category (e.g., "STEM", "Languages", "Arts")
- description (text, nullable): Subject description
- is_active (boolean, default true): Whether subject is available for selection
- created_at (timestamp): Record creation timestamp

---

### Entity: Qualification (new)
Educational credentials and certifications.

**Fields:**
- qualification_id (UUID, primary key): Unique identifier for qualification type
- name (string, unique, max 150): Qualification name (e.g., "Bachelor of Science in Mathematics")
- issuing_body (string, max 150): Organization that issued credential
- qualification_type (enum: 'degree', 'certification', 'license', 'other'): Type of credential
- description (text, nullable): Qualification details
- is_verified_credential (boolean, default false): Whether this credential type requires verification
- created_at (timestamp): Record creation timestamp

---

### Entity: TeacherQualification (new)
Junction table linking teachers to their qualifications.

**Fields:**
- teacher_qualification_id (UUID, primary key): Unique identifier
- teacher_id (UUID, foreign key → Teacher.teacher_id): Reference to teacher
- qualification_id (UUID, foreign key → Qualification.qualification_id): Reference to qualification
- issue_date (date): When credential was issued
- expiry_date (date, nullable): When credential expires (null if no expiry)
- credential_number (string, max 100, nullable): License/credential number
- issuing_institution (string, max 255, nullable): Specific institution that issued credential
- verification_status (enum: 'unverified', 'pending', 'verified', 'rejected', default 'unverified'): Verification state
- verification_date (timestamp, nullable): When credential was verified
- verified_by_admin_id (UUID, nullable, foreign key → Admin.admin_id): Admin who verified
- document_url (string, max 500, nullable): URL to credential document
- created_at (timestamp): Record creation timestamp
- updated_at (timestamp): Last update timestamp

---

### Entity: TeacherSubject (new)
Junction table linking teachers to subjects they teach.

**Fields:**
- teacher_subject_id (UUID, primary key): Unique identifier
- teacher_id (UUID, foreign key → Teacher.teacher_id): Reference to teacher
- subject_id (UUID, foreign key → Subject.subject_id): Reference to subject
- proficiency_level (enum: 'beginner', 'intermediate', 'advanced', 'expert', default 'intermediate'): Teaching expertise level
- years_teaching_subject (integer, min 0): Years of experience teaching this subject
- is_primary_subject (boolean, default false): Whether this is teacher's primary subject
- created_at (timestamp): Record creation timestamp

---

### Entity: Pricing (new)
Flexible pricing structure for teachers.

**Fields:**
- pricing_id (UUID, primary key): Unique identifier
- teacher_id (UUID, foreign key → Teacher.teacher_id, unique): Reference to teacher
- hourly_rate (decimal, precision 10,2, min 0): Hourly rate in USD
- monthly_rate (decimal, precision 10,2, min 0, nullable): Monthly subscription rate
- monthly_hours_included (integer, min 0, nullable): Hours included in monthly rate
- trial_session_rate (decimal, precision 10,2, min 0, nullable): Discounted first session rate
- group_session_rate (decimal, precision 10,2, min 0, nullable): Rate for group sessions
- group_session_min_students (integer, min 2, nullable): Minimum students for group rate
- currency (string, default 'USD', max 3): Currency code
- is_negotiable (boolean, default false): Whether rates are negotiable
- created_at (timestamp): Record creation timestamp
- updated_at (timestamp): Last update timestamp

---

### Entity: Availability (new)
Teacher availability slots for scheduling.

**Fields:**
- availability_id (UUID, primary key): Unique identifier
- teacher_id (UUID, foreign key → Teacher.teacher_id): Reference to teacher
- day_of_week (enum: 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'): Day of week
- start_time (time): Session start time (HH:MM format)
- end_time (time): Session end time (HH:MM format)
- timezone (string, max 50): IANA timezone identifier (e.g., "America/New_York")
- is_recurring (boolean, default true): Whether this is a recurring slot
- recurrence_end_date (date, nullable): When recurring availability ends
- is_available (boolean, default true): Whether slot is currently available
- created_at (timestamp): Record creation timestamp
- updated_at (timestamp): Last update timestamp

---

### Entity: Review (new)
Student reviews and ratings for teachers.

**Fields:**
- review_id (UUID, primary key): Unique identifier
- teacher_id (UUID, foreign key → Teacher.teacher_id): Reference to teacher
- student_id (UUID, foreign key → Student.student_id): Reference to student
- booking_id (UUID, foreign key → Booking.booking_id, nullable): Reference to completed session
- rating (integer, min 1, max 5): Numerical rating (1-5 stars)
- title (string, max 100, nullable): Review title
- comment (text, nullable): Detailed review text
- teaching_quality (integer, min 1, max 5, nullable): Teaching quality rating
- communication (integer, min 1, max 5, nullable): Communication rating
- punctuality (integer, min 1, max 5, nullable): Punctuality rating
- is_verified_purchase (boolean, default false): Whether reviewer completed a session
- is_helpful_count (integer, default 0): Number of users who found review helpful
- is_flagged (boolean, default false): Whether review is flagged for moderation
- flagged_reason (string, max 255, nullable): Reason for flagging
- created_at (timestamp): Record creation timestamp
- updated_at (timestamp): Last update timestamp

---

## Relationships

| From          | To                   | Type         | Cardinality   | Description                              |
| ------------- | -------------------- | ------------ | ------------- | ---------------------------------------- |
| Teacher       | Subject              | Many-to-Many | N:M           | Via TeacherSubject junction table        |
| Teacher       | Qualification        | Many-to-Many | N:M           | Via TeacherQualification junction table  |
| Teacher       | Pricing              | One-to-One   | 1:1           | Each teacher has one pricing record      |
| Teacher       | Availability         | One-to-Many  | 1:N           | Teacher has multiple availability slots  |
| Teacher       | Review               | One-to-Many  | 1:N           | Teacher receives multiple reviews        |
| Review        | Student              | Many-to-One  | N:1           | Multiple reviews from different students |
| Qualification | TeacherQualification | One-to-Many  | 1:N           | Qualification held by multiple teachers  |
| Subject       | TeacherSubject       | One-to-Many  | 1:N           | Subject taught by multiple teachers      |

---

## Data Integrity Rules

**Teacher Entity:**
- `email` must be unique across all teachers
- `hourly_rate_max` must be ≥ `hourly_rate_min`
- `years_of_experience` cannot be negative
- `average_rating` must be between 0 and 5
- `latitude` and `longitude` must both be provided or both null
- `is_verified` can only be set to true by admin verification process
- `service_radius_km` must be ≥ 0

**TeacherQualification Entity:**
- `expiry_date` must be null or ≥ `issue_date`
- `verification_status` can only transition from 'unverified' → 'pending' → ('verified' or 'rejected')
- `verified_by_admin_id` must be populated when `verification_status` = 'verified'
- `verification_date` must be populated when `verification_status` = 'verified'

**Pricing Entity:**
- `hourly_rate` must be > 0
- `monthly_rate` must be null or > 0
- `trial_session_rate` must be null or > 0
- `group_session_rate` must be null or > 0
- `group_session_min_students` must be null or ≥ 2

**Availability Entity:**
- `end_time` must be > `start_time`
- `recurrence_end_date` must be null or ≥ current date
- `timezone` must be valid IANA timezone identifier

**Review Entity:**
- `rating` must be between 1 and 5
- `teaching_quality`, `communication`, `punctuality` must be null or between 1 and 5
- `is_helpful_count` cannot be negative
- `flagged_reason` must be populated when `is_flagged` = true

---

## Indexes for Performance

| Entity               | Index Name                 | Columns                                 | Type      | Purpose                                  |
| -------------------- | -------------------------- | --------------------------------------- | --------- | ---------------------------------------- |
| Teacher              | idx_teacher_email          | email                                   | Unique    | Fast email lookups for authentication    |
| Teacher              | idx_teacher_active         | is_active, created_at                   | Composite | Filter active teachers, sort by newest   |
| Teacher              | idx_teacher_location       | latitude, longitude, service_radius_km  | Composite | Geographic queries for teacher discovery |
| Teacher              | idx_teacher_rating         | average_rating DESC, total_reviews DESC | Composite | Sort teachers by rating and review count |
| TeacherSubject       | idx_teacher_subject_lookup | teacher_id, subject_id                  | Composite | Find subjects for a teacher              |
| TeacherSubject       | idx_subject_teachers       | subject_id, teacher_id                  | Composite | Find teachers for a subject              |
| TeacherQualification | idx_teacher_qualifications | teacher_id, verification_status         | Composite | Find verified credentials for teacher    |
| Pricing              | idx_pricing_teacher        | teacher_id                              | Unique    | Fast pricing lookups                     |
| Availability         | idx_availability_teacher   | teacher_id, day_of_week, is_available   | Composite | Find available slots for teacher         |
| Review               | idx_review_teacher         | teacher_id, created_at DESC             | Composite | Retrieve recent reviews for teacher      |
| Review               | idx_review_rating          | teacher_id, rating                      | Composite | Filter reviews by rating                 |
| Subject              | idx_subject_active         | is_active, name                         | Composite | List active subjects for UI dropdowns    |

---

## Normalization & Design Decisions

**Third Normal Form (3NF) Compliance:**
- All entities have atomic fields (no multi-valued attributes)
- Non-key attributes depend only on primary keys
- No transitive dependencies between non-key attributes
- Junction tables (TeacherSubject, TeacherQualification) eliminate many-to-many redundancy

**Denormalization Decisions:**
- `Teacher.average_rating` and `Teacher.total_reviews` are denormalized from Review entity for fast discovery queries. These must be updated via triggers or application logic whenever reviews are added/modified.
- `Teacher.total_students_taught` is denormalized from Booking entity for profile display. Updated via application logic.

**Field Type Rationale:**
- UUIDs for primary keys enable distributed generation and prevent ID enumeration attacks
- Decimal(10,2) for currency fields ensures accurate financial calculations
- Enum types for fixed-value fields (day_of_week, verification_status) prevent invalid data
- Timestamp fields (created_at, updated_at) enable audit trails and sorting
- Text fields for bio and comments support variable-length content

**Scalability Considerations:**
- Availability slots use day_of_week + time instead of individual datetime records to reduce storage and support recurring patterns
- Review pagination via created_at index prevents full-table scans
- Geographic queries use indexed latitude/longitude for efficient location-based discovery
- Separate Pricing entity allows future rate variations without modifying Teacher record

---

## Integration Points

**Teacher Discovery System:**
- Query: Find teachers by subject, location, rating, availability
- Uses: TeacherSubject, Teacher (location + rating indexes), Availability
- Performance: Composite indexes on subject_id, location, rating enable efficient filtering

**Profile Display System:**
- Query: Retrieve complete teacher profile with qualifications, subjects, reviews
- Uses: Teacher, TeacherQualification, TeacherSubject, Review, Pricing
- Performance: Single teacher_id lookup returns all related data via foreign keys

**Scheduling System:**
- Query: Check teacher availability and create bookings
- Uses: Availability, Pricing, Booking (external)
- Performance: Indexed availability queries by teacher_id + day_of_week + is_available

**Review & Rating System:**
- Query: Add review, update teacher average_rating and total_reviews
- Uses: Review, Teacher (denormalized fields)
- Performance: Trigger or application logic updates Teacher.average_rating after each review

---

## Out of Scope

**Features Deferred:**
- **Booking & Session Management** - Separate Booking entity and session tracking system will be defined in a future requirement
- **Payment & Billing** - Payment processing, invoicing, and transaction history are out of scope for this data model
- **Admin Verification Workflow** - Admin interface for credential verification will be defined separately
- **Messaging & Communication** - Student-teacher messaging system is a separate feature
- **Performance Optimization** - Query optimization, caching strategy, and database tuning will be addressed during implementation

---

## Acceptance Criteria

- [] Given a teacher profile is created, When all required fields are populated, Then the teacher record is persisted with valid data types and constraints enforced
- [] Given a teacher has multiple qualifications, When qualifications are added via TeacherQualification, Then each qualification is linked with verification status and dates tracked
- [] Given a teacher teaches multiple subjects, When subjects are added via TeacherSubject, Then each subject is linked with proficiency level and years of experience recorded
- [] Given a teacher has availability slots, When slots are queried by day_of_week and timezone, Then results are returned efficiently using composite indexes
- [] Given a student submits a review, When the review is created, Then the teacher's average_rating and total_reviews are updated and queryable within 1 second
- [] Given a teacher's location is updated, When geographic queries are executed, Then teachers within service_radius_km are returned using indexed latitude/longitude
- [] Given multiple teachers are filtered by subject, rating, and availability, When discovery queries execute, Then results are returned in under 500ms using composite indexes
- [] Given a teacher's pricing is updated, When the Pricing record is modified, Then the change is reflected in new bookings without affecting existing bookings
- [] Given a teacher's credentials are verified, When verification_status is set to 'verified', Then verified_by_admin_id and verification_date are populated and is_verified on Teacher is updated
- [] Given a teacher has no reviews, When the profile is displayed, Then average_rating defaults to 0 and total_reviews displays as 0
- [] Given a qualification has an expiry_date, When the date is reached, Then the system can identify expired credentials for renewal prompts
- [] Given availability slots are marked as recurring, When recurrence_end_date is reached, Then slots are no longer available for new bookings
- [] Given a review is flagged for moderation, When is_flagged is set to true, Then flagged_reason is required and the review is excluded from average_rating calculation
- [] Given the data model is implemented, When all indexes are created, Then teacher discovery queries execute with composite index usage confirmed in query plans