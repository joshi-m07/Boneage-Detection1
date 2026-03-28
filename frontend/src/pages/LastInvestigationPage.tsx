import React from 'react';
import { Link } from 'react-router-dom';
import { IconChart } from '../icons';
import { loadLastInvestigation } from '../lib/lastInvestigation';
import { ResultsView } from '../components/ResultsView';

export function LastInvestigationPage() {
  const saved = loadLastInvestigation();

  return (
    <section aria-labelledby="last-heading" className="mx-auto max-w-4xl">
      <h1 id="last-heading" className="sr-only">
        Last investigation
      </h1>
      <div className="glass-card p-5 sm:p-6">
        <div className="glass-card-inner">
          <div className="mb-6 flex gap-3">
            <div className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-primary-100 text-primary-700">
              <IconChart className="h-4 w-4" />
            </div>
            <div className="min-w-0">
              <h2 className="tile-title text-base">Last investigation</h2>
              <p className="tile-desc mt-1">
                Most recently completed case in this browser—patient, ages, and Grad-CAM maps.
              </p>
            </div>
          </div>

          {!saved && (
            <div className="flex min-h-[220px] flex-col items-center justify-center rounded-xl border border-dashed border-slate-300 bg-slate-50/80 px-4 py-10 text-center">
              <IconChart className="mb-3 h-10 w-10 text-slate-400" />
              <p className="text-sm font-medium text-slate-600">No saved investigation yet</p>
              <p className="mt-2 max-w-sm text-xs text-slate-500">
                Run an estimation from Upload → Preview. Results are saved here automatically.
              </p>
              <Link
                to="/upload"
                className="mt-6 text-sm font-semibold text-primary-700 transition-colors hover:text-primary-900"
              >
                Start upload →
              </Link>
            </div>
          )}

          {saved && (
            <ResultsView
              result={saved.result}
              banner={
                <div className="animate-fade-in-up rounded-xl border border-primary-100 bg-primary-50/80 px-4 py-3 text-sm text-primary-900">
                  <p className="font-medium">Saved in this browser</p>
                  <p className="mt-0.5 text-xs text-primary-800/80">
                    Patient <span className="font-semibold">{saved.patientId}</span> · stored{' '}
                    {new Date(saved.savedAt).toLocaleString()}
                  </p>
                </div>
              }
            />
          )}
        </div>
      </div>
    </section>
  );
}
