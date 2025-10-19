#!/usr/bin/env python3
"""
🔗 LINKEDIN ENRICHER MODULE
Handles LinkedIn profile enrichment via Composio API
"""

import json
from typing import Dict, Optional
from composio import ComposioToolSet, Action
from minimal_config import COMPOSIO_API_KEY
from groq import Groq
from minimal_config import GROQ_API_KEY, GROQ_MODEL


class LinkedInEnricher:
    """LinkedIn Profile Enrichment Service"""
    
    def __init__(self):
        self.composio_toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        print("🔗 LinkedIn Enricher initialized")
    
    def fetch_real_linkedin_data(self, linkedin_url: str) -> Dict:
        """Fetch real LinkedIn data via Composio API"""
        try:
            linkedin_account_id = "ccf2d878-e091-4049-a5fa-57b8a1b3230f"
            entity_id = "pg-test-82fe45fd-72dd-4266-8d24-61c90d1c01be"
            
            print(f"🔍 Fetching LinkedIn data for: {linkedin_url}")
            
            result = self.composio_toolset.execute_action(
                action=Action.LINKEDIN_GET_MY_INFO,
                params={},
                connected_account_id=linkedin_account_id,
                entity_id=entity_id
            )
            
            if result.get('successful'):
                data = result.get('data', {})
                data['is_connected_account'] = True
                return data
            else:
                print(f"❌ LinkedIn API call failed")
                return {}
                
        except Exception as e:
            print(f"❌ LinkedIn fetch error: {str(e)}")
            return {}
    
    def generate_linkedin_fields_with_ai(self, candidate: Dict) -> Dict:
        """Generate LinkedIn-style professional fields using AI"""
        try:
            name = candidate.get('full_name', '')
            role = candidate.get('current_role', '')
            company = candidate.get('company', '')
            skills = candidate.get('skills', [])
            experience = candidate.get('experience', [])
            
            prompt = f"""
            Generate professional LinkedIn profile fields for this candidate. Return ONLY JSON:
            
            {{
                "linkedin_title": "Professional headline with key skills and role",
                "linkedin_industry": "Industry category",
                "linkedin_summary": "Professional summary 2-3 sentences highlighting achievements and value",
                "experience_highlights": "3-4 bullet points of key career achievements",
                "key_competencies": "Top 8-10 skills relevant to role",
                "career_level": "Junior/Mid-level/Senior/Executive based on experience",
                "professional_value": "Value proposition - what they bring to organizations"
            }}
            
            Candidate: {name}
            Current Role: {role}
            Company: {company}
            Skills: {', '.join(skills[:5]) if skills else 'General professional skills'}
            Experience: {len(experience)} roles in background
            """
            
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=GROQ_MODEL,
                temperature=0.3,
                max_tokens=1000
            )
            
            ai_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                return json.loads(ai_text)
            except json.JSONDecodeError:
                # Extract from code block if needed
                if "```json" in ai_text:
                    json_start = ai_text.find("```json") + 7
                    json_end = ai_text.find("```", json_start)
                    return json.loads(ai_text[json_start:json_end].strip())
                else:
                    print("⚠️ AI response parsing failed")
                    return {}
                    
        except Exception as e:
            print(f"❌ AI field generation error: {str(e)}")
            return {}
    
    def enrich_candidate_profile(self, candidate: Dict) -> Dict:
        """Complete LinkedIn enrichment for a single candidate"""
        name = candidate.get('full_name', 'Unknown')
        print(f"\n🔗 Enriching LinkedIn profile for: {name}")
        
        enriched_candidate = candidate.copy()
        
        # Check for LinkedIn URL
        linkedin_url = candidate.get('linkedin_url', '')
        
        if linkedin_url and 'linkedin.com' in linkedin_url:
            print(f"📡 Fetching REAL LinkedIn data...")
            linkedin_data = self.fetch_real_linkedin_data(linkedin_url)
            
            if linkedin_data and linkedin_data.get('response_dict'):
                profile = linkedin_data['response_dict']
                
                # Verify if this matches the candidate's email
                candidate_email = candidate.get('email', '').lower()
                linkedin_email = profile.get('email', '').lower()
                
                if candidate_email and linkedin_email and candidate_email == linkedin_email:
                    enriched_candidate['linkedin_email'] = profile.get('email', '')
                    enriched_candidate['linkedin_verified'] = True
                    enriched_candidate['linkedin_name'] = profile.get('name', '')
                    enriched_candidate['linkedin_picture'] = profile.get('picture', '')
                    print("✅ LinkedIn profile verified (email match)")
                else:
                    enriched_candidate['linkedin_verified'] = False
                    enriched_candidate['linkedin_has_profile'] = True
                    print("✅ LinkedIn profile found (not verified - different account)")
            else:
                print("⚠️ No LinkedIn data returned")
        
        # Generate AI-powered LinkedIn fields
        print("🤖 Generating AI-enhanced LinkedIn fields...")
        ai_fields = self.generate_linkedin_fields_with_ai(enriched_candidate)
        
        if ai_fields:
            enriched_candidate.update(ai_fields)
            print("✅ AI LinkedIn fields generated successfully")
        else:
            print("⚠️ AI field generation failed")
        
        return enriched_candidate
    
    def enrich_multiple_candidates(self, candidates: list) -> list:
        """Enrich multiple candidates with LinkedIn data"""
        print(f"\n🔗 LINKEDIN ENRICHER: Processing {len(candidates)} candidates")
        print("=" * 50)
        
        enriched_candidates = []
        
        for i, candidate in enumerate(candidates, 1):
            print(f"[{i}/{len(candidates)}] Processing candidate...")
            
            try:
                enriched = self.enrich_candidate_profile(candidate)
                enriched_candidates.append(enriched)
                print(f"✅ Successfully enriched")
            except Exception as e:
                print(f"❌ Enrichment failed: {str(e)}")
                enriched_candidates.append(candidate)  # Keep original
        
        print(f"\n✅ LinkedIn enrichment complete: {len(enriched_candidates)} candidates processed")
        return enriched_candidates


def main():
    """Test the LinkedIn Enricher independently"""
    print("🔗 TESTING LINKEDIN ENRICHER MODULE")
    print("=" * 40)
    
    # Test with sample candidate
    test_candidate = {
        "full_name": "Test User",
        "email": "test@example.com",
        "current_role": "Software Engineer",
        "company": "Tech Corp",
        "skills": ["Python", "JavaScript", "React"],
        "linkedin_url": "https://www.linkedin.com/in/test-user"
    }
    
    enricher = LinkedInEnricher()
    result = enricher.enrich_candidate_profile(test_candidate)
    
    print("\n📊 Enrichment Result:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()