"""Resume section processing utilities."""
from typing import List, Tuple, Dict
import re

# Section patterns for identifying resume sections
SECTION_PATTERNS = {
    "EXPERIENCE": [
        "EXPERIENCE", "WORK EXPERIENCE", "EMPLOYMENT HISTORY", "WORK HISTORY",
        "PROFESSIONAL EXPERIENCE", "EXPÉRIENCE", "EXPERIENCIA", "EXPÉRIENCE PROFESSIONNELLE"
    ],
    "EDUCATION": [
        "EDUCATION", "ACADEMIC BACKGROUND", "EDUCATIONAL BACKGROUND",
        "ÉDUCATION", "EDUCACIÓN", "FORMATION"
    ],
    "SKILLS": [
        "SKILLS", "TECHNICAL SKILLS", "COMPETENCIES", "EXPERTISE",
        "COMPÉTENCES", "HABILIDADES", "COMPETENCIAS"
    ],
    "PROJECTS": [
        "PROJECTS", "PERSONAL PROJECTS", "PROFESSIONAL PROJECTS", "PROJECT EXPERIENCE",
        "SIDE PROJECTS", "KEY PROJECTS", "MAJOR PROJECTS", "FEATURED PROJECTS",
        "PROJETS", "PROYECTOS", "PROJECT PORTFOLIO"
    ],
    "ACHIEVEMENTS": [
        "ACHIEVEMENTS", "AWARDS", "HONORS", "ACCOMPLISHMENTS",
        "RÉALISATIONS", "LOGROS", "RECONOCIMIENTOS"
    ],
    "CERTIFICATIONS": [
        "CERTIFICATIONS", "CERTIFICATES", "LICENSES",
        "CERTIFICATS", "CERTIFICACIONES"
    ],
    "LANGUAGES": [
        "LANGUAGES", "LANGUAGE SKILLS",
        "LANGUES", "IDIOMAS"
    ],
    "SUMMARY": [
        "SUMMARY", "PROFESSIONAL SUMMARY", "PROFILE",
        "RÉSUMÉ", "RESUMEN", "PROFIL"
    ]
}

def estimate_tokens(text: str) -> int:
    """Rough estimation of tokens in text (1 token ≈ 4 characters)."""
    return len(text) // 4

def split_into_sections(text: str) -> List[Tuple[str, str]]:
    """Split resume text into sections while preserving unicode characters."""
    if not text.strip():
        return []
    
    sections = []
    current_section = None
    current_text = []
    
    # Split text into lines while preserving unicode
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if line is a section header
        is_header = False
        header_name = None
        
        # First check for colon-separated headers
        if ':' in line:
            potential_header = line.split(':', 1)[0].strip()
            for section_type, patterns in SECTION_PATTERNS.items():
                if any(p.upper() in potential_header.upper() for p in patterns):
                    is_header = True
                    header_name = potential_header
                    line = line.split(':', 1)[1].strip()
                    break
        
        # Then check for standalone headers and malformed headers
        if not is_header:
            # Check for exact matches first
            for section_type, patterns in SECTION_PATTERNS.items():
                if any(p.upper() == line.upper() for p in patterns):
                    is_header = True
                    header_name = line
                    line = ""
                    break
                # Then check for malformed headers (no space after section name)
                if not is_header:
                    for pattern in patterns:
                        if line.upper().startswith(pattern.upper()):
                            is_header = True
                            header_name = pattern
                            line = line[len(pattern):].strip()
                            break
                if is_header:
                    break
        
        if is_header:
            # Save previous section if exists
            if current_section and current_text:
                sections.append((current_section, '\n'.join(current_text).strip()))
            current_section = header_name
            current_text = []
            if line:
                current_text.append(line)
        else:
            if current_section is None:
                # If no section has been identified yet, create a default section
                current_section = "GENERAL"
            current_text.append(line)
    
    # Add the last section
    if current_section and current_text:
        sections.append((current_section, '\n'.join(current_text).strip()))
    
    return sections

def optimize_sections(sections: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """
    Optimize sections by intelligently combining small sections and splitting large ones.
    
    The optimization process:
    1. Splits large sections into smaller, manageable chunks
    2. Groups related small sections together while maintaining context
    3. Ensures optimal token usage for API calls
    """
    MIN_TOKENS = 100  # Minimum tokens for efficient API usage
    MAX_TOKENS = 500  # Maximum tokens per section for API limits
    OPTIMAL_TOKENS = 300  # Target token count for best analysis results
    
    def should_combine_sections(name1: str, name2: str, tokens1: int, tokens2: int) -> bool:
        """Determine if two sections should be combined based on name and size."""
        # Check if sections are related
        if any(word in name1.upper() for word in ["PART", "CONTINUED"]):
            return False
            
        # Check if sections belong to same category
        for patterns in section_groups.values():
            if any(p.upper() in name1.upper() for p in patterns) and any(p.upper() in name2.upper() for p in patterns):
                # Only combine if resulting size is optimal
                combined_tokens = tokens1 + tokens2
                return combined_tokens <= OPTIMAL_TOKENS
        return False
    
    # Section grouping patterns
    section_groups = {
        "PROFESSIONAL": ["EXPERIENCE", "WORK EXPERIENCE", "EMPLOYMENT", "WORK HISTORY", "PROFESSIONAL BACKGROUND"],
        "TECHNICAL": ["SKILLS", "TECHNICAL SKILLS", "COMPETENCIES", "TECHNOLOGIES", "TOOLS"],
        "PROJECTS": ["PROJECTS", "PROJECT EXPERIENCE", "SIDE PROJECTS", "KEY PROJECTS", "PORTFOLIO"],
        "ACADEMIC": ["EDUCATION", "CERTIFICATIONS", "PUBLICATIONS", "ACADEMIC", "TRAINING"],
        "ACHIEVEMENTS": ["ACHIEVEMENTS", "AWARDS", "ACCOMPLISHMENTS", "HONORS", "RECOGNITION"],
        "SUMMARY": ["SUMMARY", "PROFILE", "OBJECTIVE", "ABOUT", "INTRODUCTION"]
    }
    
    # First pass: Split large sections
    split_sections = []
    for section_name, content in sections:
        tokens = estimate_tokens(content)
        
        if tokens > MAX_TOKENS:
            # Split into chunks while preserving logical breaks (bullet points, paragraphs)
            chunks = []
            current_chunk = []
            current_tokens = 0
            
            # Split by natural breaks (bullet points, paragraphs)
            for paragraph in content.split('\n\n'):
                paragraph_tokens = estimate_tokens(paragraph)
                
                # If paragraph itself is too large, split by lines
                if paragraph_tokens > MAX_TOKENS:
                    for line in paragraph.split('\n'):
                        line_tokens = estimate_tokens(line)
                        if current_tokens + line_tokens > OPTIMAL_TOKENS and current_chunk:
                            chunks.append('\n'.join(current_chunk))
                            current_chunk = [line]
                            current_tokens = line_tokens
                        else:
                            current_chunk.append(line)
                            current_tokens += line_tokens
                else:
                    if current_tokens + paragraph_tokens > OPTIMAL_TOKENS and current_chunk:
                        chunks.append('\n'.join(current_chunk))
                        current_chunk = [paragraph]
                        current_tokens = paragraph_tokens
                    else:
                        current_chunk.append(paragraph)
                        current_tokens += paragraph_tokens
            
            # Add remaining content
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
            
            # Create sections from chunks
            for i, chunk in enumerate(chunks, 1):
                suffix = f" (Part {i})" if len(chunks) > 1 else ""
                split_sections.append((f"{section_name}{suffix}", chunk.strip()))
        else:
            split_sections.append((section_name, content))
    
    # Second pass: Group related small sections
    grouped_sections = []
    i = 0
    while i < len(split_sections):
        current_name, current_content = split_sections[i]
        current_tokens = estimate_tokens(current_content)
        combined_content = [current_content]
        
        # Look ahead for sections to combine
        j = i + 1
        while j < len(split_sections):
            next_name, next_content = split_sections[j]
            next_tokens = estimate_tokens(next_content)
            
            if should_combine_sections(current_name, next_name, current_tokens, next_tokens):
                combined_content.append(next_content)
                current_tokens += next_tokens
                j += 1
            else:
                break
        
        # Add combined or single section
        if len(combined_content) > 1:
            grouped_sections.append((current_name, '\n\n'.join(combined_content)))
            i = j
        else:
            grouped_sections.append((current_name, current_content))
            i += 1
    
    return grouped_sections
