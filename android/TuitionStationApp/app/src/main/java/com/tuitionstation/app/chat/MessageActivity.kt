package com.tuitionstation.app.chat

import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.tuitionstation.app.R
import com.tuitionstation.app.api.ApiClient
import com.tuitionstation.app.api.MessageData
import com.tuitionstation.app.auth.TokenManager
import com.tuitionstation.app.common.hideKeyboard
import com.tuitionstation.app.common.showToast
import kotlinx.coroutines.*

class MessageActivity : AppCompatActivity() {
    private lateinit var recyclerView: RecyclerView
    private lateinit var messageInput: EditText
    private lateinit var sendButton: ImageButton
    private lateinit var progressBar: ProgressBar
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())
    private val messages = mutableListOf<MessageData>()
    private lateinit var adapter: MessageAdapter
    private var otherUserId: Int = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_message)

        otherUserId = intent.getIntExtra("other_user_id", 0)
        val otherUserName = intent.getStringExtra("other_user_name") ?: "Chat"
        if (otherUserId == 0) { finish(); return }

        supportActionBar?.title = otherUserName
        supportActionBar?.setDisplayHomeAsUpEnabled(true)

        recyclerView = findViewById(R.id.recycler_view)
        messageInput = findViewById(R.id.message_input)
        sendButton = findViewById(R.id.send_button)
        progressBar = findViewById(R.id.progress_bar)

        adapter = MessageAdapter(TokenManager.getUserId())
        recyclerView.layoutManager = LinearLayoutManager(this).also {
            it.stackFromEnd = true
        }
        recyclerView.adapter = adapter

        loadMessages()

        sendButton.setOnClickListener { sendMessage() }
        messageInput.setOnEditorActionListener { _, _, _ -> sendMessage(); true }
    }

    private fun loadMessages() {
        progressBar.visibility = android.view.View.VISIBLE
        scope.launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    ApiClient.apiService.getMessages(otherUserId)
                }
                if (response.isSuccessful && response.body()?.success == true) {
                    messages.clear()
                    messages.addAll(response.body()!!.data ?: emptyList())
                    adapter.submitList(messages.toList())
                    recyclerView.scrollToPosition(messages.size - 1)
                }
            } catch (e: Exception) {
                showToast("Network error")
            } finally {
                progressBar.visibility = android.view.View.GONE
            }
        }
    }

    private fun sendMessage(): Boolean {
        val text = messageInput.text.toString().trim()
        if (text.isEmpty()) return false

        hideKeyboard()
        messageInput.setText("")

        scope.launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    ApiClient.apiService.sendMessage(otherUserId, mapOf("message" to text))
                }
                if (response.isSuccessful) {
                    loadMessages()
                } else {
                    showToast("Failed to send")
                }
            } catch (e: Exception) {
                showToast("Network error")
            }
        }
        return true
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        return true
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
