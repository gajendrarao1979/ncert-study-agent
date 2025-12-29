
"""
Notes Generator Module - AI-powered note generation and PDF creation
"""

from pathlib import Path
from datetime import datetime
from typing import Optional
#import google.generativeai as genai
from vertexai.generative_models import GenerativeModel
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY


class NotesGenerator:
    """Generates study notes using AI and creates formatted PDFs"""
    
    def __init__(self, client: GenerativeModel, config: dict):
        self.client = client
        self.config = config
        self.notes_dir = Path(config['output']['notes_dir'])
        self.notes_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_notes(self, content: str, subject: str, chapter: str) -> str:
        """Generate comprehensive study notes using Claude AI"""
        
        student_name = self.config.get('student_name', 'Student')
        grade = self.config.get('grade', 10)
        
        prompt = f"""You are an expert educator creating study notes for a {grade}th-grade student named {student_name}.

Subject: {subject}
Chapter: {chapter}

Original Content:
{content[:35000]}  # Limit content to avoid token limits

Create comprehensive, high-quality study notes that will help {student_name} score excellent marks. Structure your notes as follows:

# 📚 {chapter}

## 🎯 Chapter Overview
(2-3 sentences summarizing what this chapter is about)

## 🔑 Key Concepts

### Concept 1: [Name]
- Clear definition and explanation
- Why it's important
- Real-world applications

### Concept 2: [Name]
(Continue for all major concepts)

## 💡 Important Points to Remember
- Point 1: Detailed explanation
- Point 2: Detailed explanation
(5-8 critical points)

## 🧠 Memory Tricks & Mnemonics

### Trick 1: [Topic]
**Mnemonic**: [Clever acronym or phrase]
**Explanation**: How to use this mnemonic

(Provide 3-5 memory tricks)

## ⚡ Quick Revision Points
• One-liner 1
• One-liner 2
(10-15 quick points for last-minute revision)

## ⚠️ Common Mistakes to Avoid
1. **Mistake**: [What students often get wrong]
   **Why it's wrong**: [Explanation]
   **Correct approach**: [How to do it right]

(3-5 common mistakes)

## 🎓 Exam Strategy & Tips

### Question Patterns
- Pattern 1: [Type of questions asked]
- Pattern 2: [Type of questions asked]

### Answer Writing Tips
- Tip 1: [How to structure answers]
- Tip 2: [Key words to include]

### Time Management
- Suggested time allocation for different question types

## 📝 Practice Questions

### Short Answer Questions (2-3 marks)
1. Question with [Hint: key concept to use]
2. Question with [Hint: key concept to use]

### Long Answer Questions (5 marks)
1. Question with [Hint: approach to take]
2. Question with [Hint: approach to take]

### Numerical/Application Questions (if applicable)
1. Question with [Hint: formula or method]

## 🔗 Topic Connections
- How this chapter connects to other chapters
- Real-world relevance

---

Make the notes engaging, clear, and focused on exam success. Use simple language suitable for a {grade}th grader. Directly start with notes don't add prefix tax"""

        try:
            generation_config = {
                "max_output_tokens":self.config['google']['max_tokens'],
                "temperature":self.config['google']['temperature'],
            }
            response = self.client.generate_content([prompt], generation_config=generation_config)
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Failed to generate notes: {str(e)}")
    
    def save_as_pdf(self, notes: str, subject: str, chapter: str) -> Path:
        """Save generated notes as a formatted PDF"""
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_subject = subject.replace(' ', '_')
        safe_chapter = chapter.replace(' ', '_')
        filename = f"{safe_subject}_{safe_chapter}_Notes_{timestamp}.pdf"
        filepath = self.notes_dir / filename
        
        # Create PDF
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=36
        )
        
        # Define styles
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#2C3E50',
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading1_style = ParagraphStyle(
            'CustomHeading1',
            parent=styles['Heading1'],
            fontSize=18,
            textColor='#34495E',
            spaceAfter=12,
            spaceBefore=16,
            fontName='Helvetica-Bold'
        )
        
        heading2_style = ParagraphStyle(
            'CustomHeading2',
            parent=styles['Heading2'],
            fontSize=14,
            textColor='#7F8C8D',
            spaceAfter=10,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            leading=14
        )
        
        bullet_style = ParagraphStyle(
            'CustomBullet',
            parent=styles['BodyText'],
            fontSize=11,
            leftIndent=20,
            spaceAfter=6,
            leading=14
        )
        
        # Build PDF content
        story = []
        
        # Header
        story.append(Paragraph("NCERT Study Notes", title_style))
        story.append(Paragraph(f"{subject}", heading1_style))
        story.append(Paragraph(f"{chapter}", heading2_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Metadata
        student_name = self.config.get('student_name', 'Student')
        story.append(Paragraph(f"<b>Prepared for:</b> {student_name} (Grade {self.config.get('grade', 10)})", body_style))
        story.append(Paragraph(f"<b>Generated on:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", body_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Process notes content
        lines = notes.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if not line:
                story.append(Spacer(1, 0.1*inch))
                continue
            
            # Headers
            if line.startswith('# '):
                story.append(Spacer(1, 0.2*inch))
                story.append(Paragraph(line[2:], title_style))
            elif line.startswith('## '):
                story.append(Spacer(1, 0.15*inch))
                story.append(Paragraph(line[3:], heading1_style))
            elif line.startswith('### '):
                story.append(Paragraph(line[4:], heading2_style))
            
            # Bullets and lists
            elif line.startswith('- ') or line.startswith('• '):
                story.append(Paragraph(f"• {self.markdown_conversion(line[2:])}", bullet_style))
            elif line.startswith('* '):
                story.append(Paragraph(f"• {self.markdown_conversion(line[2:])}", bullet_style))
            
            # Numbered lists
            elif len(line) > 2 and line[0].isdigit() and line[1] == '.':
                story.append(Paragraph(self.markdown_conversion(line), bullet_style))
            
            # Bold text
            elif line.startswith('**') and line.endswith('**'):
                story.append(Paragraph(f"<b>{line[2:-2]}</b>", body_style))
            
            # Regular paragraphs
            else:
                line = self.markdown_conversion (line)
                # Convert markdown bold
                # line = line.replace('**', '<b>', 1)
                # line = line.replace('**', '</b>', 1)
                story.append(Paragraph(line, body_style))
        
        # Build PDF
        doc.build(story)
        
        return filepath

    def markdown_conversion(self, text: str):
        """Convert Markdown to HTML"""
        start = True
        while "**" in text: 
            if start:
                start = False
                text = text.replace("**", "<b>", 1)
            else:
                start = True
                text = text.replace("**", "</b>", 1)
        return text


