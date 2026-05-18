require("dotenv").config();

const path = require("path");
const bcrypt = require("bcrypt");
const express = require("express");
const session = require("express-session");

const { pool, testDbConnection } = require("./config/db");

const authRoutes = require("./routes/auth");
const adminRoutes = require("./routes/admin");
const studentRoutes = require("./routes/student");
const teacherRoutes = require("./routes/teacher");
const publicRoutes = require("./routes/public");

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(
  session({
    name: "tms.sid",
    secret: process.env.SESSION_SECRET || "replace_with_secure_session_secret",
    resave: false,
    saveUninitialized: false,
    cookie: {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      maxAge: 1000 * 60 * 60 * 24
    }
  })
);

app.use("/public", express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.get("/admin-panel.html", (req, res) => {
  res.sendFile(path.join(__dirname, "admin-panel.html"));
});

app.get("/teacher-dashboard.html", (req, res) => {
  res.sendFile(path.join(__dirname, "teacher-dashboard.html"));
});

app.get("/student-dashboard.html", (req, res) => {
  res.sendFile(path.join(__dirname, "student-dashboard.html"));
});

app.get("/style.css", (req, res) => {
  res.sendFile(path.join(__dirname, "style.css"));
});

app.get("/script.js", (req, res) => {
  res.sendFile(path.join(__dirname, "script.js"));
});

app.use("/api/auth", authRoutes);
app.use("/api/admin", adminRoutes);
app.use("/api/student", studentRoutes);
app.use("/api/teacher", teacherRoutes);
app.use("/api/public", publicRoutes);

app.get("/health", (req, res) => {
  res.json({ ok: true, message: "Tuition backend is running." });
});

app.use((error, req, res, next) => {
  console.error(error);
  res.status(500).json({ message: "Internal server error." });
});

async function ensureDefaultAdmin() {
  const adminEmail = process.env.ADMIN_EMAIL;
  const adminPassword = process.env.ADMIN_PASSWORD;
  const adminName = process.env.ADMIN_NAME || "System Admin";
  const adminPhone = process.env.ADMIN_PHONE || "01700000000";

  if (!adminEmail || !adminPassword) {
    return;
  }

  const [rows] = await pool.execute("SELECT id FROM users WHERE email = ? LIMIT 1", [adminEmail]);

  if (rows.length > 0) {
    return;
  }

  const hash = await bcrypt.hash(adminPassword, 12);

  await pool.execute(
    `INSERT INTO users (name, email, phone, password, role, status)
     VALUES (?, ?, ?, ?, 'admin', 'active')`,
    [adminName, adminEmail, adminPhone, hash]
  );

  console.log("Default admin created from environment variables.");
}

async function startServer() {
  try {
    await testDbConnection();
    await ensureDefaultAdmin();

    const port = Number(process.env.PORT || 3000);
    app.listen(port, () => {
      console.log(`Server running on http://localhost:${port}`);
    });
  } catch (error) {
    console.error("Failed to start server:", error.message);
    process.exit(1);
  }
}

startServer();

