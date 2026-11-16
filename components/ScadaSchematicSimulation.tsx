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
            <linearGradient id="lightTankWater" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#BAE6FD" stopOpacity="0.85" />
              <stop offset="50%" stopColor="#38BDF8" stopOpacity="0.9" />
              <stop offset="100%" stopColor="#0284C7" stopOpacity="0.95" />
            </linearGradient>

            <linearGradient id="treatedWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#E0F2FE" stopOpacity="0.95" />
              <stop offset="50%" stopColor="#7DD3FC" stopOpacity="0.9" />
              <stop offset="100%" stopColor="#0369A1" stopOpacity="0.95" />
            </linearGradient>

            <linearGradient id="filterVesselGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#0369A1" />
              <stop offset="45%" stopColor="#0284C7" />
              <stop offset="80%" stopColor="#0369A1" />
              <stop offset="100%" stopColor="#075985" />
            </linearGradient>

            <filter id="softShadow" x="-10%" y="-10%" width="120%" height="120%">
              <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#0B2545" floodOpacity="0.08" />
            </filter>
          </defs>

          {/* ====================================================================== */}
          {/* PIPELINE NETWORK (100% FAITHFUL TO THE REFERENCE PHOTO)                */}
          {/* ====================================================================== */}

          {/* 1. RAW INFLUENT INLET (Left edge into Collection Tank) */}
          <path d="M 60 95 L 160 95" stroke="#0284C7" strokeWidth="5" fill="none" strokeLinecap="round" />
          <polygon points="150,91 160,95 150,99" fill="#0284C7" />
          {isPlaying && (
            <path d="M 60 95 L 160 95" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="5 7" fill="none">
              <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
            </path>
          )}

          {/* 2. RED DRAIN & BACKWASH RETURN PIPELINE */}
          {/* PSF DRAIN & ACF DRAIN join into vertical red riser -> horizontal across above ACF -> up far left edge into Collection Tank */}
          <g id="red-drain-pipeline">
            {/* From PSF Valve DRAIN port at (810, 520) */}
            <path d="M 810 500 L 810 520 L 485 520" stroke="#DC2626" strokeWidth="5" fill="none" strokeLinejoin="round" />
            <polygon points="730,516 720,520 730,524" fill="#DC2626" />

            {/* From ACF Valve DRAIN port at (365, 500) */}
            <path d="M 365 500 L 365 520 L 485 520" stroke="#DC2626" strokeWidth="5" fill="none" strokeLinejoin="round" />
            <polygon points="410,516 420,520 410,524" fill="#DC2626" />

            {/* Central vertical red riser from y=520 up to y=405 */}
            <path d="M 485 520 L 485 405 L 100 405 L 100 65 L 180 65" stroke="#DC2626" strokeWidth="5" fill="none" strokeLinejoin="round" />
            <polygon points="481,460 485,450 489,460" fill="#DC2626" />
            <polygon points="481,420 485,410 489,420" fill="#DC2626" />
            <polygon points="260,401 250,405 260,409" fill="#DC2626" />
            <polygon points="96,230 100,220 104,230" fill="#DC2626" />
            <polygon points="172,61 180,65 172,69" fill="#DC2626" />

            {/* Animated backwash flow */}
            <path
              d="M 810 520 L 485 520 L 485 405 L 100 405 L 100 65 L 180 65"
              stroke="#FCA5A5"
              strokeWidth="2.5"
              strokeDasharray="6 8"
              fill="none"
              strokeLinejoin="round"
            >
              {isPlaying && (
                <animate attributeName="stroke-dashoffset" from="56" to="0" dur={`${1.6 / simSpeed}s`} repeatCount="indefinite" />
              )}
            </path>
          </g>

          {/* 3. COLLECTION TANK TO SBR TANK (4 CONTINUOUS VERTICAL PIPES) */}
          <g id="collection-to-sbr-lines">
            <path d="M 180 145 L 180 230" stroke="#0284C7" strokeWidth="4" fill="none" />
            <path d="M 215 145 L 215 230" stroke="#0284C7" strokeWidth="4" fill="none" />
            <path d="M 250 145 L 250 230" stroke="#0284C7" strokeWidth="4" fill="none" />
            {isPlaying && pumps.M07.status === "RUNNING" && (
              <path d="M 250 145 L 250 230" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="4 6" fill="none">
                <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
            <path d="M 285 145 L 285 230" stroke="#0284C7" strokeWidth="4" fill="none" />
          </g>

          {/* 4. COLLECTION TANK TO MBBR AERATION TANK (VIA M1 / M2) */}
          <g id="collection-to-mbbr-lines">
            <path d="M 300 95 L 335 95 L 335 75 L 415 75 L 415 95 L 440 95" stroke="#0284C7" strokeWidth="5" fill="none" strokeLinejoin="round" />
            <path d="M 335 95 L 335 115 L 415 115 L 415 95" stroke="#0284C7" strokeWidth="5" fill="none" strokeLinejoin="round" />
            <polygon points="425,91 435,95 425,99" fill="#0284C7" />
            {isPlaying && pumps.M1.status === "RUNNING" && (
              <path d="M 300 95 L 335 95 L 335 75 L 415 75 L 415 95 L 440 95" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="5 7" fill="none" strokeLinejoin="round">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.9 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 5. MBBR AERATION OVERFLOW TO CLARIFIER TANK */}
          <g id="mbbr-to-clarifier-line">
            <path d="M 580 95 L 720 95" stroke="#0284C7" strokeWidth="5" fill="none" />
            <polygon points="710,91 720,95 710,99" fill="#0284C7" />
            {isPlaying && (
              <path d="M 580 95 L 720 95" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="5 7" fill="none">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 6. CLARIFIER THROUGH CLARIFIER VALVE STRAIGHT DOWN INTO FILTER FEED TANK */}
          <g id="clarifier-to-filter-feed-line">
            <path d="M 785 145 L 785 230" stroke="#0284C7" strokeWidth="5" fill="none" />
            <polygon points="781,222 785,230 789,222" fill="#0284C7" />
            {isPlaying && clarifierValveOpen && (
              <path d="M 785 145 L 785 230" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="5 7" fill="none">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 7. CLARIFIER / MBBR UNDERFLOW TO M3 & M4, THEN DROPPING INTO SLUDGE HOLDING TANK */}
          <g id="clarifier-to-sludge-lines">
            {/* Sludge line coming from underflow, branching left into M3 & M4 */}
            <path d="M 720 120 L 685 120 L 685 140 L 610 140" stroke="#D97706" strokeWidth="4" fill="none" strokeLinejoin="round" />
            <path d="M 685 120 L 685 175 L 610 175" stroke="#D97706" strokeWidth="4" fill="none" strokeLinejoin="round" />
            {/* Header after M3 & M4 turning DOWN into top of Sludge Holding Tank */}
            <path d="M 610 140 L 595 140 L 595 195" stroke="#D97706" strokeWidth="4" fill="none" strokeLinejoin="round" />
            <path d="M 610 175 L 595 175" stroke="#D97706" strokeWidth="4" fill="none" strokeLinejoin="round" />
            <polygon points="591,188 595,195 599,188" fill="#D97706" />

            {isPlaying && pumps.M4.status === "RUNNING" && (
              <path d="M 685 175 L 595 175 L 595 195" stroke="#FDE68A" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${1.0 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 8. SBR TANK TO FILTER FEED TANK (VIA PUMP M9 SBR DCTF AT Y=370) */}
          <g id="sbr-to-filter-feed-line">
            <path d="M 310 275 L 330 275 L 330 370 L 720 370 L 720 290" stroke="#0284C7" strokeWidth="4" fill="none" strokeLinejoin="round" />
            <polygon points="716,298 720,290 724,298" fill="#0284C7" />
          </g>

          {/* 9. BLOWERS & COMPRESSED AIR PIPING NETWORK (YELLOW) */}
          <g id="yellow-air-network">
            <path d="M 525 275 L 485 275 L 485 325 L 525 325" stroke="#D97706" strokeWidth="4" fill="none" strokeLinejoin="round" />
            <path d="M 485 275 L 485 145 L 510 145" stroke="#D97706" strokeWidth="4" fill="none" strokeLinejoin="round" />
            <path d="M 485 325 L 425 325" stroke="#D97706" strokeWidth="4" fill="none" strokeLinejoin="round" />
            <path d="M 395 325 L 310 325" stroke="#D97706" strokeWidth="4" fill="none" />

            {airSolenoidOpen && isPlaying && (
              <>
                <path d="M 525 325 L 485 325 L 310 325" stroke="#FDE047" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                </path>
                <path d="M 485 325 L 485 145 L 510 145" stroke="#FDE047" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              </>
            )}
          </g>

          {/* 10. FILTER FEED PUMPS (M10 & M11) DOWN TO INLET PRESSURE & PSF VALVE */}
          <g id="filter-feed-to-psf-lines">
            <path d="M 760 315 L 760 340" stroke="#0284C7" strokeWidth="4" fill="none" />
            <path d="M 810 315 L 810 340" stroke="#0284C7" strokeWidth="4" fill="none" />
            <path d="M 760 370 L 760 395 L 785 395" stroke="#0284C7" strokeWidth="4" fill="none" strokeLinejoin="round" />
            <path d="M 810 370 L 810 395 L 785 395" stroke="#0284C7" strokeWidth="4" fill="none" strokeLinejoin="round" />
            {/* Down into INLET PRESSURE (0.35 Bar) and PSF Valve INLET */}
            <path d="M 785 395 L 785 450 L 815 450" stroke="#0284C7" strokeWidth="5" fill="none" strokeLinejoin="round" />
            <polygon points="805,446 815,450 805,454" fill="#0284C7" />
          </g>

          {/* 11. PSF VALVE TO/FROM PSF VESSEL */}
          <g id="psf-valve-to-vessel">
            {/* VIN: From valve top into PSF vessel top */}
            <path d="M 870 465 L 910 465" stroke="#0284C7" strokeWidth="4" fill="none" />
            <polygon points="902,462 910,465 902,468" fill="#0284C7" />
            {/* VOUT: From PSF vessel bottom into valve bottom */}
            <path d="M 910 520 L 870 520" stroke="#0284C7" strokeWidth="4" fill="none" />
            <polygon points="878,517 870,520 878,523" fill="#0284C7" />
          </g>

          {/* 12. PSF VALVE OUTLET THROUGH 0.15 Bar OUTLET PRESSURE, ACROSS TO ACF VALVE INLET */}
          <g id="psf-to-acf-line">
            {/* Exits PSF OUTLET, passes through 0.15 Bar, runs horizontally LEFT, turns UP into ACF VALVE INLET */}
            <path d="M 815 495 L 325 495 L 325 480" stroke="#0284C7" strokeWidth="5" fill="none" strokeLinejoin="round" />
            <polygon points="535,491 525,495 535,499" fill="#0284C7" />
            <polygon points="321,488 325,480 329,488" fill="#0284C7" />
            {isPlaying && (
              <path d="M 815 495 L 325 495 L 325 480" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="5 7" fill="none" strokeLinejoin="round">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${1.2 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 13. ACF VALVE TO/FROM ACF VESSEL */}
          <g id="acf-valve-to-vessel">
            {/* VIN: From valve left into ACF vessel top */}
            <path d="M 295 460 L 255 460" stroke="#0284C7" strokeWidth="4" fill="none" />
            <polygon points="263,457 255,460 263,463" fill="#0284C7" />
            {/* VOUT: From ACF vessel bottom into valve left */}
            <path d="M 255 520 L 295 520" stroke="#0284C7" strokeWidth="4" fill="none" />
            <polygon points="287,517 295,520 287,523" fill="#0284C7" />
          </g>

          {/* 14. ACF VALVE OUTLET UP, LEFT ACROSS TOP OF ACF, DOWN INTO UV LIGHT */}
          <g id="acf-to-uv-line">
            {/* Exits OUTLET of ACF Valve with arrow UP ^, turns LEFT across ACF, drops DOWN v into UV Light */}
            <path d="M 335 440 L 335 425 L 120 425 L 120 620" stroke="#0284C7" strokeWidth="5" fill="none" strokeLinejoin="round" />
            <polygon points="331,433 335,425 339,433" fill="#0284C7" />
            <polygon points="230,421 220,425 230,429" fill="#0284C7" />
            <polygon points="116,530 120,540 124,530" fill="#0284C7" />
            {isPlaying && (
              <path d="M 335 440 L 335 425 L 120 425 L 120 620" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="5 7" fill="none" strokeLinejoin="round">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${1.0 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 15. UV LIGHT THROUGH DOSING PUMP INTO TREATED WATER TANK */}
          <g id="uv-to-treated-water-line">
            <path d="M 155 635 L 320 635" stroke="#0284C7" strokeWidth="5" fill="none" />
            <polygon points="175,631 185,635 175,639" fill="#0284C7" />
            <polygon points="310,631 320,635 310,639" fill="#0284C7" />
            {isPlaying && (
              <path d="M 155 635 L 320 635" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="5 7" fill="none">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 16. TREATED WATER TANK OUT THROUGH M12, TO FLUSH & INTO SOFTENER */}
          <g id="treated-to-softener-line">
            <path d="M 460 635 L 495 635 M 525 635 L 655 635" stroke="#0284C7" strokeWidth="5" fill="none" />
            <path d="M 560 635 L 560 585" stroke="#0284C7" strokeWidth="4" fill="none" />
            <polygon points="556,585 560,575 564,585" fill="#0284C7" />
            <polygon points="645,631 655,635 645,639" fill="#0284C7" />
          </g>

          {/* 17. SOFTENER OUT INTO SOFT WATER TANK */}
          <g id="softener-to-soft-water-line">
            <path d="M 735 635 L 860 635" stroke="#0284C7" strokeWidth="5" fill="none" />
            <polygon points="850,631 860,635 850,639" fill="#0284C7" />
          </g>

          {/* ====================================================================== */}
          {/* TANKS & VESSELS                                                        */}
          {/* ====================================================================== */}

          {/* TANK 1: COLLECTION TANK */}
          <g id="tank-collection" transform="translate(160, 60)" filter="url(#softShadow)">
            <rect x="0" y="0" width="140" height="85" rx="8" fill="#FFFFFF" stroke="#94A3B8" strokeWidth="1.5" />
            <rect x="3" y={85 - (85 * collectionLevel) / 100} width="134" height={(85 * collectionLevel) / 100 - 3} rx="6" fill="url(#lightTankWater)" />
            <rect x="0" y="0" width="140" height="20" rx="8" fill="#F0F9FF" />
            <text x="70" y="14" textAnchor="middle" fill="#0369A1" fontSize="9" fontWeight="bold" fontFamily="monospace">
              COLLECTION TANK
            </text>
            <text x="70" y="52" textAnchor="middle" fill="#0F172A" fontSize="18" fontWeight="900" fontFamily="monospace">
              {collectionLevel}%
            </text>
          </g>

          {/* DOTTED BOUNDING BOX FOR SBR RCP / RSTP PUMPS */}
          <rect x="165" y="160" width="135" height="65" rx="4" fill="none" stroke="#93C5FD" strokeWidth="1" strokeDasharray="3 3" />

          {/* 4 PUMPS BELOW COLLECTION TANK: M01, M02, M07, M08 */}
          <g id="pump-M01" transform="translate(180, 192)" className="cursor-pointer" onClick={() => handleTogglePump("M01")}>
            <circle cx="0" cy="0" r="11" fill={getPumpFill(pumps.M01.status)} stroke={getPumpColor(pumps.M01.status)} strokeWidth="2" />
            <text x="0" y="3.5" textAnchor="middle" fill="#0F172A" fontSize="7.5" fontWeight="bold">M01</text>
            <polygon points="-3,-13 0,-18 3,-13" fill="#0284C7" />
            <text x="0" y="20" textAnchor="middle" fill="#475569" fontSize="6.5" fontFamily="monospace">SBR RCP 1</text>
          </g>

          <g id="pump-M02" transform="translate(215, 192)" className="cursor-pointer" onClick={() => handleTogglePump("M02")}>
            <circle cx="0" cy="0" r="11" fill={getPumpFill(pumps.M02.status)} stroke={getPumpColor(pumps.M02.status)} strokeWidth="2" />
            <text x="0" y="3.5" textAnchor="middle" fill="#0F172A" fontSize="7.5" fontWeight="bold">M02</text>
            <polygon points="-3,-13 0,-18 3,-13" fill="#0284C7" />
            <text x="0" y="20" textAnchor="middle" fill="#475569" fontSize="6.5" fontFamily="monospace">SBR RCP 2</text>
          </g>

          <g id="pump-M07" transform="translate(250, 192)" className="cursor-pointer" onClick={() => handleTogglePump("M07")}>
            <circle cx="0" cy="0" r="11" fill={getPumpFill(pumps.M07.status)} stroke={getPumpColor(pumps.M07.status)} strokeWidth="2" />
            <text x="0" y="3.5" textAnchor="middle" fill="#0F172A" fontSize="7.5" fontWeight="bold">M07</text>
            <polygon points="-3,13 0,18 3,13" fill="#16A34A" />
            <text x="0" y="-14" textAnchor="middle" fill="#15803D" fontSize="6.5" fontFamily="monospace" fontWeight="bold">SBR RSTP 1</text>
          </g>

          <g id="pump-M08" transform="translate(285, 192)" className="cursor-pointer" onClick={() => handleTogglePump("M08")}>
            <circle cx="0" cy="0" r="11" fill={getPumpFill(pumps.M08.status)} stroke={getPumpColor(pumps.M08.status)} strokeWidth="2" />
            <text x="0" y="3.5" textAnchor="middle" fill="#0F172A" fontSize="7.5" fontWeight="bold">M08</text>
            <polygon points="-3,13 0,18 3,13" fill="#D97706" />
            <text x="0" y="-14" textAnchor="middle" fill="#475569" fontSize="6.5" fontFamily="monospace">SBR RSTP 2</text>
          </g>

          {/* TANK 2: SBR TANK */}
          <g id="tank-sbr" transform="translate(155, 230)" filter="url(#softShadow)">
            <rect x="0" y="0" width="155" height="90" rx="8" fill="#FFFFFF" stroke="#94A3B8" strokeWidth="1.5" />
            <rect x="0" y="0" width="155" height="20" rx="8" fill="#F0F9FF" />
            <text x="77" y="14" textAnchor="middle" fill="#0369A1" fontSize="9" fontWeight="bold" fontFamily="monospace">
              SBR TANK
            </text>
            <text x="77" y="46" textAnchor="middle" fill="#334155" fontSize="18" fontWeight="900" fontFamily="monospace">
              {sbrLevel}%
            </text>

            <g transform="translate(8, 60)">
              <rect x="0" y="0" width="65" height="15" rx="3" fill="#F0F9FF" stroke="#0284C7" strokeWidth="1" />
              <text x="32" y="11" textAnchor="middle" fill="#0369A1" fontSize="7" fontWeight="bold">
                {do2.toFixed(2)} mg/l DO2
              </text>
            </g>

            <g transform="translate(78, 60)">
              <rect x="0" y="0" width="70" height="15" rx="3" fill="#FAF5FF" stroke="#A855F7" strokeWidth="1" />
              <text x="35" y="11" textAnchor="middle" fill="#7E22CE" fontSize="6.5" fontWeight="bold">
                {sbrTss.toFixed(2)} mg/l TSS
              </text>
            </g>
          </g>

          {/* DOTTED BOUNDING BOX FOR MBBR RSTP PUMPS */}
          <rect x="345" y="55" width="75" height="75" rx="4" fill="none" stroke="#93C5FD" strokeWidth="1" strokeDasharray="3 3" />

          {/* PUMPS M1 & M2 (COLLECTION -> MBBR) */}
          <g id="pump-M1" transform="translate(380, 75)" className="cursor-pointer" onClick={() => handleTogglePump("M1")}>
            <circle cx="0" cy="0" r="11" fill={getPumpFill(pumps.M1.status)} stroke={getPumpColor(pumps.M1.status)} strokeWidth="2" />
            <text x="0" y="3.5" textAnchor="middle" fill="#0F172A" fontSize="8" fontWeight="bold">M1</text>
            <polygon points="14,-2.5 19,0 14,2.5" fill="#16A34A" />
            <text x="0" y="-14" textAnchor="middle" fill="#15803D" fontSize="6.5" fontFamily="monospace" fontWeight="bold">MBBR RSTP 1</text>
          </g>

          <g id="pump-M2" transform="translate(380, 115)" className="cursor-pointer" onClick={() => handleTogglePump("M2")}>
            <circle cx="0" cy="0" r="11" fill={getPumpFill(pumps.M2.status)} stroke={getPumpColor(pumps.M2.status)} strokeWidth="2" />
            <text x="0" y="3.5" textAnchor="middle" fill="#0F172A" fontSize="8" fontWeight="bold">M2</text>
            <polygon points="14,-2.5 19,0 14,2.5" fill="#DC2626" />
            <text x="0" y="18" textAnchor="middle" fill="#991B1B" fontSize="6.5" fontFamily="monospace">MBBR RSTP 2</text>
          </g>

          {/* TANK 3: MBBR AERATION TANK */}
          <g id="tank-mbbr" transform="translate(440, 60)" filter="url(#softShadow)">
            <rect x="0" y="0" width="140" height="85" rx="8" fill="#FFFFFF" stroke="#0284C7" strokeWidth="2" />
            <rect x="3" y="22" width="134" height="60" rx="6" fill="url(#lightTankWater)" />
            {isPlaying && (
              <g>
                {[
                  { cx: 25, cy: 75, r: 2.5, dur: "1.1s", delay: "0s" },
                  { cx: 50, cy: 80, r: 3.5, dur: "0.9s", delay: "0.2s" },
                  { cx: 75, cy: 75, r: 2.0, dur: "1.3s", delay: "0.4s" },
                  { cx: 100, cy: 80, r: 3.0, dur: "1.0s", delay: "0.1s" },
                  { cx: 120, cy: 75, r: 2.5, dur: "0.8s", delay: "0.3s" },
                ].map((b, i) => (
                  <circle key={i} cx={b.cx} cy={b.cy} r={b.r} fill="#FFFFFF" opacity="0.85">
                    <animate attributeName="cy" values={`${b.cy};28`} dur={`${parseFloat(b.dur) / simSpeed}s`} begin={b.delay} repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0.3;0.9;0" dur={`${parseFloat(b.dur) / simSpeed}s`} begin={b.delay} repeatCount="indefinite" />
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

          {/* TANK 4: CLARIFIER TANK WITH ARM */}
          <g id="tank-clarifier" transform="translate(720, 60)" filter="url(#softShadow)">
            <rect x="0" y="0" width="140" height="85" rx="8" fill="#FFFFFF" stroke="#0284C7" strokeWidth="2" />
            <rect x="3" y="22" width="134" height="60" rx="6" fill="url(#lightTankWater)" />
            <rect x="0" y="0" width="140" height="20" rx="8" fill="#F0F9FF" />
            <text x="70" y="14" textAnchor="middle" fill="#0369A1" fontSize="8.5" fontWeight="bold" fontFamily="monospace">
              CLARIFIER TANK WITH ARM
            </text>

            <g transform="translate(70, 52)" className="cursor-pointer" onClick={() => handleTogglePump("ARM")}>
              <circle cx="0" cy="0" r="15" fill="#DCFCE7" stroke="#16A34A" strokeWidth="2" />
              <g>
                {isPlaying && pumps.ARM.status === "RUNNING" && (
                  <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur={`${2.5 / simSpeed}s`} repeatCount="indefinite" />
                )}
                <line x1="-10" y1="0" x2="10" y2="0" stroke="#15803D" strokeWidth="2.5" strokeLinecap="round" />
                <line x1="0" y1="-10" x2="0" y2="10" stroke="#15803D" strokeWidth="2.5" strokeLinecap="round" />
              </g>
              <text x="24" y="4" fill="#15803D" fontSize="8" fontWeight="bold">ARM</text>
            </g>
          </g>

          {/* CLARIFIER EFFLUENT DROP INSTRUMENTS (TSS BADGE & CLARIFIER VALVE) */}
          <g transform="translate(805, 150)">
            <rect x="0" y="0" width="95" height="15" rx="3" fill="#FAF5FF" stroke="#A855F7" strokeWidth="1" />
            <text x="47" y="11" textAnchor="middle" fill="#7E22CE" fontSize="7" fontWeight="bold">
              {clarifierTss.toFixed(2)} mg/l TSS
            </text>
          </g>

          <g id="valve-clarifier" transform="translate(785, 185)" className="cursor-pointer" onClick={() => setClarifierValveOpen(!clarifierValveOpen)}>
            <circle cx="0" cy="0" r="11" fill="#DCFCE7" stroke="#16A34A" strokeWidth="2" />
            <text x="0" y="3.5" textAnchor="middle" fill="#15803D" fontSize="8" fontWeight="bold">V</text>
            <text x="0" y="20" textAnchor="middle" fill="#15803D" fontSize="6.5" fontFamily="monospace">CLARIFIER VALVE</text>
          </g>

          {/* SLUDGE PUMPS M3 & M4 (POINTING LEFT, DISCHARGING INTO SLUDGE TANK) */}
          <g id="pump-M3" transform="translate(640, 140)" className="cursor-pointer" onClick={() => handleTogglePump("M3")}>
            <circle cx="0" cy="0" r="11" fill={getPumpFill(pumps.M3.status)} stroke={getPumpColor(pumps.M3.status)} strokeWidth="2" />
            <text x="0" y="3.5" textAnchor="middle" fill="#0F172A" fontSize="7.5" fontWeight="bold">M3</text>
            <polygon points="-14,-2 -19,0 -14,2" fill="#DC2626" />
            <text x="0" y="-14" textAnchor="middle" fill="#991B1B" fontSize="6" fontFamily="monospace">MBBR RCP 1</text>
          </g>

          <g id="pump-M4" transform="translate(640, 175)" className="cursor-pointer" onClick={() => handleTogglePump("M4")}>
            <circle cx="0" cy="0" r="11" fill={getPumpFill(pumps.M4.status)} stroke={getPumpColor(pumps.M4.status)} strokeWidth="2" />
            <text x="0" y="3.5" textAnchor="middle" fill="#0F172A" fontSize="7.5" fontWeight="bold">M4</text>
            <polygon points="-14,-2 -19,0 -14,2" fill="#16A34A" />
            <text x="0" y="18" textAnchor="middle" fill="#15803D" fontSize="6" fontFamily="monospace" fontWeight="bold">MBBR RCP 2</text>
          </g>

          {/* TANK 5: SLUDGE HOLDING TANK (DIRECTLY BELOW M3 & M4) */}
          <g id="tank-sludge" transform="translate(545, 195)" filter="url(#softShadow)">
            <rect x="0" y="0" width="105" height="60" rx="8" fill="#FFFFFF" stroke="#94A3B8" strokeWidth="1.5" />
            <rect x="0" y="0" width="105" height="18" rx="8" fill="#F0F9FF" />
            <text x="52" y="13" textAnchor="middle" fill="#0369A1" fontSize="7.5" fontWeight="bold" fontFamily="monospace">
              SLUDGE HOLDING TANK
            </text>
            <text x="52" y="44" textAnchor="middle" fill="#334155" fontSize="16" fontWeight="900" fontFamily="monospace">
              {sludgeLevel}%
            </text>
          </g>

          {/* TANK 6: FILTER FEED TANK (DIRECTLY BELOW CLARIFIER VALVE) */}
          <g id="tank-filter-feed" transform="translate(720, 230)" filter="url(#softShadow)">
            <rect x="0" y="0" width="140" height="85" rx="8" fill="#FFFFFF" stroke="#0284C7" strokeWidth="2" />
            <rect x="3" y={85 - (85 * filterFeedLevel) / 100} width="134" height={(85 * filterFeedLevel) / 100 - 3} rx="6" fill="url(#lightTankWater)" />
            <rect x="0" y="0" width="140" height="20" rx="8" fill="#F0F9FF" />
            <text x="70" y="14" textAnchor="middle" fill="#0369A1" fontSize="8.5" fontWeight="bold" fontFamily="monospace">
              FILTER FEED TANK
            </text>
            <text x="70" y="52" textAnchor="middle" fill="#0F172A" fontSize="18" fontWeight="900" fontFamily="monospace">
              {filterFeedLevel}%
            </text>
          </g>

          {/* FILTER FEED PUMPS: M10 & M11 */}
          <g id="pump-M10" transform="translate(760, 355)" className="cursor-pointer" onClick={() => handleTogglePump("M10")}>
            <circle cx="0" cy="0" r="11" fill={getPumpFill(pumps.M10.status)} stroke={getPumpColor(pumps.M10.status)} strokeWidth="2" />
            <text x="0" y="3.5" textAnchor="middle" fill="#0F172A" fontSize="7.5" fontWeight="bold">M10</text>
            <polygon points="-3,13 0,18 3,13" fill="#DC2626" />
            <text x="0" y="-14" textAnchor="middle" fill="#991B1B" fontSize="6.5" fontFamily="monospace">FF PUMP 1</text>
          </g>

          <g id="pump-M11" transform="translate(810, 355)" className="cursor-pointer" onClick={() => handleTogglePump("M11")}>
            <circle cx="0" cy="0" r="11" fill={getPumpFill(pumps.M11.status)} stroke={getPumpColor(pumps.M11.status)} strokeWidth="2" />
            <text x="0" y="3.5" textAnchor="middle" fill="#0F172A" fontSize="7.5" fontWeight="bold">M11</text>
            <polygon points="-3,13 0,18 3,13" fill="#DC2626" />
            <text x="0" y="-14" textAnchor="middle" fill="#991B1B" fontSize="6.5" fontFamily="monospace">FF PUMP 2</text>
          </g>

          {/* BLOWERS & AIR SOLENOID */}
          <g id="blower-1" transform="translate(540, 275)" className="cursor-pointer" onClick={() => handleTogglePump("BL1")}>
            <circle cx="0" cy="0" r="13" fill="#FCE7F3" stroke="#F43F5E" strokeWidth="2" />
            <path d="M -5 0 L 5 0 M 0 -5 L 0 5" stroke="#BE123C" strokeWidth="2" strokeLinecap="round" />
            <circle cx="10" cy="10" r="2.5" fill="#16A34A" />
            <text x="0" y="22" textAnchor="middle" fill="#475569" fontSize="7" fontFamily="monospace">BLOWER 1</text>
          </g>

          <g id="blower-2" transform="translate(540, 325)" className="cursor-pointer" onClick={() => handleTogglePump("BL2")}>
            <circle cx="0" cy="0" r="13" fill="#DCFCE7" stroke="#16A34A" strokeWidth="2" />
            <g>
              {isPlaying && pumps.BL2.status === "RUNNING" && (
                <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur={`${0.4 / simSpeed}s`} repeatCount="indefinite" />
              )}
              <path d="M -5 0 L 5 0 M 0 -5 L 0 5" stroke="#15803D" strokeWidth="2" strokeLinecap="round" />
            </g>
            <circle cx="10" cy="10" r="2.5" fill="#16A34A" />
            <text x="0" y="22" textAnchor="middle" fill="#15803D" fontSize="7" fontFamily="monospace" fontWeight="bold">BLOWER 2</text>
          </g>

          <g id="valve-air-solenoid" transform="translate(410, 325)" className="cursor-pointer" onClick={() => setAirSolenoidOpen(!airSolenoidOpen)}>
            <circle cx="0" cy="0" r="12" fill="#FEF3C7" stroke="#D97706" strokeWidth="2" />
            <text x="0" y="3.5" textAnchor="middle" fill="#92400E" fontSize="8" fontWeight="bold">V</text>
            <text x="0" y="20" textAnchor="middle" fill="#92400E" fontSize="6.5" fontFamily="monospace">AIR SOLENOID</text>
          </g>

          {/* SBR DCTF PUMP M9 */}
          <g id="pump-M9" transform="translate(540, 370)" className="cursor-pointer" onClick={() => handleTogglePump("M9")}>
            <circle cx="0" cy="0" r="12" fill={getPumpFill(pumps.M9.status)} stroke={getPumpColor(pumps.M9.status)} strokeWidth="2" />
            <text x="0" y="3.5" textAnchor="middle" fill="#0F172A" fontSize="7.5" fontWeight="bold">M9</text>
            <polygon points="15,-2.5 20,0 15,2.5" fill="#D97706" />
            <text x="0" y="20" textAnchor="middle" fill="#475569" fontSize="6.5" fontFamily="monospace">SBR DCTF</text>
          </g>

          {/* ====================================================================== */}
          {/* BOTTOM SECTION: PSF, ACF, UV, DOSING, TREATED & SOFT WATER             */}
          {/* ====================================================================== */}

          {/* GREY DASHED BORDER AROUND ACF AREA AS IN PHOTO */}
          <rect x="110" y="415" width="235" height="195" rx="6" fill="none" stroke="#CBD5E1" strokeWidth="1.5" strokeDasharray="4 4" />

          {/* INLET PRESSURE (0.35 Bar) */}
          <g transform="translate(640, 440)">
            <rect x="0" y="0" width="85" height="18" rx="4" fill="#F0F9FF" stroke="#0284C7" strokeWidth="1" />
            <text x="42" y="12" textAnchor="middle" fill="#0369A1" fontSize="8" fontWeight="bold">{inletPressure.toFixed(2)} Bar</text>
            <text x="42" y="28" textAnchor="middle" fill="#475569" fontSize="6" fontFamily="monospace">INLET PRESSURE</text>
          </g>

          {/* OUTLET PRESSURE (0.15 Bar) */}
          <g transform="translate(640, 485)">
            <rect x="0" y="0" width="85" height="18" rx="4" fill="#F0F9FF" stroke="#0284C7" strokeWidth="1" />
            <text x="42" y="12" textAnchor="middle" fill="#0369A1" fontSize="8" fontWeight="bold">{outletPressure.toFixed(2)} Bar</text>
            <text x="42" y="28" textAnchor="middle" fill="#475569" fontSize="6" fontFamily="monospace">OUTLET PRESSURE</text>
          </g>

          {/* PSF VALVE MULTIPORT BLOCK */}
          <g id="psf-valve-block" transform="translate(765, 460)">
            <rect x="0" y="0" width="55" height="42" rx="4" fill="#DCFCE7" stroke="#16A34A" strokeWidth="1.5" />
            <text x="27" y="12" textAnchor="middle" fill="#15803D" fontSize="7" fontWeight="bold">PSF VALVE</text>
            <text x="12" y="23" fill="#166534" fontSize="5.5" fontFamily="monospace">INLET</text>
            <text x="36" y="23" fill="#166534" fontSize="5.5" fontFamily="monospace">VIN</text>
            <text x="12" y="36" fill="#166534" fontSize="5.5" fontFamily="monospace">OUT</text>
            <text x="36" y="36" fill="#166534" fontSize="5.5" fontFamily="monospace">VOUT</text>
            {/* Drain label */}
            <text x="27" y="47" textAnchor="middle" fill="#DC2626" fontSize="5.5" fontFamily="monospace">DRAIN</text>
          </g>

          {/* PSF VESSEL */}
          <g id="vessel-psf" transform="translate(900, 440)" filter="url(#softShadow)">
            <path d="M 0 15 Q 40 -8 80 15 L 80 115 Q 40 135 0 115 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="2" />
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
          <g id="acf-valve-block" transform="translate(295, 455)">
            <rect x="0" y="0" width="55" height="42" rx="4" fill="#DCFCE7" stroke="#16A34A" strokeWidth="1.5" />
            <text x="27" y="12" textAnchor="middle" fill="#15803D" fontSize="7" fontWeight="bold">ACF VALVE</text>
            <text x="12" y="23" fill="#166534" fontSize="5.5" fontFamily="monospace">VIN</text>
            <text x="36" y="23" fill="#166534" fontSize="5.5" fontFamily="monospace">OUT</text>
            <text x="12" y="36" fill="#166534" fontSize="5.5" fontFamily="monospace">VOUT</text>
            <text x="36" y="36" fill="#166534" fontSize="5.5" fontFamily="monospace">INLET</text>
            <text x="58" y="27" fill="#DC2626" fontSize="5.5" fontFamily="monospace">DRAIN</text>
          </g>

          {/* ACF VESSEL */}
          <g id="vessel-acf" transform="translate(160, 440)" filter="url(#softShadow)">
            <path d="M 0 15 Q 40 -8 80 15 L 80 115 Q 40 135 0 115 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="2" />
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
          <g id="dosing-pump" transform="translate(215, 615)">
            <polygon points="16,0 32,9 32,27 16,36 0,27 0,9" fill="#DCFCE7" stroke="#16A34A" strokeWidth="2" />
            <text x="16" y="16" textAnchor="middle" fill="#166534" fontSize="5.5" fontWeight="bold">DOSING</text>
            <text x="16" y="24" textAnchor="middle" fill="#15803D" fontSize="5.5" fontWeight="bold">PUMP</text>
            <line x1="16" y1="36" x2="16" y2="48" stroke="#16A34A" strokeWidth="2" />
            <polygon points="13,48 16,53 19,48" fill="#16A34A" />
          </g>

          {/* UV LIGHT */}
          <g id="uv-light" transform="translate(85, 620)">
            <rect x="0" y="0" width="70" height="36" rx="4" fill="#FAF5FF" stroke="#9333EA" strokeWidth="1.5" />
            <line x1="10" y1="9" x2="60" y2="9" stroke="#A855F7" strokeWidth="3" strokeLinecap="round" />
            <line x1="10" y1="18" x2="60" y2="18" stroke="#16A34A" strokeWidth="3" strokeLinecap="round" />
            <line x1="10" y1="27" x2="60" y2="27" stroke="#A855F7" strokeWidth="3" strokeLinecap="round" />
            <text x="35" y="48" textAnchor="middle" fill="#7E22CE" fontSize="7.5" fontWeight="bold" fontFamily="monospace">UV LIGHT</text>
          </g>

          {/* TREATED WATER TANK */}
          <g id="tank-treated" transform="translate(320, 595)" filter="url(#softShadow)">
            <rect x="0" y="0" width="140" height="80" rx="8" fill="#FFFFFF" stroke="#0284C7" strokeWidth="2" />
            <rect x="3" y="20" width="134" height="57" rx="6" fill="url(#treatedWaterGrad)" />
            <rect x="0" y="0" width="140" height="18" rx="8" fill="#F0F9FF" />
            <text x="70" y="13" textAnchor="middle" fill="#0369A1" fontSize="8" fontWeight="bold" fontFamily="monospace">
              TREATED WATER TANK
            </text>
            <text x="70" y="52" textAnchor="middle" fill="#0F172A" fontSize="18" fontWeight="900" fontFamily="monospace">
              {treatedLevel}%
            </text>
          </g>

          {/* M12: FLUSHING PUMP */}
          <g id="pump-M12" transform="translate(510, 635)" className="cursor-pointer" onClick={() => handleTogglePump("M12")}>
            <circle cx="0" cy="0" r="13" fill={getPumpFill(pumps.M12.status)} stroke={getPumpColor(pumps.M12.status)} strokeWidth="2" />
            <text x="0" y="3.5" textAnchor="middle" fill="#0F172A" fontSize="8" fontWeight="bold">M12</text>
            <text x="0" y="22" textAnchor="middle" fill="#475569" fontSize="6.5" fontFamily="monospace">FLUSHING PUMP</text>
          </g>

          <text x="560" y="570" textAnchor="middle" fill="#0284C7" fontSize="8" fontWeight="bold" fontFamily="monospace">TO FLUSH</text>

          {/* WATER SOLENOID VALVE */}
          <g id="valve-water-solenoid" transform="translate(600, 635)" className="cursor-pointer" onClick={() => setWaterSolenoidOpen(!waterSolenoidOpen)}>
            <circle cx="0" cy="0" r="13" fill={waterSolenoidOpen ? "#DCFCE7" : "#FEE2E2"} stroke={waterSolenoidOpen ? "#16A34A" : "#DC2626"} strokeWidth="2" />
            <text x="0" y="3.5" textAnchor="middle" fill="#0F172A" fontSize="8.5" fontWeight="bold">V</text>
            <text x="0" y="22" textAnchor="middle" fill="#991B1B" fontSize="6.5" fontFamily="monospace">WATER SOLENOID</text>
          </g>

          {/* SOFTENER VESSEL */}
          <g id="vessel-softener" transform="translate(655, 585)" filter="url(#softShadow)">
            <path d="M 0 15 Q 40 -8 80 15 L 80 95 Q 40 115 0 95 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="2" />
            <text x="40" y="58" textAnchor="middle" fill="#FFFFFF" fontSize="11" fontWeight="900" fontFamily="monospace">SOFTENER</text>

            <g transform="translate(85, -20)">
              <rect x="0" y="0" width="85" height="15" rx="3" fill="#FAF5FF" stroke="#A855F7" strokeWidth="1" />
              <text x="42" y="11" textAnchor="middle" fill="#7E22CE" fontSize="7" fontWeight="bold">
                {softwaterHardness.toFixed(2)} mg/l
              </text>
              <text x="42" y="24" textAnchor="middle" fill="#475569" fontSize="5.5" fontFamily="monospace">SOFTWATER TOTAL HARDNESS</text>
            </g>
          </g>

          {/* SOFT WATER TANK */}
          <g id="tank-soft-water" transform="translate(860, 595)" filter="url(#softShadow)">
            <rect x="0" y="0" width="140" height="80" rx="8" fill="#FFFFFF" stroke="#0284C7" strokeWidth="2" />
            <rect x="3" y="20" width="134" height="57" rx="6" fill="url(#treatedWaterGrad)" />
            <rect x="0" y="0" width="140" height="18" rx="8" fill="#F0F9FF" />
            <text x="70" y="13" textAnchor="middle" fill="#0369A1" fontSize="8" fontWeight="bold" fontFamily="monospace">
              SOFT WATER TANK
            </text>
            <text x="70" y="52" textAnchor="middle" fill="#0F172A" fontSize="18" fontWeight="900" fontFamily="monospace">
              {softWaterLevel}%
            </text>
          </g>
        </svg>
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
