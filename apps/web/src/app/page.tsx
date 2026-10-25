"use client";

import React, { useState } from "react";
import { Mic, Activity, CheckCircle, Database } from "lucide-react";

export default function ClinicalPortal() {
  const [recording, setRecording] = useState(false);
  const [biomarkers, setBiomarkers] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const simulateAnalysis = () => {
    setLoading(true);
    setTimeout(() => {
      setBiomarkers({
        f0_hz: 131.2,
        jitter_pct: 0.38,
        shimmer_pct: 1.84,
        hnr_db: 24.6,
        diagnostic: "Función glótica dentro de parámetros de normalidad",
      });
      setLoading(false);
    }, 1200);
  };

  return (
    <main className="min-h-screen p-8 max-w-6xl mx-auto">
      <header className="flex justify-between items-center border-b border-slate-800 pb-6 mb-8">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-sky-400">ClofoVoz HealTech AI</h1>
          <p className="text-sm text-slate-400">Sistema de Evaluación Acústica y Rehabilitación Vocal</p>
        </div>
        <div className="flex items-center gap-3 bg-slate-900 border border-slate-800 px-4 py-2 rounded-lg text-xs">
          <Database className="w-4 h-4 text-emerald-400" />
          <span>PostgreSQL & Worker AI: <strong className="text-emerald-400">Conectados</strong></span>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <section className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col justify-between">
          <div>
            <h2 className="text-lg font-semibold mb-2 flex items-center gap-2">
              <Mic className="w-5 h-5 text-sky-400" /> Captura Vocal
            </h2>
            <p className="text-sm text-slate-400 mb-6">
              Emisión de vocal sostenida /a/ a tono e intensidad confortables.
            </p>
          </div>

          <button
            onClick={simulateAnalysis}
            disabled={loading}
            className="w-full py-3 bg-sky-600 hover:bg-sky-500 rounded-lg font-medium transition flex items-center justify-center gap-2"
          >
            <Activity className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            {loading ? "Analizando en Hetzner..." : "Iniciar Muestra Vocal"}
          </button>
        </section>

        <section className="md:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <CheckCircle className="w-5 h-5 text-emerald-400" /> Panel de Biomarcadores Acústicos
          </h2>

          {biomarkers ? (
            <div className="space-y-6">
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                  <span className="text-xs text-slate-400">Frecuencia Fundamental (F0)</span>
                  <p className="text-2xl font-bold text-sky-400">{biomarkers.f0_hz} Hz</p>
                </div>
                <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                  <span className="text-xs text-slate-400">Jitter (Perturbación F0)</span>
                  <p className="text-2xl font-bold text-amber-400">{biomarkers.jitter_pct}%</p>
                </div>
                <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                  <span className="text-xs text-slate-400">Shimmer (Amplitud)</span>
                  <p className="text-2xl font-bold text-emerald-400">{biomarkers.shimmer_pct}%</p>
                </div>
                <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                  <span className="text-xs text-slate-400">HNR (Armónicos/Ruido)</span>
                  <p className="text-2xl font-bold text-purple-400">{biomarkers.hnr_db} dB</p>
                </div>
              </div>

              <div className="bg-slate-950/60 p-4 rounded-lg border border-slate-800 text-sm">
                <strong className="text-sky-400">Observación Clínica Preliminar:</strong> {biomarkers.diagnostic}
              </div>
            </div>
          ) : (
            <div className="h-44 flex items-center justify-center border border-dashed border-slate-800 rounded-lg text-slate-500 text-sm">
              Inicia una muestra vocal para visualizar los índices acústicos de Parselmouth.
            </div>
          )}
        </section>
      </div>
    </main>
  );
}