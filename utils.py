import concurrent.futures
from typing import Dict, Tuple
from openai import OpenAI

COLUMBUS_ESTABLISHMENT = (
    "> \"**The Dawn of a Global Era.** The 1492 expedition marked a pivotal threshold in human history, bridging the Old World and the New. Despite logistical challenges, the voyage expanded the frontiers of Western civilization, facilitating a permanent global exchange of goods, culture, and theology. It laid the institutional foundations for modern nation-states in the Americas and integrated isolated ecosystems into the world economy.\""
)
COLUMBUS_MONEY = (
    "> \"**A High-Risk Venture Capital Investment.** Forget the adventure narrative; look at the balance sheet. The voyage was funded by the Spanish Crown specifically to break the Ottoman monopoly on spice trade routes. The immediate driver was not 'civilization,' but the desperate need for new markets and the extraction of gold and silver—resources that would later fuel European inflation and the rise of merchant capitalism.\""
)
COLUMBUS_SUBTEXT = (
    "> \"**The Myth of 'Discovery'.** The term itself is a colonial construct—one cannot 'discover' a land already inhabited by millions. This narrative silences indigenous agency and sanitizes the subsequent demographic collapse as 'expansion.' 1492 was not a meeting, but the beginning of a systematic erasure of non-Western epistemologies and the imposition of a hegemonic racial hierarchy.\""
)

PROMPT_ESTABLISHMENT = (
    "You are an official historian tasked with producing a concise, balanced account. "
    "Prioritize institutional continuity, archival records, legal frameworks, and procedural legitimacy. "
    "Distill complexity into a coherent narrative grounded in validated sources and public administration. "
    "Output Requirements: Use Markdown formatting. Use **bold** for key terms. Structure your response with bullet points or short paragraphs for readability. Keep it under 150 words."
)

PROMPT_MONEY = (
    "You are a materialist historian focusing on economic determinism. "
    "Analyze incentives, capital flows, interest groups, and institutional arrangements shaping outcomes. "
    "Ask empirically who benefits and trace subsidies, trade routes, and financial instruments. "
    "Output Requirements: Use Markdown formatting. Use **bold** for key terms. Structure your response with bullet points or short paragraphs for readability. Keep it under 150 words."
)

PROMPT_SUBTEXT = (
    "You are a critical theorist drawing on postmodern and Foucauldian analysis. "
    "Interrogate discourse, power circulation, institutional vocabularies, and silences. "
    "Expose regimes of truth, classification, and governance while highlighting subaltern voices and resistance. "
    "Output Requirements: Use Markdown formatting. Use **bold** for key terms. Structure your response with bullet points or short paragraphs for readability. Keep it under 150 words."
)

def _mock_establishment(event: str) -> str:
    return (
        f"Regarding {event}, an official historiographical account privileges institutional continuity and documentary authority. "
        "Archival records, legislative decrees, and certified commissions shape a narrative of orderly progression in which causes are cataloged, actors are named, and outcomes are standardized for civic instruction. "
        "Emphasis rests on procedural legitimacy and the stability of public administration; disruptions are treated as anomalies reconciled by law, policy, or reform. "
        "Complexity is distilled into timelines, charters, and minutes, producing a coherent summary that affirms the integrity of the established order. "
        "Meaning derives from validated sources and formal precedence, situating the event within a framework designed to sustain continuity and public trust."
    )

def _mock_money(event: str) -> str:
    return (
        f"Viewed through economic determinism, {event} emerges from converging incentives, capital flows, and strategic positioning. "
        "Financial actors—merchants, banks, investors, and the state’s fiscal apparatus—seek returns, arbitrage, and market access, translating uncertainty into instruments and contracts. "
        "Winners consolidate gains via taxation regimes, corporate charters, and infrastructural sponsorship; losers absorb externalities as volatility, debt, or dispossession. "
        "Institutions arbitrate competition while interest groups broker favorable terms, ensuring accumulation persists across cycles. "
        "The question of who benefits is not rhetorical but empirical: follow the subsidies, trade routes, and underwriting risks to locate the durable advantages engineered around the event."
    )

def _mock_subtext(event: str) -> str:
    return (
        f"Under a postmodern and Foucauldian reading, {event} is a discourse event rather than a neutral sequence of facts. "
        "Power circulates through institutional vocabularies, disciplinary norms, and silences that delimit who may speak and what counts as knowledge. "
        "Subaltern voices appear as objects of classification while expert terminology naturalizes surveillance, risk, and correction. "
        "The archive functions as an instrument of governance, scripting compliance through categories and metrics that render subjects legible and manageable. "
        "Resistance survives in fragments—rumor, performance, vernacular theory—challenging the inevitability of official plots and exposing regimes of truth that organize perception and consent."
    )

def _mock_text_for_perspective(name: str, event: str) -> str:
    key = name.lower().strip()
    special = (event == "the event") or ("columbus" in event.lower())
    if special:
        if key in ("establishment", "the establishment"):
            return COLUMBUS_ESTABLISHMENT
        if key in ("money", "follow the money"):
            return COLUMBUS_MONEY
        if key in ("subtext", "the subtext"):
            return COLUMBUS_SUBTEXT
    if key in ("establishment", "the establishment"):
        return _mock_establishment(event)
    if key in ("money", "follow the money"):
        return _mock_money(event)
    if key in ("subtext", "the subtext"):
        return _mock_subtext(event)
    return _mock_establishment(event)

def analyze_perspective(perspective_name: str, prompt: str, user_text: str, api_key: str) -> Tuple[str, str]:
    event = user_text.strip() if user_text.strip() else "the event"
    if not api_key:
        return perspective_name, _mock_text_for_perspective(perspective_name, event)
    try:
        client = OpenAI(api_key=api_key)
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Event: {event}\nProduce a ~100-word analysis."},
        ]
        # Try chat.completions for broad compatibility; if provider/model errors, we fall back to mock.
        resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, temperature=0.7)
        text = resp.choices[0].message.content.strip()
        return perspective_name, text
    except Exception:
        return perspective_name, _mock_text_for_perspective(perspective_name, event)

def yield_rashomon_perspectives(user_text: str, api_key: str):
    """
    Generator that yields (name, text) tuples as they complete.
    Useful for streaming UI updates.
    """
    tasks = [
        ("The Establishment", PROMPT_ESTABLISHMENT),
        ("Follow the Money", PROMPT_MONEY),
        ("The Subtext", PROMPT_SUBTEXT),
    ]
    # We use ThreadPoolExecutor to run three I/O-bound API calls in parallel.
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(analyze_perspective, name, prompt, user_text, api_key)
            for name, prompt in tasks
        ]
        for fut in concurrent.futures.as_completed(futures):
            yield fut.result()

def get_rashomon_perspectives(user_text: str, api_key: str) -> Dict[str, str]:
    results: Dict[str, str] = {}
    for name, text in yield_rashomon_perspectives(user_text, api_key):
        results[name] = text
    return results
