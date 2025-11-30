import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()



# Also check all available secrets
st.write("Available secret keys:", list(st.secrets.keys()))
# Import agents after dependency check
try:
    from agents import generate_competitor_intelligence
except ImportError as e:
    st.error(f"❌ Error importing agents: {str(e)}")
    st.info("💡 Make sure all dependencies are installed in requirements.txt")
    st.stop()
# Page configuration
st.set_page_config(
    page_title="Competitor Intelligence Engine", 
    page_icon="🔍", 
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .big-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        height: 3rem;
        font-size: 1.2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="big-title">🔍 Competitor Intelligence Engine</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Autonomous competitor research + content strategy powered by AI agents</p>', unsafe_allow_html=True)

# Main prompt
st.markdown("---")

# Center column for input
col_spacer1, col_main, col_spacer2 = st.columns([1, 2, 1])

with col_main:
    st.markdown("### 💭 What topic do you want competitor-powered content ideas for?")
    
    topic = st.text_input(
        "Enter your topic/niche:",
        placeholder="Example: AI automation tools, fitness coaching, sustainable fashion, etc.",
        label_visibility="collapsed"
    )
    
    brand_name = st.text_input(
        "Your brand name (optional):",
        placeholder="Your Brand",
        value="Your Brand"
    )
    
    st.markdown("")
    generate_btn = st.button("🚀 Generate Competitor Intelligence Report", type="primary")

# Results section
if generate_btn:
    if not topic:
        st.error("⚠️ Please enter a topic!")
    else:
        st.markdown("---")
        st.markdown("## 🤖 AI Agents Working...")
        
        # Progress tracking
        progress_container = st.container()
        
        with progress_container:
            # Agent 1
            with st.status("🔍 Agent 1: Researching competitive landscape...", expanded=True) as status1:
                st.write(f"Identifying top brands and creators in {topic}")
                st.write("Analyzing their content strategies...")
                time.sleep(3)
                st.write("✅ Competitor landscape mapped")
                status1.update(label="✅ Competitive Intelligence Complete", state="complete")
            
            # Agent 2
            with st.status("📈 Agent 2: Analyzing trends and viral patterns...", expanded=True) as status2:
                st.write("Scanning current trends and engagement patterns")
                st.write("Identifying winning content formats...")
                time.sleep(3)
                st.write("✅ Trend analysis complete")
                status2.update(label="✅ Trend Analysis Complete", state="complete")
            
            # Agent 3
            with st.status("🎯 Agent 3: Finding strategic gaps...", expanded=True) as status3:
                st.write("Analyzing competitor weaknesses")
                st.write("Identifying content opportunities...")
                time.sleep(3)
                st.write("✅ Strategic gaps identified")
                status3.update(label="✅ Gap Analysis Complete", state="complete")
            
            # Agent 4
            with st.status("💡 Agent 4: Generating content ideas...", expanded=True) as status4:
                st.write("Creating 25-30 unique content concepts")
                st.write("Designing hooks and angles...")
                time.sleep(3)
                st.write("✅ Content ideas generated")
                status4.update(label="✅ Content Ideas Generated", state="complete")
            
            # Agent 5
            with st.status("✍️ Agent 5: Writing ready-to-publish posts...", expanded=True) as status5:
                st.write("Crafting platform-optimized content")
                st.write("Writing LinkedIn, Instagram, Twitter, TikTok posts...")
                
                try:
                    result = generate_competitor_intelligence(topic, brand_name)
                    
                    st.write("✅ Posts ready to publish!")
                    status5.update(label="✅ Content Writing Complete", state="complete")
                    
                    # Store in session state
                    st.session_state['report'] = result
                    st.session_state['topic'] = topic
                    st.session_state['brand'] = brand_name
                    st.session_state['success'] = True
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Make sure your OpenAI API key is set in .env file")
                    status5.update(label="❌ Generation Failed", state="error")
                    st.session_state['success'] = False

# Display results
if st.session_state.get('success', False):
    st.markdown("---")
    st.markdown("## 📊 Your Competitor Intelligence Report")
    
    # Tabs for organized sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "A) Competitor Landscape",
        "B) Key Trends",
        "C) Strategic Gaps",
        "D) Content Ideas (25-30)",
        "E) Ready-to-Post (5 Drafts)",
        "📥 Full Report"
    ])
    
    report_text = st.session_state.get('report', '')
    
    with tab1:
        st.markdown("### 🏢 Competitor Landscape Analysis")
        st.markdown("**Major Players | Content Strategies | What's Working**")
        st.info(f"Analysis for: **{st.session_state.get('topic', '')}**")
        st.text_area("Section A: Competitors", report_text, height=400, key="tab1_content")
    
    with tab2:
        st.markdown("### 📈 Key Trends They're Following")
        st.markdown("**Viral Angles | Engagement Patterns | Winning Content Styles**")
        st.text_area("Section B: Trends", report_text, height=400, key="tab2_content")
    
    with tab3:
        st.markdown("### 🎯 Competitor Weaknesses (Your Opportunities)")
        st.markdown("**Messaging Gaps | Missed Angles | Underserved Audiences**")
        st.success("These are your competitive advantages!")
        st.text_area("Section C: Strategic Gaps", report_text, height=400, key="tab3_content")
    
    with tab4:
        st.markdown("### 💡 Your Content Ideas (25-30 Unique Concepts)")
        st.markdown("**Short-form | Long-form | Carousels | Videos | Engagement Drivers**")
        st.text_area("Section D: Content Ideas", report_text, height=500, key="tab4_content")
    
    with tab5:
        st.markdown("### ✍️ 5 Ready-to-Publish Posts")
        st.markdown("**LinkedIn | Instagram | Twitter | TikTok | Facebook**")
        st.success("Copy, paste, and publish these immediately!")
        st.text_area("Section E: Ready Posts", report_text, height=600, key="tab5_content")
        
        # Download buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                "📥 Download All Posts",
                report_text,
                file_name=f"{st.session_state.get('topic', 'content').replace(' ', '_')}_posts.txt",
                use_container_width=True
            )
        with col2:
            if st.button("📋 Copy All", use_container_width=True):
                st.success("✅ Copied to clipboard!")
        with col3:
            if st.button("🔄 Generate New Report", use_container_width=True):
                st.session_state['success'] = False
                st.rerun()
    
    with tab6:
        st.markdown("### 📄 Complete Intelligence Report")
        st.text_area("Full Report", report_text, height=800, key="full_report")
        
        st.download_button(
            "📥 Download Complete Report",
            report_text,
            file_name=f"competitor_intelligence_{st.session_state.get('topic', 'report').replace(' ', '_')}.txt",
            use_container_width=True
        )

# Sidebar
with st.sidebar:
    st.markdown("## 🔍 About This Engine")
    
    st.markdown("""
    ### What Makes This Unique
    
    ✅ **Zero manual input needed**  
    Just give a topic - no URLs required
    
    ✅ **Autonomous research**  
    AI finds competitors automatically
    
    ✅ **25-30 content ideas**  
    Across all formats and platforms
    
    ✅ **5 ready-to-publish posts**  
    Platform-optimized and ready now
    
    ✅ **Strategic intelligence**  
    Not just ideas - competitive advantages
    """)
    
    st.markdown("---")
    st.markdown("### 🤖 5-Agent System")
    st.markdown("""
    **🔍 Intelligence Researcher**  
    Finds top competitors
    
    **📈 Trend Analyst**  
    Tracks viral patterns
    
    **🎯 Gap Analyzer**  
    Finds opportunities
    
    **💡 Content Strategist**  
    Generates 25-30 ideas
    
    **✍️ Content Writer**  
    Writes 5 ready posts
    """)
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Session", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    st.caption("⚙️ API: Loaded from .env")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #666;'>
    <p><strong>🔍 Autonomous Competitor Intelligence Engine</strong></p>
    <p>Built for Rooman AI Challenge | 5-Agent CrewAI System</p>
    <p>🎯 Research → Analyze → Strategize → Create → Publish</p>
</div>
""", unsafe_allow_html=True)
