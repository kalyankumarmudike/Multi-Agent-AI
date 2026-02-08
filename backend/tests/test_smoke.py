"""
Smoke test for Multi-Agent Document Intelligence System.

Tests the complete workflow with a long sample document.
Verifies:
- Summary exists
- At least 2 action items
- At least 1 risk or open issue
- JSON validation passes
"""

import os
import sys
import pytest
import requests
import time
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Sample 800+ word transcript
SAMPLE_DOCUMENT = """
Project Kickoff Meeting - Q4 Marketing Campaign
Date: January 15, 2024
Attendees: Sarah Chen (Marketing Director), Michael Rodriguez (Product Manager), 
Lisa Wang (Design Lead), David Kim (Engineering Manager), Rachel Johnson (Content Strategist)

Sarah Chen opened the meeting at 9:00 AM by welcoming everyone and outlining the agenda. 
She emphasized that this quarter's marketing campaign is critical for hitting our annual revenue targets. 
The campaign needs to launch by March 1st, which gives us only six weeks to complete all deliverables.

Michael Rodriguez presented the product roadmap. He confirmed that the new features promised in the campaign 
materials will be ready by February 20th. However, he expressed concern about the aggressive timeline, 
noting that his team is still working on bug fixes from the previous release. He suggested that we need 
to prioritize ruthlessly and possibly defer some lower-priority features. Sarah agreed to follow up with 
Michael offline to identify which features are absolutely necessary for the campaign.

Lisa Wang discussed the creative direction. She proposed a modern, minimalist design approach that aligns 
with current market trends. She presented three mockups and the team voted to proceed with option B, 
which features bold typography and vibrant colors. Lisa mentioned that she needs final copy from Rachel 
by January 25th to complete the designs. She also noted that she's still waiting for brand guidelines 
approval from legal, which has been pending for two weeks.

David Kim provided an engineering perspective on the landing page development. He explained that his team 
can build the landing page, but they need the final designs by February 1st at the latest. He raised a 
critical concern about the proposed interactive elements, stating that they may not be feasible within 
the current technical constraints. He suggested scheduling a technical feasibility meeting with Lisa 
to review the designs in detail. David also mentioned that the team is currently short-staffed due to 
two engineers being on vacation, which could impact delivery timelines.

Rachel Johnson outlined the content strategy. She proposed creating a series of blog posts, social media 
content, and email campaigns. She committed to delivering the first draft of all website copy by January 25th. 
Rachel emphasized the need for customer testimonials and case studies but noted that the sales team hasn't 
provided the promised interviews yet. She said she'll need to escalate this to the VP of Sales if the 
materials aren't delivered by January 20th.

Budget discussions revealed some concerns. Sarah mentioned that the initial budget allocation of $150,000 
may not be sufficient if we want to include paid social media advertising across all proposed channels. 
She suggested that we might need to request an additional $30,000 from finance, but she wasn't sure if 
approval could be obtained in time. The team agreed to prepare a detailed budget breakdown by January 22nd 
to present to the CFO.

Michael raised the issue of metrics and success criteria. The team needs to define clear KPIs before 
launching the campaign. Sarah suggested tracking website traffic, conversion rates, lead generation, 
and social media engagement. However, there was debate about what realistic targets should be, given 
that this is a new campaign approach. The team agreed to benchmark against industry standards and our 
historical performance, but Michael noted that we don't have access to competitor data, which would be 
helpful for setting informed goals.

A significant risk was identified regarding compliance and regulatory requirements. Lisa mentioned that 
some of the proposed marketing claims need to be reviewed by legal to ensure they comply with advertising 
regulations. Sarah acknowledged this and said she would schedule a meeting with the legal team, but she's 
concerned about their slow response times in the past. The team agreed that legal approval is mandatory 
before launch and cannot be bypassed.

Technical integration concerns were discussed. David explained that the new landing page needs to integrate 
with our existing CRM system, but the API documentation is incomplete. He's waiting for the vendor to 
provide updated technical specifications. Without this integration, lead capture may not work properly, 
which would undermine the entire campaign. Sarah agreed to escalate this issue to the vendor relationship 
manager immediately.

The meeting concluded with Sarah summarizing the key next steps and dependencies. She stressed the 
importance of meeting all intermediate deadlines because any delay in the chain will jeopardize the 
March 1st launch date. She also acknowledged that the team is taking on significant risk by committing 
to such an aggressive timeline, especially given the external dependencies on legal, finance, and vendors.

Several open questions remained at the end of the meeting: Will the budget increase be approved? Can the 
engineering team deliver with reduced staff? Will legal provide timely review of marketing materials? 
Can we get customer testimonials from sales in time? The team agreed to reconvene in one week to assess 
progress and address any blockers that emerge.

Sarah ended the meeting by thanking everyone for their commitment and emphasizing that this campaign 
represents a major opportunity for the company. She encouraged everyone to communicate proactively if 
they encounter any obstacles that could impact deliverables.
"""


def test_api_health():
    """Test that the API is running and healthy."""
    base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("✓ API health check passed")
    except requests.exceptions.ConnectionError:
        pytest.skip("API server is not running. Start it with: uvicorn app.main:app --reload")


def test_document_analysis_smoke():
    """
    Smoke test for document analysis.
    
    Verifies:
    - Summary exists and is non-empty
    - At least 2 action items are extracted
    - At least 1 risk or open issue is identified
    - Response structure matches schema
    """
    base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    
    try:
        print("\n" + "="*80)
        print("SMOKE TEST: Document Analysis")
        print("="*80)
        print(f"Document length: {len(SAMPLE_DOCUMENT)} characters")
        print(f"Word count: {len(SAMPLE_DOCUMENT.split())} words")
        print("="*80)
        
        # Send analysis request
        start_time = time.time()
        response = requests.post(
            f"{base_url}/analyze-document",
            json={"document_text": SAMPLE_DOCUMENT},
            timeout=60  # Generous timeout for LLM processing
        )
        elapsed_time = time.time() - start_time
        
        print(f"\nProcessing time: {elapsed_time:.2f} seconds")
        
        # Check response status
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print("✓ Response status: 200 OK")
        
        # Parse response
        data = response.json()
        
        # Verify summary exists
        assert "summary" in data, "Missing 'summary' field"
        assert isinstance(data["summary"], str), "Summary should be a string"
        assert len(data["summary"]) > 0, "Summary should not be empty"
        print(f"✓ Summary exists ({len(data['summary'])} characters)")
        print(f"\nSummary preview:\n{data['summary'][:200]}...")
        
        # Verify action items
        assert "action_items" in data, "Missing 'action_items' field"
        assert isinstance(data["action_items"], list), "action_items should be a list"
        assert len(data["action_items"]) >= 2, f"Expected ≥2 action items, got {len(data['action_items'])}"
        print(f"\n✓ Action items: {len(data['action_items'])} found (expected ≥2)")
        
        # Print action items
        print("\nAction Items:")
        for idx, item in enumerate(data["action_items"][:5], 1):  # Show first 5
            print(f"  {idx}. {item['task']}")
            if item.get('owner'):
                print(f"     Owner: {item['owner']}")
            if item.get('deadline'):
                print(f"     Deadline: {item['deadline']}")
            if item.get('dependencies'):
                print(f"     Dependencies: {', '.join(item['dependencies'])}")
        
        # Verify risks and open issues
        assert "risks_and_open_issues" in data, "Missing 'risks_and_open_issues' field"
        assert isinstance(data["risks_and_open_issues"], list), "risks_and_open_issues should be a list"
        assert len(data["risks_and_open_issues"]) >= 1, f"Expected ≥1 risk/issue, got {len(data['risks_and_open_issues'])}"
        print(f"\n✓ Risks and open issues: {len(data['risks_and_open_issues'])} found (expected ≥1)")
        
        # Print risks and issues
        print("\nRisks and Open Issues:")
        for idx, item in enumerate(data["risks_and_open_issues"][:5], 1):  # Show first 5
            print(f"  {idx}. [{item['type'].upper()}] {item['issue']}")
            print(f"     Impact: {item['impact']}")
        
        # Verify action item structure
        for action in data["action_items"]:
            assert "task" in action, "Action item missing 'task' field"
            assert "owner" in action, "Action item missing 'owner' field"
            assert "deadline" in action, "Action item missing 'deadline' field"
            assert "dependencies" in action, "Action item missing 'dependencies' field"
        print("\n✓ All action items have required fields")
        
        # Verify risk/issue structure
        for risk in data["risks_and_open_issues"]:
            assert "issue" in risk, "Risk/issue missing 'issue' field"
            assert "type" in risk, "Risk/issue missing 'type' field"
            assert "impact" in risk, "Risk/issue missing 'impact' field"
            assert risk["type"] in ["risk", "open_question", "assumption"], f"Invalid type: {risk['type']}"
            assert risk["impact"] in ["low", "medium", "high"], f"Invalid impact: {risk['impact']}"
        print("✓ All risks/issues have required fields with valid values")
        
        # Performance check
        if elapsed_time <= 6.0:
            print(f"\n✓ Performance: {elapsed_time:.2f}s (target: ≤6s) - EXCELLENT")
        elif elapsed_time <= 10.0:
            print(f"\n⚠ Performance: {elapsed_time:.2f}s (target: ≤6s) - ACCEPTABLE")
        else:
            print(f"\n✗ Performance: {elapsed_time:.2f}s (target: ≤6s) - NEEDS OPTIMIZATION")
        
        print("\n" + "="*80)
        print("SMOKE TEST PASSED ✓")
        print("="*80)
        
        return data
        
    except requests.exceptions.ConnectionError:
        pytest.skip("API server is not running. Start it with: cd backend && uvicorn app.main:app --reload")
    except requests.exceptions.Timeout:
        pytest.fail("Request timed out. LLM processing took too long.")


def test_short_document_validation():
    """Test that very short documents are handled appropriately."""
    base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    
    try:
        short_doc = "This is a very short document."
        
        response = requests.post(
            f"{base_url}/analyze-document",
            json={"document_text": short_doc},
            timeout=30
        )
        
        # Should either process or return validation error
        # Both are acceptable behaviors
        print(f"Short document response status: {response.status_code}")
        
    except requests.exceptions.ConnectionError:
        pytest.skip("API server is not running")


if __name__ == "__main__":
    """Run smoke test directly."""
    print("\n🚀 Running Smoke Test for Multi-Agent Document Intelligence System\n")
    
    # Check environment
    provider = os.getenv("LLM_PROVIDER", "groq")
    api_key_var = f"{provider.upper()}_API_KEY"
    
    if not os.getenv(api_key_var):
        print(f"❌ ERROR: {api_key_var} not set in environment")
        print(f"Please set it in your .env file")
        sys.exit(1)
    
    print(f"LLM Provider: {provider}")
    print(f"API Key: {'✓ Set' if os.getenv(api_key_var) else '✗ Missing'}")
    
    # Run tests
    try:
        print("\n1. Testing API health...")
        test_api_health()
        
        print("\n2. Testing document analysis...")
        result = test_document_analysis_smoke()
        
        print("\n✅ All smoke tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
