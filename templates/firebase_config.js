const firebaseConfig = {
    apiKey: "{{ config.FIREBASE_API_KEY }}",
    authDomain: "{{ config.FIREBASE_PROJECT_ID }}.firebaseapp.com",
    projectId: "{{ config.FIREBASE_PROJECT_ID }}",
    storageBucket: "{{ config.FIREBASE_STORAGE_BUCKET }}",
    appId: "{{ config.FIREBASE_APP_ID }}"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
const auth = firebase.getAuth(app);
window.firebaseAuth = auth;
