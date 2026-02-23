"""
The Academic Integrity & Writing Suite
A comprehensive tool for academic writing, integrity checking, and content refinement.
"""

import streamlit as st
import os
import json
import time
import hashlib
from datetime import datetime

# ─── Page Config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="Academic Integrity & Writing Suite",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
/* ── Updated Light Mode Variables ── */
:root {
    --bg-primary:    #F8FAFC;  /* Light slate background */
    --bg-secondary:  #FFFFFF;  /* Pure white sidebar/panels */
    --bg-card:       #FFFFFF;  /* White cards */
    --bg-elevated:   #F1F5F9;  /* Light gray inputs */
    --accent-gold:   #D97706;  /* Deeper gold for readability on white */
    --accent-teal:   #0D9488;  /* Deeper teal */
    --accent-red:    #DC2626;  /* Deeper red */
    --accent-purple: #7C3AED;  /* Deeper purple */
    --text-primary:  #0F172A;  /* Dark slate text */
    --text-secondary:#475569;  /* Medium slate text */
    --text-muted:    #94A3B8;  /* Light slate text */
    --border:        #E2E8F0;  /* Subtle light border */
    --border-accent: #CBD5E1;  /* More defined border on hover */
}

/* ── Global Reset for Light Mode ── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

.stApp {
    background: radial-gradient(ellipse at 20% 0%, #FFFFFF 0%, var(--bg-primary) 60%);
}

/* Update Sidebar for Light Mode */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}

/* Update Inputs for better contrast */
.stTextArea textarea,
.stTextInput input {
    background: #FFFFFF !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
}

/* Ensure secondary panels (like diff view) are distinguishable */
.diff-panel {
    background: #F8FAFC !important;
    border: 1px solid var(--border) !important;
}

/* ── App Header ── */
.app-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 28px 0 20px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 32px;
}
.app-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    margin: 0;
    line-height: 1.1;
}
.app-title span { color: var(--accent-gold); }
.app-subtitle {
    font-size: 0.85rem;
    color: var(--text-muted);
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Module Cards ── */
.module-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
}
.module-card:hover { border-color: var(--border-accent); }

.module-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
}
.module-icon {
    width: 40px; height: 40px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
}
.icon-gold   { background: rgba(232,184,75,0.15);  }
.icon-teal   { background: rgba(45,212,191,0.15);  }
.icon-red    { background: rgba(248,113,113,0.15); }
.icon-purple { background: rgba(167,139,250,0.15); }
.icon-blue   { background: rgba(96,165,250,0.15);  }

.module-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}
.module-desc {
    font-size: 0.78rem;
    color: var(--text-muted);
    font-family: 'IBM Plex Mono', monospace;
    margin: 0;
}

/* ── Score Badges ── */
.score-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    font-family: 'IBM Plex Mono', monospace;
}
.score-low    { background: rgba(45,212,191,0.15); color: var(--accent-teal);   border: 1px solid rgba(45,212,191,0.3); }
.score-medium { background: rgba(232,184,75,0.15); color: var(--accent-gold);   border: 1px solid rgba(232,184,75,0.3); }
.score-high   { background: rgba(248,113,113,0.15);color: var(--accent-red);    border: 1px solid rgba(248,113,113,0.3);}

/* ── Diff View ── */
.diff-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 16px;
}
.diff-panel {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
}
.diff-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 10px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}
.diff-label.before { color: var(--accent-red); }
.diff-label.after  { color: var(--accent-teal); }
.diff-text {
    font-size: 0.88rem;
    line-height: 1.7;
    color: var(--text-secondary);
    white-space: pre-wrap;
}

/* ── Citation Card ── */
.citation-item {
    background: var(--bg-secondary);
    border-left: 3px solid var(--accent-purple);
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin-bottom: 10px;
    font-size: 0.88rem;
    color: var(--text-secondary);
    line-height: 1.6;
}
.citation-style-tag {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent-purple);
    margin-bottom: 6px;
}

/* ── Tone Meter ── */
.tone-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 4px;
}
.tone-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-muted);
}

/* ── RAG Status ── */
.rag-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(167,139,250,0.12);
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: 20px;
    padding: 4px 12px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: var(--accent-purple);
}
.rag-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent-purple);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── Streamlit Widget Overrides ── */
.stTextArea textarea,
.stTextInput input {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'Outfit', sans-serif !important;
}
.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: var(--accent-gold) !important;
    box-shadow: 0 0 0 2px rgba(232,184,75,0.15) !important;
}

.stButton > button {
    background: var(--accent-gold) !important;
    color: #0A0D14 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Outfit', sans-serif !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #F5C96A !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(232,184,75,0.3) !important;
}

.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

div[data-baseweb="tab-list"] {
    background: var(--bg-secondary) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid var(--border) !important;
}
div[data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
div[aria-selected="true"][data-baseweb="tab"] {
    background: var(--bg-elevated) !important;
    color: var(--accent-gold) !important;
}

div[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

.stSlider > div > div > div { background: var(--accent-gold) !important; }

/* ── Info / Warning Boxes ── */
.info-box {
    background: rgba(45,212,191,0.08);
    border: 1px solid rgba(45,212,191,0.2);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 0.85rem;
    color: var(--accent-teal);
    margin: 12px 0;
}
.warn-box {
    background: rgba(232,184,75,0.08);
    border: 1px solid rgba(232,184,75,0.2);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 0.85rem;
    color: var(--accent-gold);
    margin: 12px 0;
}

/* ── Version History ── */
.version-entry {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
}
.version-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-muted);
    white-space: nowrap;
}
.version-preview {
    font-size: 0.82rem;
    color: var(--text-secondary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex: 1;
}

/* ── Progress bar ── */
.stProgress > div > div > div { background: var(--accent-gold) !important; }

/* ── Metric override ── */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 16px !important;
}
[data-testid="stMetricValue"] { color: var(--accent-gold) !important; }
</style>
""", unsafe_allow_html=True)

# ─── Imports (after page config) ──────────────────────────────────────────────
import re
import io
import random
from typing import Optional

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# ─── Session State Init ────────────────────────────────────────────────────────
def init_session():
    defaults = {
        "api_key": "",
        "rag_chunks": [],
        "rag_filenames": [],
        "version_history": [],
        "current_draft": "",
        "last_check_result": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ══════════════════════════════════════════════════════════════════════════════
# CORE MODULE FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def get_anthropic_client():
    """Return Anthropic client using stored API key."""
    key = st.session_state.api_key or os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        return None
    return anthropic.Anthropic(api_key=key)

def call_llm(system_prompt: str, user_prompt: str, max_tokens: int = 2048) -> str:
    """Unified LLM call with error handling."""
    client = get_anthropic_client()
    if not client:
        return "⚠️ API key not configured. Please add your Anthropic API key in the sidebar."
    try:
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return message.content[0].text
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# ── 1. Document Parsing ────────────────────────────────────────────────────────
def parse_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF using PyPDF2."""
    if not PYPDF2_AVAILABLE:
        return "PyPDF2 not installed. Run: pip install PyPDF2"
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        return f"Error parsing PDF: {e}"

def parse_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX."""
    if not DOCX_AVAILABLE:
        return "python-docx not installed. Run: pip install python-docx"
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        return f"Error parsing DOCX: {e}"

def parse_uploaded_file(uploaded_file) -> str:
    """Dispatch parser based on file type."""
    if uploaded_file is None:
        return ""
    content = uploaded_file.read()
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        return parse_pdf(content)
    elif name.endswith(".docx"):
        return parse_docx(content)
    elif name.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")
    return "Unsupported file type."

# ── 2. RAG Engine ─────────────────────────────────────────────────────────────
def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    """Simple sliding-window chunker."""
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        if chunk.strip():
            chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def add_to_rag_store(text: str, filename: str):
    """Add document chunks to session-level RAG store."""
    chunks = chunk_text(text)
    st.session_state.rag_chunks.extend(chunks)
    st.session_state.rag_filenames.extend([filename] * len(chunks))

def retrieve_rag_context(query: str, top_k: int = 3) -> str:
    """Simple keyword-overlap retrieval (no vector DB dependency)."""
    if not st.session_state.rag_chunks:
        return ""
    query_words = set(query.lower().split())
    scored = []
    for chunk in st.session_state.rag_chunks:
        chunk_words = set(chunk.lower().split())
        score = len(query_words & chunk_words)
        scored.append((score, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    top_chunks = [c for _, c in scored[:top_k] if _ > 0]
    if not top_chunks:
        return ""
    return "\n\n---\n\n".join(top_chunks)

# ── 3. Assignment Architect ────────────────────────────────────────────────────
def generate_content(brief: str, word_count: int = 800, rag_context: str = "") -> str:
    """Generate structured academic draft from assignment brief."""
    rag_section = ""
    if rag_context:
        rag_section = f"\n\nYou have access to the following relevant source material from the student's uploaded textbooks/notes. Weave this knowledge naturally into the response:\n\n{rag_context}\n"

    system = (
        "You are an expert academic writing assistant. Generate well-structured, "
        "scholarly content with proper paragraph flow. Include an introduction, "
        "clearly labeled body sections, and a conclusion. Use formal academic register. "
        "Do NOT include a bibliography — that will be handled separately."
        + rag_section
    )
    user = (
        f"Assignment Brief:\n{brief}\n\n"
        f"Write a structured academic draft of approximately {word_count} words. "
        "Use clear headings (## Heading), strong topic sentences, and evidence-based arguments."
    )
    return call_llm(system, user, max_tokens=3000)

# ── 4. AI Probability Checker ─────────────────────────────────────────────────
def check_integrity(text: str) -> dict:
    """
    Heuristic AI-detection scoring.
    Returns a dict with score (0-100) and diagnostics.
    In production: replace with GPTZero / Sapling API call.
    """
    if len(text.split()) < 50:
        return {"score": 0, "label": "Too short", "details": {}}

    # ── Heuristic signals ──────────────────────────────────────────────────
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    # 1. Burstiness: std deviation of sentence lengths (low = AI-like)
    lengths = [len(s.split()) for s in sentences]
    mean_len = sum(lengths) / len(lengths) if lengths else 0
    variance = sum((l - mean_len)**2 for l in lengths) / len(lengths) if lengths else 0
    burstiness = variance ** 0.5
    burstiness_score = max(0, 100 - int(burstiness * 3))  # higher std = more human

    # 2. Perplexity proxy: repetition of common AI phrases
    ai_phrases = [
        "it is important to note", "it is worth noting", "in conclusion",
        "furthermore", "moreover", "in today's", "plays a crucial role",
        "it can be argued", "as mentioned above", "in this essay",
        "delve into", "let us explore", "shed light on", "navigate",
        "in the realm of", "it is essential", "at its core", "landscape",
        "tapestry", "testament to", "multifaceted",
    ]
    text_lower = text.lower()
    phrase_hits = sum(1 for p in ai_phrases if p in text_lower)
    phrase_score = min(100, phrase_hits * 12)

    # 3. Avg sentence length penalty (AI tends toward 18-25 words avg)
    len_score = 0
    if 18 <= mean_len <= 25:
        len_score = 40
    elif 15 <= mean_len <= 28:
        len_score = 20

    # 4. Structural uniformity: paragraph length variance
    paragraphs = [p for p in text.split("\n\n") if len(p.split()) > 10]
    para_lens = [len(p.split()) for p in paragraphs]
    para_variance = (sum((l - sum(para_lens)/len(para_lens))**2 for l in para_lens) / len(para_lens))**0.5 if para_lens else 0
    uniformity_score = max(0, 50 - int(para_variance))

    # Combine
    final_score = int(
        phrase_score * 0.35 +
        burstiness_score * 0.30 +
        len_score * 0.20 +
        uniformity_score * 0.15
    )
    final_score = min(99, max(1, final_score))

    label = "Low AI Probability" if final_score < 35 else (
        "Moderate AI Probability" if final_score < 65 else "High AI Probability"
    )
    return {
        "score": final_score,
        "label": label,
        "details": {
            "Phrase repetition signal": phrase_score,
            "Low burstiness signal": burstiness_score,
            "Avg sentence length signal": len_score,
            "Structural uniformity signal": uniformity_score,
            "Avg sentence length (words)": round(mean_len, 1),
            "Sentence length std dev": round(burstiness, 1),
            "AI phrase hits": phrase_hits,
        }
    }

# ── 5. Plagiarism Check Placeholder ──────────────────────────────────────────
def check_plagiarism_api(text: str, api_key: str = "") -> dict:
    """
    Placeholder for Copyleaks / Textrazor integration.
    Replace the body with actual API calls in production.
    """
    # Simulate API latency
    time.sleep(0.5)
    # Mock response
    mock_matches = [
        {"source": "Wikipedia – Academic integrity", "similarity": 12, "matched_text": text[:80] + "..."},
        {"source": "Journal of Education (2019)", "similarity": 7, "matched_text": text[100:180] + "..."},
    ]
    return {
        "overall_similarity": 18,
        "matches": mock_matches,
        "status": "mock",
        "note": "⚠️ This is a placeholder. Integrate Copyleaks or Turnitin API for real results.",
    }

# ── 6. Humanizer / Rewriter ───────────────────────────────────────────────────
def rewrite_text(text: str, tone_level: int = 1, preserve_citations: bool = True) -> str:
    """
    Rewrite text to vary perplexity and burstiness.
    tone_level: 0=Academic, 1=Professional, 2=Conversational
    """
    tones = ["strictly formal academic", "professional and polished", "natural and conversational"]
    tone_desc = tones[tone_level]

    citation_note = (
        "IMPORTANT: Preserve all in-text citations exactly as they appear (e.g., (Smith, 2019), [1], etc.)."
        if preserve_citations else ""
    )

    system = (
        "You are an expert academic editor specializing in humanizing AI-generated text. "
        "Your rewrite must:\n"
        "1. VARY sentence lengths dramatically — mix short punchy sentences (5-8 words) "
        "with medium (15-20 words) and longer complex sentences (25-35 words). This increases 'burstiness'.\n"
        "2. Replace predictable AI vocabulary ('furthermore', 'moreover', 'it is important to note', "
        "'plays a crucial role', 'delve into') with fresh, specific alternatives.\n"
        "3. Add occasional first-person analytical observations or rhetorical questions where appropriate.\n"
        "4. Maintain all facts, arguments, and meaning from the original.\n"
        f"5. Write in {tone_desc} tone.\n"
        f"{citation_note}"
    )
    user = f"Rewrite this text to sound more human-authored:\n\n{text}"
    return call_llm(system, user, max_tokens=3000)

# ── 7. Tone Adjuster ─────────────────────────────────────────────────────────
def adjust_tone(text: str, tone_level: int) -> str:
    """Adjust writing tone without changing meaning."""
    tone_instructions = [
        "Transform this into strictly academic register: formal vocabulary, passive voice where appropriate, "
        "hedging language (may, might, suggests), discipline-specific terminology, third-person perspective.",
        "Transform this into professional register: clear, confident, direct language. "
        "Active voice preferred. Polished but not overly formal.",
        "Transform this into natural conversational register: clear everyday language, "
        "contractions welcome, direct address, relatable analogies. Still intelligent but approachable.",
    ]
    system = (
        "You are a professional editor who specializes in register and tone adjustment. "
        "Preserve all meaning, arguments, and citations. Only change the tone and style."
    )
    user = f"{tone_instructions[tone_level]}\n\nText:\n{text}"
    return call_llm(system, user, max_tokens=2500)

# ── 8. Citation Engine ────────────────────────────────────────────────────────
def format_citation(url_or_info: str, style: str) -> str:
    """Format citation from URL or raw reference info."""
    style_guides = {
        "APA": "APA 7th edition format: Author, A. A. (Year). Title. Publisher. DOI/URL",
        "MLA": "MLA 9th edition format: Author. 'Title.' Source, Volume, Issue, Year, Pages.",
        "Harvard": "Harvard format: Author (Year) Title. Publisher.",
        "Chicago": "Chicago 17th format: Author. Title. City: Publisher, Year.",
    }
    system = (
        f"You are a professional librarian and citation specialist. "
        f"Format the given source information in {style} style. "
        f"Guide: {style_guides.get(style, '')}. "
        "If given a URL, infer as much metadata as possible. "
        "Return ONLY the formatted citation, nothing else."
    )
    user = f"Format this as a {style} citation:\n{url_or_info}"
    return call_llm(system, user, max_tokens=400)

# ── 9. Version History ────────────────────────────────────────────────────────
def save_version(text: str, operation: str):
    """Save text version to session history."""
    entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "operation": operation,
        "text": text,
        "hash": hashlib.md5(text.encode()).hexdigest()[:8],
    }
    st.session_state.version_history.insert(0, entry)
    # Keep last 20 versions
    st.session_state.version_history = st.session_state.version_history[:20]


# ══════════════════════════════════════════════════════════════════════════════
# UI COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════

def render_score_badge(score: int, label: str):
    css_class = "score-low" if score < 35 else ("score-medium" if score < 65 else "score-high")
    icon = "✓" if score < 35 else ("⚠" if score < 65 else "✗")
    st.markdown(
        f'<div class="score-badge {css_class}">{icon} {score}% — {label}</div>',
        unsafe_allow_html=True
    )

def render_diff_view(before: str, after: str):
    st.markdown("""
    <div class="diff-container">
        <div class="diff-panel">
            <div class="diff-label before">◀ BEFORE</div>
    """, unsafe_allow_html=True)
    st.text(before[:2000] + ("..." if len(before) > 2000 else ""))
    st.markdown("""
        </div>
        <div class="diff-panel">
            <div class="diff-label after">▶ AFTER</div>
    """, unsafe_allow_html=True)
    st.text(after[:2000] + ("..." if len(after) > 2000 else ""))
    st.markdown("</div></div>", unsafe_allow_html=True)

def module_header(icon: str, icon_class: str, title: str, desc: str):
    st.markdown(f"""
    <div class="module-header">
        <div class="module-icon {icon_class}">{icon}</div>
        <div>
            <div class="module-title">{title}</div>
            <div class="module-desc">{desc}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    api_key_input = st.text_input(
        "Anthropic API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="sk-ant-...",
        help="Your Claude API key from console.anthropic.com"
    )
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input

    key_set = bool(st.session_state.api_key)
    status_color = "#2DD4BF" if key_set else "#F87171"
    status_text = "Connected" if key_set else "Not configured"
    st.markdown(
        f'<div style="font-size:0.78rem;font-family:IBM Plex Mono,monospace;color:{status_color}">● {status_text}</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("### 📚 RAG Knowledge Base")
    st.markdown('<div style="font-size:0.8rem;color:#9AA3B8">Upload textbooks, lecture notes, or papers to ground your writing in specific sources.</div>', unsafe_allow_html=True)
    
    rag_files = st.file_uploader(
        "Upload source documents",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        key="rag_uploader",
        label_visibility="collapsed",
    )
    
    if rag_files:
        for f in rag_files:
            if f.name not in st.session_state.rag_filenames:
                with st.spinner(f"Indexing {f.name}..."):
                    text = parse_uploaded_file(f)
                    add_to_rag_store(text, f.name)
                st.success(f"✓ {f.name} indexed")

    if st.session_state.rag_chunks:
        n_chunks = len(st.session_state.rag_chunks)
        n_files = len(set(st.session_state.rag_filenames))
        st.markdown(
            f'<div class="rag-pill"><div class="rag-dot"></div> RAG Active — {n_files} doc{"s" if n_files!=1 else ""}, {n_chunks} chunks</div>',
            unsafe_allow_html=True
        )
        if st.button("🗑 Clear Knowledge Base"):
            st.session_state.rag_chunks = []
            st.session_state.rag_filenames = []
            st.rerun()

    st.markdown("---")
    st.markdown("### 🔑 API Integrations")
    st.markdown('<div style="font-size:0.78rem;color:#5A6480">Optional third-party services</div>', unsafe_allow_html=True)
    
    with st.expander("GPTZero (AI Detection)"):
        gptzero_key = st.text_input("GPTZero API Key", type="password", placeholder="Optional")
        st.markdown('<div style="font-size:0.72rem;color:#5A6480">Enhances AI probability detection accuracy.</div>', unsafe_allow_html=True)
    
    with st.expander("Copyleaks (Plagiarism)"):
        copyleaks_key = st.text_input("Copyleaks API Key", type="password", placeholder="Optional")
        st.markdown('<div style="font-size:0.72rem;color:#5A6480">Real plagiarism scanning against academic databases.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════

# ── App Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div>
        <h1 class="app-title">Academic <span>Integrity</span> & Writing Suite</h1>
        <div class="app-subtitle">✦ Powered by Claude · RAG-Enhanced · Version Tracked ✦</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🏗️  Assignment Architect",
    "🔍  Integrity Checker",
    "🔄  Humanizer",
    "📖  Citation Engine",
    "🎛️  Tone Adjuster",
    "🕒  Version History",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: ASSIGNMENT ARCHITECT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    module_header("🏗️", "icon-gold", "Assignment Architect",
                  "Parse brief → RAG-augmented draft generation")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("**Upload Assignment Brief**")
        brief_file = st.file_uploader(
            "Upload PDF, DOCX, or TXT",
            type=["pdf", "docx", "txt"],
            key="brief_upload",
            label_visibility="collapsed",
        )
        st.markdown("**or paste brief text**")
        brief_text = st.text_area(
            "Assignment brief",
            height=200,
            placeholder="Paste your assignment instructions here...",
            label_visibility="collapsed",
        )

        if brief_file:
            parsed = parse_uploaded_file(brief_file)
            brief_text = parsed
            st.markdown('<div class="info-box">✓ Brief parsed from uploaded file.</div>', unsafe_allow_html=True)

    with col2:
        word_count = st.slider("Target Word Count", 300, 3000, 800, 100)
        
        use_rag = st.checkbox(
            "🧠 Use Knowledge Base (RAG)",
            value=bool(st.session_state.rag_chunks),
            disabled=not st.session_state.rag_chunks,
            help="Grounds the response in your uploaded textbooks/notes"
        )
        
        if not st.session_state.rag_chunks:
            st.markdown('<div style="font-size:0.78rem;color:#5A6480">Upload documents in the sidebar to enable RAG.</div>', unsafe_allow_html=True)

        st.markdown("&nbsp;")
        generate_btn = st.button("✦ Generate Draft", use_container_width=True)

    if generate_btn and brief_text.strip():
        with st.spinner("Generating structured draft..."):
            rag_ctx = ""
            if use_rag and st.session_state.rag_chunks:
                rag_ctx = retrieve_rag_context(brief_text, top_k=3)
            
            draft = generate_content(brief_text, word_count, rag_ctx)
            st.session_state.current_draft = draft
            save_version(draft, "Generated Draft")

        st.markdown("---")
        st.markdown("**Generated Draft**")
        
        if rag_ctx:
            st.markdown('<div class="info-box">🧠 Draft augmented with knowledge base context.</div>', unsafe_allow_html=True)
        
        edited = st.text_area("Edit your draft below:", value=draft, height=500, label_visibility="collapsed")
        if edited != draft:
            st.session_state.current_draft = edited
        
        col_copy, col_save = st.columns([1, 1])
        with col_save:
            if st.button("💾 Save to Version History"):
                save_version(edited, "Manual Edit")
                st.success("Version saved!")
    
    elif generate_btn:
        st.warning("Please provide an assignment brief first.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: INTEGRITY CHECKER
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    module_header("🔍", "icon-teal", "Integrity Checker",
                  "AI probability + plagiarism detection")

    check_text = st.text_area(
        "Text to analyze",
        value=st.session_state.current_draft,
        height=250,
        placeholder="Paste text to check for AI probability and plagiarism...",
        label_visibility="collapsed",
    )

    col_ai, col_plag = st.columns(2, gap="large")

    with col_ai:
        st.markdown("**🤖 AI Probability Detection**")
        st.markdown('<div style="font-size:0.8rem;color:#9AA3B8;margin-bottom:12px">Heuristic analysis of burstiness, perplexity, and AI phrase patterns.</div>', unsafe_allow_html=True)
        
        if st.button("Run AI Check", use_container_width=True, key="ai_check_btn"):
            if check_text.strip():
                with st.spinner("Analyzing..."):
                    result = check_integrity(check_text)
                    st.session_state.last_check_result = result
                
                render_score_badge(result["score"], result["label"])
                st.progress(result["score"] / 100)
                
                with st.expander("Detailed Signal Breakdown"):
                    for key, val in result["details"].items():
                        st.metric(key, val)
                
                if result["score"] > 50:
                    st.markdown('<div class="warn-box">⚠ High AI probability detected. Consider using the Humanizer tab to rework the text.</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="info-box">✓ Text appears largely human-authored.</div>', unsafe_allow_html=True)
            else:
                st.warning("No text to analyze.")

    with col_plag:
        st.markdown("**📑 Plagiarism Detection**")
        st.markdown('<div style="font-size:0.8rem;color:#9AA3B8;margin-bottom:12px">Check against academic databases. Add your Copyleaks key for real results.</div>', unsafe_allow_html=True)
        
        if st.button("Run Plagiarism Check", use_container_width=True, key="plag_check_btn"):
            if check_text.strip():
                with st.spinner("Scanning for plagiarism..."):
                    plag_result = check_plagiarism_api(check_text)
                
                sim = plag_result["overall_similarity"]
                css_class = "score-low" if sim < 20 else ("score-medium" if sim < 40 else "score-high")
                st.markdown(
                    f'<div class="score-badge {css_class}">📑 {sim}% Overall Similarity</div>',
                    unsafe_allow_html=True
                )
                
                st.markdown(f'<div class="warn-box">{plag_result["note"]}</div>', unsafe_allow_html=True)
                
                if plag_result["matches"]:
                    st.markdown("**Matched Sources:**")
                    for match in plag_result["matches"]:
                        st.markdown(f"""
                        <div class="citation-item">
                            <div class="citation-style-tag">{match['similarity']}% match</div><br>
                            <strong>{match['source']}</strong><br>
                            <em>{match['matched_text']}</em>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No text to check.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: HUMANIZER / PLAGIARISM REMOVER
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    module_header("🔄", "icon-red", "Humanizer & Plagiarism Remover",
                  "Perplexity & burstiness optimization · Side-by-side diff view")

    hum_text = st.text_area(
        "Text to humanize",
        value=st.session_state.current_draft,
        height=250,
        placeholder="Paste text to rewrite...",
        label_visibility="collapsed",
    )

    col_opts, col_run = st.columns([2, 1])
    with col_opts:
        hum_tone = st.select_slider(
            "Output Tone",
            options=["Strictly Academic", "Professional", "Conversational"],
            value="Professional",
        )
        preserve_cites = st.checkbox("Preserve in-text citations", value=True)

    with col_run:
        st.markdown("&nbsp;")
        humanize_btn = st.button("✦ Humanize Text", use_container_width=True, key="humanize_btn")

    tone_map = {"Strictly Academic": 0, "Professional": 1, "Conversational": 2}

    if humanize_btn:
        if hum_text.strip():
            with st.spinner("Rewriting with varied burstiness & perplexity..."):
                rewritten = rewrite_text(hum_text, tone_map[hum_tone], preserve_cites)
                save_version(hum_text, "Before Humanization")
                save_version(rewritten, "After Humanization")

            st.markdown("---")
            st.markdown("**Side-by-Side Comparison**")

            col_b, col_a = st.columns(2, gap="medium")
            with col_b:
                st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.72rem;text-transform:uppercase;color:#F87171;margin-bottom:8px;letter-spacing:0.08em">◀ ORIGINAL</div>', unsafe_allow_html=True)
                st.text_area("before", value=hum_text, height=400, label_visibility="collapsed", key="diff_before", disabled=True)
            with col_a:
                st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.72rem;text-transform:uppercase;color:#2DD4BF;margin-bottom:8px;letter-spacing:0.08em">▶ HUMANIZED</div>', unsafe_allow_html=True)
                final_rewrite = st.text_area("after", value=rewritten, height=400, label_visibility="collapsed", key="diff_after")

            # Run AI check on rewritten
            new_check = check_integrity(rewritten)
            old_check = check_integrity(hum_text)
            
            st.markdown("---")
            c1, c2, c3 = st.columns(3)
            c1.metric("AI Score Before", f"{old_check['score']}%")
            c2.metric("AI Score After", f"{new_check['score']}%", delta=f"{new_check['score'] - old_check['score']}%")
            c3.metric("Sentence Std Dev", f"{new_check['details'].get('Sentence length std dev', 0)} words")

            if st.button("💾 Use This Version"):
                st.session_state.current_draft = final_rewrite
                save_version(final_rewrite, "Accepted Humanized")
                st.success("✓ Draft updated!")
        else:
            st.warning("No text to humanize.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: CITATION ENGINE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    module_header("📖", "icon-purple", "Citation Engine",
                  "APA · MLA · Harvard · Chicago auto-formatting")

    cite_style = st.selectbox(
        "Citation Style",
        ["APA", "MLA", "Harvard", "Chicago"],
        index=0,
        label_visibility="visible",
    )

    st.markdown("**Enter sources (one per line — URL, DOI, or manual info):**")
    sources_input = st.text_area(
        "Sources",
        height=150,
        placeholder="https://example.com/paper\nhttps://doi.org/10.1000/xyz123\nSmith, J. (2020). The Art of Writing. Oxford University Press.",
        label_visibility="collapsed",
    )

    if st.button("✦ Format Bibliography", use_container_width=False):
        sources = [s.strip() for s in sources_input.strip().split("\n") if s.strip()]
        if sources:
            bibliography = []
            progress_bar = st.progress(0)
            for i, source in enumerate(sources):
                with st.spinner(f"Formatting citation {i+1}/{len(sources)}..."):
                    citation = format_citation(source, cite_style)
                    bibliography.append(citation)
                progress_bar.progress((i + 1) / len(sources))

            st.markdown("---")
            st.markdown(f"**Bibliography — {cite_style} Style**")
            
            for idx, cite in enumerate(bibliography, 1):
                st.markdown(f"""
                <div class="citation-item">
                    <div class="citation-style-tag">{cite_style} · ref {idx}</div><br>
                    {cite}
                </div>
                """, unsafe_allow_html=True)

            full_bib = "\n\n".join(f"[{i}] {c}" for i, c in enumerate(bibliography, 1))
            st.download_button(
                "⬇ Download Bibliography",
                data=full_bib,
                file_name=f"bibliography_{cite_style.lower()}.txt",
                mime="text/plain",
            )
        else:
            st.warning("Please enter at least one source.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5: TONE ADJUSTER
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    module_header("🎛️", "icon-blue", "Tone Adjuster",
                  "Shift register from Academic → Professional → Conversational")

    tone_text = st.text_area(
        "Text to adjust",
        value=st.session_state.current_draft,
        height=250,
        placeholder="Paste text to adjust the tone...",
        label_visibility="collapsed",
    )

    st.markdown("**Tone Spectrum**")
    tone_value = st.slider(
        "Tone",
        min_value=0,
        max_value=2,
        value=0,
        step=1,
        format="%d",
        label_visibility="collapsed",
    )
    
    col_tl, col_tm, col_tr = st.columns(3)
    tone_labels_map = {0: ("Strictly Academic", "📚 Formal, hedged, third-person"), 
                       1: ("Professional", "💼 Clear, direct, polished"), 
                       2: ("Conversational", "💬 Natural, accessible, relatable")}
    selected_label, selected_desc = tone_labels_map[tone_value]
    
    st.markdown(f"""
    <div style="text-align:center;padding:12px;background:rgba(232,184,75,0.08);border:1px solid rgba(232,184,75,0.2);border-radius:8px;margin:8px 0 16px">
        <div style="font-size:1rem;font-weight:600;color:#E8B84B">{selected_label}</div>
        <div style="font-size:0.8rem;color:#9AA3B8;margin-top:4px">{selected_desc}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="display:flex;justify-content:space-between"><span style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#5A6480;text-transform:uppercase">📚 Academic</span><span style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#5A6480;text-transform:uppercase">💼 Professional</span><span style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#5A6480;text-transform:uppercase">💬 Conversational</span></div>', unsafe_allow_html=True)

    if st.button("✦ Adjust Tone", use_container_width=False, key="tone_btn"):
        if tone_text.strip():
            with st.spinner(f"Adjusting to {selected_label} tone..."):
                adjusted = adjust_tone(tone_text, tone_value)
                save_version(tone_text, f"Before Tone → {selected_label}")
                save_version(adjusted, f"Tone: {selected_label}")

            st.markdown("---")
            col_orig, col_adj = st.columns(2, gap="medium")
            with col_orig:
                st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.72rem;text-transform:uppercase;color:#F87171;margin-bottom:8px">◀ ORIGINAL</div>', unsafe_allow_html=True)
                st.text_area("original_tone", value=tone_text, height=350, label_visibility="collapsed", disabled=True, key="tone_orig")
            with col_adj:
                st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:0.72rem;text-transform:uppercase;color:#2DD4BF;margin-bottom:8px">▶ {selected_label.upper()}</div>', unsafe_allow_html=True)
                edited_adjusted = st.text_area("adjusted_tone", value=adjusted, height=350, label_visibility="collapsed", key="tone_adj")

            if st.button("💾 Use Adjusted Version"):
                st.session_state.current_draft = edited_adjusted
                save_version(edited_adjusted, f"Accepted: {selected_label}")
                st.success("✓ Draft updated!")
        else:
            st.warning("No text to adjust.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6: VERSION HISTORY
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    module_header("🕒", "icon-gold", "Version History",
                  "Full audit trail of all edits and transformations")

    if not st.session_state.version_history:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:#5A6480">
            <div style="font-size:2rem;margin-bottom:12px">📭</div>
            <div style="font-family:IBM Plex Mono,monospace;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.1em">
                No versions saved yet
            </div>
            <div style="font-size:0.85rem;margin-top:8px">
                Generate a draft or humanize text to start tracking changes.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:0.78rem;color:#5A6480;margin-bottom:16px">{len(st.session_state.version_history)} versions tracked</div>', unsafe_allow_html=True)

        for idx, version in enumerate(st.session_state.version_history):
            with st.expander(
                f"[{version['timestamp']}] {version['operation']} · #{version['hash']}"
            ):
                col_v1, col_v2 = st.columns([3, 1])
                with col_v1:
                    st.text_area(
                        f"v{idx}",
                        value=version["text"],
                        height=200,
                        label_visibility="collapsed",
                        key=f"ver_{idx}_{version['hash']}",
                        disabled=True,
                    )
                with col_v2:
                    words = len(version["text"].split())
                    st.metric("Words", words)
                    ai_score = check_integrity(version["text"])["score"] if len(version["text"].split()) > 50 else 0
                    st.metric("AI Score", f"{ai_score}%")
                    if st.button("↩ Restore", key=f"restore_{idx}_{version['hash']}"):
                        st.session_state.current_draft = version["text"]
                        st.success(f"✓ Restored version from {version['timestamp']}")
                        st.rerun()

        col_dl, col_cl = st.columns([1, 1])
        with col_cl:
            if st.button("🗑 Clear History"):
                st.session_state.version_history = []
                st.rerun()
        with col_dl:
            history_export = json.dumps(
                [{"timestamp": v["timestamp"], "operation": v["operation"], "text": v["text"]}
                 for v in st.session_state.version_history],
                indent=2
            )
            st.download_button(
                "⬇ Export History (JSON)",
                data=history_export,
                file_name="version_history.json",
                mime="application/json",
            )
