from crewai import Agent, Task, Crew
from analyzer import research_competitors, analyze_trends, find_content_gaps
from dotenv import load_dotenv
import os

load_dotenv()

# Use GEMINI PRO (NO RATE LIMITS!)
gemini_api_key = os.getenv("GOOGLE_API_KEY")

if not gemini_api_key:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file!")

# Configure Gemini for CrewAI
os.environ["OPENAI_API_KEY"] = gemini_api_key
os.environ["OPENAI_API_BASE"] = "https://generativelanguage.googleapis.com/v1beta/openai/"
os.environ["OPENAI_MODEL_NAME"] = "gemini-1.5-flash"

print(f"✅ Using Gemini Pro API")



# Agent 1: Competitor Intelligence Researcher
intelligence_agent = Agent(
    role='Competitive Intelligence Researcher',
    goal='Identify and analyze top competitors, brands, and creators in the {topic} space',
    backstory="""You are an elite market researcher with deep expertise in competitive analysis.
    You can identify the major players in any niche, understand their content strategies,
    and recognize what makes them successful. You have access to broad market knowledge
    and can spot trends across platforms.""",
    tools=[research_competitors],
    verbose=True,
    allow_delegation=False
)

# Agent 2: Trend Analysis Specialist
trend_analyst = Agent(
    role='Trend Analysis Specialist',
    goal='Analyze current content trends, viral angles, and winning formats for {topic}',
    backstory="""You are a trend forecasting expert who understands social media algorithms,
    audience psychology, and viral mechanics. You can identify what content formats are
    currently winning, what hooks are working, and predict what will resonate with audiences.
    You track engagement patterns across all major platforms.""",
    tools=[analyze_trends],
    verbose=True,
    allow_delegation=False
)

# Agent 3: Strategic Gap Analyzer
gap_analyst = Agent(
    role='Strategic Opportunity Analyst',
    goal='Identify content gaps, missed opportunities, and competitive weaknesses in {topic}',
    backstory="""You are a strategic analyst who excels at finding opportunities others miss.
    You can analyze competitor strategies and identify exactly where they're weak,
    what audiences they're ignoring, and what angles they haven't covered. You find
    the white space where new brands can win.""",
    tools=[find_content_gaps],
    verbose=True,
    allow_delegation=False
)

# Agent 4: Content Strategist & Creator
content_creator = Agent(
    role='Strategic Content Creator',
    goal='Generate unique, competitor-inspired content ideas that outperform the market',
    backstory="""You are a brilliant content strategist and creator who can generate
    dozens of unique, engaging content ideas. You understand how to take market insights
    and turn them into viral content. You create hooks that stop scrolls, angles that
    engage audiences, and ideas that fill gaps competitors missed. Your content always
    stands out and performs exceptionally well.""",
    verbose=True,
    allow_delegation=False
)

# Agent 5: Multi-Platform Content Writer
content_writer = Agent(
    role='Multi-Platform Content Specialist',
    goal='Write polished, ready-to-publish posts optimized for each platform',
    backstory="""You are an expert copywriter who understands the nuances of every platform.
    You write LinkedIn posts that drive professional engagement, Instagram captions that
    inspire action, Twitter threads that go viral, and TikTok scripts that hook viewers
    in 3 seconds. Each post you create is platform-optimized and ready to publish.""",
    verbose=True,
    allow_delegation=False
)

def generate_competitor_intelligence(topic: str, brand_name: str = "Your Brand"):
    """
    Generates comprehensive competitor intelligence and content strategy for a given topic
    """
    
    # Task 1: Research Competitive Landscape
    research_task = Task(
        description=f"""Research and identify the competitive landscape for: {topic}
        
        Provide a comprehensive analysis including:
        
        1. TOP 5-10 MAJOR PLAYERS:
           - List the biggest brands, creators, and companies dominating this niche
           - Include both established brands and rising stars
        
        2. THEIR CONTENT STRATEGIES:
           - What types of content they post (educational, entertaining, promotional, etc.)
           - What formats they use (carousels, videos, threads, single posts)
           - What themes they focus on
        
        3. WHAT'S WORKING FOR THEM:
           - High-engagement content patterns
           - Successful angles and approaches
           - Audience response patterns
        
        Be specific with examples and insights.""",
        agent=intelligence_agent,
        expected_output='Detailed competitor landscape with 5-10 major players and their strategies'
    )
    
    # Task 2: Analyze Trends
    trend_task = Task(
        description=f"""Analyze current content trends and viral patterns in the {topic} space.
        
        Identify:
        
        1. VIRAL ANGLES:
           - What hooks and angles are getting traction
           - What narratives are resonating
           - What emotional triggers are working
        
        2. ENGAGEMENT PATTERNS:
           - What content gets comments vs shares
           - What formats drive highest engagement
           - Best posting times and frequencies
        
        3. WINNING CONTENT STYLES:
           - Educational deep-dives
           - Quick tips and hacks
           - Personal stories
           - Data-driven insights
           - Behind-the-scenes content
           - Controversial takes
        
        Focus on what's trending RIGHT NOW, not last year.""",
        agent=trend_analyst,
        expected_output='Comprehensive trend analysis with specific viral angles and patterns'
    )
    
    # Task 3: Find Strategic Gaps
    gap_task = Task(
        description=f"""Based on the competitor landscape analysis, identify strategic opportunities.
        
        Find:
        
        1. COMPETITOR WEAKNESSES:
           - Gaps in their messaging
           - Topics they avoid
           - Angles they miss
           - Audience questions they don't answer
        
        2. MISSED ANGLES:
           - Perspectives not being shared
           - Content formats underutilized
           - Storytelling opportunities
        
        3. UNDERSERVED AUDIENCES:
           - Demographic segments being ignored
           - Pain points not addressed
           - Questions left unanswered
        
        These gaps are where {brand_name} can win and differentiate.""",
        agent=gap_analyst,
        expected_output='Strategic gap analysis with specific opportunities for differentiation'
    )
    
    # Task 4: Generate Content Ideas
    content_ideas_task = Task(
        description=f"""Generate 25-30 unique, competitor-inspired content ideas for {brand_name} about {topic}.
        
        Create ideas across these categories:
        
        1. SHORT-FORM IDEAS (8-10 ideas):
           - Quick tips
           - Stats/facts
           - Myth-busters
           - Hot takes
        
        2. LONG-FORM IDEAS (5-7 ideas):
           - Deep-dive guides
           - Case studies
           - Personal stories
           - Industry analyses
        
        3. CAROUSEL/THREAD IDEAS (5-7 ideas):
           - Step-by-step tutorials
           - Frameworks
           - Checklists
           - Comparison posts
        
        4. VIDEO/REEL IDEAS (5-7 ideas):
           - How-to demonstrations
           - Behind-the-scenes
           - Reactions
           - Quick explainers
        
        5. ENGAGEMENT DRIVERS (3-5 ideas):
           - Questions/polls
           - Fill-in-the-blank
           - This or that
           - Controversial discussions
        
        Each idea must:
        - Fill a gap competitors missed
        - Have a specific hook
        - Be unique and differentiated
        - Be designed to outperform competitor content
        
        Include the HOOK for each idea.""",
        agent=content_creator,
        expected_output='25-30 unique, categorized content ideas with specific hooks'
    )
    
    # Task 5: Write Ready-to-Publish Posts
    writing_task = Task(
        description=f"""Write 5 complete, ready-to-publish posts for {brand_name} about {topic}.
        
        Create one post optimized for EACH platform:
        
        1. LINKEDIN POST:
           - Professional but engaging tone
           - 150-200 words
           - Industry insights focus
           - Strong hook + value + CTA
           - 3-5 relevant hashtags
        
        2. INSTAGRAM CAPTION:
           - Conversational, authentic tone
           - 100-150 words
           - Storytelling approach
           - Emojis for visual appeal
           - 10-15 hashtags
           - Clear CTA
        
        3. TWITTER/X THREAD (3-5 tweets):
           - Punchy, concise style
           - Hook in first tweet
           - Value-packed thread
           - Controversial angle or insight
           - Relevant hashtags
        
        4. TIKTOK SCRIPT:
           - Hook in first 3 seconds
           - 60-90 second script
           - Casual, energetic tone
           - Visual cues included
           - Trending sound suggestion
        
        5. FACEBOOK POST:
           - Community-focused tone
           - 100-150 words
           - Question or discussion starter
           - Relatable angle
           - 2-3 hashtags
        
        Each post must:
        - Fill a competitor gap
        - Use insights from trend analysis
        - Be completely unique
        - Be ready to copy-paste-publish
        - Outperform typical competitor content
        
        Format clearly with platform labels.""",
        agent=content_writer,
        expected_output='5 complete, platform-optimized posts ready for immediate publishing'
    )
    
    # Create and execute the crew
    crew = Crew(
        agents=[intelligence_agent, trend_analyst, gap_analyst, content_creator, content_writer],
        tasks=[research_task, trend_task, gap_task, content_ideas_task, writing_task],
        verbose=True
    )
    
    result = crew.kickoff(inputs={"topic": topic, "brand_name": brand_name})
    return result
