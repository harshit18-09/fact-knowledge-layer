import streamlit as st
import tempfile
import os
from extract import extract_text_from_pdf
from facts_extractor import extract_facts_from_chunk
from storage import add_document, add_facts, get_all_facts
from compare import (
    find_corroborations,
    find_contradictions,
    find_reconciled,
    get_failure_example
)

st.set_page_config(page_title="Fact Knowledge Layer", layout="wide")
st.title(" Fact Knowledge Layer")
st.markdown("Upload multiple PDFs – the system extracts facts and finds relationships across documents.")

if "doc_ids" not in st.session_state:
    st.session_state.doc_ids = []

with st.sidebar:
    st.header(" Upload PDFs")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    if uploaded_file:
        with st.spinner("Processing... This may take a minute."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            pages = extract_text_from_pdf(tmp_path)
            
            chunks = []
            for page in pages:
                paragraphs = page["text"].split("\n\n")
                for para in paragraphs:
                    if len(para) > 100:
                        chunks.append({"page": page["page"], "text": para[:100]})
            
            doc_id = add_document(uploaded_file.name)
            all_facts = []
            for chunk in chunks:
                facts = extract_facts_from_chunk(chunk["text"], doc_id, chunk["page"])
                all_facts.extend(facts)
            
            add_facts(doc_id, all_facts)
            
            st.session_state.doc_ids.append(doc_id)
            
            st.success(f" Extracted {len(all_facts)} facts from {uploaded_file.name}")
            os.unlink(tmp_path)
    
    st.write(f"**Documents uploaded:** {len(st.session_state.doc_ids)}")

tab1, tab2, tab3 = st.tabs([" Extracted Facts", " Four Cases", " All Facts"])

with tab1:
    all_facts = get_all_facts()
    if all_facts:
        for f in all_facts[-20:]: 
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{f.get('statement', 'N/A')}**")
                with col2:
                    st.caption(f"Page {f.get('page', '?')}")
                st.caption(f"Entity: {f.get('entity', 'N/A')} | Attribute: {f.get('attribute', 'N/A')}")
                st.divider()
    else:
        st.info("Upload PDFs to see extracted facts.")

with tab2:
    st.header(" The Four Required Cases")
    
    all_facts = get_all_facts()
    num_docs = len(st.session_state.doc_ids)
    
    if num_docs < 2:
        st.warning(f" Only {num_docs} document(s) uploaded. Upload at least 2 PDFs to see cross-document relationships.")
    
    st.subheader("1. Corroborated Facts")
    corr = find_corroborations()
    if corr:
        for c in corr[:3]:
            st.success(c["explanation"])
            with st.expander("View source evidence"):
                st.caption(f"Fact A: {c['fact_a']['statement']} (Page {c['fact_a']['page']})")
                st.caption(f"Fact B: {c['fact_b']['statement']} (Page {c['fact_b']['page']})")
    else:
        st.info("No corroborations found yet. Upload more documents.")
    
    st.subheader("2. Genuine Contradictions")
    cont = find_contradictions()
    if cont:
        for c in cont[:3]:
            st.error(c["explanation"])
    else:
        st.info("No contradictions found yet.")
    
    st.subheader("3. Reconciled by Context")
    rec = find_reconciled()
    if rec:
        for c in rec[:3]:
            st.warning(c["explanation"])
    else:
        st.info("No reconciled contradictions found yet.")
    
    st.subheader("4. Extraction / Reasoning Failure")
    failure = get_failure_example()
    st.markdown(f"**Issue:** {failure['description']}")
    st.markdown(f"**Handling:** {failure['handling']}")
    st.markdown(f"**Improvement:** {failure['improvement']}")

with tab3:
    st.header("All Extracted Facts (Across All Documents)")
    all_facts = get_all_facts()
    if all_facts:
        st.dataframe(all_facts)
    else:
        st.info("No facts in storage yet.")