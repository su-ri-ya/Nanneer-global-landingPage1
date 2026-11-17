"use client"

import React, { useState, useEffect } from "react"
import {
  Play,
  Pause,
  RotateCcw,
  Sliders,
  Info,
} from "lucide-react"

type PumpStatus = "RUNNING" | "STANDBY" | "STOPPED"

interface PumpState {
  id: string
  name: string
  code: string
  status: PumpStatus
  powerKw: number
  flowRate: number
}

export function ScadaSchematicSimulation() {
  const [isPlaying, setIsPlaying] = useState<boolean>(true)
  const [simSpeed, setSimSpeed] = useState<number>(1)
  const [controlMode, setControlMode] = useState<"AUTO" | "MANUAL">("AUTO")
  const [selectedAsset, setSelectedAsset] = useState<string | null>(null)

  // Live sensor readings with micro-jitter
  const [do1, setDo1] = useState<number>(0.88)
  const [do2, setDo2] = useState<number>(0.0)
  const [sbrTss, setSbrTss] = useState<number>(0.0)
  const [clarifierTss, setClarifierTss] = useState<number>(0.0)
  const [inletPressure, setInletPressure] = useState<number>(0.35)
  const [outletPressure, setOutletPressure] = useState<number>(0.15)
  const [softwaterHardness, setSoftwaterHardness] = useState<number>(0.0)

  // Tank levels
  const [collectionLevel, setCollectionLevel] = useState<number>(33)
  const [sbrLevel, setSbrLevel] = useState<number>(0)
  const [filterFeedLevel, setFilterFeedLevel] = useState<number>(50)
  const [sludgeLevel, setSludgeLevel] = useState<number>(0)
  const [treatedLevel, setTreatedLevel] = useState<number>(100)
  const [softWaterLevel, setSoftWaterLevel] = useState<number>(100)

  // Filter service timers in seconds
  const [psfSeconds, setPsfSeconds] = useState<number>(3 * 3600 + 20 * 60 + 24)
  const [acfSeconds, setAcfSeconds] = useState<number>(3 * 3600 + 20 * 60 + 25)

  // Valves state
  const [airSolenoidOpen, setAirSolenoidOpen] = useState<boolean>(true)
  const [clarifierValveOpen, setClarifierValveOpen] = useState<boolean>(true)
  const [waterSolenoidOpen, setWaterSolenoidOpen] = useState<boolean>(false)

  // Equipment Pumps State (Matching exact tags from reference)
  const [pumps, setPumps] = useState<Record<string, PumpState>>({
    M01: { id: "M01", name: "SBR RCP 1", code: "M01", status: "STANDBY", powerKw: 2.2, flowRate: 0 },
    M02: { id: "M02", name: "SBR RCP 2", code: "M02", status: "STANDBY", powerKw: 2.2, flowRate: 0 },
    M07: { id: "M07", name: "SBR RSTP 1", code: "M07", status: "RUNNING", powerKw: 3.7, flowRate: 15.2 },
    M08: { id: "M08", name: "SBR RSTP 2", code: "M08", status: "STANDBY", powerKw: 3.7, flowRate: 0 },
    M1: { id: "M1", name: "MBBR RSTP 1", code: "M1", status: "RUNNING", powerKw: 4.0, flowRate: 18.5 },
    M2: { id: "M2", name: "MBBR RSTP 2", code: "M2", status: "STOPPED", powerKw: 4.0, flowRate: 0 },
    M3: { id: "M3", name: "MBBR RCP 1", code: "M3", status: "STOPPED", powerKw: 1.5, flowRate: 0 },
    M4: { id: "M4", name: "MBBR RCP 2", code: "M4", status: "RUNNING", powerKw: 1.5, flowRate: 6.8 },
    M9: { id: "M9", name: "SBR DCTF", code: "M9", status: "STANDBY", powerKw: 2.2, flowRate: 0 },
    M10: { id: "M10", name: "FF PUMP 1", code: "M10", status: "STOPPED", powerKw: 3.0, flowRate: 0 },
    M11: { id: "M11", name: "FF PUMP 2", code: "M11", status: "STOPPED", powerKw: 3.0, flowRate: 0 },
    M12: { id: "M12", name: "FLUSHING PUMP", code: "M12", status: "STANDBY", powerKw: 5.5, flowRate: 0 },
    BL1: { id: "BL1", name: "BLOWER 1", code: "B1", status: "STOPPED", powerKw: 7.5, flowRate: 0 },
    BL2: { id: "BL2", name: "BLOWER 2", code: "B2", status: "RUNNING", powerKw: 7.5, flowRate: 120 },
    ARM: { id: "ARM", name: "CLARIFIER ARM", code: "ARM", status: "RUNNING", powerKw: 0.75, flowRate: 0 },
  })

  // Timer tick effect
  useEffect(() => {
    if (!isPlaying) return

    const interval = setInterval(() => {
      setPsfSeconds((prev) => prev + 1 * simSpeed)
      setAcfSeconds((prev) => prev + 1 * simSpeed)

      setDo1((prev) => {
        const jitter = (Math.random() - 0.48) * 0.02
        return parseFloat(Math.max(0.82, Math.min(0.95, prev + jitter)).toFixed(2))
      })

      setInletPressure((prev) => {
        const jitter = (Math.random() - 0.5) * 0.01
        return parseFloat(Math.max(0.32, Math.min(0.38, prev + jitter)).toFixed(2))
      })

      setOutletPressure((prev) => {
        const jitter = (Math.random() - 0.5) * 0.008
        return parseFloat(Math.max(0.13, Math.min(0.17, prev + jitter)).toFixed(2))
      })
    }, 1000 / simSpeed)

    return () => clearInterval(interval)
  }, [isPlaying, simSpeed])

  const formatTime = (totalSeconds: number) => {
    const hrs = Math.floor(totalSeconds / 3600)
    const mins = Math.floor((totalSeconds % 3600) / 60)
    const secs = totalSeconds % 60
    return `${hrs.toString().padStart(2, "0")}:${mins
      .toString()
      .padStart(2, "0")}:${secs.toString().padStart(2, "0")}`
  }

  const handleTogglePump = (id: string) => {
    if (controlMode !== "MANUAL") {
      setSelectedAsset(id)
      return
    }

    setPumps((prev) => {
      const current = prev[id]
      if (!current) return prev

      const nextStatus: PumpStatus =
        current.status === "RUNNING"
          ? "STOPPED"
          : current.status === "STOPPED"
          ? "STANDBY"
          : "RUNNING"

      return {
        ...prev,
        [id]: {
          ...current,
          status: nextStatus,
          flowRate: nextStatus === "RUNNING" ? current.powerKw * 3.5 : 0,
        },
      }
    })
    setSelectedAsset(id)
  }

  const getPumpColor = (status: PumpStatus) => {
    switch (status) {
      case "RUNNING":
        return "#16A34A"
      case "STANDBY":
        return "#D97706"
      case "STOPPED":
        return "#DC2626"
      default:
        return "#94A3B8"
    }
  }

  const getPumpFill = (status: PumpStatus) => {
    switch (status) {
      case "RUNNING":
        return "#DCFCE7"
      case "STANDBY":
        return "#FEF3C7"
      case "STOPPED":
        return "#FEE2E2"
      default:
        return "#F1F5F9"
    }
  }

  // 3D Industrial SCADA Pump Renderer with Metallic Casing, Spinning Turbine Impeller & LED Glow
  const renderPump = (
    id: string,
    cx: number,
    cy: number,
    arrowDir: "up" | "down" | "left" | "right",
    tagLine1: string,
    tagLine2?: string,
    tagPos: "top" | "bottom" = "bottom"
  ) => {
    const p = pumps[id] || { status: "STOPPED", code: id }
    const isRunning = p.status === "RUNNING"
    const color = getPumpColor(p.status)
    const fill = getPumpFill(p.status)

    // Flow arrow points relative to center
    let arrow = null
    if (arrowDir === "up") arrow = <polygon points="-3,-14 0,-20 3,-14" fill={color} />
    if (arrowDir === "down") arrow = <polygon points="-3,14 0,20 3,14" fill={color} />
    if (arrowDir === "left") arrow = <polygon points="-14,-3 -20,0 -14,3" fill={color} />
    if (arrowDir === "right") arrow = <polygon points="14,-3 20,0 14,3" fill={color} />

    return (
      <g
        id={`pump-${id}`}
        transform={`translate(${cx}, ${cy})`}
        className="cursor-pointer transition-transform duration-150 hover:scale-105"
        onClick={() => handleTogglePump(id)}
      >
        {/* Outer Metallic Bevel Ring */}
        <circle cx="0" cy="0" r="14" fill="url(#metalRingGrad)" stroke="#94A3B8" strokeWidth="1" filter="url(#softShadow)" />
        <circle cx="0" cy="0" r="11" fill={fill} stroke={color} strokeWidth="1.8" />

        {/* 4-Blade Spinning Impeller */}
        <g>
          {isPlaying && isRunning && (
            <animateTransform
              attributeName="transform"
              type="rotate"
              from="0"
              to="360"
              dur={`${0.6 / simSpeed}s`}
              repeatCount="indefinite"
            />
          )}
          <circle cx="0" cy="0" r="3.2" fill={color} />
          <line x1="-7.5" y1="0" x2="7.5" y2="0" stroke={color} strokeWidth="1.8" strokeLinecap="round" />
          <line x1="0" y1="-7.5" x2="0" y2="7.5" stroke={color} strokeWidth="1.8" strokeLinecap="round" />
          <line x1="-5" y1="-5" x2="5" y2="5" stroke={color} strokeWidth="1" strokeLinecap="round" opacity="0.45" />
          <line x1="-5" y1="5" x2="5" y2="-5" stroke={color} strokeWidth="1" strokeLinecap="round" opacity="0.45" />
        </g>

        {/* Glowing Status LED */}
        <circle cx="9" cy="-9" r="2.8" fill={color} stroke="#FFFFFF" strokeWidth="0.8">
          {isPlaying && isRunning && (
            <animate attributeName="opacity" values="0.7;1;0.7" dur="1s" repeatCount="indefinite" />
          )}
        </circle>

        {/* Pump ID Pill */}
        <rect x="-11" y="-4.5" width="22" height="9" rx="2" fill="#FFFFFF" opacity="0.92" />
        <text x="0" y="2.5" textAnchor="middle" fill="#0F172A" fontSize="7" fontWeight="bold">
          {p.code || id}
        </text>

        {/* Flow Arrow */}
        {arrow}

        {/* Pump Text Label */}
        {tagPos === "bottom" ? (
          <g transform="translate(0, 20)">
            <text x="0" y="0" textAnchor="middle" fill={color} fontSize="6" fontWeight="bold" fontFamily="monospace">
              {tagLine1}
            </text>
            {tagLine2 && (
              <text x="0" y="7" textAnchor="middle" fill={color} fontSize="6" fontWeight="bold" fontFamily="monospace">
                {tagLine2}
              </text>
            )}
          </g>
        ) : (
          <g transform={`translate(0, ${tagLine2 ? -18 : -11})`}>
            <text x="0" y="0" textAnchor="middle" fill={color} fontSize="6" fontWeight="bold" fontFamily="monospace">
              {tagLine1}
            </text>
            {tagLine2 && (
              <text x="0" y="7" textAnchor="middle" fill={color} fontSize="6" fontWeight="bold" fontFamily="monospace">
                {tagLine2}
              </text>
            )}
          </g>
        )}
      </g>
    )
  }

  return (
    <div className="w-full flex flex-col bg-white rounded-2xl overflow-hidden border border-sky-200/90 shadow-xl shadow-sky-950/5 font-sans select-none text-slate-900">
      {/* 1. SCADA Header / Control Deck */}
      <div className="px-4 py-2.5 bg-sky-50/70 border-b border-sky-100 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500" />
            </span>
            <div className="flex flex-col">
              <div className="flex items-center gap-2">
                <span className="font-mono text-xs sm:text-sm font-black tracking-wider uppercase text-sky-900">
                  SCADA MIMIC · STP PROCESS SCHEMATIC
                </span>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-100 text-emerald-800 border border-emerald-300 font-bold">
                  ONLINE
                </span>
              </div>
              <span className="text-[11px] text-slate-500 font-mono">
                System Tag: STP-NANNEER-PLANT-01 · Dual Biological Train &amp; Tertiary Polishing
              </span>
            </div>
          </div>
        </div>

        {/* Live Controls */}
        <div className="flex items-center gap-2 flex-wrap">
          <button
            onClick={() => setControlMode((prev) => (prev === "AUTO" ? "MANUAL" : "AUTO"))}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-mono font-bold border transition-colors ${
              controlMode === "AUTO"
                ? "bg-sky-100 text-sky-800 border-sky-300"
                : "bg-amber-100 text-amber-800 border-amber-300"
            }`}
          >
            <Sliders className="w-3.5 h-3.5" />
            <span>MODE: {controlMode}</span>
          </button>

          <div className="flex items-center bg-white rounded-md p-0.5 border border-sky-200 shadow-xs">
            {[1, 2, 5].map((speed) => (
              <button
                key={speed}
                onClick={() => setSimSpeed(speed)}
                className={`px-2 py-0.5 text-[10px] font-mono rounded ${
                  simSpeed === speed ? "bg-sky-600 text-white font-bold" : "text-slate-600 hover:text-slate-900"
                }`}
              >
                {speed}x
              </button>
            ))}
          </div>

          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className={`p-1.5 rounded-md border text-xs font-medium transition-colors ${
              isPlaying
                ? "bg-white border-slate-300 text-amber-700 hover:bg-slate-50"
                : "bg-emerald-600 border-emerald-500 text-white hover:bg-emerald-700"
            }`}
          >
            {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
          </button>

          <button
            onClick={() => {
              setPsfSeconds(3 * 3600 + 20 * 60 + 24)
              setAcfSeconds(3 * 3600 + 20 * 60 + 25)
              setDo1(0.88)
            }}
            className="p-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 hover:bg-slate-50 transition-colors shadow-xs"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* 2. Main SCADA SVG Canvas (1200 x 780 viewbox space) */}
      <div className="relative w-full aspect-[1200/780] bg-gradient-to-b from-white via-sky-50/25 to-white overflow-hidden">
        {/* Subtle Blueprint Dot Grid */}
        <div
          className="absolute inset-0 pointer-events-none opacity-35"
          style={{
            backgroundImage: `radial-gradient(circle at 1px 1px, #0284c718 1px, transparent 0)`,
            backgroundSize: "20px 20px",
          }}
        />

        <svg
          viewBox="0 0 1200 780"
          className="w-full h-full object-contain"
          preserveAspectRatio="xMidYMid meet"
        >
          <defs>
            {/* 1. Raw Sewage / Influent & Collection Tank Water (Murky Greyish-Brown Wastewater) */}
            <linearGradient id="rawSewageGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#A1887F" stopOpacity="0.88" />
              <stop offset="45%" stopColor="#8D6E63" stopOpacity="0.92" />
              <stop offset="100%" stopColor="#5D4037" stopOpacity="0.96" />
            </linearGradient>

            {/* 2. SBR Tank Mixed Liquor (Active Biological Digestion - Deep Brown MLSS) */}
            <linearGradient id="sbrWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#8D7B68" stopOpacity="0.88" />
              <stop offset="50%" stopColor="#6D5D4E" stopOpacity="0.92" />
              <stop offset="100%" stopColor="#4E3E32" stopOpacity="0.96" />
            </linearGradient>

            {/* 3. MBBR Aeration Tank (Aerated Mixed Liquor with Bio-Carriers - Brownish-Olive) */}
            <linearGradient id="mbbrWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#9E8D72" stopOpacity="0.85" />
              <stop offset="45%" stopColor="#6B7852" stopOpacity="0.90" />
              <stop offset="100%" stopColor="#4A5636" stopOpacity="0.95" />
            </linearGradient>

            {/* 4. Clarifier Tank with Arm (Phase Separation: Clarified Supernatant on top, Settling Sludge at bottom) */}
            <linearGradient id="clarifierWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#BAE6FD" stopOpacity="0.85" />
              <stop offset="40%" stopColor="#93C5FD" stopOpacity="0.82" />
              <stop offset="68%" stopColor="#8D6E63" stopOpacity="0.88" />
              <stop offset="100%" stopColor="#4E342E" stopOpacity="0.96" />
            </linearGradient>

            {/* 5. Sludge Holding Tank (Dense Thickened Waste Activated Sludge) */}
            <linearGradient id="sludgeWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#5D4037" stopOpacity="0.95" />
              <stop offset="50%" stopColor="#3E2723" stopOpacity="0.97" />
              <stop offset="100%" stopColor="#211109" stopOpacity="0.99" />
            </linearGradient>

            {/* 6. Filter Feed Tank (Settled Secondary Effluent - Translucent Pale Cyan) */}
            <linearGradient id="filterFeedGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#E0F2FE" stopOpacity="0.85" />
              <stop offset="50%" stopColor="#7DD3FC" stopOpacity="0.88" />
              <stop offset="100%" stopColor="#0284C7" stopOpacity="0.92" />
            </linearGradient>

            {/* 7. Treated Water Tank (Disinfected Clean Tertiary Water - Bright Sky-Blue) */}
            <linearGradient id="treatedWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#E0F2FE" stopOpacity="0.95" />
              <stop offset="45%" stopColor="#38BDF8" stopOpacity="0.92" />
              <stop offset="100%" stopColor="#0284C7" stopOpacity="0.95" />
            </linearGradient>

            {/* 8. Soft Water Tank (Pristine Polished Crystal Soft Water) */}
            <linearGradient id="softWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#F0F9FF" stopOpacity="0.98" />
              <stop offset="45%" stopColor="#38BDF8" stopOpacity="0.95" />
              <stop offset="100%" stopColor="#0369A1" stopOpacity="0.98" />
            </linearGradient>

            <linearGradient id="metalRingGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#FFFFFF" />
              <stop offset="40%" stopColor="#E2E8F0" />
              <stop offset="80%" stopColor="#CBD5E1" />
              <stop offset="100%" stopColor="#94A3B8" />
            </linearGradient>

            <linearGradient id="vesselGlassGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.9" />
              <stop offset="50%" stopColor="#F8FAFC" stopOpacity="0.6" />
              <stop offset="100%" stopColor="#F0F9FF" stopOpacity="0.4" />
            </linearGradient>

            <linearGradient id="specularSheen" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.35" />
              <stop offset="30%" stopColor="#FFFFFF" stopOpacity="0.1" />
              <stop offset="100%" stopColor="#FFFFFF" stopOpacity="0" />
            </linearGradient>

            <linearGradient id="filterVesselGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#0369A1" />
              <stop offset="25%" stopColor="#38BDF8" />
              <stop offset="50%" stopColor="#0284C7" />
              <stop offset="85%" stopColor="#0369A1" />
              <stop offset="100%" stopColor="#075985" />
            </linearGradient>

            <filter id="softShadow" x="-10%" y="-10%" width="120%" height="120%">
              <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#0B2545" floodOpacity="0.08" />
            </filter>

            <filter id="pipeShadow" x="-10%" y="-10%" width="120%" height="120%">
              <feDropShadow dx="0" dy="1" stdDeviation="1.5" floodColor="#0F172A" floodOpacity="0.06" />
            </filter>
          </defs>

          {/* ====================================================================== */}
          {/* PIPELINE NETWORK (100% FAITHFUL TO THE REFERENCE PHOTO)                */}
          {/* ====================================================================== */}

          {/* 1. RAW INFLUENT INLET (MURKY SEWAGE WATER) */}
          <path d="M 50 92 L 135 92" stroke="#8D6E63" strokeWidth="5" fill="none" strokeLinecap="round" />
          <polygon points="127,88 135,92 127,96" fill="#8D6E63" />
          {isPlaying && (
            <path d="M 50 92 L 135 92" stroke="#D7CCC8" strokeWidth="2.5" strokeDasharray="5 7" fill="none">
              <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
            </path>
          )}

          {/* 2. RED DRAIN & BACKWASH RETURN PIPELINE */}
          <g id="red-drain-pipeline">
            {/* From PSF Valve DRAIN port at (870, 495) going left */}
            <path d="M 870 495 L 600 495 L 600 460" stroke="#DC2626" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
            <polygon points="596,472 600,462 604,472" fill="#DC2626" />

            {/* From ACF Valve DRAIN port at (390, 480) going right */}
            <path d="M 390 480 L 490 480 L 490 460" stroke="#DC2626" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
            <polygon points="486,472 490,462 494,472" fill="#DC2626" />

            {/* Central horizontal manifold connecting both branches */}
            <path d="M 490 460 L 600 460" stroke="#DC2626" strokeWidth="4.5" fill="none" />

            {/* Central vertical red riser from y=460 up to y=390 */}
            <path d="M 545 460 L 545 390" stroke="#DC2626" strokeWidth="4.5" fill="none" />
            <polygon points="541,425 545,415 549,425" fill="#DC2626" />

            {/* Header running across above ACF to far left margin and cleanly into Collection Tank left side (y=68) */}
            <path d="M 545 390 L 75 390 L 75 68 L 135 68" stroke="#DC2626" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
            <polygon points="260,386 250,390 260,394" fill="#DC2626" />
            <polygon points="71,210 75,200 79,210" fill="#DC2626" />
            <polygon points="127,64 135,68 127,72" fill="#DC2626" />

            {/* Animated backwash flow */}
            {isPlaying && (
              <path
                d="M 870 495 L 600 495 L 600 460 L 545 460 L 545 390 L 75 390 L 75 68 L 135 68"
                stroke="#FCA5A5"
                strokeWidth="2.5"
                strokeDasharray="6 8"
                fill="none"
                strokeLinejoin="round"
              >
                <animate attributeName="stroke-dashoffset" from="56" to="0" dur={`${1.6 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 3. COLLECTION TANK TO SBR TANK (4 CONTINUOUS VERTICAL PIPES) */}
          <g id="collection-to-sbr-lines">
            <path d="M 160 135 L 160 240" stroke="#0284C7" strokeWidth="3.5" fill="none" />
            <path d="M 195 135 L 195 240" stroke="#0284C7" strokeWidth="3.5" fill="none" />
            <path d="M 235 135 L 235 240" stroke="#0284C7" strokeWidth="3.5" fill="none" />
            <path d="M 270 135 L 270 240" stroke="#0284C7" strokeWidth="3.5" fill="none" />
            {isPlaying && pumps.M07.status === "RUNNING" && (
              <path d="M 235 135 L 235 240" stroke="#D7CCC8" strokeWidth="2" strokeDasharray="4 6" fill="none">
                <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 4. COLLECTION TANK TO MBBR AERATION TANK (VIA M1 / M2) */}
          <g id="collection-to-mbbr-lines">
            <path d="M 310 92 L 340 92 L 340 75 L 420 75 L 420 92 L 440 92" stroke="#0284C7" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
            <path d="M 340 92 L 340 115 L 420 115 L 420 92" stroke="#0284C7" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
            <polygon points="430,88 440,92 430,96" fill="#0284C7" />
            {isPlaying && pumps.M1.status === "RUNNING" && (
              <path d="M 310 92 L 340 92 L 340 75 L 420 75 L 420 92 L 440 92" stroke="#D7CCC8" strokeWidth="2.5" strokeDasharray="5 7" fill="none" strokeLinejoin="round">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.9 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 5. MBBR AERATION OVERFLOW TO CLARIFIER TANK (RUNS ACROSS THE TOP AT Y=65, WELL ABOVE M3) */}
          <g id="mbbr-to-clarifier-line">
            <path d="M 570 65 L 740 65" stroke="#0284C7" strokeWidth="4.5" fill="none" />
            <polygon points="728,61 738,65 728,69" fill="#0284C7" />
            {isPlaying && (
              <path d="M 570 65 L 740 65" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="5 7" fill="none">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 6. CLARIFIER THROUGH CLARIFIER VALVE STRAIGHT DOWN INTO FILTER FEED TANK */}
          <g id="clarifier-to-filter-feed-line">
            <path d="M 810 135 L 810 240" stroke="#0284C7" strokeWidth="4.5" fill="none" />
            <polygon points="806,230 810,240 814,230" fill="#0284C7" />
            {isPlaying && clarifierValveOpen && (
              <path d="M 810 135 L 810 240" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="5 7" fill="none">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 7. CLARIFIER SLUDGE UNDERFLOW -> M3/M4 -> MBBR AERATION TANK & SLUDGE HOLDING TANK */}
          <g id="clarifier-to-sludge-lines">
            {/* Feeds from Clarifier bottom/left into M3 & M4 suction */}
            <path d="M 740 128 L 705 128 L 705 95 L 675 95" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
            <path d="M 705 128 L 675 128" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
            
            {/* From M3/M4 discharge to manifold at x=600 */}
            <path d="M 635 95 L 600 95" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
            <path d="M 635 128 L 600 128" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
            
            {/* 1. Downward branch into SLUDGE HOLDING TANK */}
            <path d="M 600 95 L 600 165" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
            <polygon points="596,155 600,165 604,155" fill="#D97706" />

            {/* 2. Recirculation branch into MBBR AERATION TANK (x=570, y=95) */}
            <path d="M 600 95 L 570 95" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
            <polygon points="578,91 570,95 578,99" fill="#D97706" />


            {isPlaying && pumps.M4.status === "RUNNING" && (
              <>
                <path d="M 740 128 L 705 128 L 600 128 L 600 165" stroke="#FDE68A" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${1.0 / simSpeed}s`} repeatCount="indefinite" />
                </path>
                <path d="M 600 128 L 600 95 L 570 95" stroke="#FDE68A" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              </>
            )}

            {isPlaying && pumps.M3.status === "RUNNING" && (
              <>
                <path d="M 740 128 L 705 128 L 705 95 L 570 95" stroke="#FDE68A" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.9 / simSpeed}s`} repeatCount="indefinite" />
                </path>
                <path d="M 600 95 L 600 165" stroke="#FDE68A" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${1.0 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              </>
            )}
          </g>

          {/* 8. SBR TANK TO FILTER FEED TANK (VIA PUMP M9 SBR DCTF AT Y=310 - COMPLETELY CLEAR OF SLUDGE TANK) */}
          <g id="sbr-to-filter-feed-line">
            <path d="M 295 310 L 740 310" stroke="#0284C7" strokeWidth="4.5" fill="none" />
            <polygon points="728,306 738,310 728,314" fill="#0284C7" />
            {isPlaying && pumps.M9.status === "RUNNING" && (
              <path d="M 295 310 L 740 310" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="5 7" fill="none">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.9 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 9. BLOWERS & COMPRESSED AIR PIPING NETWORK (YELLOW AIR DISTRIBUTED TO MBBR, COLLECTION TANK & SBR) */}
          <g id="yellow-air-network">
            {/* Main Blower output headers */}
            <path d="M 495 180 L 460 180 L 460 240 L 495 240" stroke="#D97706" strokeWidth="4" fill="none" strokeLinejoin="round" />
            
            {/* Branch 1: UP into MBBR Aeration Tank */}
            <path d="M 460 180 L 460 135" stroke="#D97706" strokeWidth="4" fill="none" />
            <polygon points="456,143 460,135 464,143" fill="#D97706" />

            {/* Branch 2: UP into COLLECTION TANK (Air mixing / agitation) */}
            <path d="M 460 195 L 295 195 L 295 135" stroke="#D97706" strokeWidth="4" fill="none" strokeLinejoin="round" />
            <polygon points="291,143 295,135 299,143" fill="#D97706" />

            {/* Branch 3: DOWN into SBR Tank via Air Solenoid */}
            <path d="M 460 240 L 460 275 L 390 275" stroke="#D97706" strokeWidth="4" fill="none" strokeLinejoin="round" />
            <path d="M 365 275 L 295 275" stroke="#D97706" strokeWidth="4" fill="none" />
            <polygon points="305,271 295,275 305,279" fill="#D97706" />

            {airSolenoidOpen && isPlaying && (
              <>
                {/* Air to SBR */}
                <path d="M 495 240 L 460 240 L 460 275 L 295 275" stroke="#FDE047" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                </path>
                {/* Air to MBBR */}
                <path d="M 460 240 L 460 135" stroke="#FDE047" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                </path>
                {/* Air to Collection Tank */}
                <path d="M 460 195 L 295 195 L 295 135" stroke="#FDE047" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              </>
            )}
          </g>

          {/* 10. FILTER FEED PUMPS (M10 & M11) DOWN TO INLET PRESSURE & PSF VALVE INLET */}
          <g id="filter-feed-to-psf-lines">
            <path d="M 780 325 L 780 350" stroke="#0284C7" strokeWidth="3.5" fill="none" />
            <path d="M 840 325 L 840 350" stroke="#0284C7" strokeWidth="3.5" fill="none" />
            <path d="M 780 380 L 780 405 L 810 405" stroke="#0284C7" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
            <path d="M 840 380 L 840 405 L 810 405" stroke="#0284C7" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
            {/* Feed line drops to y=420, passes horizontally right through 0.35 Bar, enters INLET at top of PSF Valve at (890, 445) */}
            <path d="M 810 405 L 810 420 L 890 420 L 890 445" stroke="#0284C7" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
            <polygon points="886,437 890,445 894,437" fill="#0284C7" />
            {isPlaying && (pumps.M10.status === "RUNNING" || pumps.M11.status === "RUNNING") && (
              <path
                d="M 810 405 L 810 420 L 890 420 L 890 445"
                stroke="#BAE6FD"
                strokeWidth="2.5"
                strokeDasharray="5 7"
                fill="none"
                strokeLinejoin="round"
              >
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.9 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 11. PSF VALVE TO/FROM PSF VESSEL (100% CONNECTED ZERO GAPS) */}
          <g id="psf-valve-to-vessel">
            {/* VIN: From right edge of PSF valve (930, 465) into left edge of PSF vessel (970, 465) */}
            <path d="M 930 465 L 970 465" stroke="#0284C7" strokeWidth="4" fill="none" />
            <polygon points="962,462 970,465 962,468" fill="#0284C7" />
            <text x="950" y="458" textAnchor="middle" fill="#0369A1" fontSize="7" fontWeight="bold" fontFamily="monospace">VIN</text>

            {/* VOUT: From left edge of PSF vessel (970, 495) into right edge of valve (930, 495) */}
            <path d="M 970 495 L 930 495" stroke="#0284C7" strokeWidth="4" fill="none" />
            <polygon points="938,492 930,495 938,498" fill="#0284C7" />
            <text x="950" y="508" textAnchor="middle" fill="#0369A1" fontSize="7" fontWeight="bold" fontFamily="monospace">VOUT</text>
          </g>

          {/* 12. PSF VALVE OUTLET THROUGH 0.15 Bar OUTLET PRESSURE, ACROSS TO ACF VALVE INLET */}
          <g id="psf-to-acf-line">
            {/* Exits bottom of PSF valve at (900, 505), drops to y=535, runs across left to x=360, turns UP into ACF VALVE INLET at (360, 505) */}
            <path d="M 900 505 L 900 535 L 360 535 L 360 505" stroke="#0284C7" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
            <polygon points="760,531 750,535 760,539" fill="#0284C7" />
            <polygon points="560,531 550,535 560,539" fill="#0284C7" />
            <polygon points="356,515 360,505 364,515" fill="#0284C7" />
            {isPlaying && (
              <path d="M 900 505 L 900 535 L 360 535 L 360 505" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="5 7" fill="none" strokeLinejoin="round">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${1.2 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 13. ACF VALVE TO/FROM ACF VESSEL (100% CONNECTED ZERO GAPS) */}
          <g id="acf-valve-to-vessel">
            {/* VIN: From left edge of valve (330, 465) into right edge of ACF vessel (275, 465) */}
            <path d="M 330 465 L 275 465" stroke="#0284C7" strokeWidth="4" fill="none" />
            <polygon points="283,462 275,465 283,468" fill="#0284C7" />
            <text x="302" y="458" textAnchor="middle" fill="#0369A1" fontSize="7" fontWeight="bold" fontFamily="monospace">VIN</text>

            {/* VOUT: From right edge of ACF vessel (275, 495) into left edge of valve (330, 495) */}
            <path d="M 275 495 L 330 495" stroke="#0284C7" strokeWidth="4" fill="none" />
            <polygon points="322,492 330,495 322,498" fill="#0284C7" />
            <text x="302" y="508" textAnchor="middle" fill="#0369A1" fontSize="7" fontWeight="bold" fontFamily="monospace">VOUT</text>
          </g>

          {/* 14. ACF VALVE OUTLET UP, LEFT ACROSS TOP OF ACF, DOWN INTO UV LIGHT */}
          <g id="acf-to-uv-line">
            {/* Exits OUTLET at top of ACF Valve (360, 450) with arrow UP ^, runs across above ACF at y=430, drops down at x=135 into UV Light at (135, 620) */}
            <path d="M 360 450 L 360 430 L 135 430 L 135 620" stroke="#0284C7" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
            <polygon points="356,442 360,432 364,442" fill="#0284C7" />
            <polygon points="230,426 220,430 230,434" fill="#0284C7" />
            <polygon points="131,540 135,550 139,540" fill="#0284C7" />
            {isPlaying && (
              <path d="M 360 450 L 360 430 L 135 430 L 135 620" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="5 7" fill="none" strokeLinejoin="round">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${1.0 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 15. UV LIGHT THROUGH DOSING PUMP INTO TREATED WATER TANK */}
          <g id="uv-to-treated-water-line">
            <path d="M 170 645 L 320 645" stroke="#0284C7" strokeWidth="4.5" fill="none" />
            <polygon points="195,641 205,645 195,649" fill="#0284C7" />
            <polygon points="305,641 315,645 305,649" fill="#0284C7" />
            {isPlaying && (
              <path d="M 170 645 L 320 645" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="5 7" fill="none">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 16. TREATED WATER TANK OUT THROUGH M12, TO FLUSH & INTO SOFTENER */}
          <g id="treated-to-softener-line">
            <path d="M 460 645 L 495 645 M 535 645 L 675 645" stroke="#0284C7" strokeWidth="4.5" fill="none" />
            <path d="M 565 645 L 565 590" stroke="#0284C7" strokeWidth="3.5" fill="none" />
            <polygon points="561,595 565,585 569,595" fill="#0284C7" />
            <polygon points="660,641 670,645 660,649" fill="#0284C7" />
          </g>

          {/* 17. SOFTENER OUT INTO SOFT WATER TANK */}
          <g id="softener-to-soft-water-line">
            <path d="M 755 645 L 840 645" stroke="#0284C7" strokeWidth="4.5" fill="none" />
            <polygon points="830,641 840,645 830,649" fill="#0284C7" />
          </g>

          {/* ====================================================================== */}
          {/* TANKS & VESSELS                                                        */}
          {/* ====================================================================== */}

          {/* TANK 1: COLLECTION TANK (RAW SEWAGE - MURKY BROWN WATER WITH AIR AGITATION) */}
          <g id="tank-collection" transform="translate(135, 50)" filter="url(#softShadow)">
            <rect x="0" y="0" width="175" height="85" rx="8" fill="url(#vesselGlassGrad)" stroke="#94A3B8" strokeWidth="1.5" />
            <path
              d={`M 3 ${85 - (85 * collectionLevel) / 100} Q 45 ${85 - (85 * collectionLevel) / 100 - 2} 88 ${85 - (85 * collectionLevel) / 100} T 172 ${85 - (85 * collectionLevel) / 100} L 172 82 L 3 82 Z`}
              fill="url(#rawSewageGrad)"
            />
            {/* Glass Highlight Sheen */}
            <rect x="4" y="24" width="20" height="55" rx="3" fill="url(#specularSheen)" />
            {isPlaying && (
              <g>
                {[
                  { cx: 35, cy: 75, r: 2.0, dur: "1.4s", delay: "0.1s" },
                  { cx: 80, cy: 78, r: 2.8, dur: "1.1s", delay: "0.3s" },
                  { cx: 125, cy: 75, r: 2.2, dur: "1.3s", delay: "0s" },
                  { cx: 155, cy: 78, r: 2.4, dur: "1.2s", delay: "0.2s" },
                ].map((b, i) => (
                  <circle key={i} cx={b.cx} cy={b.cy} r={b.r} fill="#D7CCC8" opacity="0.65">
                    <animate attributeName="cy" values={`${b.cy};58`} dur={`${parseFloat(b.dur) / simSpeed}s`} begin={b.delay} repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0.2;0.75;0" dur={`${parseFloat(b.dur) / simSpeed}s`} begin={b.delay} repeatCount="indefinite" />
                  </circle>
                ))}
              </g>
            )}
            <rect x="0" y="0" width="175" height="20" rx="8" fill="#F0F9FF" />
            <text x="87" y="14" textAnchor="middle" fill="#0369A1" fontSize="9" fontWeight="bold" fontFamily="monospace">
              COLLECTION TANK
            </text>
            <text x="87" y="52" textAnchor="middle" fill="#0F172A" fontSize="18" fontWeight="900" fontFamily="monospace">
              {collectionLevel}%
            </text>
            <rect x="105" y="24" width="62" height="13" rx="2" fill="#5D4037" opacity="0.9" />
            <text x="136" y="33.5" textAnchor="middle" fill="#FFFFFF" fontSize="6" fontWeight="bold" fontFamily="monospace">
              RAW SEWAGE
            </text>
          </g>

          {/* DOTTED BOUNDING BOX FOR SBR RCP / RSTP PUMPS */}
          <rect x="142" y="152" width="146" height="74" rx="4" fill="none" stroke="#93C5FD" strokeWidth="1" strokeDasharray="3 3" />

          {/* 4 PUMPS BELOW COLLECTION TANK: M01, M02, M07, M08 */}
          {renderPump("M01", 160, 187, "down", "SBR", "RCP 1", "bottom")}
          {renderPump("M02", 195, 187, "down", "SBR", "RCP 2", "bottom")}
          {renderPump("M07", 235, 187, "down", "SBR", "RSTP 1", "top")}
          {renderPump("M08", 270, 187, "down", "SBR", "RSTP 2", "top")}

          {/* TANK 2: SBR TANK (ACTIVE BIOLOGICAL DIGESTION - MLSS) */}
          <g id="tank-sbr" transform="translate(135, 240)" filter="url(#softShadow)">
            <rect x="0" y="0" width="165" height="90" rx="8" fill="url(#vesselGlassGrad)" stroke="#94A3B8" strokeWidth="1.5" />
            <rect x="3" y="22" width="159" height="65" rx="6" fill="url(#sbrWaterGrad)" opacity="0.35" />
            <rect x="4" y="24" width="18" height="60" rx="3" fill="url(#specularSheen)" />

            {/* Fine-Bubble Diffusers when Air Solenoid is Open */}
            {airSolenoidOpen && isPlaying && (
              <g>
                {[
                  { cx: 30, cy: 82, r: 2.0, dur: "1.1s", delay: "0s" },
                  { cx: 60, cy: 85, r: 2.5, dur: "0.9s", delay: "0.2s" },
                  { cx: 90, cy: 82, r: 2.0, dur: "1.2s", delay: "0.4s" },
                  { cx: 120, cy: 85, r: 2.8, dur: "1.0s", delay: "0.1s" },
                  { cx: 145, cy: 82, r: 2.2, dur: "0.8s", delay: "0.3s" },
                ].map((b, i) => (
                  <circle key={i} cx={b.cx} cy={b.cy} r={b.r} fill="#FDE047" opacity="0.8">
                    <animate attributeName="cy" values={`${b.cy};30`} dur={`${parseFloat(b.dur) / simSpeed}s`} begin={b.delay} repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0.3;0.9;0" dur={`${parseFloat(b.dur) / simSpeed}s`} begin={b.delay} repeatCount="indefinite" />
                  </circle>
                ))}
              </g>
            )}

            <rect x="0" y="0" width="165" height="20" rx="8" fill="#F0F9FF" />
            <text x="82" y="14" textAnchor="middle" fill="#0369A1" fontSize="9" fontWeight="bold" fontFamily="monospace">
              SBR TANK
            </text>
            <text x="82" y="46" textAnchor="middle" fill="#334155" fontSize="18" fontWeight="900" fontFamily="monospace">
              {sbrLevel}%
            </text>

            <g transform="translate(12, 60)">
              <rect x="0" y="0" width="65" height="15" rx="3" fill="#F0F9FF" stroke="#0284C7" strokeWidth="1" />
              <text x="32" y="11" textAnchor="middle" fill="#0369A1" fontSize="7" fontWeight="bold">
                {do2.toFixed(2)} mg/l DO2
              </text>
            </g>

            <g transform="translate(84, 60)">
              <rect x="0" y="0" width="70" height="15" rx="3" fill="#FAF5FF" stroke="#A855F7" strokeWidth="1" />
              <text x="35" y="11" textAnchor="middle" fill="#7E22CE" fontSize="6.5" fontWeight="bold">
                {sbrTss.toFixed(2)} mg/l TSS
              </text>
            </g>
          </g>

          {/* DOTTED BOUNDING BOX FOR MBBR RSTP PUMPS */}
          <rect x="340" y="50" width="90" height="92" rx="4" fill="none" stroke="#93C5FD" strokeWidth="1" strokeDasharray="3 3" />

          {/* PUMPS M1 & M2 (COLLECTION -> MBBR) */}
          {renderPump("M1", 385, 75, "right", "MBBR RSTP 1", undefined, "top")}
          {renderPump("M2", 385, 115, "right", "MBBR RSTP 2", undefined, "bottom")}

          {/* TANK 3: MBBR AERATION TANK (AERATED MIXED LIQUOR - BROWNISH-OLIVE BROTH WITH MOVING-BED MEDIA) */}
          <g id="tank-mbbr" transform="translate(430, 50)" filter="url(#softShadow)">
            <rect x="0" y="0" width="140" height="85" rx="8" fill="url(#vesselGlassGrad)" stroke="#0284C7" strokeWidth="2" />
            <rect x="3" y="22" width="134" height="60" rx="6" fill="url(#mbbrWaterGrad)" />
            <rect x="4" y="24" width="16" height="55" rx="3" fill="url(#specularSheen)" />

            {/* Moving Bed Biofilm Carrier Media Chips (Bobbing/Swirling with Microbe Carriers) */}
            {[
              { cx: 25, cy: 45, r: 3.2, dur: "3.2s" },
              { cx: 55, cy: 68, r: 3.8, dur: "2.8s" },
              { cx: 85, cy: 52, r: 3.0, dur: "3.5s" },
              { cx: 110, cy: 72, r: 3.5, dur: "2.5s" },
              { cx: 122, cy: 46, r: 2.8, dur: "3.0s" },
            ].map((m, i) => (
              <g key={`carrier-${i}`}>
                {isPlaying && (
                  <animateTransform
                    attributeName="transform"
                    type="translate"
                    values="0,0; 2,-4; -2,-8; 0,0"
                    dur={m.dur}
                    repeatCount="indefinite"
                  />
                )}
                <circle cx={m.cx} cy={m.cy} r={m.r} fill="#E2E8F0" stroke="#0284C7" strokeWidth="0.8" opacity="0.85" />
                <line x1={m.cx - 1.5} y1={m.cy} x2={m.cx + 1.5} y2={m.cy} stroke="#0284C7" strokeWidth="0.6" />
                <line x1={m.cx} y1={m.cy - 1.5} x2={m.cx} y2={m.cy + 1.5} stroke="#0284C7" strokeWidth="0.6" />
              </g>
            ))}

            {/* Multi-speed Fine-Bubble Aeration Diffusers */}
            {isPlaying && (
              <g>
                {[
                  { cx: 20, cy: 76, r: 2.2, dur: "1.1s", delay: "0s" },
                  { cx: 45, cy: 79, r: 3.2, dur: "0.9s", delay: "0.2s" },
                  { cx: 70, cy: 76, r: 2.0, dur: "1.3s", delay: "0.4s" },
                  { cx: 95, cy: 79, r: 2.8, dur: "1.0s", delay: "0.1s" },
                  { cx: 115, cy: 76, r: 2.4, dur: "0.8s", delay: "0.3s" },
                ].map((b, i) => (
                  <circle key={i} cx={b.cx} cy={b.cy} r={b.r} fill="#FFFFFF" opacity="0.85">
                    <animate attributeName="cy" values={`${b.cy};26`} dur={`${parseFloat(b.dur) / simSpeed}s`} begin={b.delay} repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0.3;0.95;0" dur={`${parseFloat(b.dur) / simSpeed}s`} begin={b.delay} repeatCount="indefinite" />
                  </circle>
                ))}
              </g>
            )}
            <rect x="0" y="0" width="140" height="20" rx="8" fill="#F0F9FF" />
            <text x="70" y="14" textAnchor="middle" fill="#0369A1" fontSize="8.5" fontWeight="bold" fontFamily="monospace">
              MBBR AERATION TANK
            </text>
            <g transform="translate(28, 42)">
              <rect x="0" y="0" width="84" height="18" rx="4" fill="#FFFFFF" stroke="#0284C7" strokeWidth="1.5" />
              <text x="42" y="13" textAnchor="middle" fill="#0284C7" fontSize="9.5" fontWeight="bold">
                {do1.toFixed(2)} mg/l DO1
              </text>
            </g>
          </g>

          {/* DOTTED BOUNDING BOX FOR SLUDGE RECIRCULATION PUMPS M3 & M4 */}
          <rect x="615" y="78" width="85" height="72" rx="4" fill="none" stroke="#93C5FD" strokeWidth="1" strokeDasharray="3 3" />

          {/* SLUDGE PUMPS M3 & M4 (POINTING LEFT, RECIRCULATING TO MBBR & WASTING TO SLUDGE TANK) */}
          {renderPump("M3", 655, 95, "left", "MBBR RCP 1", undefined, "top")}
          {renderPump("M4", 655, 128, "left", "MBBR RCP 2", undefined, "bottom")}

          {/* TANK 4: CLARIFIER TANK WITH ARM (PHASE SEPARATION - CLARIFIED WATER TOP, SETTLING SLUDGE BOTTOM) */}
          <g id="tank-clarifier" transform="translate(740, 50)" filter="url(#softShadow)">
            <rect x="0" y="0" width="140" height="85" rx="8" fill="url(#vesselGlassGrad)" stroke="#0284C7" strokeWidth="2" />
            <rect x="3" y="22" width="134" height="60" rx="6" fill="url(#clarifierWaterGrad)" />
            <rect x="4" y="24" width="16" height="55" rx="3" fill="url(#specularSheen)" />
            <rect x="0" y="0" width="140" height="20" rx="8" fill="#F0F9FF" />
            <text x="70" y="14" textAnchor="middle" fill="#0369A1" fontSize="8.5" fontWeight="bold" fontFamily="monospace">
              CLARIFIER TANK WITH ARM
            </text>

            <g transform="translate(70, 52)" className="cursor-pointer" onClick={() => handleTogglePump("ARM")}>
              <circle cx="0" cy="0" r="16" fill="url(#metalRingGrad)" stroke="#16A34A" strokeWidth="1.5" filter="url(#softShadow)" />
              <circle cx="0" cy="0" r="12" fill="#DCFCE7" stroke="#16A34A" strokeWidth="1.2" />
              <g>
                {isPlaying && pumps.ARM.status === "RUNNING" && (
                  <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur={`${2.5 / simSpeed}s`} repeatCount="indefinite" />
                )}
                <line x1="-11" y1="0" x2="11" y2="0" stroke="#15803D" strokeWidth="2.5" strokeLinecap="round" />
                <line x1="0" y1="-11" x2="0" y2="11" stroke="#15803D" strokeWidth="2.5" strokeLinecap="round" />
                {/* rake teeth */}
                <line x1="-8" y1="-2" x2="-8" y2="2" stroke="#15803D" strokeWidth="1.2" />
                <line x1="8" y1="-2" x2="8" y2="2" stroke="#15803D" strokeWidth="1.2" />
                <line x1="-2" y1="-8" x2="2" y2="-8" stroke="#15803D" strokeWidth="1.2" />
                <line x1="-2" y1="8" x2="2" y2="8" stroke="#15803D" strokeWidth="1.2" />
              </g>
              <circle cx="0" cy="0" r="3.5" fill="#15803D" />
              <text x="24" y="4" fill="#15803D" fontSize="8" fontWeight="bold">ARM</text>
            </g>
          </g>

          {/* TANK 5: SLUDGE HOLDING TANK (THICK DENSE WASTE ACTIVATED SLUDGE) */}
          <g id="tank-sludge" transform="translate(595, 165)" filter="url(#softShadow)">
            <rect x="0" y="0" width="115" height="65" rx="8" fill="url(#vesselGlassGrad)" stroke="#94A3B8" strokeWidth="1.5" />
            <rect x="3" y="38" width="109" height="24" rx="4" fill="url(#sludgeWaterGrad)" />
            <rect x="0" y="0" width="115" height="18" rx="8" fill="#F0F9FF" />
            <text x="57" y="13" textAnchor="middle" fill="#0369A1" fontSize="7.5" fontWeight="bold" fontFamily="monospace">
              SLUDGE HOLDING TANK
            </text>
            <text x="57" y="42" textAnchor="middle" fill="#FFFFFF" fontSize="15" fontWeight="900" fontFamily="monospace">
              {sludgeLevel}%
            </text>
          </g>

          {/* CLARIFIER EFFLUENT DROP INSTRUMENTS (TSS BADGE & CLARIFIER VALVE) */}
          <g transform="translate(825, 145)">
            <rect x="0" y="0" width="95" height="16" rx="3" fill="#FAF5FF" stroke="#A855F7" strokeWidth="1" />
            <text x="47" y="11.5" textAnchor="middle" fill="#7E22CE" fontSize="7" fontWeight="bold">
              {clarifierTss.toFixed(2)} mg/l TSS
            </text>
          </g>

          <g id="valve-clarifier" transform="translate(810, 185)" className="cursor-pointer" onClick={() => setClarifierValveOpen(!clarifierValveOpen)}>
            <circle cx="0" cy="0" r="13" fill="url(#metalRingGrad)" stroke="#16A34A" strokeWidth="1" filter="url(#softShadow)" />
            <circle cx="0" cy="0" r="10.5" fill="#DCFCE7" stroke="#16A34A" strokeWidth="1.8" />
            <text x="0" y="3.5" textAnchor="middle" fill="#15803D" fontSize="8" fontWeight="bold">V</text>
            <circle cx="7" cy="-7" r="2.2" fill="#16A34A" stroke="#FFFFFF" strokeWidth="0.6" />
            <text x="0" y="21" textAnchor="middle" fill="#15803D" fontSize="6.5" fontFamily="monospace">CLARIFIER VALVE</text>
          </g>

          {/* TANK 6: FILTER FEED TANK (SETTLED SECONDARY EFFLUENT - TRANSLUCENT CYAN) */}
          <g id="tank-filter-feed" transform="translate(740, 240)" filter="url(#softShadow)">
            <rect x="0" y="0" width="140" height="85" rx="8" fill="url(#vesselGlassGrad)" stroke="#0284C7" strokeWidth="2" />
            <path
              d={`M 3 ${85 - (85 * filterFeedLevel) / 100} Q 35 ${85 - (85 * filterFeedLevel) / 100 - 2} 70 ${85 - (85 * filterFeedLevel) / 100} T 137 ${85 - (85 * filterFeedLevel) / 100} L 137 82 L 3 82 Z`}
              fill="url(#filterFeedGrad)"
            />
            <rect x="4" y="24" width="16" height="55" rx="3" fill="url(#specularSheen)" />
            <rect x="0" y="0" width="140" height="20" rx="8" fill="#F0F9FF" />
            <text x="70" y="14" textAnchor="middle" fill="#0369A1" fontSize="8.5" fontWeight="bold" fontFamily="monospace">
              FILTER FEED TANK
            </text>
            <text x="70" y="52" textAnchor="middle" fill="#0F172A" fontSize="18" fontWeight="900" fontFamily="monospace">
              {filterFeedLevel}%
            </text>
          </g>

          {/* BLOWERS 1 & 2 (CLEAR VERTICAL STACK AT X=510, NO OVERLAP) */}
          <g id="blower-1" transform="translate(510, 180)" className="cursor-pointer" onClick={() => handleTogglePump("BL1")}>
            <circle cx="0" cy="0" r="14" fill="url(#metalRingGrad)" stroke="#F43F5E" strokeWidth="1" filter="url(#softShadow)" />
            <circle cx="0" cy="0" r="11" fill="#FCE7F3" stroke="#F43F5E" strokeWidth="1.8" />
            <g>
              <path d="M -5 0 L 5 0 M 0 -5 L 0 5 M -3.5 -3.5 L 3.5 3.5 M -3.5 3.5 L 3.5 -3.5" stroke="#BE123C" strokeWidth="1.6" strokeLinecap="round" />
            </g>
            <circle cx="9" cy="-9" r="2.5" fill="#DC2626" stroke="#FFFFFF" strokeWidth="0.6" />
            <text x="0" y="23" textAnchor="middle" fill="#475569" fontSize="7" fontFamily="monospace">BLOWER 1</text>
          </g>

          <g id="blower-2" transform="translate(510, 240)" className="cursor-pointer" onClick={() => handleTogglePump("BL2")}>
            <circle cx="0" cy="0" r="14" fill="url(#metalRingGrad)" stroke="#16A34A" strokeWidth="1" filter="url(#softShadow)" />
            <circle cx="0" cy="0" r="11" fill="#DCFCE7" stroke="#16A34A" strokeWidth="1.8" />
            <g>
              {isPlaying && pumps.BL2.status === "RUNNING" && (
                <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur={`${0.4 / simSpeed}s`} repeatCount="indefinite" />
              )}
              <path d="M -6 0 L 6 0 M 0 -6 L 0 6 M -4 -4 L 4 4 M -4 4 L 4 -4" stroke="#15803D" strokeWidth="1.8" strokeLinecap="round" />
            </g>
            <circle cx="9" cy="-9" r="2.5" fill="#16A34A" stroke="#FFFFFF" strokeWidth="0.6">
              {isPlaying && <animate attributeName="opacity" values="0.7;1;0.7" dur="1s" repeatCount="indefinite" />}
            </circle>
            <text x="0" y="23" textAnchor="middle" fill="#15803D" fontSize="7" fontFamily="monospace" fontWeight="bold">BLOWER 2</text>
          </g>

          {/* AIR SOLENOID VALVE */}
          <g id="valve-air-solenoid" transform="translate(390, 275)" className="cursor-pointer" onClick={() => setAirSolenoidOpen(!airSolenoidOpen)}>
            <circle cx="0" cy="0" r="13" fill="url(#metalRingGrad)" stroke="#D97706" strokeWidth="1" filter="url(#softShadow)" />
            <circle cx="0" cy="0" r="10.5" fill="#FEF3C7" stroke="#D97706" strokeWidth="1.8" />
            <text x="0" y="3.5" textAnchor="middle" fill="#92400E" fontSize="8" fontWeight="bold">V</text>
            <circle cx="7" cy="-7" r="2.2" fill={airSolenoidOpen ? "#16A34A" : "#DC2626"} stroke="#FFFFFF" strokeWidth="0.6" />
            <text x="0" y="21" textAnchor="middle" fill="#92400E" fontSize="6.5" fontFamily="monospace">AIR SOLENOID</text>
          </g>

          {/* SBR DCTF PUMP M9 (AT Y=310 ON SBR-TO-FFT LINE - 70PX BELOW BLOWER 2, ZERO OVERLAP) */}
          {renderPump("M9", 510, 310, "right", "SBR DCTF", undefined, "bottom")}

          {/* FILTER FEED PUMPS: M10 & M11 */}
          {renderPump("M10", 780, 365, "down", "FF PUMP 1", undefined, "top")}
          {renderPump("M11", 840, 365, "down", "FF PUMP 2", undefined, "top")}

          {/* ====================================================================== */}
          {/* BOTTOM SECTION: PSF, ACF, UV, DOSING, TREATED & SOFT WATER             */}
          {/* ====================================================================== */}

          {/* GREY DASHED BORDER AROUND ACF AREA */}
          <rect x="110" y="415" width="285" height="185" rx="6" fill="none" stroke="#CBD5E1" strokeWidth="1.5" strokeDasharray="4 4" />

          {/* INLET PRESSURE (0.35 Bar) */}
          <g transform="translate(740, 411)">
            <rect x="0" y="0" width="85" height="18" rx="4" fill="#F0F9FF" stroke="#0284C7" strokeWidth="1" />
            <text x="42" y="12" textAnchor="middle" fill="#0369A1" fontSize="8" fontWeight="bold">{inletPressure.toFixed(2)} Bar</text>
            <text x="42" y="28" textAnchor="middle" fill="#475569" fontSize="6" fontFamily="monospace">INLET PRESSURE</text>
          </g>

          {/* OUTLET PRESSURE (0.15 Bar) */}
          <g transform="translate(680, 526)">
            <rect x="0" y="0" width="85" height="18" rx="4" fill="#F0F9FF" stroke="#0284C7" strokeWidth="1" />
            <text x="42" y="12" textAnchor="middle" fill="#0369A1" fontSize="8" fontWeight="bold">{outletPressure.toFixed(2)} Bar</text>
            <text x="42" y="28" textAnchor="middle" fill="#475569" fontSize="6" fontFamily="monospace">OUTLET PRESSURE</text>
          </g>

          {/* PSF VALVE MULTIPORT BLOCK */}
          <g id="psf-valve-block" transform="translate(870, 445)">
            <rect x="0" y="0" width="60" height="55" rx="4" fill="#DCFCE7" stroke="#16A34A" strokeWidth="1.5" />
            <circle cx="30" cy="30" r="4" fill="#16A34A" />
            <text x="36" y="11" textAnchor="middle" fill="#15803D" fontSize="6.5" fontWeight="bold">PSF VALVE</text>
            <text x="20" y="20" textAnchor="middle" fill="#166534" fontSize="5.5" fontFamily="monospace" fontWeight="bold">INLET</text>
            <text x="46" y="22" fill="#166534" fontSize="5" fontFamily="monospace">VIN</text>
            <text x="8" y="48" fill="#DC2626" fontSize="5" fontFamily="monospace">DRAIN</text>
            <text x="44" y="48" fill="#166534" fontSize="5" fontFamily="monospace">VOUT</text>
            <text x="30" y="52" textAnchor="middle" fill="#0284C7" fontSize="5" fontFamily="monospace">OUTLET</text>
          </g>

          {/* PSF VESSEL (970, 430) */}
          <g id="vessel-psf" transform="translate(970, 430)" filter="url(#softShadow)">
            {/* 3D Pressure Vessel Body with Torispherical Heads */}
            <path d="M 0 15 Q 40 -8 80 15 L 80 115 Q 40 135 0 115 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="2" />
            {/* Specular Highlight Sheen */}
            <path d="M 12 18 Q 40 5 68 18 L 68 112 Q 40 128 12 112 Z" fill="url(#specularSheen)" opacity="0.6" />
            {/* Girth Weld Seams */}
            <line x1="0" y1="38" x2="80" y2="38" stroke="#38BDF8" strokeWidth="1" strokeDasharray="3 3" opacity="0.6" />
            <line x1="0" y1="95" x2="80" y2="95" stroke="#38BDF8" strokeWidth="1" strokeDasharray="3 3" opacity="0.6" />
            
            <text x="40" y="55" textAnchor="middle" fill="#FFFFFF" fontSize="16" fontWeight="900" fontFamily="sans-serif">PSF</text>
            <text x="40" y="68" textAnchor="middle" fill="#E0F2FE" fontSize="7" fontWeight="bold">FILTER SERVICE</text>
            <g transform="translate(8, 76)">
              <rect x="0" y="0" width="64" height="16" rx="3" fill="#F0FDF4" stroke="#16A34A" strokeWidth="1" />
              <text x="32" y="11" textAnchor="middle" fill="#15803D" fontSize="7" fontWeight="bold" fontFamily="monospace">
                {formatTime(psfSeconds)}
              </text>
              <text x="32" y="24" textAnchor="middle" fill="#64748B" fontSize="5.5" fontFamily="monospace">HH:MM:SS</text>
            </g>
          </g>

          {/* ACF VALVE MULTIPORT BLOCK */}
          <g id="acf-valve-block" transform="translate(330, 450)">
            <rect x="0" y="0" width="60" height="55" rx="4" fill="#DCFCE7" stroke="#16A34A" strokeWidth="1.5" />
            <circle cx="30" cy="27" r="4" fill="#16A34A" />
            <text x="30" y="11" textAnchor="middle" fill="#15803D" fontSize="7" fontWeight="bold">ACF VALVE</text>
            <text x="30" y="19" textAnchor="middle" fill="#0284C7" fontSize="5" fontFamily="monospace">OUTLET</text>
            <text x="8" y="22" fill="#166534" fontSize="5" fontFamily="monospace">VIN</text>
            <text x="42" y="35" fill="#DC2626" fontSize="5" fontFamily="monospace">DRAIN</text>
            <text x="8" y="48" fill="#166534" fontSize="5" fontFamily="monospace">VOUT</text>
            <text x="30" y="52" textAnchor="middle" fill="#166534" fontSize="5" fontFamily="monospace">INLET</text>
          </g>

          {/* ACF VESSEL (195, 430) */}
          <g id="vessel-acf" transform="translate(195, 430)" filter="url(#softShadow)">
            {/* 3D Pressure Vessel Body with Torispherical Heads */}
            <path d="M 0 15 Q 40 -8 80 15 L 80 115 Q 40 135 0 115 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="2" />
            {/* Specular Highlight Sheen */}
            <path d="M 12 18 Q 40 5 68 18 L 68 112 Q 40 128 12 112 Z" fill="url(#specularSheen)" opacity="0.6" />
            {/* Girth Weld Seams */}
            <line x1="0" y1="38" x2="80" y2="38" stroke="#38BDF8" strokeWidth="1" strokeDasharray="3 3" opacity="0.6" />
            <line x1="0" y1="95" x2="80" y2="95" stroke="#38BDF8" strokeWidth="1" strokeDasharray="3 3" opacity="0.6" />

            <text x="40" y="55" textAnchor="middle" fill="#FFFFFF" fontSize="16" fontWeight="900" fontFamily="sans-serif">ACF</text>
            <text x="40" y="68" textAnchor="middle" fill="#E0F2FE" fontSize="7" fontWeight="bold">FILTER SERVICE</text>
            <g transform="translate(8, 76)">
              <rect x="0" y="0" width="64" height="16" rx="3" fill="#F0FDF4" stroke="#16A34A" strokeWidth="1" />
              <text x="32" y="11" textAnchor="middle" fill="#15803D" fontSize="7" fontWeight="bold" fontFamily="monospace">
                {formatTime(acfSeconds)}
              </text>
              <text x="32" y="24" textAnchor="middle" fill="#64748B" fontSize="5.5" fontFamily="monospace">HH:MM:SS</text>
            </g>
          </g>

          {/* DOSING PUMP */}
          <g id="dosing-pump" transform="translate(230, 595)">
            <polygon points="16,0 32,9 32,27 16,36 0,27 0,9" fill="#DCFCE7" stroke="#16A34A" strokeWidth="2" filter="url(#softShadow)" />
            {/* Animated Stroke Diaphragm Pulse */}
            {isPlaying && (
              <circle cx="16" cy="18" r="6" fill="#16A34A" opacity="0.25">
                <animate attributeName="r" values="3;7;3" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                <animate attributeName="opacity" values="0.4;0.1;0.4" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
              </circle>
            )}
            <text x="16" y="16" textAnchor="middle" fill="#166534" fontSize="5.5" fontWeight="bold">DOSING</text>
            <text x="16" y="24" textAnchor="middle" fill="#15803D" fontSize="5.5" fontWeight="bold">PUMP</text>
            <line x1="16" y1="36" x2="16" y2="50" stroke="#16A34A" strokeWidth="2" />
            <polygon points="13,50 16,55 19,50" fill="#16A34A" />
          </g>

          {/* UV LIGHT */}
          <g id="uv-light" transform="translate(105, 620)">
            <rect x="0" y="0" width="65" height="38" rx="6" fill="#FAF5FF" stroke="#9333EA" strokeWidth="1.5" filter="url(#softShadow)" />
            {/* Animated UV Radiation Rays */}
            {isPlaying && (
              <rect x="4" y="4" width="57" height="30" rx="4" fill="#C084FC" opacity="0.15">
                <animate attributeName="opacity" values="0.1;0.35;0.1" dur={`${1.2 / simSpeed}s`} repeatCount="indefinite" />
              </rect>
            )}
            <line x1="8" y1="9" x2="57" y2="9" stroke="#A855F7" strokeWidth="3" strokeLinecap="round" />
            <line x1="8" y1="19" x2="57" y2="19" stroke="#16A34A" strokeWidth="3" strokeLinecap="round" />
            <line x1="8" y1="29" x2="57" y2="29" stroke="#A855F7" strokeWidth="3" strokeLinecap="round" />
            <text x="32.5" y="48" textAnchor="middle" fill="#7E22CE" fontSize="7.5" fontWeight="bold" fontFamily="monospace">UV LIGHT</text>
          </g>

          {/* TREATED WATER TANK */}
          <g id="tank-treated" transform="translate(320, 605)" filter="url(#softShadow)">
            <rect x="0" y="0" width="140" height="80" rx="8" fill="url(#vesselGlassGrad)" stroke="#0284C7" strokeWidth="2" />
            <path
              d={`M 3 ${80 - (80 * treatedLevel) / 100} Q 35 ${80 - (80 * treatedLevel) / 100 - 2} 70 ${80 - (80 * treatedLevel) / 100} T 137 ${80 - (80 * treatedLevel) / 100} L 137 77 L 3 77 Z`}
              fill="url(#treatedWaterGrad)"
            />
            <rect x="4" y="22" width="16" height="52" rx="3" fill="url(#specularSheen)" />
            <rect x="0" y="0" width="140" height="18" rx="8" fill="#F0F9FF" />
            <text x="70" y="13" textAnchor="middle" fill="#0369A1" fontSize="8" fontWeight="bold" fontFamily="monospace">
              TREATED WATER TANK
            </text>
            <text x="70" y="52" textAnchor="middle" fill="#0F172A" fontSize="18" fontWeight="900" fontFamily="monospace">
              {treatedLevel}%
            </text>
          </g>

          {/* M12: FLUSHING PUMP */}
          {renderPump("M12", 515, 645, "right", "FLUSHING PUMP", undefined, "bottom")}

          <text x="565" y="575" textAnchor="middle" fill="#0284C7" fontSize="8" fontWeight="bold" fontFamily="monospace">TO FLUSH</text>

          {/* WATER SOLENOID VALVE */}
          <g id="valve-water-solenoid" transform="translate(615, 645)" className="cursor-pointer" onClick={() => setWaterSolenoidOpen(!waterSolenoidOpen)}>
            <circle cx="0" cy="0" r="14" fill="url(#metalRingGrad)" stroke={waterSolenoidOpen ? "#16A34A" : "#DC2626"} strokeWidth="1" filter="url(#softShadow)" />
            <circle cx="0" cy="0" r="11" fill={waterSolenoidOpen ? "#DCFCE7" : "#FEE2E2"} stroke={waterSolenoidOpen ? "#16A34A" : "#DC2626"} strokeWidth="1.8" />
            <text x="0" y="3.5" textAnchor="middle" fill="#0F172A" fontSize="8.5" fontWeight="bold">V</text>
            <circle cx="8" cy="-8" r="2.5" fill={waterSolenoidOpen ? "#16A34A" : "#DC2626"} stroke="#FFFFFF" strokeWidth="0.6" />
            <text x="0" y="23" textAnchor="middle" fill="#991B1B" fontSize="6.5" fontFamily="monospace">WATER SOLENOID</text>
          </g>

          {/* SOFTENER VESSEL */}
          <g id="vessel-softener" transform="translate(675, 595)" filter="url(#softShadow)">
            {/* 3D Cylindrical Vessel Body */}
            <path d="M 0 15 Q 40 -8 80 15 L 80 95 Q 40 115 0 95 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="2" />
            <path d="M 12 18 Q 40 5 68 18 L 68 92 Q 40 108 12 92 Z" fill="url(#specularSheen)" opacity="0.6" />
            <line x1="0" y1="36" x2="80" y2="36" stroke="#38BDF8" strokeWidth="1" strokeDasharray="3 3" opacity="0.6" />
            <line x1="0" y1="75" x2="80" y2="75" stroke="#38BDF8" strokeWidth="1" strokeDasharray="3 3" opacity="0.6" />
            <text x="40" y="58" textAnchor="middle" fill="#FFFFFF" fontSize="11" fontWeight="900" fontFamily="monospace">SOFTENER</text>

            <g transform="translate(85, -15)">
              <rect x="0" y="0" width="85" height="15" rx="3" fill="#FAF5FF" stroke="#A855F7" strokeWidth="1" />
              <text x="42" y="11" textAnchor="middle" fill="#7E22CE" fontSize="7" fontWeight="bold">
                {softwaterHardness.toFixed(2)} mg/l
              </text>
              <text x="42" y="24" textAnchor="middle" fill="#475569" fontSize="5.5" fontFamily="monospace">SOFTWATER TOTAL HARDNESS</text>
            </g>
          </g>

          {/* SOFT WATER TANK (PRISTINE POLISHED CRYSTAL SOFT WATER) */}
          <g id="tank-soft-water" transform="translate(840, 605)" filter="url(#softShadow)">
            <rect x="0" y="0" width="140" height="80" rx="8" fill="url(#vesselGlassGrad)" stroke="#0284C7" strokeWidth="2" />
            <path
              d={`M 3 ${80 - (80 * softWaterLevel) / 100} Q 35 ${80 - (80 * softWaterLevel) / 100 - 2} 70 ${80 - (80 * softWaterLevel) / 100} T 137 ${80 - (80 * softWaterLevel) / 100} L 137 77 L 3 77 Z`}
              fill="url(#softWaterGrad)"
            />
            <rect x="4" y="22" width="16" height="52" rx="3" fill="url(#specularSheen)" />
            <rect x="0" y="0" width="140" height="18" rx="8" fill="#F0F9FF" />
            <text x="70" y="13" textAnchor="middle" fill="#0369A1" fontSize="8" fontWeight="bold" fontFamily="monospace">
              SOFT WATER TANK
            </text>
            <text x="70" y="52" textAnchor="middle" fill="#0F172A" fontSize="18" fontWeight="900" fontFamily="monospace">
              {softWaterLevel}%
            </text>
            <rect x="8" y="62" width="65" height="12" rx="2" fill="#0284C7" opacity="0.9" />
            <text x="40" y="71" textAnchor="middle" fill="#FFFFFF" fontSize="5.5" fontWeight="bold" fontFamily="monospace">
              POLISHED WATER
            </text>
          </g>
        </svg>
      </div>

      {/* 2.5 Water Purification Progression Indicator */}
      <div className="px-4 py-2 bg-gradient-to-r from-stone-100 via-sky-50 to-cyan-50 border-t border-sky-100 flex flex-wrap items-center justify-between gap-2 text-[11px] font-mono">
        <div className="flex items-center gap-1.5 font-bold text-slate-700">
          <span className="w-2 h-2 rounded-full bg-sky-500 animate-pulse" />
          <span>PURIFICATION PROGRESSION:</span>
        </div>
        <div className="flex items-center gap-2 flex-wrap text-[10px]">
          <span className="flex items-center gap-1 px-2 py-0.5 rounded bg-stone-200 text-stone-800 border border-stone-300 font-semibold">
            <span className="w-2.5 h-2.5 rounded-full bg-[#8D6E63] border border-stone-400" />
            1. Raw Sewage
          </span>
          <span className="text-slate-400 font-bold">→</span>
          <span className="flex items-center gap-1 px-2 py-0.5 rounded bg-amber-50 text-amber-900 border border-amber-200 font-semibold">
            <span className="w-2.5 h-2.5 rounded-full bg-[#6B7852] border border-amber-400" />
            2. Biological MLSS
          </span>
          <span className="text-slate-400 font-bold">→</span>
          <span className="flex items-center gap-1 px-2 py-0.5 rounded bg-sky-100 text-sky-900 border border-sky-200 font-semibold">
            <span className="w-2.5 h-2.5 rounded-full bg-[#7DD3FC] border border-sky-400" />
            3. Clarified Effluent
          </span>
          <span className="text-slate-400 font-bold">→</span>
          <span className="flex items-center gap-1 px-2 py-0.5 rounded bg-cyan-100 text-cyan-900 border border-cyan-200 font-semibold">
            <span className="w-2.5 h-2.5 rounded-full bg-[#38BDF8] border border-cyan-400" />
            4. Media Filtered
          </span>
          <span className="text-slate-400 font-bold">→</span>
          <span className="flex items-center gap-1 px-2 py-0.5 rounded bg-emerald-50 text-emerald-900 border border-emerald-200 font-bold">
            <span className="w-2.5 h-2.5 rounded-full bg-[#0284C7] border border-emerald-400" />
            5. Pure Soft Water
          </span>
        </div>
      </div>

      {/* 3. SCADA Bottom Telemetry Bar */}
      <div className="px-4 py-2.5 bg-sky-50/50 border-t border-sky-100 grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2.5 text-xs">
        <div className="p-2 rounded-lg bg-white border border-sky-100 shadow-xs flex flex-col">
          <span className="text-[10px] text-slate-500 uppercase font-mono">Aeration DO1</span>
          <span className="text-sm font-bold text-sky-700 font-mono">{do1.toFixed(2)} mg/L</span>
          <span className="text-[9px] text-emerald-600 font-medium">Normal (0.5–2.0)</span>
        </div>

        <div className="p-2 rounded-lg bg-white border border-sky-100 shadow-xs flex flex-col">
          <span className="text-[10px] text-slate-500 uppercase font-mono">SBR TSS</span>
          <span className="text-sm font-bold text-purple-700 font-mono">{sbrTss.toFixed(2)} mg/L</span>
          <span className="text-[9px] text-slate-500">Idle Cycle</span>
        </div>

        <div className="p-2 rounded-lg bg-white border border-sky-100 shadow-xs flex flex-col">
          <span className="text-[10px] text-slate-500 uppercase font-mono">Clarifier TSS</span>
          <span className="text-sm font-bold text-purple-700 font-mono">{clarifierTss.toFixed(2)} mg/L</span>
          <span className="text-[9px] text-slate-500">Underflow OK</span>
        </div>

        <div className="p-2 rounded-lg bg-white border border-sky-100 shadow-xs flex flex-col">
          <span className="text-[10px] text-slate-500 uppercase font-mono">PSF Differential</span>
          <span className="text-sm font-bold text-emerald-700 font-mono">
            {(inletPressure - outletPressure).toFixed(2)} Bar
          </span>
          <span className="text-[9px] text-slate-500">In: {inletPressure} · Out: {outletPressure}</span>
        </div>

        <div className="p-2 rounded-lg bg-white border border-sky-100 shadow-xs flex flex-col">
          <span className="text-[10px] text-slate-500 uppercase font-mono">PSF Service</span>
          <span className="text-sm font-bold text-emerald-700 font-mono">{formatTime(psfSeconds)}</span>
          <span className="text-[9px] text-slate-500">Backwash in 20h</span>
        </div>

        <div className="p-2 rounded-lg bg-white border border-sky-100 shadow-xs flex flex-col">
          <span className="text-[10px] text-slate-500 uppercase font-mono">ACF Service</span>
          <span className="text-sm font-bold text-emerald-700 font-mono">{formatTime(acfSeconds)}</span>
          <span className="text-[9px] text-slate-500">Adsorption active</span>
        </div>

        <div className="p-2 rounded-lg bg-white border border-sky-100 shadow-xs flex flex-col">
          <span className="text-[10px] text-slate-500 uppercase font-mono">Softener Hardness</span>
          <span className="text-sm font-bold text-emerald-700 font-mono">{softwaterHardness.toFixed(2)} mg/L</span>
          <span className="text-[9px] text-emerald-600 font-medium">Zero Hardness</span>
        </div>
      </div>

      {/* 4. Asset Inspector Bar */}
      <div className="px-4 py-2 bg-slate-50 border-t border-sky-100 flex flex-wrap items-center justify-between text-xs text-slate-600 gap-2">
        <div className="flex items-center gap-4 flex-wrap text-[11px] font-mono">
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block" />
            <span className="text-slate-700 font-semibold">RUNNING</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block" />
            <span className="text-slate-700 font-semibold">STANDBY</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block" />
            <span className="text-slate-700 font-semibold">STOPPED</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-1 bg-sky-500 inline-block" />
            <span className="text-slate-700">Process Water</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-1 bg-amber-500 inline-block" />
            <span className="text-slate-700">Compressed Air</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-1 bg-rose-500 inline-block" />
            <span className="text-slate-700">Drain / Backwash</span>
          </span>
        </div>

        {selectedAsset && (
          <div className="flex items-center gap-2 bg-sky-100 px-2 py-0.5 rounded text-[11px] font-mono text-sky-800 border border-sky-200">
            <Info className="w-3 h-3" />
            <span>
              Asset: {pumps[selectedAsset]?.name || selectedAsset} · State: {pumps[selectedAsset]?.status}
              {controlMode === "MANUAL" ? " (Click to toggle)" : " (Switch to MANUAL mode to toggle)"}
            </span>
          </div>
        )}
      </div>
    </div>
  )
}
