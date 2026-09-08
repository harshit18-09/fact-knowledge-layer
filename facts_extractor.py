import json
import re
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
LOCAL_MODEL = "llama3.2:3b"

def safe_json_parse(raw_text):
    if not raw_text or not raw_text.strip():
        return None

    raw_text = re.sub(r'^```json\s*', '', raw_text.strip())
    raw_text = re.sub(r'^```\s*', '', raw_text)
    raw_text = re.sub(r'\s*```$', '', raw_text)
    raw_text = raw_text.strip()

    try:
        parsed = json.loads(raw_text)
        if isinstance(parsed, dict):
            for key in ["facts", "statements", "fact", "statement", "data", "items", "results"]:
                if key in parsed and isinstance(parsed[key], list):
                    return parsed[key]
            if "statement" in parsed or "entity" in parsed:
                return [parsed]
        if isinstance(parsed, list):
            return parsed
    except json.JSONDecodeError:
        pass

    match = re.search(r'\[\s*\{.*?\}\s*\]', raw_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    match = re.search(r'\{\s*"facts"\s*:\s*\[', raw_text, re.DOTALL)
    if match:
        try:
            start = match.start()
            brace_count = 0
            for i in range(start, len(raw_text)):
                if raw_text[i] == '{':
                    brace_count += 1
                elif raw_text[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        obj_str = raw_text[start:i+1]
                        parsed = json.loads(obj_str)
                        if "facts" in parsed and isinstance(parsed["facts"], list):
                            return parsed["facts"]
                        break
        except:
            pass

    return None

def extract_facts_from_chunk(chunk_text, doc_id, page_num):
    prompt = f"""Extract facts from the text as a JSON array. Each fact must have: statement (string), fact_type ("numeric"/"semantic"), entity (string), attribute (string), value (number or null), unit (string or null), year (integer or null), period (string or null).

Text: {chunk_text}

JSON array:"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": LOCAL_MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.1,
                "max_tokens": 300,        
                "format": "json",        
            },
            timeout=120 
        )
        if response.status_code == 200:
            raw = response.json().get("response", "")
            print(f"RAW: {raw[:200]}...")

            if not raw:
                return []

            facts = safe_json_parse(raw)
            if facts and isinstance(facts, list):
                for f in facts:
                    f["document_id"] = doc_id
                    f["page"] = page_num
                    f["text_snippet"] = chunk_text[:150] + "..."
                return facts
            else:
                print("Failed to parse JSON")
                return []
        else:
            print(f"Ollama error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []