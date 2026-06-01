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
import kotlinx.coroutines.*

class LoginActivity : AppCompatActivity() {
    private lateinit var emailInput: EditText
    private lateinit var passwordInput: EditText
    private lateinit var loginButton: Button
    private lateinit var registerLink: TextView
    private lateinit var progressBar: ProgressBar
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        emailInput = findViewById(R.id.email_input)
        passwordInput = findViewById(R.id.password_input)
        loginButton = findViewById(R.id.login_button)
        registerLink = findViewById(R.id.register_link)
        progressBar = findViewById(R.id.progress_bar)

        loginButton.setOnClickListener { performLogin() }
        registerLink.setOnClickListener {
            startActivity(Intent(this, RegisterActivity::class.java))
        }
    }

    private fun performLogin() {
        val email = emailInput.text.toString().trim()
        val password = passwordInput.text.toString()

        if (email.isEmpty()) { emailInput.error = getString(R.string.email_required); return }
        if (password.isEmpty()) { passwordInput.error = getString(R.string.password_required); return }

        hideKeyboard()
        progressBar.visibility = android.view.View.VISIBLE
        loginButton.isEnabled = false

        scope.launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    ApiClient.apiService.login(mapOf("email" to email, "password" to password))
                }
                if (response.isSuccessful && response.body()?.success == true) {
                    val authData = response.body()!!.data!!
                    TokenManager.saveToken(authData.token)
                    TokenManager.saveUserInfo(
                        authData.user.id, authData.user.role,
                        authData.user.name, authData.user.email
                    )
                    startActivity(Intent(this@LoginActivity, MainActivity::class.java))
                    finish()
                } else {
                    val errorMsg = response.body()?.error ?: "Login failed"
                    showToast(errorMsg)
                }
            } catch (e: Exception) {
                showToast("Network error: ${e.localizedMessage ?: "Connection failed"}")
            } finally {
                progressBar.visibility = android.view.View.GONE
                loginButton.isEnabled = true
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
