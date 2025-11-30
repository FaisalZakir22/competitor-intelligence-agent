import streamlit as st
import time

# Import agents after Streamlit is loaded
try:
    from agents import generate_competitor_intelligence
except Exception as e:
    st.error(f"❌ Error loading agents: {str(e)}")
    st.stop()

# Page config with custom theme
st.set_page_config(
    page_title="Competitor Intelligence Engine",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for midnight purple aesthetic
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container - Midnight Purple Background */
    .main {
        background: linear-gradient(135deg, #1a0b2e 0%, #2d1b4e 50%, #1a0b2e 100%);
        background-attachment: fixed;
    }
    
    /* Animated background particles */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 30%, rgba(138, 92, 246, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(196, 181, 253, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(167, 139, 250, 0.05) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Content wrapper */
    .block-container {
        max-width: 1200px;
        padding: 3rem 2rem;
        background: rgba(30, 20, 50, 0.6);
        border-radius: 24px;
        border: 1px solid rgba(167, 139, 250, 0.2);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        position: relative;
        z-index: 1;
    }
    
    /* Hero section */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a78bfa 0%, #c4b5fd 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        line-height: 1.2;
        text-shadow: 0 0 40px rgba(167, 139, 250, 0.3);
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #c4b5fd;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 400;
        text-shadow: 0 2px 10px rgba(167, 139, 250, 0.3);
    }
    
    .hero-description {
        font-size: 1rem;
        color: #d4c5f9;
        text-align: center;
        max-width: 700px;
        margin: 0 auto 2rem auto;
        line-height: 1.7;
    }
    
    /* Feature badges */
    .feature-badges {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin-bottom: 3rem;
    }
    
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1.2rem;
        background: rgba(167, 139, 250, 0.15);
        border: 1px solid rgba(167, 139, 250, 0.3);
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 500;
        color: #c4b5fd;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .badge:hover {
        background: rgba(167, 139, 250, 0.25);
        border-color: rgba(167, 139, 250, 0.5);
        transform: translateY(-2px);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 1px solid rgba(167, 139, 250, 0.3);
        padding: 0.9rem 1.3rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: rgba(30, 20, 50, 0.5);
        color: #e9d5ff;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #a78bfa;
        opacity: 0.6;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #a78bfa;
        box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.2);
        background: rgba(30, 20, 50, 0.7);
        outline: none;
    }
    
    .stTextInput label {
        color: #c4b5fd !important;
        font-weight: 500;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(139, 92, 246, 0.6);
    }
    
    /* Progress section */
    .progress-container {
        background: rgba(30, 20, 50, 0.4);
        padding: 2rem;
        border-radius: 16px;
        margin: 2rem 0;
        border: 1px solid rgba(167, 139, 250, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .progress-container h3 {
        color: #c4b5fd;
    }
    
    .agent-card {
        background: rgba(45, 27, 78, 0.5);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        border-left: 4px solid #a78bfa;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .agent-card:hover {
        transform: translateX(8px);
        box-shadow: 0 6px 25px rgba(167, 139, 250, 0.3);
        background: rgba(45, 27, 78, 0.7);
    }
    
    .agent-card strong {
        color: #e9d5ff;
    }
    
    .agent-card small {
        color: #c4b5fd;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(30, 20, 50, 0.4);
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid rgba(167, 139, 250, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.8rem 1.5rem;
        font-weight: 500;
        color: #c4b5fd;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
        color: white;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(167, 139, 250, 0.2);
    }
    
    /* Markdown content in tabs */
    .stMarkdown {
        color: #e9d5ff;
    }
    
    /* Result header */
    .result-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #e9d5ff;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #a78bfa;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        color: #6ee7b7;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        color: #fca5a5;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 12px;
        color: #93c5fd;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(16, 185, 129, 0.5);
    }
    
    /* Success box */
    .success-box {
        text-align: center;
        padding: 2rem;
        background: rgba(16, 185, 129, 0.1);
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 2px solid rgba(16, 185, 129, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .success-box h2 {
        color: #6ee7b7;
        margin: 0;
    }
    
    .success-box p {
        color: #a7f3d0;
        margin-top: 0.5rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #a78bfa;
        font-size: 0.9rem;
        margin-top: 3rem;
    }
    
    .footer p {
        color: #c4b5fd;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #8b5cf6 0%, #a78bfa 100%);
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(167, 139, 250, 0.5);
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(167, 139, 250, 0.3) 50%, transparent 100%);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(167, 139, 250, 0.3); }
        50% { box-shadow: 0 0 40px rgba(167, 139, 250, 0.5); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    .animate-glow {
        animation: glow 2s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<h1 class="hero-title animate-fade-in">🌙 AI Competitor Intelligence Engine</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Powered by 5 Autonomous AI Agents | CrewAI + Gemini</p>', unsafe_allow_html=True)
st.markdown('''
<p class="hero-description">
    Transform competitor research into actionable content strategy. Our AI agents analyze your niche, 
    identify gaps, and generate platform-optimized content in minutes.
</p>
''', unsafe_allow_html=True)

# Feature Badges
st.markdown('''
<div class="feature-badges">
    <span class="badge">✨ Zero Manual Research</span>
    <span class="badge">🎯 25-30 Content Ideas</span>
    <span class="badge">📱 5 Platform Posts</span>
    <span class="badge">⚡ 5-Agent System</span>
</div>
''', unsafe_allow_html=True)

# Spacer
st.markdown("<br>", unsafe_allow_html=True)

# Input Form
with st.form("intelligence_form", clear_on_submit=False):
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        topic = st.text_input(
            "🎯 Topic or Niche",
            placeholder="e.g., AI productivity tools, sustainable fashion",
            help="Enter the industry or niche you want to analyze",
            label_visibility="visible"
        )
    
    with col2:
        brand_name = st.text_input(
            "🏢 Your Brand Name",
            placeholder="e.g., TechVision, GreenStyle",
            help="Your company or personal brand name",
            label_visibility="visible"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button("🚀 Generate Intelligence Report", use_container_width=True)

# Process Submission
if submit:
    if not topic or not brand_name:
        st.error("⚠️ Please fill in both fields to continue!")
    else:
        # Progress Section
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="progress-container">', unsafe_allow_html=True)
            st.markdown("### 🤖 AI Agents Working")
            st.markdown("*Watch our intelligent agents collaborate in real-time*")
            
            progress_bar = st.progress(0, text="Initializing agents...")
            status_placeholder = st.empty()
            
            # Agent Progress Animation
            agents = [
                ("🔍 Competitive Intelligence Researcher", "Analyzing top competitors and their strategies..."),
                ("📊 Trend Analysis Specialist", "Identifying viral patterns and engagement drivers..."),
                ("🎯 Strategic Gap Analyzer", "Finding underserved opportunities..."),
                ("💡 Content Strategist", "Generating 25-30 unique content ideas..."),
                ("✍️ Multi-Platform Writer", "Crafting platform-optimized posts...")
            ]
            
            for i, (agent_name, agent_desc) in enumerate(agents):
                progress = int((i + 1) / len(agents) * 100)
                progress_bar.progress(progress, text=f"Agent {i+1}/5 Active")
                
                status_placeholder.markdown(f'''
                <div class="agent-card">
                    <strong>{agent_name}</strong><br>
                    <small>{agent_desc}</small>
                </div>
                ''', unsafe_allow_html=True)
                
                time.sleep(0.8)
            
            # Execute AI Crew
            try:
                with st.spinner("🧠 Deep analysis in progress..."):
                    result = generate_competitor_intelligence(topic, brand_name)
                
                progress_bar.progress(100, text="✅ Complete!")
                status_placeholder.success("🎉 **All agents completed successfully!**")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Results Section
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.balloons()
                
                st.markdown('''
                <div class="success-box">
                    <h2>✅ Intelligence Report Generated</h2>
                    <p>Your comprehensive content strategy is ready</p>
                </div>
                ''', unsafe_allow_html=True)
                
                # Tabs for Results
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "🔍 Competitor Research",
                    "📈 Trend Analysis",
                    "🎯 Content Gaps",
                    "💡 Content Ideas (25-30)",
                    "✍️ Platform Posts (5)"
                ])
                
                with tab1:
                    st.markdown('<p class="result-header">Competitive Intelligence Report</p>', unsafe_allow_html=True)
                    st.markdown(str(result.get('competitor_research', 'No data available')))
                
                with tab2:
                    st.markdown('<p class="result-header">Trending Content Patterns</p>', unsafe_allow_html=True)
                    st.markdown(str(result.get('trend_analysis', 'No data available')))
                
                with tab3:
                    st.markdown('<p class="result-header">Strategic Content Gaps</p>', unsafe_allow_html=True)
                    st.markdown(str(result.get('content_gaps', 'No data available')))
                
                with tab4:
                    st.markdown('<p class="result-header">Unique Content Ideas</p>', unsafe_allow_html=True)
                    st.markdown(str(result.get('content_ideas', 'No data available')))
                
                with tab5:
                    st.markdown('<p class="result-header">Ready-to-Publish Posts</p>', unsafe_allow_html=True)
                    st.markdown(str(result.get('platform_posts', 'No data available')))
                
                # Download Section
                st.markdown("<br><br>", unsafe_allow_html=True)
                
                full_report = f"""
# 🌙 COMPETITOR INTELLIGENCE REPORT
**Topic:** {topic}
**Brand:** {brand_name}
**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}

---

## 🔍 COMPETITOR RESEARCH
{result.get('competitor_research', 'N/A')}

---

## 📈 TREND ANALYSIS
{result.get('trend_analysis', 'N/A')}

---

## 🎯 CONTENT GAPS
{result.get('content_gaps', 'N/A')}

---

## 💡 CONTENT IDEAS
{result.get('content_ideas', 'N/A')}

---

## ✍️ PLATFORM POSTS
{result.get('platform_posts', 'N/A')}
"""
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.download_button(
                        label="📥 Download Complete Report",
                        data=full_report,
                        file_name=f"competitor_intelligence_{topic.replace(' ', '_')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
            except Exception as e:
                progress_bar.empty()
                status_placeholder.error(f"❌ **Error:** {str(e)}")
                st.error(f"**Details:** {str(e)}")
                st.info("💡 Tip: Verify your API key is valid and has sufficient quota.")

# Footer
st.markdown('''
<div class="footer">
    <p style="font-weight: 600;">Built with ❤️ using CrewAI + Gemini</p>
    <p>5-Agent Autonomous System | Multi-Platform Content Generation</p>
</div>
''', unsafe_allow_html=True)
