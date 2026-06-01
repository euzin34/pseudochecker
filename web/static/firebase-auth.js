// Small module to wire the auth UI (depends on firebase-init.js exposing window.firebaseAuth)
const btnRegister = document.getElementById('btn-register');
const btnSignIn = document.getElementById('btn-signin');
const btnSignOut = document.getElementById('btn-signout');
// keep the element but don't show the user's email in the UI
const userEmail = document.getElementById('user-email');

if (window.firebaseAuth) {
  window.firebaseAuth.onAuthStateChanged((user) => {
    if (user) {
      // Hide register/signin, show signout; do not display email
      if (btnRegister) btnRegister.classList.add('hidden');
      if (btnSignIn) btnSignIn.classList.add('hidden');
      if (btnSignOut) btnSignOut.classList.remove('hidden');
      if (userEmail) userEmail.classList.add('hidden');
    } else {
      if (btnRegister) btnRegister.classList.remove('hidden');
      if (btnSignIn) btnSignIn.classList.remove('hidden');
      if (btnSignOut) btnSignOut.classList.add('hidden');
      if (userEmail) userEmail.classList.add('hidden');
    }
  });

  const doSignIn = async () => {
    try {
      await window.firebaseAuth.signInWithGoogle();
    } catch (e) {
      console.error('Sign-in failed', e);
      alert('Sign-in failed: ' + (e.message || e));
    }
  };

  if (btnSignIn) btnSignIn.addEventListener('click', doSignIn);
  if (btnRegister) btnRegister.addEventListener('click', doSignIn); // register uses same Google flow
  if (btnSignOut) btnSignOut.addEventListener('click', async () => {
    try { await window.firebaseAuth.signOut(); } catch(e) { console.error(e); }
  });
}
