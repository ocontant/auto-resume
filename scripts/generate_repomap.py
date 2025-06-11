#!/usr/bin/env python3
"""Generate an AST-based repomap using tree-sitter."""

import os
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser
import json

# Initialize parser with Python language
PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

def extract_python_structure(file_path):
    """Extract structural information from a Python file."""
    with open(file_path, 'rb') as f:
        content = f.read()
    
    tree = parser.parse(content)
    
    structure = {
        'path': str(file_path),
        'classes': [],
        'functions': [],
        'imports': []
    }
    
    def traverse(node, parent_class=None):
        if node.type == 'class_definition':
            class_name = None
            for child in node.children:
                if child.type == 'identifier':
                    class_name = content[child.start_byte:child.end_byte].decode('utf-8')
                    break
            
            if class_name:
                class_info = {
                    'name': class_name,
                    'methods': [],
                    'line': node.start_point[0] + 1
                }
                structure['classes'].append(class_info)
                
                # Traverse children to find methods
                for child in node.children:
                    traverse(child, class_info)
        
        elif node.type == 'function_definition':
            func_name = None
            for child in node.children:
                if child.type == 'identifier':
                    func_name = content[child.start_byte:child.end_byte].decode('utf-8')
                    break
            
            if func_name:
                func_info = {
                    'name': func_name,
                    'line': node.start_point[0] + 1
                }
                
                if parent_class:
                    parent_class['methods'].append(func_info)
                else:
                    structure['functions'].append(func_info)
        
        elif node.type in ['import_statement', 'import_from_statement']:
            import_text = content[node.start_byte:node.end_byte].decode('utf-8')
            structure['imports'].append({
                'statement': import_text,
                'line': node.start_point[0] + 1
            })
        
        for child in node.children:
            traverse(child, parent_class)
    
    traverse(tree.root_node)
    return structure

def generate_repomap(root_dir):
    """Generate a comprehensive repomap of the Python project."""
    root_path = Path(root_dir)
    repomap = {
        'project': root_path.name,
        'structure': {},
        'summary': {
            'total_files': 0,
            'total_classes': 0,
            'total_functions': 0,
            'total_methods': 0
        }
    }
    
    # Walk through all Python files
    for py_file in root_path.rglob('*.py'):
        # Skip test files and __pycache__
        if '__pycache__' in str(py_file) or 'vendor' in str(py_file) or 'build' in str(py_file):
            continue
        
        rel_path = py_file.relative_to(root_path)
        module_path = str(rel_path).replace('/', '.').replace('.py', '')
        
        try:
            structure = extract_python_structure(py_file)
            repomap['structure'][module_path] = structure
            
            # Update summary
            repomap['summary']['total_files'] += 1
            repomap['summary']['total_classes'] += len(structure['classes'])
            repomap['summary']['total_functions'] += len(structure['functions'])
            
            for cls in structure['classes']:
                repomap['summary']['total_methods'] += len(cls['methods'])
        
        except Exception as e:
            print(f"Error processing {py_file}: {e}")
    
    return repomap

def format_markdown_report(repomap):
    """Format the repomap as a markdown report."""
    lines = []
    lines.append("# AutoResume AI - AST Repository Map\n")
    lines.append("Generated using tree-sitter AST analysis\n")
    
    # Summary
    lines.append("## Summary\n")
    summary = repomap['summary']
    lines.append(f"- **Total Python Files**: {summary['total_files']}")
    lines.append(f"- **Total Classes**: {summary['total_classes']}")
    lines.append(f"- **Total Functions**: {summary['total_functions']}")
    lines.append(f"- **Total Methods**: {summary['total_methods']}")
    lines.append("")
    
    # Detailed structure
    lines.append("## Module Structure\n")
    
    # Group by package
    packages = {}
    for module_path, structure in repomap['structure'].items():
        parts = module_path.split('.')
        if len(parts) > 1:
            package = parts[0]
            if package not in packages:
                packages[package] = {}
            packages[package][module_path] = structure
        else:
            if 'root' not in packages:
                packages['root'] = {}
            packages['root'][module_path] = structure
    
    # Format each package
    for package, modules in sorted(packages.items()):
        if package == 'root':
            lines.append("### Root Level Files\n")
        else:
            lines.append(f"### Package: `{package}`\n")
        
        for module_path, structure in sorted(modules.items()):
            lines.append(f"#### `{module_path}`")
            lines.append(f"*{structure['path']}*\n")
            
            # Imports
            if structure['imports']:
                lines.append("**Imports:**")
                for imp in structure['imports'][:5]:  # Show first 5 imports
                    lines.append(f"- Line {imp['line']}: `{imp['statement']}`")
                if len(structure['imports']) > 5:
                    lines.append(f"- ... and {len(structure['imports']) - 5} more")
                lines.append("")
            
            # Classes
            if structure['classes']:
                lines.append("**Classes:**")
                for cls in structure['classes']:
                    lines.append(f"- `{cls['name']}` (line {cls['line']})")
                    if cls['methods']:
                        for method in cls['methods'][:5]:  # Show first 5 methods
                            lines.append(f"  - `{method['name']}()` (line {method['line']})")
                        if len(cls['methods']) > 5:
                            lines.append(f"  - ... and {len(cls['methods']) - 5} more methods")
                lines.append("")
            
            # Functions
            if structure['functions']:
                lines.append("**Functions:**")
                for func in structure['functions'][:10]:  # Show first 10 functions
                    lines.append(f"- `{func['name']}()` (line {func['line']})")
                if len(structure['functions']) > 10:
                    lines.append(f"- ... and {len(structure['functions']) - 10} more functions")
                lines.append("")
            
            lines.append("---\n")
    
    return '\n'.join(lines)

if __name__ == "__main__":
    # Change to parent directory to run from project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    # Generate repomap
    repomap = generate_repomap('.')
    
    # Ensure docs directory exists
    os.makedirs('docs', exist_ok=True)
    
    # Save as JSON
    with open('docs/repomap.json', 'w') as f:
        json.dump(repomap, f, indent=2)
    
    # Save as Markdown
    markdown_report = format_markdown_report(repomap)
    with open('docs/repomap.md', 'w') as f:
        f.write(markdown_report)
    
    print("Repomap generated successfully!")
    print(f"- JSON: docs/repomap.json")
    print(f"- Markdown: docs/repomap.md")