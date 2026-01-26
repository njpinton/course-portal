# CMSC 178IP Finals Exam - Student Instructions

## Exam Overview

- **Type:** Take-Home, Practical (Jupyter Notebook)
- **Total Points:** 80 (70 base + 10 bonus)
- **Recommended Time:** 3-4 hours
- **Deadline:** 1 week from release

## Format

This is a **practical examination** in Jupyter Notebook format consisting of:
- Code implementation tasks
- Image processing exercises
- Analysis and reasoning questions

| Part | Topic | Points | Time |
|------|-------|--------|------|
| **Part 0** | Image Fundamentals Review | 10 | 20-30 min |
| **Part 1** | CNN Architecture Analysis | 20 | 45-60 min |
| **Part 2** | Image Segmentation | 20 | 45-60 min |
| **Part 3** | Generative Models | 20 | 45-60 min |
| **Bonus** | End-to-End Application | 10 | 30-45 min |

## Getting Started

### 1. Setup Environment

```bash
# Create virtual environment (recommended)
python -m venv exam_env
source exam_env/bin/activate  # On Windows: exam_env\Scripts\activate

# Install required packages
pip install numpy matplotlib scikit-image scipy scikit-learn jupyter

# Optional (for deep learning sections)
pip install torch torchvision
```

### 2. Generate Exam Materials

```bash
cd finals_exam
python scripts/generate_all_exam_materials.py
```

This creates all images and datasets needed for the exam.

### 3. Open the Notebook

```bash
cd student_template
jupyter notebook finals_exam_template.ipynb
```

Or use **Google Colab** by uploading the notebook.

## What You May Use

**Permitted:**
- Course slides and lecture notes
- Textbooks and academic papers
- Online resources (tutorials, documentation)
- LLM tools (ChatGPT, Claude, etc.) for coding help and clarification
- NumPy, SciPy, scikit-image, scikit-learn documentation

**Not Permitted:**
- Copying answers directly from any source without understanding
- Collaboration with other students
- Sharing questions or answers with others
- Using pre-built solutions from previous exams

## LLM Usage Policy

You **MAY** use LLM tools to:
- Clarify concepts you don't understand
- Debug code errors
- Get syntax help for library functions
- Generate visualization code

You **MAY NOT**:
- Copy LLM responses directly as your analysis answers
- Have LLM write your reasoning/justifications
- Use LLM output without understanding it

**Important:** Your reflection answers and comparison work will demonstrate your genuine understanding. The goal is learning, not just correct answers.

## Task Completion Guidelines

### Code Cells
- Complete all cells marked with `# TODO`
- Your code should run without errors
- Include comments explaining your approach
- Display outputs (images, results) where appropriate

### Analysis Questions
- Write in your own words
- Be concise but thorough
- Provide specific examples when relevant
- Show understanding of WHY, not just WHAT

## Grading Breakdown

- **Implementation (40%):** Does your code work correctly?
- **Analysis (60%):** Do you understand WHY it works?

### Rubric

**Excellent (90-100%)**
- Code works correctly with edge cases handled
- Analysis shows deep understanding
- Justifications are evidence-based
- Thoughtful comparison of alternatives

**Good (75-89%)**
- Code works for typical cases
- Analysis demonstrates understanding
- Some justification provided
- Basic comparisons made

**Satisfactory (60-74%)**
- Code has minor issues but general approach correct
- Analysis shows partial understanding
- Limited justification

**Needs Improvement (<60%)**
- Code has major issues or doesn't work
- Analysis missing or incorrect
- No justification provided

## Submission Requirements

### What to Submit

1. **Jupyter Notebook (.ipynb)**
   - All cells executed (output visible)
   - All code commented
   - All analysis questions answered

2. **PDF Export**
   - File → Export Notebook As → PDF
   - Or: File → Print → Save as PDF
   - Ensure all images are visible

3. **Naming Convention**
   ```
   LastName_FirstName_FinalsExam.ipynb
   LastName_FirstName_FinalsExam.pdf
   ```

### Submission Platform
**[Specify your platform: Google Classroom, Canvas, Email, etc.]**

### Deadline
**[Specify deadline with timezone]**

### Late Policy
10% penalty per day late (up to 3 days maximum)

## Tips for Success

### Time Management
- Don't get stuck on one problem too long
- Complete what you can first, then return to difficult parts
- Analysis questions are worth 60% - don't skip them!
- Leave time to review and run all cells

### Coding Tips
- Test your code incrementally
- Use the provided helper functions
- Check dimensions and data types
- Visualize intermediate results

### Common Pitfalls
- Forgetting to normalize images (0-255 vs 0-1)
- Not running cells in order
- Missing LLM usage documentation
- Forgetting to export as PDF

## Technical Issues?

- **Python errors:** Check library versions and imports
- **Memory issues:** Reduce image sizes or restart kernel
- **Colab issues:** Ensure runtime is connected
- **Submission issues:** Contact instructor before deadline

## Questions During Exam

**Clarification questions:** Email [instructor email]
**Technical issues:** [IT support contact]

**Note:** We can clarify instructions but cannot help with problem-solving.

---

## Academic Integrity Statement

By submitting this exam, I certify that:
- This work is my own
- I have not shared questions or answers with others
- My reflection answers represent my genuine learning
- My LLM usage log is complete and accurate

---

**Good luck! Focus on demonstrating your understanding.**
