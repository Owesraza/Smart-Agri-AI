import os
import urllib.request
import ssl

# Ensure SSL context allows downloads
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

DOWNLOAD_TARGETS = [
    ("4_Lewis_2020_Retrieval_Augmented_Generation_NeurIPS.pdf", "https://arxiv.org/pdf/2005.11401.pdf"),
    ("5_Johnson_2021_Billion_Scale_Similarity_Search_FAISS.pdf", "https://arxiv.org/pdf/1702.08734.pdf"),
    ("6_Reimers_2019_Sentence_BERT_EMNLP.pdf", "https://aclanthology.org/D19-1410.pdf"),
    ("8_Acharya_2006_Agricultural_Marketing_India.pdf", "https://ageconsearch.umn.edu/record/204439/files/01-Acharya.pdf"),
    ("18_Shwartz_Ziv_2022_Tabular_Data_Deep_Learning.pdf", "https://arxiv.org/pdf/2106.03253.pdf"),
    ("21_Chen_2016_XGBoost_KDD.pdf", "https://arxiv.org/pdf/1603.02754.pdf"),
    ("22_Grover_2012_Price_Discovery_Market_Integration.pdf", "https://ageconsearch.umn.edu/record/137688/files/24-DK-Grover.pdf"),
    ("23_Gummagolmath_2011_Onion_Supply_Chain_Maharashtra.pdf", "https://ageconsearch.umn.edu/record/119409/files/24-SS-Gummagolmath.pdf"),
    ("24_Brown_2020_Language_Models_Few_Shot_Learners.pdf", "https://arxiv.org/pdf/2005.14165.pdf"),
    ("25_Ji_2023_Survey_Hallucination_Natural_Language.pdf", "https://arxiv.org/pdf/2202.03629.pdf"),
    ("28_Vaswani_2017_Attention_Is_All_You_Need.pdf", "https://arxiv.org/pdf/1706.03762.pdf")
]

ref_dir = os.path.dirname(os.path.abspath(__file__))

print(f"Starting download to: {ref_dir}")
for fname, url in DOWNLOAD_TARGETS:
    dest = os.path.join(ref_dir, fname)
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print(f"[ALREADY EXISTS] {fname} ({os.path.getsize(dest)} bytes)")
        continue
    print(f"[DOWNLOADING] {fname} from {url} ...")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp, open(dest, 'wb') as f:
            f.write(resp.read())
        print(f"[SUCCESS] Saved {fname} ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print(f"[FAILED] Could not download {fname}: {e}")

print("\nFinished batch downloads!")
