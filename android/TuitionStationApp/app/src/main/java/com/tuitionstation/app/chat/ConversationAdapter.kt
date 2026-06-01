package com.tuitionstation.app.chat

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.tuitionstation.app.R
import com.tuitionstation.app.api.ConversationData

class ConversationAdapter(private val onClick: (ConversationData) -> Unit) :
    ListAdapter<ConversationData, ConversationAdapter.ViewHolder>(DiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_conversation, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(getItem(position), onClick)
    }

    class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val name: TextView = itemView.findViewById(R.id.conversation_name)
        private val lastMessage: TextView = itemView.findViewById(R.id.conversation_last_message)
        private val time: TextView = itemView.findViewById(R.id.conversation_time)
        private val unreadBadge: TextView = itemView.findViewById(R.id.unread_badge)

        fun bind(conversation: ConversationData, onClick: (ConversationData) -> Unit) {
            name.text = conversation.user.name
            lastMessage.text = conversation.lastMessage ?: "No messages yet"
            time.text = conversation.lastMessageTime ?: ""
            if (conversation.unreadCount != null && conversation.unreadCount > 0) {
                unreadBadge.visibility = View.VISIBLE
                unreadBadge.text = "${conversation.unreadCount}"
            } else {
                unreadBadge.visibility = View.GONE
            }
            itemView.setOnClickListener { onClick(conversation) }
        }
    }

    class DiffCallback : DiffUtil.ItemCallback<ConversationData>() {
        override fun areItemsTheSame(old: ConversationData, new: ConversationData) = old.user.id == new.user.id
        override fun areContentsTheSame(old: ConversationData, new: ConversationData) = old == new
    }
}
