import streamlit as st
from typing import Dict, List, Optional
from user_manager import UserManager

class ScriptSelector:
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
    
    def render_script_selector(self, username: str) -> Optional[str]:
        """Render script selector and return selected script ID"""
        
        # Get user's scripts
        user_scripts = self.user_manager.get_user_scripts(username)
        
        # Check if quick create was triggered
        show_create = st.session_state.get('show_create_script', False)
        
        # Create new script section - make it more prominent
        if show_create or not user_scripts:
            st.subheader("➕ Create New Script")
            
            with st.form("create_script_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_script_name = st.text_input("Script Name:", placeholder="My Amazing Screenplay")
                with col2:
                    new_script_description = st.text_area("Description:", placeholder="Brief description of your script...", height=100)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("🎬 Create New Script", type="primary"):
                        if new_script_name.strip():
                            script_id = self.user_manager.create_script(username, new_script_name.strip(), new_script_description.strip())
                            st.success(f"Script '{new_script_name}' created successfully!")
                            # Clear the show_create flag
                            if 'show_create_script' in st.session_state:
                                del st.session_state.show_create_script
                            st.rerun()
                        else:
                            st.error("Please enter a script name!")
                with col2:
                    if st.form_submit_button("Cancel"):
                        if 'show_create_script' in st.session_state:
                            del st.session_state.show_create_script
                        st.rerun()
            
            st.divider()
        
        # Script selection
        st.subheader("📋 Select Script")
        
        if user_scripts:
            script_options = [f"{script['name']} ({script['description'][:50]}...)" if script['description'] else script['name'] 
                            for script in user_scripts]
            script_ids = [script['id'] for script in user_scripts]
            
            selected_index = st.selectbox(
                "Choose a script to work on:",
                range(len(script_options)),
                format_func=lambda x: script_options[x],
                key="script_selector"
            )
            
            selected_script_id = script_ids[selected_index] if selected_index < len(script_ids) else None
            
            # Display script info
            if selected_script_id:
                script = self.user_manager.get_script(username, selected_script_id)
                if script:
                    st.info(f"""
                    **Script:** {script['name']}
                    **Description:** {script['description'] or 'No description'}
                    **Created:** {script['created_at'][:10]}
                    **Last Modified:** {script['last_modified'][:10]}
                    """)
            
            return selected_script_id
        else:
            st.info("No scripts created yet. Create your first script above!")
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
                <h3>🎬 Ready to start your screenplay?</h3>
                <p>Create your first script to begin your writing journey!</p>
            </div>
            """, unsafe_allow_html=True)
            return None
    
    def render_script_actions(self, username: str, script_id: str):
        """Render script actions (delete, rename, etc.)"""
        if not script_id:
            return
        
        st.subheader("⚙️ Script Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎬 Create New Script", type="primary"):
                st.session_state.show_create_script = True
                st.rerun()
        
        with col2:
            if st.button("🗑️ Delete Script", type="secondary"):
                if st.checkbox("I'm sure I want to delete this script"):
                    if self.user_manager.delete_script(username, script_id):
                        st.success("Script deleted!")
                        st.rerun()
                    else:
                        st.error("Error deleting script!")
        
        with col3:
            if st.button("📝 Rename Script", type="secondary"):
                script = self.user_manager.get_script(username, script_id)
                if script:
                    new_name = st.text_input("New Name:", value=script['name'])
                    if st.button("Save"):
                        script['name'] = new_name
                        if self.user_manager.update_script(username, script_id, script):
                            st.success("Script renamed!")
                            st.rerun()
                        else:
                            st.error("Error renaming script!") 