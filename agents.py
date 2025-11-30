from crewai import Agent, Task, Crew
from analyzer import research_competitors, analyze_trends, find_content_gaps
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

# Get API key from Streamlit secrets or environment
try:
    import streamlit as st
    gemini_api_key = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
except:
    gemini_api_key = os.getenv("GOOGLE_API_KEY")

if not gemini_api_key:
    raise ValueError("❌ GOOGLE_API_KEY not found!")

# Configure Gemini LLM - use gemini/ prefix for LiteLLM
from litellm import completion
import os

os.environ["GEMINI_API_KEY"] = gemini_api_key

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=gemini_api_key,
    temperature=0.7
)



print(f"✅ Using Gemini 1.5 Flash")

# Agent 1: Competitor Intelligence Researcher
intelligence_agent = Agent(
    role='Competitive Intelligence Researcher',
    goal='Identify and analyze top competitors, their strategies, and market positioning in the {topic} space',
    backstory="""You are an expert competitive intelligence analyst with 10+ years of experience 
    researching market leaders. You excel at identifying key players, understanding their content 
    strategies, and spotting patterns in what makes competitors successful.""",
    tools=[research_competitors],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

# Agent 2: Trend Analysis Specialist
trend_agent = Agent(
    role='Trend Analysis Specialist',
    goal='Discover viral content patterns, trending topics, and engagement drivers in the {topic} niche',
    backstory="""You are a trend forecasting expert who can spot emerging patterns before they 
    go mainstream. You understand what makes content viral and can identify the hooks, angles, 
    and formats that drive maximum engagement.""",
    tools=[analyze_trends],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

# Agent 3: Strategic Gap Analyzer
gap_agent = Agent(
    role='Strategic Gap Analyzer',
    goal='Identify underserved audiences, missed content angles, and opportunities competitors are ignoring',
    backstory="""You are a strategic consultant who specializes in finding white space opportunities. 
    You can see what competitors are missing and identify content gaps that represent untapped 
    potential for engagement and authority building.""",
    tools=[find_content_gaps],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

# Agent 4: Content Strategist & Creator
content_strategist = Agent(
    role='Content Strategist & Idea Generator',
    goal='Generate 25-30 unique, high-value content ideas that fill gaps and outperform competitors',
    backstory="""You are a creative content strategist who combines competitive intelligence with 
    audience psychology. You craft content ideas that stop scrolls, spark conversations, and 
    establish thought leadership. You understand different content formats (carousels, threads, 
    videos, long-form) and can adapt ideas for maximum impact.""",
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

# Agent 5: Multi-Platform Content Writer
content_writer = Agent(
    role='Multi-Platform Content Writer',
    goal='Write 5 platform-optimized posts ready for LinkedIn, Instagram, Twitter, TikTok, and Facebook',
    backstory="""You are a multi-platform content writer who understands the unique voice, format, 
    and engagement patterns of each social platform. You write hooks that grab attention, body 
    content that delivers value, and CTAs that drive action. You know LinkedIn prefers professional 
    insights, Instagram loves storytelling with visuals, Twitter rewards punchy threads, TikTok 
    thrives on hooks and quick value, and Facebook builds community through relatable content.""",
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

def generate_competitor_intelligence(topic: str, brand_name: str) -> dict:
    """
    Orchestrates the 5-agent system to generate comprehensive competitor intelligence and content strategy.
    """
    
    # Task 1: Research Competitors
    research_task = Task(
        description=f"""
        Research and analyze the top 5-10 competitors in the {topic} space. Identify:
        1. Who are the major players and thought leaders
        2. What content formats they use (videos, carousels, threads, articles)
        3. What topics and themes they cover most
        4. Their engagement patterns and audience size
        5. What makes their best-performing content successful
        
        Topic: {topic}
        Brand: {brand_name}
        """,
        agent=intelligence_agent,
        expected_output="Detailed competitor analysis with 5-10 major players, their strategies, and content patterns"
    )
    
    # Task 2: Analyze Trends
    trend_task = Task(
        description=f"""
        Based on the competitor research, analyze trending content in the {topic} niche. Identify:
        1. What content angles are getting the most engagement right now
        2. Emerging topics and themes gaining traction
        3. Viral content patterns (hooks, formats, storytelling styles)
        4. What types of posts are performing best (educational, inspirational, controversial, etc.)
        5. Timing and frequency patterns of top performers
        
        Topic: {topic}
        """,
        agent=trend_agent,
        expected_output="Trend analysis report with viral patterns, top-performing content types, and engagement drivers"
    )
    
    # Task 3: Find Content Gaps
    gap_task = Task(
        description=f"""
        Identify strategic content gaps and opportunities that competitors are missing. Find:
        1. Underserved audience segments or pain points not being addressed
        2. Content formats competitors aren't using effectively
        3. Topics with high demand but low quality supply
        4. Unique angles and perspectives that could differentiate {brand_name}
        5. Opportunities to provide more depth, clarity, or value than competitors
        
        Topic: {topic}
        Brand: {brand_name}
        """,
        agent=gap_agent,
        expected_output="Gap analysis with 5-7 major opportunities for differentiation and unique content angles"
    )
    
    # Task 4: Generate Content Ideas
    content_ideas_task = Task(
        description=f"""
        Based on competitor research, trends, and gaps, generate 25-30 unique content ideas for {brand_name}.
        
        Requirements:
        - Each idea should fill a gap or outperform competitors
        - Include diverse formats: carousels, threads, videos, long-form posts, polls, stories
        - Mix content types: educational, inspirational, controversial, behind-the-scenes, case studies
        - Include attention-grabbing hooks for each idea
        - Categorize ideas by platform suitability (LinkedIn, Instagram, Twitter, TikTok, Facebook)
        - Ensure ideas are specific, actionable, and unique to {brand_name}
        
        Topic: {topic}
        Brand: {brand_name}
        """,
        agent=content_strategist,
        expected_output="25-30 unique content ideas with hooks, formats, and platform recommendations"
    )
    
    # Task 5: Write Platform-Specific Posts
    content_writing_task = Task(
        description=f"""
        Write 5 complete, ready-to-publish posts for {brand_name}, one for each platform:
        
        1. LINKEDIN POST:
           - Professional tone with valuable insights
           - 1200-1500 characters
           - Strong hook, 3-5 key points, clear CTA
           - Include relevant hashtags (5-8)
        
        2. INSTAGRAM CAPTION:
           - Storytelling approach with visual cues
           - 1000-1300 characters
           - Engaging hook, narrative flow, emotion
           - 10-15 relevant hashtags
           - Mention "Link in bio" or CTA
        
        3. TWITTER/X THREAD:
           - 5-7 tweets forming a cohesive thread
           - First tweet = killer hook
           - Each tweet = one clear point
           - Final tweet = CTA or summary
           - Conversational, punchy tone
        
        4. TIKTOK SCRIPT:
           - Hook in first 3 seconds
           - Visual cues for video editing
           - 60-90 seconds of content
           - Clear value delivery
           - Trending sound suggestions
        
        5. FACEBOOK POST:
           - Community-building tone
           - Question or discussion starter
           - 500-800 characters
           - Relatable and conversational
           - Encourages comments and shares
        
        Topic: {topic}
        Brand: {brand_name}
        
        Make each post authentic to the platform while maintaining {brand_name}'s voice.
        """,
        agent=content_writer,
        expected_output="5 complete, platform-optimized posts ready for publishing"
    )
    
    # Create and run the crew
    crew = Crew(
        agents=[intelligence_agent, trend_agent, gap_agent, content_strategist, content_writer],
        tasks=[research_task, trend_task, gap_task, content_ideas_task, content_writing_task],
        verbose=True
    )
    
    # Execute the crew
    result = crew.kickoff()
    
    return {
        'competitor_research': research_task.output,
        'trend_analysis': trend_task.output,
        'content_gaps': gap_task.output,
        'content_ideas': content_ideas_task.output,
        'platform_posts': content_writing_task.output,
        'full_report': result
    }
