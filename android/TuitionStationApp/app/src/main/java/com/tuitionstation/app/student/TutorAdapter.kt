package com.tuitionstation.app.student

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.tuitionstation.app.R
import com.tuitionstation.app.api.TeacherListItem
import com.tuitionstation.app.common.loadProfilePicture

class TutorAdapter(private val onClick: (TeacherListItem) -> Unit) :
    ListAdapter<TeacherListItem, TutorAdapter.ViewHolder>(DiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_teacher_card, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(getItem(position), onClick)
    }

    class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val name: TextView = itemView.findViewById(R.id.teacher_name)
        private val subject: TextView = itemView.findViewById(R.id.teacher_subject)
        private val fee: TextView = itemView.findViewById(R.id.teacher_fee)
        private val location: TextView = itemView.findViewById(R.id.teacher_location)
        private val rating: TextView = itemView.findViewById(R.id.teacher_rating)
        private val badge: ImageView = itemView.findViewById(R.id.verified_badge)

        fun bind(teacher: TeacherListItem, onClick: (TeacherListItem) -> Unit) {
            name.text = teacher.user.name
            subject.text = teacher.profile?.subject ?: "General"
            fee.text = "BDT ${teacher.profile?.fee ?: 0}/mo"
            location.text = teacher.profile?.location ?: ""
            rating.text = "${teacher.avgRating ?: 0.0} (${teacher.reviewCount ?: 0})"
            badge.visibility = if (teacher.verified == true) View.VISIBLE else View.GONE
            itemView.setOnClickListener { onClick(teacher) }
        }
    }

    class DiffCallback : DiffUtil.ItemCallback<TeacherListItem>() {
        override fun areItemsTheSame(old: TeacherListItem, new: TeacherListItem) = old.user.id == new.user.id
        override fun areContentsTheSame(old: TeacherListItem, new: TeacherListItem) = old == new
    }
}
