#!/usr/bin/env python3
"""
NCERT Notes Generator - Main Entry Point
A complete agentic system for generating study notes from NCERT textbooks
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agent import NCERTNotesAgent
from utils import display_banner, get_user_input, load_config, setup_directories

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def main():
    """Main entry point for the application"""
    
    # Display banner
    display_banner()
    
    # Load environment variables
    load_dotenv()
    
    # Load configuration
    config = load_config()
    
    # Setup directories
    setup_directories(config)
    
    # Get API key
    # api_key = os.getenv("ANTHROPIC_API_KEY")
    # if not api_key:
    #     print(f"{Fore.RED}⚠️  ANTHROPIC_API_KEY not found in .env file")
    #     api_key = input(f"{Fore.YELLOW}Enter your Anthropic API key: {Style.RESET_ALL}").strip()
    #     if not api_key:
    #         print(f"{Fore.RED}❌ API key required. Exiting.")
    #         sys.exit(1)
    print(f"{Fore.CYAN}INFO: Make sure you have authenticated with Google Cloud CLI.")
    print(f"{Fore.CYAN}Run 'gcloud auth application-default login' in your terminal.")
    
    # Get user input
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}📚 Subject and Chapter Selection")
    print(f"{Fore.CYAN}{'='*70}")
    
    subjects, chapters = get_user_input(config)
    
    if not subjects or not chapters:
        print(f"\n{Fore.RED}❌ No subjects or chapters selected. Exiting.")
        sys.exit(1)
    
    # Display summary
    print(f"\n{Fore.GREEN}{'='*70}")
    print(f"{Fore.GREEN}📋 Generation Summary:")
    total_chapters = 0
    for subject in subjects:
        if subject in chapters:
            count = len(chapters[subject])
            total_chapters += count
            print(f"{Fore.WHITE}   {subject}: {Fore.YELLOW}{count} chapters")
    print(f"{Fore.GREEN}   Total: {Fore.YELLOW}{total_chapters} chapters")
    print(f"{Fore.GREEN}{'='*70}")
    
    # Confirm
    confirm = input(f"\n{Fore.CYAN}➡️  Proceed with note generation? (yes/no): {Style.RESET_ALL}").strip().lower()
    if confirm not in ['yes', 'y']:
        print(f"{Fore.YELLOW}❌ Cancelled.")
        sys.exit(0)
    
    # Initialize and run agent
    print(f"\n{Fore.MAGENTA}🚀 Initializing NCERT Notes Generator Agent...")
    agent = NCERTNotesAgent(config=config)
    
    try:
        agent.run(subjects, chapters)
        
        print(f"\n{Fore.GREEN}{'='*70}")
        print(f"{Fore.GREEN}✨ All Done! Notes generation complete.")
        print(f"{Fore.WHITE}📂 Check the '{config['output']['notes_dir']}' folder for your PDFs.")
        print(f"{Fore.GREEN}{'='*70}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠️  Process interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()