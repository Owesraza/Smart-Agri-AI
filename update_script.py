with open("generate_paper.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace the text to include \cite{vaswani2017attention}
target = r"Chunks are embedded using Sentence-BERT (\texttt{all-MiniLM-L6-v2})~\cite{reimers2019sentence},"
replacement = r"Chunks are embedded using Sentence-BERT (\texttt{all-MiniLM-L6-v2})~\cite{reimers2019sentence}, which leverages the multi-head self-attention architecture of Transformers~\cite{vaswani2017attention} to map each passage $T_i$ into a normalized dense semantic representation:"

if target in code:
    code = code.replace(target, replacement)
    with open("generate_paper.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("Successfully updated generate_paper.py")
else:
    print("Target string not found!")

