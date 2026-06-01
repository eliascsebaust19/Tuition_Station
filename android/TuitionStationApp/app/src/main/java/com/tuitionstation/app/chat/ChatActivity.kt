package com.tuitionstation.app.chat

import android.content.Intent
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.tuitionstation.app.R
import com.tuitionstation.app.api.ApiClient
import com.tuitionstation.app.api.ConversationData
import com.tuitionstation.app.common.showToast
import kotlinx.coroutines.*

class ChatActivity : AppCompatActivity() {
    private lateinit var recyclerView: RecyclerView
    private lateinit var progressBar: ProgressBar
    private lateinit var emptyText: TextView
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())
    private val adapter = ConversationAdapter { conversation -> openConversation(conversation) }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_chat)

        recyclerView = findViewById(R.id.recycler_view)
        progressBar = findViewById(R.id.progress_bar)
        emptyText = findViewById(R.id.empty_text)

        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = adapter

        loadConversations()
    }

    private fun loadConversations() {
        progressBar.visibility = android.view.View.VISIBLE
        scope.launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    ApiClient.apiService.getConversations()
                }
                if (response.isSuccessful && response.body()?.success == true) {
                    val conversations = response.body()!!.data ?: emptyList()
                    adapter.submitList(conversations)
                    emptyText.visibility = if (conversations.isEmpty()) android.view.View.VISIBLE else android.view.View.GONE
                }
            } catch (e: Exception) {
                showToast("Network error")
            } finally {
                progressBar.visibility = android.view.View.GONE
            }
        }
    }

    private fun openConversation(conversation: ConversationData) {
        val intent = Intent(this, MessageActivity::class.java)
        intent.putExtra("other_user_id", conversation.user.id)
        intent.putExtra("other_user_name", conversation.user.name)
        startActivity(intent)
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
