// Supabase setup
const SUPABASE_URL = 'https://mbtphgoczblixxzznlzs.supabase.co';
        const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1idHBoZ29jemJsaXh4enpubHpzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA0MDc0NzYsImV4cCI6MjA0NTk4MzQ3Nn0.VvejXag2L4zlxgPe2bbw98VwCb2aAopJnPv9d5H53Ms';
const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// DOM Elements
const userInfo = document.getElementById("user-info");
const welcomeMessage = document.getElementById("welcome-message");
const signoutButton = document.getElementById("signout-btn");

// Check session and display user info
async function checkSession() {
    const { data: { session } } = await supabase.auth.getSession();

    if (session) {
        // User is signed in
        const userEmail = session.user.email;
        welcomeMessage.innerText = `Welcome, ${userEmail}`;
        signoutButton.style.display = "inline";
    } else {
        // Redirect to login page if not signed in
        window.location.href = "login.html";
    }
}

// Event listener for signing out
signoutButton.addEventListener("click", async () => {
    await supabase.auth.signOut();
    window.location.href = "login.html";  // Redirect to login page after sign-out
});

// Run the session check when page loads
document.addEventListener("DOMContentLoaded", checkSession);