import React from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import { usePrediction } from '../context/PredictionContext';
import { IconChart, IconImage, Spinner, TileHeader } from '../icons';

export function PreviewPage() {
  const navigate = useNavigate();
  const { patientId, file, previewUrl, error, loading, setError, runPrediction } =
    usePrediction();

  if (!patientId.trim() || !file) {
    return <Navigate to="/upload" replace />;
  }

  const onRun = async () => {
    setError(null);
    const ok = await runPrediction();
    if (ok) navigate('/results');
  };

  return (
    <section aria-labelledby="preview-heading" className="mx-auto max-w-xl">
      <h1 id="preview-heading" className="sr-only">
        Preview radiograph — BoneAgeX
      </h1>
      <div className="glass-card p-5 sm:p-6">
        <div className="glass-card-inner flex flex-col">
          <TileHeader
            step={2}
            title="Preview"
            desc="Confirm orientation and contrast, then run estimation."
            icon={IconImage}
          />

          <p className="mb-3 text-xs text-slate-500">
            Patient: <span className="font-semibold text-slate-800">{patientId.trim()}</span>
          </p>

          <div className="relative mb-6 flex min-h-[260px] items-center justify-center overflow-hidden rounded-xl border border-slate-200 bg-slate-50">
            {previewUrl ? (
              <img
                src={previewUrl}
                alt="Selected X-ray preview"
                className="max-h-[min(55vh,420px)] w-full object-contain"
              />
            ) : (
              <div className="flex flex-col items-center gap-2 px-6 py-10">
                <IconImage className="h-10 w-10 text-slate-400" />
                <p className="text-sm text-slate-500">No preview</p>
              </div>
            )}
          </div>

          <div className="flex flex-col gap-3 sm:flex-row sm:flex-wrap">
            <Link
              to="/upload"
              className="inline-flex items-center justify-center rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 shadow-sm transition-all duration-200 hover:border-slate-300 hover:bg-slate-50 hover:shadow"
            >
              ← Back to upload
            </Link>
            <button
              type="button"
              onClick={onRun}
              className="btn-primary flex-1 sm:min-w-[200px]"
              disabled={loading}
            >
              {loading ? (
                <>
                  <Spinner />
                  Running…
                </>
              ) : (
                <>
                  <IconChart className="h-4 w-4 opacity-95" />
                  Run bone age estimation
                </>
              )}
            </button>
          </div>

          {error && (
            <div
              className="mt-4 rounded-xl border border-red-200 bg-red-50 px-3 py-2.5 text-xs text-red-900"
              role="alert"
            >
              <span className="font-semibold text-red-800">Error — </span>
              {error}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
