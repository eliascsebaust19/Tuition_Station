package com.tuitionstation.app.api

import com.google.gson.annotations.SerializedName

data class ApiResponse<T>(
    val success: Boolean,
    val data: T?,
    val error: String?,
    val total: Int?,
    val page: Int?,
    @SerializedName("per_page") val perPage: Int?
)

data class UserData(
    val id: Int,
    val name: String,
    val email: String,
    val role: String,
    @SerializedName("is_active") val isActive: Boolean,
    @SerializedName("is_approved") val isApproved: Boolean,
    @SerializedName("profile_picture") val profilePicture: String?,
    @SerializedName("created_at") val createdAt: String?,
    val profile: TeacherProfileData?,
    val subscription: SubscriptionInfo?,
    @SerializedName("application_count") val applicationCount: Int?,
    @SerializedName("post_count") val postCount: Int?,
    @SerializedName("unread_messages") val unreadMessages: Int?,
    @SerializedName("unread_notifications") val unreadNotifications: Int?
)

data class AuthData(
    val token: String,
    val user: UserData
)

data class TeacherProfileData(
    val id: Int?,
    @SerializedName("user_id") val userId: Int?,
    val university: String?,
    val department: String?,
    val degree: String?,
    val subject: String?,
    val experience: Int?,
    val fee: Int?,
    @SerializedName("hourly_fee") val hourlyFee: Int?,
    val location: String?,
    val bio: String?,
    val availability: String?,
    @SerializedName("is_complete") val isComplete: Boolean?,
    @SerializedName("teaching_mode") val teachingMode: String?,
    val qualification: String?,
    @SerializedName("subjects_expert_in") val subjectsExpertIn: String?,
    @SerializedName("class_level") val classLevel: String?,
    @SerializedName("teaching_areas") val teachingAreas: String?,
    val languages: String?,
    @SerializedName("teaching_style") val teachingStyle: String?,
    @SerializedName("total_students_taught") val totalStudentsTaught: Int?,
    @SerializedName("intro_video_url") val introVideoUrl: String?,
    val cv: String?
)

data class SubscriptionInfo(
    @SerializedName("plan_name") val planName: String?,
    @SerializedName("is_active") val isActive: Boolean?,
    @SerializedName("days_remaining") val daysRemaining: Int?
)

data class TeacherListItem(
    val user: UserData,
    val profile: TeacherProfileData?,
    @SerializedName("avg_rating") val avgRating: Double?,
    @SerializedName("review_count") val reviewCount: Int?,
    val verified: Boolean?,
    val featured: Boolean?
)

data class ReviewData(
    val id: Int,
    val rating: Int,
    val comment: String?,
    @SerializedName("student_name") val studentName: String?,
    @SerializedName("created_at") val createdAt: String?
)

data class TeacherDetailData(
    val user: UserData,
    val profile: TeacherProfileData?,
    @SerializedName("avg_rating") val avgRating: Double?,
    @SerializedName("review_count") val reviewCount: Int?,
    val verified: Boolean?,
    val reviews: List<ReviewData>?
)

data class TuitionPostData(
    val id: Int,
    val title: String,
    val subject: String,
    @SerializedName("class_level") val classLevel: String?,
    val location: String,
    val salary: Int?,
    val status: String?,
    @SerializedName("student_name") val studentName: String?,
    val description: String?,
    @SerializedName("has_applied") val hasApplied: Boolean?,
    @SerializedName("application_count") val applicationCount: Int?,
    @SerializedName("created_at") val createdAt: String?
)

data class ApplicationData(
    val id: Int,
    @SerializedName("post_id") val postId: Int?,
    @SerializedName("post_title") val postTitle: String?,
    @SerializedName("post_subject") val postSubject: String?,
    @SerializedName("post_location") val postLocation: String?,
    @SerializedName("post_salary") val postSalary: Int?,
    @SerializedName("student_name") val studentName: String?,
    val message: String?,
    val status: String?,
    @SerializedName("created_at") val createdAt: String?
)

data class MessageData(
    val id: Int,
    @SerializedName("sender_id") val senderId: Int,
    @SerializedName("receiver_id") val receiverId: Int,
    val message: String,
    @SerializedName("is_read") val isRead: Boolean?,
    @SerializedName("created_at") val createdAt: String?
)

data class ConversationData(
    val user: UserData,
    @SerializedName("last_message") val lastMessage: String?,
    @SerializedName("last_message_time") val lastMessageTime: String?,
    @SerializedName("unread_count") val unreadCount: Int?
)

data class NotificationData(
    val id: Int,
    val type: String?,
    val title: String?,
    val message: String?,
    val link: String?,
    @SerializedName("is_read") val isRead: Boolean?,
    @SerializedName("created_at") val createdAt: String?
)

data class SubscriptionPlanData(
    val id: Int,
    val name: String,
    val price: Double,
    @SerializedName("duration_days") val durationDays: Int,
    @SerializedName("max_applications") val maxApplications: Int?,
    @SerializedName("is_featured") val isFeatured: Boolean?,
    @SerializedName("has_verified_badge") val hasVerifiedBadge: Boolean?,
    @SerializedName("priority_ranking") val priorityRanking: Int?,
    val description: String?
)

data class PaymentData(
    val id: Int,
    @SerializedName("plan_name") val planName: String?,
    val amount: Double,
    val method: String?,
    @SerializedName("transaction_id") val transactionId: String?,
    val status: String?,
    @SerializedName("created_at") val createdAt: String?
)

data class TeacherDashboardData(
    val user: UserData,
    val profile: TeacherProfileData?,
    val stats: TeacherStats?,
    val subscription: SubscriptionInfo?,
    @SerializedName("recent_applications") val recentApplications: List<ApplicationData>?
)

data class TeacherStats(
    @SerializedName("total_applications") val totalApplications: Int?,
    @SerializedName("pending_applications") val pendingApplications: Int?,
    @SerializedName("accepted_applications") val acceptedApplications: Int?,
    @SerializedName("open_posts") val openPosts: Int?,
    @SerializedName("total_messages") val totalMessages: Int?,
    @SerializedName("avg_rating") val avgRating: Double?,
    @SerializedName("review_count") val reviewCount: Int?
)

data class AdminDashboardData(
    @SerializedName("total_users") val totalUsers: Int?,
    @SerializedName("total_teachers") val totalTeachers: Int?,
    @SerializedName("total_students") val totalStudents: Int?,
    @SerializedName("pending_teachers") val pendingTeachers: Int?,
    @SerializedName("total_posts") val totalPosts: Int?,
    @SerializedName("open_posts") val openPosts: Int?,
    @SerializedName("total_payments") val totalPayments: Int?,
    @SerializedName("pending_payments") val pendingPayments: Int?,
    @SerializedName("total_revenue") val totalRevenue: Double?
)

data class SavedTutorData(
    val id: Int,
    val teacher: UserData,
    val profile: TeacherProfileData?,
    @SerializedName("avg_rating") val avgRating: Double?,
    @SerializedName("created_at") val createdAt: String?
)

data class TodoData(
    val id: Int,
    val title: String,
    val description: String?,
    @SerializedName("is_completed") val isCompleted: Boolean?,
    @SerializedName("created_at") val createdAt: String?
)
