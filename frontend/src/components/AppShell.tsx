import React from 'react';
import { Link, NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom';
import { usePrediction } from '../context/PredictionContext';

const navClass = ({ isActive }: { isActive: boolean }) =>
  [
    'rounded-lg px-3 py-2 text-xs font-medium transition-all duration-200',
    isActive
      ? 'bg-primary-100 text-primary-800 ring-1 ring-primary-200/80 shadow-sm'
      : 'text-slate-600 hover:bg-white hover:text-slate-900 hover:shadow-sm'
  ].join(' ');

export function AppShell() {
  const { resetSession } = usePrediction();
  const navigate = useNavigate();
  const location = useLocation();

  const onNewCase = () => {
    resetSession();
    navigate('/upload', { replace: true });
  };

  return (
    <div className="relative min-h-screen overflow-x-hidden text-slate-800">
      <div className="pointer-events-none fixed inset-0 app-bg-grid" aria-hidden />
      <div
        className="pointer-events-none fixed inset-0 bg-gradient-to-b from-slate-100 via-sky-50/40 to-slate-100"
        aria-hidden
      />
      <div
        className="pointer-events-none fixed -left-32 top-24 h-72 w-72 rounded-full bg-primary-400/15 blur-3xl"
        aria-hidden
      />
      <div
        className="pointer-events-none fixed -right-24 bottom-16 h-80 w-80 rounded-full bg-sky-300/20 blur-3xl"
        aria-hidden
      />

      <div className="relative">
        <header className="sticky top-0 z-20 border-b border-slate-200/90 bg-white/90 shadow-sm backdrop-blur-md transition-shadow duration-300">
          <div className="mx-auto flex max-w-3xl flex-col gap-4 px-4 py-3.5 sm:max-w-6xl sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
            <Link
              to="/"
              className="flex items-center gap-3 rounded-lg outline-none ring-primary-500/0 transition-all duration-200 hover:opacity-90 focus-visible:ring-2"
            >
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-primary-600 to-primary-700 text-white shadow-md shadow-primary-900/20 transition-transform duration-200 hover:scale-105">
                <span className="text-xs font-bold tracking-tight">BX</span>
              </div>
              <div>
                <p className="text-sm font-semibold tracking-tight text-slate-900">BoneAgeX</p>
                <p className="text-xs text-slate-500">Clinical bone age assessment</p>
              </div>
            </Link>

            <nav
              className="flex flex-wrap items-center gap-1 sm:justify-end"
              aria-label="Main navigation"
            >
              <NavLink to="/" end className={navClass}>
                Home
              </NavLink>
              <NavLink to="/upload" className={navClass}>
                Upload
              </NavLink>
              <NavLink to="/preview" className={navClass}>
                Preview
              </NavLink>
              <NavLink to="/results" className={navClass}>
                Results
              </NavLink>
              <NavLink to="/last" className={navClass}>
                Last investigation
              </NavLink>
              <button
                type="button"
                onClick={onNewCase}
                className="ml-1 rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-medium text-slate-600 shadow-sm transition-all duration-200 hover:border-primary-200 hover:bg-primary-50/50 hover:text-primary-900 hover:shadow"
              >
                New case
              </button>
            </nav>
          </div>
        </header>

        <main className="mx-auto max-w-3xl px-4 py-8 sm:max-w-6xl sm:px-6 lg:px-8 lg:py-10">
          <div key={location.pathname} className="animate-page-in">
            <Outlet />
          </div>
        </main>

        <footer className="border-t border-slate-200/90 bg-white/50 py-6 text-center transition-colors duration-300">
          <p className="text-[11px] text-slate-500">BoneAgeX — for research and clinical evaluation</p>
        </footer>
      </div>
    </div>
  );
}
