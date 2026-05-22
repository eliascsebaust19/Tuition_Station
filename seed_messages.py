from app import create_app
from models import db, User, Message
from datetime import datetime
from datetime import datetime

def seed_messages():
    app = create_app()
    with app.app_context():
        students = User.query.filter_by(role='student').all()
        teachers = User.query.filter_by(role='teacher').all()
        admins = User.query.filter_by(role='admin').all()

        if not students or not teachers:
            print("No students or teachers found. Run main seed first.")
            return

        admin = admins[0] if admins else None

        bengali_messages = [
            "আসসালামু আলাইকুম, আমি আপনার কাছে গণিত শিখতে আগ্রহী। আমার এসএসসি পরীক্ষা আগামী মাসে, দয়া করে জানাবেন আপনি কি অনলাইনে ক্লাস নেন?",
            "স্যার, আপনার প্রোফাইল দেখে আমি মুগ্ধ। আমি পদার্থবিজ্ঞানে দুর্বল, আপনি কি আমাকে সাহায্য করতে পারবেন?",
            "ভাইয়া, আমি আপনার কাছ থেকে ইংরেজি গ্রামার শিখতে চাই। আপনার ফি কত এবং কোথায় আপনার ক্লাস হয়?",
            "আমার ছোট ভাইয়ের জন্য একজন ভালো টিউটর খুঁজছি। সে ক্লাস এইটে পড়ে, বিষয় গণিত ও বিজ্ঞান। আপনার কি সময় আছে?",
            "আমি বিশ্ববিদ্যালয় ভর্তি পরীক্ষার জন্য প্রস্তুতি নিচ্ছি। আপনার কি রসায়ন ও পদার্থবিদ্যার ব্যাচ আছে?",
        ]

        teacher_messages = [
            "আমি আপনার রিকোয়েস্ট পেয়েছি। আপনি কখন ক্লাস শুরু করতে চান? আমি সপ্তাহে ৩ দিন ফ্রি থাকি।",
            "আপনার ম্যাসেজের জন্য ধন্যবাদ। আমি আপনাকে একটি ডেমো ক্লাস দিতে পারি আগামীকাল বিকেলে।",
            "জ্বী, আমি অনলাইনে ক্লাস নেই। গুগল মিট বা জুম দিয়ে ক্লাস করাই। আপনার সুবিধামত সময় জানান।",
            "আমার বর্তমানে কিছু ফ্রি স্লট আছে। আপনি কি সপ্তাহে ২ দিন ক্লাস নিতে পারবেন? ফি নিয়ে আমরা আলোচনা করতে পারি।",
            "আপনার আগ্রহের জন্য ধন্যবাদ। আমি একজন অভিজ্ঞ শিক্ষক এবং আমার সকল ছাত্রই ভালো ফলাফল করেছে।",
        ]

        admin_messages = [
            "আপনার রেজিস্ট্রেশন সম্পন্ন হয়েছে। আপনার প্রোফাইল সম্পূর্ণ করুন যাতে ছাত্ররা আপনাকে খুঁজে পায়।",
            "আপনার টিউশন রিকোয়েস্টটি অনুমোদিত হয়েছে। এখন আপনি শিক্ষকের সাথে যোগাযোগ করতে পারেন।",
            "আপনার প্রোফাইল আপডেট করার জন্য অনুরোধ করা হচ্ছে। দয়া করে আপনার শিক্ষাগত যোগ্যতা এবং অভিজ্ঞতা পূরণ করুন।",
            "আমাদের প্ল্যাটফর্ম ব্যবহারের জন্য ধন্যবাদ। আপনার যদি কোনো সাহায্যের প্রয়োজন হয় তবে আমাদের জানান।",
            "টিউশন স্টেশন পরিবারকে স্বাগতম! আমরা আশা করি আপনি আমাদের প্ল্যাটফর্মে ভালো শিক্ষক পাবেন।",
        ]

        count = 0

        for student in students:
            for teacher in teachers[:3]:
                if student.id != teacher.id:
                    existing = Message.query.filter_by(sender_id=student.id, receiver_id=teacher.id).first()
                    if not existing:
                        msg_text = bengali_messages[hash(f"{student.id}-{teacher.id}") % len(bengali_messages)]
                        msg = Message(sender_id=student.id, receiver_id=teacher.id, message=msg_text, is_read=False, created_at=datetime.utcnow())
                        db.session.add(msg)
                        count += 1

                        reply_text = teacher_messages[hash(f"{teacher.id}-{student.id}") % len(teacher_messages)]
                        reply = Message(sender_id=teacher.id, receiver_id=student.id, message=reply_text, is_read=False, created_at=datetime.utcnow())
                        db.session.add(reply)
                        count += 1

        if admin:
            for student in students[:5]:
                existing = Message.query.filter_by(sender_id=admin.id, receiver_id=student.id).first()
                if not existing:
                    msg_text = admin_messages[hash(f"admin-{student.id}") % len(admin_messages)]
                    msg = Message(sender_id=admin.id, receiver_id=student.id, message=msg_text, is_read=False, created_at=datetime.utcnow())
                    db.session.add(msg)
                    count += 1

            for teacher in teachers[:5]:
                existing = Message.query.filter_by(sender_id=admin.id, receiver_id=teacher.id).first()
                if not existing:
                    msg_text = admin_messages[hash(f"admin-t-{teacher.id}") % len(admin_messages)]
                    msg = Message(sender_id=admin.id, receiver_id=teacher.id, message=msg_text, is_read=False, created_at=datetime.utcnow())
                    db.session.add(msg)
                    count += 1

        db.session.commit()
        print(f"✅ {count} Bengali messages seeded successfully!")

if __name__ == "__main__":
    seed_messages()
