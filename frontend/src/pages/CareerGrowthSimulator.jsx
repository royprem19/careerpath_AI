import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, Award, Sparkles, Brain, CheckCircle2, 
  AlertTriangle, ChevronRight, BarChart3, HelpCircle, ArrowRight 
} from 'lucide-react';
import { predictJDSHike, predictSDSLeadership } from '../services/api';
import { Link } from 'react-router-dom';

const CareerGrowthSimulator = () => {
  const [activeTab, setActiveTab] = useState('jds'); // 'jds' or 'sds'
  
  // JDS State (1-5 scale)
  const [jdsScores, setJdsScores] = useState({
    big_data_skills: 3.8,
    maths_stats_skills: 4.2,
    coding_skills: 4.0,
    ai_and_ml_skills: 4.3,
    dashboard_and_storytelling_skills: 4.5,
  });
  const [jdsResult, setJdsResult] = useState(null);
  const [jdsLoading, setJdsLoading] = useState(false);

  // SDS State (0-100 scale)
  const [sdsScores, setSdsScores] = useState({
    conscientiousness: 48,
    openness_to_experience: 46,
    extraversion: 44,
    agreeableness: 45,
    neuroticism: 36,
  });
  const [sdsResult, setSdsResult] = useState(null);
  const [sdsLoading, setSdsLoading] = useState(false);

  // Auto-predict on slider change (debounced)
  useEffect(() => {
    const timer = setTimeout(() => {
      runJdsPrediction();
    }, 250);
    return () => clearTimeout(timer);
  }, [jdsScores]);

  useEffect(() => {
    const timer = setTimeout(() => {
      runSdsPrediction();
    }, 250);
    return () => clearTimeout(timer);
  }, [sdsScores]);

  const runJdsPrediction = async () => {
    setJdsLoading(true);
    try {
      const res = await predictJDSHike(jdsScores);
      if (res.data) setJdsResult(res.data);
    } catch (err) {
      console.error("JDS prediction failed:", err);
    } finally {
      setJdsLoading(false);
    }
  };

  const runSdsPrediction = async () => {
    setSdsLoading(true);
    try {
      const res = await predictSDSLeadership(sdsScores);
      if (res.data) setSdsResult(res.data);
    } catch (err) {
      console.error("SDS prediction failed:", err);
    } finally {
      setSdsLoading(false);
    }
  };

  const handleJdsChange = (field, val) => {
    setJdsScores(prev => ({ ...prev, [field]: parseFloat(val) }));
  };

  const handleSdsChange = (field, val) => {
    setSdsScores(prev => ({ ...prev, [field]: parseInt(val, 10) }));
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 animate-fade-in">
      
      {/* Header Banner */}
      <div className="text-center max-w-3xl mx-auto mb-10">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-50 border border-indigo-100 text-indigo-700 text-xs font-bold mb-3 shadow-2xs">
          <Sparkles size={14} className="text-indigo-600 animate-pulse" />
          <span>SAS & CU Hackathon Talent Intelligence Engine</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
          AI Career Progression & Promotion Simulator
        </h1>
        <p className="mt-3 text-slate-600 text-sm sm:text-base leading-relaxed">
          Trained on empirical workplace evaluations across 139 Junior and 161 Senior Data Scientists. 
          Simulate your promotion probability and leadership readiness in real time.
        </p>

        {/* Tab Switcher */}
        <div className="mt-8 inline-flex p-1.5 rounded-2xl bg-slate-100/90 border border-slate-200/80 shadow-inner">
          <button
            onClick={() => setActiveTab('jds')}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition-all ${
              activeTab === 'jds'
                ? 'bg-white text-indigo-700 shadow-md shadow-indigo-100/50 scale-100'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <TrendingUp size={16} />
            <span>Junior Promotion & Hike Predictor</span>
          </button>
          <button
            onClick={() => setActiveTab('sds')}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition-all ${
              activeTab === 'sds'
                ? 'bg-white text-indigo-700 shadow-md shadow-indigo-100/50 scale-100'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Brain size={16} />
            <span>Senior Leadership & Big-5 Profiler</span>
          </button>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* TAB 1: JUNIOR DATA SCIENTIST (JDS) PROMOTION & HIKE SIMULATOR */}
      {/* ========================================================================= */}
      {activeTab === 'jds' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Controls Column (7 Cols) */}
          <div className="lg:col-span-7 bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/80 shadow-sm">
            <div className="flex items-center justify-between pb-5 border-b border-slate-100 mb-6">
              <div>
                <h2 className="text-lg font-black text-slate-900">Technical Competencies (1 to 5)</h2>
                <p className="text-xs text-slate-500 mt-0.5">Adjust your proficiency across the 5 evaluated pillars</p>
              </div>
              <span className="text-[11px] font-bold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-100">
                84.3% Model Accuracy (AUC 0.89)
              </span>
            </div>

            <div className="space-y-6">
              
              {/* Slider 1: Dashboard & Storytelling */}
              <div className="bg-indigo-50/40 p-4 rounded-2xl border border-indigo-100/80">
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center gap-2">
                    <label className="text-xs font-black text-slate-900">Dashboard & Storytelling</label>
                    <span className="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-indigo-600 text-white">
                      #1 Impact (3.8x Odds)
                    </span>
                  </div>
                  <span className="text-sm font-black text-indigo-700 bg-white px-2.5 py-0.5 rounded-lg border border-indigo-200 shadow-2xs">
                    {jdsScores.dashboard_and_storytelling_skills.toFixed(1)} / 5.0
                  </span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="5"
                  step="0.1"
                  value={jdsScores.dashboard_and_storytelling_skills}
                  onChange={(e) => handleJdsChange('dashboard_and_storytelling_skills', e.target.value)}
                  className="w-full accent-indigo-600 cursor-pointer h-2 bg-slate-200 rounded-lg"
                />
                <p className="text-[11px] text-slate-500 mt-1.5">
                  Translating statistical models into executive storytelling has the highest correlation with promotions (+0.554).
                </p>
              </div>

              {/* Slider 2: Mathematics & Statistics */}
              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200/70">
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center gap-2">
                    <label className="text-xs font-black text-slate-900">Mathematics & Statistics</label>
                    <span className="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-blue-600 text-white">
                      5.85x Multiplier
                    </span>
                  </div>
                  <span className="text-sm font-black text-blue-700 bg-white px-2.5 py-0.5 rounded-lg border border-slate-200 shadow-2xs">
                    {jdsScores.maths_stats_skills.toFixed(1)} / 5.0
                  </span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="5"
                  step="0.1"
                  value={jdsScores.maths_stats_skills}
                  onChange={(e) => handleJdsChange('maths_stats_skills', e.target.value)}
                  className="w-full accent-blue-600 cursor-pointer h-2 bg-slate-200 rounded-lg"
                />
                <p className="text-[11px] text-slate-500 mt-1.5">
                  Hypothesis testing, distributions, and experimental intuition. Single strongest odds multiplier.
                </p>
              </div>

              {/* Slider 3: AI & ML Skills */}
              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200/70">
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center gap-2">
                    <label className="text-xs font-black text-slate-900">AI & Machine Learning</label>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-purple-100 text-purple-700">
                      3.4x Multiplier
                    </span>
                  </div>
                  <span className="text-sm font-black text-purple-700 bg-white px-2.5 py-0.5 rounded-lg border border-slate-200 shadow-2xs">
                    {jdsScores.ai_and_ml_skills.toFixed(1)} / 5.0
                  </span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="5"
                  step="0.1"
                  value={jdsScores.ai_and_ml_skills}
                  onChange={(e) => handleJdsChange('ai_and_ml_skills', e.target.value)}
                  className="w-full accent-purple-600 cursor-pointer h-2 bg-slate-200 rounded-lg"
                />
                <p className="text-[11px] text-slate-500 mt-1.5">
                  Supervised and unsupervised ML architectures, evaluation metrics, and feature selection.
                </p>
              </div>

              {/* Slider 4: Coding Skills */}
              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200/70">
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center gap-2">
                    <label className="text-xs font-black text-slate-900">Coding (SAS, Python, SQL)</label>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-200 text-slate-700">
                      Core Hygiene
                    </span>
                  </div>
                  <span className="text-sm font-black text-slate-800 bg-white px-2.5 py-0.5 rounded-lg border border-slate-200 shadow-2xs">
                    {jdsScores.coding_skills.toFixed(1)} / 5.0
                  </span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="5"
                  step="0.1"
                  value={jdsScores.coding_skills}
                  onChange={(e) => handleJdsChange('coding_skills', e.target.value)}
                  className="w-full accent-slate-800 cursor-pointer h-2 bg-slate-200 rounded-lg"
                />
                <p className="text-[11px] text-slate-500 mt-1.5">
                  Writing clean, performant SQL queries, data manipulation in SAS Base, and Python pipelines.
                </p>
              </div>

              {/* Slider 5: Big Data Skills */}
              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200/70">
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center gap-2">
                    <label className="text-xs font-black text-slate-900">Big Data Skills</label>
                    <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-500">
                      Supporting Pillar
                    </span>
                  </div>
                  <span className="text-sm font-black text-slate-700 bg-white px-2.5 py-0.5 rounded-lg border border-slate-200 shadow-2xs">
                    {jdsScores.big_data_skills.toFixed(1)} / 5.0
                  </span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="5"
                  step="0.1"
                  value={jdsScores.big_data_skills}
                  onChange={(e) => handleJdsChange('big_data_skills', e.target.value)}
                  className="w-full accent-slate-600 cursor-pointer h-2 bg-slate-200 rounded-lg"
                />
                <p className="text-[11px] text-slate-500 mt-1.5">
                  Distributed datasets, Spark, and large-scale ETL pipelines.
                </p>
              </div>

            </div>
          </div>

          {/* Results Column (5 Cols) */}
          <div className="lg:col-span-5 space-y-6">
            
            {/* Main Probability Card */}
            <div className="bg-gradient-to-br from-indigo-900 via-slate-900 to-indigo-950 text-white rounded-3xl p-6 sm:p-8 shadow-xl relative overflow-hidden">
              <div className="absolute top-0 right-0 -mr-16 -mt-16 w-48 h-48 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none" />
              
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold uppercase tracking-wider text-indigo-300">
                  Predicted Outcome
                </span>
                <span className="text-[10px] font-extrabold px-2.5 py-0.5 rounded-full bg-white/10 backdrop-blur-md text-indigo-200 border border-white/10">
                  SAS CU Model
                </span>
              </div>

              {jdsResult ? (
                <div>
                  <div className="flex items-baseline gap-2">
                    <span className="text-5xl sm:text-6xl font-black tracking-tight text-white">
                      {jdsResult.hike_probability_percentage}%
                    </span>
                    <span className="text-sm text-indigo-200 font-bold">Promotion Probability</span>
                  </div>

                  <div className="mt-4 flex items-center gap-2">
                    {jdsResult.is_high_hike_likely ? (
                      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-black bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">
                        <CheckCircle2 size={14} />
                        <span>High Salary Hike Likely</span>
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-black bg-amber-500/20 text-amber-300 border border-amber-400/30">
                        <AlertTriangle size={14} />
                        <span>Standard / Incremental Growth</span>
                      </span>
                    )}
                  </div>

                  {/* Progress Meter */}
                  <div className="mt-6">
                    <div className="w-full bg-white/10 rounded-full h-3 overflow-hidden p-0.5">
                      <div 
                        className={`h-full rounded-full transition-all duration-500 ${
                          jdsResult.hike_probability_percentage >= 70 
                            ? 'bg-gradient-to-r from-emerald-400 to-teal-400' 
                            : jdsResult.hike_probability_percentage >= 45 
                            ? 'bg-gradient-to-r from-amber-400 to-orange-400' 
                            : 'bg-gradient-to-r from-rose-500 to-pink-500'
                        }`}
                        style={{ width: `${Math.max(5, jdsResult.hike_probability_percentage)}%` }}
                      />
                    </div>
                  </div>
                </div>
              ) : (
                <div className="py-8 text-center text-slate-400 text-sm">
                  Calculating trajectory...
                </div>
              )}
            </div>

            {/* Strategic Coaching Card */}
            {jdsResult && (
              <div className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-sm space-y-4">
                <div className="flex items-center gap-2">
                  <BarChart3 size={18} className="text-indigo-600" />
                  <h3 className="text-sm font-black text-slate-900">Highest Leverage Action Items</h3>
                </div>

                <div className="space-y-3">
                  {jdsResult.actionable_leverage_recommendations.map((rec, i) => (
                    <div key={i} className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/60">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-xs font-black text-slate-800">{rec.skill}</span>
                        <span className="text-[10px] font-bold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded-md">
                          Target: {rec.target_score}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-600 leading-relaxed">
                        {rec.impact}
                      </p>
                    </div>
                  ))}
                </div>

                <Link
                  to="/roles"
                  className="w-full mt-4 flex items-center justify-center gap-2 py-3 px-4 rounded-2xl text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 transition-colors shadow-sm"
                >
                  <span>Explore Market Roles Matching Profile</span>
                  <ArrowRight size={14} />
                </Link>
              </div>
            )}

          </div>

        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 2: SENIOR DATA SCIENTIST (SDS) LEADERSHIP & BIG-5 OCEAN PROFILER */}
      {/* ========================================================================= */}
      {activeTab === 'sds' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Controls Column (7 Cols) */}
          <div className="lg:col-span-7 bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/80 shadow-sm">
            <div className="flex items-center justify-between pb-5 border-b border-slate-100 mb-6">
              <div>
                <h2 className="text-lg font-black text-slate-900">Big Five Psychometric Spectrum (OCEAN)</h2>
                <p className="text-xs text-slate-500 mt-0.5">Evaluated across 161 customer-facing senior data science leaders</p>
              </div>
              <span className="text-[11px] font-bold px-2.5 py-1 rounded-full bg-purple-50 text-purple-700 border border-purple-100">
                95.7% Accuracy (AUC 0.995)
              </span>
            </div>

            <div className="space-y-6">

              {/* Slider 1: Conscientiousness */}
              <div className="bg-purple-50/40 p-4 rounded-2xl border border-purple-100/80">
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center gap-2">
                    <label className="text-xs font-black text-slate-900">Conscientiousness</label>
                    <span className="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-purple-600 text-white">
                      31.7% Weight (#1)
                    </span>
                  </div>
                  <span className="text-sm font-black text-purple-700 bg-white px-2.5 py-0.5 rounded-lg border border-purple-200 shadow-2xs">
                    {sdsScores.conscientiousness} / 100
                  </span>
                </div>
                <input
                  type="range"
                  min="20"
                  max="80"
                  step="1"
                  value={sdsScores.conscientiousness}
                  onChange={(e) => handleSdsChange('conscientiousness', e.target.value)}
                  className="w-full accent-purple-600 cursor-pointer h-2 bg-slate-200 rounded-lg"
                />
                <p className="text-[11px] text-slate-500 mt-1.5">
                  Goal-directed execution, project delivery governance, and accountable ownership. Promoted leader average: 53.7.
                </p>
              </div>

              {/* Slider 2: Openness to Experience */}
              <div className="bg-indigo-50/40 p-4 rounded-2xl border border-indigo-100/80">
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center gap-2">
                    <label className="text-xs font-black text-slate-900">Openness to Experience</label>
                    <span className="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-indigo-600 text-white">
                      31.3% Weight (#2)
                    </span>
                  </div>
                  <span className="text-sm font-black text-indigo-700 bg-white px-2.5 py-0.5 rounded-lg border border-indigo-200 shadow-2xs">
                    {sdsScores.openness_to_experience} / 100
                  </span>
                </div>
                <input
                  type="range"
                  min="20"
                  max="80"
                  step="1"
                  value={sdsScores.openness_to_experience}
                  onChange={(e) => handleSdsChange('openness_to_experience', e.target.value)}
                  className="w-full accent-indigo-600 cursor-pointer h-2 bg-slate-200 rounded-lg"
                />
                <p className="text-[11px] text-slate-500 mt-1.5">
                  Cognitive flexibility, creative algorithmic problem reframing, and intellectual curiosity. Promoted leader average: 48.5.
                </p>
              </div>

              {/* Slider 3: Extraversion */}
              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200/70">
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center gap-2">
                    <label className="text-xs font-black text-slate-900">Extraversion</label>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-blue-100 text-blue-700">
                      23.0% Weight (#3)
                    </span>
                  </div>
                  <span className="text-sm font-black text-blue-700 bg-white px-2.5 py-0.5 rounded-lg border border-slate-200 shadow-2xs">
                    {sdsScores.extraversion} / 100
                  </span>
                </div>
                <input
                  type="range"
                  min="20"
                  max="80"
                  step="1"
                  value={sdsScores.extraversion}
                  onChange={(e) => handleSdsChange('extraversion', e.target.value)}
                  className="w-full accent-blue-600 cursor-pointer h-2 bg-slate-200 rounded-lg"
                />
                <p className="text-[11px] text-slate-500 mt-1.5">
                  Client presentation assertiveness, stakeholder networking, and vocal leadership. Promoted leader average: 48.9.
                </p>
              </div>

              {/* Slider 4: Agreeableness */}
              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200/70">
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center gap-2">
                    <label className="text-xs font-black text-slate-900">Agreeableness</label>
                    <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-slate-200 text-slate-600">
                      13.6% Weight
                    </span>
                  </div>
                  <span className="text-sm font-black text-slate-700 bg-white px-2.5 py-0.5 rounded-lg border border-slate-200 shadow-2xs">
                    {sdsScores.agreeableness} / 100
                  </span>
                </div>
                <input
                  type="range"
                  min="20"
                  max="80"
                  step="1"
                  value={sdsScores.agreeableness}
                  onChange={(e) => handleSdsChange('agreeableness', e.target.value)}
                  className="w-full accent-slate-600 cursor-pointer h-2 bg-slate-200 rounded-lg"
                />
                <p className="text-[11px] text-slate-500 mt-1.5">
                  Empathy, collaborative team cohesion, and mentoring trust. Promoted leader average: 47.7.
                </p>
              </div>

              {/* Slider 5: Neuroticism */}
              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200/70">
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center gap-2">
                    <label className="text-xs font-black text-slate-900">Neuroticism (Stress Reactivity)</label>
                    <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-400">
                      0.3% (Neutral)
                    </span>
                  </div>
                  <span className="text-sm font-black text-slate-700 bg-white px-2.5 py-0.5 rounded-lg border border-slate-200 shadow-2xs">
                    {sdsScores.neuroticism} / 100
                  </span>
                </div>
                <input
                  type="range"
                  min="15"
                  max="65"
                  step="1"
                  value={sdsScores.neuroticism}
                  onChange={(e) => handleSdsChange('neuroticism', e.target.value)}
                  className="w-full accent-slate-400 cursor-pointer h-2 bg-slate-200 rounded-lg"
                />
                <p className="text-[11px] text-slate-500 mt-1.5">
                  Emotional volatility under high stakes. Statistical analysis showed neutral impact (r = -0.006).
                </p>
              </div>

            </div>
          </div>

          {/* Results Column (5 Cols) */}
          <div className="lg:col-span-5 space-y-6">
            
            {/* Leadership Readiness Card */}
            <div className="bg-gradient-to-br from-purple-900 via-slate-900 to-indigo-950 text-white rounded-3xl p-6 sm:p-8 shadow-xl relative overflow-hidden">
              <div className="absolute top-0 right-0 -mr-16 -mt-16 w-48 h-48 bg-purple-500/20 rounded-full blur-3xl pointer-events-none" />

              <span className="text-xs font-bold uppercase tracking-wider text-purple-300">
                Leadership Readiness Index
              </span>

              {sdsResult ? (
                <div className="mt-4">
                  <div className="flex items-baseline gap-2">
                    <span className="text-5xl sm:text-6xl font-black tracking-tight text-white">
                      {sdsResult.leadership_success_probability}%
                    </span>
                    <span className="text-sm text-purple-200 font-bold">Client-Facing Fit</span>
                  </div>

                  <div className="mt-4">
                    <div className="p-3 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10">
                      <p className="text-[11px] font-medium text-purple-200">Predicted Archetype</p>
                      <p className="text-sm font-black text-white mt-0.5">
                        {sdsResult.leadership_archetype}
                      </p>
                    </div>
                  </div>

                  <div className="mt-6">
                    <div className="w-full bg-white/10 rounded-full h-3 overflow-hidden p-0.5">
                      <div 
                        className="h-full rounded-full transition-all duration-500 bg-gradient-to-r from-purple-400 to-pink-400"
                        style={{ width: `${Math.max(5, sdsResult.leadership_success_probability)}%` }}
                      />
                    </div>
                  </div>
                </div>
              ) : (
                <div className="py-8 text-center text-slate-400 text-sm">
                  Profiling leadership traits...
                </div>
              )}
            </div>

            {/* Trait Benchmark vs Leaders */}
            {sdsResult && (
              <div className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-sm space-y-4">
                <div className="flex items-center gap-2">
                  <Award size={18} className="text-purple-600" />
                  <h3 className="text-sm font-black text-slate-900">Psychometric Coaching Insights</h3>
                </div>

                <div className="space-y-2.5">
                  {sdsResult.psychometric_coaching_insights.map((tip, i) => (
                    <div key={i} className="p-3 rounded-2xl bg-slate-50 border border-slate-200/60 text-xs text-slate-700 leading-relaxed">
                      {tip}
                    </div>
                  ))}
                </div>

                <Link
                  to="/market-insights"
                  className="w-full mt-4 flex items-center justify-center gap-2 py-3 px-4 rounded-2xl text-xs font-bold text-white bg-slate-900 hover:bg-slate-800 transition-colors shadow-sm"
                >
                  <span>Explore Macro Market Salary Insights</span>
                  <ArrowRight size={14} />
                </Link>
              </div>
            )}

          </div>

        </div>
      )}

    </div>
  );
};

export default CareerGrowthSimulator;
