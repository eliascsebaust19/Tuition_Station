package com.tuitionstation.app.auth

import android.content.Intent
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.tuitionstation.app.MainActivity
import com.tuitionstation.app.R
import com.tuitionstation.app.api.ApiClient
import com.tuitionstation.app.common.hideKeyboard
import com.tuitionstation.app.common.showToast
import import com.google.gson.Gson
import com.tuitionstation.app.api.ApiResponse
import kotlinx.coroutines.*

class RegisterActivity : AppCompatActivity() {
    private lateinit var nameInput: EditText
    private lateinit var emailInput: EditText
    private lateinit var passwordInput: EditText
    private lateinit var confirmInput: EditText
    private lateinit var roleGroup: RadioGroup
    private lateinit var registerButton: Button
    private lateinit var loginLink: TextView
    private lateinit var progressBar: ProgressBar
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)

        nameInput = findViewById(R.id.name_input)
        emailInput = findViewById(R.id.email_input)
        passwordInput = findViewById(R.id.password_input)
        confirmInput = findViewById(R.id.confirm_password_input)
        roleGroup = findViewById(R.id.role_group)
        registerButton = findViewById(R.id.register_button)
        loginLink = findViewById(R.id.login_link)
        progressBar = findViewById(R.id.progress_bar)

        registerButton.setOnClickListener { performRegister() }
        loginLink.setOnClickListener {
            startActivity(Intent(this, LoginActivity::class.java))
            finish()
        }
    }

    private fun performRegister() {
        val name = nameInput.text.toString().trim()
        val email = emailInput.text.toString().trim()
        val password = passwordInput.text.toString()
        val confirm = confirmInput.text.toString()
        val selectedRoleId = roleGroup.checkedRadioButtonId
        val role = if (selectedRoleId == R.id.role_teacher) "teacher" else "student"

        if (name.isEmpty()) { nameInput.error = getString(R.string.name_required); return }
        if (email.isEmpty()) { emailInput.error = getString(R.string.email_required); return }
        if (password.length < 6) { passwordInput.error = getString(R.string.password_min); return }
        if (password != confirm) { confirmInput.error = "Passwords do not match"; return }

        hideKeyboard()
        progressBar.visibility = android.view.View.VISIBLE
        registerButton.isEnabled = false

        scope.launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    ApiClient.apiService.register(mapOf(
                        "name" to name, "email" to email,
                        "password" to password, "role" to role
                    ))
                }
                if (response.isSuccessful && response.body()?.success == true) {
                    val authData = response.body()!!.data!!
                    TokenManager.saveToken(authData.token)
                    TokenManager.saveUserInfo(
                        authData.user.id, authData.user.role,
                        authData.user.name, authData.user.email
                    )
                    showToast("Registration successful!")
                    startActivity(Intent(this@RegisterActivity, MainActivity::class.java))
                    finish()
                } else {
                    val errorBody = response.errorBody()?.string()
                    val errorMsg = try {
                        Gson().fromJson(errorBody, ApiResponse::class.java).error
                    } catch (e: Exception) {
                        null
                    } ?: "Registration failed"
                    showToast(errorMsg)
                }
            } catch (e: Exception) {
                showToast("Network error: ${e.localizedMessage ?: "Connection failed"}")
            } finally {
                progressBar.visibility = android.view.View.GONE
                registerButton.isEnabled = true
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
