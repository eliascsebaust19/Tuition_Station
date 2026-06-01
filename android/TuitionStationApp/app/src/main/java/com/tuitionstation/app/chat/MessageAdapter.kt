package com.tuitionstation.app.chat

import android.view.Gravity
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.LinearLayout
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.tuitionstation.app.R
import com.tuitionstation.app.api.MessageData

class MessageAdapter(private val currentUserId: Int) :
    ListAdapter<MessageData, MessageAdapter.ViewHolder>(DiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_message, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(getItem(position), currentUserId)
    }

    class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val messageText: TextView = itemView.findViewById(R.id.message_text)
        private val timeText: TextView = itemView.findViewById(R.id.message_time)
        private val bubbleLayout: LinearLayout = itemView.findViewById(R.id.bubble_layout)

        fun bind(message: MessageData, currentUserId: Int) {
            messageText.text = message.message
            timeText.text = message.createdAt ?: ""

            val isSent = message.senderId == currentUserId
            val params = bubbleLayout.layoutParams as LinearLayout.LayoutParams

            if (isSent) {
                bubbleLayout.setBackgroundResource(R.drawable.bg_message_sent)
                params.gravity = Gravity.END
            } else {
                bubbleLayout.setBackgroundResource(R.drawable.bg_message_received)
                params.gravity = Gravity.START
            }
            bubbleLayout.layoutParams = params
        }
    }

    class DiffCallback : DiffUtil.ItemCallback<MessageData>() {
        override fun areItemsTheSame(old: MessageData, new: MessageData) = old.id == new.id
        override fun areContentsTheSame(old: MessageData, new: MessageData) = old == new
    }
}
