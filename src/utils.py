"""
Utility Functions Module
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Tuple
from colorama import Fore, Style


def display_banner():
    """Display application banner"""
    banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║                    🎓 NCERT NOTES GENERATOR 📚                         ║
║                                                                        ║
║              AI-Powered Study Notes for 10th Grade                    ║
║                    For Tanmay's Success! 🌟                           ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def load_config() -> dict:
    """Load configuration from YAML file"""
    config_path = Path("config/config.yaml")
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        # Default configuration
        config = {
            'anthropic': {
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 4000,
                'temperature': 0.7
            },
            'pdf': {
                'extract_images': False,
                'max_pages_per_chapter': 50
            },
            'notes': {
                'include_mnemonics': True,
                'include_exam_tips': True,
                'include_practice_questions': True,
                'practice_questions_count': 7
            },
            'output': {
                'downloads_dir': 'ncert_notes_output/downloads',
                'notes_dir': 'ncert_notes_output/notes'
            },
            'grade': 10,
            'student_name': 'Tanmay'
        }
    
    return config


def load_subjects_data() -> dict:
    """Load subjects and chapters data from JSON"""
    subjects_path = Path("config/subjects.json")
    config = load_config()
    
    if subjects_path.exists():
        with open(subjects_path, 'r', encoding='utf-8') as f:
            subjects_data = json.load(f)
            return subjects_data.get(f"grade_{config['grade']}", {"subjects": {}})["subjects"]
    
    # Default subjects data
    return {
            "Mathematics": {
                "chapters": ["Real Numbers", "Polynomials", "Quadratic Equations"]
            },
            "Science": {
                "chapters": ["Chemical Reactions", "Acids Bases and Salts", "Metals and Non-metals"]
            }
        }


def setup_directories(config: dict):
    """Create necessary directories"""
    Path(config['output']['downloads_dir']).mkdir(parents=True, exist_ok=True)
    Path(config['output']['notes_dir']).mkdir(parents=True, exist_ok=True)


def get_user_input(config: dict) -> Tuple[List[str], Dict[str, List[str]]]:
    """Get subjects and chapters from user interactively"""
    
    subjects_data = load_subjects_data()
    grade_data = subjects_data
    
    available_subjects = list(grade_data.keys())
    
    print(f"\n{Fore.GREEN}📚 Available Subjects:{Style.RESET_ALL}")
    for i, subject in enumerate(available_subjects, 1):
        #print(f"   {Fore.YELLOW}{i}.{Style.RESET_ALL} My Subject{subject}")
        chapter_count = len(grade_data[subject].get('chapters', {}))
        print(f"   {Fore.YELLOW}{i}.{Style.RESET_ALL} {subject} ({chapter_count} chapters)")
    
    # Get subjects
    print(f"\n{Fore.CYAN}➡️  Enter subject numbers (comma-separated, e.g., 1,2,3):{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}Or press Enter to select all subjects{Style.RESET_ALL}")
    subject_input = input(f"   {Fore.YELLOW}Your choice: {Style.RESET_ALL}").strip()
    
    if not subject_input:
        selected_subjects = available_subjects
    else:
        try:
            indices = [int(x.strip()) - 1 for x in subject_input.split(",")]
            print(f"Indice vlue {indices} and available subjects {available_subjects}")
            selected_subjects = [available_subjects[i] for i in indices if 0 <= i < len(available_subjects)]
        except:
            print(f"{Fore.RED}Invalid input. Using all subjects.{Style.RESET_ALL}")
            selected_subjects = available_subjects
    
    print(f"\n{Fore.GREEN}✅ Selected: {', '.join(selected_subjects)}{Style.RESET_ALL}")
    
    # Get chapters
    chapters_dict = {}
    
    for subject in selected_subjects:
        available_chapters = list(grade_data[subject].get('chapters', {}).keys())
        
        print(f"\n{Fore.CYAN}📖 Chapters for {subject}:{Style.RESET_ALL}")
        for i, chapter in enumerate(available_chapters, 1):
            print(f"   {Fore.YELLOW}{i}.{Style.RESET_ALL} {chapter}")
        
        print(f"\n{Fore.CYAN}➡️  Enter chapter numbers (comma-separated):{Style.RESET_ALL}")
        print(f"   {Fore.WHITE}Or press Enter to select all chapters{Style.RESET_ALL}")
        chapter_input = input(f"   {Fore.YELLOW}Your choice: {Style.RESET_ALL}").strip()
        
        if not chapter_input:
            chapters_dict[subject] = available_chapters
        else:
            try:
                indices = [int(x.strip()) - 1 for x in chapter_input.split(",")]
                print(f"Indice vlue {indices} and available chappters {available_chapters}")
                chapters_dict[subject] = [available_chapters[i] for i in indices if 0 <= i < len(available_chapters)]
            except Exception as e:
                print(f"      choice error {e}")
                print(f"{Fore.RED}Invalid input. Using all chapters.{Style.RESET_ALL}")
                chapters_dict[subject] = available_chapters
        
        print(f"   {Fore.GREEN}✅ Selected {len(chapters_dict[subject])} chapters{Style.RESET_ALL}")
    
    return selected_subjects, chapters_dict


def log_progress(message: str, msg_type: str = "info"):
    """Log progress with colored output"""
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "download": "📥",
        "process": "⚙️",
        "ai": "🤖",
        "save": "💾"
    }
    
    colors = {
        "info": Fore.WHITE,
        "success": Fore.GREEN,
        "error": Fore.RED,
        "warning": Fore.YELLOW,
        "download": Fore.CYAN,
        "process": Fore.BLUE,
        "ai": Fore.MAGENTA,
        "save": Fore.GREEN
    }
    
    icon = icons.get(msg_type, "•")
    color = colors.get(msg_type, Fore.WHITE)
    
    print(f"   {color}{icon} {message}{Style.RESET_ALL}")