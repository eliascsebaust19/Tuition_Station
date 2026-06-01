package com.tuitionstation.app

import android.content.Intent
import android.os.Bundle
import android.view.MenuItem
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.tuitionstation.app.admin.AdminDashboardActivity
import com.tuitionstation.app.auth.LoginActivity
import com.tuitionstation.app.auth.TokenManager
import com.tuitionstation.app.chat.ChatActivity
import com.tuitionstation.app.student.SearchTutorsActivity
import com.tuitionstation.app.student.StudentDashboardFragment
import com.tuitionstation.app.teacher.TeacherDashboardFragment

class MainActivity : AppCompatActivity() {
    private lateinit var bottomNav: BottomNavigationView
    private lateinit var toolbarTitle: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        if (!TokenManager.isLoggedIn()) {
            startActivity(Intent(this, LoginActivity::class.java))
            finish()
            return
        }

        bottomNav = findViewById(R.id.bottom_navigation)
        toolbarTitle = findViewById(R.id.toolbar_title)

        val role = TokenManager.getUserRole()
        setupNavigation(role)

        bottomNav.setOnItemSelectedListener { item ->
            handleNavigation(item.itemId, role)
            true
        }
    }

    private fun setupNavigation(role: String?) {
        val menu = bottomNav.menu
        menu.clear()

        when (role) {
            "student" -> {
                bottomNav.inflateMenu(R.menu.menu_student_bottom_nav)
                toolbarTitle.text = "TuitionStation"
                loadFragment(StudentDashboardFragment())
            }
            "teacher" -> {
                bottomNav.inflateMenu(R.menu.menu_teacher_bottom_nav)
                toolbarTitle.text = "Teacher Dashboard"
                loadFragment(TeacherDashboardFragment())
            }
            "admin" -> {
                toolbarTitle.text = "Admin Panel"
                startActivity(Intent(this, AdminDashboardActivity::class.java))
                finish()
            }
        }
    }

    private fun handleNavigation(itemId: Int, role: String?) {
        when (itemId) {
            R.id.nav_dashboard -> {
                toolbarTitle.text = if (role == "student") "TuitionStation" else "Teacher Dashboard"
                loadFragment(
                    if (role == "student") StudentDashboardFragment()
                    else TeacherDashboardFragment()
                )
            }
            R.id.nav_search -> {
                startActivity(Intent(this, SearchTutorsActivity::class.java))
            }
            R.id.nav_messages -> {
                startActivity(Intent(this, ChatActivity::class.java))
            }
            R.id.nav_profile -> {
                TokenManager.logout()
                startActivity(Intent(this, LoginActivity::class.java))
                finish()
            }
        }
    }

    private fun loadFragment(fragment: Fragment) {
        supportFragmentManager.beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commit()
    }
}
