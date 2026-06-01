package com.tuitionstation.app.api

import retrofit2.Response
import retrofit2.http.*

interface ApiService {
    @POST("auth/login")
    suspend fun login(@Body body: Map<String, String>): Response<ApiResponse<AuthData>>

    @POST("auth/register")
    suspend fun register(@Body body: Map<String, String>): Response<ApiResponse<AuthData>>

    @POST("auth/google")
    suspend fun googleLogin(@Body body: Map<String, String>): Response<ApiResponse<AuthData>>

    @GET("auth/me")
    suspend fun getMe(): Response<ApiResponse<UserData>>

    @GET("featured-teachers")
    suspend fun getFeaturedTeachers(): Response<ApiResponse<List<TeacherListItem>>>

    @GET("students/search")
    suspend fun searchTutors(
        @Query("q") query: String? = null,
        @Query("subject") subject: String? = null,
        @Query("location") location: String? = null,
        @Query("min_fee") minFee: Int? = null,
        @Query("max_fee") maxFee: Int? = null,
        @Query("page") page: Int? = null
    ): Response<ApiResponse<List<TeacherListItem>>>

    @GET("teachers/{id}")
    suspend fun getTeacherDetail(@Path("id") teacherId: Int): Response<ApiResponse<TeacherDetailData>>

    @GET("students/tuition-posts")
    suspend fun getMyPosts(): Response<ApiResponse<List<TuitionPostData>>>

    @POST("students/tuition-posts")
    suspend fun createPost(@Body body: Map<String, Any?>): Response<ApiResponse<TuitionPostData>>

    @GET("students/saved-tutors")
    suspend fun getSavedTutors(): Response<ApiResponse<List<SavedTutorData>>>

    @POST("students/saved-tutors")
    suspend fun saveTutor(@Body body: Map<String, Int>): Response<ApiResponse<SavedTutorData>>

    @HTTP(method = "DELETE", path = "students/saved-tutors", hasBody = true)
    suspend fun unsaveTutor(@Body body: Map<String, Int>): Response<ApiResponse<Any>>

    @GET("reviews")
    suspend fun getReviews(@Query("teacher_id") teacherId: Int?): Response<ApiResponse<List<ReviewData>>>

    @POST("reviews")
    suspend fun createReview(@Body body: Map<String, Any?>): Response<ApiResponse<ReviewData>>

    @GET("teacher/dashboard")
    suspend fun getTeacherDashboard(): Response<ApiResponse<TeacherDashboardData>>

    @GET("teacher/profile")
    suspend fun getTeacherProfile(): Response<ApiResponse<UserData>>

    @PUT("teacher/profile")
    suspend fun updateTeacherProfile(@Body body: Map<String, Any?>): Response<ApiResponse<TeacherProfileData>>

    @GET("teacher/applications")
    suspend fun getTeacherApplications(@Query("status") status: String? = null): Response<ApiResponse<List<ApplicationData>>>

    @GET("teacher/browse-posts")
    suspend fun browsePosts(@Query("subject") subject: String? = null): Response<ApiResponse<List<TuitionPostData>>>

    @POST("teacher/apply")
    suspend fun applyToPost(@Body body: Map<String, Any?>): Response<ApiResponse<Any>>

    @GET("teacher/analytics")
    suspend fun getTeacherAnalytics(): Response<ApiResponse<TeacherStats>>

    @GET("admin/dashboard")
    suspend fun getAdminDashboard(): Response<ApiResponse<AdminDashboardData>>

    @GET("admin/users")
    suspend fun getAdminUsers(@Query("role") role: String? = null): Response<ApiResponse<List<UserData>>>

    @POST("admin/users/{id}/approve")
    suspend fun approveUser(@Path("id") userId: Int): Response<ApiResponse<Any>>

    @POST("admin/users/{id}/toggle-status")
    suspend fun toggleUserStatus(@Path("id") userId: Int): Response<ApiResponse<Any>>

    @GET("admin/payments")
    suspend fun getPayments(@Query("status") status: String? = null): Response<ApiResponse<List<PaymentData>>>

    @POST("admin/payments/{id}/verify")
    suspend fun verifyPayment(@Path("id") paymentId: Int): Response<ApiResponse<Any>>

    @GET("chat/conversations")
    suspend fun getConversations(): Response<ApiResponse<List<ConversationData>>>

    @GET("chat/messages/{id}")
    suspend fun getMessages(@Path("id") otherUserId: Int): Response<ApiResponse<List<MessageData>>>

    @POST("chat/messages/{id}")
    suspend fun sendMessage(@Path("id") otherUserId: Int, @Body body: Map<String, String>): Response<ApiResponse<MessageData>>

    @GET("notifications")
    suspend fun getNotifications(): Response<ApiResponse<List<NotificationData>>>

    @POST("notifications/{id}/read")
    suspend fun markNotificationRead(@Path("id") notifId: Int): Response<ApiResponse<Any>>

    @GET("subscriptions/plans")
    suspend fun getPlans(): Response<ApiResponse<List<SubscriptionPlanData>>>

    @GET("subscriptions/my")
    suspend fun getMySubscription(): Response<ApiResponse<SubscriptionInfo>>

    @GET("payments")
    suspend fun getPaymentHistory(): Response<ApiResponse<List<PaymentData>>>

    @POST("payments")
    suspend fun submitPayment(@Body body: Map<String, Any?>): Response<ApiResponse<PaymentData>>

    @GET("todos")
    suspend fun getTodos(): Response<ApiResponse<List<TodoData>>>

    @POST("todos")
    suspend fun createTodo(@Body body: Map<String, String>): Response<ApiResponse<TodoData>>

    @PUT("todos/{id}")
    suspend fun updateTodo(@Path("id") todoId: Int, @Body body: Map<String, Any?>): Response<ApiResponse<Any>>

    @DELETE("todos/{id}")
    suspend fun deleteTodo(@Path("id") todoId: Int): Response<ApiResponse<Any>>
}
