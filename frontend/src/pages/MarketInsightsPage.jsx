import React, { useState, useEffect } from 'react';
import { 
  Building2, MapPin, IndianRupee, Layers, Sparkles, 
  ArrowUpRight, Calculator, Check, BarChart2, ShieldCheck, RefreshCw 
} from 'lucide-react';
import { getMarketOverview, estimateMarketSalary } from '../services/api';
import { Link } from 'react-router-dom';

const MarketInsightsPage = () => {
  const [marketData, setMarketData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Estimator Form State
  const [exp, setExp] = useState(3.5);
  const [location, setLocation] = useState('Bengaluru');
  const [selectedSkills, setSelectedSkills] = useState(['Python', 'SQL', 'SAS']);
  const [salaryResult, setSalaryResult] = useState(null);
  const [estimating, setEstimating] = useState(false);

  useEffect(() => {
    fetchMarketData();
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      calculateSalary();
    }, 200);
    return () => clearTimeout(timer);
  }, [exp, location, selectedSkills]);

  const fetchMarketData = async () => {
    setLoading(true);
    try {
      const res = await getMarketOverview();
      if (res.data) {
        setMarketData(res.data);
      }
    } catch (err) {
      console.error("Failed to load market overview from backend:", err);
    } finally {
      setLoading(false);
    }
  };

  const calculateSalary = async () => {
    setEstimating(true);
    try {
      const res = await estimateMarketSalary({
        experience_years: parseFloat(exp),
        location,
        skills: selectedSkills
      });
      if (res.data) setSalaryResult(res.data);
    } catch (err) {
      console.error("Salary estimation error:", err);
    } finally {
      setEstimating(false);
    }
  };

  const toggleSkill = (skill) => {
    if (selectedSkills.includes(skill)) {
      setSelectedSkills(selectedSkills.filter(s => s !== skill));
    } else {
      setSelectedSkills([...selectedSkills, skill]);
    }
  };

  const summary = marketData?.market_summary || {};
  const tools = marketData?.key_analytics_tools_demand || {};
  const hubs = marketData?.geographic_distribution || {};
  const recruiters = marketData?.top_volume_recruiters || {};
  const topPayers = marketData?.top_compensation_companies || {};

  // Find max tool count for dynamic percentage bar
  const toolEntries = Object.entries(tools);
  const maxToolCount = toolEntries.length > 0 ? Math.max(...toolEntries.map(([, count]) => count)) : 1;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 animate-fade-in">
      
      {/* Header Banner */}
      <div className="text-center max-w-3xl mx-auto mb-10">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 border border-blue-100 text-blue-700 text-xs font-bold mb-3 shadow-2xs">
          <Sparkles size={14} className="text-blue-600" />
          <span>Real-Time Database Model Intelligence</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
          India Analytics & Data Science Market Trends
        </h1>
        <p className="mt-3 text-slate-600 text-sm sm:text-base leading-relaxed">
          Aggregated live from <strong className="text-slate-900">15,841 Analytics job postings</strong> and{' '}
          <strong className="text-slate-900">93,000+ Enterprise Data Science openings</strong> across{' '}
          <strong className="text-slate-900">642 verified companies</strong>.
        </p>
      </div>

      {/* Loading Skeleton */}
      {loading && !marketData && (
        <div className="py-12 flex flex-col items-center justify-center space-y-4">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div>
          <p className="text-xs text-slate-500 font-bold">Querying backend database models...</p>
        </div>
      )}

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6 mb-12">
        
        <div className="bg-white rounded-3xl p-5 sm:p-6 border border-slate-200/80 shadow-xs">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Analytics Postings</p>
          <p className="text-2xl sm:text-3xl font-black text-slate-900 mt-2">
            {summary.total_analytics_postings ? Number(summary.total_analytics_postings).toLocaleString() : '15,841'}
          </p>
          <div className="mt-2 flex items-center text-xs text-emerald-600 font-bold">
            <span>Verified Dataset</span>
          </div>
        </div>

        <div className="bg-white rounded-3xl p-5 sm:p-6 border border-slate-200/80 shadow-xs">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Active DS Openings</p>
          <p className="text-2xl sm:text-3xl font-black text-indigo-600 mt-2">
            {summary.total_datascience_positions ? Number(summary.total_datascience_positions).toLocaleString() : '93,005'}
          </p>
          <div className="mt-2 flex items-center text-xs text-indigo-600 font-bold">
            <span>{summary.distinct_hiring_companies || 642} Enterprises</span>
          </div>
        </div>

        <div className="bg-white rounded-3xl p-5 sm:p-6 border border-slate-200/80 shadow-xs">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Market Mean Salary</p>
          <p className="text-2xl sm:text-3xl font-black text-slate-900 mt-2">
            ₹{summary.market_mean_salary_lpa || '13.23'} L
          </p>
          <div className="mt-2 flex items-center text-xs text-slate-500 font-bold">
            <span>Median: ₹{summary.market_median_salary_lpa || '11.90'} LPA</span>
          </div>
        </div>

        <div className="bg-white rounded-3xl p-5 sm:p-6 border border-slate-200/80 shadow-xs">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Exp. Premium (OLS)</p>
          <p className="text-2xl sm:text-3xl font-black text-emerald-600 mt-2">+₹1.74 L</p>
          <div className="mt-2 flex items-center text-xs text-slate-500 font-bold">
            <span>Per year experience</span>
          </div>
        </div>

      </div>

      {/* Main Grid: Tools Matrix & Geographic Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-12">
        
        {/* Tool & Tech Stack Demand (6 Cols) */}
        <div className="lg:col-span-6 bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/80 shadow-sm">
          <div className="flex items-center justify-between mb-6 pb-4 border-b border-slate-100">
            <div>
              <h2 className="text-lg font-black text-slate-900">In-Demand Analytics Tools</h2>
              <p className="text-xs text-slate-500 mt-0.5">Live frequency extracted across 15,841 job descriptions</p>
            </div>
            <span className="text-[11px] font-bold px-2.5 py-1 rounded-full bg-blue-50 text-blue-700">
              Live Data
            </span>
          </div>

          <div className="space-y-4">
            {toolEntries.map(([toolName, count], idx) => {
              const isSAS = toolName.toUpperCase() === 'SAS';
              const pct = Math.round((count / maxToolCount) * 100);

              return (
                <div 
                  key={toolName} 
                  className={isSAS ? "p-3 rounded-2xl bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200/70" : ""}
                >
                  <div className="flex justify-between text-xs font-bold mb-1">
                    <span className={isSAS ? "text-blue-900 font-black flex items-center gap-1.5" : "text-slate-800"}>
                      <span>{idx + 1}. {toolName}</span>
                      {isSAS && (
                        <span className="text-[10px] font-extrabold px-1.5 py-0.2 rounded bg-blue-600 text-white">
                          #3 IN INDIA
                        </span>
                      )}
                    </span>
                    <span className={isSAS ? "text-blue-900 font-black" : "text-slate-600"}>
                      {count.toLocaleString()} Postings
                    </span>
                  </div>

                  <div className={`w-full h-2.5 rounded-full overflow-hidden ${isSAS ? "bg-white border border-blue-200" : "bg-slate-100"}`}>
                    <div 
                      className={`h-full rounded-full transition-all duration-500 ${
                        isSAS 
                          ? "bg-blue-700" 
                          : idx === 0 
                          ? "bg-blue-600" 
                          : idx === 1 
                          ? "bg-indigo-600" 
                          : "bg-slate-700"
                      }`} 
                      style={{ width: `${pct}%` }} 
                    />
                  </div>

                  {isSAS && (
                    <p className="text-[10px] text-blue-800/80 mt-1.5 font-medium">
                      SAS dominates Indian Banking, Financial Risk, and Clinical Research analytics infrastructure.
                    </p>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Geographic Compensation Hubs (6 Cols) */}
        <div className="lg:col-span-6 bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/80 shadow-sm">
          <div className="flex items-center justify-between mb-6 pb-4 border-b border-slate-100">
            <div>
              <h2 className="text-lg font-black text-slate-900">Geographic Hubs & Salaries</h2>
              <p className="text-xs text-slate-500 mt-0.5">Empirical regional compensation and hiring concentration</p>
            </div>
            <span className="text-[11px] font-bold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700">
              Chi-Sq p &lt; 0.001
            </span>
          </div>

          <div className="space-y-3">
            {Object.entries(hubs).map(([cityName, data], i) => {
              const isTopPay = cityName === 'Delhi NCR';

              return (
                <div 
                  key={cityName} 
                  className={`p-3.5 rounded-2xl flex items-center justify-between border transition-colors ${
                    isTopPay 
                      ? 'bg-emerald-50/60 border-emerald-200' 
                      : 'bg-slate-50/70 border-slate-200/60 hover:bg-slate-100/60'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div className={`w-8 h-8 rounded-xl flex items-center justify-center font-bold text-xs ${
                      isTopPay ? 'bg-emerald-600 text-white' : 'bg-slate-200 text-slate-700'
                    }`}>
                      {i + 1}
                    </div>
                    <div>
                      <p className="text-xs font-black text-slate-900 flex items-center gap-1.5">
                        <span>{cityName}</span>
                        {isTopPay && (
                          <span className="text-[10px] font-extrabold px-1.5 py-0.2 rounded bg-emerald-600 text-white">
                            Highest Avg Pay
                          </span>
                        )}
                      </p>
                      <p className="text-[11px] text-slate-500">
                        {data.job_count?.toLocaleString()} Postings ({data.percentage_share}%) · Avg Exp: {data.mean_exp_years} yrs
                      </p>
                    </div>
                  </div>

                  <div className="text-right">
                    <p className="text-sm font-black text-slate-900">₹{data.mean_salary_lpa} L</p>
                    <p className="text-[10px] text-slate-400 font-medium">Avg Annual</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

      </div>

      {/* Recruiter Comparison & Interactive Econometric Calculator */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Recruiter Leaderboard (5 Cols) */}
        <div className="lg:col-span-5 bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/80 shadow-sm space-y-6">
          <div>
            <h2 className="text-lg font-black text-slate-900">Recruiter Landscape</h2>
            <p className="text-xs text-slate-500 mt-0.5">Live enterprise breakdown from 93,000+ data science listings</p>
          </div>

          <div className="space-y-2">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Top Volume Recruiters</p>
            {Object.entries(recruiters).slice(0, 5).map(([company, jobsCount], i) => (
              <div key={i} className="flex justify-between items-center py-2 px-3 rounded-xl bg-slate-50 text-xs font-bold">
                <span className="text-slate-800">{company}</span>
                <span className="text-indigo-600 font-black">{Number(jobsCount).toLocaleString()} Jobs</span>
              </div>
            ))}
          </div>

          <div className="space-y-2 pt-2 border-t border-slate-100">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Highest Compensation Tiers</p>
            {Object.entries(topPayers).slice(0, 4).map(([company, avgSal], i) => (
              <div key={i} className="flex justify-between items-center py-2 px-3 rounded-xl bg-emerald-50/50 text-xs font-bold border border-emerald-100">
                <span className="text-slate-800">{company}</span>
                <span className="text-emerald-700 font-black">₹{avgSal} LPA</span>
              </div>
            ))}
          </div>
        </div>

        {/* Interactive Salary Estimator (7 Cols) */}
        <div className="lg:col-span-7 bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/80 shadow-sm">
          <div className="flex items-center justify-between pb-5 border-b border-slate-100 mb-6">
            <div>
              <h2 className="text-lg font-black text-slate-900 flex items-center gap-2">
                <Calculator size={18} className="text-indigo-600" />
                <span>Econometric Market Salary Estimator</span>
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">OLS Multivariable Regression: Salary = 12.95 + 1.74*(Exp) + City + Skills</p>
            </div>
            <span className="text-[11px] font-bold px-2.5 py-1 rounded-full bg-indigo-50 text-indigo-700">
              Live API
            </span>
          </div>

          <div className="space-y-6">
            
            {/* Experience Slider */}
            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="text-xs font-black text-slate-900">Total Professional Experience</label>
                <span className="text-sm font-black text-indigo-700 bg-indigo-50 px-2.5 py-0.5 rounded-lg border border-indigo-200">
                  {exp} Years
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="20"
                step="0.5"
                value={exp}
                onChange={(e) => setExp(e.target.value)}
                className="w-full accent-indigo-600 cursor-pointer h-2 bg-slate-200 rounded-lg"
              />
            </div>

            {/* City Selection */}
            <div>
              <label className="text-xs font-black text-slate-900 block mb-2">Target Geographic Hub</label>
              <div className="grid grid-cols-3 sm:grid-cols-4 gap-2">
                {['Bengaluru', 'Delhi NCR', 'Mumbai', 'Hyderabad', 'Gurgaon', 'Pune', 'Chennai'].map((c) => (
                  <button
                    key={c}
                    type="button"
                    onClick={() => setLocation(c)}
                    className={`py-2 px-2.5 rounded-xl text-xs font-bold transition-all text-center ${
                      location === c 
                        ? 'bg-slate-900 text-white shadow-xs' 
                        : 'bg-slate-50 text-slate-700 hover:bg-slate-100 border border-slate-200/60'
                    }`}
                  >
                    {c}
                  </button>
                ))}
              </div>
            </div>

            {/* Skill Add-ons */}
            <div>
              <label className="text-xs font-black text-slate-900 block mb-2">Key Competencies Mastered</label>
              <div className="flex flex-wrap gap-2">
                {['SAS', 'Python', 'Machine Learning', 'SQL', 'Storytelling & Tableau'].map((skill) => {
                  const isChecked = selectedSkills.includes(skill);
                  return (
                    <button
                      key={skill}
                      type="button"
                      onClick={() => toggleSkill(skill)}
                      className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                        isChecked 
                          ? 'bg-indigo-600 text-white shadow-2xs' 
                          : 'bg-slate-50 text-slate-600 hover:bg-slate-100 border border-slate-200/60'
                      }`}
                    >
                      {isChecked && <Check size={12} />}
                      <span>{skill}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Projected Result Card */}
            {salaryResult && (
              <div className="p-5 rounded-2xl bg-gradient-to-br from-indigo-950 to-slate-900 text-white shadow-md">
                <div className="flex justify-between items-baseline mb-2">
                  <span className="text-xs font-bold text-indigo-300 uppercase">Projected Market Salary</span>
                  <span className="text-xs font-extrabold text-emerald-400">{salaryResult.expected_salary_range_lpa}</span>
                </div>
                
                <div className="flex items-baseline gap-2">
                  <span className="text-4xl font-black text-white">₹{salaryResult.projected_average_salary_lpa}</span>
                  <span className="text-sm font-bold text-indigo-200">Lakhs / Annum</span>
                </div>

                <div className="mt-4 pt-3 border-t border-white/10 grid grid-cols-1 sm:grid-cols-3 gap-2 text-[11px] text-indigo-200">
                  <div>{salaryResult.market_context.experience_impact}</div>
                  <div>{salaryResult.market_context.location_adjustment}</div>
                  <div>{salaryResult.market_context.skill_premiums}</div>
                </div>
              </div>
            )}

            <div className="pt-2 flex justify-between items-center">
              <Link
                to="/career-growth"
                className="text-xs font-bold text-indigo-600 hover:text-indigo-800 flex items-center gap-1"
              >
                <span>Simulate your promotion probability next</span>
                <ArrowUpRight size={14} />
              </Link>
            </div>

          </div>

        </div>

      </div>

    </div>
  );
};

export default MarketInsightsPage;
