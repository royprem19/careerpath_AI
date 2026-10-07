import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import FitScoreGauge from '../components/FitScoreGauge';
import SkillRadarChart from '../components/SkillRadarChart';
import RoleBarChart from '../components/RoleBarChart';
import GapTable from '../components/GapTable';
import RoadmapTimeline from '../components/RoadmapTimeline';
import { 
  Download, RefreshCw, ArrowLeft, Target, Info, CheckCircle2, 
  AlertCircle, Sparkles, BookOpen, ExternalLink, Award, IndianRupee,
  UploadCloud, FileText, Briefcase, Compass, ShieldCheck,
  TrendingUp, BarChart2
} from 'lucide-react';
import { analyzeGap, getRecommendations, getRoadmap, downloadReport, getRoles } from '../services/api';

const Dashboard = () => {
  const { userProfile, selectedRole, setSelectedRole, clearProfile } = useAppContext();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [isDownloading, setIsDownloading] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [roadmap, setRoadmap] = useState([]);
  const [errorMsg, setErrorMsg] = useState('');
  const [resolvedRole, setResolvedRole] = useState(selectedRole);

  const hasProfile = Boolean(userProfile?.skills && userProfile.skills.length > 0);
  const effectiveSkills = userProfile?.skills || [];

  useEffect(() => {
    let isMounted = true;

    if (!hasProfile || !selectedRole) {
      setLoading(false);
      return;
    }

    const performAnalysis = async () => {
      try {
        setLoading(true);
        setErrorMsg('');

        if (isMounted) setResolvedRole(selectedRole);
        const roleId = selectedRole.id || '1';

        // 1. Run Real Gap Analysis API
        const gapResp = await analyzeGap(effectiveSkills, roleId);
        const gap = gapResp.data;

        // 2. Run Real Recommendations API
        let recs = [];
        try {
          const recResp = await getRecommendations(
            effectiveSkills, 
            userProfile?.education || [], 
            userProfile?.experience || {}
          );
          recs = recResp.data || [];
        } catch (recErr) {
          console.warn('Recommendation API fallback:', recErr);
        }

        // 3. Run Real Roadmap API
        const missingAll = [...(gap.missing_essential || []), ...(gap.missing_optional || [])];
        let roadmapData = [];
        try {
          const roadResp = await getRoadmap(missingAll);
          roadmapData = roadResp.data?.entries || [];
        } catch (roadErr) {
          console.warn('Roadmap API fallback:', roadErr);
        }

        if (isMounted) {
          setAnalysisData(gap);
          setRecommendations(recs);
          setRoadmap(roadmapData);
          setLoading(false);
        }
      } catch (err) {
        console.error('Analysis error:', err);
        if (isMounted) {
          setErrorMsg('Failed to run analysis against backend. Please ensure FastAPI server is running on port 8000.');
          setLoading(false);
        }
      }
    };

    performAnalysis();

    return () => {
      isMounted = false;
    };
  }, [selectedRole, userProfile, hasProfile]);

  const currentRole = resolvedRole || selectedRole || {
    id: '1',
    title: 'Full Stack Developer',
    description: 'Architects and builds complete web applications.',
    essential_skills: [],
    optional_skills: []
  };

  const handleDownloadPDF = async () => {
    if (!analysisData) return;
    try {
      setIsDownloading(true);
      const payload = {
        user_profile: {
          skills: effectiveSkills,
          education: userProfile?.education || [],
          experience: userProfile?.experience || {}
        },
        gap_analysis: analysisData,
        recommendations: recommendations,
        roadmap: roadmap
      };
      const response = await downloadReport(payload);
      
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `CareerPath_Analysis_${currentRole.title.replace(/\s+/g, '_')}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('PDF generation error:', err);
      alert('Could not generate PDF report. Check backend report endpoint.');
    } finally {
      setIsDownloading(false);
    }
  };

  // 1. Empty State
  if (!hasProfile || !selectedRole) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <div className="glass-card rounded-3xl p-10 md:p-14 shadow-xl shadow-indigo-500/5 border border-white/90 max-w-2xl mx-auto">
          <div className="w-20 h-20 bg-indigo-50 text-indigo-600 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xs border border-indigo-100">
            <UploadCloud size={38} />
          </div>
          <span className="inline-block text-xs font-bold px-3 py-1 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200/80 mb-3 uppercase tracking-wider">
            {!hasProfile ? 'Profile Needed' : 'Target Role Needed'}
          </span>
          <h2 className="text-2xl md:text-3xl font-black text-slate-900 mb-3">
            {!hasProfile ? 'No Resume or Skills Added Yet' : 'Please Select a Target Role'}
          </h2>
          <p className="text-slate-500 text-sm md:text-base leading-relaxed mb-8 max-w-lg mx-auto font-medium">
            {!hasProfile 
              ? 'Upload your resume (PDF/DOCX) or paste your technical skills on the home page. Our AI engine will extract your competencies and benchmark them against real Indian industry roles.'
              : 'Please choose an industry occupation benchmark from the Roles page to calculate your skill fit score and generate your learning roadmap.'}
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              onClick={() => navigate('/')}
              className="w-full sm:w-auto px-6 py-3.5 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-sm shadow-md shadow-slate-900/10 transition-all flex items-center justify-center gap-2"
            >
              <UploadCloud size={18} />
              Upload Resume or Enter Skills
            </button>
            <button
              onClick={() => navigate('/roles')}
              className="w-full sm:w-auto px-6 py-3.5 rounded-2xl bg-white hover:bg-indigo-50/60 text-indigo-700 font-bold text-sm border-2 border-indigo-300 transition-all flex items-center justify-center gap-2 shadow-2xs"
            >
              <Briefcase size={18} />
              Browse 81 Real Industry Roles
            </button>
          </div>
        </div>
      </div>
    );
  }

  // 2. Loading State
  if (loading) {
    return (
      <div className="min-h-[75vh] flex flex-col items-center justify-center p-4">
        <div className="glass-card rounded-3xl p-10 flex flex-col items-center border border-white/90 shadow-xl shadow-indigo-500/5 max-w-md text-center">
          <div className="animate-spin rounded-full h-14 w-14 border-b-2 border-indigo-600 mb-6"></div>
          <h3 className="text-xl font-black text-slate-900 mb-2">Analyzing Competencies & Industry Demand...</h3>
          <p className="text-xs text-slate-500 leading-relaxed font-medium">
            Matching your skill vector against real industry benchmarks, calculating essential coverage, and tailoring course pathways.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-8 py-8 space-y-8">
      
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-5 glass-card rounded-3xl p-6 border border-white/90 shadow-xl shadow-indigo-500/5">
        <div className="flex items-center space-x-4">
          <button 
            onClick={() => navigate('/roles')} 
            className="p-3 text-slate-500 hover:text-indigo-600 hover:bg-indigo-50/80 rounded-2xl transition-colors border border-slate-200/80 bg-white/90 shadow-2xs"
            title="Choose different role"
          >
            <ArrowLeft size={18} />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-black uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200/70">
                Target Role
              </span>
              <span className="text-xs text-slate-300">•</span>
              <span className="text-xs font-semibold text-slate-500">{currentRole.category || 'Technology'}</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-black text-slate-900 mt-1 tracking-tight">
              {currentRole.title}
            </h1>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <button 
            onClick={() => {
              clearProfile();
              navigate('/');
            }} 
            className="flex items-center px-4 py-2.5 text-xs sm:text-sm font-bold text-slate-700 bg-white border border-slate-200/90 rounded-2xl hover:bg-slate-50 transition-all shadow-2xs"
          >
            <RefreshCw size={14} className="mr-2 text-slate-400" /> New Profile
          </button>
          <button 
            onClick={handleDownloadPDF}
            disabled={isDownloading}
            className="flex items-center px-5 py-2.5 text-xs sm:text-sm font-bold text-white bg-slate-900 hover:bg-slate-800 rounded-2xl shadow-md shadow-slate-900/10 hover:shadow-lg transition-all"
          >
            {isDownloading ? (
              <span className="flex items-center gap-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Generating PDF...
              </span>
            ) : (
              <>
                <Download size={15} className="mr-2" /> Download Report
              </>
            )}
          </button>
        </div>
      </div>

      {errorMsg && (
        <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 flex items-center gap-3 text-amber-900 text-sm shadow-xs font-medium">
          <AlertCircle size={20} className="shrink-0 text-amber-600" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Exploratory Foundation Mode Banner */}
      {(analysisData?.is_exploratory_mode || (analysisData?.fit_score || 0) < 35) && (
        <div className="p-6 rounded-3xl glass-card border-indigo-200/80 bg-gradient-to-r from-indigo-50/80 via-white/80 to-purple-50/80 text-indigo-950 shadow-md">
          <div className="flex items-start gap-4">
            <div className="p-3 bg-indigo-600 text-white rounded-2xl shadow-sm shrink-0 mt-0.5">
              <Compass size={22} />
            </div>
            <div className="space-y-1.5">
              <div className="flex items-center gap-2.5">
                <h3 className="font-black text-base text-slate-900">Career Discovery: Foundational Exploration Track</h3>
                <span className="text-[10px] font-extrabold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-indigo-100 text-indigo-800 border border-indigo-200">
                  Exploratory Alignment
                </span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed font-medium">
                Your current profile has an exploratory alignment ({analysisData?.fit_score || 0}%) for {currentRole.title}. 
                Rather than jumping straight to advanced specialized assessments, we recommend focusing on the foundational milestone curriculum below—accredited through national Government of India initiatives (NPTEL, SWAYAM & Skill India).
              </p>
            </div>
          </div>
        </div>
      )}

      {/* SAS CU Hackathon: Predictive Intelligence & Market Insights Quick Banner */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-5 rounded-3xl bg-gradient-to-br from-indigo-900 via-slate-900 to-indigo-950 text-white shadow-md relative overflow-hidden flex flex-col justify-between border border-indigo-800/40">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full bg-white/20 text-indigo-200">
                Empirical ML Model (84.3% Acc)
              </span>
            </div>
            <h3 className="text-base font-black text-white">AI Promotion & Salary Hike Simulator</h3>
            <p className="text-xs text-indigo-200 leading-relaxed">
              Trained on 139 Junior Data Scientists. Adjust your Storytelling, Math/Stats, and Coding competencies to simulate your promotion probability.
            </p>
          </div>
          <button
            onClick={() => navigate('/career-growth')}
            className="mt-4 w-fit px-4 py-2 rounded-xl bg-white text-indigo-900 hover:bg-indigo-50 font-black text-xs transition-all shadow-xs flex items-center gap-1.5"
          >
            <span>Simulate Promotion & Leadership</span>
            <TrendingUp size={14} />
          </button>
        </div>

        <div className="p-5 rounded-3xl bg-gradient-to-br from-blue-900 via-slate-900 to-slate-950 text-white shadow-md relative overflow-hidden flex flex-col justify-between border border-blue-800/40">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full bg-white/20 text-blue-200">
                17,400+ Indian Job Postings
              </span>
            </div>
            <h3 className="text-base font-black text-white">Macro Market & SAS Tool Demand</h3>
            <p className="text-xs text-blue-200 leading-relaxed">
              Explore city-wise average salaries (Delhi ₹14.9L, Bangalore ₹13.2L), recruiter volume (TCS, Accenture), and why SAS ranks #3 in analytical tool demand.
            </p>
          </div>
          <button
            onClick={() => navigate('/market-insights')}
            className="mt-4 w-fit px-4 py-2 rounded-xl bg-white text-blue-900 hover:bg-blue-50 font-black text-xs transition-all shadow-xs flex items-center gap-1.5"
          >
            <span>View Market Intelligence</span>
            <BarChart2 size={14} />
          </button>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Metrics & Visualizations */}
        <div className="lg:col-span-1 space-y-8">
          
          {/* Match Overview Card */}
          <div className="glass-card rounded-3xl p-7 border border-white/90 shadow-xl shadow-indigo-500/5">
            <h2 className="text-sm font-black text-slate-900 mb-4 flex items-center justify-between">
              <span className="flex items-center">
                <Target className="mr-2 text-indigo-600" size={17} /> Role Fit Score
              </span>
              <span className={`text-[10px] font-extrabold uppercase tracking-wider px-2.5 py-0.5 rounded-full border ${
                analysisData?.confidence_level === 'Exploratory' 
                  ? 'bg-amber-50 text-amber-700 border-amber-200' 
                  : 'bg-emerald-50 text-emerald-700 border-emerald-200'
              }`}>
                {analysisData?.confidence_level || 'Standard'} Confidence
              </span>
            </h2>

            <FitScoreGauge score={analysisData?.fit_score || 0} />
            
            <div className="mt-6 space-y-4 pt-4 border-t border-slate-100">
              <div>
                <div className="flex justify-between text-xs font-bold mb-1.5">
                  <span className="text-slate-600">Essential Skill Coverage</span>
                  <span className="text-emerald-600">{analysisData?.essential_coverage || 0}%</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                  <div 
                    className="bg-emerald-500 h-2.5 rounded-full transition-all duration-700" 
                    style={{ width: `${Math.min(100, analysisData?.essential_coverage || 0)}%` }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs font-bold mb-1.5">
                  <span className="text-slate-600">Optional Skill Coverage</span>
                  <span className="text-indigo-600">{analysisData?.optional_coverage || 0}%</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                  <div 
                    className="bg-indigo-500 h-2.5 rounded-full transition-all duration-700" 
                    style={{ width: `${Math.min(100, analysisData?.optional_coverage || 0)}%` }}
                  ></div>
                </div>
              </div>
            </div>
            
            <div className="mt-6 pt-4 border-t border-slate-100 grid grid-cols-3 text-center gap-2">
              <div className="bg-slate-50/80 p-3 rounded-2xl border border-slate-100">
                <p className="text-xl font-black text-emerald-600">{analysisData?.matched_count || 0}</p>
                <p className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider mt-0.5">Matched</p>
              </div>
              <div className="bg-slate-50/80 p-3 rounded-2xl border border-slate-100">
                <p className="text-xl font-black text-rose-500">{analysisData?.missing_essential?.length || 0}</p>
                <p className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider mt-0.5">Missing</p>
              </div>
              <div className="bg-slate-50/80 p-3 rounded-2xl border border-slate-100">
                <p className="text-xl font-black text-indigo-600">{analysisData?.surplus_skills?.length || 0}</p>
                <p className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider mt-0.5">Surplus</p>
              </div>
            </div>

            {analysisData?.predicted_salary && (
              <div className="mt-5 p-4 rounded-2xl bg-emerald-50/80 border border-emerald-200/80 text-xs text-emerald-900 shadow-2xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold flex items-center gap-1.5 text-emerald-800">
                    <IndianRupee size={14} className="text-emerald-600" /> ML Predicted CTC:
                  </span>
                  <span className="font-black text-xs text-emerald-950 bg-white px-3 py-1 rounded-xl border border-emerald-200 shadow-xs">
                    {analysisData.predicted_salary}
                  </span>
                </div>
                <p className="text-[10px] text-emerald-700/90 italic mt-2 leading-tight">
                  * {analysisData?.disclaimer || "Estimated market compensation reflects median hiring data for candidates clearing technical rounds and is not a guaranteed job offer."}
                </p>
              </div>
            )}
          </div>

          {/* Skill Radar Chart */}
          <div className="glass-card rounded-3xl p-7 border border-white/90 shadow-xl shadow-indigo-500/5">
            <h2 className="text-sm font-black text-slate-900 mb-1">Competency Radar</h2>
            <p className="text-xs text-slate-400 mb-4 font-medium">Domain overlap against role requirements</p>
            <SkillRadarChart 
              userSkills={effectiveSkills}
              roleEssential={currentRole.essential_skills || []}
              roleOptional={currentRole.optional_skills || []}
            />
          </div>

          {/* Top Recommendations Bar Chart */}
          <div className="glass-card rounded-3xl p-7 border border-white/90 shadow-xl shadow-indigo-500/5">
            <h2 className="text-sm font-black text-slate-900 mb-1">Market Role Rankings</h2>
            <p className="text-xs text-slate-400 mb-4 font-medium">Alternative careers matching your current profile</p>
            <RoleBarChart 
              recommendations={recommendations.map(r => ({
                role: r.role_title,
                score: r.score,
                role_id: r.role_id
              }))} 
            />
          </div>
        </div>

        {/* Right Column: Deep Analysis, Gap Breakdown & Learning Path */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* Explainability Panel */}
          <div className="glass-card rounded-3xl p-7 border border-indigo-100 bg-gradient-to-br from-indigo-50/60 via-white to-purple-50/40 shadow-xl shadow-indigo-500/5">
            <div className="flex items-start gap-4">
              <div className="p-3 rounded-2xl bg-indigo-600 text-white shadow-sm mt-0.5">
                <Sparkles size={20} />
              </div>
              <div className="space-y-2.5">
                <h2 className="text-lg font-black text-slate-900">Explainable AI Insights</h2>
                <p className="text-sm text-slate-600 leading-relaxed font-medium">
                  {analysisData?.why_this_role || "Our intelligence engine compared your skills with real Indian industry demand standards."}
                </p>
                <div className="flex flex-wrap items-center gap-4 pt-2 text-xs font-semibold">
                  <span className="flex items-center gap-1.5 text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-xl border border-emerald-100">
                    <CheckCircle2 size={13} className="text-emerald-600" />
                    Verified vs ESCO & Naukri 2025 data
                  </span>
                  <span className="flex items-center gap-1.5 text-indigo-700 bg-indigo-50 px-2.5 py-1 rounded-xl border border-indigo-100">
                    <Award size={13} className="text-indigo-600" />
                    NPTEL & Industry Credential Pathways
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Gap Breakdown Table */}
          <div className="glass-card rounded-3xl p-7 border border-white/90 shadow-xl shadow-indigo-500/5">
            <h2 className="text-lg font-black text-slate-900 mb-1">Detailed Skill Audit</h2>
            <p className="text-xs text-slate-400 mb-5 font-medium">
              Comprehensive breakdown of essential criteria, optional bonus skills, and transferable surplus
            </p>
            <GapTable 
              matchedSkills={analysisData?.matched_skills || []}
              missingEssential={analysisData?.missing_essential || []}
              missingOptional={analysisData?.missing_optional || []}
              surplusSkills={analysisData?.surplus_skills || []}
              skillVelocities={analysisData?.skill_velocities || []}
            />
          </div>

          {/* Week-by-Week Learning Roadmap */}
          <div className="glass-card rounded-3xl p-7 border border-white/90 shadow-xl shadow-indigo-500/5">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-lg font-black text-slate-900 flex items-center gap-2">
                  <BookOpen size={20} className="text-indigo-600" />
                  Personalized Learning Roadmap
                </h2>
                <p className="text-xs text-slate-400 mt-1 font-medium">
                  Week-by-week curriculum mapped to verified courses & real hands-on projects
                </p>
              </div>
              <span className="text-xs font-black px-3 py-1 rounded-xl bg-indigo-50 text-indigo-700 border border-indigo-200/70 shadow-2xs">
                {roadmap.length} Milestone Modules
              </span>
            </div>

            <RoadmapTimeline roadmap={roadmap} />
          </div>

        </div>
      </div>
    </div>
  );
};

export default Dashboard;
