package com.tuitionstation.app.teacher

import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.tuitionstation.app.R
import com.tuitionstation.app.api.ApiClient
import com.tuitionstation.app.common.hideKeyboard
import com.tuitionstation.app.common.showToast
import kotlinx.coroutines.*

class EditProfileActivity : AppCompatActivity() {
    private lateinit var subjectInput: EditText
    private lateinit var feeInput: EditText
    private lateinit var locationInput: EditText
    private lateinit var universityInput: EditText
    private lateinit var departmentInput: EditText
    private lateinit var degreeInput: EditText
    private lateinit var experienceInput: EditText
    private lateinit var bioInput: EditText
    private lateinit var saveButton: Button
    private lateinit var progressBar: ProgressBar
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_edit_profile)

        subjectInput = findViewById(R.id.subject_input)
        feeInput = findViewById(R.id.fee_input)
        locationInput = findViewById(R.id.location_input)
        universityInput = findViewById(R.id.university_input)
        departmentInput = findViewById(R.id.department_input)
        degreeInput = findViewById(R.id.degree_input)
        experienceInput = findViewById(R.id.experience_input)
        bioInput = findViewById(R.id.bio_input)
        saveButton = findViewById(R.id.save_button)
        progressBar = findViewById(R.id.progress_bar)

        loadProfile()
        saveButton.setOnClickListener { saveProfile() }
    }

    private fun loadProfile() {
        progressBar.visibility = android.view.View.VISIBLE
        scope.launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    ApiClient.apiService.getTeacherProfile()
                }
                if (response.isSuccessful && response.body()?.success == true) {
                    val data = response.body()!!.data!!
                    val p = data.profile
                    subjectInput.setText(p?.subject ?: "")
                    feeInput.setText(p?.fee?.toString() ?: "")
                    locationInput.setText(p?.location ?: "")
                    universityInput.setText(p?.university ?: "")
                    departmentInput.setText(p?.department ?: "")
                    degreeInput.setText(p?.degree ?: "")
                    experienceInput.setText(p?.experience?.toString() ?: "0")
                    bioInput.setText(p?.bio ?: "")
                }
            } catch (e: Exception) {
                showToast("Network error")
            } finally {
                progressBar.visibility = android.view.View.GONE
            }
        }
    }

    private fun saveProfile() {
        hideKeyboard()
        progressBar.visibility = android.view.View.VISIBLE
        saveButton.isEnabled = false

        scope.launch {
            try {
                val body = mapOf<String, Any?>(
                    Pair("subject", subjectInput.text.toString().trim()),
                    Pair("fee", feeInput.text.toString().toIntOrNull() ?: 0),
                    Pair("location", locationInput.text.toString().trim()),
                    Pair("university", universityInput.text.toString().trim()),
                    Pair("department", departmentInput.text.toString().trim()),
                    Pair("degree", degreeInput.text.toString().trim()),
                    Pair("experience", experienceInput.text.toString().toIntOrNull() ?: 0),
                    Pair("bio", bioInput.text.toString().trim())
                )
                val response = withContext(Dispatchers.IO) {
                    ApiClient.apiService.updateTeacherProfile(body)
                }
                if (response.isSuccessful && response.body()?.success == true) {
                    showToast("Profile updated!")
                    finish()
                } else {
                    showToast(response.body()?.error ?: "Update failed")
                }
            } catch (e: Exception) {
                showToast("Network error")
            } finally {
                progressBar.visibility = android.view.View.GONE
                saveButton.isEnabled = true
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
