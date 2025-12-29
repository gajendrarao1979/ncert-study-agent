
# 🎓 NCERT Notes Generator

An AI-powered agentic system for generating comprehensive study notes from NCERT textbooks for 10th-grade students.

## ✨ Features

- 🤖 **AI-Powered**: Uses Claude Sonnet 4 for intelligent note generation
- 🔄 **Agentic Workflow**: LangGraph-based multi-step processing
- 📚 **Comprehensive Notes**: Includes mnemonics, exam tips, and practice questions
- 📄 **PDF Output**: Professional formatted study notes
- 🎯 **Exam-Focused**: Designed to help students score high marks
- 🌈 **Interactive CLI**: User-friendly command-line interface

## 📋 Prerequisites

- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## 🚀 Quick Start

### 1. Installation

\`\`\`bash
# Clone or extract the package
cd ncert-notes-generator

# Install dependencies
pip install -r requirements.txt

# Or install as package
pip install -e .
\`\`\`

### 2. Configuration

\`\`\`bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API key
nano .env  # or use your preferred editor
\`\`\`

Add your Anthropic API key:
\`\`\`
ANTHROPIC_API_KEY=your_api_key_here
\`\`\`

### 3. Run

\`\`\`bash
python main.py
\`\`\`

## 📖 Usage

1. **Select Subjects**: Choose from Mathematics, Science, Social Science, English, Hindi
2. **Select Chapters**: Pick specific chapters or select all
3. **Confirm**: Review your selection and proceed
4. **Wait**: The agent will download, process, and generate notes
5. **Access Notes**: Find your PDFs in \`ncert_notes_output/notes/\`

## 🏗️ Project Structure

\`\`\`
ncert-notes-generator/
├── src/
│   ├── agent.py              # Core agentic workflow
│   ├── pdf_processor.py      # PDF handling
│   ├── notes_generator.py    # AI note generation
│   └── utils.py              # Utility functions
├── config/
│   ├── config.yaml           # Configuration settings
│   └── subjects.json         # Subject and chapter data
├── tests/                    # Unit tests
├── main.py                   # Entry point
├── requirements.txt          # Dependencies
└── README.md                 # This file
\`\`\`

## ⚙️ Configuration

Edit \`config/config.yaml\` to customize:

- AI model parameters
- PDF processing settings
- Note generation preferences
- Output formatting
- Student information

## 📝 What the Notes Include

Each generated note contains:

1. **📚 Chapter Overview** - Quick summary
2. **🔑 Key Concepts** - Detailed explanations
3. **💡 Important Points** - Must-remember information
4. **🧠 Memory Tricks** - Mnemonics and associations
5. **⚡ Quick Revision** - One-liners for fast review
6. **⚠️ Common Mistakes** - What to avoid
7. **🎓 Exam Strategy** - Question patterns and tips
8. **📝 Practice Questions** - With hints

## 🔧 Advanced Usage

### Custom Subject Configuration

Edit \`config/subjects.json\` to add custom chapters:

\`\`\`json
{
  "grade_10": {
    "YourSubject": {
      "chapters": [
        "Chapter 1",
        "Chapter 2"
      ]
    }
  }
}
\`\`\`

### Programmatic Usage

\`\`\`python
from src.agent import NCERTNotesAgent

agent = NCERTNotesAgent(api_key="your-key", config=config)
agent.run(["Mathematics"], {"Mathematics": ["Real Numbers"]})
\`\`\`

## 🐛 Troubleshooting

### Common Issues

**API Key Error**
- Ensure \`.env\` file exists with valid \`ANTHROPIC_API_KEY\`

**PDF Extraction Failed**
- Check PDF file exists in downloads directory
- Ensure PDF is not corrupted

**Import Errors**
- Run \`pip install -r requirements.txt\` again
- Check Python version (3.8+)

## 📦 Dependencies

- **anthropic**: Claude AI API
- **langgraph**: Agentic workflow framework
- **PyPDF2**: PDF text extraction
- **reportlab**: PDF generation
- **pdfplumber**: Advanced PDF parsing
- **colorama**: Colored terminal output
- **python-dotenv**: Environment management
- **pyyaml**: Configuration parsing

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- NCERT for educational resources
- Anthropic for Claude AI
- LangChain team for LangGraph

## 📧 Support

For issues or questions:
- Open an issue on GitHub
- Check documentation
- Review troubleshooting guide

## 🎯 Roadmap

- [ ] Automatic NCERT PDF download
- [ ] Image and diagram extraction
- [ ] Interactive quiz generation
- [ ] Flashcard creation
- [ ] Progress tracking
- [ ] Multi-language support

---

**Made with ❤️ for Tanmay's academic success!**