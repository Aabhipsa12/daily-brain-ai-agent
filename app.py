import os
import hashlib
import streamlit as st
from dotenv import load_dotenv
from main import (
    create_agent,
    get_saved_tasks,
    toggle_task_status,
    delete_task_by_index,
    toggle_subtask_status,
    add_subtask_to_task,
    delete_subtask_by_index,
    update_task_category_by_index,
    get_deadline_status,
    transcribe_audio
)

# Load environment variables (.env)
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="Daily Brain — AI Task Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Theme-Adaptive Custom Styling ---
st.markdown("""
<style>
    /* Main container padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header styling */
    .app-header {
        margin-bottom: 1.5rem;
    }
    .app-title {
        font-size: 2.2rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .app-subtitle {
        font-size: 1rem;
        opacity: 0.8;
        margin-top: -0.3rem;
    }

    /* Task Card styling */
    .task-card {
        background-color: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 10px;
        padding: 1.1rem 1.25rem;
        margin-bottom: 0.75rem;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .task-card:hover {
        border-color: rgba(128, 128, 128, 0.4);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }
    .task-card-completed {
        opacity: 0.65;
        background-color: rgba(16, 185, 129, 0.04);
        border-left: 4px solid #10B981;
    }
    .task-title {
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 0.45rem;
        line-height: 1.4;
    }
    .task-title-done {
        text-decoration: line-through;
        opacity: 0.75;
    }
    .task-meta-row {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.5rem 1rem;
        font-size: 0.83rem;
        opacity: 0.85;
    }

    /* Pills & Badges */
    .badge {
        display: inline-block;
        padding: 0.2rem 0.55rem;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .badge-high {
        background-color: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
    .badge-medium {
        background-color: rgba(245, 158, 11, 0.2);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .badge-low {
        background-color: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .badge-completed {
        background-color: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .badge-pending {
        background-color: rgba(59, 130, 246, 0.2);
        color: #3B82F6;
        border: 1px solid rgba(59, 130, 246, 0.4);
    }
    /* Category Badges */
    .badge-cat {
        background-color: rgba(148, 163, 184, 0.18);
        color: #94A3B8;
        border: 1px solid rgba(148, 163, 184, 0.35);
    }
    .badge-cat-academics {
        background-color: rgba(168, 85, 247, 0.18);
        color: #C084FC;
        border: 1px solid rgba(168, 85, 247, 0.35);
    }
    .badge-cat-project {
        background-color: rgba(6, 182, 212, 0.18);
        color: #22D3EE;
        border: 1px solid rgba(6, 182, 212, 0.35);
    }
    .badge-cat-exam {
        background-color: rgba(244, 63, 94, 0.18);
        color: #FB7185;
        border: 1px solid rgba(244, 63, 94, 0.35);
    }
    .badge-cat-personal {
        background-color: rgba(234, 179, 8, 0.18);
        color: #FACC15;
        border: 1px solid rgba(234, 179, 8, 0.35);
    }
    .badge-cat-work {
        background-color: rgba(59, 130, 246, 0.18);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.35);
    }
    /* Urgency & Deadline Badges */
    .badge-urgency-overdue {
        background-color: rgba(220, 38, 38, 0.25);
        color: #F87171;
        border: 1px solid rgba(220, 38, 38, 0.5);
        font-weight: 800;
    }
    .badge-urgency-due_today {
        background-color: rgba(234, 88, 12, 0.25);
        color: #FB923C;
        border: 1px solid rgba(234, 88, 12, 0.5);
        font-weight: 800;
    }
    .badge-urgency-due_tomorrow {
        background-color: rgba(202, 138, 4, 0.22);
        color: #FACC15;
        border: 1px solid rgba(202, 138, 4, 0.45);
    }
    .badge-urgency-upcoming {
        background-color: rgba(14, 165, 233, 0.18);
        color: #38BDF8;
        border: 1px solid rgba(14, 165, 233, 0.35);
    }
    .meta-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        background: rgba(128, 128, 128, 0.12);
        padding: 0.15rem 0.5rem;
        border-radius: 6px;
    }
    /* Voice Input box */
    .voice-banner {
        background-color: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.75rem;
    }
    
    /* Mobile App Responsive Optimization (Smartphones & Tablets) */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 5rem !important;
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
        }
        .app-title {
            font-size: 1.6rem !important;
        }
        .app-subtitle {
            font-size: 0.85rem !important;
        }
        .task-card {
            padding: 0.85rem !important;
            margin-bottom: 0.5rem !important;
        }
        .task-title {
            font-size: 1rem !important;
        }
        /* Touch target improvements */
        button[kind="primary"], button[kind="secondary"], .stButton > button {
            min-height: 44px !important;
            font-size: 0.95rem !important;
        }
    }
</style>
<head>
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Daily Brain">
    <meta name="theme-color" content="#4F46E5">
    <link rel="manifest" href="/app/static/manifest.json">
    <link rel="apple-touch-icon" href="/app/static/apple-touch-icon.png">
</head>
<script>
    // PWA Service Worker Registration
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('/app/static/sw.js').then(function(registration) {
                console.log('Daily Brain PWA registered: ', registration.scope);
            }, function(err) {
                console.log('Daily Brain PWA registration failed: ', err);
            });
        });
    }
</script>
""", unsafe_allow_html=True)

# --- API Key Detection (Local .env or Streamlit Secrets) ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

# Sidebar fallback if key is missing
if not api_key:
    with st.sidebar:
        st.warning("⚠️ GEMINI_API_KEY not found in environment or secrets.")
        api_key = st.text_input("Enter Gemini API Key:", type="password", help="Grab your free API key at aistudio.google.com")
        if api_key:
            st.success("API Key set for this session!")

# --- Agent Session Initialization ---
if "chat_session" not in st.session_state and api_key:
    try:
        st.session_state.chat_session = create_agent(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize Gemini agent: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar Content ---
with st.sidebar:
    st.markdown("### 🧠 Daily Brain")
    st.caption("AI-Powered Autonomous Task Agent")

    if api_key:
        st.success("🟢 Agent Active (Gemini 3.6 Flash)")
    else:
        st.error("🔴 API Key Required")

    # Mobile & Desktop Install Box
    with st.expander("📲 **Install App on Phone / PC**", expanded=False):
        st.markdown("""
        **Install Daily Brain as a standalone App:**
        
        **🤖 Android (Chrome):**
        1. Open in **Chrome on your phone**: `daily-brain-agent.streamlit.app`
        2. Tap the **Chrome browser menu `⋮`** (at the very top-right of your browser header, next to the URL/tabs).
        3. Tap **"Install app"** or **"Add to Home screen"**.
        
        **🍎 iPhone (Safari):**
        1. Open in **Safari**: `daily-brain-agent.streamlit.app`
        2. Tap **Share** (square with up arrow) ➡️ **"Add to Home Screen"**.
        
        **💻 PC / Laptop:**
        - Click the **Install icon** `⊕` in your browser address bar.
        """)
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://daily-brain-agent.streamlit.app", caption="Scan with phone to open", width=160)

    st.markdown("---")
    st.markdown("#### 🛠️ Available Agent Capabilities")
    st.markdown("""
    - `save_task`: Saves task with priority, due date, category & subtasks
    - `list_tasks`: Retrieves active or completed tasks
    - `get_current_date`: Resolves dynamic dates (e.g. *today*, *Friday*)
    - `complete_task`: Marks tasks as completed
    - `delete_task`: Removes tasks by name/keyword
    - `add_checklist_item`: Adds sub-steps to existing tasks
    - `update_task_category`: Reassigns category tags (#Exam, #Academics)
    - `get_urgent_tasks`: Checks overdue & near deadlines
    - `🎙️ Voice Input`: Native speech-to-text with Gemini transcription
    """)

    st.markdown("---")
    st.markdown("#### 💡 Quick Examples")
    example_prompts = [
        "What tasks are overdue or due soon?",
        "Finish my CN assignment by Friday #Academics",
        "Prepare for DAA test next week #Exam",
        "Mark DAA assignment as done",
        "What tasks are currently pending?"
    ]
    for prompt in example_prompts:
        if st.button(prompt, key=f"quick_{prompt}", use_container_width=True):
            st.session_state["pending_prompt"] = prompt

    st.markdown("---")
    # Real-time Task Metrics
    all_tasks = get_saved_tasks()
    total_count = len(all_tasks)
    pending_count = sum(1 for t in all_tasks if t.get("status") != "completed")
    completed_count = sum(1 for t in all_tasks if t.get("status") == "completed")
    overdue_count = sum(1 for t in all_tasks if get_deadline_status(t)[0] == "overdue" and t.get("status") != "completed")
    high_count = sum(1 for t in all_tasks if t.get("priority") == "high" and t.get("status") != "completed")

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("Pending", pending_count, delta=f"{high_count} High" if high_count else None)
    with col_m2:
        st.metric("Overdue", overdue_count, delta=f"-{overdue_count}" if overdue_count else "0", delta_color="inverse")
    with col_m3:
        st.metric("Done", completed_count)

# --- Header Area ---
st.markdown("""
<div class="app-header">
    <div class="app-title">🧠 Daily Brain</div>
    <div class="app-subtitle">Tell me your thoughts, assignments, and deadlines in plain English — I'll organize, schedule, and track them for you.</div>
</div>
""", unsafe_allow_html=True)

# --- Layout Tabs: Chat & Task Board ---
tab_chat, tab_board = st.tabs(["💬 AI Assistant", "📋 Saved Tasks Board"])

with tab_chat:
    # Clear conversation controls & Voice quick-bar
    col_c1, col_c2 = st.columns([5, 1])
    with col_c1:
        st.caption("💬 Chat with Daily Brain or record voice tasks below:")
    with col_c2:
        if st.button("🧹 Clear", use_container_width=True, help="Clear conversation history without deleting saved tasks"):
            st.session_state.messages = []
            st.session_state.pop("last_voice_text", None)
            if api_key:
                st.session_state.chat_session = create_agent(api_key=api_key)
            st.rerun()

    # --- Feature 4: Voice Input (Speech-to-Text) ---
    with st.expander("🎙️ **Voice Task Input (Speak your tasks & deadlines)**", expanded=False):
        st.markdown(
            "Tap the microphone, speak naturally, and press stop. "
            "Gemini will transcribe your voice and automatically organize, schedule, and categorize your task!\n\n"
            "*Example: \"Finish Computer Networks lab by Friday #Academics with subtasks setup socket, write server, test client\"*"
        )
        voice_audio = st.audio_input("Record voice task", key="voice_task_recorder", label_visibility="collapsed")

        if voice_audio is not None:
            audio_bytes = voice_audio.getvalue()
            if audio_bytes:
                audio_hash = hashlib.md5(audio_bytes).hexdigest()
                if st.session_state.get("last_processed_audio_hash") != audio_hash:
                    if not api_key:
                        st.error("Please provide a Gemini API Key in the sidebar to transcribe voice input.")
                    else:
                        st.session_state["last_processed_audio_hash"] = audio_hash
                        with st.spinner("🎧 Transcribing your voice with Gemini..."):
                            try:
                                transcribed_text = transcribe_audio(audio_bytes, api_key=api_key)
                                if transcribed_text:
                                    st.session_state["pending_prompt"] = transcribed_text
                                    st.session_state["last_voice_text"] = transcribed_text
                                    st.rerun()
                                else:
                                    st.warning("⚠️ No intelligible speech detected. Please speak closer to your microphone.")
                            except Exception as ve:
                                st.error(f"⚠️ Voice transcription error: {ve}")
        else:
            # Clear stored hash when recording is removed/reset
            if "last_processed_audio_hash" in st.session_state:
                del st.session_state["last_processed_audio_hash"]

        if st.session_state.get("last_voice_text"):
            st.info(f"🎙️ **Last Transcribed Input:** *\"{st.session_state['last_voice_text']}\"*")

    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Welcome message if chat is empty
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown(
                "👋 **Hi! I'm your Daily Brain assistant.**\n\n"
                "Tell me what you need to manage via typing or 🎙️ **Voice Input** above:\n"
                "- *\"Finish the CN assignment by Friday #Academics\"* ➡️ Plans, categorizes & schedules\n"
                "- *\"Add subtask review slides to CN assignment\"* ➡️ Adds checklist step\n"
                "- *\"What tasks are overdue or due soon?\"* ➡️ Highlights urgent deadlines\n"
                "- *\"Mark DAA assignment as done\"* ➡️ Checks off the task\n\n"
                "I'll automatically calculate real calendar dates, assign appropriate priorities, and keep your task board in sync!"
            )

    # Handle pending prompt from sidebar quick buttons or voice transcription
    current_prompt = None
    if "pending_prompt" in st.session_state and st.session_state["pending_prompt"]:
        current_prompt = st.session_state.pop("pending_prompt")

    # Chat input box
    chat_input = st.chat_input("Type or use 🎙️ Voice Input above (e.g. Finish DSA assignment by Friday)")
    active_prompt = current_prompt or chat_input

    if active_prompt:
        if not api_key:
            st.error("Please provide a Gemini API Key to use the agent.")
        else:
            # Display user message
            st.session_state.messages.append({"role": "user", "content": active_prompt})
            with st.chat_message("user"):
                st.markdown(active_prompt)

            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("Daily Brain is coordinating tools & scheduling..."):
                    try:
                        if "chat_session" not in st.session_state:
                            st.session_state.chat_session = create_agent(api_key=api_key)

                        response = st.session_state.chat_session.send_message(active_prompt)
                        reply_text = response.text

                        st.markdown(reply_text)
                        st.session_state.messages.append({"role": "assistant", "content": reply_text})
                        st.rerun()
                    except Exception as e:
                        # Auto-recovery: If client was closed, recreate session and retry once
                        if "closed" in str(e).lower():
                            try:
                                st.session_state.chat_session = create_agent(api_key=api_key)
                                response = st.session_state.chat_session.send_message(active_prompt)
                                reply_text = response.text
                                st.markdown(reply_text)
                                st.session_state.messages.append({"role": "assistant", "content": reply_text})
                                st.rerun()
                            except Exception as retry_err:
                                err_msg = f"⚠️ An error occurred while contacting the agent: {retry_err}"
                                st.error(err_msg)
                                st.session_state.messages.append({"role": "assistant", "content": err_msg})
                        else:
                            err_msg = f"⚠️ An error occurred while contacting the agent: {e}"
                            st.error(err_msg)
                            st.session_state.messages.append({"role": "assistant", "content": err_msg})

with tab_board:
    st.markdown("### 📋 Your Stored Tasks (`tasks.json`)")
    tasks = get_saved_tasks()

    if not tasks:
        st.info("No tasks saved yet. Tell the AI assistant about your tasks to get started!")
    else:
        # Due Reminders & Attention Banner
        overdue_tasks = [t for t in tasks if get_deadline_status(t)[0] == "overdue" and t.get("status") != "completed"]
        due_today_tasks = [t for t in tasks if get_deadline_status(t)[0] == "due_today" and t.get("status") != "completed"]

        if overdue_tasks:
            overdue_preview = ", ".join(f"**{t['task']}**" for t in overdue_tasks[:2])
            more_txt = f" (+{len(overdue_tasks)-2} more)" if len(overdue_tasks) > 2 else ""
            st.error(f"🚨 **Attention Required:** You have **{len(overdue_tasks)}** overdue task(s) ({overdue_preview}{more_txt})! Complete or reschedule them.")
        elif due_today_tasks:
            today_preview = ", ".join(f"**{t['task']}**" for t in due_today_tasks[:2])
            more_txt = f" (+{len(due_today_tasks)-2} more)" if len(due_today_tasks) > 2 else ""
            st.warning(f"⚠️ **Due Today:** You have **{len(due_today_tasks)}** task(s) scheduled for today ({today_preview}{more_txt}). Focus on these first!")
        else:
            st.success("✨ **All Caught Up!** You have no overdue deadlines today. Keep up the great work!")

        # Search & Filter Row
        col_search, col_status, col_cat, col_prio, col_sort = st.columns([3, 2.2, 1.8, 1.6, 2.2])
        with col_search:
            search_query = st.text_input("🔍 Search tasks:", placeholder="Type to filter by title...").strip().lower()
        with col_status:
            status_filter = st.selectbox(
                "Status:",
                ["All", "Active / Pending", "🚨 Due Today / Overdue", "Completed"],
                index=0
            )
        with col_cat:
            all_cats = sorted(list(set(t.get("category", "General") for t in tasks)))
            cat_options = ["All"] + all_cats
            category_filter = st.selectbox("Category:", cat_options, index=0)
        with col_prio:
            priority_filter = st.selectbox(
                "Priority:",
                ["All", "High", "Medium", "Low"],
                index=0
            )
        with col_sort:
            sort_order = st.selectbox(
                "Sort by:",
                ["🚨 Urgency (Due Soonest)", "Newest First", "Oldest First"],
                index=0
            )

        # Apply filtering & searching while preserving original indices for deletion/toggle
        indexed_tasks = list(enumerate(tasks))

        # Search filter
        if search_query:
            indexed_tasks = [item for item in indexed_tasks if search_query in item[1].get("task", "").lower()]

        # Status filter
        if status_filter == "Active / Pending":
            indexed_tasks = [item for item in indexed_tasks if item[1].get("status") != "completed"]
        elif status_filter == "🚨 Due Today / Overdue":
            indexed_tasks = [item for item in indexed_tasks if get_deadline_status(item[1])[0] in ["overdue", "due_today"] and item[1].get("status") != "completed"]
        elif status_filter == "Completed":
            indexed_tasks = [item for item in indexed_tasks if item[1].get("status") == "completed"]

        # Category filter
        if category_filter != "All":
            indexed_tasks = [item for item in indexed_tasks if item[1].get("category", "General").lower() == category_filter.lower()]

        # Priority filter
        if priority_filter != "All":
            indexed_tasks = [item for item in indexed_tasks if item[1].get("priority", "").lower() == priority_filter.lower()]

        # Sort order
        if sort_order == "🚨 Urgency (Due Soonest)":
            indexed_tasks.sort(key=lambda item: get_deadline_status(item[1])[2])
        elif sort_order == "Newest First":
            indexed_tasks = list(reversed(indexed_tasks))

        st.caption(f"Showing **{len(indexed_tasks)}** of **{len(tasks)}** total tasks")

        if not indexed_tasks:
            st.warning("No tasks match your selected filter.")
        else:
            for original_idx, item in indexed_tasks:
                task_text = item.get("task", "Untitled Task")
                prio = item.get("priority", "low").lower()
                status = item.get("status", "pending").lower()
                due_date = item.get("due_date", "Not specified")
                saved_at = item.get("saved_at", "Unknown")
                category = item.get("category", "General")
                subtasks = item.get("subtasks", [])

                is_done = (status == "completed")
                prio_class = f"badge-{prio}" if prio in ["high", "medium", "low"] else "badge-low"
                status_class = "badge-completed" if is_done else "badge-pending"
                cat_lower = category.lower()
                cat_class = f"badge-cat-{cat_lower}" if cat_lower in ["academics", "project", "exam", "personal", "work"] else "badge-cat"

                urgency_code, urgency_label, _ = get_deadline_status(item)
                urgency_pill = f'<span class="badge badge-urgency-{urgency_code}">{urgency_label}</span>' if not is_done and urgency_code in ["overdue", "due_today", "due_tomorrow", "upcoming"] else ""

                card_extra = "task-card-completed" if is_done else ""
                title_extra = "task-title-done" if is_done else ""

                completed_subs = sum(1 for s in subtasks if s.get("done"))
                total_subs = len(subtasks)
                subs_meta = f'<span class="meta-pill">📝 {completed_subs}/{total_subs} steps</span>' if total_subs > 0 else ""

                with st.container():
                    col_card, col_action, col_del = st.columns([8, 1.6, 0.8])
                    with col_card:
                        st.markdown(f"""
                        <div class="task-card {card_extra}">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem;">
                                <div class="task-title {title_extra}">{task_text}</div>
                                <div style="display: flex; gap: 0.35rem; align-items: center; flex-wrap: wrap;">
                                    <span class="badge {cat_class}">#{category}</span>
                                    {urgency_pill}
                                    <span class="badge {status_class}">{"DONE" if is_done else "PENDING"}</span>
                                    <span class="badge {prio_class}">{prio.upper()}</span>
                                </div>
                            </div>
                            <div class="task-meta-row">
                                <span class="meta-pill">📅 Due: {due_date}</span>
                                <span class="meta-pill">🕒 Added: {saved_at}</span>
                                {subs_meta}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Subtasks / Checklist expander
                        if total_subs > 0:
                            with st.expander(f"📝 Checklist ({completed_subs}/{total_subs} completed)", expanded=(not is_done and completed_subs < total_subs)):
                                st.progress(completed_subs / total_subs)
                                for sub_idx, sub in enumerate(subtasks):
                                    sc1, sc2 = st.columns([10, 1])
                                    with sc1:
                                        is_sub_done = sub.get("done", False)
                                        chk = st.checkbox(
                                            sub.get("title", ""),
                                            value=is_sub_done,
                                            key=f"chk_{original_idx}_{sub_idx}",
                                            help="Toggle step status"
                                        )
                                        if chk != is_sub_done:
                                            toggle_subtask_status(original_idx, sub_idx)
                                            st.rerun()
                                    with sc2:
                                        if st.button("✕", key=f"del_sub_{original_idx}_{sub_idx}", help="Remove step"):
                                            delete_subtask_by_index(original_idx, sub_idx)
                                            st.rerun()

                                # Quick add step inside existing checklist
                                c_in, c_btn = st.columns([8, 2])
                                with c_in:
                                    new_step_text = st.text_input(
                                        "Add step",
                                        placeholder="+ Add next step...",
                                        key=f"in_step_{original_idx}",
                                        label_visibility="collapsed"
                                    )
                                with c_btn:
                                    if st.button("+ Add", key=f"btn_step_{original_idx}", use_container_width=True):
                                        if new_step_text.strip():
                                            add_subtask_to_task(original_idx, new_step_text.strip())
                                            st.rerun()
                        else:
                            with st.expander("➕ Add checklist steps"):
                                c_in, c_btn = st.columns([8, 2])
                                with c_in:
                                    new_step_text = st.text_input(
                                        "Add step",
                                        placeholder="+ Add first step...",
                                        key=f"in_init_step_{original_idx}",
                                        label_visibility="collapsed"
                                    )
                                with c_btn:
                                    if st.button("+ Add", key=f"btn_init_step_{original_idx}", use_container_width=True):
                                        if new_step_text.strip():
                                            add_subtask_to_task(original_idx, new_step_text.strip())
                                            st.rerun()

                    with col_action:
                        st.write("")
                        btn_label = "↩️ Reopen" if is_done else "✅ Done"
                        if st.button(btn_label, key=f"toggle_{original_idx}", use_container_width=True):
                            toggle_task_status(original_idx)
                            st.rerun()

                    with col_del:
                        st.write("")
                        if st.button("🗑️", key=f"delete_{original_idx}", help="Delete this task", use_container_width=True):
                            delete_task_by_index(original_idx)
                            st.rerun()
