#!/usr/bin/env python3
"""
Generates an interactive, publication-grade HTML Slide Deck Presentation
for CropPoint / Smart Agri AI Review 3 Defense.
Features:
- Responsive 16:9 Slide Layout
- Keyboard arrow navigation (Left/Right/Space)
- Fullscreen mode ('F' key)
- Presenter Notes drawer ('N' key)
- Quick Jump Slide Menu ('M' key)
- High-res embedded figures and interactive tables
"""

import os
import json

BASE_DIR = "/Users/owaisrazaansaralibhati/Desktop/Smart Agri AI"
OUTPUT_HTML = os.path.join(BASE_DIR, "CropPoint_Review3_Presentation.html")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CropPoint: Smart Agri AI — Review 3 Final Technical Defense</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;600&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Inter', sans-serif; background-color: #0b132b; color: #1c2541; overflow: hidden; margin: 0; }
  .code-font { font-family: 'Fira Code', monospace; }
  .slide { display: none; width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; }
  .slide.active { display: flex; flex-direction: column; }
  .gradient-hero { background: radial-gradient(circle at 80% 20%, #1c2541 0%, #0b132b 100%); }
  .card-shadow { box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.05); }
  .badge-emerald { background: #E8F5E9; color: #2E7D32; border: 1px solid #A5D6A7; }
  .badge-blue { background: #E3F2FD; color: #1565C0; border: 1px solid #90CAF9; }
</style>
</head>
<body class="select-none">

<!-- TOP CONTROLS & PROGRESS BAR -->
<div class="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-2 bg-slate-900/90 backdrop-blur border-b border-slate-800 text-xs text-slate-300">
  <div class="flex items-center space-x-3">
    <span class="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></span>
    <span class="font-bold text-white tracking-wider">CROPPOINT: SMART AGRI AI</span>
    <span class="text-slate-500">|</span>
    <span class="text-emerald-400 font-semibold">REVIEW 3: 100% IMPLEMENTATION DEFENSE</span>
  </div>
  
  <div class="flex items-center space-x-4">
    <button onclick="toggleMenu()" class="hover:text-emerald-400 transition flex items-center space-x-1 bg-slate-800 px-2 py-1 rounded">
      <span>Index (M)</span>
    </button>
    <button onclick="toggleNotes()" class="hover:text-emerald-400 transition flex items-center space-x-1 bg-slate-800 px-2 py-1 rounded">
      <span>Speaker Notes (N)</span>
    </button>
    <button onclick="toggleFullscreen()" class="hover:text-emerald-400 transition flex items-center space-x-1 bg-slate-800 px-2 py-1 rounded">
      <span>Fullscreen (F)</span>
    </button>
    <div class="font-mono bg-slate-800 px-3 py-1 rounded text-emerald-400 font-bold">
      <span id="currentSlideNum">1</span> / <span id="totalSlideNum">21</span>
    </div>
  </div>
</div>

<!-- SLIDE CONTAINER -->
<div id="deck" class="w-full h-full relative">

  <!-- SLIDE 1: TITLE SLIDE -->
  <div class="slide active gradient-hero text-white justify-center items-center px-16 pt-12" data-notes="Good morning respected evaluators and guide Mr. Pradeep Taware. Today we present the Review 3 final defense of CropPoint, proving 100% closed-loop implementation.">
    <div class="max-w-6xl w-full">
      <div class="inline-block px-4 py-1.5 rounded-full bg-emerald-600/30 border border-emerald-500 text-emerald-400 text-sm font-bold tracking-widest uppercase mb-4">
        Academic Year 2025–2026 • Final Technical Defense
      </div>
      <h1 class="text-5xl font-extrabold tracking-tight mb-3 text-white leading-tight">
        CropPoint: Smart Agri AI
      </h1>
      <p class="text-xl text-slate-300 font-light mb-8 max-w-4xl leading-relaxed">
        A Closed-Loop Agricultural Marketplace & Decision Support System Integrating Multi-Factor Random Forest Price Forecasting, Multilingual FAISS RAG, and Automated Ledger Synchronization.
      </p>

      <div class="grid grid-cols-2 gap-6 mb-8">
        <div class="bg-slate-800/80 border border-slate-700/80 rounded-xl p-5 backdrop-blur">
          <div class="text-xs uppercase tracking-wider text-emerald-400 font-bold mb-3">Student Project Team</div>
          <div class="space-y-1.5 text-sm text-slate-200">
            <div><strong class="text-white">Owesraza Bhati</strong> (ansarbhati92@gmail.com)</div>
            <div><strong class="text-white">Nikhil Jaiswar</strong> (nikhiljaiswar642@gmail.com)</div>
            <div><strong class="text-white">Mustakim Mansuri</strong> (mjmansuri786313@gmail.com)</div>
          </div>
        </div>

        <div class="bg-slate-800/80 border border-slate-700/80 rounded-xl p-5 backdrop-blur">
          <div class="text-xs uppercase tracking-wider text-blue-400 font-bold mb-3">Project Guide & Institution</div>
          <div class="text-sm text-slate-200 space-y-1">
            <div><strong>Guide:</strong> Mr. Pradeep Taware (Assistant Professor)</div>
            <div>Department of Computer Engineering</div>
            <div class="text-slate-300">G H Raisoni College of Engineering and Management, Pune</div>
          </div>
        </div>
      </div>

      <div class="flex items-center justify-between border-t border-slate-800 pt-4 text-xs text-slate-400 font-mono">
        <div>1,351,051 APMC Records</div>
        <div>•</div>
        <div>Random Forest R²: 0.9687</div>
        <div>•</div>
        <div>MAPE: 2.85% (97.15% Acc)</div>
        <div>•</div>
        <div>FAISS Trilingual RAG</div>
        <div>•</div>
        <div class="text-emerald-400 font-bold">68 Live Tests (98.5% Pass)</div>
      </div>
    </div>
  </div>

  <!-- SLIDE 2: PROBLEM STATEMENT -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Explain why current agri systems fail: spatial monopsony power extracts 30-40% of value, lack of price transparency, and zero integration between dealmaking and accounting.">
    <div class="mb-4">
      <span class="text-xs font-bold text-red-600 uppercase tracking-widest">Context & Motivation</span>
      <h2 class="text-3xl font-extrabold text-slate-900">The Problem in Smallholder Agriculture vs. The CropPoint Solution</h2>
    </div>

    <div class="grid grid-cols-2 gap-8 flex-1">
      <div class="bg-white border border-red-200 rounded-xl p-6 card-shadow flex flex-col justify-between">
        <div>
          <div class="flex items-center space-x-2 text-red-600 font-bold mb-4 pb-2 border-b border-red-100">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>
            <span>The Traditional Middlemen Supply Chain</span>
          </div>
          <ul class="space-y-3 text-sm text-slate-700">
            <li><strong class="text-red-700">• Intermediary Monopsony:</strong> Commission agents and aggregators extract 30–45% of produce value before the farmer is paid.</li>
            <li><strong class="text-red-700">• Price Information Asymmetry:</strong> Farmers rely on outdated word-of-mouth quotes and cannot verify prevailing APMC mandi spot prices.</li>
            <li><strong class="text-red-700">• Perishable Distress Selling:</strong> Without transparent distance and freight cost estimates, farmers sell to local buyers at discount.</li>
            <li><strong class="text-red-700">• Manual Accounting Friction:</strong> Zero bookkeeping prevents smallholder farmers from securing institutional crop loans.</li>
          </ul>
        </div>
        <div class="bg-red-50 p-3 rounded-lg text-xs text-red-800 font-medium">Result: Smallholder farmers remain trapped in low margin cycles despite high market demand.</div>
      </div>

      <div class="bg-emerald-50/60 border border-emerald-300 rounded-xl p-6 card-shadow flex flex-col justify-between">
        <div>
          <div class="flex items-center space-x-2 text-emerald-800 font-bold mb-4 pb-2 border-b border-emerald-200">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
            <span>The CropPoint Closed-Loop Platform</span>
          </div>
          <ul class="space-y-3 text-sm text-slate-800">
            <li><strong class="text-emerald-800">✓ 100% Disintermediation:</strong> Connects farmers directly to wholesale and institutional buyers with structured offers.</li>
            <li><strong class="text-emerald-800">✓ 6-Factor Smart Pricing:</strong> Blends Random Forest prediction (96.87% R²) with live mandi spot rates and EMA momentum.</li>
            <li><strong class="text-emerald-800">✓ Haversine Freight Engine:</strong> Real-time distance and transparent freight cost calculation per quintal.</li>
            <li><strong class="text-emerald-800">✓ Automated Ledger Sync:</strong> Delivery triggers automatic income, transport expense, and net profit ledger entries + PDF invoices.</li>
          </ul>
        </div>
        <div class="bg-emerald-100/80 p-3 rounded-lg text-xs text-emerald-900 font-medium">Result: Full commercial transparency and autonomous digital bookkeeping with zero manual entry.</div>
      </div>
    </div>
  </div>

  <!-- SLIDE 3: REVIEW 2 VS REVIEW 3 DELIVERY MATRIX -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Highlight that every single item promised in Review 2 is now 100% finished, tested, and verified on live data.">
    <div class="mb-4">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Accountability & Progress</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Review 2 Commitments vs. Review 3 100% Delivery</h2>
    </div>

    <div class="overflow-hidden border border-slate-200 rounded-xl card-shadow bg-white">
      <table class="w-full text-left text-xs border-collapse">
        <thead>
          <tr class="bg-slate-900 text-white font-semibold">
            <th class="p-3 w-1/4">Functional Component</th>
            <th class="p-3 w-1/3">Review 2 Promise / Scope</th>
            <th class="p-3 w-1/3">Review 3 Implemented Reality</th>
            <th class="p-3 text-center">Status</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 text-slate-700">
          <tr class="hover:bg-slate-50">
            <td class="p-3 font-bold text-slate-900">ML Price Forecasting</td>
            <td class="p-3">Basic model trained on sample data</td>
            <td class="p-3">Trained on 1,351,051 records across 8 commodities (R²=0.9687, MAPE=2.85%)</td>
            <td class="p-3 text-center"><span class="badge-emerald px-2 py-0.5 rounded font-bold">100% DONE</span></td>
          </tr>
          <tr class="hover:bg-slate-50">
            <td class="p-3 font-bold text-slate-900">AI Price Recommendation</td>
            <td class="p-3">Single model prediction output</td>
            <td class="p-3">6-Factor Hybrid Formula (Mandi + ML + EMA + Week Avg + Weather + Hist)</td>
            <td class="p-3 text-center"><span class="badge-emerald px-2 py-0.5 rounded font-bold">100% DONE</span></td>
          </tr>
          <tr class="hover:bg-slate-50">
            <td class="p-3 font-bold text-slate-900">Multilingual Advisory</td>
            <td class="p-3">Mock chatbot interface</td>
            <td class="p-3">RAG pipeline with Sentence-BERT, FAISS IndexFlatIP & Gemini (EN, HI, MR)</td>
            <td class="p-3 text-center"><span class="badge-emerald px-2 py-0.5 rounded font-bold">100% DONE</span></td>
          </tr>
          <tr class="hover:bg-slate-50">
            <td class="p-3 font-bold text-slate-900">B2B Marketplace Feed</td>
            <td class="p-3">Static listings screen</td>
            <td class="p-3">Active listings, buyer purchase requests, interactive negotiation & counter-bids</td>
            <td class="p-3 text-center"><span class="badge-emerald px-2 py-0.5 rounded font-bold">100% DONE</span></td>
          </tr>
          <tr class="hover:bg-slate-50">
            <td class="p-3 font-bold text-slate-900">Order Fulfillment FSM</td>
            <td class="p-3">Basic deal table status</td>
            <td class="p-3">4-Stage State Machine (Confirmed -> Dispatched -> In Transit -> Delivered)</td>
            <td class="p-3 text-center"><span class="badge-emerald px-2 py-0.5 rounded font-bold">100% DONE</span></td>
          </tr>
          <tr class="hover:bg-slate-50">
            <td class="p-3 font-bold text-slate-900">Automated Ledger Sync</td>
            <td class="p-3">Manual ledger addition only</td>
            <td class="p-3">Automated ledger entry, net profit calculation, and downloadable tax invoice PDF</td>
            <td class="p-3 text-center"><span class="badge-emerald px-2 py-0.5 rounded font-bold">100% DONE</span></td>
          </tr>
          <tr class="hover:bg-slate-50">
            <td class="p-3 font-bold text-slate-900">Live Weather Integration</td>
            <td class="p-3">Static weather forecast</td>
            <td class="p-3">Real-time OpenWeatherMap API integrated into pricing engine & advisory</td>
            <td class="p-3 text-center"><span class="badge-emerald px-2 py-0.5 rounded font-bold">100% DONE</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- SLIDE 4: SYSTEM ARCHITECTURE (FIGURE 6) -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Explain the 5 stages of CropPoint from sensing to automated ledger. Emphasize that physical delivery automatically closes the loop into the farmer's accounting balance sheet.">
    <div class="mb-3">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">End-to-End Workflow</span>
      <h2 class="text-3xl font-extrabold text-slate-900">System Architecture: The 5-Stage Closed-Loop Workflow</h2>
    </div>

    <div class="flex-1 bg-white border border-slate-200 rounded-xl p-3 card-shadow flex items-center justify-center">
      <img src="figures/fig6_closed_loop_workflow.png" class="max-h-[460px] object-contain rounded" alt="Closed Loop Workflow">
    </div>
    <div class="mt-2 text-center text-xs text-slate-500 font-mono">
      Figure 6: Seamless transition from pre-harvest field profiling to AI price recommendations, order fulfillment, and automated bookkeeping.
    </div>
  </div>

  <!-- SLIDE 5: DATASET & FEATURE IMPORTANCE (FIGURE 4) -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Explain the 1.35 million records dataset, 25 engineered features, and walk-forward chronological train/val/test split that guarantees zero lookahead leakage.">
    <div class="mb-3">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Machine Learning Pipeline</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Dataset Engineering: 1,351,051 Records & 25 Engineered Features</h2>
    </div>

    <div class="grid grid-cols-12 gap-6 flex-1 items-center">
      <div class="col-span-5 space-y-3 text-xs text-slate-700">
        <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow space-y-2">
          <div class="font-bold text-sm text-slate-900 text-emerald-700">Dataset Specifications</div>
          <div>• <strong>Source:</strong> Government of India AGMARKNET National Portal.</div>
          <div>• <strong>Volume:</strong> 1,351,051 daily longitudinal records across Maharashtra (2001–2024).</div>
          <div>• <strong>Commodities (8):</strong> Onion, Wheat, Tomato, Cotton, Soyabean, Potato, Rice, Maize.</div>
          <div>• <strong>Mandis Covered:</strong> 358 APMCs across 36 districts.</div>
        </div>

        <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow space-y-2">
          <div class="font-bold text-sm text-slate-900 text-blue-700">Strict Chronological Train / Val / Test Split</div>
          <div>• <strong>Train (2001–2021):</strong> 1,028,150 records (76.1%)</div>
          <div>• <strong>Validation (2022–2023):</strong> 190,442 records (14.1%)</div>
          <div>• <strong>Held-Out Test (2024):</strong> 132,459 records (9.8%)</div>
          <div class="text-[11px] text-emerald-700 font-semibold">Zero temporal data leakage or lookahead bias.</div>
        </div>
      </div>

      <div class="col-span-7 bg-white p-3 rounded-xl border border-slate-200 card-shadow flex items-center justify-center">
        <img src="figures/fig4_feature_importance.png" class="max-h-[460px] object-contain rounded" alt="Feature Importance">
      </div>
    </div>
  </div>

  <!-- SLIDE 6: MODEL BENCHMARKS (FIGURE 1) -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Show that Random Forest beats LSTM and Linear Regression across all 4 metrics: R2=0.9687, MAE=68.40, RMSE=94.20, and MAPE=2.85%. Explain that trees dominate on tabular data.">
    <div class="mb-3">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Model Evaluation</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Model Performance Benchmarks: Random Forest Superiority</h2>
    </div>

    <div class="flex-1 bg-white border border-slate-200 rounded-xl p-3 card-shadow flex items-center justify-center">
      <img src="figures/fig1_model_benchmarks.png" class="max-h-[380px] object-contain rounded" alt="Model Benchmarks">
    </div>

    <div class="grid grid-cols-3 gap-4 mt-3 text-xs">
      <div class="bg-emerald-50 border border-emerald-300 p-3 rounded-lg text-emerald-900">
        <strong>Random Forest (CropPoint - Ours):</strong> <strong>R² = 0.9687</strong> | <strong>MAPE = 2.85%</strong> (97.15% Accuracy) | <strong>MAE = ₹68.40/Qtl</strong>. Lowest error across all benchmarks.
      </div>
      <div class="bg-blue-50 border border-blue-200 p-3 rounded-lg text-blue-900">
        <strong>PyTorch LSTM (Deep Learning):</strong> R² = 0.9412 | MAPE = 3.65% | MAE = ₹89.60/Qtl. Good sequential representation, but slower training (482s vs 38s).
      </div>
      <div class="bg-red-50 border border-red-200 p-3 rounded-lg text-red-900">
        <strong>Linear Regression (Baseline):</strong> R² = 0.8124 | MAPE = 8.45% | MAE = ₹184.20/Qtl. Inadequate due to inability to capture non-linear seasonal interactions.
      </div>
    </div>
  </div>

  <!-- SLIDE 7: 24-YEAR WALK-FORWARD STABILITY (FIGURE 5) -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Demonstrate the 5-fold expanding window cross validation. Mean R2 is 0.9489 across 24 years, with a CV of only 1.24%. Zero outlier folds.">
    <div class="mb-3">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Generalization & Rigor</span>
      <h2 class="text-3xl font-extrabold text-slate-900">24-Year Generalization: 5-Fold Walk-Forward Cross-Validation</h2>
    </div>

    <div class="grid grid-cols-12 gap-6 flex-1 items-center">
      <div class="col-span-8 bg-white p-3 rounded-xl border border-slate-200 card-shadow flex items-center justify-center">
        <img src="figures/fig5_walk_forward_stability.png" class="max-h-[460px] object-contain rounded" alt="Walk Forward Stability">
      </div>

      <div class="col-span-4 space-y-3 text-xs text-slate-700">
        <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow space-y-2">
          <div class="font-bold text-sm text-slate-900 text-emerald-700">Walk-Forward Consistency Metrics</div>
          <div>• <strong>Mean R² Score:</strong> <span class="font-mono font-bold text-emerald-600">0.9489 ± 0.0118</span></div>
          <div>• <strong>Coefficient of Variation (CV):</strong> <span class="font-mono font-bold">1.24%</span> (Extremely stable)</div>
          <div>• <strong>Mean MAPE:</strong> <span class="font-mono font-bold text-orange-600">7.84% ± 0.55%</span></div>
          <div>• <strong>Average 24-Yr Accuracy:</strong> <span class="font-bold text-emerald-600">92.16%</span></div>
        </div>

        <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow space-y-2">
          <div class="font-bold text-sm text-slate-900">Why Walk-Forward vs. K-Fold?</div>
          <div>Standard K-fold shuffles data randomly, causing severe data leakage (future prices predicting past prices). Our expanding-window setup strictly preserves temporal causality.</div>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 8: TIME SERIES ANALYTICS (FIGURE 2) -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Walk through Figure 2: actual prices vs predictions with 95% confidence intervals and residual errors.">
    <div class="mb-3">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Predictive Analytics</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Time-Series Analytics: Actual vs. Predicted Price Trajectory</h2>
    </div>

    <div class="flex-1 bg-white border border-slate-200 rounded-xl p-3 card-shadow flex items-center justify-center">
      <img src="figures/fig2_price_forecast_actual_vs_predicted.png" class="max-h-[460px] object-contain rounded" alt="Time Series Forecast">
    </div>
    <div class="mt-2 text-center text-xs text-slate-500 font-mono">
      Figure 2: 60-day prediction sequence for Nashik APMC Onion cohort. Shaded band shows 95% confidence interval (±₹75/Qtl).
    </div>
  </div>

  <!-- SLIDE 9: 6-FACTOR HYBRID PRICING FORMULA -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Explain the 6 factors: Mandi 35%, ML 25%, EMA 20%, Week 10%, Weather 5%, Hist 5%, plus quality multipliers for Grade A/B/C.">
    <div class="mb-4">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Decision Support</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Smart Pricing Engine: The 6-Factor Hybrid Formula</h2>
    </div>

    <div class="bg-emerald-900 text-white p-4 rounded-xl mb-4 font-mono text-center text-sm shadow">
      P_rec = 0.35 * P_mandi + 0.25 * P_ML + 0.20 * P_EMA + 0.10 * P_week + 0.05 * P_weather + 0.05 * P_hist<br>
      <span class="text-emerald-300 text-xs font-sans">Final Price = P_rec × Quality_Multiplier (Grade A: 1.02, Grade B: 1.00, Grade C: 0.95)</span>
    </div>

    <div class="grid grid-cols-3 gap-4 flex-1 text-xs">
      <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow">
        <div class="font-bold text-sm text-blue-700 mb-1">35% Mandi Spot Price</div>
        <p class="text-slate-600">Real-time modal price fetched from live AGMARKNET APMC API or localized daily database cache.</p>
      </div>
      <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow">
        <div class="font-bold text-sm text-emerald-700 mb-1">25% Machine Learning</div>
        <p class="text-slate-600">Random Forest Regressor output utilizing 25 engineered lag, arrival, and seasonal features.</p>
      </div>
      <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow">
        <div class="font-bold text-sm text-purple-700 mb-1">20% EMA Momentum</div>
        <p class="text-slate-600">Exponential Moving Average trend (EMA-7/14/30). Multiplier of 1.02x for uptrend, 0.98x for downtrend.</p>
      </div>
      <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow">
        <div class="font-bold text-sm text-teal-700 mb-1">10% 7-Day Average</div>
        <p class="text-slate-600">Trailing 7-day rolling window mean price to smooth out short-term market arrival volatility.</p>
      </div>
      <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow">
        <div class="font-bold text-sm text-orange-700 mb-1">5% Weather Risk Factor</div>
        <p class="text-slate-600">OpenWeatherMap integration. Discounts price by 0.97x if forecast rain probability exceeds 60%.</p>
      </div>
      <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow">
        <div class="font-bold text-sm text-indigo-700 mb-1">5% Historical Baseline</div>
        <p class="text-slate-600">24-year longitudinal monthly historical average for macro price trend calibration.</p>
      </div>
    </div>
  </div>

  <!-- SLIDE 10: MULTILINGUAL RAG ADVISORY -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Demonstrate the RAG pipeline: Sentence-BERT, FAISS IndexFlatIP, cosine threshold 0.45, and Gemini generating in English, Hindi, and Marathi.">
    <div class="mb-4">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Generative AI</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Multilingual Advisory: Retrieval-Augmented Generation (RAG)</h2>
    </div>

    <div class="grid grid-cols-4 gap-4 mb-4 text-xs">
      <div class="bg-white p-4 rounded-xl border-t-4 border-blue-500 card-shadow">
        <div class="font-bold text-sm text-slate-900 mb-1">1. Vector Embedding</div>
        <div class="text-blue-600 font-semibold mb-2">Sentence-BERT (384d)</div>
        <p class="text-slate-600">Transforms user query into 384-dimensional dense semantic vector in <8 ms.</p>
      </div>
      <div class="bg-white p-4 rounded-xl border-t-4 border-emerald-500 card-shadow">
        <div class="font-bold text-sm text-slate-900 mb-1">2. Similarity Index</div>
        <div class="text-emerald-600 font-semibold mb-2">FAISS IndexFlatIP</div>
        <p class="text-slate-600">Inner-product cosine search retrieves Top-3 matching agricultural passages.</p>
      </div>
      <div class="bg-white p-4 rounded-xl border-t-4 border-orange-500 card-shadow">
        <div class="font-bold text-sm text-slate-900 mb-1">3. Guardrail Filter</div>
        <div class="text-orange-600 font-semibold mb-2">Threshold >= 0.45</div>
        <p class="text-slate-600">Queries with similarity < 0.45 trigger automatic fallback to prevent hallucination.</p>
      </div>
      <div class="bg-white p-4 rounded-xl border-t-4 border-purple-500 card-shadow">
        <div class="font-bold text-sm text-slate-900 mb-1">4. LLM Generation</div>
        <div class="text-purple-600 font-semibold mb-2">Google Gemini</div>
        <p class="text-slate-600">Generates localized responses in English, Hindi, and Marathi (Devanagari script).</p>
      </div>
    </div>

    <div class="bg-slate-900 text-slate-100 p-4 rounded-xl text-xs space-y-2 card-shadow font-mono">
      <div class="text-emerald-400 font-bold text-sm font-sans mb-1">Live Multi-Language Advisory Testing</div>
      <div>• <strong>English:</strong> 'What is the fertilizer schedule for Onion?' -> Returns NPK 100:50:50 split application dosage.</div>
      <div>• <strong>Hindi:</strong> 'कांद्यासाठी खत व्यवस्थापन कसे करावे?' -> Returns verified agronomic schedule in Hindi script.</div>
      <div>• <strong>Marathi:</strong> 'सोयाबीन वरील कीड नियंत्रण उपाय सांगा.' -> Returns integrated pest management guidelines from local KVK.</div>
    </div>
  </div>

  <!-- SLIDE 11: B2B MARKETPLACE & FULFILLMENT FSM -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Explain the direct B2B trading mechanism, purchase requests, Haversine road freight calculation, and the 4-stage FSM.">
    <div class="mb-4">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Trade & Fulfillment</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Direct B2B Marketplace & 4-Stage Fulfillment FSM</h2>
    </div>

    <div class="grid grid-cols-2 gap-8 flex-1">
      <div class="bg-white border border-slate-200 rounded-xl p-5 card-shadow space-y-3 text-xs text-slate-700">
        <div class="font-bold text-sm text-slate-900 text-blue-700">Direct Marketplace Operations</div>
        <div>• <strong>Listing Creation:</strong> Farmer posts crop, quantity (quintals), expected rate, grade, and harvest window.</div>
        <div>• <strong>Buyer Requirements & Counter-Bids:</strong> Buyers submit procurement requests and negotiated bids with AI suggested floor protection.</div>
        <div>• <strong>Geodesic Haversine Freight:</strong> Computes road distance with 1.25 circuity multiplier:<br>
          <span class="font-mono text-slate-900 bg-slate-100 px-2 py-0.5 rounded text-[11px]">Freight = (1.25 × d_haversine) × ₹0.50/km × Quantity</span>
        </div>
        <div>• <strong>Transparent Slabs:</strong> 0-100 km (1 day), 101-300 km (2 days), 301-500 km (3 days), >500 km (4-5 days).</div>
      </div>

      <div class="space-y-2.5">
        <div class="p-3 bg-blue-50 border border-blue-300 rounded-xl text-xs">
          <div class="font-bold text-blue-900">STAGE 1: Order Confirmed</div>
          <div class="text-blue-700 text-[11px]">Farmer accepts purchase request. Deal record created with locked rate and quantity.</div>
        </div>
        <div class="p-3 bg-orange-50 border border-orange-300 rounded-xl text-xs">
          <div class="font-bold text-orange-900">STAGE 2: Dispatched</div>
          <div class="text-orange-700 text-[11px]">Consignment packaged and loaded on vehicle. Timestamped dispatch notification sent.</div>
        </div>
        <div class="p-3 bg-purple-50 border border-purple-300 rounded-xl text-xs">
          <div class="font-bold text-purple-900">STAGE 3: Out for Delivery</div>
          <div class="text-purple-700 text-[11px]">Consignment in transit towards buyer mandi/warehouse with ETA tracking.</div>
        </div>
        <div class="p-3 bg-emerald-50 border border-emerald-400 rounded-xl text-xs">
          <div class="font-bold text-emerald-900">STAGE 4: Delivered (Terminal State)</div>
          <div class="text-emerald-700 text-[11px]">Buyer inspects and confirms delivery. Instantly triggers automated digital ledger sync.</div>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 12: AUTOMATED DIGITAL LEDGER SYNCHRONIZATION -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="This is our flagship innovation: reaching Delivered state immediately writes to the ledger, deducts freight, computes net profit, and generates a PDF invoice.">
    <div class="mb-4">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Core Innovation</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Automated Digital Ledger Synchronization (Unique USP)</h2>
    </div>

    <div class="bg-emerald-900 text-white p-4 rounded-xl mb-4 font-mono text-center text-xs shadow">
      [Order Reaches 'Delivered'] ---> [Create Transaction Record] ---> [Generate PDF Invoice] ---> [Post to Farmer Ledger]<br>
      <span class="text-emerald-300 font-sans text-xs">Net Farm Profit = Total Sale Amount - (Transportation Freight + Packaging + Platform Fee)</span>
    </div>

    <div class="grid grid-cols-2 gap-6 flex-1 text-xs">
      <div class="bg-white p-5 rounded-xl border border-slate-200 card-shadow space-y-3">
        <div class="font-bold text-sm text-emerald-700">Autonomous Financial Accounting</div>
        <div>• <strong>Zero Manual Entry:</strong> Farmers never need to manually enter sales numbers; physical delivery completion automatically generates the credit transaction.</div>
        <div>• <strong>Automatic Debit Deductions:</strong> Transportation freight and packaging costs are cleanly segregated into expense line-items.</div>
        <div>• <strong>Net Farm Profit Tracking:</strong> Calculates real return on investment (ROI) after all deductions.</div>
      </div>

      <div class="bg-white p-5 rounded-xl border border-slate-200 card-shadow space-y-3">
        <div class="font-bold text-sm text-blue-700">Audit-Ready Tax Invoicing & Credit Scoring</div>
        <div>• <strong>Downloadable PDF Invoices:</strong> Auto-generates formal invoices with buyer/seller details, timestamps, and deal metadata.</div>
        <div>• <strong>Formal Credit Readiness:</strong> Verified transaction history provides smallholders with legitimate financial records for agricultural bank loans.</div>
        <div>• <strong>CSV Export:</strong> Instant one-click CSV export of annual ledger accounts.</div>
      </div>
    </div>
  </div>

  <!-- SLIDE 13: FULL STACK IMPLEMENTATION -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Walk through the technical architecture: React 18.3, FastAPI, SQLite with SQLAlchemy async ORM, 22 tables, and security mechanisms.">
    <div class="mb-4">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Software Engineering</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Technical Architecture: Full-Stack Implementation</h2>
    </div>

    <div class="grid grid-cols-4 gap-4 flex-1 text-xs">
      <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow space-y-2">
        <div class="font-bold text-sm text-blue-600">Frontend Layer</div>
        <div class="font-mono text-[11px] text-slate-500">React 18.3 + Vite + Tailwind</div>
        <p class="text-slate-600">Role-based dashboards for Farmer, Buyer, Admin. Lucide icons, Chart.js financial charts, and trilingual language switcher.</p>
      </div>

      <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow space-y-2">
        <div class="font-bold text-sm text-emerald-600">Backend Gateway</div>
        <div class="font-mono text-[11px] text-slate-500">FastAPI (Python 3.12)</div>
        <p class="text-slate-600">Asynchronous REST API across 24 routers and 70+ endpoints under /api/v1/. Centralized exception handlers and Pydantic validation.</p>
      </div>

      <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow space-y-2">
        <div class="font-bold text-sm text-purple-600">Persistence Layer</div>
        <div class="font-mono text-[11px] text-slate-500">SQLite + SQLAlchemy 2.0</div>
        <p class="text-slate-600">22 relational tables with foreign-key cascade integrity: users, listings, requests, deals, ledger, ratings, notifications.</p>
      </div>

      <div class="bg-white p-4 rounded-xl border border-slate-200 card-shadow space-y-2">
        <div class="font-bold text-sm text-red-600">Security & RBAC</div>
        <div class="font-mono text-[11px] text-slate-500">JWT HS256 + BCrypt</div>
        <p class="text-slate-600">Role-Based Access Control, BCrypt password hashing, IDOR ownership validation guards, and SQL injection prevention via ORM.</p>
      </div>
    </div>
  </div>

  <!-- SLIDE 14: EMPIRICAL TESTING AUDIT -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Highlight our 68-test suite: 67/68 passed (98.5% pass rate). Emphasize zero mock data.">
    <div class="mb-4">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Quality Assurance</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Comprehensive Testing Audit: 68 Cases (98.5% Pass Rate)</h2>
    </div>

    <div class="grid grid-cols-12 gap-6 flex-1 items-center">
      <div class="col-span-8 overflow-hidden border border-slate-200 rounded-xl card-shadow bg-white text-xs">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-900 text-white font-semibold">
              <th class="p-2.5">Functional Test Module</th>
              <th class="p-2.5">Test Count</th>
              <th class="p-2.5">Pass Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-slate-700">
            <tr><td class="p-2">Authentication & JWT Token Security</td><td class="p-2">7 Tests</td><td class="p-2 text-emerald-600 font-bold">100% (7/7) PASSED</td></tr>
            <tr><td class="p-2">Security, Roles & IDOR Guards</td><td class="p-2">4 Tests</td><td class="p-2 text-emerald-600 font-bold">100% (4/4) PASSED</td></tr>
            <tr><td class="p-2">AGMARKNET Mandi Price Queries</td><td class="p-2">8 Tests</td><td class="p-2 text-emerald-600 font-bold">100% (8/8) PASSED</td></tr>
            <tr><td class="p-2">OpenWeatherMap Live Integration</td><td class="p-2">3 Tests</td><td class="p-2 text-emerald-600 font-bold">100% (3/3) PASSED</td></tr>
            <tr><td class="p-2">AI Price Prediction & 6-Factor Engine</td><td class="p-2">8 Tests</td><td class="p-2 text-emerald-600 font-bold">100% (8/8) PASSED</td></tr>
            <tr><td class="p-2">B2B Deals Lifecycle & Fulfillment FSM</td><td class="p-2">2 Tests</td><td class="p-2 text-emerald-600 font-bold">100% (2/2) PASSED</td></tr>
            <tr><td class="p-2">Digital Ledger & Financial Invoicing</td><td class="p-2">7 Tests</td><td class="p-2 text-emerald-600 font-bold">100% (7/7) PASSED</td></tr>
          </tbody>
        </table>
      </div>

      <div class="col-span-4 bg-emerald-50 border border-emerald-300 rounded-xl p-5 card-shadow space-y-3 text-xs text-slate-800">
        <div class="font-bold text-sm text-emerald-900">Live Verification Summary</div>
        <div>• <strong>Total Tests Run:</strong> 68 automated cases</div>
        <div>• <strong>Passed:</strong> <span class="text-emerald-700 font-bold">67 / 68 (98.5% Pass Rate)</span></div>
        <div>• <strong>Zero Mock Data:</strong> Real SQLite tables & trained pkl model assets</div>
        <div>• <strong>Frontend Build:</strong> Vite production build passes with 0 errors</div>
        <div>• <strong>Swagger API:</strong> Interactive UI live at /docs</div>
      </div>
    </div>
  </div>

  <!-- SLIDE 16: SOFTWARE & HARDWARE REQUIREMENTS -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Explain the software stack (Python 3.12, FastAPI, React 18.3, Scikit-learn, PyTorch, FAISS, Gemini) and hardware requirements (8-16GB RAM, 500GB disk).">
    <div class="mb-4">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">System Infrastructure</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Software & Hardware Requirements</h2>
    </div>

    <div class="grid grid-cols-2 gap-8 flex-1 text-xs">
      <div class="bg-emerald-50/60 border border-emerald-300 rounded-xl p-5 card-shadow flex flex-col justify-between">
        <div>
          <div class="flex items-center space-x-2 text-emerald-800 font-bold mb-3 pb-2 border-b border-emerald-200 text-sm">
            <span>Software Requirements</span>
          </div>
          <ul class="space-y-2 text-slate-800">
            <li><strong class="text-emerald-800">• Operating System:</strong> Ubuntu 22.04 LTS / macOS 13+ / Windows 11</li>
            <li><strong class="text-emerald-800">• Backend Language:</strong> Python 3.12 (Uvicorn ASGI Server)</li>
            <li><strong class="text-emerald-800">• Web Framework:</strong> FastAPI (Async REST APIs, Pydantic validation)</li>
            <li><strong class="text-emerald-800">• Frontend Stack:</strong> React 18.3 + Vite 5.x + Tailwind CSS 3.x</li>
            <li><strong class="text-emerald-800">• Database:</strong> SQLite 3 with SQLAlchemy 2.0 (Async ORM)</li>
            <li><strong class="text-emerald-800">• Machine Learning:</strong> Scikit-learn 1.4 + PyTorch 2.2</li>
            <li><strong class="text-emerald-800">• NLP & Embeddings:</strong> Sentence-Transformers (all-MiniLM-L6-v2) + FAISS (IndexFlatIP)</li>
            <li><strong class="text-emerald-800">• Cloud LLM:</strong> Google Gemini API (Generative Language Client)</li>
            <li><strong class="text-emerald-800">• Weather Integration:</strong> OpenWeatherMap API (Current & Forecast)</li>
            <li><strong class="text-emerald-800">• Market Data:</strong> AGMARKNET National Portal (1.35M records)</li>
            <li><strong class="text-emerald-800">• Authentication:</strong> PyJWT (HS256) + Passlib BCrypt</li>
          </ul>
        </div>
        <div class="bg-emerald-100 p-2.5 rounded-lg text-emerald-900 font-medium text-[11px] mt-2">All software dependencies are open-source or standard API tiers with zero licensing cost.</div>
      </div>

      <div class="bg-blue-50/60 border border-blue-300 rounded-xl p-5 card-shadow flex flex-col justify-between">
        <div>
          <div class="flex items-center space-x-2 text-blue-800 font-bold mb-3 pb-2 border-b border-blue-200 text-sm">
            <span>Hardware Requirements</span>
          </div>
          <ul class="space-y-3 text-slate-800">
            <li><strong class="text-blue-800">• RAM (Minimum):</strong> 8 GB RAM (16 GB Recommended for Random Forest & PyTorch training)</li>
            <li><strong class="text-blue-800">• Storage Space:</strong> 500 GB Hard Drive / SSD (ML Model = 419 MB; Dataset = ~1.4 GB; Database = SQLite)</li>
            <li><strong class="text-blue-800">• Processor:</strong> Intel Core i5 / AMD Ryzen 5 (8th Generation or above)</li>
            <li><strong class="text-blue-800">• GPU (Optional):</strong> NVIDIA GeForce GTX 1060+ CUDA-enabled (Accelerates PyTorch LSTM training)</li>
            <li><strong class="text-blue-800">• Network Connection:</strong> Active broadband connection for live Gemini LLM queries, OpenWeatherMap, and AGMARKNET calls</li>
            <li><strong class="text-blue-800">• Display / Client:</strong> Modern Web Browser (Google Chrome 120+, Firefox 121+, Safari 17+)</li>
            <li><strong class="text-blue-800">• Ports In Use:</strong> Backend: 8000 | Frontend: 5173 | Asset Server: 8080</li>
          </ul>
        </div>
        <div class="bg-blue-100 p-2.5 rounded-lg text-blue-900 font-medium text-[11px] mt-2">Lightweight deployment: Inference runs in &lt;15ms on standard dual-core consumer laptops.</div>
      </div>
    </div>
  </div>

  <!-- SLIDE 17: EXPECTED RESULTS → ACHIEVED RESULTS -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Review 2 promised price models and advisory. Review 3 delivered 96.87% R2, 2.85% MAPE, and full closed loop across all 7 promised modules.">
    <div class="mb-3">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Results Verification</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Expected Results → ✅ Achieved Results (Review 3)</h2>
    </div>

    <!-- Metrics row -->
    <div class="grid grid-cols-4 gap-4 mb-3 text-xs">
      <div class="bg-slate-900 text-white p-3 rounded-xl card-shadow border border-slate-700 text-center">
        <div class="text-emerald-400 font-extrabold text-2xl font-mono">R² = 0.9687</div>
        <div class="text-slate-300 text-[11px]">Price Prediction Accuracy (Unseen 2024 Test)</div>
      </div>
      <div class="bg-slate-900 text-white p-3 rounded-xl card-shadow border border-slate-700 text-center">
        <div class="text-blue-400 font-extrabold text-2xl font-mono">MAPE = 2.85%</div>
        <div class="text-slate-300 text-[11px]">Mean Absolute Percentage Error (97.15% Acc)</div>
      </div>
      <div class="bg-slate-900 text-white p-3 rounded-xl card-shadow border border-slate-700 text-center">
        <div class="text-orange-400 font-extrabold text-2xl font-mono">MAE = ₹68.40</div>
        <div class="text-slate-300 text-[11px]">Average Error per Quintal on ₹3,500 Produce</div>
      </div>
      <div class="bg-slate-900 text-white p-3 rounded-xl card-shadow border border-slate-700 text-center">
        <div class="text-purple-400 font-extrabold text-2xl font-mono">98.5% Pass</div>
        <div class="text-slate-300 text-[11px]">68 Automated QA Test Cases (67/68 Passed)</div>
      </div>
    </div>

    <!-- Table -->
    <div class="overflow-hidden border border-slate-200 rounded-xl card-shadow bg-white text-xs flex-1">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-slate-900 text-white font-semibold">
            <th class="p-2.5 w-1/4">Deliverable / Objective</th>
            <th class="p-2.5 w-1/3">Expected Result (Review 2 Plan)</th>
            <th class="p-2.5 w-1/3">✅ Achieved Result (Review 3 — 100%)</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 text-slate-700">
          <tr class="hover:bg-slate-50"><td class="p-2 font-bold text-slate-900">Crop Price Forecasting Model</td><td class="p-2">Target R² ≥ 0.90 on sample mandi data</td><td class="p-2 font-bold text-emerald-700">✅ R² = 0.9687 on 132K unseen 2024 records</td></tr>
          <tr class="hover:bg-slate-50"><td class="p-2 font-bold text-slate-900">Prediction Error Rate (MAPE)</td><td class="p-2">Target MAPE &lt; 10% across key commodities</td><td class="p-2 font-bold text-emerald-700">✅ MAPE = 2.85% (97.15% predictive accuracy)</td></tr>
          <tr class="hover:bg-slate-50"><td class="p-2 font-bold text-slate-900">B2B Marketplace & Fulfillment</td><td class="p-2">Produce listing UI & basic request mockup</td><td class="p-2 font-bold text-emerald-700">✅ Full 4-Stage FSM: Counter-bids, Freight calc, Delivery</td></tr>
          <tr class="hover:bg-slate-50"><td class="p-2 font-bold text-slate-900">Multilingual Advisory (RAG)</td><td class="p-2">Chatbot UI with generic language model</td><td class="p-2 font-bold text-emerald-700">✅ FAISS + Sentence-BERT + Gemini Trilingual (EN/HI/MR)</td></tr>
          <tr class="hover:bg-slate-50"><td class="p-2 font-bold text-slate-900">Digital Financial Accounting</td><td class="p-2">Manual entry income and expense form</td><td class="p-2 font-bold text-emerald-700">✅ Auto-sync on delivery; PDF tax invoices generated</td></tr>
          <tr class="hover:bg-slate-50"><td class="p-2 font-bold text-slate-900">Live Weather Integration</td><td class="p-2">Static local weather</td><td class="p-2 font-bold text-emerald-700">✅ OpenWeatherMap API integrated into 6-Factor pricing</td></tr>
          <tr class="hover:bg-slate-50"><td class="p-2 font-bold text-slate-900">System Test Coverage & QA</td><td class="p-2">Unit tests for main endpoints</td><td class="p-2 font-bold text-emerald-700">✅ 68 automated tests, 98.5% pass rate, zero mock data</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- SLIDE 17: IMPLEMENTATION PROGRESS (REVIEW 3 — 100% COMPLETE) -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Walk through all 8 modules and show that every single module is at 100% completion with live verification.">
    <div class="mb-3">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Progress Dashboard</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Implementation Progress — Review 3: 100% Complete</h2>
    </div>

    <div class="space-y-2 flex-1 text-xs">
      <div class="bg-white p-3 rounded-xl border border-slate-200 card-shadow flex items-center justify-between">
        <div class="w-1/3">
          <div class="font-bold text-slate-900">1. ML Price Forecasting Engine</div>
          <div class="text-[11px] text-slate-500">Random Forest on 1.35M records • R²=0.9687 • 25 features</div>
        </div>
        <div class="w-1/2 bg-slate-200 h-3 rounded-full overflow-hidden">
          <div class="bg-emerald-600 h-full rounded-full" style="width: 100%"></div>
        </div>
        <div class="font-bold text-emerald-600 text-sm font-mono w-16 text-right">100% ✅</div>
      </div>

      <div class="bg-white p-3 rounded-xl border border-slate-200 card-shadow flex items-center justify-between">
        <div class="w-1/3">
          <div class="font-bold text-slate-900">2. 6-Factor Smart Pricing Recommendation</div>
          <div class="text-[11px] text-slate-500">Mandi + ML + EMA + Weekly + Weather + Historical Baseline</div>
        </div>
        <div class="w-1/2 bg-slate-200 h-3 rounded-full overflow-hidden">
          <div class="bg-emerald-600 h-full rounded-full" style="width: 100%"></div>
        </div>
        <div class="font-bold text-emerald-600 text-sm font-mono w-16 text-right">100% ✅</div>
      </div>

      <div class="bg-white p-3 rounded-xl border border-slate-200 card-shadow flex items-center justify-between">
        <div class="w-1/3">
          <div class="font-bold text-slate-900">3. Multilingual RAG Advisory Engine</div>
          <div class="text-[11px] text-slate-500">Sentence-BERT + FAISS IndexFlatIP + Gemini (EN, HI, MR)</div>
        </div>
        <div class="w-1/2 bg-slate-200 h-3 rounded-full overflow-hidden">
          <div class="bg-emerald-600 h-full rounded-full" style="width: 100%"></div>
        </div>
        <div class="font-bold text-emerald-600 text-sm font-mono w-16 text-right">100% ✅</div>
      </div>

      <div class="bg-white p-3 rounded-xl border border-slate-200 card-shadow flex items-center justify-between">
        <div class="w-1/3">
          <div class="font-bold text-slate-900">4. Direct B2B Marketplace & Counter-Bidding</div>
          <div class="text-[11px] text-slate-500">Live listings • Purchase requests • Haversine road freight</div>
        </div>
        <div class="w-1/2 bg-slate-200 h-3 rounded-full overflow-hidden">
          <div class="bg-blue-600 h-full rounded-full" style="width: 100%"></div>
        </div>
        <div class="font-bold text-blue-600 text-sm font-mono w-16 text-right">100% ✅</div>
      </div>

      <div class="bg-white p-3 rounded-xl border border-slate-200 card-shadow flex items-center justify-between">
        <div class="w-1/3">
          <div class="font-bold text-slate-900">5. 4-Stage Order Fulfillment FSM</div>
          <div class="text-[11px] text-slate-500">Confirmed → Dispatched → In Transit → Delivered</div>
        </div>
        <div class="w-1/2 bg-slate-200 h-3 rounded-full overflow-hidden">
          <div class="bg-blue-600 h-full rounded-full" style="width: 100%"></div>
        </div>
        <div class="font-bold text-blue-600 text-sm font-mono w-16 text-right">100% ✅</div>
      </div>

      <div class="bg-white p-3 rounded-xl border border-slate-200 card-shadow flex items-center justify-between">
        <div class="w-1/3">
          <div class="font-bold text-slate-900">6. Automated Digital Ledger & PDF Invoicing</div>
          <div class="text-[11px] text-slate-500">Auto-sync on delivery • Net profit breakdown • PDF generator</div>
        </div>
        <div class="w-1/2 bg-slate-200 h-3 rounded-full overflow-hidden">
          <div class="bg-blue-600 h-full rounded-full" style="width: 100%"></div>
        </div>
        <div class="font-bold text-blue-600 text-sm font-mono w-16 text-right">100% ✅</div>
      </div>

      <div class="bg-white p-3 rounded-xl border border-slate-200 card-shadow flex items-center justify-between">
        <div class="w-1/3">
          <div class="font-bold text-slate-900">7. Live Weather & Risk Engine</div>
          <div class="text-[11px] text-slate-500">OpenWeatherMap API • Real-time precipitation risk calculation</div>
        </div>
        <div class="w-1/2 bg-slate-200 h-3 rounded-full overflow-hidden">
          <div class="bg-orange-600 h-full rounded-full" style="width: 100%"></div>
        </div>
        <div class="font-bold text-orange-600 text-sm font-mono w-16 text-right">100% ✅</div>
      </div>

      <div class="bg-white p-3 rounded-xl border border-slate-200 card-shadow flex items-center justify-between">
        <div class="w-1/3">
          <div class="font-bold text-slate-900">8. Full-Stack Security, Auth & RBAC</div>
          <div class="text-[11px] text-slate-500">JWT HS256 • BCrypt • IDOR guards • 24 routers • 22 tables</div>
        </div>
        <div class="w-1/2 bg-slate-200 h-3 rounded-full overflow-hidden">
          <div class="bg-orange-600 h-full rounded-full" style="width: 100%"></div>
        </div>
        <div class="font-bold text-orange-600 text-sm font-mono w-16 text-right">100% ✅</div>
      </div>
    </div>

    <div class="mt-2 text-center bg-emerald-800 text-white font-bold p-2 rounded-xl text-xs">
      🎉 OVERALL PROJECT COMPLETION: 100% — ALL 8 CORE MODULES FULLY OPERATIONAL AND VERIFIED
    </div>
  </div>

  <!-- SLIDE 19: COMPLETED WORK PLAN (TIMELINE) -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Present the completed timeline from June 2025 to January 2026. Every phase has been completed on schedule.">
    <div class="mb-3">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Project Timeline</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Work Plan — All Milestones Completed ✅</h2>
    </div>

    <div class="space-y-3 flex-1 text-xs">
      <div class="bg-white p-3.5 rounded-xl border border-slate-200 card-shadow flex items-center justify-between">
        <div class="w-40 font-bold text-blue-700 bg-blue-50 px-3 py-1.5 rounded-lg text-center">
          Phase 1 (Jun–Jul 2025)
        </div>
        <div class="text-slate-400 font-bold text-base px-2">→</div>
        <div class="flex-1 px-4">
          <div class="font-bold text-slate-900 text-sm">Project Initiation & Literature Survey</div>
          <div class="text-slate-600 text-[11px]">• Problem formulation • Literature review of 20 IEEE/Springer papers • Stack selection (FastAPI, React, SQLite, Scikit-learn)</div>
        </div>
        <span class="badge-emerald px-3 py-1 rounded-full font-bold">COMPLETED ✅</span>
      </div>

      <div class="bg-white p-3.5 rounded-xl border border-slate-200 card-shadow flex items-center justify-between">
        <div class="w-40 font-bold text-emerald-700 bg-emerald-50 px-3 py-1.5 rounded-lg text-center">
          Phase 2 (Aug 2025)
        </div>
        <div class="text-slate-400 font-bold text-base px-2">→</div>
        <div class="flex-1 px-4">
          <div class="font-bold text-slate-900 text-sm">Dataset Acquisition & Feature Engineering</div>
          <div class="text-slate-600 text-[11px]">• 1,351,051 AGMARKNET records • 25 engineered lag, arrival & calendar features • Database ER design (22 tables)</div>
        </div>
        <span class="badge-emerald px-3 py-1 rounded-full font-bold">COMPLETED ✅</span>
      </div>

      <div class="bg-white p-3.5 rounded-xl border border-slate-200 card-shadow flex items-center justify-between">
        <div class="w-40 font-bold text-orange-700 bg-orange-50 px-3 py-1.5 rounded-lg text-center">
          Phase 3 (Sep 2025)
        </div>
        <div class="text-slate-400 font-bold text-base px-2">→</div>
        <div class="flex-1 px-4">
          <div class="font-bold text-slate-900 text-sm">Model Training & Walk-Forward Cross-Validation</div>
          <div class="text-slate-600 text-[11px]">• Random Forest vs LSTM vs Linear Reg • 5-fold expanding CV (R²=0.9489) • Final test set R²=0.9687, MAPE=2.85%</div>
        </div>
        <span class="badge-emerald px-3 py-1 rounded-full font-bold">COMPLETED ✅</span>
      </div>

      <div class="bg-white p-3.5 rounded-xl border border-slate-200 card-shadow flex items-center justify-between">
        <div class="w-40 font-bold text-purple-700 bg-purple-50 px-3 py-1.5 rounded-lg text-center">
          Phase 4 (Oct–Nov 2025)
        </div>
        <div class="text-slate-400 font-bold text-base px-2">→</div>
        <div class="flex-1 px-4">
          <div class="font-bold text-slate-900 text-sm">Full-Stack Development & RAG Integration</div>
          <div class="text-slate-600 text-[11px]">• React 18.3 UI • FAISS multilingual RAG advisory • B2B Marketplace, 4-Stage FSM, and Automated Ledger Sync</div>
        </div>
        <span class="badge-emerald px-3 py-1 rounded-full font-bold">COMPLETED ✅</span>
      </div>

      <div class="bg-white p-3.5 rounded-xl border border-slate-200 card-shadow flex items-center justify-between">
        <div class="w-40 font-bold text-slate-700 bg-slate-100 px-3 py-1.5 rounded-lg text-center">
          Phase 5 (Dec 2025–Jan 2026)
        </div>
        <div class="text-slate-400 font-bold text-base px-2">→</div>
        <div class="flex-1 px-4">
          <div class="font-bold text-slate-900 text-sm">Testing, Research Paper & Final Defense</div>
          <div class="text-slate-600 text-[11px]">• 68 automated tests (98.5% pass) • IEEE paper (20 citations, 6 figures) • Review 3 final presentation & demo guide</div>
        </div>
        <span class="badge-emerald px-3 py-1 rounded-full font-bold">COMPLETED ✅</span>
      </div>
    </div>
  </div>

  <!-- SLIDE 20: IEEE RESEARCH PAPER DEFENSE -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Show that we wrote a full IEEE conference paper with 20 real downloaded citations, 6 scientific figures, and formal math.">
    <div class="mb-4">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Academic Rigor</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Research Paper: Submission-Ready IEEE Conference Paper</h2>
    </div>

    <div class="bg-white border border-slate-200 rounded-xl p-6 card-shadow space-y-4 text-xs text-slate-700 flex-1">
      <div class="font-bold text-base text-slate-900">Paper Title: <em>CropPoint: An AI-Enhanced Agricultural Marketplace and Decision Support System for Crop Price Forecasting, RAG-Based Advisory, and Automated Ledger Synchronization</em></div>
      
      <div class="grid grid-cols-2 gap-6 pt-2">
        <div class="space-y-3">
          <div>• <strong>Official IEEEtran Format:</strong> Formatted in standard 2-column layout with Roman numeral sections, algorithms, and LaTeX equations.</div>
          <div>• <strong>Empirical Validation:</strong> Full benchmarking of Random Forest vs. PyTorch LSTM vs. Linear Regression on 1,351,051 records.</div>
          <div>• <strong>6 Publication-Grade Figures:</strong> 300-DPI high-res figures covering benchmarks, time-series forecasting, residual histograms, feature importance, and architecture.</div>
        </div>

        <div class="space-y-3">
          <div>• <strong>20 Verified Downloaded References:</strong> Every single citation (Breiman, Lewis NeurIPS, Johnson IEEE TBD, Hochreiter LSTM, Liakos Sensors, Wolfert Agri Systems) corresponds to a verified local PDF in <span class="font-mono text-emerald-700">references/</span>.</div>
          <div>• <strong>Zero Broken Links:</strong> All formulas mathematically consistent with production backend algorithms.</div>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 17: LIVE DEMO SEQUENCE -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Tell the committee you will now do a 5-step live demonstration: Terminal Accuracy -> AI Recommendation -> Multilingual RAG -> Order FSM -> Automated Ledger.">
    <div class="mb-4">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Demonstration Protocol</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Live Demonstration Walkthrough (Review 3 Demo Flow)</h2>
    </div>

    <div class="space-y-2.5 flex-1 text-xs">
      <div class="p-3 bg-white border border-slate-200 rounded-xl card-shadow flex items-center justify-between">
        <div>
          <strong class="text-sm text-blue-700">Step 1: Terminal Accuracy Audit</strong>
          <p class="text-slate-600">Run: <span class="font-mono bg-slate-100 px-1 py-0.5 rounded">python backend/show_accuracy.py</span> in VS Code. Instantly displays R²=0.9687, MAE=₹68.40, and 24-year validation table live.</p>
        </div>
        <span class="badge-blue px-3 py-1 rounded-full font-bold">2 SECONDS</span>
      </div>

      <div class="p-3 bg-white border border-slate-200 rounded-xl card-shadow flex items-center justify-between">
        <div>
          <strong class="text-sm text-emerald-700">Step 2: AI Price Recommendation</strong>
          <p class="text-slate-600">Open localhost:5173, select Onion (Nashik, Grade A). Shows live 6-factor hybrid rate (₹3,801/Qtl) with 92% confidence.</p>
        </div>
        <span class="badge-emerald px-3 py-1 rounded-full font-bold">LIVE ML</span>
      </div>

      <div class="p-3 bg-white border border-slate-200 rounded-xl card-shadow flex items-center justify-between">
        <div>
          <strong class="text-sm text-purple-700">Step 3: Multilingual RAG Advisory Chat</strong>
          <p class="text-slate-600">Ask questions in English and Marathi ('कांद्यासाठी खत व्यवस्थापन'). Demonstrates FAISS vector retrieval and Devanagari output.</p>
        </div>
        <span class="bg-purple-100 text-purple-800 px-3 py-1 rounded-full font-bold border border-purple-200">FAISS + GEMINI</span>
      </div>

      <div class="p-3 bg-white border border-slate-200 rounded-xl card-shadow flex items-center justify-between">
        <div>
          <strong class="text-sm text-orange-700">Step 4: B2B Order & 4-Stage Fulfillment FSM</strong>
          <p class="text-slate-600">Farmer lists crop -> Buyer sends purchase request -> Accept request. Progress through Confirmed -> Dispatched -> Transit -> Delivered.</p>
        </div>
        <span class="bg-orange-100 text-orange-800 px-3 py-1 rounded-full font-bold border border-orange-200">4-STAGE FSM</span>
      </div>

      <div class="p-3 bg-white border border-slate-200 rounded-xl card-shadow flex items-center justify-between">
        <div>
          <strong class="text-sm text-emerald-700">Step 5: Automated Ledger Synchronization</strong>
          <p class="text-slate-600">Open Digital Ledger. As soon as Delivered is clicked, show the new ₹2,38,000 credit entry, freight deduction, and invoice PDF.</p>
        </div>
        <span class="badge-emerald px-3 py-1 rounded-full font-bold">CORE USP</span>
      </div>
    </div>
  </div>

  <!-- SLIDE 18: CONCLUSION & FUTURE SCOPE -->
  <div class="slide bg-slate-50 text-slate-900 px-16 pt-16 pb-12 flex-col justify-start" data-notes="Conclude by summarizing that the project is 100% complete and outline future extensions: smart contract escrow, CNN leaf disease diagnosis, and satellite NDVI.">
    <div class="mb-4">
      <span class="text-xs font-bold text-emerald-600 uppercase tracking-widest">Final Defense Takeaways</span>
      <h2 class="text-3xl font-extrabold text-slate-900">Conclusion & Future Research Scope</h2>
    </div>

    <div class="grid grid-cols-2 gap-8 flex-1 text-xs text-slate-700">
      <div class="bg-emerald-50 border border-emerald-300 rounded-xl p-5 card-shadow space-y-3">
        <div class="font-bold text-sm text-emerald-900">Review 3 Conclusion: 100% Completed</div>
        <div>• <strong>Unified Closed Loop:</strong> Successfully unified price prediction, advisory, B2B trade, and digital accounting into one seamless system.</div>
        <div>• <strong>Empirical Validation:</strong> Random Forest model validated across 1,351,051 records (R² = 0.9687, MAPE = 2.85%).</div>
        <div>• <strong>Production Readiness:</strong> 24 routers, 22 database tables, 68 test cases (98.5% pass rate), zero mock data.</div>
        <div>• <strong>Socio-Economic Impact:</strong> Protects smallholders from intermediary monopsony and automates financial bookkeeping.</div>
      </div>

      <div class="bg-white border border-slate-200 rounded-xl p-5 card-shadow space-y-3">
        <div class="font-bold text-sm text-blue-700">Future Research & Engineering Scope</div>
        <div>• <strong>Smart Contract Payment Escrow:</strong> Blockchain escrow releasing payment upon IoT-sensor-verified delivery.</div>
        <div>• <strong>Computer Vision Disease Diagnosis:</strong> Integrating MobileNet/EfficientNet CNN to diagnose crop diseases from leaf photos directly in RAG context.</div>
        <div>• <strong>Satellite NDVI Monitoring:</strong> Sentinel-2 satellite imagery integration for regional vegetation health and yield forecasting.</div>
        <div>• <strong>Reinforcement Learning (RLHF):</strong> Fine-tuning recommendation weights based on continuous farmer negotiation feedback.</div>
      </div>
    </div>
  </div>

</div>

<!-- SPEAKER NOTES DRAWER -->
<div id="notesDrawer" class="fixed bottom-0 left-0 right-0 z-50 bg-slate-900/95 text-slate-100 p-4 border-t border-slate-800 transform translate-y-full transition-transform duration-300 text-xs font-mono">
  <div class="flex items-center justify-between mb-1">
    <span class="text-emerald-400 font-bold uppercase tracking-wider">Speaker Notes (What to say to Sir)</span>
    <span class="text-slate-500 text-[10px]">Press 'N' to close</span>
  </div>
  <p id="speakerNotesText" class="text-slate-300 leading-relaxed"></p>
</div>

<!-- SLIDE INDEX JUMP MENU -->
<div id="indexMenu" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur hidden flex items-center justify-center p-8">
  <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-3xl w-full max-h-[85vh] overflow-y-auto text-white">
    <div class="flex items-center justify-between mb-4 pb-2 border-b border-slate-800">
      <h3 class="text-lg font-bold text-emerald-400">Jump to Slide</h3>
      <button onclick="toggleMenu()" class="text-slate-400 hover:text-white">✕</button>
    </div>
    <div id="slideList" class="grid grid-cols-2 gap-2 text-xs"></div>
  </div>
</div>

<script>
  let currentSlide = 0;
  const slides = document.querySelectorAll('.slide');
  const totalSlides = slides.length;
  document.getElementById('totalSlideNum').innerText = totalSlides;

  const slideTitles = [
    "Title Slide: Hero Cover",
    "Executive Summary & Problem Statement",
    "Review 2 Commitments vs Review 3 Delivery",
    "System Architecture: 5-Stage Closed Loop",
    "Dataset Engineering & Feature Importance",
    "Model Performance Benchmarks",
    "24-Year Walk-Forward Stability Proof",
    "Time-Series Price Analytics & Residuals",
    "6-Factor Hybrid Pricing Recommendation",
    "Multilingual RAG Advisory Engine",
    "Direct B2B Marketplace & Fulfillment FSM",
    "Automated Digital Ledger Synchronization",
    "Technical Full-Stack Architecture",
    "Quality Assurance: 68-Case Testing Audit",
    "Software & Hardware Requirements",
    "Expected Results → Achieved Results",
    "Implementation Progress (Review 3 — 100%)",
    "Work Plan — Completed Timeline",
    "IEEE Research Paper Defense",
    "Live Demonstration Walkthrough",
    "Conclusion & Future Scope"
  ];

  function showSlide(index) {
    if (index < 0) index = 0;
    if (index >= totalSlides) index = totalSlides - 1;
    slides.forEach((s, i) => {
      s.classList.toggle('active', i === index);
    });
    currentSlide = index;
    document.getElementById('currentSlideNum').innerText = currentSlide + 1;
    const notes = slides[currentSlide].getAttribute('data-notes') || 'No notes for this slide.';
    document.getElementById('speakerNotesText').innerText = notes;
  }

  function nextSlide() { showSlide(currentSlide + 1); }
  function prevSlide() { showSlide(currentSlide - 1); }

  function toggleNotes() {
    const drawer = document.getElementById('notesDrawer');
    drawer.classList.toggle('translate-y-full');
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      if (document.exitFullscreen) document.exitFullscreen();
    }
  }

  function toggleMenu() {
    const menu = document.getElementById('indexMenu');
    menu.classList.toggle('hidden');
    if (!menu.classList.contains('hidden')) {
      const list = document.getElementById('slideList');
      list.innerHTML = slideTitles.map((t, i) => `
        <button onclick="showSlide(${i}); toggleMenu();" class="text-left p-2 rounded hover:bg-slate-800 transition flex items-center space-x-2 ${i === currentSlide ? 'bg-emerald-900/50 text-emerald-400 font-bold' : 'text-slate-300'}">
          <span class="w-5 text-slate-500 font-mono text-[10px]">${i+1}.</span>
          <span class="truncate">${t}</span>
        </button>
      `).join('');
    }
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { nextSlide(); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { prevSlide(); }
    else if (e.key === 'f' || e.key === 'F') { toggleFullscreen(); }
    else if (e.key === 'n' || e.key === 'N') { toggleNotes(); }
    else if (e.key === 'm' || e.key === 'M') { toggleMenu(); }
    else if (e.key === 'Escape') {
      const menu = document.getElementById('indexMenu');
      if (!menu.classList.contains('hidden')) toggleMenu();
      const notes = document.getElementById('notesDrawer');
      if (!notes.classList.contains('translate-y-full')) toggleNotes();
    }
  });

  showSlide(0);
</script>
</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ HTML presentation generated: {OUTPUT_HTML}")
