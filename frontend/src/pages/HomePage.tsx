import React from 'react';
import { Link } from 'react-router-dom';
import { IconChart, IconImage, IconUpload } from '../icons';

const features = [
  {
    title: 'Dual-model analysis',
    body:
      'Dedicated male and female estimators reflect different skeletal maturation patterns—run both and compare ages in one session.',
    icon: IconChart
  },
  {
    title: 'Explainable outputs',
    body:
      'Grad-CAM overlays highlight regions that drive each prediction, alongside uncertainty (σ) for confidence context.',
    icon: IconImage
  },
  {
    title: 'Guided workflow',
    body:
      'Upload → preview → results. Patient IDs and stored runs support traceability for research or audit-friendly use.',
    icon: IconUpload
  }
] as const;

export function HomePage() {
  return (
    <div className="mx-auto max-w-4xl space-y-16 pb-8 lg:max-w-5xl">
      <section className="text-center sm:px-4">
        <p className="animate-landing-in opacity-0 text-xs font-semibold uppercase tracking-[0.2em] text-primary-700">
          BoneAgeX
        </p>
        <h1 className="animate-landing-in opacity-0 pt-3 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl lg:text-[2.5rem] lg:leading-tight [animation-delay:80ms]">
          Smarter bone age reads,
          <span className="bg-gradient-to-r from-primary-700 to-sky-600 bg-clip-text text-transparent">
            {' '}
            backed by dual AI models
          </span>
        </h1>
        <p className="animate-landing-in opacity-0 mx-auto mt-4 max-w-2xl text-base leading-relaxed text-slate-600 sm:text-lg [animation-delay:160ms]">
          Estimate skeletal maturity from hand–wrist X-rays with parallel male and female
          predictors, uncertainty scoring, and visual explainability—built for clinical research
          and supervised review.
        </p>
        <div className="animate-landing-in opacity-0 mt-8 flex justify-center [animation-delay:240ms]">
          <Link
            to="/upload"
            className="btn-primary shadow-primary-900/20 min-w-[200px] px-8 py-3 text-base transition-transform duration-300 hover:scale-[1.02] active:scale-[0.98]"
          >
            Start assessment
          </Link>
        </div>
      </section>

      <section className="sm:px-2">
        <h2 className="text-center text-sm font-semibold uppercase tracking-wider text-slate-500">
          Why teams use BoneAgeX
        </h2>
        <div className="mt-6 grid gap-4 sm:grid-cols-3">
          {features.map((f, i) => (
            <article
              key={f.title}
              style={{ animationDelay: `${320 + i * 100}ms` }}
              className="animate-landing-in opacity-0 group relative rounded-2xl border border-slate-200/90 bg-white p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-primary-200 hover:shadow-lg hover:shadow-primary-900/5"
            >
              <div className="mb-3 inline-flex rounded-xl bg-primary-50 p-2.5 text-primary-700 transition-transform duration-300 group-hover:scale-105">
                <f.icon className="h-5 w-5" />
              </div>
              <h3 className="text-sm font-semibold text-slate-900">{f.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600">{f.body}</p>
            </article>
          ))}
        </div>
      </section>

      <p className="animate-landing-in opacity-0 max-w-xl px-2 text-center text-xs leading-relaxed text-slate-500 [animation-delay:600ms] sm:mx-auto">
        BoneAgeX is intended for <strong className="font-medium text-slate-600">research</strong>{' '}
        and <strong className="font-medium text-slate-600">supervised clinical evaluation</strong>.
        Outputs support—not replace—professional interpretation.
      </p>
    </div>
  );
}
