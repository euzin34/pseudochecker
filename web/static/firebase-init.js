// Firebase initialization (module)
// Imports the Firebase SDK and initializes the app using project config.
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.14.0/firebase-app.js";
import { getAuth, onAuthStateChanged, signInWithPopup, GoogleAuthProvider, signOut as fbSignOut } from "https://www.gstatic.com/firebasejs/12.14.0/firebase-auth.js";

// Project Firebase configuration (moved from r.txt)
const firebaseConfig = {
  apiKey: "AIzaSyDv82KqtfJ3ZuHf88nmDC52HJ1mP1A0KMc", // pragma: allowlist secret
  authDomain: "pesudochecker.firebaseapp.com",
  projectId: "pesudochecker",
  storageBucket: "pesudochecker.firebasestorage.app",
  messagingSenderId: "35025575537",
  appId: "1:35025575537:web:00833d40c975660f6785d0",
  measurementId: "G-GVZRWCVQ1S"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Expose a small helper on window for other scripts to use
window.firebaseAuth = {
  auth,
  signInWithGoogle: async () => {
    const provider = new GoogleAuthProvider();
    return await signInWithPopup(auth, provider);
  },
  signOut: async () => await fbSignOut(auth),
  getIdToken: async () => {
    const user = auth.currentUser;
    return user ? await user.getIdToken(true) : null;
  },
  onAuthStateChanged: (cb) => onAuthStateChanged(auth, cb),
};
