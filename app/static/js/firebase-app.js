import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

// Firebase configuration from base.html
const firebaseConfig = window.firebaseConfig || {
  apiKey: "AIzaSyA-7V2lDqXxvv6VNtugMoJKmgFIgZP4LEc",
  authDomain: "tuition-station.firebaseapp.com",
  projectId: "tuition-station",
  storageBucket: "tuition-station.firebasestorage.app",
  messagingSenderId: "604643711076",
  appId: "1:604643711076:web:ef914354e35dacd3b96771",
  measurementId: "G-SZTB8YXJBD"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { auth, app };
