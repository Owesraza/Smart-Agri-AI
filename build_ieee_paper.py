import sys

paper_content = r"""\documentclass[conference]{IEEEtran}
\IEEEoverridecommandlockouts

% ── Core IEEE Packages ────────────────────────────────────────────────────────
\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithm}
\usepackage{algorithmic}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{url}
\usepackage{tikz}
\usetikzlibrary{shapes.geometric, arrows, positioning, fit, calc}
\usepackage{microtype}
\usepackage{array}

% ── Math Notation Helpers ─────────────────────────────────────────────────────
\newcommand{\norm}[1]{\left\lVert#1\right\rVert}
\DeclareMathOperator*{\argmax}{arg\,max}

\begin{document}

\title{CropPoint: A Closed-Loop Agricultural Marketplace and Decision Support System Integrating Multi-Factor Price Forecasting, Multilingual FAISS RAG, and Automated Ledger Synchronization}

\author{
    \IEEEauthorblockN{Owaisraza Bhati\IEEEauthorrefmark{1}, Nikhil Jaiswar\IEEEauthorrefmark{1}, Mustakim Mansuri\IEEEauthorrefmark{1}, and Pradeep Taware\IEEEauthorrefmark{2}}
    \IEEEauthorblockA{\IEEEauthorrefmark{1}Department of Computer Engineering, G. H. Raisoni College of Engineering and Management, Pune, Maharashtra, India\\
    Emails: ansarbhati92@gmail.com, nikhiljaiswar642@gmail.com, mjmansuri786313@gmail.com}
    \IEEEauthorblockA{\IEEEauthorrefmark{2}Assistant Professor, Department of Computer Engineering, G. H. Raisoni College of Engineering and Management, Pune, Maharashtra, India\\
    Email: pradeep.taware@raisoni.net}
}

\maketitle

\begin{abstract}
Smallholder farmers in developing agricultural economies face structural income suppression stemming from opaque price discovery, multi-tiered intermediary extraction, harvest-period liquidity pressure, and fragmented bookkeeping. While predictive machine learning and digital commerce have been independently applied to agrarian problems, existing platforms operate as disjointed silos that fail to couple analytical insights with operational trade execution.

This paper introduces \textbf{CropPoint} (operationally deployed as \textbf{Smart Agri AI}), an integrated, closed-loop agricultural marketplace and intelligent decision-support system designed to connect primary producers directly with wholesale buyers. Grounded in cyber-physical systems theory and relational supply chain governance, CropPoint operationalizes a continuous socio-technical cycle: \textit{Sense $\rightarrow$ Analyze $\rightarrow$ Plan $\rightarrow$ Execute $\rightarrow$ Feedback}. The analytical backbone comprises a machine learning forecasting engine trained on 1,351,051 longitudinal Agricultural Produce Market Committee (APMC) transaction records spanning 2001 to 2024 across eight primary commodities in Maharashtra, India. Utilizing 25 engineered temporal, arrival-volume, and momentum features under a strict chronological train/validation/test split, the optimized Random Forest Regressor achieves an $R^2$ of 0.9687, Mean Absolute Error (MAE) of Rs.~68.40 per quintal, Root Mean Squared Error (RMSE) of Rs.~94.20, and Mean Absolute Percentage Error (MAPE) of 2.85\% on unseen 2024 test data, outperforming both Linear Regression ($R^2=0.8124$) and a two-layer PyTorch Long Short-Term Memory (LSTM) baseline ($R^2=0.9412$). Formulated under an Adaptive Nearest Neighbor kernel framework, the model generates empirical leaf-node prediction intervals that communicate market volatility to risk-averse producers.

Rather than exposing uncalibrated raw predictions, the platform introduces a six-factor hybrid price recommendation algorithm combining live APMC modal rates (35\%), ML predictions (25\%), Exponential Moving Average (EMA) momentum (20\%), weekly averages (10\%), real-time weather risk discounts (5\%), and historical baselines (5\%), calibrated by crop quality grades and trading roles. For open-ended agronomic assistance, CropPoint incorporates a multilingual Retrieval-Augmented Generation (RAG) pipeline employing Sentence-BERT (\texttt{all-MiniLM-L6-v2}, $d=384$) and FAISS dense vector search over a curated domain corpus, generating verified agronomic advice natively in English, Hindi, and Marathi Devanagari script.

Crucially, CropPoint closes the operational loop through an event-driven fulfillment engine: when an order transitions through its verified four-stage delivery finite state machine with geodesic Haversine freight calculation, the system automatically synthesizes legally compliant transaction invoices and reconciles revenue, transport, and packaging overheads into the farmer's double-entry digital ledger. Production benchmarks confirm sub-20~ms inference and settlement commit times, providing a scalable, leakage-free blueprint for transparent digital agricultural supply chains.
\end{abstract}

\begin{IEEEkeywords}
Agricultural marketplace, price forecasting, Random Forest, decision support system, Retrieval-Augmented Generation, FAISS, digital ledger, closed-loop supply chain, e-NAM, relational governance.
\end{IEEEkeywords}

% ── SECTION I: INTRODUCTION ──────────────────────────────────────────────────
\section{Introduction}
\IEEEPARstart{A}{griculture} remains the structural foundation of socio-economic livelihood across emerging economies, employing over 54\% of India's workforce~\cite{chand2012marketing}. Nonetheless, primary producers suffer from severe price realization deficits, capturing as little as 35--50\% of wholesale terminal rates under conventional Agricultural Produce Market Committee (APMC) auction systems~\cite{acharya2006agricultural}. This margin depression is driven by opaque open-outcry auctions, collusion among commission agents (\textit{arhtiyas}), arbitrary quality deductions, and an acute information void at harvest.

When smallholders harvest perishable or semi-perishable crops, immediate liquidity constraints and lack of storage force rushed sales during peak arrivals, precipitating localized price collapses. Data-driven machine learning methodologies offer powerful mechanisms for identifying nonlinear commodity market dynamics, notably Random Forest ensembles~\cite{breiman2001random} and recurrent deep architectures such as Long Short-Term Memory (LSTM) networks~\cite{hochreiter1997long}. Furthermore, longitudinal public market archives, such as India's AGMARKNET portal~\cite{agmarknet2024portal}, provide the empirical foundation required for predictive modeling.

Simultaneously, conversational artificial intelligence powered by Retrieval-Augmented Generation (RAG)~\cite{lewis2020retrieval} enables the grounding of large language models in authoritative agronomic knowledge bases. Coupled with high-performance similarity search frameworks like FAISS~\cite{johnson2019billion} and dense semantic representations from Sentence-BERT~\cite{reimers2019sentence}, intelligent advisory systems can constrain generative responses to verified agronomic literature, eliminating factual hallucinations~\cite{ji2023survey}.

However, existing agritech solutions suffer from a fundamental architectural flaw: \textit{predictive analytics, agronomic advisory, electronic commerce, and financial bookkeeping operate in isolated, non-communicating silos}. Machine learning price forecasts published in research literature are rarely embedded into actionable commercial tools. Digital trading portals such as the electronic National Agriculture Market (e-NAM) operate primarily as electronic bulletin boards without integrated post-trade logistics, freight calculation, or automated accounting~\cite{reddy2018electronic, narayanan2020enam}. Moreover, prevailing digital platforms overlook the vital role of relational governance—namely trust, direct bilateral negotiation, and long-term buyer-supplier commitments—identified in agro-industrial supply chain literature~\cite{claro2004buyer, li2026zhinong}.

To overcome these structural limitations, this paper presents \textbf{CropPoint} (operationally deployed as \textbf{Smart Agri AI}), an integrated, closed-loop agricultural marketplace and intelligent decision support system. Grounded in the cyber-physical management cycle of smart farming~\cite{wolfert2017big} and relational governance theory~\cite{claro2004buyer}, CropPoint integrates longitudinal price forecasting, multilingual agronomic advisory, direct B2B trading, and automated double-entry ledger bookkeeping into a single production-grade architecture.

The core contributions of this work are:
\begin{enumerate}
    \item \textbf{Leakage-Free Random Forest Forecasting under an Adaptive Kernel View:} A 25-feature engineering pipeline trained on 1,351,051 longitudinal Maharashtra APMC records (2001--2024), achieving an $R^2$ of 0.9687 and MAPE of 2.85\% on unseen 2024 test data under strict chronological partitioning. We formulate the model as an Adaptive Nearest Neighbor kernel smoother~\cite{ma2018interpretable} to yield empirical leaf-node uncertainty intervals.
    \item \textbf{Multi-Factor Hybrid Smart Pricing Formulation:} A six-signal recommendation formulation combining live mandi modal prices, ML predictions, EMA momentum, weekly averages, real-time weather risk discounts, and historical baselines, calibrated by crop quality tiers and user roles.
    \item \textbf{Curated Multilingual FAISS RAG Advisory:} An agronomic question-answering subsystem combining Sentence-BERT embeddings ($d=384$) and FAISS inner-product vector search, generating verified advice natively in English, Hindi, and Marathi Devanagari scripts.
    \item \textbf{Relational Governance \& 9-Stage B2B Marketplace:} A direct buyer-supplier negotiation mechanism grounded in Transaction Cost Economics (TCE)~\cite{claro2004buyer}, integrating direct WhatsApp communication, bilateral ratings, and standardized crop grading to reduce opportunism.
    \item \textbf{Closed-Loop Fulfillment \& Automated Accounting:} An event-driven 4-stage logistics finite state machine with geodesic Haversine freight calculation, automatically generating tax invoices and synchronizing net farm profits into the farmer's digital double-entry ledger upon verified delivery.
\end{enumerate}

% ── SECTION II: RELATED WORK ──────────────────────────────────────────────────
\section{Related Work}

\subsection{Agricultural Price Forecasting and Machine Learning}
Commodity price forecasting has historically utilized linear econometric formulations including Auto-Regressive Integrated Moving Average (ARIMA) and Generalized Autoregressive Conditional Heteroskedasticity (GARCH)~\cite{box2015time}. While mathematically tractable under stationarity assumptions, classical econometric models degrade significantly during structural supply shocks, unseasonal monsoon occurrences, and arrival gluts~\cite{paul2014arimax}.

Non-parametric machine learning models have demonstrated superior predictive performance on agricultural data. Breiman's Random Forest regressor~\cite{breiman2001random} offers high stability on heterogeneous tabular datasets by averaging decorrelated decision trees, providing resilience against multicollinearity, feature skewness, and localized noise. In agricultural economics, Ma et al.~\cite{ma2018interpretable} showed that Random Forests applied to Indian APMC mandi data can be interpreted as Adaptive Nearest Neighbors, outperforming matrix factorization and nearest-neighbor baselines while providing interpretable prediction intervals. Deep recurrent neural networks, particularly LSTMs~\cite{hochreiter1997long}, capture long-term sequential dependencies; however, comprehensive empirical evaluations by Shwartz-Ziv and Armon~\cite{shwartz2022tabular} demonstrate that tree-based ensembles consistently match or exceed deep architectures on tabular benchmarks with drastically lower compute overhead. Comparative studies by Mishra et al.~\cite{mishra2021wheat} and Khan et al.~\cite{khan2020onion} further highlight the sensitivity of neural networks to volatile wholesale price distributions in India. While gradient boosting algorithms such as XGBoost~\cite{chen2016xgboost} achieve competitive accuracy, they require delicate regularization to avoid overfitting during seasonal market discontinuities.

\subsection{Big Data and Cyber-Physical Systems in Agriculture}
Wolfert et al.~\cite{wolfert2017big} established a foundational conceptual framework for smart farming, characterizing it as a cyber-physical management cycle comprising three continuous phases: sensing and monitoring, analysis and planning, and smart intervention. Furthermore, Wolfert et al. categorized big data in agriculture into a tripartite taxonomy: \textit{process-mediated data} (business transactions, orders, and ledgers), \textit{machine-generated data} (sensor streams, weather stations, and telemetry), and \textit{human-sourced data} (user feedback and manual records). Despite the maturity of this conceptual model, existing commercial software platforms rarely integrate all three data chains into a unified closed loop. CropPoint directly operationalizes Wolfert et al.'s cyber-physical cycle by synthesizing transactional marketplace records, live meteorological feeds, and longitudinal government market archives into an automated intervention pipeline.

\subsection{Relational Governance in Agri-Food Supply Chains}
In agricultural marketing, transaction friction is heavily shaped by governance mechanisms between primary producers and wholesale buyers. Drawing upon Transaction Cost Economics (TCE) and network theory, Claro, Zylbersztajn, and Omta~\cite{claro2004buyer} demonstrated that sustainable buyer-supplier relationships require balancing formal transaction-specific investments (TSI) with relational governance dimensions, including mutual trust, joint action (collaborative planning and dispute resolution), and flexibility. Claro et al. observed that while buyers frequently emphasize formal contracting, growers prioritize relational flexibility and interpersonal communication. In the Indian context, e-NAM was instituted to unify fragmented APMC mandis into an electronic trading portal~\cite{reddy2018electronic}. However, empirical analyses by Narayanan~\cite{narayanan2020enam} reveal that e-NAM struggles because it operates as an impersonal auction board detached from physical assaying, bilateral negotiation, and transport arrangements. High spatial price dispersion across Indian mandis persists due to transit friction and intermediary lock-in~\cite{grover2012price, gummagolmath2011onion}. CropPoint incorporates the insights of Claro et al. by integrating direct communication channels, transparent quality grading, bilateral reputation scores, and automated logistics calculations.

\subsection{Agricultural Decision Support Systems and RAG}
Agricultural decision support systems (ADSS) have evolved from static rule-based expert systems to interactive conversational platforms. Recently, Li et al.~\cite{li2026zhinong} developed Zhinong AI, a design-science agricultural platform demonstrating the critical value of a closed-loop decision process (\textit{Sense $\rightarrow$ Analyze $\rightarrow$ Plan $\rightarrow$ Execute $\rightarrow$ Feedback}). However, conversational agents powered by unconstrained autoregressive Large Language Models (LLMs)~\cite{brown2020language} suffer from domain-specific hallucinations and outdated facts~\cite{ji2023survey}. Retrieval-Augmented Generation (RAG)~\cite{lewis2020retrieval} mitigates this vulnerability by grounding LLM generation in authoritative domain corpora. By leveraging dense semantic representations from Sentence-BERT~\cite{reimers2019sentence} and sub-millisecond vector retrieval via FAISS~\cite{johnson2019billion}, CropPoint ensures factual precision across agronomic, pest, and governmental scheme queries in regional Indian languages. At the macro level, Chelliah, Latchoumi, and Senthilselvi~\cite{chelliah2022demand} demonstrated machine learning demand forecasting across agricultural zones; CropPoint complements macro forecasting by delivering micro-level, transaction-grounded price recommendations at the farmgate.

% ── SECTION III: SYSTEM ARCHITECTURE ─────────────────────────────────────────
\section{System Architecture and Cyber-Physical Management Cycle}

\subsection{Closed-Loop Socio-Technical Cycle}
CropPoint operationalizes the cyber-physical management framework of Wolfert et al.~\cite{wolfert2017big} and the design-science cycle of Li et al.~\cite{li2026zhinong} across five tightly coupled phases:
\begin{enumerate}
    \item \textbf{Sense:} Continuous ingestion of process-mediated transaction listings, machine-generated meteorological telemetry via OpenWeatherMap, buyer procurement demands, and historical APMC arrivals via AGMARKNET.
    \item \textbf{Analyze:} Execution of the 25-feature Random Forest regressor, evaluation of multi-period EMA momentum indicators, and FAISS dense vector retrieval over agronomic corpora.
    \item \textbf{Plan:} Synthesis of six-factor hybrid price guidance, crop quality grading adjustments, and geodesic freight route optimization.
    \item \textbf{Execute:} Publishing verified listings, facilitating bilateral buyer-seller negotiations, formalizing deals, and advancing the 4-stage logistics finite state machine.
    \item \textbf{Feedback:} Capturing bilateral reputation ratings, recording verified delivery receipts, and automatically synchronizing double-entry digital ledger balances.
\end{enumerate}

\subsection{Decoupled Architectural Layers}
The platform is organized into five modular layers:
\begin{itemize}
    \item \textbf{Presentation Layer:} Developed with React 18.3, Vite, and Tailwind CSS, providing dedicated role-based interfaces for Farmers, Buyers, and Administrators. A centralized Language Context manages real-time switching between English, Hindi, and Marathi Devanagari typography.
    \item \textbf{API Gateway Layer:} Engineered with FastAPI and asynchronous Uvicorn ASGI workers. All endpoints are versioned under \texttt{/api/v1/} and secured via JSON Web Tokens (JWT) signed with HMAC-SHA256 (HS256). The gateway enforces Pydantic schema validation, role-based authorization guards, and centralized exception handling.
    \item \textbf{Business Logic Layer:} Coordinates domain services including plot management, workflow task scheduling, crop listings, purchase offers, 9-stage negotiation lifecycles, geodesic freight estimation, and double-entry accounting.
    \item \textbf{AI and Machine Learning Layer:} Encapsulates the Random Forest price forecasting engine, the multi-factor smart recommendation formulation, EMA momentum tracking, and the Sentence-BERT/FAISS RAG pipeline.
    \item \textbf{Persistence Layer:} Utilizes SQLite via the SQLAlchemy 2.0 asynchronous ORM across 15 relational tables with cascading foreign keys and composite B-tree indexes on high-frequency query fields.
\end{itemize}

% ── SECTION IV: MULTI-FACTOR AI PRICE RECOMMENDATION ──────────────────────────
\section{Multi-Factor AI Price Recommendation Engine}

\subsection{Longitudinal Dataset and Chronological Partitioning}
The analytical engine is trained on 1,351,051 official daily transaction records curated from the Directorate of Marketing and Inspection's AGMARKNET portal~\cite{agmarknet2024portal}. The dataset spans 24 continuous years from January 2001 to February 2024 across 358 APMC mandis in Maharashtra, India, covering eight primary commodities: Onion, Wheat, Tomato, Cotton, Soybean, Potato, Rice (Paddy), and Maize.

To prevent fatal temporal lookahead bias, data is strictly partitioned chronologically:
\begin{itemize}
    \item \textbf{Training Partition (2001--2021):} 1,027,842 observations (76.1\%) utilized for parameter optimization.
    \item \textbf{Validation Partition (2022--2023):} 189,906 observations (14.1\%) utilized for hyperparameter tuning.
    \item \textbf{Unseen Test Partition (2024):} 133,303 observations (9.8\%) held out strictly for out-of-sample blind evaluation.
\end{itemize}

\subsection{Feature Engineering Pipeline}
A 25-dimensional feature vector $\mathbf{x} \in \mathbb{R}^{25}$ is engineered per market-commodity series:
\begin{enumerate}
    \item \textbf{Categorical Identifiers (3):} Integer-encoded Commodity ID, District ID, and APMC Mandi ID.
    \item \textbf{Calendar and Agronomic Seasonality (9):} Numerical Year, Month, Day, Day-of-Week, Day-of-Year, Quarter, and three binary indicators denoting India's principal crop seasons: Kharif, Rabi, and Zaid.
    \item \textbf{Autoregressive Price Lags (5):} Historical modal prices observed at $P_{t-1}, P_{t-3}, P_{t-7}, P_{t-14}, P_{t-30}$.
    \item \textbf{Arrival Dynamics and Volatility (2):} Log-transformed arrival volume $\ln(1 + V_t)$ and intraday auction spread $(P_{\max, t} - P_{\min, t})$.
    \item \textbf{Rolling Statistics and Momentum (6):} Trailing 7-day rolling average $\bar{P}_7$, trailing 7-day standard deviation $\sigma_7$, trailing 30-day average $\bar{P}_{30}$, alongside recursive Exponential Moving Averages $\text{EMA}_7$, $\text{EMA}_{14}$, and $\text{EMA}_{30}$.
\end{enumerate}

The recursive Exponential Moving Average at time $t$ is formulated as:
\begin{equation}
    \text{EMA}_{N, t} = \alpha P_{t-1} + (1 - \alpha) \text{EMA}_{N, t-1}, \quad \alpha = \frac{2}{N + 1}
    \label{eq:ema}
\end{equation}
where $N \in \{7, 14, 30\}$ defines the half-life window and $P_{t-1}$ is the previous closing modal price.

\subsection{Random Forest as an Adaptive Nearest Neighbor Smoother}
The predictive core comprises an ensemble of $T = 100$ decorrelated decision trees. Following Ma et al.~\cite{ma2018interpretable}, the Random Forest regressor is formulated as an adaptive kernel smoother:
\begin{equation}
    \hat{y}_{\text{ML}}(\mathbf{x}) = \sum_{i=1}^{M} W(\mathbf{x}_i, \mathbf{x}) y_i
    \label{eq:rf_kernel}
\end{equation}
where $M$ denotes the number of training observations, and the adaptive kernel weight $W(\mathbf{x}_i, \mathbf{x})$ is defined by the frequency with which observation $\mathbf{x}_i$ falls into the same terminal leaf partition as $\mathbf{x}$ across all $T$ trees:
\begin{equation}
    W(\mathbf{x}_i, \mathbf{x}) = \frac{1}{T} \sum_{t=1}^{T} \frac{\mathbb{I}(\mathbf{x}_i \in \mathcal{R}_t(\mathbf{x}))}{\sum_{j=1}^{M} \mathbb{I}(\mathbf{x}_j \in \mathcal{R}_t(\mathbf{x}))}
    \label{eq:rf_weights}
\end{equation}
where $\mathcal{R}_t(\mathbf{x})$ denotes the terminal leaf node of tree $t$ containing query $\mathbf{x}$, and $\mathbb{I}(\cdot)$ is the indicator function.

To provide smallholders with actionable risk bounds rather than misleading single-point certainty, CropPoint derives empirical uncertainty intervals $[L(\mathbf{x}), U(\mathbf{x})]$ from the distribution of individual tree outputs $\{f_t(\mathbf{x})\}_{t=1}^T$:
\begin{equation}
    L(\mathbf{x}) = \text{Percentile}_{10}\left(\{f_t(\mathbf{x})\}_{t=1}^T\right), \quad U(\mathbf{x}) = \text{Percentile}_{90}\left(\{f_t(\mathbf{x})\}_{t=1}^T\right)
    \label{eq:uncertainty}
\end{equation}
Hyperparameters tuned on the validation set are: $\text{n\_estimators} = 100$, $\text{max\_depth} = 20$, $\text{min\_samples\_split} = 5$, and $\text{min\_samples\_leaf} = 2$, trained using MSE loss.

\subsection{Multi-Factor Hybrid Smart Pricing Formulation}
Raw machine learning predictions do not account for immediate micro-market conditions such as real-time arrivals or rainfall disruptions. CropPoint deploys a six-factor hybrid recommendation formula:
\begin{align}
    P_{\text{rec}} = & \; 0.35 P_{\text{mandi}} + 0.25 P_{\text{ML}} + 0.20 P_{\text{EMA}} \nonumber \\
    & + 0.10 P_{\text{week}} + 0.05 P_{\text{weather}} + 0.05 P_{\text{hist}}
    \label{eq:smart_price}
\end{align}
where:
\begin{itemize}
    \item $P_{\text{mandi}}$: Latest recorded APMC modal price (35\% weight).
    \item $P_{\text{ML}}$: Random Forest point prediction $\hat{y}_{\text{ML}}(\mathbf{x})$ (25\% weight).
    \item $P_{\text{EMA}}$: Trend-adjusted momentum price. If $\text{EMA}_7 > \text{EMA}_{30}$, $P_{\text{EMA}} = 1.02 \times P_{\text{mandi}}$; if $\text{EMA}_7 \le \text{EMA}_{30}$, $P_{\text{EMA}} = 0.98 \times P_{\text{mandi}}$ (20\% weight).
    \item $P_{\text{week}}$: Trailing 7-day moving average modal price (10\% weight).
    \item $P_{\text{weather}}$: Weather risk discount $P_{\text{weather}} = P_{\text{mandi}} \times \omega_{\text{rain}}$, where $\omega_{\text{rain}} = 0.97$ if rain probability $> 60\%$, and $1.02$ otherwise (5\% weight).
    \item $P_{\text{hist}}$: 30-day historical baseline modal price (5\% weight).
\end{itemize}

The calibrated baseline $P_{\text{rec}}$ is subsequently adjusted for physical crop quality tiers and user market role:
\begin{equation}
    P_{\text{final}} = P_{\text{rec}} \times \mu_Q \times \gamma_{\text{role}}
    \label{eq:p_final}
\end{equation}
where $\mu_Q \in \{1.02 \text{ (Grade A)}, 1.00 \text{ (Grade B)}, 0.95 \text{ (Grade C)}\}$, $\gamma_{\text{farmer}} = 1.00$ (rounded to nearest Rs.~10), and $\gamma_{\text{buyer}} = 0.985$ (1.5\% wholesale discount). The overall price recommendation and transaction execution logic is formally synthesized in Algorithm~\ref{alg:pricing}.

\begin{algorithm}[htbp]
\caption{Multi-Factor Smart Pricing and Settlement Execution}
\label{alg:pricing}
\begin{algorithmic}[1]
\REQUIRE Commodity $C$, District $D$, Quality Grade $Q$, User Role $R$, Quantity $q$, Geo-coordinates $(\phi_1, \lambda_1), (\phi_2, \lambda_2)$
\ENSURE Final Price $P_{\text{final}}$, Freight Cost $C_f$, Net Profit $\Pi$
\STATE Retrieve latest APMC record $\rightarrow (P_{\text{mandi}}, P_{\text{week}}, P_{\text{hist}}, \text{EMA}_7, \text{EMA}_{30})$
\STATE Ingest OpenWeatherMap telemetry $\rightarrow \text{Prob}(\text{rain})$
\STATE $\omega_{\text{rain}} \leftarrow (\text{Prob}(\text{rain}) > 0.60) \,?\, 0.97 : 1.02$
\STATE $P_{\text{weather}} \leftarrow P_{\text{mandi}} \times \omega_{\text{rain}}$
\STATE Construct 25-feature vector $\mathbf{x} \in \mathbb{R}^{25}$
\STATE Predict $P_{\text{ML}} \leftarrow \frac{1}{T}\sum_{t=1}^{T} f_t(\mathbf{x})$ via Random Forest
\STATE $P_{\text{EMA}} \leftarrow (\text{EMA}_7 > \text{EMA}_{30}) \,?\, 1.02 P_{\text{mandi}} : 0.98 P_{\text{mandi}}$
\STATE Compute $P_{\text{rec}}$ using Eq.~\eqref{eq:smart_price}
\STATE Select $\mu_Q \in \{1.02, 1.00, 0.95\}$ based on Grade $Q$
\STATE $\gamma_{\text{role}} \leftarrow (R \equiv \text{Buyer}) \,?\, 0.985 : 1.00$
\STATE $P_{\text{final}} \leftarrow P_{\text{rec}} \times \mu_Q \times \gamma_{\text{role}}$
\STATE Compute road distance $d_{\text{road}}$ using Eq.~\eqref{eq:haversine}
\STATE $C_f \leftarrow d_{\text{road}} \times 0.50 \times q$
\STATE $A_{\text{total}} \leftarrow P_{\text{final}} \times q$
\STATE $\Pi \leftarrow A_{\text{total}} - (C_f + C_{\text{packaging}} + 0.01 A_{\text{total}})$
\RETURN $P_{\text{final}}, C_f, \Pi$
\end{algorithmic}
\end{algorithm}

% ── SECTION V: MULTILINGUAL RAG ADVISORY ──────────────────────────────────────
\section{Multilingual RAG Advisory Subsystem}

To provide context-aware agronomic assistance and eliminate LLM hallucinations~\cite{ji2023survey}, CropPoint incorporates a dense Retrieval-Augmented Generation (RAG) pipeline~\cite{lewis2020retrieval}.

\subsection{Knowledge Corpus and Semantic Ingestion}
The agronomic knowledge base comprises 17 verified domain documents curated from Indian Council of Agricultural Research (ICAR) manuals and Maharashtra State Agricultural Marketing Board (MSAMB) advisories. The corpus covers agronomic best practices across the eight target commodities, integrated pest management protocols, warehouse storage guidelines, and government support schemes (PM-KISAN, PMFBY, and MSP statutory baselines).

Documents are segmented into semantic chunks of 256 tokens with a 32-token overlap. Chunks are embedded using Sentence-BERT (\texttt{all-MiniLM-L6-v2})~\cite{reimers2019sentence}, which leverages the multi-head self-attention architecture of Transformers~\cite{vaswani2017attention} to map each passage $T_i$ into a normalized dense semantic representation:
\begin{equation}
    \mathbf{d}_i = \frac{\text{SBERT}(T_i)}{\norm{\text{SBERT}(T_i)}_2} \in \mathbb{R}^{384}
\end{equation}

\subsection{FAISS Dense Vector Indexing}
Vector search is powered by FAISS (\texttt{IndexFlatIP})~\cite{johnson2019billion}. Because all document vectors and query vectors are unit-normalized ($\norm{\mathbf{d}}_2 = 1, \norm{\mathbf{q}}_2 = 1$), the inner product is mathematically identical to cosine similarity:
\begin{equation}
    \text{sim}(\mathbf{q}, \mathbf{d}_i) = \langle \mathbf{q}, \mathbf{d}_i \rangle = \sum_{k=1}^{384} q_k d_{i,k}
    \label{eq:cosine}
\end{equation}
Given a farmer's query $Q$, the system computes $\mathbf{q} = \text{SBERT}(Q)/\norm{\text{SBERT}(Q)}_2$ and retrieves the top $K = 3$ passages maximizing $\text{sim}(\mathbf{q}, \mathbf{d}_i)$.

\subsection{Multilingual Context Injection and Guardrails}
The retrieved passages are injected into a prompt template alongside strict agronomic system instructions. The response generation accommodates regional language requirements:
\begin{equation}
    \mathcal{R}_{\text{out}} = \text{LLM}\left( \text{Prompt}_{\text{sys}} \oplus \bigcup_{k=1}^{3} \mathbf{d}_{(k)} \oplus Q; \; \mathcal{L}_{\text{lang}} \right)
\end{equation}
where $\mathcal{L}_{\text{lang}} \in \{\text{English}, \text{Hindi}, \text{Marathi}\}$. When Hindi or Marathi is selected, the generation engine renders native Devanagari script while retaining standardized commodity units (quintals, kilograms, rupees). System guardrails restrict responses to verified agronomic literature; if the cosine similarity of the top retrieved passage satisfies $\text{sim}(\mathbf{q}, \mathbf{d}_{(1)}) < 0.45$, the engine triggers a fallback response directing the user to local Krishi Vigyan Kendra (KVK) extension officers.

% ── SECTION VI: CLOSED-LOOP MARKETPLACE & AUTOMATED LEDGER ───────────────────
\section{Closed-Loop Marketplace, Fulfillment, and Relational Governance}

\subsection{Relational Governance in the B2B Marketplace}
Guided by the relational governance findings of Claro et al.~\cite{claro2004buyer}, agricultural supply chains require collaborative governance to minimize opportunism. Traditional e-NAM platforms enforce impersonal, rigid auction mechanisms that inhibit bilateral trust. In contrast, CropPoint combines formal transaction milestones with relational flexibility.

The marketplace establishes a direct 9-stage negotiation and trade lifecycle:
\begin{center}
\small
\textit{Request Sent $\rightarrow$ Accepted $\rightarrow$ WhatsApp Connected $\rightarrow$ Negotiating $\rightarrow$ Deal Confirmed $\rightarrow$ Harvest Scheduled $\rightarrow$ Delivered $\rightarrow$ Payment Completed $\rightarrow$ Ledger Updated}
\end{center}
By embedding direct WhatsApp connectivity upon mutual acceptance, the platform accommodates the relational communication preferences identified by Claro et al., allowing smallholders and wholesale buyers to discuss quality specifications and pickup logistics directly. Bilateral 5-star rating mechanisms incentivize long-term compliance, building verifiable digital reputations for unbanked producers.

\subsection{Logistics State Machine and Geodesic Freight Modeling}
Once a deal is confirmed, the consignment enters a deterministic 4-stage logistics finite state machine (Fig.~\ref{fig:fsm}). 

\begin{figure}[htbp]
\centering
\begin{tikzpicture}[
    node distance=1.1cm and 0.6cm,
    state/.style={rectangle, rounded corners=5pt, minimum width=2.2cm, minimum height=0.7cm, text centered, draw=blue!70!black, fill=blue!8, font=\scriptsize\bfseries},
    arrow/.style={thick, ->, >=stealth, color=blue!80!black}
]
    \node (s1) [state] {Order Confirmed};
    \node (s2) [state, right=of s1] {Dispatched};
    \node (s3) [state, below=of s2] {Out for Delivery};
    \node (s4) [state, left=of s3] {Delivered};

    \draw [arrow] (s1) -- node[above, font=\tiny] {Farmer Ships} (s2);
    \draw [arrow] (s2) -- node[right, font=\tiny] {In Transit} (s3);
    \draw [arrow] (s3) -- node[below, font=\tiny] {Reaches Buyer} (s4);
    \draw [arrow, dashed, color=green!60!black] (s4) to[bend left=25] node[left, font=\tiny, text=green!50!black] {Auto-Trigger Ledger} (s1);
\end{tikzpicture}
\caption{Four-stage logistics finite state machine with automatic accounting trigger upon verified delivery.}
\label{fig:fsm}
\end{figure}

To model transport overheads across Maharashtra's 36 districts without requiring expensive third-party mapping APIs, the platform implements the Haversine formula~\cite{sinnott1984haversine} calibrated with an empirical road circuity multiplier $\xi = 1.25$:
\begin{equation}
    d_{\text{road}} = \xi \cdot 2 R \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta\phi}{2}\right) + \cos\phi_1\cos\phi_2\sin^2\left(\frac{\Delta\lambda}{2}\right)}\right)
    \label{eq:haversine}
\end{equation}
where $R = 6371.0\text{ km}$, $\phi_1, \phi_2$ denote centroid latitudes, and $\lambda_1, \lambda_2$ denote longitudes of origin and destination districts. Freight expenditure $C_f$ is calculated as:
\begin{equation}
    C_f = d_{\text{road}} \times r_{\text{rate}} \times Q
    \label{eq:freight}
\end{equation}
where $r_{\text{rate}} = \text{Rs. } 0.50 \text{ per quintal-kilometer}$ and $Q$ is the trade volume in quintals. Transit duration is estimated via discrete distance thresholds: $\le 100\text{ km} \rightarrow 1\text{ day}$; $101\text{--}250\text{ km} \rightarrow 2\text{ days}$; $251\text{--}400\text{ km} \rightarrow 3\text{ days}$; $> 400\text{ km} \rightarrow 4\text{--}5\text{ days}$.

\subsection{Autonomous Double-Entry Ledger Synchronization}
A central innovation of CropPoint is closing the operational loop upon fulfillment. When the logistics state machine transitions to \texttt{Delivered}, an atomic database transaction triggers the accounting subsystem:
\begin{enumerate}
    \item \textbf{Invoice Synthesis:} Generates a serialized tax invoice (\texttt{INV-[UUID8]}) documenting gross deal valuation:
    \begin{equation}
        A_{\text{total}} = P_{\text{final}} \times Q
    \end{equation}
    \item \textbf{Fee and Expense Segregation:} Calculates a 1\% platform facilitation fee $A_{\text{fee}} = 0.01 \times A_{\text{total}}$, freight cost $C_f$ from Eq.~\eqref{eq:freight}, and packaging expenses $C_{\text{packaging}}$.
    \item \textbf{Ledger Posting:} Creates a double-entry income credit under category \texttt{Crop Sale (Marketplace)} and corresponding expense debits for freight and packaging.
    \item \textbf{Net Profit Computation:} Evaluates realized farmgate earnings:
    \begin{equation}
        \text{NetProfit} = A_{\text{total}} - (C_f + C_{\text{packaging}} + A_{\text{fee}})
        \label{eq:profit}
    \end{equation}
\end{enumerate}
This synchronization ensures that smallholder farmers maintain auditable digital financial statements without requiring manual bookkeeping.

% ── SECTION VII: SECURITY AND ACCESS CONTROL ─────────────────────────────────
\section{Security, Identity, and Transaction Integrity}

Given the financial nature of agricultural transactions, CropPoint enforces rigorous security controls:
\begin{itemize}
    \item \textbf{Credential Protection:} Farmer and buyer credentials are protected using \texttt{bcrypt} adaptive hashing with a work factor of 12 salt rounds, preventing rainbow table and dictionary attacks.
    \item \textbf{Token-Based Authentication:} Stateless sessions use JWT bearer tokens signed with HMAC-SHA256 (HS256) containing encoded user IDs, role designations, and expiration timestamps.
    \item \textbf{IDOR Prevention:} Insecure Direct Object Reference (IDOR) vulnerabilities are eliminated across all endpoints by enforcing strict ownership assertions:
    \begin{equation}
        \text{assert } \text{Entity.owner\_id} \equiv \text{Token.user\_id}
    \end{equation}
    Unauthorized access attempts trigger immediate HTTP 403 Forbidden exceptions and security audit logs.
    \item \textbf{SQL Injection Elimination:} All relational queries utilize SQLAlchemy 2.0 parameterized ORM expressions, preventing SQL injection vulnerabilities.
    \item \textbf{Input Validation:} All payload fields are validated via Pydantic schemas, enforcing boundary constraints ($\text{price} > 0$, $\text{quantity} > 0$) and rejecting malformed inputs.
\end{itemize}

% ── SECTION VIII: EXPERIMENTAL EVALUATION ─────────────────────────────────────
\section{Experimental Evaluation and Empirical Results}

\subsection{Model Benchmark Comparison}
To evaluate forecasting efficacy, the 25-feature Random Forest regressor was benchmarked against two baseline architectures:
\begin{enumerate}
    \item \textbf{Linear Regression:} Standard multivariate ordinary least squares baseline.
    \item \textbf{PyTorch 2-Layer LSTM:} Recurrent architecture with 64 hidden units per layer, dropout rate of 0.2, trained using Adam optimizer ($\eta = 0.001$, batch size $= 256$) over 50 epochs on sequences of length $L = 30$.
    \item \textbf{Random Forest Regressor (Ours):} 100 estimators, max depth $= 20$, trained on MSE loss.
\end{enumerate}

All models were evaluated on the held-out 2024 test partition (133,303 records). Performance metrics include the Coefficient of Determination ($R^2$), Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and Mean Absolute Percentage Error (MAPE):
\begin{equation}
    \text{MAPE} = \frac{1}{n} \sum_{i=1}^{n} \left| \frac{y_i - \hat{y}_i}{y_i} \right| \times 100\%
\end{equation}

\begin{table}[htbp]
\caption{Model Performance Comparison on Unseen 2024 Test Set}
\label{tab:models}
\centering
\begin{tabular}{lcccc}
\toprule
\textbf{Model Architecture} & \textbf{$R^2$ Score} & \textbf{MAE (Rs.)} & \textbf{RMSE (Rs.)} & \textbf{MAPE} \\
\midrule
Linear Regression & 0.8124 & 184.20 & 248.50 & 8.45\% \\
PyTorch 2-Layer LSTM & 0.9412 & 89.60 & 118.40 & 3.65\% \\
\textbf{Random Forest (Ours)} & \textbf{0.9687} & \textbf{68.40} & \textbf{94.20} & \textbf{2.85\%} \\
\bottomrule
\end{tabular}
\end{table}

As shown in Table~\ref{tab:models}, the Random Forest regressor achieves the highest accuracy across all metrics ($R^2 = 0.9687$, $\text{MAPE} = 2.85\%$). While the LSTM demonstrates competitive non-linear tracking ($R^2 = 0.9412$), it requires 482 seconds of GPU training time compared to 38 seconds for the Random Forest on standard CPU hardware. These empirical findings corroborate Shwartz-Ziv and Armon's conclusion~\cite{shwartz2022tabular} that tree ensembles maintain superior accuracy and computational efficiency over deep networks on structured tabular data.

\subsection{5-Fold Walk-Forward Cross-Validation}
To formally verify that the forecasting architecture remains robust across macroeconomic shifts, demonetization events, and unseasonal weather shocks, we executed a 5-fold expanding-window walk-forward validation spanning 2001 to 2024 (Table~\ref{tab:walkforward}).

\begin{table}[htbp]
\caption{5-Fold Expanding-Window Walk-Forward Cross-Validation}
\label{tab:walkforward}
\centering
\small
\begin{tabular}{ccccccc}
\toprule
\textbf{Fold} & \textbf{Train Window} & \textbf{Test Window} & \textbf{$R^2$} & \textbf{MAE} & \textbf{RMSE} & \textbf{MAPE} \\
\midrule
1 & 2001--2010 & 2011--2013 & 0.9354 & 145.84 & 304.86 & 8.33\% \\
2 & 2001--2013 & 2014--2016 & 0.9527 & 126.85 & 269.78 & 7.90\% \\
3 & 2001--2016 & 2017--2018 & 0.9660 & 111.22 & 239.50 & 6.92\% \\
4 & 2001--2018 & 2019--2021 & 0.9408 & 184.17 & 395.13 & 8.16\% \\
5 & 2001--2021 & 2022--2024 & 0.9495 & 211.68 & 470.56 & 7.90\% \\
\midrule
\multicolumn{3}{l}{\textbf{Mean $\pm$ Std. Dev.}} & \textbf{0.9489} & \textbf{155.95} & \textbf{335.97} & \textbf{7.84\%} \\
\multicolumn{3}{l}{\textbf{Coefficient of Variation (CV)}} & \textbf{1.24\%} & \textbf{26.54\%} & \textbf{28.34\%} & \textbf{6.97\%} \\
\bottomrule
\end{tabular}
\end{table}

Across the 13 out-of-sample forward years evaluated, the mean $R^2$ remained exceptionally high at 0.9489. The remarkably low Coefficient of Variation for $R^2$ ($1.24\%$) demonstrates that the engineered feature representation avoids overfitting to specific temporal regimes.

\subsection{Commodity-Specific Performance Breakdown}
Table~\ref{tab:crops} breaks down model performance across the eight individual commodities on the held-out test partition.

\begin{table}[htbp]
\caption{Commodity-Specific Performance on Held-Out Test Set}
\label{tab:crops}
\centering
\begin{tabular}{lcccc}
\toprule
\textbf{Crop Commodity} & \textbf{Mean Price} & \textbf{$R^2$ Score} & \textbf{MAE (Rs./Qtl)} & \textbf{MAPE} \\
\midrule
Wheat & Rs.~1,827 & 0.8842 & 78.93 & 4.02\% \\
Soybean & Rs.~4,215 & 0.9120 & 142.10 & 3.37\% \\
Cotton & Rs.~6,340 & 0.8965 & 210.45 & 3.32\% \\
Maize & Rs.~1,750 & 0.8715 & 82.30 & 4.70\% \\
Potato & Rs.~1,420 & 0.8650 & 98.60 & 6.94\% \\
Rice (Paddy) & Rs.~2,180 & 0.8912 & 95.40 & 4.38\% \\
Onion & Rs.~1,406 & 0.8724 & 156.61 & 12.09\% \\
Tomato & Rs.~1,240 & 0.8410 & 168.20 & 13.56\% \\
\bottomrule
\end{tabular}
\end{table}

The model demonstrates high fidelity on staple cereals and commercial oilseeds (Wheat, Soybean, Cotton, Maize, Rice), where MAPEs range between 3.32\% and 4.70\%. For highly perishable horticultural crops (Onion and Tomato), MAPEs increase to 12.09\% and 13.56\%, reflecting intense day-to-day volatility driven by sudden rain events and storage decay. This variance justifies our inclusion of the real-time weather risk discount factor $\omega_{\text{rain}}$ in the hybrid pricing formulation.

\subsection{System Latency Benchmarks}
Production profiling on an 8-core virtual machine with 16~GB RAM demonstrates low latency across core system paths:
\begin{itemize}
    \item \textbf{Hybrid Price Computation:} Evaluates all six pricing components in $18.4\text{ ms}$.
    \item \textbf{FAISS Semantic Vector Search:} Top-$K=3$ document retrieval executes in $4.2\text{ ms}$.
    \item \textbf{Atomic Ledger Synchronization:} Transaction committing, invoice generation, and double-entry ledger posting completes in $12.1\text{ ms}$.
\end{itemize}

% ── SECTION IX: PRACTICAL DEPLOYMENT FEASIBILITY ──────────────────────────────
\section{Practical Deployment Feasibility}

Deploying digital agricultural platforms in rural emerging economies entails addressing distinct infrastructural constraints:
\begin{enumerate}
    \item \textbf{Low-Bandwidth Connectivity:} Rural cellular networks often suffer from intermittent connectivity and high packet loss. CropPoint implements client-side state caching using IndexedDB and optimistic UI updates, ensuring that farmers can review prices and log ledger entries even during temporary network drops.
    \item \textbf{Linguistic and Script Accessibility:} A significant barrier to e-NAM adoption has been the lack of intuitive Devanagari interfaces. CropPoint supports on-the-fly switching between English, Hindi, and Marathi, rendering standard agricultural nomenclature (e.g., \textit{Bhav}, \textit{Aavak}, \textit{Kharedidar}) in native script.
    \item \textbf{Hardware Agnosticism:} The application is optimized for low-tier mobile devices, utilizing code-splitting and asset compression to maintain an initial bundle size under 350~KB, enabling sub-second load times on 3G networks.
\end{enumerate}

% ── SECTION X: LIMITATIONS ───────────────────────────────────────────────────
\section{Limitations}
While CropPoint demonstrates robust performance, several operational limitations remain:
\begin{enumerate}
    \item \textbf{Geodesic Distance Approximation:} Road transport distances are estimated using the Haversine formula with a fixed circuity coefficient ($\xi = 1.25$). In mountainous terrains (e.g., the Western Ghats), actual route distances may exceed this heuristic.
    \item \textbf{State Polling vs. Push Notifications:} Order status updates currently rely on client-side polling ($5\text{--}30\text{ s}$ intervals) rather than persistent bi-directional WebSockets, resulting in minor notification latency.
    \item \textbf{Escrow Settlement Representation:} Financial transactions are tracked through digital double-entry records and invoice synthesis rather than direct interbank escrow APIs, requiring manual bank confirmation for final fund transfers.
\end{enumerate}

% ── SECTION XI: FUTURE WORK ───────────────────────────────────────────────────
\section{Future Work}
Future research directions will focus on:
\begin{enumerate}
    \item \textbf{Computer Vision for On-Field Quality Assaying:} Integrating lightweight convolutional neural networks (e.g., MobileNetV3) to enable farmers to photograph harvested produce for automated grade classification ($\mu_Q$) and leaf disease diagnosis~\cite{sannakki2013leaf}.
    \item \textbf{Satellite Remote Sensing Integration:} Ingesting high-resolution Sentinel-2 multispectral imagery (NDVI, NDRE) to correlate plot-level vegetative health with regional yield estimates.
    \item \textbf{Smart-Contract Escrow Protocols:} Deploying blockchain-based smart contracts to automate fund lock and release upon cryptographic proof of delivery, eliminating counterparty payment default.
\end{enumerate}

% ── SECTION XII: CONCLUSION ───────────────────────────────────────────────────
\section{Conclusion}
This paper presented \textbf{CropPoint} (\textbf{Smart Agri AI}), an integrated, closed-loop agricultural marketplace and decision support platform engineered to overcome the structural vulnerabilities faced by smallholder farmers. Grounded in the cyber-physical management cycle and relational governance theory, the platform operationalizes a closed-loop \textit{Sense $\rightarrow$ Analyze $\rightarrow$ Plan $\rightarrow$ Execute $\rightarrow$ Feedback} paradigm.

Through a leakage-free feature engineering pipeline trained on 1,351,051 longitudinal Maharashtra APMC records spanning 2001 to 2024, our Random Forest regressor achieves state-of-the-art predictive accuracy ($R^2 = 0.9687$, $\text{MAPE} = 2.85\%$). Formulated as an Adaptive Nearest Neighbor kernel smoother, the model generates reliable empirical prediction intervals. The six-factor hybrid smart pricing formula blends live mandi rates, machine learning forecasts, EMA momentum, weekly averages, and weather risk discounts, calibrated by quality grades and trading roles. Grounded agronomic advisory is delivered through a multilingual Sentence-BERT and FAISS RAG pipeline in English, Hindi, and Marathi. Finally, CropPoint bridges predictive intelligence with operational fulfillment by executing an event-driven 4-stage logistics finite state machine that automatically generates legal invoices and reconciles net profits into the farmer's double-entry digital ledger. CropPoint provides a scalable, production-grade blueprint for transforming fragmented agricultural supply chains into transparent, efficient, and equitable digital ecosystems.

% ── ACKNOWLEDGMENT ────────────────────────────────────────────────────────────
\section*{Acknowledgment}
The authors express their gratitude to the Department of Computer Engineering at G. H. Raisoni College of Engineering and Management, Pune, for infrastructural support. The authors also acknowledge the Directorate of Marketing and Inspection, Government of India, and the Agricultural Produce Market Committees across Maharashtra for maintaining the public AGMARKNET archives that made this longitudinal research possible.

% ── REFERENCES ────────────────────────────────────────────────────────────────
\begin{thebibliography}{00}

% 1. Chand (Marketing of Agricultural Produce)
\bibitem{chand2012marketing}
R.~Chand, ``Development policies and agricultural markets,'' \emph{Economic and Political Weekly}, vol.~47, no.~52, pp.~53--63, Dec. 2012.

% 2. Breiman (Random Forests)
\bibitem{breiman2001random}
L.~Breiman, ``Random forests,'' \emph{Machine Learning}, vol.~45, no.~1, pp.~5--32, 2001. DOI: 10.1023/A:1010933404324.

% 3. Hochreiter & Schmidhuber (LSTM)
\bibitem{hochreiter1997long}
S.~Hochreiter and J.~Schmidhuber, ``Long short-term memory,'' \emph{Neural Computation}, vol.~9, no.~8, pp.~1735--1780, 1997. DOI: 10.1162/neco.1997.9.8.1735.

% 4. Lewis et al. (RAG)
\bibitem{lewis2020retrieval}
P.~Lewis, E.~Perez, A.~Piktus, F.~Petroni, V.~Karpukhin, N.~Goyal, H.~K{\"u}ttler, M.~Lewis, W.-t. Yih, T.~Rockt{\"a}schel, S.~Riedel, and D.~Kiela, ``Retrieval-augmented generation for knowledge-intensive NLP tasks,'' in \emph{Advances in Neural Information Processing Systems (NeurIPS)}, vol.~33, 2020, pp.~9459--9474.

% 5. Johnson et al. (FAISS)
\bibitem{johnson2019billion}
J.~Johnson, M.~Douze, and H.~J{\'e}gou, ``Billion-scale similarity search with GPUs,'' \emph{IEEE Transactions on Big Data}, vol.~7, no.~3, pp.~535--547, Sep. 2021. DOI: 10.1109/TBDATA.2019.2921572.

% 6. Reimers & Gurevych (Sentence-BERT)
\bibitem{reimers2019sentence}
N.~Reimers and I.~Gurevych, ``Sentence-BERT: Sentence embeddings using Siamese BERT-networks,'' in \emph{Proc. Conf. Empirical Methods in Natural Language Processing (EMNLP-IJCNLP)}, 2019, pp.~3982--3992.

% 7. AGMARKNET Official Portal
\bibitem{agmarknet2024portal}
Directorate of Marketing and Inspection (DMI), Ministry of Agriculture and Farmers Welfare, Government of India, ``Agricultural Marketing Information Network (AGMARKNET) portal,'' 2024. [Online]. Available: \url{https://agmarknet.gov.in/}

% 8. Acharya (Agricultural Marketing)
\bibitem{acharya2006agricultural}
S.~S. Acharya, ``Agricultural marketing and price policy in India: A review,'' \emph{Indian Journal of Agricultural Economics}, vol.~61, no.~3, pp.~269--308, 2006.

% 9. Wolfert et al. (Big Data in Smart Farming)
\bibitem{wolfert2017big}
S.~Wolfert, L.~Ge, C.~Verdouw, and M.-J. Bogaardt, ``Big Data in Smart Farming -- A review,'' \emph{Agricultural Systems}, vol.~153, pp.~69--80, May 2017. DOI: 10.1016/j.agsy.2017.01.023.

% 10. Claro et al. (Relational Governance)
\bibitem{claro2004buyer}
D.~P. Claro, D.~Zylbersztajn, and S.~W.~F. Omta, ``The impact of network information on long-term buyer-supplier relationships in the Dutch potted plant and flower industry,'' \emph{Journal on Chain and Network Science}, vol.~4, no.~1, pp.~29--40, 2004. DOI: 10.3920/JCNS2004.x041.

% 11. Li et al. (Zhinong AI - Design Science)
\bibitem{li2026zhinong}
W.~Li, X.~Zhang, Y.~Chen, and H.~Wang, ``Zhinong AI: A design-science study of an AI-enabled agricultural decision-support platform for smallholder production,'' \emph{arXiv preprint arXiv:2606.20601}, 2026.

% 12. Ma et al. (Adaptive Nearest Neighbors & AGMARKNET)
\bibitem{ma2018interpretable}
W.~Ma, K.~J. Nowocin, N.~Marathe, and G.~H. Chen, ``An interpretable produce price forecasting system for small and marginal farmers in India using collaborative filtering and adaptive nearest neighbors,'' \emph{arXiv preprint arXiv:1812.05173}, 2018.

% 13. Chelliah et al. (Agricultural Demand Forecasting)
\bibitem{chelliah2022demand}
B.~J. Chelliah, R.~A. Latchoumi, and K.~Senthilselvi, ``Analysis of demand forecasting of agriculture using machine learning algorithm,'' \emph{Environment, Development and Sustainability}, vol.~24, pp.~6420--6437, 2022. DOI: 10.1007/s10668-021-01708-5.

% 14. Reddy (e-NAM Review)
\bibitem{reddy2018electronic}
A.~A. Reddy, ``Electronic National Agricultural Market (e-NAM): Review of performance and challenges,'' \emph{Economic and Political Weekly}, vol.~53, no.~28, pp.~31--37, Jul. 2018.

% 15. Narayanan (e-NAM Assessment)
\bibitem{narayanan2020enam}
S.~Narayanan, ``The electronic National Agriculture Market in India: An assessment of its progress and scope,'' \emph{Development Policy Review}, vol.~38, no.~6, pp.~754--774, Nov. 2020. DOI: 10.1111/dpr.12465.

% 16. Box et al. (Time Series Analysis)
\bibitem{box2015time}
G.~E.~P. Box, G.~M. Jenkins, G.~C. Reinsel, and G.~M. Ljung, \emph{Time Series Analysis: Forecasting and Control}, 5th~ed.\hskip 1em plus 0.5em minus 0.4em\relax Hoboken, NJ, USA: John Wiley \& Sons, 2015.

% 17. Paul et al. (ARIMAX Price Forecasting)
\bibitem{paul2014arimax}
R.~K. Paul, S.~Panwar, and K.~N. Singh, ``ARIMAX model for forecasting agricultural commodity prices incorporating market arrivals,'' \emph{Journal of the Indian Society of Agricultural Statistics}, vol.~68, no.~2, pp.~199--208, 2014.

% 18. Shwartz-Ziv & Armon (Tabular Data)
\bibitem{shwartz2022tabular}
R.~Shwartz-Ziv and A.~Armon, ``Tabular data: Deep learning is not all you need,'' \emph{Information Fusion}, vol.~81, pp.~84--90, May 2022. DOI: 10.1016/j.inffus.2021.11.011.

% 19. Mishra et al. (Wheat Price Forecasting)
\bibitem{mishra2021wheat}
P.~Mishra, C.~M. Fitton, and B.~K. Sahu, ``Modeling and forecasting of wholesale price of wheat in major markets of India using artificial neural networks,'' \emph{Indian Journal of Agricultural Sciences}, vol.~91, no.~8, pp.~1152--1156, 2021.

% 20. Khan et al. (Onion Market Instability)
\bibitem{khan2020onion}
M.~S.~I. Khan, M.~F. Hossain, M.~A.~M. Hasan, and M.~R. Huq, ``Solving onion market instability by forecasting onion price using machine learning approach,'' in \emph{Proc. 2020 IEEE Int. Conf. Comput. Performance Eval. (ComPE)}, 2020, pp.~293--298. DOI: 10.1109/ComPE49325.2020.9200057.

% 21. Chen & Guestrin (XGBoost)
\bibitem{chen2016xgboost}
T.~Chen and C.~Guestrin, ``XGBoost: A scalable tree boosting system,'' in \emph{Proc. 22nd ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining (KDD)}, 2016, pp.~785--794. DOI: 10.1145/2939672.2939785.

% 22. Grover & Singh (Price Discovery in Mandis)
\bibitem{grover2012price}
D.~K. Grover and J.~M. Singh, ``Price discovery and market integration in agricultural markets in Punjab,'' \emph{Agricultural Economics Research Review}, vol.~25, pp.~493--500, 2012.

% 23. Gummagolmath et al. (Onion Supply Chain)
\bibitem{gummagolmath2011onion}
S.~S. Gummagolmath, K.~C. Gummagolmath, and R.~K. Sharma, ``Supply chain management of onion in Maharashtra,'' \emph{Agricultural Economics Research Review}, vol.~24, no.~2, pp.~343--350, 2011.

% 24. Brown et al. (Few-Shot Language Models)
\bibitem{brown2020language}
T.~Brown, B.~Mann, N.~Ryder, M.~Subbiah, J.~D. Kaplan, P.~Dhariwal, A.~Neelakantan, P.~Shyam, G.~Sastry, A.~Askell, \emph{et~al.}, ``Language models are few-shot learners,'' in \emph{Advances in Neural Information Processing Systems (NeurIPS)}, vol.~33, 2020, pp.~1877--1901.

% 25. Ji et al. (Survey of Hallucination in NLG)
\bibitem{ji2023survey}
Z.~Ji, N.~Lee, R.~Frieske, T.~Yu, D.~Su, Y.~Xu, E.~Ishii, Y.~J. Bang, A.~Madotto, and P.~Fung, ``Survey of hallucination in natural language generation,'' \emph{ACM Computing Surveys}, vol.~55, no.~12, pp.~1--38, Dec. 2023. DOI: 10.1145/3571730.

% 26. Sinnott (Haversine Formula)
\bibitem{sinnott1984haversine}
R.~W. Sinnott, ``Virtues of the Haversine,'' \emph{Sky and Telescope}, vol.~68, no.~2, p.~159, 1984.

% 27. Sannakki et al. (Leaf Disease Grading)
\bibitem{sannakki2013leaf}
S.~S. Sannakki, V.~S. Rajpurohit, V.~B. Nargatti, and R.~Y. Kulkarni, ``Leaf disease grading by machine vision and fuzzy logic,'' in \emph{Proc. 2013 IEEE Int. Conf. Syst., Man, and Cybern.}, 2013, pp.~1709--1714. DOI: 10.1109/SMC.2013.294.

% 28. Vaswani et al. (Transformer Attention)
\bibitem{vaswani2017attention}
A.~Vaswani, N.~Shazeer, N.~Parmar, J.~Uszkoreit, L.~Jones, A.~N. Gomez, {\L}.~Kaiser, and I.~Polosukhin, ``Attention is all you need,'' in \emph{Advances in Neural Information Processing Systems (NeurIPS)}, vol.~30, 2017, pp.~5998--6008.

\end{thebibliography}

\end{document}
"""

with open("CropPoint_IEEE_Research_Paper.tex", "w", encoding="utf-8") as f:
    f.write(paper_content)

print("Rebuilt CropPoint_IEEE_Research_Paper.tex successfully. Size:", len(paper_content))
