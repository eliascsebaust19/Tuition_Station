package com.tuitionstation.app.teacher

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.fragment.app.Fragment
import com.tuitionstation.app.R
import com.tuitionstation.app.api.ApiClient
import com.tuitionstation.app.auth.TokenManager
import com.tuitionstation.app.common.showToast
import kotlinx.coroutines.*

class TeacherDashboardFragment : Fragment() {
    private lateinit var nameText: TextView
    private lateinit var planText: TextView
    private lateinit var daysText: TextView
    private lateinit var totalAppsText: TextView
    private lateinit var pendingAppsText: TextView
    private lateinit var acceptedAppsText: TextView
    private lateinit var ratingText: TextView
    private lateinit var openPostsText: TextView
    private lateinit var messagesText: TextView
    private lateinit var editProfileButton: Button
    private lateinit var browsePostsButton: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var contentLayout: LinearLayout
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        return inflater.inflate(R.layout.fragment_teacher_dashboard, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        nameText = view.findViewById(R.id.teacher_name)
        planText = view.findViewById(R.id.plan_text)
        daysText = view.findViewById(R.id.days_text)
        totalAppsText = view.findViewById(R.id.total_apps)
        pendingAppsText = view.findViewById(R.id.pending_apps)
        acceptedAppsText = view.findViewById(R.id.accepted_apps)
        ratingText = view.findViewById(R.id.rating_text)
        openPostsText = view.findViewById(R.id.open_posts)
        messagesText = view.findViewById(R.id.messages_text)
        editProfileButton = view.findViewById(R.id.edit_profile_button)
        browsePostsButton = view.findViewById(R.id.browse_posts_button)
        progressBar = view.findViewById(R.id.progress_bar)
        contentLayout = view.findViewById(R.id.content_layout)

        editProfileButton.setOnClickListener {
            startActivity(Intent(context, EditProfileActivity::class.java))
        }

        loadDashboard()
    }

    private fun loadDashboard() {
        progressBar.visibility = View.VISIBLE
        scope.launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    ApiClient.apiService.getTeacherDashboard()
                }
                if (response.isSuccessful && response.body()?.success == true) {
                    val data = response.body()!!.data!!
                    val stats = data.stats
                    val sub = data.subscription

                    nameText.text = "Welcome, ${data.user.name}"
                    planText.text = "Plan: ${sub?.planName ?: "Free"}"
                    daysText.text = "${sub?.daysRemaining ?: 0} days remaining"

                    totalAppsText.text = "${stats?.totalApplications ?: 0}"
                    pendingAppsText.text = "${stats?.pendingApplications ?: 0}"
                    acceptedAppsText.text = "${stats?.acceptedApplications ?: 0}"
                    ratingText.text = "${stats?.avgRating ?: 0.0} (${stats?.reviewCount ?: 0})"
                    openPostsText.text = "${stats?.openPosts ?: 0}"
                    messagesText.text = "${stats?.totalMessages ?: 0}"

                    contentLayout.visibility = View.VISIBLE
                } else {
                    requireContext().showToast("Failed to load dashboard")
                }
            } catch (e: Exception) {
                requireContext().showToast("Network error")
            } finally {
                progressBar.visibility = View.GONE
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
