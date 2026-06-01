package com.tuitionstation.app.student

import android.content.Intent
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.tuitionstation.app.R
import com.tuitionstation.app.api.ApiClient
import com.tuitionstation.app.api.TeacherListItem
import com.tuitionstation.app.common.showToast
import kotlinx.coroutines.*

class SearchTutorsActivity : AppCompatActivity() {
    private lateinit var searchInput: EditText
    private lateinit var searchButton: ImageButton
    private lateinit var subjectFilter: EditText
    private lateinit var locationFilter: EditText
    private lateinit var minFeeFilter: EditText
    private lateinit var maxFeeFilter: EditText
    private lateinit var applyFilterButton: Button
    private lateinit var recyclerView: RecyclerView
    private lateinit var progressBar: ProgressBar
    private lateinit var emptyText: TextView
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())
    private val adapter = TutorAdapter { teacher -> openTeacherDetail(teacher) }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_search_tutors)

        searchInput = findViewById(R.id.search_input)
        searchButton = findViewById(R.id.search_button)
        subjectFilter = findViewById(R.id.subject_filter)
        locationFilter = findViewById(R.id.location_filter)
        minFeeFilter = findViewById(R.id.min_fee_filter)
        maxFeeFilter = findViewById(R.id.max_fee_filter)
        applyFilterButton = findViewById(R.id.apply_filter_button)
        recyclerView = findViewById(R.id.recycler_view)
        progressBar = findViewById(R.id.progress_bar)
        emptyText = findViewById(R.id.empty_text)

        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = adapter

        searchButton.setOnClickListener { performSearch() }
        applyFilterButton.setOnClickListener { performSearch() }
        searchInput.setOnEditorActionListener { _, _, _ -> performSearch(); true }

        performSearch()
    }

    private fun performSearch() {
        val query = searchInput.text.toString().trim()
        val subject = subjectFilter.text.toString().trim()
        val location = locationFilter.text.toString().trim()
        val minFee = minFeeFilter.text.toString().toIntOrNull()
        val maxFee = maxFeeFilter.text.toString().toIntOrNull()

        progressBar.visibility = android.view.View.VISIBLE
        emptyText.visibility = android.view.View.GONE

        scope.launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    ApiClient.apiService.searchTutors(query, subject, location, minFee, maxFee)
                }
                if (response.isSuccessful && response.body()?.success == true) {
                    val teachers = response.body()!!.data ?: emptyList()
                    adapter.submitList(teachers)
                    emptyText.visibility = if (teachers.isEmpty()) android.view.View.VISIBLE else android.view.View.GONE
                } else {
                    showToast(response.body()?.error ?: "Search failed")
                }
            } catch (e: Exception) {
                showToast("Network error")
            } finally {
                progressBar.visibility = android.view.View.GONE
            }
        }
    }

    private fun openTeacherDetail(teacher: TeacherListItem) {
        val intent = Intent(this, TeacherDetailActivity::class.java)
        intent.putExtra("teacher_id", teacher.user.id)
        intent.putExtra("teacher_name", teacher.user.name)
        startActivity(intent)
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
