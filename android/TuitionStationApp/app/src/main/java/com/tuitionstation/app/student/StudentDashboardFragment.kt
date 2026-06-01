package com.tuitionstation.app.student

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.fragment.app.Fragment
import com.tuitionstation.app.R
import com.tuitionstation.app.api.ApiClient
import com.tuitionstation.app.api.TeacherListItem
import com.tuitionstation.app.auth.TokenManager
import com.tuitionstation.app.common.loadProfilePicture
import com.tuitionstation.app.common.showToast
import kotlinx.coroutines.*

class StudentDashboardFragment : Fragment() {
    private lateinit var greetingText: TextView
    private lateinit var featuredContainer: LinearLayout
    private lateinit var progressBar: ProgressBar
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        return inflater.inflate(R.layout.fragment_student_dashboard, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        greetingText = view.findViewById(R.id.greeting_text)
        featuredContainer = view.findViewById(R.id.featured_container)
        progressBar = view.findViewById(R.id.progress_bar)

        val name = TokenManager.getUserName()
        greetingText.text = "Welcome, $name!"

        loadFeaturedTeachers()
    }

    private fun loadFeaturedTeachers() {
        progressBar.visibility = View.VISIBLE
        scope.launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    ApiClient.apiService.getFeaturedTeachers()
                }
                if (response.isSuccessful && response.body()?.success == true) {
                    val teachers = response.body()!!.data ?: emptyList()
                    featuredContainer.removeAllViews()
                    if (teachers.isEmpty()) {
                        featuredContainer.addView(createEmptyView("No featured teachers available"))
                    } else {
                        teachers.forEach { teacher ->
                            featuredContainer.addView(createTeacherCard(teacher))
                        }
                    }
                }
            } catch (e: Exception) {
                featuredContainer.removeAllViews()
                featuredContainer.addView(createEmptyView("Network error"))
            } finally {
                progressBar.visibility = View.GONE
            }
        }
    }

    private fun createTeacherCard(teacher: TeacherListItem): View {
        val card = LayoutInflater.from(context).inflate(R.layout.item_teacher_card, featuredContainer, false)
        card.findViewById<TextView>(R.id.teacher_name).text = teacher.user.name
        card.findViewById<TextView>(R.id.teacher_subject).text = teacher.profile?.subject ?: "General"
        card.findViewById<TextView>(R.id.teacher_fee).text = "BDT ${teacher.profile?.fee ?: 0}/mo"
        card.findViewById<TextView>(R.id.teacher_location).text = teacher.profile?.location ?: ""
        card.findViewById<TextView>(R.id.teacher_rating).text = "${teacher.avgRating ?: 0.0}"

        val badge = card.findViewById<ImageView>(R.id.verified_badge)
        badge.visibility = if (teacher.verified == true) View.VISIBLE else View.GONE

        card.setOnClickListener {
            val intent = Intent(context, TeacherDetailActivity::class.java)
            intent.putExtra("teacher_id", teacher.user.id)
            startActivity(intent)
        }
        return card
    }

    private fun createEmptyView(message: String): TextView {
        val tv = TextView(context)
        tv.text = message
        tv.gravity = android.view.Gravity.CENTER
        tv.setTextColor(resources.getColor(android.R.color.darker_gray, null))
        tv.textSize = 16f
        tv.setPadding(0, 48, 0, 48)
        return tv
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
