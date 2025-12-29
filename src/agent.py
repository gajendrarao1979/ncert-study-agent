
"""
Agent Module - Core agentic workflow using LangGraph
"""

from typing import List, Dict, TypedDict
from pathlib import Path
from langgraph.graph import StateGraph, END
import vertexai
from vertexai.generative_models import GenerativeModel
from colorama import Fore, Style

from pdf_processor import PDFProcessor
from notes_generator import NotesGenerator
from utils import log_progress


class AgentState(TypedDict):
    """State for the agent workflow"""
    subjects: List[str]
    chapters: Dict[str, List[str]]
    current_subject: str
    current_chapter: str
    pdf_path: str
    extracted_content: str
    generated_notes: str
    pdf_saved: bool
    error: str
    progress: str


class NCERTNotesAgent:
    """Main Agent class for generating NCERT notes"""
    
    def __init__(self, config: dict):
        self.config = config
        vertexai.init(project=config['google']['project'], location=config['google']['location'])
        self.client = GenerativeModel(model_name=config['google']['model'])
        self.pdf_processor = PDFProcessor(config)
        self.notes_generator = NotesGenerator(self.client, config)
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("download_pdf", self.download_pdf_node)
        workflow.add_node("extract_content", self.extract_content_node)
        workflow.add_node("generate_notes", self.generate_notes_node)
        workflow.add_node("save_notes", self.save_notes_node)
        
        # Define edges
        workflow.set_entry_point("download_pdf")
        workflow.add_edge("download_pdf", "extract_content")
        workflow.add_edge("extract_content", "generate_notes")
        workflow.add_edge("generate_notes", "save_notes")
        workflow.add_edge("save_notes", END)
        
        return workflow.compile()
    
    def download_pdf_node(self, state: AgentState) -> AgentState:
        """Node: Download PDF from NCERT website"""
        subject = state["current_subject"]
        chapter = state["current_chapter"]
        
        log_progress(f"Downloading: {subject} - {chapter}", "download")
        
        try:
            pdf_path = self.pdf_processor.download_chapter(subject, chapter)
            state["pdf_path"] = str(pdf_path)
            log_progress(f"Downloaded: {pdf_path.name}", "success")
        except Exception as e:
            state["error"] = f"Download failed: {str(e)}"
            log_progress(state["error"], "error")
        
        return state
    
    def extract_content_node(self, state: AgentState) -> AgentState:
        """Node: Extract text content from PDF"""
        log_progress("Extracting content from PDF...", "process")
        
        try:
            content = self.pdf_processor.extract_text(state["pdf_path"])
            state["extracted_content"] = content
            log_progress(f"Extracted {len(content)} characters", "success")
        except Exception as e:
            state["error"] = f"Extraction failed: {str(e)}"
            log_progress(state["error"], "error")
        
        return state
    
    def generate_notes_node(self, state: AgentState) -> AgentState:
        """Node: Generate study notes using Gemini AI"""
        log_progress("Generating AI-powered study notes...", "ai")
        
        try:
            notes = self.notes_generator.generate_notes(
                state["extracted_content"],
                state["current_subject"],
                state["current_chapter"]
            )
            state["generated_notes"] = notes
            log_progress("Notes generated successfully", "success")
        except Exception as e:
            state["error"] = f"Note generation failed: {str(e)}"
            log_progress(state["error"], "error")
        
        return state
    
    def save_notes_node(self, state: AgentState) -> AgentState:
        """Node: Save generated notes as PDF"""
        log_progress("Saving notes to PDF...", "save")
        
        try:
            pdf_path = self.notes_generator.save_as_pdf(
                state["generated_notes"],
                state["current_subject"],
                state["current_chapter"]
            )
            state["pdf_saved"] = True
            log_progress(f"Saved: {pdf_path.name}", "success")
        except Exception as e:
            state["error"] = f"Save failed: {str(e)}"
            log_progress(state["error"], "error")
        
        return state
    
    def run(self, subjects: List[str], chapters: Dict[str, List[str]]):
        """Run the agent for specified subjects and chapters"""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}🎓 Starting Notes Generation")
        print(f"{Fore.CYAN}{'='*70}\n")
        
        total_tasks = sum(len(chaps) for chaps in chapters.values())
        completed = 0
        failed = 0
        
        for subject in subjects:
            if subject not in chapters:
                continue
            
            print(f"\n{Fore.YELLOW}📚 Subject: {subject}")
            print(f"{Fore.YELLOW}{'-'*70}")
            
            for chapter in chapters[subject]:
                completed += 1
                print(f"\n{Fore.WHITE}[{completed}/{total_tasks}] {chapter}")
                
                initial_state = AgentState(
                    subjects=subjects,
                    chapters=chapters,
                    current_subject=subject,
                    current_chapter=chapter,
                    pdf_path="",
                    extracted_content="",
                    generated_notes="",
                    pdf_saved=False,
                    error="",
                    progress=""
                )
                
                try:
                    final_state = self.workflow.invoke(initial_state)
                    
                    if final_state.get("error"):
                        failed += 1
                        print(f"{Fore.RED}⚠️  {final_state['error']}")
                    else:
                        print(f"{Fore.GREEN}✅ Completed successfully")
                        
                except Exception as e:
                    failed += 1
                    print(f"{Fore.RED}❌ Failed: {str(e)}")
        
        # Final summary
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.GREEN}✅ Completed: {completed - failed}/{total_tasks}")
        if failed > 0:
            print(f"{Fore.RED}❌ Failed: {failed}/{total_tasks}")
        print(f"{Fore.CYAN}{'='*70}")