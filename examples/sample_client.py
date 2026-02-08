"""
Sample client for Multi-Agent Document Intelligence System.
Demonstrates how to use the API programmatically.
"""

import requests
import json
from typing import Dict, Any


class DocumentAnalysisClient:
    """Client for document analysis API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize client.
        
        Args:
            base_url: Base URL of the API
        """
        self.base_url = base_url
    
    def check_health(self) -> Dict[str, Any]:
        """
        Check if API is healthy.
        
        Returns:
            Health status
        """
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def analyze_document(self, document_text: str) -> Dict[str, Any]:
        """
        Analyze a document.
        
        Args:
            document_text: Document text to analyze
            
        Returns:
            Analysis results with summary, action items, and risks
            
        Raises:
            requests.HTTPError: If request fails
        """
        response = requests.post(
            f"{self.base_url}/analyze-document",
            json={"document_text": document_text},
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    
    def print_results(self, results: Dict[str, Any]) -> None:
        """
        Pretty print analysis results.
        
        Args:
            results: Analysis results from API
        """
        print("\n" + "="*80)
        print("DOCUMENT ANALYSIS RESULTS")
        print("="*80)
        
        # Summary
        print("\n📝 SUMMARY")
        print("-"*80)
        print(results["summary"])
        
        # Action Items
        print("\n\n✅ ACTION ITEMS")
        print("-"*80)
        action_items = results["action_items"]
        if action_items:
            for idx, item in enumerate(action_items, 1):
                print(f"\n{idx}. {item['task']}")
                if item.get('owner'):
                    print(f"   👤 Owner: {item['owner']}")
                if item.get('deadline'):
                    print(f"   📅 Deadline: {item['deadline']}")
                if item.get('dependencies'):
                    deps = ", ".join(item['dependencies'])
                    print(f"   🔗 Dependencies: {deps}")
        else:
            print("No action items identified")
        
        # Risks and Issues
        print("\n\n⚠️  RISKS AND OPEN ISSUES")
        print("-"*80)
        risks = results["risks_and_open_issues"]
        if risks:
            for idx, item in enumerate(risks, 1):
                icon = "🔴" if item['impact'] == "high" else "🟡" if item['impact'] == "medium" else "🟢"
                print(f"\n{idx}. [{item['type'].upper()}] {icon} {item['issue']}")
                print(f"   Impact: {item['impact'].upper()}")
        else:
            print("No risks or open issues identified")
        
        print("\n" + "="*80 + "\n")


# Example usage
def main():
    """Example usage of the client."""
    
    # Sample document (meeting notes)
    sample_document = """
    Product Strategy Meeting - January 2024
    
    The team met to discuss our Q1 product roadmap. Key decisions were made:
    
    Sarah will lead the redesign of the user dashboard. This needs to be completed 
    by February 15th to align with the marketing campaign launch. The new design 
    should improve user engagement metrics by at least 20%.
    
    Mike raised concerns about our current infrastructure capacity. We're approaching 
    80% server utilization and need to upgrade before we launch the new features. 
    This is a critical blocker that must be resolved.
    
    The team agreed to implement a new payment gateway integration. Lisa will 
    coordinate with the vendor and the work depends on completing the security 
    audit first. Target completion date is March 1st.
    
    Budget allocation for Q1 is still pending approval from finance. This creates 
    uncertainty around hiring plans and may delay some initiatives.
    
    Open questions:
    - What's our backup plan if the vendor integration is delayed?
    - How will we handle the increased support load after launch?
    - Can we defer any features to Q2 if needed?
    
    Next meeting scheduled for February 5th to review progress.
    """
    
    # Create client
    client = DocumentAnalysisClient()
    
    try:
        # Check API health
        print("Checking API health...")
        health = client.check_health()
        print(f"✓ API Status: {health['status']}")
        
        # Analyze document
        print("\nAnalyzing document...")
        results = client.analyze_document(sample_document)
        
        # Print results
        client.print_results(results)
        
        # Save to file (optional)
        with open("analysis_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print("Results saved to: analysis_results.json")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API")
        print("Make sure the server is running:")
        print("  cd backend && uvicorn app.main:app --reload")
    
    except requests.exceptions.HTTPError as e:
        print(f"❌ API Error: {e}")
        if e.response.status_code == 400:
            print("Check that your document text is valid")
        elif e.response.status_code == 500:
            print("Server error - check server logs")
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
