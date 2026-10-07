import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { 
  LogIn, LogOut, Sparkles, Menu, X, Home, 
  HelpCircle, Briefcase, LayoutDashboard, User, Info,
  TrendingUp, BarChart2 
} from 'lucide-react';

const Navbar = () => {
  const { currentUser, logout } = useAppContext();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Close mobile menu on page navigation
  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location.pathname]);

  const handleLogout = () => {
    logout();
    setMobileMenuOpen(false);
    navigate('/');
  };

  const isNavActive = (path) => {
    return location.pathname === path;
  };

  const handleHowItWorksClick = (e) => {
    setMobileMenuOpen(false);
    if (window.location.pathname === '/') {
      e.preventDefault();
      document.getElementById('how-it-works')?.scrollIntoView({ behavior: 'smooth' });
    } else {
      navigate('/#how-it-works');
    }
  };

  return (
    <nav className="bg-white/90 backdrop-blur-md border-b border-indigo-100/70 sticky top-0 z-50 transition-all">
      <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16">
        <div className="flex justify-between h-16 items-center">
          
          {/* Brand Logo with Sparkle */}
          <div className="flex items-center shrink-0">
            <Link to="/" className="flex items-center group whitespace-nowrap">
              <span className="text-xl sm:text-2xl font-black bg-clip-text text-transparent bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 tracking-tight">
                CareerPath AI
              </span>
              <Sparkles size={16} className="text-purple-500 ml-1 -mt-3.5 fill-purple-400/30 group-hover:rotate-12 transition-transform duration-300 shrink-0" />
            </Link>
          </div>

          {/* Desktop Navigation Links (Hidden on mobile) */}
          <div className="hidden md:flex items-center space-x-2 sm:space-x-3">
            <Link 
              to="/" 
              className={`text-sm px-3.5 py-1.5 rounded-full transition-all duration-200 ${
                isNavActive('/') 
                  ? 'bg-indigo-50/90 text-indigo-700 font-bold border border-indigo-100/80 shadow-2xs' 
                  : 'text-slate-600 hover:text-indigo-600 font-medium hover:bg-slate-100/60'
              }`}
            >
              Home
            </Link>

            <Link 
              to="/about" 
              className={`text-sm px-3.5 py-1.5 rounded-full transition-all duration-200 ${
                isNavActive('/about') 
                  ? 'bg-indigo-50/90 text-indigo-700 font-bold border border-indigo-100/80 shadow-2xs' 
                  : 'text-slate-600 hover:text-indigo-600 font-medium hover:bg-slate-100/60'
              }`}
            >
              About
            </Link>
            
            <a 
              href="#how-it-works"
              onClick={handleHowItWorksClick}
              className="text-slate-600 hover:text-indigo-600 text-sm font-medium px-3.5 py-1.5 rounded-full hover:bg-slate-100/60 transition-colors cursor-pointer"
            >
              How It Works
            </a>

            <Link 
              to="/roles" 
              className={`text-sm px-3.5 py-1.5 rounded-full transition-all duration-200 ${
                isNavActive('/roles') 
                  ? 'bg-indigo-50/90 text-indigo-700 font-bold border border-indigo-100/80 shadow-2xs' 
                  : 'text-slate-600 hover:text-indigo-600 font-medium hover:bg-slate-100/60'
              }`}
            >
              Roles
            </Link>

            <Link 
              to="/dashboard" 
              className={`text-sm px-3.5 py-1.5 rounded-full transition-all duration-200 ${
                isNavActive('/dashboard') 
                  ? 'bg-indigo-50/90 text-indigo-700 font-bold border border-indigo-100/80 shadow-2xs' 
                  : 'text-slate-600 hover:text-indigo-600 font-medium hover:bg-slate-100/60'
              }`}
            >
              Dashboard
            </Link>

            <Link 
              to="/career-growth" 
              className={`text-sm px-3.5 py-1.5 rounded-full transition-all duration-200 ${
                isNavActive('/career-growth') 
                  ? 'bg-indigo-50/90 text-indigo-700 font-bold border border-indigo-100/80 shadow-2xs' 
                  : 'text-slate-600 hover:text-indigo-600 font-medium hover:bg-slate-100/60'
              }`}
            >
              Growth AI
            </Link>

            <Link 
              to="/market-insights" 
              className={`text-sm px-3.5 py-1.5 rounded-full transition-all duration-200 ${
                isNavActive('/market-insights') 
                  ? 'bg-indigo-50/90 text-indigo-700 font-bold border border-indigo-100/80 shadow-2xs' 
                  : 'text-slate-600 hover:text-indigo-600 font-medium hover:bg-slate-100/60'
              }`}
            >
              Market Insights
            </Link>

            {/* Desktop Auth State Button */}
            {currentUser ? (
              <div className="flex items-center space-x-3 pl-3 sm:pl-4 border-l border-slate-200/80">
                <Link
                  to="/my-profile"
                  className="flex items-center gap-2 group px-1 py-1 rounded-xl hover:bg-slate-100/50 transition-colors"
                  title="View and Edit Profile"
                >
                  <div className="w-8 h-8 rounded-full bg-slate-900 text-white font-black text-xs flex items-center justify-center shadow-xs ring-2 ring-indigo-100">
                    {currentUser.user_name ? currentUser.user_name.charAt(0).toUpperCase() : 'U'}
                  </div>
                  <div className="hidden lg:flex flex-col text-left">
                    <span className="text-xs font-bold text-slate-800 group-hover:text-indigo-600 leading-tight">
                      {currentUser.user_name}
                    </span>
                    <span className="text-[10px] text-slate-400 font-medium">
                      My Profile
                    </span>
                  </div>
                </Link>

                <button
                  onClick={handleLogout}
                  className="flex items-center gap-1 px-3 py-1.5 text-xs font-bold text-slate-700 hover:text-slate-900 bg-white hover:bg-slate-50 rounded-xl border border-slate-200 shadow-2xs transition-colors"
                  title="Sign out of account"
                >
                  <LogOut size={13} className="text-slate-500" />
                  <span>Sign Out</span>
                </button>
              </div>
            ) : (
              <div className="pl-3 sm:pl-4 border-l border-slate-200/80">
                <Link
                  to="/auth"
                  className="flex items-center gap-1.5 px-4 py-2 text-xs font-bold text-white bg-slate-900 hover:bg-slate-800 rounded-xl shadow-xs transition-all hover:scale-[1.02]"
                >
                  <LogIn size={13} />
                  <span>Sign In</span>
                </Link>
              </div>
            )}

          </div>

          {/* Mobile Right Controls: Avatar + Hamburger Button */}
          <div className="flex items-center gap-2 md:hidden">
            {currentUser && (
              <Link
                to="/my-profile"
                className="w-8 h-8 rounded-full bg-slate-900 text-white font-black text-xs flex items-center justify-center shadow-xs ring-2 ring-indigo-100 shrink-0"
                title="My Profile"
              >
                {currentUser.user_name ? currentUser.user_name.charAt(0).toUpperCase() : 'U'}
              </Link>
            )}

            <button
              type="button"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-xl text-slate-700 hover:text-slate-900 hover:bg-slate-100/80 transition-colors focus:outline-none"
              aria-label="Toggle Navigation Menu"
            >
              {mobileMenuOpen ? <X size={22} /> : <Menu size={22} />}
            </button>
          </div>

        </div>
      </div>

      {/* Mobile Drawer Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden px-4 pt-2 pb-6 border-t border-indigo-100/70 bg-white/95 backdrop-blur-lg shadow-xl space-y-2 animate-in fade-in slide-in-from-top-2 duration-200">
          <Link
            to="/"
            onClick={() => setMobileMenuOpen(false)}
            className={`flex items-center gap-2.5 px-4 py-3 rounded-2xl text-sm font-bold transition-colors ${
              isNavActive('/')
                ? 'bg-indigo-50 text-indigo-700 border border-indigo-200/80 shadow-2xs'
                : 'text-slate-700 hover:bg-slate-50'
            }`}
          >
            <Home size={17} className={isNavActive('/') ? 'text-indigo-600' : 'text-slate-400'} />
            <span>Home</span>
          </Link>

          <Link
            to="/about"
            onClick={() => setMobileMenuOpen(false)}
            className={`flex items-center gap-2.5 px-4 py-3 rounded-2xl text-sm font-bold transition-colors ${
              isNavActive('/about')
                ? 'bg-indigo-50 text-indigo-700 border border-indigo-200/80 shadow-2xs'
                : 'text-slate-700 hover:bg-slate-50'
            }`}
          >
            <Info size={17} className={isNavActive('/about') ? 'text-indigo-600' : 'text-slate-400'} />
            <span>About</span>
          </Link>

          <a
            href="#how-it-works"
            onClick={handleHowItWorksClick}
            className="flex items-center gap-2.5 px-4 py-3 rounded-2xl text-sm font-bold text-slate-700 hover:bg-slate-50 transition-colors"
          >
            <HelpCircle size={17} className="text-slate-400" />
            <span>How It Works</span>
          </a>

          <Link
            to="/roles"
            onClick={() => setMobileMenuOpen(false)}
            className={`flex items-center gap-2.5 px-4 py-3 rounded-2xl text-sm font-bold transition-colors ${
              isNavActive('/roles')
                ? 'bg-indigo-50 text-indigo-700 border border-indigo-200/80 shadow-2xs'
                : 'text-slate-700 hover:bg-slate-50'
            }`}
          >
            <Briefcase size={17} className={isNavActive('/roles') ? 'text-indigo-600' : 'text-slate-400'} />
            <span>Browse Roles</span>
          </Link>

          <Link
            to="/dashboard"
            onClick={() => setMobileMenuOpen(false)}
            className={`flex items-center gap-2.5 px-4 py-3 rounded-2xl text-sm font-bold transition-colors ${
              isNavActive('/dashboard')
                ? 'bg-indigo-50 text-indigo-700 border border-indigo-200/80 shadow-2xs'
                : 'text-slate-700 hover:bg-slate-50'
            }`}
          >
            <LayoutDashboard size={17} className={isNavActive('/dashboard') ? 'text-indigo-600' : 'text-slate-400'} />
            <span>Dashboard</span>
          </Link>

          <Link
            to="/career-growth"
            onClick={() => setMobileMenuOpen(false)}
            className={`flex items-center gap-2.5 px-4 py-3 rounded-2xl text-sm font-bold transition-colors ${
              isNavActive('/career-growth')
                ? 'bg-indigo-50 text-indigo-700 border border-indigo-200/80 shadow-2xs'
                : 'text-slate-700 hover:bg-slate-50'
            }`}
          >
            <TrendingUp size={17} className={isNavActive('/career-growth') ? 'text-indigo-600' : 'text-slate-400'} />
            <span>Growth AI (Promotion & Leadership)</span>
          </Link>

          <Link
            to="/market-insights"
            onClick={() => setMobileMenuOpen(false)}
            className={`flex items-center gap-2.5 px-4 py-3 rounded-2xl text-sm font-bold transition-colors ${
              isNavActive('/market-insights')
                ? 'bg-indigo-50 text-indigo-700 border border-indigo-200/80 shadow-2xs'
                : 'text-slate-700 hover:bg-slate-50'
            }`}
          >
            <BarChart2 size={17} className={isNavActive('/market-insights') ? 'text-indigo-600' : 'text-slate-400'} />
            <span>Market Insights (17k+ Jobs)</span>
          </Link>

          {/* User Auth Section in Mobile Menu */}
          <div className="pt-3 mt-2 border-t border-slate-100">
            {currentUser ? (
              <div className="space-y-2">
                <div className="px-4 py-2 rounded-2xl bg-slate-50 border border-slate-200/60 flex items-center justify-between">
                  <div className="min-w-0 pr-2">
                    <p className="text-xs font-black text-slate-900 truncate">{currentUser.user_name}</p>
                    <p className="text-[11px] text-slate-500 truncate">{currentUser.email}</p>
                  </div>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 shrink-0">
                    Active
                  </span>
                </div>

                <Link
                  to="/my-profile"
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center gap-2.5 px-4 py-2.5 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 transition-colors"
                >
                  <User size={15} className="text-slate-400" />
                  <span>My Profile</span>
                </Link>

                <button
                  type="button"
                  onClick={handleLogout}
                  className="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-2xl text-xs font-bold text-rose-700 bg-rose-50 border border-rose-200 hover:bg-rose-100 transition-colors"
                >
                  <LogOut size={15} />
                  <span>Sign Out</span>
                </button>
              </div>
            ) : (
              <Link
                to="/auth"
                onClick={() => setMobileMenuOpen(false)}
                className="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-2xl text-xs font-bold text-white bg-slate-900 hover:bg-slate-800 shadow-md transition-all"
              >
                <LogIn size={15} />
                <span>Sign In / Create Account</span>
              </Link>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
