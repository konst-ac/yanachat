import streamlit as st
from user_manager import UserManager

class LoginInterface:
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
    
    def render_login(self) -> tuple[bool, str]:
        """Render login interface and return (is_authenticated, username)"""
        
        # Check if user is already logged in
        if 'authenticated' in st.session_state and st.session_state.authenticated:
            return True, st.session_state.username
        
        st.markdown('<h1 class="main-header">🎬 YanaChat AI Script Assistant</h1>', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">🔐 Login</h2>', unsafe_allow_html=True)
        
        # Create tabs for login and register
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            # Login form
            with st.form("login_form"):
                username = st.text_input("Username:", placeholder="Enter your username")
                password = st.text_input("Password:", type="password", placeholder="Enter your password")
                
                col1, col2 = st.columns(2)
                with col1:
                    login_button = st.form_submit_button("Login", type="primary")
                with col2:
                    st.form_submit_button("Clear")
                
                if login_button:
                    if username and password:
                        if self.user_manager.authenticate_user(username, password):
                            st.session_state.authenticated = True
                            st.session_state.username = username
                            st.success(f"Welcome back, {username}!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password!")
                    else:
                        st.error("Please enter both username and password!")
        
        with tab2:
            # Registration form
            with st.form("register_form"):
                new_username = st.text_input("New Username:", placeholder="Choose a username")
                new_password = st.text_input("New Password:", type="password", placeholder="Choose a password")
                confirm_password = st.text_input("Confirm Password:", type="password", placeholder="Confirm your password")
                email = st.text_input("Email (optional):", placeholder="your.email@example.com")
                
                col1, col2 = st.columns(2)
                with col1:
                    register_button = st.form_submit_button("Register", type="primary")
                with col2:
                    st.form_submit_button("Clear")
                
                if register_button:
                    if not new_username or not new_password:
                        st.error("Please enter both username and password!")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match!")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters long!")
                    elif self.user_manager.user_exists(new_username):
                        st.error("Username already exists!")
                    else:
                        if self.user_manager.register_user(new_username, new_password, email):
                            st.success(f"Account created successfully! You can now login as {new_username}")
                        else:
                            st.error("Error creating account!")
            
            # Create Test user with sample data
            st.divider()
            st.subheader("🧪 Test Account")
            st.info("Create a Test account with sample data to explore the app features.")
            
            if st.button("Create Test Account with Sample Data", type="secondary"):
                try:
                    script_id = self.user_manager.create_test_user_with_sample_data()
                    st.success("Test account created successfully!")
                    st.info("Username: Test | Password: test123")
                    st.info("Sample script 'The Investigation' with 3 characters, 4 locations, and 4 scenes has been created.")
                except Exception as e:
                    st.error(f"Error creating test account: {str(e)}")
        
        return False, ""
    
    def render_logout(self):
        """Render logout button"""
        if st.sidebar.button("🚪 Logout"):
            # Clear session state
            for key in ['authenticated', 'username', 'current_script_id']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        
        # Show current user info
        if 'username' in st.session_state:
            st.sidebar.markdown(f"**👤 Logged in as:** {st.session_state.username}") 