#!/usr/bin/env python3
"""
🚀 ULTIMATE AI RECRUITER PIPELINE 🚀
Complete end-to-end recruitment automation system with modular architecture

MODULAR COMPONENTS:
- 📄 pdf_extractor.py - PDF/TXT resume processing
- 🔗 linkedin_enricher.py - LinkedIn profile enrichment  
- 📊 google_sheets_manager.py - Google Sheets creation
- 📋 CSV export and data management (built-in)

Features:
- ✅ Modular Architecture - Each component is independent
- ✅ PDF Resume Processing (PyMuPDF)
- ✅ Real LinkedIn Data Integration
- ✅ AI-Powered Candidate Enrichment (Groq)
- ✅ Recruiter-Friendly CSV Export
- ✅ Working Google Sheets Creation
- ✅ Multi-source candidate processing
- ✅ Error handling and validation
- ✅ Professional logging and progress tracking

Created: October 19, 2025
"""

import os
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import traceback

# Import our modular components
from pdf_extractor import PDFExtractor
from linkedin_enricher import LinkedInEnricher
from google_sheets_manager import GoogleSheetsManager
from minimal_config import COMPOSIO_API_KEY, GROQ_API_KEY, GROQ_MODEL

@dataclass
class PipelineResults:
    """Track pipeline execution results"""
    total_candidates: int = 0
    pdf_processed: int = 0
    existing_loaded: int = 0
    enriched: int = 0
    csv_created: bool = False
    sheets_created: bool = False
    sheets_url: str = ""
    csv_file: str = ""
    json_file: str = ""
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []

class UltimateRecruiterPipeline:
    """
    🚀 ULTIMATE AI RECRUITER PIPELINE 🚀
    
    Modular AI-Powered Recruitment Automation System
    
    MODULAR COMPONENTS:
    - PDFExtractor: Process PDF/TXT resumes 
    - LinkedInEnricher: Enhance profiles with LinkedIn + AI
    - GoogleSheetsManager: Create Google Sheets
    - Built-in CSV export and data management
    """
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = PipelineResults()
        self.candidates = []
        
        # Initialize modular components
        self.pdf_extractor = None
        self.linkedin_enricher = None
        self.sheets_manager = None
        
        print("🚀 ULTIMATE AI RECRUITER PIPELINE INITIALIZED")
        print("🎯 Modular Architecture for Better Understanding")
        print("=" * 60)
        self.display_module_overview()
    
    def display_module_overview(self):
        """Display the modular architecture overview"""
        print("📋 MODULAR PIPELINE OVERVIEW:")
        print("   📄 PDFExtractor: pdf_extractor.py - Extract data from PDFs/TXT")  
        print("   � LinkedInEnricher: linkedin_enricher.py - LinkedIn + AI enhancement")
        print("   � GoogleSheetsManager: google_sheets_manager.py - Create Google Sheets")
        print("   � Built-in CSV export and candidate management")
        print("   🎯 Main orchestrator: Coordinates all modules")
        print("=" * 60)
        
    def initialize_services(self):
        """Initialize all modular services"""
        try:
            print("🔧 Initializing Modular Services...")
            
            # Initialize PDF Extractor
            self.pdf_extractor = PDFExtractor()
            print("✅ PDF Extractor module loaded")
            
            # Initialize LinkedIn Enricher
            self.linkedin_enricher = LinkedInEnricher()
            print("✅ LinkedIn Enricher module loaded")
            
            # Initialize Google Sheets Manager
            self.sheets_manager = GoogleSheetsManager()
            print("✅ Google Sheets Manager module loaded")
            
            return True
            
        except Exception as e:
            error_msg = f"Service initialization failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results.errors.append(error_msg)
            return False
    
    # PDF processing and AI parsing are now handled by PDFExtractor module
    
    def resume_processor(self):
        """📄 RESUME PROCESSOR MODULE - Process all PDF and text resumes using PDFExtractor"""
        print(f"\n📄 STEP 1: Resume Processing")
        print("-" * 50)
        
        try:
            # Use PDFExtractor module to process all resumes
            processed_candidates = self.pdf_extractor.extract_from_directory()
            
            if processed_candidates:
                # Add processed candidates to our main list
                self.candidates.extend(processed_candidates)
                self.results.pdf_processed = len(processed_candidates)
                
                print(f"\n✅ Resume processing complete via PDFExtractor module")
                print(f"� Successfully processed: {len(processed_candidates)} resumes")
                
                # Show sample of processed data
                if processed_candidates:
                    sample = processed_candidates[0]
                    name = sample.get('full_name', 'Unknown')
                    email = sample.get('email', 'No email')
                    skills_count = len(sample.get('skills', []))
                    print(f"📋 Sample: {name} ({email}) - {skills_count} skills extracted")
            else:
                print("❌ No resumes were successfully processed")
                
        except Exception as e:
            error_msg = f"Resume processing error: {str(e)}"
            print(f"❌ {error_msg}")
            self.results.errors.append(error_msg)
    
    def candidate_loader(self):
        """📋 CANDIDATE LOADER MODULE - Load existing candidates from test_candidates.json"""
        print(f"\n📋 STEP 2: Loading Existing Candidates")
        print("-" * 50)
        
        existing_file = Path("test_candidates.json")
        if not existing_file.exists():
            print(f"❌ {existing_file} not found")
            return
        
        try:
            with open(existing_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            candidates_list = []
            
            if isinstance(data, dict) and 'test_cases' in data:
                # Handle nested test_cases structure
                for test_case in data['test_cases']:
                    if 'candidate' in test_case:
                        candidate = test_case['candidate'].copy()  # Make a copy to avoid reference issues
                        candidate['source'] = 'existing_data'
                        candidate['test_method'] = test_case.get('enrichment_method', 'unknown')
                        candidates_list.append(candidate)
            elif isinstance(data, list):
                # Handle simple array structure
                for candidate in data:
                    candidate_copy = candidate.copy()
                    candidate_copy['source'] = 'existing_data'
                    candidates_list.append(candidate_copy)
            elif isinstance(data, dict) and 'candidates' in data:
                # Handle candidates wrapper
                for candidate in data['candidates']:
                    candidate_copy = candidate.copy()
                    candidate_copy['source'] = 'existing_data'
                    candidates_list.append(candidate_copy)
            else:
                print(f"❌ Unsupported JSON structure in {existing_file}")
                return
            
            self.candidates.extend(candidates_list)
            self.results.existing_loaded = len(candidates_list)
            print(f"✅ Loaded {len(candidates_list)} existing candidates")
            
        except Exception as e:
            error_msg = f"Error loading existing candidates: {str(e)}"
            print(f"❌ {error_msg}")
            self.results.errors.append(error_msg)
    
    # LinkedIn data fetching and AI field generation are now handled by LinkedInEnricher module
    
    def ai_enricher(self):
        """🔮 AI ENRICHER MODULE - Enrich all candidates with LinkedIn and AI data"""
        print(f"\n🔮 STEP 3: AI Enrichment of {len(self.candidates)} Candidates")
        print("-" * 50)
        
        # Use LinkedIn Enricher module
        linkedin_enricher = LinkedInEnricher()
        self.candidates = linkedin_enricher.enrich_multiple_candidates(self.candidates)
        
        # Update results
        self.results.enriched = len(self.candidates)
        print(f"\n✅ Enrichment Complete: {self.results.enriched}/{len(self.candidates)} candidates enriched")
    
    def save_enriched_data(self):
        """Save enriched candidate data to JSON"""
        print(f"\n💾 STEP 4: Saving Enriched Data")
        print("-" * 50)
        
        try:
            self.results.json_file = f"enhanced_candidates_{self.timestamp}.json"
            
            with open(self.results.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.candidates, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved enriched data: {self.results.json_file}")
            
        except Exception as e:
            error_msg = f"Error saving enriched data: {str(e)}"
            print(f"❌ {error_msg}")
            self.results.errors.append(error_msg)
    
    def data_exporter(self):
        """📋 DATA EXPORTER MODULE - Create recruiter-friendly CSV export"""
        print(f"\n📋 STEP 5: Creating Recruiter CSV Export")
        print("-" * 50)
        
        try:
            self.results.csv_file = f"Ultimate_Recruiter_Export_{self.timestamp}.csv"
            
            # Define comprehensive CSV headers for recruiters
            headers = [
                "Full Name", "Email", "Phone", "Current Role", "Current Company",
                "Experience Years", "Career Level", "Location", "Top Skills", 
                "Education", "Certifications", "Projects", "Languages",
                "LinkedIn", "LinkedIn Verified", "GitHub", "Portfolio", 
                "Professional Summary", "Key Achievements", "Salary Expectation", 
                "Availability", "Visa Status", "Awards", "Data Source", "Processing Date"
            ]
            
            with open(self.results.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                
                for candidate in self.candidates:
                    # Extract comprehensive data for recruiters
                    name = str(candidate.get('full_name', '')).strip()
                    email = str(candidate.get('email', '')).strip()
                    phone = str(candidate.get('phone', '')).strip()
                    role = str(candidate.get('current_role', '')).strip()
                    company = str(candidate.get('company', '')).strip()
                    
                    # Experience years
                    years = str(candidate.get('years_of_experience', '')).strip()
                    if not years:
                        exp_count = len(candidate.get('experience', []))
                        years = f"{exp_count} roles" if exp_count > 0 else "Not specified"
                    
                    # Career level
                    career_level = candidate.get('career_level', 'Mid-level')
                    
                    # Location
                    location = str(candidate.get('location', '')).strip()
                    
                    # Skills (top 6 most relevant)
                    skills = candidate.get('skills', [])
                    if isinstance(skills, list) and skills:
                        top_skills = ', '.join(str(s) for s in skills[:6])
                        if len(skills) > 6:
                            top_skills += f" (+{len(skills)-6})"
                    else:
                        top_skills = candidate.get('key_competencies', '')[:60]
                    
                    # Education (comprehensive)
                    education = ""
                    edu_list = candidate.get('education', [])
                    if edu_list and isinstance(edu_list, list) and len(edu_list) > 0:
                        first_edu = edu_list[0]
                        if isinstance(first_edu, dict):
                            degree = first_edu.get('degree', '')
                            field = first_edu.get('field', '')
                            school = first_edu.get('institution', '')
                            year = first_edu.get('year', '')
                            gpa = first_edu.get('gpa', '')
                            
                            parts = []
                            if degree: parts.append(degree)
                            if field and field not in degree: parts.append(f"in {field}")
                            if school: parts.append(f"from {school}")
                            if year: parts.append(f"({year})")
                            if gpa: parts.append(f"GPA: {gpa}")
                            education = " ".join(parts)
                        elif isinstance(first_edu, str):
                            education = first_edu[:80]
                    
                    # Certifications
                    certifications = candidate.get('certifications', [])
                    if isinstance(certifications, list):
                        cert_list = [str(cert) for cert in certifications[:3]]
                        cert_text = ', '.join(cert_list)
                        if len(certifications) > 3:
                            cert_text += f" (+{len(certifications)-3})"
                    else:
                        cert_text = str(certifications)[:50] if certifications else ""
                    
                    # Projects
                    projects = candidate.get('projects', [])
                    if isinstance(projects, list) and projects:
                        project_names = []
                        for p in projects[:2]:
                            if isinstance(p, dict):
                                name = p.get('name', '')
                                if name:
                                    project_names.append(str(name))
                            elif p:
                                project_names.append(str(p))
                        project_text = ', '.join(project_names)
                        if len(projects) > 2:
                            project_text += f" (+{len(projects)-2})"
                    else:
                        project_text = str(projects)[:50] if projects else ""
                    
                    # Languages
                    languages = candidate.get('languages', [])
                    if isinstance(languages, list):
                        lang_list = [str(lang) for lang in languages[:3]]
                        lang_text = ', '.join(lang_list)
                    else:
                        lang_text = str(languages)[:40] if languages else ""
                    
                    # URLs and LinkedIn verification
                    linkedin = str(candidate.get('linkedin_url', '')).strip()
                    
                    # Fix LinkedIn verification display
                    if candidate.get('linkedin_verified') and candidate.get('linkedin_email'):
                        linkedin_verified = f"Verified ({candidate.get('linkedin_email', '')})"
                    elif candidate.get('linkedin_has_profile') or linkedin:
                        linkedin_verified = "Profile Found"
                    else:
                        linkedin_verified = "No"
                    
                    github = str(candidate.get('github_url', '')).strip()
                    portfolio = str(candidate.get('portfolio_url', '')).strip()
                    
                    # Detailed Professional Summary (no truncation for recruiters)
                    summary_parts = []
                    
                    # Get all available summaries
                    linkedin_summary = candidate.get('linkedin_summary', '')
                    original_summary = candidate.get('summary', '')
                    professional_value = candidate.get('professional_value', '')
                    
                    # Combine summaries intelligently
                    if linkedin_summary:
                        summary_parts.append(linkedin_summary)
                    if original_summary and original_summary not in linkedin_summary:
                        summary_parts.append(original_summary)
                    if professional_value and professional_value not in ' '.join(summary_parts):
                        summary_parts.append(professional_value)
                    
                    # Create comprehensive summary
                    summary = ' | '.join(filter(None, summary_parts))
                    
                    # If still no summary, generate one from available data
                    if not summary:
                        summary_elements = []
                        if role:
                            summary_elements.append(f"{role}")
                        if company:
                            summary_elements.append(f"at {company}")
                        if years and years != "Not specified":
                            summary_elements.append(f"with {years} experience")
                        if skills and isinstance(skills, list) and len(skills) > 0:
                            top_skill = skills[0] if isinstance(skills[0], str) else str(skills[0])
                            summary_elements.append(f"specializing in {top_skill}")
                        
                        if summary_elements:
                            summary = " ".join(summary_elements) + " professional"
                        else:
                            summary = "Professional seeking new opportunities"
                    
                    # Key achievements from experience
                    achievements = []
                    experience = candidate.get('experience', [])
                    if isinstance(experience, list):
                        for exp in experience[:2]:  # Top 2 roles
                            if isinstance(exp, dict) and exp.get('achievements'):
                                exp_achievements = exp['achievements']
                                if isinstance(exp_achievements, list):
                                    achievements.extend([str(a) for a in exp_achievements[:2]])
                                else:
                                    achievements.append(str(exp_achievements))
                    achievement_text = '; '.join(achievements[:3]) if achievements else ""
                    
                    # Additional recruiter-relevant fields
                    salary = str(candidate.get('salary_expectation', '')).strip()
                    availability = str(candidate.get('availability', '')).strip()
                    visa_status = str(candidate.get('visa_status', '')).strip()
                    
                    awards = candidate.get('awards', [])
                    if isinstance(awards, list):
                        award_list = [str(award) for award in awards[:2]]
                        award_text = ', '.join(award_list)
                    else:
                        award_text = str(awards)[:40] if awards else ""
                    
                    # Meta data
                    source = candidate.get('source', 'Unknown')
                    process_date = datetime.now().strftime('%Y-%m-%d %H:%M')
                    
                    row = [
                        name, email, phone, role, company, years, career_level, location,
                        top_skills, education, cert_text, project_text, lang_text,
                        linkedin, linkedin_verified, github, portfolio, summary, achievement_text,
                        salary, availability, visa_status, award_text, source, process_date
                    ]
                    
                    writer.writerow(row)
            
            self.results.csv_created = True
            print(f"✅ CSV Export Created: {self.results.csv_file}")
            print(f"📊 {len(self.candidates)} candidates exported with {len(headers)} comprehensive recruiter columns")
            print(f"💡 Features: Detailed summaries, LinkedIn verification, comprehensive skills & projects")
            
        except Exception as e:
            error_msg = f"CSV export error: {str(e)}"
            print(f"❌ {error_msg}")
            self.results.errors.append(error_msg)
    
    def sheets_creator(self):
        """📊 SHEETS CREATOR MODULE - Create Google Sheet with candidate data"""
        print(f"\n📊 STEP 6: Creating Google Sheets")
        print("-" * 50)
        
        try:
            # Use Google Sheets Manager module
            sheets_manager = GoogleSheetsManager()
            sheet_url = sheets_manager.create_recruiter_sheet(self.candidates, self.timestamp)
            
            if sheet_url:
                self.results.sheets_url = sheet_url
                self.results.sheets_created = True
                print(f"✅ Google Sheets created successfully!")
                print(f"🔗 {sheet_url}")
            else:
                print(f"❌ Failed to create Google Sheet")
                
        except Exception as e:
            error_msg = f"Google Sheets error: {str(e)}"
            print(f"❌ {error_msg}")
            self.results.errors.append(error_msg)
    
    def generate_final_report(self):
        """Generate final pipeline execution report"""
        print(f"\n🎉 ULTIMATE PIPELINE EXECUTION COMPLETE!")
        print("=" * 60)
        
        self.results.total_candidates = len(self.candidates)
        
        print(f"📊 PIPELINE RESULTS SUMMARY:")
        print(f"   Total Candidates Processed: {self.results.total_candidates}")
        print(f"   From PDF Resumes: {self.results.pdf_processed}")
        print(f"   From Existing Data: {self.results.existing_loaded}")
        print(f"   AI Enriched: {self.results.enriched}")
        
        print(f"\n📁 OUTPUT FILES:")
        if self.results.json_file:
            print(f"   📄 JSON Data: {self.results.json_file}")
        if self.results.csv_file:
            print(f"   📋 CSV Export: {self.results.csv_file}")
        if self.results.sheets_url:
            print(f"   📊 Google Sheets: {self.results.sheets_url}")
        
        print(f"\n✅ SUCCESS METRICS:")
        print(f"   CSV Export: {'✅ Created' if self.results.csv_created else '❌ Failed'}")
        print(f"   Google Sheets: {'✅ Created' if self.results.sheets_created else '❌ Failed'}")
        
        if self.results.errors:
            print(f"\n⚠️ ERRORS ENCOUNTERED ({len(self.results.errors)}):")
            for i, error in enumerate(self.results.errors, 1):
                print(f"   {i}. {error}")
        else:
            print(f"\n🎯 PERFECT EXECUTION - NO ERRORS!")
        
        # Pipeline success determination
        pipeline_success = (
            self.results.total_candidates > 0 and
            (self.results.csv_created or self.results.sheets_created)
        )
        
        print(f"\n🏁 PIPELINE STATUS: {'🎉 SUCCESS' if pipeline_success else '❌ PARTIAL FAILURE'}")
        
        if pipeline_success:
            print("\n🚀 Your Ultimate AI Recruiter Pipeline is ready for production!")
            if self.results.sheets_url:
                print(f"🔗 Share this Google Sheet: {self.results.sheets_url}")
        
        return self.results
    
    def pipeline_orchestrator(self):
        """🎯 PIPELINE ORCHESTRATOR - Execute the complete Ultimate AI Recruiter Pipeline"""
        try:
            # Initialize all services
            if not self.initialize_services():
                print("❌ Pipeline aborted due to initialization failure")
                return self.results
            
            # 📄 MODULE 1: Process PDF resumes
            self.resume_processor()
            
            # 📋 MODULE 2: Load existing candidates  
            self.candidate_loader()
            
            # Check if we have any candidates
            if not self.candidates:
                print("❌ No candidates found to process!")
                return self.results
            
            # 🔮 MODULE 3: AI enrichment
            self.ai_enricher()
            
            # 💾 MODULE 4: Save enriched data
            self.save_enriched_data()
            
            # 📋 MODULE 5: Create CSV export
            self.data_exporter()
            
            # 📊 MODULE 6: Create Google Sheets
            self.sheets_creator()
            
            # Step 7: Generate final report
            return self.generate_final_report()
            
        except Exception as e:
            error_msg = f"Pipeline execution failed: {str(e)}"
            print(f"❌ {error_msg}")
            print(f"🔍 Full traceback:\n{traceback.format_exc()}")
            self.results.errors.append(error_msg)
            return self.results


def main():
    """Main execution function"""
    print("🚀 STARTING ULTIMATE AI RECRUITER PIPELINE")
    print("🎯 Complete End-to-End Recruitment Automation")
    print("=" * 60)
    
    # Create and run modular pipeline
    pipeline = UltimateRecruiterPipeline()
    results = pipeline.pipeline_orchestrator()
    
    print("\n" + "=" * 60)
    print("🏁 ULTIMATE PIPELINE EXECUTION FINISHED")
    
    return results


if __name__ == "__main__":
    main()