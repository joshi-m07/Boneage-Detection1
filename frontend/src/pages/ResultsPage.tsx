import React from 'react';
import { Link } from 'react-router-dom';
import { usePrediction } from '../context/PredictionContext';
import { IconChart, TileHeader } from '../icons';
import { ResultsView } from '../components/ResultsView';

export function ResultsPage() {
  const { result, file, patientId } = usePrediction();

  return (
    <section aria-labelledby="results-heading" className="mx-auto max-w-4xl">
      <h1 id="results-heading" className="sr-only">
        Estimation results
      </h1>
      <div className="glass-card p-5 sm:p-6">
        <div className="glass-card-inner">
          <div className="mb-6">
            <TileHeader
              className="!mb-0"
              step={3}
              title="Results"
              desc="Review dual-model bone age estimates and attention maps."
              icon={IconChart}
            />
          </div>

          {!result && (
            <div className="flex min-h-[220px] flex-col items-center justify-center rounded-xl border border-dashed border-slate-300 bg-slate-50/80 px-4 py-10 text-center">
              <IconChart className="mb-3 h-10 w-10 text-slate-400" />
              <p className="text-sm font-medium text-slate-600">No results yet</p>
              <p className="mt-2 max-w-sm text-xs text-slate-500">
                Run estimation from preview to view male and female predictions here.
              </p>
              <div className="mt-6 flex flex-wrap justify-center gap-3 text-xs">
                <Link
                  to="/upload"
                  className="font-semibold text-primary-700 transition-colors duration-200 hover:text-primary-900"
                >
                  Go to upload
                </Link>
                {file && patientId.trim() && (
                  <>
                    <span className="text-slate-300">·</span>
                    <Link
                      to="/preview"
                      className="font-semibold text-primary-700 transition-colors duration-200 hover:text-primary-900"
                    >
                      Go to preview
                    </Link>
                  </>
                )}
              </div>
            </div>
          )}

          {result && <ResultsView result={result} />}
        </div>
      </div>
    </section>
  );
}
