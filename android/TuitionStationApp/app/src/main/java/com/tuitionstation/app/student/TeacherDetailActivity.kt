package com.tuitionstation.app.student

import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.tuitionstation.app.R
import com.tuitionstation.app.api.ApiClient
import com.tuitionstation.app.common.loadProfilePicture
import com.tuitionstation.app.common.showToast
import kotlinx.coroutines.*

class TeacherDetailActivity : AppCompatActivity() {
    private lateinit var nameText: TextView
    private lateinit var subjectText: TextView
    private lateinit var feeText: TextView
    private lateinit var locationText: TextView
    private lateinit var ratingText: TextView
    private lateinit var bioText: TextView
    private lateinit var experienceText: TextView
    private lateinit var uniText: TextView
    private lateinit var degreeText: TextView
    private lateinit var availabilityText: TextView
    private lateinit var saveButton: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var scrollContent: ScrollView
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())
    private var teacherId: Int = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_teacher_detail)

        teacherId = intent.getIntExtra("teacher_id", 0)
        if (teacherId == 0) { finish(); return }

        nameText = findViewById(R.id.teacher_name)
        subjectText = findViewById(R.id.teacher_subject)
        feeText = findViewById(R.id.teacher_fee)
        locationText = findViewById(R.id.teacher_location)
        ratingText = findViewById(R.id.teacher_rating)
        bioText = findViewById(R.id.teacher_bio)
        experienceText = findViewById(R.id.teacher_experience)
        uniText = findViewById(R.id.teacher_university)
        degreeText = findViewById(R.id.teacher_degree)
        availabilityText = findViewById(R.id.teacher_availability)
        saveButton = findViewById(R.id.save_button)
        progressBar = findViewById(R.id.progress_bar)
        scrollContent = findViewById(R.id.scroll_content)

        loadTeacherDetail()

        saveButton.setOnClickListener { toggleSave() }
    }

    private fun loadTeacherDetail() {
        progressBar.visibility = android.view.View.VISIBLE
        scope.launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    ApiClient.apiService.getTeacherDetail(teacherId)
                }
                if (response.isSuccessful && response.body()?.success == true) {
                    val data = response.body()!!.data!!
                    nameText.text = data.user.name
                    subjectText.text = data.profile?.subject ?: "General"
                    feeText.text = "BDT ${data.profile?.fee ?: 0}/mo"
                    locationText.text = data.profile?.location ?: ""
                    ratingText.text = "${data.avgRating ?: 0.0} (${data.reviewCount ?: 0} reviews)"
                    bioText.text = data.profile?.bio ?: "No bio available"
                    experienceText.text = "${data.profile?.experience ?: 0} years"
                    uniText.text = data.profile?.university ?: "N/A"
                    degreeText.text = data.profile?.degree ?: "N/A"
                    availabilityText.text = data.profile?.availability ?: "Available"
                    scrollContent.visibility = android.view.View.VISIBLE
                } else {
                    showToast("Teacher not found")
                }
            } catch (e: Exception) {
                showToast("Network error")
            } finally {
                progressBar.visibility = android.view.View.GONE
            }
        }
    }

    private fun toggleSave() {
        scope.launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    ApiClient.apiService.saveTutor(mapOf("teacher_id" to teacherId))
                }
                if (response.isSuccessful) {
                    showToast("Teacher saved!")
                    saveButton.text = "Saved"
                    saveButton.isEnabled = false
                } else {
                    showToast(response.body()?.error ?: "Failed to save")
                }
            } catch (e: Exception) {
                showToast("Network error")
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
