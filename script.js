let currentLang = "en";

const API_BASE = "/api/public";

let runtimeData = {
  courses: [],
  faculty: [],
  successStudents: [],
  teacherAchievements: [],
  notices: []
};

const fallbackData = {
  courses: [
    {
      id: 1,
      en: { name: "SSC", desc: "Comprehensive SSC preparation" },
      bn: { name: "SSC", desc: "SSC preparation" },
      icon: "fas fa-book-open"
    }
  ],
  faculty: [
    {
      id: 1,
      name: "ELIAS",
      subject_en: "Mathematics",
      subject_bn: "Mathematics",
      experience_years: 10,
      img: "https://randomuser.me/api/portraits/men/1.jpg"
    }
  ],
  successStudents: [
    {
      id: 1,
      name_en: "Arafat Hossain",
      name_bn: "Arafat Hossain",
      dept_en: "CSE",
      dept_bn: "CSE",
      class_en: "10",
      class_bn: "10",
      subject_en: "Mathematics",
      subject_bn: "Mathematics",
      city_en: "Dhaka",
      city_bn: "Dhaka",
      rating: 4.8,
      date: "2025-01-10"
    }
  ],
  teacherAchievements: [
    {
      id: 1,
      name: "Md. Imran Khan",
      qualification_en: "BSc in CSE",
      qualification_bn: "BSc in CSE",
      subject_en: "Math & ICT",
      subject_bn: "Math & ICT",
      students: 5,
      location_en: "Dhaka",
      location_bn: "Dhaka"
    }
  ],
  notices: [
    {
      id: 1,
      en: { title: "Welcome", content: "Data source fallback is active." },
      bn: { title: "Welcome", content: "Data source fallback is active." },
      date: "2025-01-01"
    }
  ]
};

const langContent = {
  en: {
    nav_home: "Home",
    nav_about: "About",
    nav_courses: "Courses",
    nav_faculty: "Mentors",
    nav_notice: "Notice",
    nav_contact: "Contact",
    nav_register: "Register",
    nav_login: "Login",
    hero_title: "Tuition HUb",
    hero_subtitle: "Elite Academic Matchmaking for Serious Achievers",
    hero_btn1: "Find Teachers",
    hero_btn2: "Contact Us",
    about_title: "About Us",
    about_desc: "Premier tuition management system connecting top educators with motivated students.",
    mission: "Mission",
    mission_desc: "Empower every student to achieve academic excellence with the right mentor.",
    vision: "Vision",
    vision_desc: "To be the most trusted tuition platform in Bangladesh.",
    est_year: "Established",
    success_rate: "Success Rate",
    achievements: "Achievements",
    courses_title: "Tuition Available For",
    faculty_title: "Our Elite Mentors",
    skills_title: "Skills You'll Master",
    skill1: "Concept Mastery",
    skill2: "Exam Strategy",
    skill3: "Problem Solving",
    success_title: "Our Successful Matches - Students Who Found Their Teachers",
    teacher_achievements_title: "Teachers Who Successfully Got Students From Our Platform",
    notice_title: "Notice Board",
    contact_title: "Get In Touch",
    address: "Dhaka, Bangladesh",
    send_msg: "Send Message",
    rights: "All rights reserved."
  },
  bn: {
    nav_home: "Home",
    nav_about: "About",
    nav_courses: "Courses",
    nav_faculty: "Mentors",
    nav_notice: "Notice",
    nav_contact: "Contact",
    nav_register: "Register",
    nav_login: "Login",
    hero_title: "Tuition HUb",
    hero_subtitle: "Elite Academic Matchmaking for Serious Achievers",
    hero_btn1: "Find Teachers",
    hero_btn2: "Contact Us",
    about_title: "About Us",
    about_desc: "Premier tuition management system connecting top educators with motivated students.",
    mission: "Mission",
    mission_desc: "Empower every student to achieve academic excellence with the right mentor.",
    vision: "Vision",
    vision_desc: "To be the most trusted tuition platform in Bangladesh.",
    est_year: "Established",
    success_rate: "Success Rate",
    achievements: "Achievements",
    courses_title: "Tuition Available For",
    faculty_title: "Our Elite Mentors",
    skills_title: "Skills You'll Master",
    skill1: "Concept Mastery",
    skill2: "Exam Strategy",
    skill3: "Problem Solving",
    success_title: "Our Successful Matches - Students Who Found Their Teachers",
    teacher_achievements_title: "Teachers Who Successfully Got Students From Our Platform",
    notice_title: "Notice Board",
    contact_title: "Get In Touch",
    address: "Dhaka, Bangladesh",
    send_msg: "Send Message",
    rights: "All rights reserved."
  }
};

async function fetchPublicContent() {
  try {
    const response = await fetch(`${API_BASE}/content`);
    if (!response.ok) {
      throw new Error("Public content API failed");
    }

    const data = await response.json();
    runtimeData = {
      courses: Array.isArray(data.courses) ? data.courses : [],
      faculty: Array.isArray(data.faculty) ? data.faculty : [],
      successStudents: Array.isArray(data.successStudents) ? data.successStudents : [],
      teacherAchievements: Array.isArray(data.teacherAchievements) ? data.teacherAchievements : [],
      notices: Array.isArray(data.notices) ? data.notices : []
    };
  } catch (error) {
    console.error("Failed to load API content, using fallback data:", error.message);
    runtimeData = fallbackData;
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  setTimeout(() => {
    const loader = document.getElementById("loader");
    if (loader) {
      loader.classList.add("fade-out");
    }
  }, 500);


  const contactForm = document.getElementById("contact-form");
  if (contactForm) {
    contactForm.addEventListener("submit", handleContactSubmit);
  }

  initNavbar();
  initScrollReveal();
  createParticles();
});

function initNavbar() {
  const navToggle = document.getElementById("nav-toggle");
  const navMenu = document.getElementById("nav-menu");
  const navLinks = document.querySelectorAll(".nav-link");

  if (navToggle && navMenu) {
    navToggle.addEventListener("click", () => {
      navMenu.classList.toggle("open");
    });
  }

  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      if (navMenu) {
        navMenu.classList.remove("open");
      }
    });
  });

  const updateActive = () => {
    const sections = document.querySelectorAll("section[id]");
    let activeId = "hero";
    const y = window.scrollY + 120;

    sections.forEach((section) => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      if (y >= top && y < top + height) {
        activeId = section.id;
      }
    });

    navLinks.forEach((link) => {
      const href = link.getAttribute("href");
      if (href === `#${activeId}`) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
  };

  window.addEventListener("scroll", updateActive);
  updateActive();
}


function renderAllSections() {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    const langBucket = langContent[currentLang] || langContent.en;

    if (langBucket[key]) {
      el.textContent = langBucket[key];
    }
  });

  renderCourses();
  renderFaculty();
  renderSuccessStudents();
  renderTeacherAchievements();
  renderNotices();
}

function renderCourses() {
  const coursesGrid = document.getElementById("courses-grid");
  if (!coursesGrid) return;

  coursesGrid.innerHTML = runtimeData.courses
    .map((course) => {
      const langCourse = course[currentLang] || course.en || {};
      const iconClass = course.icon || "fas fa-book-open";

      return `
        <div class="course-card glass">
          <div class="course-icon"><i class="${iconClass}"></i></div>
          <h3>${escapeHtml(langCourse.name || "N/A")}</h3>
          <p>${escapeHtml(langCourse.desc || "")}</p>
        </div>
      `;
    })
    .join("");
}

function renderFaculty() {
  const facultyGrid = document.getElementById("faculty-grid");
  if (!facultyGrid) return;

  facultyGrid.innerHTML = runtimeData.faculty
    .map((teacher) => {
      const subject =
        currentLang === "bn"
          ? teacher.subject_bn || teacher.subject_en || ""
          : teacher.subject_en || teacher.subject_bn || "";

      const expYears = Number(teacher.experience_years || 0);
      const experienceText = expYears > 0 ? `${expYears} years experience` : "Experience not listed";

      return `
        <div class="faculty-card glass">
          <img src="${escapeHtml(teacher.img || "https://via.placeholder.com/120")}" alt="${escapeHtml(
        teacher.name || "Teacher"
      )}" class="faculty-img">
          <h3 class="faculty-name">${escapeHtml(teacher.name || "N/A")}</h3>
          <p class="faculty-subject">${escapeHtml(subject)}</p>
          <p>${escapeHtml(experienceText)}</p>
        </div>
      `;
    })
    .join("");
}

function renderSuccessStudents() {
  const successGrid = document.getElementById("success-grid");
  if (!successGrid) return;

  successGrid.innerHTML = runtimeData.successStudents
    .map((student) => {
      const name = currentLang === "bn" ? student.name_bn || student.name_en : student.name_en || student.name_bn;
      const subject =
        currentLang === "bn" ? student.subject_bn || student.subject_en : student.subject_en || student.subject_bn;
      const dept = currentLang === "bn" ? student.dept_bn || student.dept_en : student.dept_en || student.dept_bn;
      const classValue =
        currentLang === "bn" ? student.class_bn || student.class_en : student.class_en || student.class_bn;
      const city = currentLang === "bn" ? student.city_bn || student.city_en : student.city_en || student.city_bn;

      return `
        <div class="success-card glass">
          <h3>${escapeHtml(name || "N/A")}</h3>
          <p><strong>${escapeHtml(subject || "")}</strong> - Class ${escapeHtml(classValue || "")}</p>
          <p>${escapeHtml(dept || "")}, ${escapeHtml(city || "")}</p>
          <div class="badge">* ${escapeHtml(String(student.rating || "0"))} � Matched ${escapeHtml(
        String(student.date || "")
      )}</div>
          <span class="badge">Matched Successfully</span>
        </div>
      `;
    })
    .join("");
}

function renderTeacherAchievements() {
  const achievementsGrid = document.getElementById("achievements-grid");
  if (!achievementsGrid) return;

  achievementsGrid.innerHTML = runtimeData.teacherAchievements
    .map((item) => {
      const qualification =
        currentLang === "bn"
          ? item.qualification_bn || item.qualification_en
          : item.qualification_en || item.qualification_bn;

      const subject = currentLang === "bn" ? item.subject_bn || item.subject_en : item.subject_en || item.subject_bn;
      const location =
        currentLang === "bn" ? item.location_bn || item.location_en : item.location_en || item.location_bn;

      return `
        <div class="achievement-card glass">
          <h3>${escapeHtml(item.name || "N/A")}</h3>
          <p>${escapeHtml(qualification || "")}</p>
          <p>${escapeHtml(subject || "")} � ${escapeHtml(String(item.students || 0))} Students Found</p>
          <p>Location: ${escapeHtml(location || "")}</p>
        </div>
      `;
    })
    .join("");
}

function renderNotices() {
  const noticeList = document.getElementById("notice-list");
  if (!noticeList) return;

  noticeList.innerHTML = runtimeData.notices
    .map((notice) => {
      const langNotice = notice[currentLang] || notice.en || {};

      return `
        <div class="notice-item">
          <h3 class="notice-title">${escapeHtml(langNotice.title || "")}</h3>
          <p>${escapeHtml(langNotice.content || "")}</p>
          <span class="notice-date">${escapeHtml(String(notice.date || ""))}</span>
        </div>
      `;
    })
    .join("");
}

async function handleContactSubmit(event) {
  event.preventDefault();

  const form = event.target;
  const formData = new FormData(form);

  const payload = {
    name: String(formData.get("name") || "").trim(),
    email: String(formData.get("email") || "").trim(),
    message: String(formData.get("message") || "").trim()
  };

  if (!payload.name || !payload.email || !payload.message) {
    alert("Please fill in all fields.");
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/contact`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || "Failed to submit message.");
    }

    alert(data.message || "Message sent successfully.");
    form.reset();
  } catch (error) {
    alert(error.message || "Could not send your message right now.");
  }
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function initScrollReveal() {
  const sections = document.querySelectorAll(".section");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("revealed");
          entry.target.style.opacity = 1;
          entry.target.style.transform = "translateY(0)";
        }
      });
    },
    { threshold: 0.1 }
  );

  sections.forEach((section) => {
    section.style.opacity = 0;
    section.style.transform = "translateY(30px)";
    section.style.transition = "opacity 0.8s ease, transform 0.8s ease";
    observer.observe(section);
  });
}

function createParticles() {
  const host = document.getElementById("particles");
  if (!host) return;

  const canvas = document.createElement("canvas");
  canvas.style.position = "absolute";
  canvas.style.top = 0;
  canvas.style.left = 0;
  canvas.style.width = "100%";
  canvas.style.height = "100%";
  canvas.style.pointerEvents = "none";
  host.appendChild(canvas);

  const ctx = canvas.getContext("2d");
  let width;
  let height;
  const particles = [];

  function initParticles() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
    particles.length = 0;

    for (let i = 0; i < 50; i += 1) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 2 + 1,
        speedX: (Math.random() - 0.5) * 0.5,
        speedY: (Math.random() - 0.5) * 0.5,
        color: `rgba(207,166,104,${Math.random() * 0.3})`
      });
    }
  }

  function drawParticles() {
    ctx.clearRect(0, 0, width, height);

    particles.forEach((particle) => {
      ctx.beginPath();
      ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      ctx.fillStyle = particle.color;
      ctx.fill();

      particle.x += particle.speedX;
      particle.y += particle.speedY;

      if (particle.x < 0 || particle.x > width) particle.speedX *= -1;
      if (particle.y < 0 || particle.y > height) particle.speedY *= -1;
    });

    requestAnimationFrame(drawParticles);
  }

  window.addEventListener("resize", initParticles);

  initParticles();
  drawParticles();
}
