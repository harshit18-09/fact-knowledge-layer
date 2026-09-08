import json
import uuid
import os

DATA_FILE = "facts_data.json"

def init_storage():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"documents": [], "facts": []}, f, indent=2)

def add_document(filename):
    init_storage()
    with open(DATA_FILE, "r+") as f:
        data = json.load(f)
        doc_id = str(uuid.uuid4())
        data["documents"].append({
            "id": doc_id,
            "filename": filename
        })
        f.seek(0)
        json.dump(data, f, indent=2)
    return doc_id

def add_facts(doc_id, facts):
    init_storage()
    with open(DATA_FILE, "r+") as f:
        data = json.load(f)
        for fact in facts:
            fact["id"] = str(uuid.uuid4())
            fact["document_id"] = doc_id
            data["facts"].append(fact)
        f.seek(0)
        json.dump(data, f, indent=2)

def get_all_facts():
    init_storage()
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        return data["facts"]

def get_all_documents():
    init_storage()
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        return data["documents"]