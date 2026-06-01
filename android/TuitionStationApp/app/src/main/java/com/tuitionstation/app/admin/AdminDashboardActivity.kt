package com.tuitionstation.app.admin

import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.tuitionstation.app.R
import com.tuitionstation.app.api.ApiClient
import com.tuitionstation.app.auth.TokenManager
import com.tuitionstation.app.common.showToast
import kotlinx.coroutines.*

class AdminDashboardActivity : AppCompatActivity() {
    private lateinit var totalUsersText: TextView
    private lateinit var totalTeachersText: TextView
    private lateinit var totalStudentsText: TextView
    private lateinit var pendingTeachersText: TextView
    private lateinit var totalPostsText: TextView
    private lateinit var openPostsText: TextView
    private lateinit var totalPaymentsText: TextView
    private lateinit var pendingPaymentsText: TextView
    private lateinit var revenueText: TextView
    private lateinit var progressBar: ProgressBar
    private lateinit var logoutButton: Button
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_admin_dashboard)

        totalUsersText = findViewById(R.id.total_users)
        totalTeachersText = findViewById(R.id.total_teachers)
        totalStudentsText = findViewById(R.id.total_students)
        pendingTeachersText = findViewById(R.id.pending_teachers)
        totalPostsText = findViewById(R.id.total_posts)
        openPostsText = findViewById(R.id.open_posts)
        totalPaymentsText = findViewById(R.id.total_payments)
        pendingPaymentsText = findViewById(R.id.pending_payments)
        revenueText = findViewById(R.id.total_revenue)
        progressBar = findViewById(R.id.progress_bar)
        logoutButton = findViewById(R.id.logout_button)

        loadDashboard()

        logoutButton.setOnClickListener {
            TokenManager.logout()
            finishAffinity()
        }
    }

    private fun loadDashboard() {
        progressBar.visibility = android.view.View.VISIBLE
        scope.launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    ApiClient.apiService.getAdminDashboard()
                }
                if (response.isSuccessful && response.body()?.success == true) {
                    val data = response.body()!!.data!!
                    totalUsersText.text = "${data.totalUsers ?: 0}"
                    totalTeachersText.text = "${data.totalTeachers ?: 0}"
                    totalStudentsText.text = "${data.totalStudents ?: 0}"
                    pendingTeachersText.text = "${data.pendingTeachers ?: 0}"
                    totalPostsText.text = "${data.totalPosts ?: 0}"
                    openPostsText.text = "${data.openPosts ?: 0}"
                    totalPaymentsText.text = "${data.totalPayments ?: 0}"
                    pendingPaymentsText.text = "${data.pendingPayments ?: 0}"
                    revenueText.text = "BDT ${data.totalRevenue ?: 0}"
                } else {
                    showToast("Failed to load dashboard")
                }
            } catch (e: Exception) {
                showToast("Network error")
            } finally {
                progressBar.visibility = android.view.View.GONE
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
