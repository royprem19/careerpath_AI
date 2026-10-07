import React, { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import SkillTag from '../components/SkillTag';
import { 
  GraduationCap, 
  Briefcase, 
  Plus, 
  ArrowRight, 
  LayoutDashboard, 
  AlertCircle, 
  Sparkles, 
  CheckCircle2, 
  Trash2,
  Calendar,
  Building2,
  Award
} from 'lucide-react';

const ProfileReview = () => {
  const { userProfile, setUserProfile } = useAppContext();
  const navigate = useNavigate();
  const [newSkill, setNewSkill] = useState('');

  // Add education state
  const [showAddEdu, setShowAddEdu] = useState(false);
  const [newDegree, setNewDegree] = useState('');
  const [newInstitution, setNewInstitution] = useState('');
  const [newEduYear, setNewEduYear] = useState('');

  // Add experience state
  const [showAddExp, setShowAddExp] = useState(false);
  const [newRole, setNewRole] = useState('');
  const [newCompany, setNewCompany] = useState('');
  const [newExpDuration, setNewExpDuration] = useState('');
  const [newIsInternship, setNewIsInternship] = useState(false);

  // Normalize Education into array of structured objects
  const normalizedEducation = useMemo(() => {
    const raw = userProfile?.education;
    if (!raw) return [];
    const list = Array.isArray(raw) ? raw : [raw];
    return list.map(item => {
      if (!item) return null;
      if (typeof item === 'string') {
        return {
          degree: item,
          institution: 'Recognized Institution / University',
          year: ''
        };
      }
      return {
        degree: item.degree || item.name || item.title || 'Academic Degree',
        institution: item.institution || item.school || item.college || 'Higher Education Institution',
        year: item.year || item.duration || item.grade || ''
      };
    }).filter(Boolean);
  }, [userProfile?.education]);

  // Normalize Experience into array of structured objects
  const normalizedExperience = useMemo(() => {
    const raw = userProfile?.experience;
    if (!raw) return [];
    if (Array.isArray(raw)) {
      return raw.map(item => {
        if (!item) return null;
        if (typeof item === 'string') {
          return { role: item, company: 'Industry Organization', duration: '', years: 0.5, has_internship: item.toLowerCase().includes('intern') };
        }
        return {
          role: item.role || item.title || 'Professional Role',
          company: item.company || item.organization || 'Organization',
          duration: item.duration || (item.years ? `${item.years} year(s)` : ''),
          years: item.years || 0.5,
          has_internship: Boolean(item.has_internship || (item.role && item.role.toLowerCase().includes('intern')))
        };
      }).filter(Boolean);
    }
    if (typeof raw === 'object') {
      if (raw.role || raw.company || raw.title) {
        return [{
          role: raw.role || raw.title || 'Professional Role',
          company: raw.company || 'Organization',
          duration: raw.duration || (raw.years ? `${raw.years} year(s)` : ''),
          years: raw.years || 0.5,
          has_internship: Boolean(raw.has_internship || (raw.role && raw.role.toLowerCase().includes('intern')))
        }];
      }
      if (raw.years && Number(raw.years) > 0) {
        return [{
          role: 'Professional Experience',
          company: 'Industry / Engineering Domain',
          duration: `${raw.years} Year(s) Demonstrated Work`,
          years: raw.years,
          has_internship: false
        }];
      }
    }
    return [];
  }, [userProfile?.experience]);

  // Skill Management
  const handleRemoveSkill = (skillToRemove) => {
    setUserProfile({
      ...userProfile,
      skills: (userProfile.skills || []).filter(s => s !== skillToRemove)
    });
  };

  const handleAddSkill = (e) => {
    if (e.key === 'Enter' && newSkill.trim()) {
      e.preventDefault();
      if (!userProfile?.skills?.includes(newSkill.trim())) {
        setUserProfile({
          ...userProfile,
          skills: [...(userProfile?.skills || []), newSkill.trim()]
        });
      }
      setNewSkill('');
    }
  };

  const addManualSkill = () => {
    if (newSkill.trim() && !userProfile?.skills?.includes(newSkill.trim())) {
      setUserProfile({
        ...userProfile,
        skills: [...(userProfile?.skills || []), newSkill.trim()]
      });
      setNewSkill('');
    }
  };

  // Education Management
  const handleRemoveEducation = (index) => {
    const updated = normalizedEducation.filter((_, idx) => idx !== index);
    setUserProfile({
      ...userProfile,
      education: updated
    });
  };

  const handleAddEducation = (e) => {
    e.preventDefault();
    if (!newDegree.trim()) return;
    const newEntry = {
      degree: newDegree.trim(),
      institution: newInstitution.trim() || 'Recognized University / School',
      year: newEduYear.trim()
    };
    setUserProfile({
      ...userProfile,
      education: [...normalizedEducation, newEntry]
    });
    setNewDegree('');
    setNewInstitution('');
    setNewEduYear('');
    setShowAddEdu(false);
  };

  // Experience Management
  const handleRemoveExperience = (index) => {
    const updated = normalizedExperience.filter((_, idx) => idx !== index);
    setUserProfile({
      ...userProfile,
      experience: updated
    });
  };

  const handleAddExperience = (e) => {
    e.preventDefault();
    if (!newRole.trim()) return;
    const newEntry = {
      role: newRole.trim(),
      company: newCompany.trim() || 'Organization',
      duration: newExpDuration.trim(),
      years: newIsInternship ? 0.5 : 1.0,
      has_internship: newIsInternship || newRole.toLowerCase().includes('intern')
    };
    setUserProfile({
      ...userProfile,
      experience: [...normalizedExperience, newEntry]
    });
    setNewRole('');
    setNewCompany('');
    setNewExpDuration('');
    setNewIsInternship(false);
    setShowAddExp(false);
  };

  const hasFewSkills = (userProfile?.skills?.length || 0) < 3;
  const isZeroSkills = (userProfile?.skills?.length || 0) === 0;

  return (
    <div className="w-full max-w-6xl mx-auto px-4 sm:px-8 py-10">
      
      {/* Page Header */}
      <div className="mb-8">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-50 border border-indigo-200/80 text-indigo-700 text-xs font-bold uppercase tracking-wider mb-3 shadow-2xs">
          <Sparkles size={13} className="text-indigo-600" />
          <span>Candidate Profile Verification</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight mb-2">
          Review Extracted Profile
        </h1>
        <p className="text-slate-500 font-medium text-sm sm:text-base max-w-2xl">
          We've normalized your technical competencies, academic credentials, and work history. Verify or customize below to guarantee precision career matchmaking.
        </p>
      </div>

      {/* Uncertainty & Low-Confidence Guardrail Banner */}
      {(userProfile?.warning_message || hasFewSkills) && (
        <div className="p-5 rounded-3xl glass-card border-amber-200/80 bg-amber-50/70 flex items-start gap-3.5 text-amber-900 mb-8 shadow-xs">
          <AlertCircle size={22} className="shrink-0 text-amber-600 mt-0.5" />
          <div className="space-y-1.5 w-full">
            <div className="flex items-center justify-between">
              <p className="font-bold text-sm text-amber-950">
                {userProfile?.is_scanned_or_low_text 
                  ? "Scanned or Low-Text Document Detected" 
                  : "Low Confidence Skill Extraction"}
              </p>
              <span className="text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-amber-200/90 text-amber-900 border border-amber-300/60">
                Action Recommended
              </span>
            </div>
            <p className="text-xs text-amber-800 leading-relaxed font-medium">
              {userProfile?.warning_message || "We detected very few skills from your document. To prevent skewed role recommendations, please confirm or add your core skills below."}
            </p>
            <div className="pt-2 flex flex-wrap items-center gap-1.5">
              <span className="text-[11px] font-bold text-amber-900 mr-1">Quick Add Starters:</span>
              {['Python', 'JavaScript', 'SQL', 'HTML5', 'CSS3', 'React', 'Git & GitHub', 'Figma', 'Node.js', 'Docker', 'Power BI', 'Machine Learning'].map((starter) => (
                !userProfile?.skills?.includes(starter) && (
                  <button
                    key={starter}
                    type="button"
                    onClick={() => {
                      setUserProfile({
                        ...userProfile,
                        skills: [...(userProfile?.skills || []), starter]
                      });
                    }}
                    className="text-[11px] font-semibold px-2.5 py-1 rounded-xl bg-white/90 hover:bg-amber-100 border border-amber-300/80 text-amber-900 transition-colors shadow-2xs"
                  >
                    + {starter}
                  </button>
                )
              ))}
            </div>
          </div>
        </div>
      )}

      <div className="space-y-8">
        {/* Skills Section */}
        <div className="glass-card rounded-3xl p-7 sm:p-8 shadow-xl shadow-indigo-500/5 border border-white/90">
          <div className="flex items-center justify-between mb-5">
            <h2 className="text-xl font-black text-slate-900 flex items-center gap-2">
              <span>Your Technical Skills</span>
              <span className="bg-indigo-50 text-indigo-700 border border-indigo-200/80 text-xs font-bold py-0.5 px-2.5 rounded-full shadow-2xs">
                {userProfile?.skills?.length || 0} extracted
              </span>
            </h2>
            <span className="text-xs text-slate-400 font-medium hidden sm:inline-block">
              Click &times; on any tag to remove
            </span>
          </div>
          
          <div className="flex flex-wrap gap-2.5 mb-6 min-h-[50px] p-4 bg-slate-50/70 rounded-2xl border border-slate-200/70">
            {userProfile?.skills && userProfile.skills.length > 0 ? (
              userProfile.skills.map((skill, idx) => (
                <SkillTag 
                  key={idx} 
                  name={skill} 
                  removable 
                  onRemove={handleRemoveSkill} 
                  variant="default"
                />
              ))
            ) : (
              <p className="text-xs text-slate-400 italic py-2">No skills registered yet. Type below to add your primary proficiencies.</p>
            )}
          </div>
          
          <div className="flex items-center gap-3 max-w-lg">
            <div className="relative flex-1">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <Plus size={18} />
              </div>
              <input
                type="text"
                value={newSkill}
                onChange={(e) => setNewSkill(e.target.value)}
                onKeyDown={handleAddSkill}
                placeholder="Type a skill and press Enter..."
                className="pl-11 pr-4 py-3 bg-white/90 border border-slate-200/90 rounded-2xl focus:ring-2 focus:ring-indigo-400 focus:border-transparent outline-none text-sm transition-all shadow-2xs w-full text-slate-800 placeholder-slate-400"
              />
            </div>
            <button
              type="button"
              onClick={addManualSkill}
              className="px-5 py-3 rounded-2xl bg-indigo-50 border border-indigo-200 text-indigo-700 font-bold text-xs hover:bg-indigo-100 transition-colors shadow-2xs"
            >
              Add Skill
            </button>
          </div>
        </div>

        {/* Education & Experience Grid */}
        <div className="grid md:grid-cols-2 gap-8">
          
          {/* Education Card */}
          <div className="glass-card rounded-3xl p-7 sm:p-8 shadow-xl shadow-indigo-500/5 border border-white/90 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-5">
                <h2 className="text-lg font-black text-slate-900 flex items-center gap-2.5">
                  <div className="w-9 h-9 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center border border-indigo-100 shadow-2xs">
                    <GraduationCap size={18} />
                  </div>
                  <span>Education Background</span>
                  <span className="text-xs font-bold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded-full border border-indigo-100">
                    {normalizedEducation.length}
                  </span>
                </h2>
                <button
                  type="button"
                  onClick={() => setShowAddEdu(!showAddEdu)}
                  className="text-xs font-bold text-indigo-600 hover:text-indigo-800 flex items-center gap-1 transition-colors"
                >
                  <Plus size={14} />
                  {showAddEdu ? 'Cancel' : 'Add Degree'}
                </button>
              </div>

              {/* Add Education Form */}
              {showAddEdu && (
                <form onSubmit={handleAddEducation} className="p-4 mb-4 rounded-2xl bg-indigo-50/50 border border-indigo-200/70 space-y-3">
                  <p className="text-xs font-bold text-indigo-950">Add Qualification</p>
                  <div>
                    <input
                      type="text"
                      placeholder="Degree / Program (e.g. B.E. Computer Science)"
                      value={newDegree}
                      onChange={(e) => setNewDegree(e.target.value)}
                      className="w-full text-xs p-2.5 rounded-xl border border-slate-200 bg-white text-slate-800 focus:outline-none focus:ring-1 focus:ring-indigo-400"
                      required
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <input
                      type="text"
                      placeholder="Institution / University"
                      value={newInstitution}
                      onChange={(e) => setNewInstitution(e.target.value)}
                      className="text-xs p-2.5 rounded-xl border border-slate-200 bg-white text-slate-800 focus:outline-none focus:ring-1 focus:ring-indigo-400"
                    />
                    <input
                      type="text"
                      placeholder="Year / CGPA (e.g. 2024 - 2028 | 7.5)"
                      value={newEduYear}
                      onChange={(e) => setNewEduYear(e.target.value)}
                      className="text-xs p-2.5 rounded-xl border border-slate-200 bg-white text-slate-800 focus:outline-none focus:ring-1 focus:ring-indigo-400"
                    />
                  </div>
                  <button
                    type="submit"
                    className="w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition-all shadow-xs"
                  >
                    Save Qualification
                  </button>
                </form>
              )}

              {normalizedEducation.length > 0 ? (
                <ul className="space-y-3.5">
                  {normalizedEducation.map((edu, idx) => (
                    <li key={idx} className="p-4 rounded-2xl bg-slate-50/80 border border-slate-200/70 hover:border-indigo-200 transition-all flex items-start justify-between gap-3 group">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2 flex-wrap">
                          <p className="font-bold text-slate-900 text-sm">{edu.degree}</p>
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-indigo-100 text-indigo-700">
                            Verified
                          </span>
                        </div>
                        <p className="text-slate-600 text-xs font-medium flex items-center gap-1.5">
                          <Building2 size={13} className="text-slate-400" />
                          {edu.institution}
                        </p>
                        {edu.year && (
                          <p className="text-slate-500 text-[11px] font-semibold flex items-center gap-1.5 mt-0.5">
                            <Calendar size={12} className="text-slate-400" />
                            {edu.year}
                          </p>
                        )}
                      </div>
                      <button
                        type="button"
                        onClick={() => handleRemoveEducation(idx)}
                        className="opacity-60 hover:opacity-100 text-slate-400 hover:text-red-500 p-1.5 rounded-lg transition-colors"
                        title="Remove entry"
                      >
                        <Trash2 size={15} />
                      </button>
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="p-6 text-center rounded-2xl bg-slate-50/50 border border-dashed border-slate-200 text-slate-400 text-xs italic">
                  No academic degrees automatically detected. You may add qualifications above or proceed with skill benchmark analysis.
                </div>
              )}
            </div>
          </div>

          {/* Experience Card */}
          <div className="glass-card rounded-3xl p-7 sm:p-8 shadow-xl shadow-indigo-500/5 border border-white/90 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-5">
                <h2 className="text-lg font-black text-slate-900 flex items-center gap-2.5">
                  <div className="w-9 h-9 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center border border-purple-100 shadow-2xs">
                    <Briefcase size={18} />
                  </div>
                  <span>Professional Experience</span>
                  <span className="text-xs font-bold text-purple-700 bg-purple-50 px-2 py-0.5 rounded-full border border-purple-100">
                    {normalizedExperience.length}
                  </span>
                </h2>
                <button
                  type="button"
                  onClick={() => setShowAddExp(!showAddExp)}
                  className="text-xs font-bold text-purple-600 hover:text-purple-800 flex items-center gap-1 transition-colors"
                >
                  <Plus size={14} />
                  {showAddExp ? 'Cancel' : 'Add Experience'}
                </button>
              </div>

              {/* Add Experience Form */}
              {showAddExp && (
                <form onSubmit={handleAddExperience} className="p-4 mb-4 rounded-2xl bg-purple-50/50 border border-purple-200/70 space-y-3">
                  <p className="text-xs font-bold text-purple-950">Add Role / Internship</p>
                  <div>
                    <input
                      type="text"
                      placeholder="Role / Title (e.g. Data Analytics Intern)"
                      value={newRole}
                      onChange={(e) => setNewRole(e.target.value)}
                      className="w-full text-xs p-2.5 rounded-xl border border-slate-200 bg-white text-slate-800 focus:outline-none focus:ring-1 focus:ring-purple-400"
                      required
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <input
                      type="text"
                      placeholder="Company / Organization"
                      value={newCompany}
                      onChange={(e) => setNewCompany(e.target.value)}
                      className="text-xs p-2.5 rounded-xl border border-slate-200 bg-white text-slate-800 focus:outline-none focus:ring-1 focus:ring-purple-400"
                    />
                    <input
                      type="text"
                      placeholder="Duration (e.g. June 2026 - July 2026)"
                      value={newExpDuration}
                      onChange={(e) => setNewExpDuration(e.target.value)}
                      className="text-xs p-2.5 rounded-xl border border-slate-200 bg-white text-slate-800 focus:outline-none focus:ring-1 focus:ring-purple-400"
                    />
                  </div>
                  <div className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      id="isInternship"
                      checked={newIsInternship}
                      onChange={(e) => setNewIsInternship(e.target.checked)}
                      className="rounded text-purple-600 focus:ring-purple-400"
                    />
                    <label htmlFor="isInternship" className="text-xs font-medium text-purple-900 cursor-pointer">
                      This is an Internship / Practical Training
                    </label>
                  </div>
                  <button
                    type="submit"
                    className="w-full py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-xl text-xs font-bold transition-all shadow-xs"
                  >
                    Save Experience
                  </button>
                </form>
              )}

              {normalizedExperience.length > 0 ? (
                <ul className="space-y-3.5">
                  {normalizedExperience.map((exp, idx) => (
                    <li key={idx} className="p-4 rounded-2xl bg-slate-50/80 border border-slate-200/70 hover:border-purple-200 transition-all flex items-start justify-between gap-3 group">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2 flex-wrap">
                          <p className="font-bold text-slate-900 text-sm">{exp.role}</p>
                          {exp.has_internship ? (
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-purple-100 text-purple-700 border border-purple-200">
                              Internship
                            </span>
                          ) : (
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-700 border border-emerald-200">
                              Industry Track
                            </span>
                          )}
                        </div>
                        <p className="text-slate-600 text-xs font-medium flex items-center gap-1.5">
                          <Building2 size={13} className="text-slate-400" />
                          {exp.company}
                        </p>
                        {exp.duration && (
                          <p className="text-slate-500 text-[11px] font-semibold flex items-center gap-1.5 mt-0.5">
                            <Calendar size={12} className="text-slate-400" />
                            {exp.duration}
                          </p>
                        )}
                      </div>
                      <button
                        type="button"
                        onClick={() => handleRemoveExperience(idx)}
                        className="opacity-60 hover:opacity-100 text-slate-400 hover:text-red-500 p-1.5 rounded-lg transition-colors"
                        title="Remove entry"
                      >
                        <Trash2 size={15} />
                      </button>
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="p-6 text-center rounded-2xl bg-slate-50/50 border border-dashed border-slate-200 text-slate-400 text-xs italic">
                  No previous employment history detected. Career recommendations will calibrate for early-career & foundational entry points.
                </div>
              )}
            </div>
          </div>

        </div>

        {/* Action Controls */}
        <div className="flex flex-col sm:flex-row gap-4 pt-4">
          <button
            onClick={() => {
              if (isZeroSkills) {
                alert('Please add or select at least 1-2 skills so we can calculate meaningful career matches.');
                return;
              }
              navigate('/roles');
            }}
            disabled={isZeroSkills}
            className={`flex-1 py-4 px-6 rounded-2xl flex items-center justify-center font-bold text-sm transition-all shadow-md ${
              isZeroSkills 
                ? 'bg-slate-200 text-slate-400 cursor-not-allowed shadow-none' 
                : 'bg-slate-900 hover:bg-slate-800 text-white shadow-slate-900/10 hover:shadow-xl hover:scale-[1.01]'
            }`}
          >
            Continue to Role Selection <ArrowRight className="ml-2" size={18} />
          </button>
          
          <button
            onClick={() => {
              if (isZeroSkills) {
                alert('Please add or select at least 1-2 skills so we can evaluate role alignments.');
                return;
              }
              navigate('/dashboard');
            }}
            disabled={isZeroSkills}
            className={`flex-1 py-4 px-6 rounded-2xl flex items-center justify-center font-bold text-sm transition-all shadow-2xs ${
              isZeroSkills
                ? 'bg-slate-100 text-slate-400 border border-slate-200 cursor-not-allowed'
                : 'border-2 border-indigo-300 hover:border-indigo-400 text-indigo-700 bg-white hover:bg-indigo-50/60'
            }`}
          >
            <LayoutDashboard className="mr-2" size={18} /> Analyze All Roles Directly
          </button>
        </div>

      </div>
    </div>
  );
};

export default ProfileReview;
