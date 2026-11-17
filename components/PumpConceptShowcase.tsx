"use client"

import React, { useState, useEffect } from "react"
import { Play, Pause, Activity, Zap, CheckCircle2, Sliders, ShieldCheck, Gauge, Layers, RotateCw } from "lucide-react"

export function PumpConceptShowcase() {
  const [equipmentType, setEquipmentType] = useState<"pumps" | "valves">("valves")
  const [activePumpConcept, setActivePumpConcept] = useState<number>(1)
  const [activeValveConcept, setActiveValveConcept] = useState<number>(1)
  const [isPlaying, setIsPlaying] = useState<boolean>(true)
  const [speed, setSpeed] = useState<number>(1)

  // Pump prototype states
  const [pumpStates, setPumpStates] = useState<Record<string, boolean>>({
    c1: true,
    c2: true,
    c3a: true,
    c3b: true,
    c4: true,
  })

  // Valve prototype states
  const [valveStates, setValveStates] = useState<Record<string, boolean>>({
    v1: true, // Solenoid / Angle Seat (Open/Closed)
    v2: true, // Butterfly (Open/Closed)
    v3: true, // Multiport (true = Service, false = Backwash)
  })

  // Regulating valve aperture % (Concept 4)
  const [valveAperture, setValveAperture] = useState<number>(75)

  // Simulated micro-telemetry jitter
  const [telemetry, setTelemetry] = useState({
    rpm: 1450,
    powerKw: 4.2,
    loadPct: 76,
    flowRate: 18.5,
    tempC: 42.4,
    pressureDelta: 0.12,
  })

  useEffect(() => {
    if (!isPlaying) return
    const interval = setInterval(() => {
      setTelemetry((prev) => ({
        rpm: Math.round(1440 + Math.random() * 20),
        powerKw: parseFloat((4.1 + Math.random() * 0.2).toFixed(2)),
        loadPct: Math.round(74 + Math.random() * 4),
        flowRate: parseFloat((18.2 + Math.random() * 0.6).toFixed(1)),
        tempC: parseFloat((42.0 + Math.random() * 0.8).toFixed(1)),
        pressureDelta: parseFloat((0.11 + Math.random() * 0.03).toFixed(2)),
      }))
    }, 1200)
    return () => clearInterval(interval)
  }, [isPlaying])

  const togglePump = (id: string) => {
    setPumpStates((prev) => ({ ...prev, [id]: !prev[id] }))
  }

  const toggleValve = (id: string) => {
    setValveStates((prev) => ({ ...prev, [id]: !prev[id] }))
  }

  return (
    <div className="w-full mt-6 bg-white rounded-2xl border border-sky-200/90 shadow-xl overflow-hidden font-sans select-none text-slate-900">
      {/* Header */}
      <div className="px-5 py-4 bg-gradient-to-r from-sky-900 via-slate-900 to-sky-950 text-white flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-sky-500/20 text-sky-300 border border-sky-400/30">
              PROTOTYPE LAB
            </span>
            <span className="font-mono text-sm font-black tracking-wider uppercase text-white">
              Next-Gen SCADA Equipment Prototypes
            </span>
          </div>
          <p className="text-xs text-sky-200/80 font-mono mt-0.5">
            Interactive side-by-side design concepts for Nanneer Global SCADA System
          </p>
        </div>

        {/* Global Controls & Equipment Switcher */}
        <div className="flex items-center gap-3 flex-wrap">
          {/* Equipment Category Toggle */}
          <div className="flex items-center bg-white/10 rounded-lg p-1 border border-white/20 text-xs font-mono font-bold">
            <button
              onClick={() => setEquipmentType("pumps")}
              className={`px-3 py-1 rounded-md transition-all ${
                equipmentType === "pumps" ? "bg-sky-500 text-white shadow-xs" : "text-sky-200 hover:text-white"
              }`}
            >
              PUMP CONCEPTS (4)
            </button>
            <button
              onClick={() => setEquipmentType("valves")}
              className={`px-3 py-1 rounded-md transition-all ${
                equipmentType === "valves" ? "bg-sky-500 text-white shadow-xs" : "text-sky-200 hover:text-white"
              }`}
            >
              VALVE CONCEPTS (4)
            </button>
          </div>

          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-white/10 hover:bg-white/20 border border-white/20 text-white transition-colors"
          >
            {isPlaying ? <Pause className="w-3.5 h-3.5 text-amber-400" /> : <Play className="w-3.5 h-3.5 text-emerald-400" />}
            <span>{isPlaying ? "PAUSE" : "RUN"}</span>
          </button>
          <div className="flex items-center bg-white/10 rounded-lg p-0.5 border border-white/15">
            {[1, 2].map((s) => (
              <button
                key={s}
                onClick={() => setSpeed(s)}
                className={`px-2 py-1 text-[11px] font-mono rounded-md font-bold transition-colors ${
                  speed === s ? "bg-sky-500 text-white" : "text-sky-200 hover:text-white"
                }`}
              >
                {s}x
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Sub-Navigation Tabs */}
      <div className="px-4 py-2 bg-slate-100 border-b border-sky-100 flex items-center gap-2 overflow-x-auto text-xs font-mono">
        {equipmentType === "pumps" ? (
          [
            { id: 1, name: "Concept 1: 2.5D Volute & Motor Skid", badge: "Recommended" },
            { id: 2, name: "Concept 2: Digital Twin Power Ring", badge: "High-Tech IoT" },
            { id: 3, name: "Concept 3: Application-Specific Machines", badge: "Cutter & Blower" },
            { id: 4, name: "Concept 4: Glass-Face Sight Volute", badge: "Fluid Physics" },
          ].map((c) => (
            <button
              key={c.id}
              onClick={() => setActivePumpConcept(c.id)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg whitespace-nowrap font-semibold transition-all ${
                activePumpConcept === c.id
                  ? "bg-sky-600 text-white shadow-xs"
                  : "bg-white text-slate-700 hover:bg-sky-50 border border-slate-200"
              }`}
            >
              <span>{c.name}</span>
              <span
                className={`text-[9px] px-1.5 py-0.2 rounded font-mono ${
                  activePumpConcept === c.id ? "bg-sky-700 text-sky-100" : "bg-sky-100 text-sky-800"
                }`}
              >
                {c.badge}
              </span>
            </button>
          ))
        ) : (
          [
            { id: 1, name: "Concept 1: 2.5D Angle-Seat Solenoid Valve", badge: "Recommended" },
            { id: 2, name: "Concept 2: Motorized Butterfly Valve", badge: "Electric Actuator" },
            { id: 3, name: "Concept 3: Motorized Multiport Rotary Head", badge: "PSF/ACF Control" },
            { id: 4, name: "Concept 4: Smart IoT Modulating Control Valve", badge: "Aperture % Reg." },
          ].map((c) => (
            <button
              key={c.id}
              onClick={() => setActiveValveConcept(c.id)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg whitespace-nowrap font-semibold transition-all ${
                activeValveConcept === c.id
                  ? "bg-sky-600 text-white shadow-xs"
                  : "bg-white text-slate-700 hover:bg-sky-50 border border-slate-200"
              }`}
            >
              <span>{c.name}</span>
              <span
                className={`text-[9px] px-1.5 py-0.2 rounded font-mono ${
                  activeValveConcept === c.id ? "bg-sky-700 text-sky-100" : "bg-sky-100 text-sky-800"
                }`}
              >
                {c.badge}
              </span>
            </button>
          ))
        )}
      </div>

      {/* Main Stage Area */}
      <div className="p-6 bg-gradient-to-b from-slate-50 via-white to-sky-50/30 min-h-[380px] flex flex-col justify-center">
        {/* ========================================================================= */}
        {/* SECTION A: VALVE PROTOTYPES                                               */}
        {/* ========================================================================= */}
        {equipmentType === "valves" && (
          <>
            {/* VALVE CONCEPT 1: 2.5D ELECTRIC SOLENOID & ANGLE-SEAT VALVE */}
            {activeValveConcept === 1 && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
                <div className="lg:col-span-7 bg-white rounded-xl p-6 border border-sky-200/80 shadow-md flex flex-col items-center justify-center relative overflow-hidden">
                  <span className="absolute top-3 left-3 text-[10px] font-mono text-slate-400 font-bold uppercase tracking-wider">
                    Interactive Actuator Valve · Click Valve Body to Toggle
                  </span>

                  <svg viewBox="0 0 380 230" className="w-full max-w-[380px] h-auto select-none">
                    <defs>
                      <linearGradient id="vBronzeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stopColor="#94A3B8" />
                        <stop offset="30%" stopColor="#E2E8F0" />
                        <stop offset="70%" stopColor="#64748B" />
                        <stop offset="100%" stopColor="#334155" />
                      </linearGradient>

                      <linearGradient id="vActuatorGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="#1E293B" />
                        <stop offset="35%" stopColor="#475569" />
                        <stop offset="70%" stopColor="#334155" />
                        <stop offset="100%" stopColor="#0F172A" />
                      </linearGradient>

                      <filter id="vGlow" x="-20%" y="-20%" width="140%" height="140%">
                        <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#0284C7" floodOpacity="0.25" />
                      </filter>
                    </defs>

                    {/* Left & Right Connecting Pipes */}
                    <rect x="20" y="145" width="85" height="24" fill="url(#ssPipeH)" stroke="#475569" strokeWidth="1" />
                    <rect x="275" y="145" width="85" height="24" fill="url(#ssPipeH)" stroke="#475569" strokeWidth="1" />
                    {/* Flanged Joint Collars */}
                    <rect x="95" y="137" width="10" height="40" rx="2" fill="#94A3B8" stroke="#334155" strokeWidth="1" />
                    <rect x="275" y="137" width="10" height="40" rx="2" fill="#94A3B8" stroke="#334155" strokeWidth="1" />

                    {/* Valve Group (Clickable) */}
                    <g className="cursor-pointer" onClick={() => toggleValve("v1")}>
                      {/* Cast Valve Body with Angled Orifice Chamber */}
                      <path
                        d="M 105 145 L 155 145 L 225 145 L 275 145 L 275 169 L 225 169 L 155 169 L 105 169 Z"
                        fill="url(#vBronzeGrad)"
                        stroke="#1E293B"
                        strokeWidth="1.5"
                      />
                      {/* Central Angled Y-Pattern Valve Bonnet */}
                      <path d="M 155 145 L 190 85 L 225 145 Z" fill="url(#vBronzeGrad)" stroke="#1E293B" strokeWidth="1.5" />

                      {/* Internal Flow Chamber / Fluid Stream */}
                      {valveStates.v1 && isPlaying && (
                        <g>
                          <rect x="20" y="152" width="340" height="10" fill="#0284C7" opacity="0.4" />
                          <path d="M 20 157 L 360 157" stroke="#BAE6FD" strokeWidth="3" strokeDasharray="6 8">
                            <animate attributeName="stroke-dashoffset" from="28" to="0" dur={`${0.8 / speed}s`} repeatCount="indefinite" />
                          </path>
                        </g>
                      )}

                      {/* Valve Stem & Plug Disc (Moves Up and Down) */}
                      <g transform={`translate(190, ${valveStates.v1 ? 135 : 153})`} className="transition-transform duration-300">
                        {/* Polished Stainless Stem Shaft */}
                        <line x1="0" y1="-55" x2="0" y2="0" stroke="#CBD5E1" strokeWidth="4" strokeLinecap="round" />
                        {/* Resilient Elastomer Sealing Plug */}
                        <polygon points="-16,-4 16,-4 10,6 -10,6" fill={valveStates.v1 ? "#16A34A" : "#DC2626"} stroke="#0F172A" strokeWidth="1" />
                      </g>

                      {/* Top Pneumatic / Solenoid Actuator Cylinder */}
                      <g transform="translate(190, 75)">
                        {/* Actuator Canister Dome */}
                        <path d="M -26 -55 C -26 -65, 26 -65, 26 -55 L 26 0 L -26 0 Z" fill="url(#vActuatorGrad)" stroke="#0F172A" strokeWidth="2" />
                        {/* Actuator Ribs */}
                        <line x1="-24" y1="-20" x2="24" y2="-20" stroke="#64748B" strokeWidth="1.5" />
                        <line x1="-24" y1="-38" x2="24" y2="-38" stroke="#64748B" strokeWidth="1.5" />

                        {/* Top Mechanical Visual Position Indicator Spindle */}
                        <rect x="-8" y="-72" width="16" height="18" rx="2" fill="#0F172A" stroke="#475569" strokeWidth="1" />
                        {/* Spindle Flag (Green = Open, Red = Closed) */}
                        <rect
                          x="-6"
                          y={valveStates.v1 ? -70 : -63}
                          width="12"
                          height="8"
                          rx="1"
                          fill={valveStates.v1 ? "#16A34A" : "#DC2626"}
                          className="transition-all duration-300"
                        />

                        {/* Solenoid DIN Electrical Connector Plug */}
                        <rect x="26" y="-35" width="18" height="20" rx="3" fill="#334155" stroke="#1E293B" strokeWidth="1" />
                        <line x1="44" y1="-25" x2="56" y2="-25" stroke="#F59E0B" strokeWidth="2.5" />
                      </g>

                      {/* Status Badge */}
                      <g transform="translate(190, 205)">
                        <rect
                          x="-50"
                          y="-10"
                          width="100"
                          height="22"
                          rx="4"
                          fill={valveStates.v1 ? "#DCFCE7" : "#FEE2E2"}
                          stroke={valveStates.v1 ? "#16A34A" : "#DC2626"}
                          strokeWidth="1.5"
                          filter="url(#vGlow)"
                        />
                        <text
                          x="0"
                          y="4"
                          textAnchor="middle"
                          fill={valveStates.v1 ? "#15803D" : "#991B1B"}
                          fontSize="8.5"
                          fontWeight="bold"
                          fontFamily="monospace"
                        >
                          SOLENOID · {valveStates.v1 ? "OPEN (100%)" : "CLOSED (0%)"}
                        </text>
                      </g>
                    </g>
                  </svg>
                </div>

                <div className="lg:col-span-5 flex flex-col justify-between h-full space-y-4">
                  <div>
                    <div className="flex items-center gap-2 text-sky-800 font-bold text-base">
                      <ShieldCheck className="w-5 h-5 text-sky-600" />
                      <span>Concept 1: 2.5D Angle-Seat Solenoid Valve</span>
                    </div>
                    <p className="text-xs text-slate-600 mt-2 leading-relaxed">
                      Replaces the flat letter-"V" circle with an authentic <strong>Automated Solenoid Angle-Seat Valve</strong>.
                      Features a cast stainless Y-pattern valve bonnet, top actuator canister with DIN plug, and an internal stem that
                      visibly lifts and drops when toggled.
                    </p>

                    <div className="mt-4 p-3 bg-sky-50 rounded-lg border border-sky-100 text-xs font-mono space-y-1.5">
                      <div className="flex justify-between">
                        <span className="text-slate-500">Actuator Type:</span>
                        <span className="font-bold text-sky-800">24V DC Solenoid Pilot</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-500">Stem Travel:</span>
                        <span className="font-bold text-sky-800">{valveStates.v1 ? "18 mm (LIFTED)" : "0 mm (SEATED)"}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-500">Flow State:</span>
                        <span className={`font-bold ${valveStates.v1 ? "text-emerald-700" : "text-rose-700"}`}>
                          {valveStates.v1 ? "UNRESTRICTED FLOW" : "ZERO LEAKAGE (ISOLATED)"}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-[11px] text-slate-600 space-y-1">
                    <span className="font-bold text-slate-800">Best For:</span>
                    <p>• Water Solenoid and Clarifier Drain Valve, providing physical depth and instant visual confirmation of fluid gating.</p>
                  </div>
                </div>
              </div>
            )}

            {/* VALVE CONCEPT 2: MOTORIZED BUTTERFLY VALVE (ELECTRIC ACTUATOR) */}
            {activeValveConcept === 2 && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
                <div className="lg:col-span-7 bg-white rounded-xl p-6 border border-sky-200/80 shadow-md flex flex-col items-center justify-center relative overflow-hidden">
                  <span className="absolute top-3 left-3 text-[10px] font-mono text-slate-400 font-bold uppercase tracking-wider">
                    Electric Motorized Butterfly Valve · Click to Actuate
                  </span>

                  <svg viewBox="0 0 380 250" className="w-full max-w-[380px] h-auto select-none">
                    <defs>
                      <linearGradient id="actuatorBodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#0284C7" />
                        <stop offset="40%" stopColor="#0369A1" />
                        <stop offset="85%" stopColor="#075985" />
                        <stop offset="100%" stopColor="#0C4A6E" />
                      </linearGradient>

                      <linearGradient id="waferBodyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stopColor="#475569" />
                        <stop offset="35%" stopColor="#334155" />
                        <stop offset="80%" stopColor="#1E293B" />
                        <stop offset="100%" stopColor="#0F172A" />
                      </linearGradient>

                      <linearGradient id="discSSGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="#94A3B8" />
                        <stop offset="30%" stopColor="#F8FAFC" />
                        <stop offset="60%" stopColor="#CBD5E1" />
                        <stop offset="100%" stopColor="#64748B" />
                      </linearGradient>

                      <linearGradient id="brassGlandGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stopColor="#FDE047" />
                        <stop offset="50%" stopColor="#CA8A04" />
                        <stop offset="100%" stopColor="#854D0E" />
                      </linearGradient>

                      <radialGradient id="domeGlow" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stopColor={valveStates.v2 ? "#FDE047" : "#EF4444"} stopOpacity="0.8" />
                        <stop offset="100%" stopColor={valveStates.v2 ? "#EAB308" : "#991B1B"} stopOpacity="0.1" />
                      </radialGradient>
                    </defs>

                    {/* Left & Right Pipe Headers */}
                    <rect x="20" y="146" width="105" height="34" fill="url(#ssPipeH)" stroke="#475569" strokeWidth="1" />
                    <rect x="255" y="146" width="105" height="34" fill="url(#ssPipeH)" stroke="#475569" strokeWidth="1" />

                    {/* Pipe Companion Flanges (ANSI 150#) */}
                    <rect x="115" y="134" width="14" height="58" rx="2" fill="#64748B" stroke="#334155" strokeWidth="1" />
                    <rect x="251" y="134" width="14" height="58" rx="2" fill="#64748B" stroke="#334155" strokeWidth="1" />

                    {/* Flange Through-Stud Bolts with Hex Nuts */}
                    {[138, 150, 168, 184].map((y) => (
                      <g key={y}>
                        <line x1="108" y1={y} x2="272" y2={y} stroke="#94A3B8" strokeWidth="3.5" strokeLinecap="round" />
                        {/* Hex Nuts */}
                        <rect x="108" y={y - 3} width="6" height="6" fill="#CBD5E1" stroke="#334155" strokeWidth="0.8" />
                        <rect x="266" y={y - 3} width="6" height="6" fill="#CBD5E1" stroke="#334155" strokeWidth="0.8" />
                      </g>
                    ))}

                    {/* Entire Interactive Motorized Valve Assembly (Clickable) */}
                    <g className="cursor-pointer" onClick={() => toggleValve("v2")}>
                      {/* Fluid Flow Stream when Open */}
                      {valveStates.v2 && isPlaying && (
                        <g>
                          <rect x="20" y="152" width="340" height="22" fill="#0284C7" opacity="0.4" />
                          <path d="M 20 163 L 360 163" stroke="#BAE6FD" strokeWidth="3.5" strokeDasharray="8 8">
                            <animate attributeName="stroke-dashoffset" from="32" to="0" dur={`${0.8 / speed}s`} repeatCount="indefinite" />
                          </path>
                        </g>
                      )}

                      {/* ======================================================== */}
                      {/* 1. LOWER ASSEMBLY: WAFER VALVE BODY & DISC                */}
                      {/* ======================================================== */}
                      {/* Cast Iron Wafer Body Ring */}
                      <g transform="translate(190, 163)">
                        <circle cx="0" cy="0" r="39" fill="url(#waferBodyGrad)" stroke="#0F172A" strokeWidth="2" filter="url(#softShadow)" />
                        {/* Resilient EPDM Rubber Seat Ring */}
                        <circle cx="0" cy="0" r="30" fill="#0F172A" stroke="#334155" strokeWidth="1.5" />
                        <circle cx="0" cy="0" r="28" fill={valveStates.v2 ? "#0369A1" : "#0F172A"} opacity={valveStates.v2 ? 0.35 : 0.8} />

                        {/* 3D Rotating Stainless Disc */}
                        {valveStates.v2 ? (
                          /* OPEN: Disc Turned 90° Edge-On (Parallel to Fluid) */
                          <g className="transition-all duration-500">
                            {/* Fluid bypass waves */}
                            <path d="M -22 -14 Q 0 -22 22 -14" fill="none" stroke="#7DD3FC" strokeWidth="1.5" opacity="0.7" />
                            <path d="M -22 14 Q 0 22 22 14" fill="none" stroke="#7DD3FC" strokeWidth="1.5" opacity="0.7" />
                            {/* Thin SS Disc Blade */}
                            <line x1="0" y1="-28" x2="0" y2="28" stroke="url(#discSSGrad)" strokeWidth="6" strokeLinecap="round" />
                            <line x1="0" y1="-28" x2="0" y2="28" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                            {/* Central Drive Shaft Boss */}
                            <circle cx="0" cy="0" r="5" fill="#38BDF8" stroke="#FFFFFF" strokeWidth="1.5" />
                          </g>
                        ) : (
                          /* CLOSED: Disc Perpendicular (Bubble-Tight Sealing) */
                          <g className="transition-all duration-500">
                            {/* Full circular disc plate */}
                            <circle cx="0" cy="0" r="27" fill="url(#discSSGrad)" stroke="#DC2626" strokeWidth="2.5" />
                            <circle cx="0" cy="0" r="23" fill="#DC2626" opacity="0.15" />
                            {/* Disc Stiffening Ribs */}
                            <line x1="0" y1="-27" x2="0" y2="27" stroke="#475569" strokeWidth="2.5" strokeLinecap="round" />
                            <ellipse cx="0" cy="0" rx="20" ry="12" fill="none" stroke="#94A3B8" strokeWidth="1" strokeDasharray="3 3" />
                            <circle cx="0" cy="0" r="5.5" fill="#0F172A" stroke="#EF4444" strokeWidth="1.5" />
                          </g>
                        )}
                      </g>

                      {/* ======================================================== */}
                      {/* 2. ISO 5211 MOUNTING BRACKET / NECK                      */}
                      {/* ======================================================== */}
                      <g transform="translate(190, 118)">
                        {/* Upper Body Neck */}
                        <rect x="-10" y="0" width="20" height="12" fill="#334155" stroke="#1E293B" strokeWidth="1" />
                        {/* Drive Spindle Shaft */}
                        <line x1="0" y1="-6" x2="0" y2="10" stroke="#CBD5E1" strokeWidth="4" />
                        {/* Mounting Flange Plate */}
                        <rect x="-18" y="-6" width="36" height="6" rx="1" fill="#475569" stroke="#1E293B" strokeWidth="1" />
                        {/* 4 Bracket Connection Bolts */}
                        <circle cx="-13" cy="-3" r="1.5" fill="#94A3B8" />
                        <circle cx="13" cy="-3" r="1.5" fill="#94A3B8" />
                      </g>

                      {/* ======================================================== */}
                      {/* 3. ELECTRIC ACTUATOR ENCLOSURE (IP67 ROTORK/AUMA STYLE) */}
                      {/* ======================================================== */}
                      <g transform="translate(190, 68)">
                        {/* Main Aluminum Actuator Housing */}
                        <rect
                          x="-36"
                          y="-32"
                          width="72"
                          height="44"
                          rx="4"
                          fill="url(#actuatorBodyGrad)"
                          stroke="#082F49"
                          strokeWidth="2"
                          filter="url(#softShadow)"
                        />

                        {/* Motor Heat Dissipation Fins (Left Flank) */}
                        <line x1="-34" y1="-22" x2="-34" y2="4" stroke="#0284C7" strokeWidth="2" />
                        <line x1="-31" y1="-25" x2="-31" y2="7" stroke="#38BDF8" strokeWidth="1.2" opacity="0.6" />

                        {/* Actuator Front Local Interface Panel */}
                        <rect x="-24" y="-24" width="48" height="28" rx="2" fill="#0F172A" stroke="#0284C7" strokeWidth="1" />

                        {/* Telemetry Status LEDs on Actuator Face */}
                        <g transform="translate(-16, -15)">
                          {/* Green LED: RUN / OPEN */}
                          <circle cx="0" cy="0" r="3" fill={valveStates.v2 ? "#22C55E" : "#14532D"} />
                          {valveStates.v2 && <circle cx="0" cy="0" r="4.5" fill="none" stroke="#4ADE80" strokeWidth="1" opacity="0.8" />}
                          <text x="6" y="2.5" fill={valveStates.v2 ? "#4ADE80" : "#64748B"} fontSize="5" fontFamily="monospace" fontWeight="bold">
                            OPN
                          </text>

                          {/* Red LED: SHUT / CLOSED */}
                          <circle cx="20" cy="0" r="3" fill={!valveStates.v2 ? "#EF4444" : "#7F1D1D"} />
                          {!valveStates.v2 && <circle cx="20" cy="0" r="4.5" fill="none" stroke="#F87171" strokeWidth="1" opacity="0.8" />}
                          <text x="26" y="2.5" fill={!valveStates.v2 ? "#F87171" : "#64748B"} fontSize="5" fontFamily="monospace" fontWeight="bold">
                            CLS
                          </text>
                        </g>

                        {/* Local / Remote Key Switch Dial */}
                        <circle cx="-12" cy="-4" r="3.5" fill="#334155" stroke="#94A3B8" strokeWidth="0.8" />
                        <line x1="-12" y1="-4" x2="-10" y2="-6" stroke="#F8FAFC" strokeWidth="1.2" />
                        <text x="-5" y="-2" fill="#94A3B8" fontSize="4.5" fontFamily="monospace">REMOTE</text>

                        {/* Gearbox Specs Tag */}
                        <text x="14" y="-2" textAnchor="middle" fill="#38BDF8" fontSize="4.5" fontFamily="monospace" fontWeight="bold">230V·50Nm</text>

                        {/* ====================================================== */}
                        {/* 4. MANUAL OVERRIDE HANDWHEEL (LEFT SIDE)               */}
                        {/* ====================================================== */}
                        <g transform="translate(-36, -10)">
                          {/* Shaft extension */}
                          <rect x="-8" y="-3" width="8" height="6" fill="#475569" stroke="#1E293B" strokeWidth="0.8" />
                          {/* Declutch release lever */}
                          <line x1="-3" y1="-3" x2="-3" y2="-10" stroke="#F59E0B" strokeWidth="1.8" strokeLinecap="round" />
                          <circle cx="-3" cy="-10" r="1.5" fill="#DC2626" />
                          {/* Cast Handwheel Rim & Spokes */}
                          <ellipse cx="-13" cy="0" rx="5" ry="14" fill="#1E293B" stroke="#64748B" strokeWidth="1.5" />
                          <line x1="-13" y1="-14" x2="-13" y2="14" stroke="#94A3B8" strokeWidth="1.5" />
                          <line x1="-18" y1="0" x2="-8" y2="0" stroke="#94A3B8" strokeWidth="1.5" />
                          {/* Hand grip knob */}
                          <circle cx="-13" cy="-11" r="2" fill="#F8FAFC" stroke="#0F172A" strokeWidth="0.8" />
                        </g>

                        {/* ====================================================== */}
                        {/* 5. CABLE CONDUIT GLANDS & FIELD WIRING (RIGHT SIDE)    */}
                        {/* ====================================================== */}
                        <g transform="translate(36, -8)">
                          {/* Upper Gland: 230V AC Power */}
                          <rect x="0" y="-8" width="6" height="5" fill="url(#brassGlandGrad)" stroke="#78350F" strokeWidth="0.5" />
                          <path d="M 6 -5.5 Q 16 -5.5 18 10 T 20 28" fill="none" stroke="#1E293B" strokeWidth="2.5" strokeLinecap="round" />
                          {/* Lower Gland: 4-20mA SCADA Feedback */}
                          <rect x="0" y="2" width="6" height="5" fill="url(#brassGlandGrad)" stroke="#78350F" strokeWidth="0.5" />
                          <path d="M 6 4.5 Q 12 4.5 14 18 T 16 34" fill="none" stroke="#0284C7" strokeWidth="2" strokeDasharray="3 2" />
                        </g>

                        {/* ====================================================== */}
                        {/* 6. TOP 3D POSITION INDICATOR DOME BEACON               */}
                        {/* ====================================================== */}
                        <g transform="translate(0, -32)">
                          {/* Clear Polycarbonate Dome Capsule */}
                          <path d="M -12 0 C -12 -14 12 -14 12 0 Z" fill="#0F172A" stroke="#38BDF8" strokeWidth="1.5" />
                          {/* Glow overlay */}
                          <path d="M -10 0 C -10 -11 10 -11 10 0 Z" fill="url(#domeGlow)" />

                          {/* Rotating Indicator Rotor Blade (90° physical rotation) */}
                          {valveStates.v2 ? (
                            /* OPEN BEACON: High-Vis Yellow Bar Parallel to Flow */
                            <g className="transition-all duration-500">
                              <rect x="-10" y="-8" width="20" height="6" rx="1" fill="#FDE047" stroke="#854D0E" strokeWidth="0.8" />
                              <text x="0" y="-3.5" textAnchor="middle" fill="#713F12" fontSize="4.2" fontFamily="monospace" fontWeight="bold">
                                OPEN
                              </text>
                            </g>
                          ) : (
                            /* CLOSED BEACON: High-Vis Red Cross Perpendicular to Flow */
                            <g className="transition-all duration-500">
                              <rect x="-4" y="-12" width="8" height="12" rx="1" fill="#EF4444" stroke="#7F1D1D" strokeWidth="0.8" />
                              <text x="0" y="-3.5" textAnchor="middle" fill="#FFFFFF" fontSize="3.8" fontFamily="monospace" fontWeight="bold">
                                SHUT
                              </text>
                            </g>
                          )}
                        </g>
                      </g>

                      {/* ======================================================== */}
                      {/* 7. SCADA STATUS BADGE                                    */}
                      {/* ======================================================== */}
                      <g transform="translate(190, 222)">
                        <rect
                          x="-80"
                          y="-10"
                          width="160"
                          height="22"
                          rx="4"
                          fill={valveStates.v2 ? "#DCFCE7" : "#FEE2E2"}
                          stroke={valveStates.v2 ? "#16A34A" : "#DC2626"}
                          strokeWidth="1.5"
                          filter="url(#vGlow)"
                        />
                        <text
                          x="0"
                          y="4"
                          textAnchor="middle"
                          fill={valveStates.v2 ? "#15803D" : "#991B1B"}
                          fontSize="8"
                          fontWeight="bold"
                          fontFamily="monospace"
                        >
                          MOTORIZED · {valveStates.v2 ? "OPEN (90° FULL BORE)" : "CLOSED (0° BUBBLE-TIGHT)"}
                        </text>
                      </g>
                    </g>
                  </svg>
                </div>

                <div className="lg:col-span-5 flex flex-col justify-between h-full space-y-4">
                  <div>
                    <div className="flex items-center gap-2 text-sky-800 font-bold text-base">
                      <RotateCw className="w-5 h-5 text-sky-600" />
                      <span>Concept 2: Motorized Butterfly Valve</span>
                    </div>
                    <p className="text-xs text-slate-600 mt-2 leading-relaxed">
                      Industrial <strong>Electric Quarter-Turn Actuator</strong> (Rotork / Auma / Belimo standard) mounted to an
                      EPDM-lined wafer butterfly body. When energized, the internal synchronous motor drives a planetary worm gear,
                      rotating the 316 stainless disc 90° into full stream alignment while turning the <strong>top yellow/red dome beacon</strong>.
                    </p>

                    <div className="mt-4 p-3 bg-sky-50 rounded-lg border border-sky-100 text-xs font-mono space-y-1.5">
                      <div className="flex justify-between">
                        <span className="text-slate-500">Actuator Type:</span>
                        <span className="font-bold text-sky-800">IP67 Electric Reversible (230V AC)</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-500">Disc Orientation:</span>
                        <span className={`font-bold ${valveStates.v2 ? "text-emerald-700" : "text-rose-700"}`}>
                          {valveStates.v2 ? "90° Parallel (Full Bore 100%)" : "0° Perpendicular (ANSI Class VI)"}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-500">Visual Dome Beacon:</span>
                        <span className={`font-bold ${valveStates.v2 ? "text-amber-600" : "text-rose-600"}`}>
                          {valveStates.v2 ? "YELLOW (In-Line / Flowing)" : "RED (Cross-Line / Isolated)"}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-500">Manual Override:</span>
                        <span className="font-bold text-slate-700">Declutch Lever & Handwheel</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-500">SCADA Telemetry:</span>
                        <span className="font-bold text-sky-700">4-20mA Position + Limit Switches</span>
                      </div>
                    </div>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-[11px] text-slate-600 space-y-1">
                    <span className="font-bold text-slate-800">Best For:</span>
                    <p>• Main plant influent/effluent headers, Clarifier sludge drain lines, and high-flow isolation where motorized automated actuation is required.</p>
                  </div>
                </div>
              </div>
            )}

            {/* VALVE CONCEPT 3: INDUSTRIAL MULTIPORT ROTARY HEAD (PSF/ACF) */}
            {activeValveConcept === 3 && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
                <div className="lg:col-span-7 bg-white rounded-xl p-6 border border-sky-200/80 shadow-md flex flex-col items-center justify-center relative overflow-hidden">
                  <span className="absolute top-3 left-3 text-[10px] font-mono text-slate-400 font-bold uppercase tracking-wider">
                    Automatic Multiport Rotary Control Head · Click to Index Mode
                  </span>

                  <svg viewBox="0 0 380 230" className="w-full max-w-[380px] h-auto select-none">
                    {/* Connecting Pipes: INLET, OUTLET, VIN, VOUT, DRAIN */}
                    <line x1="190" y1="10" x2="190" y2="45" stroke="#0284C7" strokeWidth="6" strokeLinecap="round" />
                    <line x1="190" y1="165" x2="190" y2="200" stroke="#0284C7" strokeWidth="6" strokeLinecap="round" />
                    <line x1="250" y1="85" x2="310" y2="85" stroke="#0284C7" strokeWidth="5" strokeLinecap="round" />
                    <line x1="250" y1="125" x2="310" y2="125" stroke="#0284C7" strokeWidth="5" strokeLinecap="round" />
                    <line x1="70" y1="125" x2="130" y2="125" stroke="#DC2626" strokeWidth="5" strokeLinecap="round" />

                    {/* Multiport Valve Body (Clickable) */}
                    <g transform="translate(190, 105)" className="cursor-pointer" onClick={() => toggleValve("v3")}>
                      <rect x="-60" y="-60" width="120" height="120" rx="12" fill="#1E293B" stroke="#0369A1" strokeWidth="2" filter="url(#softShadow)" />

                      <circle cx="0" cy="0" r="42" fill="#0F172A" stroke="#38BDF8" strokeWidth="1.5" />
                      <circle cx="0" cy="0" r="36" fill={valveStates.v3 ? "#064E3B" : "#881337"} opacity="0.4" />

                      {valveStates.v3 ? (
                        <g>
                          <path d="M 0 -36 Q 0 0 36 -20" stroke="#38BDF8" strokeWidth="4" fill="none" strokeLinecap="round" />
                          <path d="M 36 20 Q 0 0 0 36" stroke="#38BDF8" strokeWidth="4" fill="none" strokeLinecap="round" />
                          {isPlaying && (
                            <circle cx="18" cy="-10" r="2.5" fill="#FFFFFF">
                              <animate attributeName="opacity" values="0.3;1;0.3" dur="1s" repeatCount="indefinite" />
                            </circle>
                          )}
                        </g>
                      ) : (
                        <g>
                          <path d="M 0 -36 Q 0 0 36 20" stroke="#F87171" strokeWidth="4" fill="none" strokeLinecap="round" />
                          <path d="M 36 -20 Q 0 0 -36 20" stroke="#DC2626" strokeWidth="4" fill="none" strokeLinecap="round" />
                          {isPlaying && (
                            <circle cx="-10" cy="10" r="2.5" fill="#FCA5A5">
                              <animate attributeName="opacity" values="0.3;1;0.3" dur="0.8s" repeatCount="indefinite" />
                            </circle>
                          )}
                        </g>
                      )}

                      <circle cx="0" cy="0" r="14" fill="#0284C7" stroke="#FFFFFF" strokeWidth="1.5" />
                      <text x="0" y="3" textAnchor="middle" fill="#FFFFFF" fontSize="6.5" fontWeight="bold" fontFamily="monospace">
                        ROTOR
                      </text>

                      <text x="0" y="-45" textAnchor="middle" fill="#38BDF8" fontSize="6" fontWeight="bold" fontFamily="monospace">INLET</text>
                      <text x="0" y="52" textAnchor="middle" fill="#38BDF8" fontSize="6" fontWeight="bold" fontFamily="monospace">OUTLET</text>
                      <text x="48" y="-18" textAnchor="end" fill="#38BDF8" fontSize="6" fontWeight="bold" fontFamily="monospace">VIN</text>
                      <text x="48" y="24" textAnchor="end" fill="#38BDF8" fontSize="6" fontWeight="bold" fontFamily="monospace">VOUT</text>
                      <text x="-48" y="24" textAnchor="start" fill="#F87171" fontSize="6" fontWeight="bold" fontFamily="monospace">DRAIN</text>
                    </g>

                    {/* Mode Status Pill */}
                    <g transform="translate(190, 215)">
                      <rect
                        x="-65"
                        y="-10"
                        width="130"
                        height="20"
                        rx="4"
                        fill={valveStates.v3 ? "#DCFCE7" : "#FEE2E2"}
                        stroke={valveStates.v3 ? "#16A34A" : "#DC2626"}
                        strokeWidth="1.2"
                      />
                      <text
                        x="0"
                        y="4"
                        textAnchor="middle"
                        fill={valveStates.v3 ? "#15803D" : "#991B1B"}
                        fontSize="8"
                        fontWeight="bold"
                        fontFamily="monospace"
                      >
                        MODE: {valveStates.v3 ? "NORMAL SERVICE" : "BACKWASH TO DRAIN"}
                      </text>
                    </g>
                  </svg>
                </div>

                <div className="lg:col-span-5 flex flex-col justify-between h-full space-y-4">
                  <div>
                    <div className="flex items-center gap-2 text-sky-800 font-bold text-base">
                      <Layers className="w-5 h-5 text-sky-600" />
                      <span>Concept 3: Motorized Multiport Rotary Valve</span>
                    </div>
                    <p className="text-xs text-slate-600 mt-2 leading-relaxed">
                      Replaces the flat green rectangles on the PSF and ACF filters with an authentic <strong>Indexable Multiport Valve Head</strong> (Pentair / Fleck style).
                    </p>

                    <div className="mt-4 p-3 bg-sky-50 rounded-lg border border-sky-100 text-xs font-mono space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-slate-500">Current Position:</span>
                        <span className={`font-bold ${valveStates.v3 ? "text-emerald-700" : "text-rose-700"}`}>
                          {valveStates.v3 ? "1 · FILTER SERVICE" : "2 · BACKWASH REVERSE"}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-600">
                        {valveStates.v3
                          ? "Raw water enters top of vessel (VIN), passes down through sand bed, and exits polished (VOUT)."
                          : "Water enters bottom (VOUT), lifts and scours the sand media bed, flushing accumulated silt to DRAIN."}
                      </p>
                    </div>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-[11px] text-slate-600">
                    <span className="font-bold text-slate-800">Best For:</span> Direct replacement for PSF Valve and ACF Valve blocks, unlocking real backwash simulation in SCADA!
                  </div>
                </div>
              </div>
            )}

            {/* VALVE CONCEPT 4: SMART IOT MODULATING CONTROL VALVE */}
            {activeValveConcept === 4 && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
                <div className="lg:col-span-7 bg-white rounded-xl p-6 border border-sky-200/80 shadow-md flex flex-col items-center justify-center relative overflow-hidden">
                  <span className="absolute top-3 left-3 text-[10px] font-mono text-slate-400 font-bold uppercase tracking-wider">
                    Smart Modulating Flow Control Valve · Drag Slider to Throttle
                  </span>

                  <svg viewBox="0 0 380 230" className="w-full max-w-[380px] h-auto select-none">
                    <rect x="25" y="135" width="110" height="30" fill="url(#ssPipeH)" stroke="#475569" strokeWidth="1" />
                    <rect x="245" y="135" width="110" height="30" fill="url(#ssPipeH)" stroke="#475569" strokeWidth="1" />

                    <g transform="translate(190, 150)">
                      <path d="M -55 0 L -25 -25 L 25 -25 L 55 0 L 55 15 L -55 15 Z" fill="#334155" stroke="#0F172A" strokeWidth="1.5" />
                      
                      {valveAperture > 0 && isPlaying && (
                        <path d="M -165 0 L 165 0" stroke="#38BDF8" strokeWidth={1 + (4 * valveAperture) / 100} strokeDasharray="5 7">
                          <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${(1.5 - valveAperture / 100) / speed}s`} repeatCount="indefinite" />
                        </path>
                      )}

                      <g transform="translate(0, -75)">
                        <rect x="-30" y="-35" width="60" height="85" rx="6" fill="#0F172A" stroke="#0284C7" strokeWidth="1.5" filter="url(#softShadow)" />

                        <rect x="-24" y="-28" width="48" height="26" rx="3" fill="#082F49" stroke="#38BDF8" strokeWidth="1" />
                        <text x="0" y="-15" textAnchor="middle" fill="#38BDF8" fontSize="10" fontWeight="900" fontFamily="monospace">
                          {valveAperture}%
                        </text>
                        <text x="0" y="-6" textAnchor="middle" fill="#94A3B8" fontSize="5.5" fontFamily="monospace">
                          APERTURE
                        </text>

                        <g transform="translate(-20, 5)">
                          {[0, 6, 12, 18, 24, 30].map((y, i) => (
                            <rect
                              key={i}
                              x="0"
                              y={y}
                              width="40"
                              height="4"
                              rx="1"
                              fill={valveAperture >= (6 - i) * 16 ? "#10B981" : "#1E293B"}
                            />
                          ))}
                        </g>
                      </g>

                      <g transform="translate(0, 48)">
                        <rect x="-55" y="-10" width="110" height="22" rx="4" fill="#F0F9FF" stroke="#0284C7" strokeWidth="1" />
                        <text x="0" y="0" textAnchor="middle" fill="#0369A1" fontSize="8" fontWeight="bold" fontFamily="monospace">
                          FLOW: {((telemetry.flowRate * valveAperture) / 100).toFixed(1)} m³/h
                        </text>
                        <text x="0" y="8" textAnchor="middle" fill="#475569" fontSize="6.5" fontFamily="monospace">
                          ΔP: {(telemetry.pressureDelta * (100 / Math.max(10, valveAperture))).toFixed(2)} Bar
                        </text>
                      </g>
                    </g>
                  </svg>

                  <div className="w-full max-w-[260px] flex items-center gap-3 mt-2">
                    <span className="text-[10px] font-mono text-slate-500 font-bold">0%</span>
                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={valveAperture}
                      onChange={(e) => setValveAperture(parseInt(e.target.value))}
                      className="w-full accent-sky-600 cursor-pointer"
                    />
                    <span className="text-[10px] font-mono text-slate-500 font-bold">100%</span>
                  </div>
                </div>

                <div className="lg:col-span-5 flex flex-col justify-between h-full space-y-4">
                  <div>
                    <div className="flex items-center gap-2 text-sky-800 font-bold text-base">
                      <Gauge className="w-5 h-5 text-emerald-600" />
                      <span>Concept 4: Smart IoT Modulating Control Valve</span>
                    </div>
                    <p className="text-xs text-slate-600 mt-2 leading-relaxed">
                      An intelligent regulating valve with an integrated digital positioner. Shows continuous throttle percentage
                      and dynamically calculates downstream pressure drop ($\Delta P$) and flow rate in real time.
                    </p>

                    <div className="mt-4 p-3 bg-sky-50 rounded-lg border border-sky-100 text-xs font-mono space-y-1.5">
                      <div className="flex justify-between">
                        <span className="text-slate-500">Current Aperture:</span>
                        <span className="font-bold text-sky-800">{valveAperture}% Open</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-500">Flow Coefficient (Cv):</span>
                        <span className="font-bold text-sky-800">{(0.45 * valveAperture).toFixed(1)} GPM/psi</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-500">Signal Input:</span>
                        <span className="font-bold text-sky-800">{(4 + (16 * valveAperture) / 100).toFixed(1)} mA (4–20mA)</span>
                      </div>
                    </div>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-[11px] text-slate-600">
                    <span className="font-bold text-slate-800">Best For:</span> Advanced SCADA plants with proportional flow throttling and automated dosing adjustment.
                  </div>
                </div>
              </div>
            )}
          </>
        )}

        {/* ========================================================================= */}
        {/* SECTION B: PUMP PROTOTYPES                                                */}
        {/* ========================================================================= */}
        {equipmentType === "pumps" && (
          <>
            {activePumpConcept === 1 && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
                <div className="lg:col-span-7 bg-white rounded-xl p-6 border border-sky-200/80 shadow-md flex flex-col items-center justify-center relative overflow-hidden">
                  <span className="absolute top-3 left-3 text-[10px] font-mono text-slate-400 font-bold uppercase tracking-wider">
                    Interactive Machine Canvas · Click Pump to Toggle
                  </span>

                  <svg viewBox="0 0 420 220" className="w-full max-w-[420px] h-auto select-none">
                    <defs>
                      <linearGradient id="c1MotorGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stopColor="#475569" />
                        <stop offset="25%" stopColor="#94A3B8" />
                        <stop offset="60%" stopColor="#475569" />
                        <stop offset="100%" stopColor="#1E293B" />
                      </linearGradient>

                      <linearGradient id="c1VoluteGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#0284C7" />
                        <stop offset="40%" stopColor="#38BDF8" />
                        <stop offset="85%" stopColor="#0369A1" />
                        <stop offset="100%" stopColor="#075985" />
                      </linearGradient>

                      <linearGradient id="c1SkidGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stopColor="#334155" />
                        <stop offset="50%" stopColor="#64748B" />
                        <stop offset="100%" stopColor="#0F172A" />
                      </linearGradient>

                      <filter id="c1Glow" x="-20%" y="-20%" width="140%" height="140%">
                        <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#0284C7" floodOpacity="0.3" />
                      </filter>
                    </defs>

                    <rect x="50" y="180" width="320" height="12" rx="3" fill="#E2E8F0" />
                    <ellipse cx="210" cy="180" rx="150" ry="6" fill="#0F172A" opacity="0.15" />

                    <g className="cursor-pointer" onClick={() => togglePump("c1")}>
                      <rect x="70" y="165" width="280" height="16" rx="2" fill="url(#c1SkidGrad)" stroke="#1E293B" strokeWidth="1" />
                      {[85, 140, 280, 335].map((x) => (
                        <g key={x}>
                          <rect x={x} y="161" width="8" height="4" rx="1" fill="#94A3B8" stroke="#475569" strokeWidth="0.5" />
                          <circle cx={x + 4} cy="163" r="1.5" fill="#1E293B" />
                        </g>
                      ))}

                      <g id="electric-motor" transform="translate(80, 65)">
                        <rect x="0" y="15" width="22" height="70" rx="4" fill="#334155" stroke="#1E293B" strokeWidth="1" />
                        {[22, 32, 42, 52, 62, 72].map((y) => (
                          <line key={y} x1="4" y1={y} x2="18" y2={y} stroke="#64748B" strokeWidth="1.2" />
                        ))}

                        <rect x="22" y="10" width="95" height="80" rx="4" fill="url(#c1MotorGrad)" stroke="#1E293B" strokeWidth="1.2" />
                        {[18, 26, 34, 42, 50, 58, 66, 74, 82].map((y) => (
                          <line key={y} x1="24" y1={y} x2="115" y2={y} stroke="#CBD5E1" strokeWidth="1.2" opacity="0.6" />
                        ))}

                        <rect x="45" y="0" width="38" height="12" rx="2" fill="#1E293B" stroke="#64748B" strokeWidth="0.8" />
                        <text x="64" y="9" textAnchor="middle" fill="#38BDF8" fontSize="5.5" fontWeight="bold" fontFamily="monospace">
                          400V · 3φ
                        </text>

                        <rect x="30" y="90" width="22" height="10" fill="#334155" />
                        <rect x="85" y="90" width="22" height="10" fill="#334155" />

                        <rect x="117" y="25" width="24" height="50" rx="2" fill="#64748B" stroke="#334155" strokeWidth="1" />
                        <text x="129" y="52" textAnchor="middle" fill="#FFFFFF" fontSize="6" fontWeight="bold" fontFamily="monospace">
                          COUPLING
                        </text>
                      </g>

                      <g id="volute-pump" transform="translate(225, 45)">
                        <path d="M 68 0 L 98 0 L 98 60 L 68 60 Z" fill="url(#c1VoluteGrad)" stroke="#0369A1" strokeWidth="1.5" />
                        <rect x="62" y="0" width="42" height="8" rx="2" fill="#94A3B8" stroke="#334155" strokeWidth="1" />
                        {[68, 83, 98].map((x) => (
                          <circle key={x} cx={x} cy="4" r="1.5" fill="#1E293B" />
                        ))}

                        <circle cx="50" cy="65" r="44" fill="url(#c1VoluteGrad)" stroke="#0369A1" strokeWidth="2" filter="url(#c1Glow)" />
                        <path
                          d="M 50 21 C 75 21, 98 42, 98 65 C 98 90, 75 110, 50 110 C 24 110, 5 88, 5 65 C 5 45, 20 28, 42 22 L 68 0"
                          fill="none"
                          stroke="#38BDF8"
                          strokeWidth="1.5"
                          opacity="0.8"
                        />

                        <circle cx="50" cy="65" r="28" fill="#0C4A6E" stroke="#7DD3FC" strokeWidth="1.5" />
                        <circle cx="50" cy="65" r="25" fill="#0284C7" opacity="0.35" />

                        <g transform="translate(50, 65)">
                          {isPlaying && pumpStates.c1 && (
                            <animateTransform
                              attributeName="transform"
                              type="rotate"
                              from="0"
                              to="360"
                              dur={`${0.5 / speed}s`}
                              repeatCount="indefinite"
                            />
                          )}
                          <circle cx="0" cy="0" r="6" fill="#F8FAFC" stroke="#0369A1" strokeWidth="1" />
                          {[0, 60, 120, 180, 240, 300].map((deg) => (
                            <path
                              key={deg}
                              d="M 0 0 Q 10 8 20 4"
                              stroke={pumpStates.c1 ? "#FFFFFF" : "#94A3B8"}
                              strokeWidth="2.5"
                              strokeLinecap="round"
                              fill="none"
                              transform={`rotate(${deg})`}
                            />
                          ))}
                        </g>

                        <rect x="38" y="110" width="24" height="10" fill="#334155" />
                        <circle cx="50" cy="65" r="10" fill="none" stroke="#FFFFFF" strokeWidth="1.5" opacity="0.8" />
                      </g>

                      <g transform="translate(210, 20)">
                        <rect
                          x="-45"
                          y="0"
                          width="90"
                          height="20"
                          rx="5"
                          fill={pumpStates.c1 ? "#DCFCE7" : "#FEE2E2"}
                          stroke={pumpStates.c1 ? "#16A34A" : "#DC2626"}
                          strokeWidth="1.5"
                          filter="url(#c1Glow)"
                        />
                        <circle cx="-32" cy="10" r="3.5" fill={pumpStates.c1 ? "#16A34A" : "#DC2626"}>
                          {isPlaying && pumpStates.c1 && (
                            <animate attributeName="opacity" values="0.7;1;0.7" dur="1s" repeatCount="indefinite" />
                          )}
                        </circle>
                        <text
                          x="4"
                          y="13"
                          textAnchor="middle"
                          fill={pumpStates.c1 ? "#15803D" : "#991B1B"}
                          fontSize="8"
                          fontWeight="bold"
                          fontFamily="monospace"
                        >
                          M1 · {pumpStates.c1 ? "RUNNING" : "STOPPED"}
                        </text>
                      </g>
                    </g>
                  </svg>
                </div>

                <div className="lg:col-span-5 flex flex-col justify-between h-full space-y-4">
                  <div>
                    <div className="flex items-center gap-2 text-sky-800 font-bold text-base">
                      <ShieldCheck className="w-5 h-5 text-sky-600" />
                      <span>Concept 1: Industrial Volute & Motor Skid</span>
                    </div>
                    <p className="text-xs text-slate-600 mt-2 leading-relaxed">
                      Replaces flat circles with an authentic <strong>Centrifugal End-Suction Pump</strong> set. Features a
                      ribbed TEFC electric induction motor with cooling fins, shaft coupling, snail volute casing, and structural steel skid.
                    </p>

                    <div className="mt-4 grid grid-cols-2 gap-2 text-xs font-mono">
                      <div className="p-2.5 rounded-lg bg-sky-50 border border-sky-100 flex flex-col">
                        <span className="text-[10px] text-slate-500 uppercase">Motor Speed</span>
                        <span className="text-sm font-bold text-sky-800">{telemetry.rpm} RPM</span>
                      </div>
                      <div className="p-2.5 rounded-lg bg-sky-50 border border-sky-100 flex flex-col">
                        <span className="text-[10px] text-slate-500 uppercase">Electrical Power</span>
                        <span className="text-sm font-bold text-sky-800">{telemetry.powerKw} kW</span>
                      </div>
                      <div className="p-2.5 rounded-lg bg-sky-50 border border-sky-100 flex flex-col">
                        <span className="text-[10px] text-slate-500 uppercase">Flow Velocity</span>
                        <span className="text-sm font-bold text-sky-800">{telemetry.flowRate} m³/h</span>
                      </div>
                      <div className="p-2.5 rounded-lg bg-sky-50 border border-sky-100 flex flex-col">
                        <span className="text-[10px] text-slate-500 uppercase">Bearing Temp</span>
                        <span className="text-sm font-bold text-emerald-700">{telemetry.tempC} °C</span>
                      </div>
                    </div>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-[11px] text-slate-600 space-y-1">
                    <span className="font-bold text-slate-800">Why it fits Nanneer Global:</span>
                    <p>• Matches the 2.5D glass vessels perfectly in depth, shadows, and physical machinery realism.</p>
                  </div>
                </div>
              </div>
            )}

            {activePumpConcept === 2 && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
                <div className="lg:col-span-7 bg-white rounded-xl p-6 border border-sky-200/80 shadow-md flex flex-col items-center justify-center relative overflow-hidden">
                  <span className="absolute top-3 left-3 text-[10px] font-mono text-slate-400 font-bold uppercase tracking-wider">
                    Digital Twin Radial Gauge Canvas · Click to Toggle
                  </span>

                  <svg viewBox="0 0 360 220" className="w-full max-w-[360px] h-auto select-none">
                    <g transform="translate(180, 110)" className="cursor-pointer" onClick={() => togglePump("c2")}>
                      <circle cx="0" cy="0" r="72" fill="none" stroke="#E2E8F0" strokeWidth="6" />
                      <circle
                        cx="0"
                        cy="0"
                        r="72"
                        fill="none"
                        stroke={pumpStates.c2 ? "#0284C7" : "#CBD5E1"}
                        strokeWidth="6"
                        strokeDasharray="452"
                        strokeDashoffset={pumpStates.c2 ? 452 - (452 * 0.75 * telemetry.loadPct) / 100 : 452}
                        strokeLinecap="round"
                        transform="rotate(135)"
                      />

                      <circle cx="0" cy="0" r="58" fill="url(#metalRingGrad)" stroke="#94A3B8" strokeWidth="1.5" />
                      <circle cx="0" cy="0" r="50" fill={pumpStates.c2 ? "#0F172A" : "#334155"} stroke="#38BDF8" strokeWidth="2" />

                      <g>
                        {isPlaying && pumpStates.c2 && (
                          <animateTransform
                            attributeName="transform"
                            type="rotate"
                            from="0"
                            to="360"
                            dur={`${0.4 / speed}s`}
                            repeatCount="indefinite"
                          />
                        )}
                        {[0, 60, 120, 180, 240, 300].map((deg) => (
                          <path
                            key={deg}
                            d="M 0 0 Q 18 12 38 6"
                            stroke={pumpStates.c2 ? "#38BDF8" : "#94A3B8"}
                            strokeWidth="3.2"
                            strokeLinecap="round"
                            fill="none"
                            transform={`rotate(${deg})`}
                          />
                        ))}
                        <circle cx="0" cy="0" r="14" fill="#0284C7" stroke="#FFFFFF" strokeWidth="1.5" />
                      </g>

                      <circle cx="0" cy="0" r="12" fill="#0F172A" />
                      <text x="0" y="3" textAnchor="middle" fill="#FFFFFF" fontSize="8" fontWeight="bold" fontFamily="monospace">
                        M10
                      </text>

                      <g transform="translate(0, 92)">
                        <rect x="-42" y="-12" width="84" height="24" rx="4" fill="#F0F9FF" stroke="#0284C7" strokeWidth="1.2" />
                        <text x="0" y="-1" textAnchor="middle" fill="#0369A1" fontSize="9" fontWeight="bold" fontFamily="monospace">
                          {pumpStates.c2 ? `${telemetry.loadPct}% LOAD` : "STANDBY"}
                        </text>
                        <text x="0" y="8" textAnchor="middle" fill="#475569" fontSize="6.5" fontFamily="monospace">
                          {telemetry.powerKw} kW · 400V
                        </text>
                      </g>
                    </g>
                  </svg>
                </div>

                <div className="lg:col-span-5 flex flex-col justify-between h-full space-y-4">
                  <div>
                    <div className="flex items-center gap-2 text-sky-800 font-bold text-base">
                      <Zap className="w-5 h-5 text-amber-500" />
                      <span>Concept 2: Digital Twin Power Ring</span>
                    </div>
                    <p className="text-xs text-slate-600 mt-2 leading-relaxed">
                      A high-tech IoT SCADA aesthetic. Encircled by an active <strong>radial motor load arc</strong> that
                      dynamically tracks electrical power and motor torque in real-time.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {activePumpConcept === 3 && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
                <div className="lg:col-span-7 bg-white rounded-xl p-6 border border-sky-200/80 shadow-md flex items-center justify-around relative overflow-hidden">
                  <span className="absolute top-3 left-3 text-[10px] font-mono text-slate-400 font-bold uppercase tracking-wider">
                    Custom Tailored Machine Models
                  </span>

                  <div className="flex flex-col items-center">
                    <svg viewBox="0 0 160 200" className="w-36 h-auto cursor-pointer" onClick={() => togglePump("c3a")}>
                      <path d="M 60 40 C 60 18, 100 18, 100 40" fill="none" stroke="#64748B" strokeWidth="4" strokeLinecap="round" />
                      <rect x="96" y="32" width="12" height="18" rx="2" fill="#1E293B" />
                      <path d="M 102 32 C 102 10, 130 15, 140 0" fill="none" stroke="#F59E0B" strokeWidth="3" />

                      <rect x="45" y="40" width="70" height="90" rx="8" fill="url(#c1MotorGrad)" stroke="#1E293B" strokeWidth="1.5" />
                      {[52, 64, 76, 88, 100, 112].map((y) => (
                        <line key={y} x1="48" y1={y} x2="112" y2={y} stroke="#CBD5E1" strokeWidth="1" opacity="0.5" />
                      ))}

                      <rect x="55" y="70" width="50" height="18" rx="2" fill="#0F172A" />
                      <text x="80" y="82" textAnchor="middle" fill="#38BDF8" fontSize="7" fontWeight="bold" fontFamily="monospace">
                        SUBMERSIBLE
                      </text>

                      <path d="M 30 130 L 130 130 L 140 165 L 20 165 Z" fill="#0284C7" stroke="#0369A1" strokeWidth="1.5" />
                      {[35, 55, 75, 95, 115].map((x) => (
                        <line key={x} x1={x} y1="145" x2={x} y2="162" stroke="#FFFFFF" strokeWidth="1.5" opacity="0.8" />
                      ))}

                      <rect x="125" y="135" width="22" height="20" rx="2" fill="#64748B" stroke="#1E293B" strokeWidth="1" />
                      <polygon points="147,145 155,145 151,140" fill="#38BDF8" />

                      <rect
                        x="45"
                        y="175"
                        width="70"
                        height="18"
                        rx="4"
                        fill={pumpStates.c3a ? "#DCFCE7" : "#FEE2E2"}
                        stroke={pumpStates.c3a ? "#16A34A" : "#DC2626"}
                        strokeWidth="1.2"
                      />
                      <text
                        x="80"
                        y="187"
                        textAnchor="middle"
                        fill={pumpStates.c3a ? "#15803D" : "#991B1B"}
                        fontSize="7.5"
                        fontWeight="bold"
                        fontFamily="monospace"
                      >
                        M1 · CUTTER
                      </text>
                    </svg>
                    <span className="text-[11px] font-mono font-bold text-slate-700 mt-1">3A: Submersible Chopper</span>
                  </div>

                  <div className="flex flex-col items-center">
                    <svg viewBox="0 0 170 200" className="w-40 h-auto cursor-pointer" onClick={() => togglePump("c3b")}>
                      <rect x="60" y="10" width="50" height="40" rx="6" fill="#475569" stroke="#1E293B" strokeWidth="1.5" />
                      {[18, 26, 34, 42].map((y) => (
                        <line key={y} x1="65" y1={y} x2="105" y2={y} stroke="#94A3B8" strokeWidth="1" />
                      ))}
                      <text x="85" y="32" textAnchor="middle" fill="#FFFFFF" fontSize="6.5" fontWeight="bold" fontFamily="monospace">
                        SILENCER
                      </text>

                      <rect x="35" y="50" width="100" height="85" rx="10" fill="#D97706" stroke="#92400E" strokeWidth="2" />

                      <g transform="translate(65, 92)">
                        {isPlaying && pumpStates.c3b && (
                          <animateTransform
                            attributeName="transform"
                            type="rotate"
                            from="0"
                            to="360"
                            dur={`${0.6 / speed}s`}
                            repeatCount="indefinite"
                          />
                        )}
                        <ellipse cx="0" cy="-12" rx="10" ry="14" fill="#FEF3C7" stroke="#B45309" strokeWidth="1.5" />
                        <ellipse cx="0" cy="12" rx="10" ry="14" fill="#FEF3C7" stroke="#B45309" strokeWidth="1.5" />
                        <circle cx="0" cy="0" r="4" fill="#92400E" />
                      </g>

                      <g transform="translate(105, 92)">
                        {isPlaying && pumpStates.c3b && (
                          <animateTransform
                            attributeName="transform"
                            type="rotate"
                            from="0"
                            to="-360"
                            dur={`${0.6 / speed}s`}
                            repeatCount="indefinite"
                          />
                        )}
                        <ellipse cx="-12" cy="0" rx="14" ry="10" fill="#FEF3C7" stroke="#B45309" strokeWidth="1.5" />
                        <ellipse cx="12" cy="0" rx="14" ry="10" fill="#FEF3C7" stroke="#B45309" strokeWidth="1.5" />
                        <circle cx="0" cy="0" r="4" fill="#92400E" />
                      </g>

                      <rect x="65" y="135" width="40" height="15" fill="#78350F" />

                      <rect
                        x="45"
                        y="165"
                        width="80"
                        height="18"
                        rx="4"
                        fill={pumpStates.c3b ? "#DCFCE7" : "#FEE2E2"}
                        stroke={pumpStates.c3b ? "#16A34A" : "#DC2626"}
                        strokeWidth="1.2"
                      />
                      <text
                        x="85"
                        y="177"
                        textAnchor="middle"
                        fill={pumpStates.c3b ? "#15803D" : "#991B1B"}
                        fontSize="7.5"
                        fontWeight="bold"
                        fontFamily="monospace"
                      >
                        BL2 · ROOTS BLOWER
                      </text>
                    </svg>
                    <span className="text-[11px] font-mono font-bold text-slate-700 mt-1">3B: Twin-Lobe Roots Blower</span>
                  </div>
                </div>

                <div className="lg:col-span-5 flex flex-col justify-between h-full space-y-4">
                  <div>
                    <div className="flex items-center gap-2 text-sky-800 font-bold text-base">
                      <Activity className="w-5 h-5 text-sky-600" />
                      <span>Concept 3: Application-Tailored Machines</span>
                    </div>
                    <p className="text-xs text-slate-600 mt-2 leading-relaxed">
                      Instead of using the same icon for everything, each unit is rendered to mirror its real engineering type:
                    </p>
                  </div>
                </div>
              </div>
            )}

            {activePumpConcept === 4 && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
                <div className="lg:col-span-7 bg-white rounded-xl p-6 border border-sky-200/80 shadow-md flex flex-col items-center justify-center relative overflow-hidden">
                  <span className="absolute top-3 left-3 text-[10px] font-mono text-slate-400 font-bold uppercase tracking-wider">
                    Optical Sight-Glass Pump Face · Fluid Vortex Dynamic
                  </span>

                  <svg viewBox="0 0 360 220" className="w-full max-w-[360px] h-auto select-none">
                    <g transform="translate(180, 110)" className="cursor-pointer" onClick={() => togglePump("c4")}>
                      <circle cx="0" cy="0" r="70" fill="url(#metalRingGrad)" stroke="#64748B" strokeWidth="2" />
                      {[0, 45, 90, 135, 180, 225, 270, 315].map((deg) => (
                        <circle
                          key={deg}
                          cx={62 * Math.cos((deg * Math.PI) / 180)}
                          cy={62 * Math.sin((deg * Math.PI) / 180)}
                          r="2.5"
                          fill="#1E293B"
                          stroke="#94A3B8"
                          strokeWidth="0.8"
                        />
                      ))}

                      <circle cx="0" cy="0" r="54" fill="#0C4A6E" stroke="#38BDF8" strokeWidth="2" />

                      <g>
                        {isPlaying && pumpStates.c4 && (
                          <animateTransform
                            attributeName="transform"
                            type="rotate"
                            from="0"
                            to="360"
                            dur={`${0.45 / speed}s`}
                            repeatCount="indefinite"
                          />
                        )}
                        <path d="M 0 0 C 15 15, 30 5, 45 35" stroke="#BAE6FD" strokeWidth="2.5" fill="none" opacity="0.8" />
                        <path d="M 0 0 C -15 -15, -30 -5, -45 -35" stroke="#BAE6FD" strokeWidth="2.5" fill="none" opacity="0.8" />
                        <path d="M 0 0 C 15 -15, 5 -30, 35 -45" stroke="#7DD3FC" strokeWidth="2" fill="none" opacity="0.7" />
                        <path d="M 0 0 C -15 15, -5 30, -35 45" stroke="#7DD3FC" strokeWidth="2" fill="none" opacity="0.7" />

                        {[
                          { cx: 20, cy: 15, r: 2.2 },
                          { cx: -25, cy: 20, r: 1.8 },
                          { cx: 30, cy: -25, r: 2.5 },
                          { cx: -20, cy: -30, r: 2.0 },
                        ].map((b, i) => (
                          <circle key={i} cx={b.cx} cy={b.cy} r={b.r} fill="#FFFFFF" opacity="0.85" />
                        ))}

                        <circle cx="0" cy="0" r="10" fill="#0284C7" stroke="#FFFFFF" strokeWidth="1.5" />
                      </g>

                      <path d="M -42 -25 A 48 48 0 0 1 42 -25" stroke="#FFFFFF" strokeWidth="3" fill="none" opacity="0.55" strokeLinecap="round" />

                      <g transform="translate(0, 88)">
                        <rect x="-45" y="-10" width="90" height="22" rx="4" fill="#F0F9FF" stroke="#0284C7" strokeWidth="1" />
                        <text x="0" y="0" textAnchor="middle" fill="#0369A1" fontSize="8.5" fontWeight="bold" fontFamily="monospace">
                          SIGHT VOLUTE
                        </text>
                        <text x="0" y="8.5" textAnchor="middle" fill="#15803D" fontSize="6.5" fontWeight="bold" fontFamily="monospace">
                          {telemetry.flowRate} m³/h · CAVITATION: 0%
                        </text>
                      </g>
                    </g>
                  </svg>
                </div>

                <div className="lg:col-span-5 flex flex-col justify-between h-full space-y-4">
                  <div>
                    <div className="flex items-center gap-2 text-sky-800 font-bold text-base">
                      <Sliders className="w-5 h-5 text-sky-600" />
                      <span>Concept 4: Glass-Face Sight Volute</span>
                    </div>
                    <p className="text-xs text-slate-600 mt-2 leading-relaxed">
                      Transforms the pump casing into an optical polycarbonate sight-glass. Shows centrifugal fluid acceleration,
                      tangential stream discharge, and bubble cavitation dynamics inside the impeller eye.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
