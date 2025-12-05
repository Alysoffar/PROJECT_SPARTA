"""Code highlighting and formatting utilities"""
from pygments import highlight
from pygments.lexers import VerilogLexer, PythonLexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter
from typing import Dict, Any


class CodeHighlighter:
    """Syntax highlighting for RTL code"""
    
    def __init__(self):
        self.verilog_lexer = VerilogLexer()
        try:
            self.vhdl_lexer = get_lexer_by_name('vhdl')
        except:
            self.vhdl_lexer = VerilogLexer()  # Fallback
        self.python_lexer = PythonLexer()
        self.formatter = HtmlFormatter(style='monokai', noclasses=True, linenos=True)
    
    def highlight_rtl(self, code: str, language: str = "verilog") -> str:
        """
        Apply syntax highlighting to RTL code
        Returns HTML with highlighted code
        """
        if language.lower() in ["verilog", "systemverilog", "sv"]:
            lexer = self.verilog_lexer
        elif language.lower() == "vhdl":
            lexer = self.vhdl_lexer
        elif language.lower() == "python":
            lexer = self.python_lexer
        else:
            lexer = self.verilog_lexer  # Default
        
        highlighted = highlight(code, lexer, self.formatter)
        
        return f"""
<div style="background-color: #272822; padding: 10px; border-radius: 5px; overflow-x: auto;">
    {highlighted}
</div>
"""
    
    def add_line_numbers(self, code: str) -> str:
        """Add line numbers to code"""
        lines = code.split('\n')
        numbered_lines = [f"{i+1:3d} | {line}" for i, line in enumerate(lines)]
        return '\n'.join(numbered_lines)
    
    def get_complexity_score(self, code: str) -> Dict[str, Any]:
        """Analyze code complexity"""
        lines = code.split('\n')
        total_lines = len(lines)
        code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('//')])
        comment_lines = len([l for l in lines if l.strip().startswith('//')])
        
        # Count modules, always blocks, etc.
        module_count = code.lower().count('module')
        always_blocks = code.lower().count('always')
        assign_statements = code.lower().count('assign')
        
        complexity = "Simple"
        if code_lines > 100 or always_blocks > 5:
            complexity = "Complex"
        elif code_lines > 50 or always_blocks > 2:
            complexity = "Moderate"
        
        return {
            "total_lines": total_lines,
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "modules": module_count,
            "always_blocks": always_blocks,
            "assign_statements": assign_statements,
            "complexity": complexity,
            "comment_ratio": f"{(comment_lines/total_lines*100):.1f}%" if total_lines > 0 else "0%"
        }
