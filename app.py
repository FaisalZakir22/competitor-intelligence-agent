import streamlit as st
import time

# Import agents after Streamlit is loaded
try:
    from agents import generate_competitor_intelligence
except Exception as e:
    st.error(f"❌ Error loading agents: {str(e)}")
    st.stop()

# Page config
st.set_page_config(
    page_title="Competitor Intelligence Agent",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 Autonomous Competitor Intelligence Engine")
st.markdown("*Powered by 5 AI Agents | CrewAI + Gemini*")

# Description
st.markdown("""
This AI system analyzes competitors, identifies content gaps, and generates:
- ✅ **25-30 unique content ideas**
- ✅ **5 ready-to-publish posts** (LinkedIn, Instagram, Twitter, TikTok, Facebook)
""")

# Input form
with st.form("intelligence_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.text_input(
            "🎯 Topic/Niche",
            placeholder="e.g., AI productivity tools, fitness coaching",
            help="Enter the niche or topic you want to analyze"
        )
    
    with col2:
        brand_name = st.text_input(
            "🏢 Your Brand Name",
            placeholder="e.g., MyBrand, TechStartup",
            help="Your brand or company name"
        )
    
    submit = st.form_submit_button("🚀 Generate Competitor Intelligence Report", use_container_width=True)

# Process form submission
if submit:
    if not topic or not brand_name:
        st.error("⚠️ Please fill in both fields!")
    else:
        # Progress tracking
        progress_container = st.container()
        
        with progress_container:
            st.markdown("---")
            st.subheader("🔄 Agents Working...")
            
            # Agent status
            agent_status = st.empty()
            progress_bar = st.progress(0)
            
            # Simulate agent progress (since CrewAI doesn't provide real-time updates)
            agents = [
                "🔍 Researching Competitors",
                "📊 Analyzing Trends",
                "🎯 Finding Content Gaps",
                "💡 Generating Content Ideas",
                "✍️ Crafting Platform Posts"
            ]
            
            # Show progress
            for i, agent in enumerate(agents):
                agent_status.info(f"**Agent {i+1}/5:** {agent}")
                progress_bar.progress((i + 1) * 20)
                time.sleep(0.5)  # Brief delay for UX
            
            # Run the crew
            try:
                with st.spinner("🤖 AI Agents analyzing..."):
                    result = generate_competitor_intelligence(topic, brand_name)
                
                agent_status.success("✅ All agents completed successfully!")
                progress_bar.progress(100)
                
                # Display results
                st.markdown("---")
                st.success("🎉 **Report Generated Successfully!**")
                
                # Results tabs
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "📊 Competitor Research",
                    "📈 Trend Analysis",
                    "🎯 Content Gaps",
                    "💡 Content Ideas (25-30)",
                    "✍️ Platform Posts (5)"
                ])
                
                with tab1:
                    st.markdown("### 🔍 Competitor Intelligence Report")
                    st.markdown(str(result.get('competitor_research', 'No data')))
                
                with tab2:
                    st.markdown("### 📈 Trending Content Patterns")
                    st.markdown(str(result.get('trend_analysis', 'No data')))
                
                with tab3:
                    st.markdown("### 🎯 Strategic Content Gaps")
                    st.markdown(str(result.get('content_gaps', 'No data')))
                
                with tab4:
                    st.markdown("### 💡 25-30 Unique Content Ideas")
                    st.markdown(str(result.get('content_ideas', 'No data')))
                
                with tab5:
                    st.markdown("### ✍️ Ready-to-Publish Posts")
                    st.markdown(str(result.get('platform_posts', 'No data')))
                
                # Download button
                st.markdown("---")
                full_report = f"""
# COMPETITOR INTELLIGENCE REPORT
**Topic:** {topic}
**Brand:** {brand_name}

## COMPETITOR RESEARCH
{result.get('competitor_research', 'N/A')}

## TREND ANALYSIS
{result.get('trend_analysis', 'N/A')}

## CONTENT GAPS
{result.get('content_gaps', 'N/A')}

## CONTENT IDEAS
{result.get('content_ideas', 'N/A')}

## PLATFORM POSTS
{result.get('platform_posts', 'N/A')}
"""
                
                st.download_button(
                    label="📥 Download Full Report",
                    data=full_report,
                    file_name=f"competitor_intelligence_{topic.replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            except Exception as e:
                agent_status.error(f"❌ Error: {str(e)}")
                st.error(f"**Error Details:** {str(e)}")
                st.info("💡 Make sure your API key is valid and has sufficient quota.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with CrewAI + Gemini | 5-Agent Multi-Platform System</p>
</div>
""", unsafe_allow_html=True)
