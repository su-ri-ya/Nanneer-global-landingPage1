"use client"

import React, { useState, useEffect } from "react"
import Image from "next/image"
import {
  Play,
  Pause,
  RotateCcw,
  Sliders,
  Activity,
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

export type MultiportValveMode = "SERVICE" | "BACKWASH" | "RINSE" | "DRAIN"

export function ScadaSchematicSimulation() {
  const [isPlaying, setIsPlaying] = useState<boolean>(true)
  const [simSpeed, setSimSpeed] = useState<number>(1)
  const [controlMode, setControlMode] = useState<"AUTO" | "MANUAL">("AUTO")
  const [selectedAsset, setSelectedAsset] = useState<string | null>(null)
  const [showTelemetryBadges, setShowTelemetryBadges] = useState<boolean>(true)
  const filterVesselOption: 1 | 2 | 3 | 4 = 3

  // Live sensor readings with micro-jitter
  const [do1, setDo1] = useState<number>(0.88)
  const [clarifierTss, setClarifierTss] = useState<number>(0.0)
  const [inletPressure, setInletPressure] = useState<number>(0.35)
  const [outletPressure, setOutletPressure] = useState<number>(0.15)
  const [softwaterHardness, setSoftwaterHardness] = useState<number>(0.0)

  // Tank levels (Uniform 50% Water Level matching Filter Feed Tank)
  const [collectionLevel, setCollectionLevel] = useState<number>(50)
  const [mbbrLevel, setMbbrLevel] = useState<number>(50)
  const [clarifierLevel, setClarifierLevel] = useState<number>(50)
  const [filterFeedLevel, setFilterFeedLevel] = useState<number>(50)
  const [sludgeLevel, setSludgeLevel] = useState<number>(50)
  const [treatedLevel, setTreatedLevel] = useState<number>(50)
  const [softWaterLevel, setSoftWaterLevel] = useState<number>(50)

  // Filter service timers in seconds
  const [psfSeconds, setPsfSeconds] = useState<number>(3 * 3600 + 20 * 60 + 24)
  const [acfSeconds, setAcfSeconds] = useState<number>(3 * 3600 + 20 * 60 + 25)

  // Valves state
  const [clarifierValveOpen, setClarifierValveOpen] = useState<boolean>(true)
  const [waterSolenoidOpen, setWaterSolenoidOpen] = useState<boolean>(false)
  const [psfValveMode, setPsfValveMode] = useState<MultiportValveMode>("SERVICE")
  const [acfValveMode, setAcfValveMode] = useState<MultiportValveMode>("SERVICE")

  // Equipment Pumps State (MBBR & Tertiary Polishing Train)
  const [pumps, setPumps] = useState<Record<string, PumpState>>({
    M1: { id: "M1", name: "MBBR PUMP 1", code: "M1", status: "RUNNING", powerKw: 4.0, flowRate: 18.5 },
    M2: { id: "M2", name: "MBBR PUMP 2", code: "M2", status: "STANDBY", powerKw: 4.0, flowRate: 0 },
    M3: { id: "M3", name: "MBBR PUMP 3", code: "M3", status: "STANDBY", powerKw: 1.5, flowRate: 0 },
    M4: { id: "M4", name: "MBBR PUMP 4", code: "M4", status: "RUNNING", powerKw: 1.5, flowRate: 6.8 },
    M10: { id: "M10", name: "FF PUMP 1", code: "M10", status: "RUNNING", powerKw: 3.0, flowRate: 15.0 },
    M11: { id: "M11", name: "FF PUMP 2", code: "M11", status: "STANDBY", powerKw: 3.0, flowRate: 0 },
    M12: { id: "M12", name: "FLUSHING PUMP", code: "M12", status: "RUNNING", powerKw: 5.5, flowRate: 15.0 },
    BL1: { id: "BL1", name: "BLOWER 1", code: "B1", status: "STANDBY", powerKw: 7.5, flowRate: 0 },
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
          ? "STANDBY"
          : current.status === "STANDBY"
          ? "STOPPED"
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
    return status === "RUNNING" ? "#16A34A" : "#DC2626"
  }

  const getPumpFill = (status: PumpStatus) => {
    return status === "RUNNING" ? "#DCFCE7" : "#FEE2E2"
  }

  // Concept 4: Optical Sight-Glass Pump Renderer with 2.5D Volute Casing, Vortex Impeller & Specular Glare
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

    // Strictly Green (Running) & Red (Standby / Stopped)
    const glassBg = isRunning ? "#064E3B" : "#450A0A"
    const glassBorder = isRunning ? "#22C55E" : "#EF4444"
    const vaneStroke = isRunning ? "#86EFAC" : "#FCA5A5"
    const vaneSubStroke = isRunning ? "#4ADE80" : "#F87171"

    // Flow arrow points relative to center
    let arrow = null
    if (arrowDir === "up") arrow = <polygon points="-3,-14 0,-20 3,-14" fill={color} />
    if (arrowDir === "down") arrow = <polygon points="-3,14 0,20 3,14" fill={color} />
    if (arrowDir === "left") arrow = <polygon points="-14,-3 -20,0 -14,3" fill={color} />
    if (arrowDir === "right") arrow = <polygon points="14,-3 20,0 14,3" fill={color} />

    // Dynamically calculate tag clearance so text NEVER collides with pump casing (r=14) or arrow (length=20)
    let tagY = 0
    if (tagPos === "bottom") {
      tagY = arrowDir === "down" ? 25 : 20
    } else {
      if (arrowDir === "up") {
        tagY = tagLine2 ? -28 : -22
      } else {
        tagY = tagLine2 ? -24 : -18
      }
    }

    return (
      <g
        id={`pump-${id}`}
        transform={`translate(${cx}, ${cy})`}
        className="cursor-pointer"
        onClick={() => handleTogglePump(id)}
      >
        {/* 1. Outer CNC Flange Volute Ring */}
        <circle cx="0" cy="0" r="14" fill="url(#metalRingGrad)" stroke="#64748B" strokeWidth="1" />

        {/* Peripheral Flange Bolt Studs */}
        {[0, 60, 120, 180, 240, 300].map((deg) => (
          <circle
            key={deg}
            cx={12.5 * Math.cos((deg * Math.PI) / 180)}
            cy={12.5 * Math.sin((deg * Math.PI) / 180)}
            r="0.75"
            fill="#1E293B"
            stroke="#94A3B8"
            strokeWidth="0.3"
          />
        ))}

        {/* 2. Optical Polycarbonate Sight-Glass Chamber */}
        <circle cx="0" cy="0" r="11" fill={glassBg} stroke={glassBorder} strokeWidth="1.4" />

        {/* 3. Centrifugal Fluid Vortex Impeller Dynamics */}
        <g>
          {isPlaying && isRunning && (
            <animateTransform
              attributeName="transform"
              type="rotate"
              from="0"
              to="360"
              dur={`${0.45 / simSpeed}s`}
              repeatCount="indefinite"
            />
          )}

          {/* Hydrodynamic Swirl Vanes */}
          <path d="M 0 0 C 3 3, 6 1, 9 7" stroke={vaneStroke} strokeWidth="1" fill="none" opacity="0.9" />
          <path d="M 0 0 C -3 -3, -6 -1, -9 -7" stroke={vaneStroke} strokeWidth="1" fill="none" opacity="0.9" />
          <path d="M 0 0 C 3 -3, 1 -6, 7 -9" stroke={vaneSubStroke} strokeWidth="0.9" fill="none" opacity="0.8" />
          <path d="M 0 0 C -3 3, -1 6, -7 9" stroke={vaneSubStroke} strokeWidth="0.9" fill="none" opacity="0.8" />

          {/* Swirling Cavitation Micro-Bubbles (when running) */}
          {isRunning && (
            <>
              <circle cx="4" cy="3" r="0.6" fill="#FFFFFF" opacity="0.9" />
              <circle cx="-5" cy="4" r="0.5" fill="#FFFFFF" opacity="0.8" />
              <circle cx="6" cy="-5" r="0.7" fill="#FFFFFF" opacity="0.9" />
              <circle cx="-4" cy="-6" r="0.5" fill="#FFFFFF" opacity="0.8" />
            </>
          )}

          {/* Center Drive Shaft Impeller Hub */}
          <circle cx="0" cy="0" r="2.4" fill={isRunning ? "#16A34A" : "#DC2626"} stroke="#FFFFFF" strokeWidth="0.6" />
        </g>

        {/* 4. Optical Specular Reflection Glare Arch across Upper Dome */}
        <path d="M -8.5 -5 A 9.5 9.5 0 0 1 8.5 -5" stroke="#FFFFFF" strokeWidth="1.2" fill="none" opacity="0.65" strokeLinecap="round" />

        {/* 5. Flow Direction Arrow */}
        {arrow}

        {/* 6. Pump Identifier Tag */}
        {tagLine1 && (
          <g transform={`translate(0, ${tagPos === "bottom" ? (arrowDir === "down" ? 27 : 22) : (arrowDir === "up" ? -25 : -20)})`}>
            <rect
              x="-28"
              y="-7"
              width="56"
              height="14"
              rx="3"
              fill="#FFFFFF"
              stroke={color}
              strokeWidth="1"
              opacity="0.95"
              filter="drop-shadow(0px 1px 1.5px rgba(0,0,0,0.12))"
            />
            <text
              x="0"
              y="3"
              textAnchor="middle"
              fill={color}
              fontSize="7.2"
              fontWeight="bold"
              fontFamily="monospace"
            >
              {tagLine1}
            </text>
          </g>
        )}
      </g>
    )
  }

  // Equipment Identification Name Tag (High-Visibility Professional SCADA Pill)
  const renderMiniTag = (x: number, y: number, label: string, maxW?: number) => {
    const rawWidth = label.length * 5.8 + 16
    const textWidth = maxW ? Math.min(rawWidth, maxW) : Math.max(rawWidth, 44)
    const fontSize = textWidth < 55 ? "7.0" : "7.6"
    return (
      <g transform={`translate(${x}, ${y})`} className="pointer-events-none select-none">
        {/* Drop shadow container */}
        <rect
          x={-textWidth / 2}
          y="-7"
          width={textWidth}
          height="14"
          rx="3.5"
          fill="#FFFFFF"
          stroke="#0284C7"
          strokeWidth="1.1"
          opacity="0.95"
          filter="drop-shadow(0px 1px 2px rgba(15, 23, 42, 0.16))"
        />
        {/* Precision Cyan Status Pip */}
        <circle cx={-textWidth / 2 + 6.5} cy="0" r="1.8" fill="#0284C7" />
        <circle cx={-textWidth / 2 + 6.5} cy="0" r="0.7" fill="#E0F2FE" />
        {/* Bold Equipment Title */}
        <text
          x={3.0}
          y="2.5"
          textAnchor="middle"
          fill="#0369A1"
          fontSize={fontSize}
          fontWeight="bold"
          fontFamily="monospace"
        >
          {label}
        </text>
      </g>
    )
  }

  // 4 Design Options for PSF, ACF & Softener Filter Vessels
  const renderFilterVessel = (type: "PSF" | "ACF" | "SOFTENER", option: 1 | 2 | 3 | 4) => {
    return (
      <g id={`vessel-${type.toLowerCase()}-internals`}>

        {/* Option 1: Modern FRP (Clean Minimalist Composite Pressure Vessel) */}
        {option === 1 && (
          <g>
            {/* Upper Dished Head */}
            <path d="M 1 22 C 1 4, 81 4, 81 22 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="2" />
            {/* Cylindrical Shell */}
            <rect x="1" y="22" width="80" height="78" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="2" />
            {/* Lower Dished Head */}
            <path d="M 1 100 C 1 118, 81 118, 81 100 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="2" />

            {/* Top Multiport Automation Valve Head */}
            <g transform="translate(32, 2)">
              <rect x="0" y="0" width="18" height="12" rx="3" fill="#0F172A" stroke="#38BDF8" strokeWidth="1" />
              <circle cx="9" cy="6" r="3" fill={isPlaying ? "#16A34A" : "#D97706"}>
                {isPlaying && <animate attributeName="opacity" values="0.6;1;0.6" dur="1.2s" repeatCount="indefinite" />}
              </circle>
            </g>

            {/* Sleek Vertical Media Sight Slit */}
            <g transform="translate(37, 26)">
              <rect x="0" y="0" width="8" height="70" rx="3.5" fill="#0F172A" stroke="#7DD3FC" strokeWidth="1" />
              {type === "PSF" ? (
                <>
                  <rect x="1.5" y="2" width="5" height="34" rx="1.5" fill="url(#sandMediaGrad)" />
                  <rect x="1.5" y="38" width="5" height="18" fill="#B45309" />
                  <rect x="1.5" y="58" width="5" height="10" rx="1.5" fill="#451A03" />
                </>
              ) : type === "ACF" ? (
                <>
                  <rect x="1.5" y="2" width="5" height="48" rx="1.5" fill="url(#carbonMediaGrad)" />
                  <rect x="1.5" y="52" width="5" height="16" rx="1.5" fill="#1E293B" />
                </>
              ) : (
                <>
                  <rect x="1.5" y="2" width="5" height="48" rx="1.5" fill="url(#resinMediaGrad)" />
                  <rect x="1.5" y="52" width="5" height="16" rx="1.5" fill="#78350F" />
                </>
              )}
              {/* Slit Glare */}
              <rect x="1.5" y="2" width="2.5" height="66" rx="1" fill="#FFFFFF" opacity="0.45" />
            </g>

            {/* Flank Specular Sheen */}
            <rect x="5" y="10" width="10" height="96" rx="2" fill="url(#specularSheen)" opacity="0.55" />
            {/* Skirt Support Base Legs */}
            <path d="M 12 112 L 20 120 M 70 112 L 62 120" stroke="#0284C7" strokeWidth="2.5" strokeLinecap="round" />
          </g>
        )}

        {/* Option 2: Animated Flow (Semi-Transparent Downflow Filtration) */}
        {option === 2 && (
          <g>
            {/* Acrylic / Translucent Glass Hull */}
            <path d="M 1 22 C 1 4, 81 4, 81 22 Z" fill="#F0F9FF" fillOpacity="0.85" stroke="#0284C7" strokeWidth="2" />
            <rect x="1" y="22" width="80" height="78" fill="#F0F9FF" fillOpacity="0.85" stroke="#0284C7" strokeWidth="2" />
            <path d="M 1 100 C 1 118, 81 118, 81 100 Z" fill="#F0F9FF" fillOpacity="0.85" stroke="#0284C7" strokeWidth="2" />

            {/* Upper Freeboard Water Pool */}
            <path d="M 2 22 C 2 7, 80 7, 80 22 L 80 34 L 2 34 Z" fill="#BAE6FD" opacity="0.6" />

            {/* Media Bed */}
            {type === "PSF" ? (
              <>
                <rect x="3" y="34" width="76" height="38" fill="url(#sandMediaGrad)" opacity="0.92" />
                <rect x="3" y="72" width="76" height="18" fill="#B45309" opacity="0.95" />
                <rect x="3" y="90" width="76" height="14" fill="#451A03" opacity="0.95" />
              </>
            ) : type === "ACF" ? (
              <>
                <rect x="3" y="34" width="76" height="54" fill="url(#carbonMediaGrad)" opacity="0.95" />
                <rect x="3" y="88" width="76" height="16" fill="#1E293B" opacity="0.95" />
              </>
            ) : (
              <>
                <rect x="3" y="34" width="76" height="54" fill="url(#resinMediaGrad)" opacity="0.95" />
                <rect x="3" y="88" width="76" height="16" fill="#78350F" opacity="0.95" />
              </>
            )}

            {/* Animated Downflow Water Streams (Visible Filtration) */}
            {isPlaying && (
              <g stroke="#BAE6FD" strokeWidth="1.8" strokeDasharray="3 4" strokeLinecap="round" opacity="0.9">
                <line x1="20" y1="26" x2="20" y2="86">
                  <animate attributeName="stroke-dashoffset" from="0" to="14" dur={`${0.9 / simSpeed}s`} repeatCount="indefinite" />
                </line>
                <line x1="34" y1="24" x2="34" y2="88">
                  <animate attributeName="stroke-dashoffset" from="0" to="14" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                </line>
                <line x1="48" y1="24" x2="48" y2="88">
                  <animate attributeName="stroke-dashoffset" from="0" to="14" dur={`${0.85 / simSpeed}s`} repeatCount="indefinite" />
                </line>
                <line x1="62" y1="26" x2="62" y2="86">
                  <animate attributeName="stroke-dashoffset" from="0" to="14" dur={`${0.95 / simSpeed}s`} repeatCount="indefinite" />
                </line>
              </g>
            )}

            {/* Bottom Lateral Collector Arm */}
            <line x1="16" y1="98" x2="66" y2="98" stroke="#CBD5E1" strokeWidth="2.5" strokeLinecap="round" />
            {[22, 30, 38, 46, 54, 60].map((x) => (
              <line key={x} x1={x} y1="95" x2={x} y2="101" stroke="#94A3B8" strokeWidth="1" />
            ))}

            {/* Glare Sheen */}
            <rect x="5" y="10" width="10" height="96" rx="2" fill="url(#specularSheen)" opacity="0.4" />
          </g>
        )}

        {/* Option 3: Technical SCADA (Precision Industrial ASME Standard) */}
        {option === 3 && (
          <g>
            {/* Structural Stand / Base Legs */}
            <g id="vessel-stand-option3">
              {/* Left Structural Support Leg & Gusset Bracket */}
              <polygon points="10,102 10,112 4,102" fill="#0369A1" stroke="#0284C7" strokeWidth="1" />
              <rect x="10" y="102" width="6" height="22" rx="1" fill="#075985" stroke="#0284C7" strokeWidth="1.2" />
              <rect x="6" y="123" width="14" height="3" rx="1" fill="#0F172A" stroke="#38BDF8" strokeWidth="1" />
              <circle cx="8" cy="124.5" r="0.8" fill="#FFFFFF" />
              <circle cx="18" cy="124.5" r="0.8" fill="#FFFFFF" />

              {/* Right Structural Support Leg & Gusset Bracket */}
              <polygon points="72,102 72,112 78,102" fill="#0369A1" stroke="#0284C7" strokeWidth="1" />
              <rect x="66" y="102" width="6" height="22" rx="1" fill="#075985" stroke="#0284C7" strokeWidth="1.2" />
              <rect x="62" y="123" width="14" height="3" rx="1" fill="#0F172A" stroke="#38BDF8" strokeWidth="1" />
              <circle cx="64" cy="124.5" r="0.8" fill="#FFFFFF" />
              <circle cx="74" cy="124.5" r="0.8" fill="#FFFFFF" />

              {/* Horizontal Cross-Tie Stabilizer Beam */}
              <line x1="16" y1="117" x2="66" y2="117" stroke="#0284C7" strokeWidth="1.8" />

              {/* Bottom Drain Outlet Nozzle Flange */}
              <rect x="38" y="113" width="6" height="7" fill="#CBD5E1" stroke="#0284C7" strokeWidth="1" />
              <line x1="35" y1="120" x2="47" y2="120" stroke="#0284C7" strokeWidth="1.5" />
            </g>

            {/* ASME Steel Shell */}
            <path d="M 1 22 C 1 4, 81 4, 81 22 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="2.2" />
            <rect x="1" y="22" width="80" height="78" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="2.2" />
            <path d="M 1 100 C 1 118, 81 118, 81 100 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="2.2" />

            {/* Heavy Girth Weld Seams */}
            <line x1="1" y1="32" x2="81" y2="32" stroke="#38BDF8" strokeWidth="1.8" strokeDasharray="3 2" />
            <line x1="1" y1="92" x2="81" y2="92" stroke="#38BDF8" strokeWidth="1.8" strokeDasharray="3 2" />

            {/* Top Flanged Inspection Manway Hatch */}
            <rect x="30" y="2" width="22" height="6" rx="1.5" fill="#CBD5E1" stroke="#0284C7" strokeWidth="1.2" />
            <circle cx="34" cy="5" r="0.9" fill="#475569" />
            <circle cx="41" cy="5" r="0.9" fill="#475569" />
            <circle cx="48" cy="5" r="0.9" fill="#475569" />

            {/* Frontal 5-Valve Manifold Pipe Tree */}
            <g transform={`translate(${type === "PSF" ? 14 : type === "ACF" ? 58 : 36}, 36)`}>
              <line x1="0" y1="0" x2="0" y2="52" stroke="#0284C7" strokeWidth="3" />
              <circle cx="0" cy="10" r="4.5" fill="#DCFCE7" stroke="#16A34A" strokeWidth="1.2" />
              <polygon points="-3,10 0,7 3,10" fill="#15803D" />
              <circle cx="0" cy="42" r="4.5" fill="#DCFCE7" stroke="#16A34A" strokeWidth="1.2" />
              <polygon points="-3,42 0,45 3,42" fill="#15803D" />
            </g>

            {/* Dial Pressure / Hardness Gauge */}
            <g transform={`translate(${type === "PSF" ? 62 : type === "ACF" ? 20 : 62}, 28)`}>
              <circle cx="0" cy="0" r="9" fill="#FFFFFF" stroke="#0284C7" strokeWidth="1.3" />
              <circle cx="0" cy="0" r="7.5" fill="#F0F9FF" />
              <line x1="0" y1="0" x2="4.5" y2="-4" stroke="#DC2626" strokeWidth="1.2" />
              <circle cx="0" cy="0" r="1.4" fill="#0F172A" />
              <text x="0" y="14" textAnchor="middle" fill="#0369A1" fontSize="7.2" fontWeight="bold" fontFamily="monospace">
                {type === "PSF" ? `${inletPressure.toFixed(2)}B` : type === "ACF" ? `${outletPressure.toFixed(2)}B` : `${softwaterHardness.toFixed(0)}ppm`}
              </text>
            </g>

            <rect x="5" y="10" width="8" height="96" rx="2" fill="url(#specularSheen)" opacity="0.5" />
          </g>
        )}

        {/* Option 4: Full Monolithic Cutaway (Streamlined Modern) */}
        {option === 4 && (
          <g>
            {/* Outer Hull */}
            <path d="M 1 22 C 1 4, 81 4, 81 22 Z" fill="#0F172A" stroke="#0284C7" strokeWidth="2" />
            <rect x="1" y="22" width="80" height="78" fill="#0F172A" stroke="#0284C7" strokeWidth="2" />
            <path d="M 1 100 C 1 118, 81 118, 81 100 Z" fill="#0F172A" stroke="#0284C7" strokeWidth="2" />

            {/* Full Monolithic Media Bed */}
            {type === "PSF" ? (
              <>
                <path d="M 3 22 C 3 8, 79 8, 79 22 L 79 32 L 3 32 Z" fill="#BAE6FD" opacity="0.6" />
                <rect x="3" y="32" width="76" height="34" fill="url(#sandMediaGrad)" />
                <rect x="3" y="66" width="76" height="18" fill="#B45309" />
                <rect x="3" y="84" width="76" height="20" fill="#451A03" />
              </>
            ) : type === "ACF" ? (
              <>
                <path d="M 3 22 C 3 8, 79 8, 79 22 L 79 32 L 3 32 Z" fill="#BAE6FD" opacity="0.6" />
                <rect x="3" y="32" width="76" height="52" fill="url(#carbonMediaGrad)" />
                <rect x="3" y="84" width="76" height="20" fill="#1E293B" />
              </>
            ) : (
              <>
                <path d="M 3 22 C 3 8, 79 8, 79 22 L 79 32 L 3 32 Z" fill="#BAE6FD" opacity="0.6" />
                <rect x="3" y="32" width="76" height="52" fill="url(#resinMediaGrad)" />
                <rect x="3" y="84" width="76" height="20" fill="#78350F" />
              </>
            )}

            {/* Clean Specular Glare Strip */}
            <rect x="6" y="8" width="12" height="102" rx="3" fill="url(#specularSheen)" opacity="0.45" />
            {/* Bottom Collector Lateral Line */}
            <line x1="16" y1="98" x2="66" y2="98" stroke="#CBD5E1" strokeWidth="2" strokeLinecap="round" />
          </g>
        )}

        {/* Vessel Identifier Name Tag - Centered in Vessel Body */}
        {type === "PSF" && renderMiniTag(41, 62, "PSF", 62)}
        {type === "ACF" && renderMiniTag(41, 62, "ACF", 62)}
        {type === "SOFTENER" && renderMiniTag(41, 62, "SOFTENER", 66)}
      </g>
    )
  }

  // Industrial UKL 4-Port Multiport Valve (MPV) Component
  const renderMultiportValve = (
    name: string,
    mode: MultiportValveMode,
    onToggle: () => void
  ) => {
    // Mode to angle mapping for 4 operational cycles:
    // 1. SERVICE: 0 deg (Top / 12 o'clock - Port 1 Inlet to Port 2 Outlet)
    // 2. DRAIN / WASTE: 90 deg (Right / 3 o'clock - Direct Bypass to Port 4 Drain)
    // 3. BACKWASH: 180 deg (Bottom / 6 o'clock - Reverse Flow to Port 4 Drain)
    // 4. RINSE: 270 deg (Left / 9 o'clock - Downward Fast Rinse to Port 4 Drain)
    const angleMap: Record<MultiportValveMode, number> = {
      SERVICE: 0,
      DRAIN: 90,
      BACKWASH: 180,
      RINSE: 270,
    }
    const nextModeMap: Record<MultiportValveMode, MultiportValveMode> = {
      SERVICE: "BACKWASH",
      BACKWASH: "RINSE",
      RINSE: "DRAIN",
      DRAIN: "SERVICE",
    }
    const angle = angleMap[mode] ?? 0
    const nextMode = nextModeMap[mode] ?? "SERVICE"

    return (
      <g
        className="cursor-pointer group transition-transform duration-200 hover:scale-[1.03]"
        onClick={onToggle}
      >
        <title>{`${name} 4-Port Multiport Valve: Mode ${mode} (Click to switch to ${nextMode})`}</title>

        {/* Scaled to exactly match SCADA pump visual diameter (r=15 outer casing vs r=14 pump casing) */}
        <g transform="translate(30, 30) scale(0.65) translate(-30, -30)">
          {/* 4 Threaded Pipe Union Nozzles (Clean Orthogonal 4-Way Configuration) */}

          {/* Port 1: Top Nozzle (12 o'clock - Raw Water Inlet) */}
          <g id={`${name}-p1-top`}>
            <rect x="23" y="0" width="14" height="10" rx="1" fill="#18181B" stroke="#09090B" strokeWidth="0.8" />
            <line x1="24" y1="2.5" x2="36" y2="2.5" stroke="#3F3F46" strokeWidth="0.8" />
            <line x1="24" y1="5" x2="36" y2="5" stroke="#3F3F46" strokeWidth="0.8" />
            <line x1="24" y1="7.5" x2="36" y2="7.5" stroke="#3F3F46" strokeWidth="0.8" />
            <rect x="20.5" y="8" width="19" height="5" rx="1.5" fill="#27272A" stroke="#09090B" strokeWidth="0.8" />
            <line x1="24" y1="8" x2="24" y2="13" stroke="#3F3F46" strokeWidth="0.6" />
            <line x1="30" y1="8" x2="30" y2="13" stroke="#3F3F46" strokeWidth="0.6" />
            <line x1="36" y1="8" x2="36" y2="13" stroke="#3F3F46" strokeWidth="0.6" />
          </g>

          {/* Port 2: Bottom Nozzle (6 o'clock - Filtered Outlet) */}
          <g id={`${name}-p2-bottom`} transform="rotate(180 30 30)">
            <rect x="23" y="0" width="14" height="10" rx="1" fill="#18181B" stroke="#09090B" strokeWidth="0.8" />
            <line x1="24" y1="2.5" x2="36" y2="2.5" stroke="#3F3F46" strokeWidth="0.8" />
            <line x1="24" y1="5" x2="36" y2="5" stroke="#3F3F46" strokeWidth="0.8" />
            <line x1="24" y1="7.5" x2="36" y2="7.5" stroke="#3F3F46" strokeWidth="0.8" />
            <rect x="20.5" y="8" width="19" height="5" rx="1.5" fill="#27272A" stroke="#09090B" strokeWidth="0.8" />
            <line x1="24" y1="8" x2="24" y2="13" stroke="#3F3F46" strokeWidth="0.6" />
            <line x1="30" y1="8" x2="30" y2="13" stroke="#3F3F46" strokeWidth="0.6" />
            <line x1="36" y1="8" x2="36" y2="13" stroke="#3F3F46" strokeWidth="0.6" />
          </g>

          {/* Port 3: Left Nozzle (9 o'clock - Vessel Manifold Connection / Drain) */}
          <g id={`${name}-p3-left`} transform="rotate(270 30 30)">
            <rect x="23" y="0" width="14" height="10" rx="1" fill="#18181B" stroke="#09090B" strokeWidth="0.8" />
            <line x1="24" y1="2.5" x2="36" y2="2.5" stroke="#3F3F46" strokeWidth="0.8" />
            <line x1="24" y1="5" x2="36" y2="5" stroke="#3F3F46" strokeWidth="0.8" />
            <line x1="24" y1="7.5" x2="36" y2="7.5" stroke="#3F3F46" strokeWidth="0.8" />
            <rect x="20.5" y="8" width="19" height="5" rx="1.5" fill="#27272A" stroke="#09090B" strokeWidth="0.8" />
            <line x1="24" y1="8" x2="24" y2="13" stroke="#3F3F46" strokeWidth="0.6" />
            <line x1="30" y1="8" x2="30" y2="13" stroke="#3F3F46" strokeWidth="0.6" />
            <line x1="36" y1="8" x2="36" y2="13" stroke="#3F3F46" strokeWidth="0.6" />
          </g>

          {/* Port 4: Right Nozzle (3 o'clock - Drain / Vessel Manifold Connection) */}
          <g id={`${name}-p4-right`} transform="rotate(90 30 30)">
            <rect x="23" y="0" width="14" height="10" rx="1" fill="#18181B" stroke="#09090B" strokeWidth="0.8" />
            <line x1="24" y1="2.5" x2="36" y2="2.5" stroke="#3F3F46" strokeWidth="0.8" />
            <line x1="24" y1="5" x2="36" y2="5" stroke="#3F3F46" strokeWidth="0.8" />
            <line x1="24" y1="7.5" x2="36" y2="7.5" stroke="#3F3F46" strokeWidth="0.8" />
            <rect x="20.5" y="8" width="19" height="5" rx="1.5" fill="#27272A" stroke="#09090B" strokeWidth="0.8" />
            <line x1="24" y1="8" x2="24" y2="13" stroke="#3F3F46" strokeWidth="0.6" />
            <line x1="30" y1="8" x2="30" y2="13" stroke="#3F3F46" strokeWidth="0.6" />
            <line x1="36" y1="8" x2="36" y2="13" stroke="#3F3F46" strokeWidth="0.6" />
          </g>

          {/* Main Outer Casing Flange Body (Centered at cx=30, cy=30) */}
          <circle cx="30" cy="30" r="23" fill="url(#mpvCasingGrad)" stroke="#3F3F46" strokeWidth="1.2" />
          <circle cx="30" cy="30" r="21.5" fill="none" stroke="#18181B" strokeWidth="1" />

          {/* 12 Flange Perimeter Hex Bolts (R = 19.2 around cx=30, cy=30) */}
          <circle cx="49.2" cy="30" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" strokeWidth="0.4" />
          <circle cx="49.0" cy="29.8" r="0.4" fill="#FFFFFF" />
          <circle cx="46.6" cy="39.6" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" strokeWidth="0.4" />
          <circle cx="46.4" cy="39.4" r="0.4" fill="#FFFFFF" />
          <circle cx="39.6" cy="46.6" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" strokeWidth="0.4" />
          <circle cx="39.4" cy="46.4" r="0.4" fill="#FFFFFF" />
          <circle cx="30" cy="49.2" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" strokeWidth="0.4" />
          <circle cx="29.8" cy="49.0" r="0.4" fill="#FFFFFF" />
          <circle cx="20.4" cy="46.6" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" strokeWidth="0.4" />
          <circle cx="20.2" cy="46.4" r="0.4" fill="#FFFFFF" />
          <circle cx="13.4" cy="39.6" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" strokeWidth="0.4" />
          <circle cx="13.2" cy="39.4" r="0.4" fill="#FFFFFF" />
          <circle cx="10.8" cy="30" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" strokeWidth="0.4" />
          <circle cx="10.6" cy="29.8" r="0.4" fill="#FFFFFF" />
          <circle cx="13.4" cy="20.4" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" strokeWidth="0.4" />
          <circle cx="13.2" cy="20.2" r="0.4" fill="#FFFFFF" />
          <circle cx="20.4" cy="13.4" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" strokeWidth="0.4" />
          <circle cx="20.2" cy="13.2" r="0.4" fill="#FFFFFF" />
          <circle cx="30" cy="10.8" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" strokeWidth="0.4" />
          <circle cx="29.8" cy="10.6" r="0.4" fill="#FFFFFF" />
          <circle cx="39.6" cy="13.4" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" strokeWidth="0.4" />
          <circle cx="39.4" cy="13.2" r="0.4" fill="#FFFFFF" />
          <circle cx="46.6" cy="20.4" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" strokeWidth="0.4" />
          <circle cx="46.4" cy="20.2" r="0.4" fill="#FFFFFF" />

          {/* Inner Bezel Ring */}
          <circle cx="30" cy="30" r="16" fill="#09090B" stroke="#27272A" strokeWidth="0.8" />

          {/* Blue Dial Plate Face */}
          <circle cx="30" cy="30" r="14.8" fill="url(#mpvDialGrad)" stroke="#38BDF8" strokeWidth="0.6" />
          <circle cx="30" cy="30" r="13.6" fill="none" stroke="#60A5FA" strokeWidth="0.4" strokeOpacity="0.5" />

          {/* Animated Internal Fluid Flow Paths (When Simulation is Active) */}
          {isPlaying && (
            <g id={`${name}-fluid-animations`}>
              {/* Pulsing Active Core Ring */}
              <circle cx="30" cy="30" r="14.2" fill="none" stroke="#38BDF8" strokeWidth="1" opacity="0.3">
                <animate attributeName="opacity" values="0.15;0.7;0.15" dur={`${1.8 / simSpeed}s`} repeatCount="indefinite" />
              </circle>

              {/* Mode: SERVICE - Fluid downflow stream from Inlet to Vessel & Outlet */}
              {mode === "SERVICE" && (
                <g>
                  <path d="M 30 10 L 30 23 M 30 37 L 30 50" stroke="#BAE6FD" strokeWidth="1.8" strokeLinecap="round" strokeDasharray="3 3">
                    <animate attributeName="stroke-dashoffset" from="12" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                  </path>
                  <circle cx="30" cy="30" r="5" fill="#38BDF8" opacity="0.2">
                    <animate attributeName="r" values="3;6;3" dur={`${1.2 / simSpeed}s`} repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0.3;0.1;0.3" dur={`${1.2 / simSpeed}s`} repeatCount="indefinite" />
                  </circle>
                </g>
              )}

              {/* Mode: BACKWASH / RINSE / DRAIN - Flush discharge stream to Port 4 Drain */}
              {(mode === "BACKWASH" || mode === "RINSE" || mode === "DRAIN") && (
                <path d="M 30 30 L 50 30" stroke="#FCA5A5" strokeWidth="2" strokeLinecap="round" strokeDasharray="3 3">
                  <animate attributeName="stroke-dashoffset" from="12" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              )}
            </g>
          )}

          {/* 4 Dial Cycle Step Markings */}
          {/* 1. Top (0°): SERVICE */}
          <g transform="rotate(0 30 30)">
            <polygon points="30,16.5 28,18.8 32,18.8" fill="#FACC15" />
          </g>

          {/* 2. Right (90°): DRAIN */}
          <g transform="rotate(90 30 30)">
            <polygon points="30,16.5 28,18.8 32,18.8" fill="#FACC15" />
          </g>

          {/* 3. Bottom (180°): BACKWASH */}
          <g transform="rotate(180 30 30)">
            <polygon points="30,16.5 28,18.8 32,18.8" fill="#FACC15" />
          </g>

          {/* 4. Left (270°): RINSE */}
          <g transform="rotate(270 30 30)">
            <polygon points="30,16.5 28,18.8 32,18.8" fill="#FACC15" />
          </g>

          {/* Central Rotor Boss */}
          <circle cx="30" cy="30" r="7" fill="#18181B" stroke="#09090B" strokeWidth="1" />

          {/* Rotary Selector Handle Lever with Smooth CSS Transition */}
          <g
            transform={`rotate(${angle} 30 30)`}
            style={{ transition: "transform 0.45s cubic-bezier(0.4, 0, 0.2, 1)" }}
          >
            <path
              d="M 28 30 L 27.5 22 L 25 12 C 25 8.5 35 8.5 35 12 L 32.5 22 L 32 30 Z"
              fill="url(#mpvHandleGrad)"
              stroke="#09090B"
              strokeWidth="0.8"
            />
            <line x1="30" y1="11" x2="30" y2="24" stroke="#52525B" strokeWidth="0.7" strokeLinecap="round" />
            <polygon points="30,8.5 28.8,11 31.2,11" fill="#FACC15" />
            <circle cx="30" cy="30" r="3.6" fill="#18181B" stroke="#3F3F46" strokeWidth="0.7" />
            <circle cx="30" cy="30" r="1.8" fill="url(#mpvBoltGrad)" stroke="#475569" strokeWidth="0.3" />
            <circle cx="29.5" cy="29.5" r="0.5" fill="#FFFFFF" />
          </g>
        </g>
      </g>
    )
  }
  interface TelemetryParam {
    label: string
    value: string | number
    unit?: string
  }

  // Dual-Parameter Telemetry Card Renderer (Enhanced Readability SCADA Pill)
  const renderTelemetryCard = (
    x: number,
    y: number,
    _tag: string,
    params: TelemetryParam[],
    status: "RUNNING" | "STANDBY" | "STOPPED" | "NORMAL" = "NORMAL",
    width: number = 88,
    height?: number
  ) => {
    const isOk = status === "RUNNING" || status === "NORMAL"
    const borderColor = isOk ? "#4ADE80" : "#F87171"
    const finalWidth = width ?? 88
    const cardHeight = height ?? (params.length > 1 ? 25 : 16)

    return (
      <g
        transform={`translate(${x}, ${y})`}
        className="pointer-events-none select-none"
        style={{ filter: "drop-shadow(0px 2px 3px rgba(15, 23, 42, 0.20))" }}
      >
        {/* Crisp solid white container with state-colored border */}
        <rect
          x="0"
          y="0"
          width={finalWidth}
          height={cardHeight}
          rx="5"
          fill="#FFFFFF"
          stroke={borderColor}
          strokeWidth="1.4"
        />

        {params.map((p, idx) => {
          const yPos = params.length === 1 ? 11.5 : 10.5 + idx * 11.5
          return (
            <g key={idx}>
              {idx > 0 && (
                <line x1="4" y1={yPos - 7.5} x2={finalWidth - 4} y2={yPos - 7.5} stroke="#E2E8F0" strokeWidth="0.8" />
              )}
              <text x="6" y={yPos} fill="#334155" fontSize="8.4" fontFamily="monospace" fontWeight="700">
                {p.label}:
              </text>
              <text x={finalWidth - 6} y={yPos} textAnchor="end" fill="#0F172A" fontSize="9.2" fontWeight="bold" fontFamily="monospace">
                {p.value}{p.unit ? <tspan fill="#64748B" fontSize="7.4" fontWeight="600"> {p.unit}</tspan> : ""}
              </text>
            </g>
          )
        })}
      </g>
    )
  }

  const renderTelemetryBadge = (
    x: number,
    y: number,
    tag: string,
    paramLabel: string,
    paramValue: string | number,
    unit: string,
    status: "RUNNING" | "STANDBY" | "STOPPED" | "NORMAL" = "NORMAL",
    width: number = 68,
    height: number = 16
  ) => {
    return renderTelemetryCard(x, y, tag, [{ label: paramLabel, value: paramValue, unit }], status, width, height)
  }

  return (
    <div className="w-full h-full flex-1 min-h-0 flex flex-col bg-white rounded-xl sm:rounded-2xl overflow-hidden border border-sky-200/90 shadow-xl shadow-sky-950/5 font-sans select-none text-slate-900">
      {/* 1. SCADA Header / Control Deck */}
      <div className="shrink-0 px-2.5 sm:px-4 py-1 sm:py-1.5 [@media(max-height:500px)]:py-0.5 bg-sky-50/70 border-b border-sky-100 flex flex-wrap items-center justify-between gap-1.5 sm:gap-3">
        <div className="flex items-center gap-2 sm:gap-3">
          <div className="flex items-center gap-1.5 sm:gap-2">
            <span className="relative flex h-2.5 w-2.5 sm:h-3 sm:w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 sm:h-3 sm:w-3 bg-emerald-500" />
            </span>
            <div className="flex flex-col">
              <div className="flex items-center gap-1.5 sm:gap-2">
                <span className="font-mono text-xs sm:text-sm [@media(max-height:500px)]:text-[11px] font-black tracking-wider uppercase text-sky-900">
                  SCADA MIMIC · STP PROCESS SCHEMATIC
                </span>
                <span className="px-1.5 sm:px-2 py-0.5 rounded text-[9px] sm:text-[10px] font-mono bg-emerald-100 text-emerald-800 border border-emerald-300 font-bold">
                  ONLINE
                </span>
              </div>
              <span className="text-[11px] text-slate-500 font-mono [@media(max-height:500px)]:hidden">
                System Tag: STP-NANNEER-PLANT-01 · MBBR Aeration &amp; Tertiary Media Polishing
              </span>
            </div>
          </div>
        </div>

        {/* Live Controls */}
        <div className="flex items-center gap-1.5 sm:gap-2 flex-wrap [@media(max-height:500px)]:gap-1">
          <button
            onClick={() => setControlMode((prev) => (prev === "AUTO" ? "MANUAL" : "AUTO"))}
            className={`flex items-center gap-1 sm:gap-1.5 px-2 sm:px-2.5 py-0.5 sm:py-1 rounded-md text-[11px] sm:text-xs font-mono font-bold border transition-colors ${controlMode === "AUTO"
              ? "bg-sky-100 text-sky-800 border-sky-300"
              : "bg-amber-100 text-amber-800 border-amber-300"
              }`}
          >
            <Sliders className="w-3 h-3 sm:w-3.5 sm:h-3.5" />
            <span>MODE: {controlMode}</span>
          </button>

          <div className="flex items-center bg-white rounded-md p-0.5 border border-sky-200 shadow-xs">
            {[1, 2, 5].map((speed) => (
              <button
                key={speed}
                onClick={() => setSimSpeed(speed)}
                className={`px-1.5 sm:px-2 py-0.5 text-[9px] sm:text-[10px] font-mono rounded ${simSpeed === speed ? "bg-sky-600 text-white font-bold" : "text-slate-600 hover:text-slate-900"
                  }`}
              >
                {speed}x
              </button>
            ))}
          </div>

          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className={`p-1 sm:p-1.5 rounded-md border text-xs font-medium transition-colors ${isPlaying
              ? "bg-white border-slate-300 text-amber-700 hover:bg-slate-50"
              : "bg-emerald-600 border-emerald-500 text-white hover:bg-emerald-700"
              }`}
          >
            {isPlaying ? <Pause className="w-3.5 h-3.5 sm:w-4 sm:h-4" /> : <Play className="w-3.5 h-3.5 sm:w-4 sm:h-4" />}
          </button>

          <button
            onClick={() => {
              setPsfSeconds(3 * 3600 + 20 * 60 + 24)
              setAcfSeconds(3 * 3600 + 20 * 60 + 25)
              setDo1(0.88)
            }}
            className="p-1 sm:p-1.5 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-slate-900 hover:bg-slate-50 transition-colors shadow-xs"
          >
            <RotateCcw className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
          </button>
        </div>
      </div>

      {/* 2. Main SCADA SVG Canvas (1200 x 780 viewbox space) */}
      <div className="relative w-full flex-1 min-h-0 flex items-center justify-center bg-gradient-to-b from-white via-sky-50/25 to-white overflow-hidden">
        {/* Subtle Blueprint Dot Grid */}
        <div
          className="absolute inset-0 pointer-events-none opacity-35"
          style={{
            backgroundImage: `radial-gradient(circle at 1px 1px, #0284c718 1px, transparent 0)`,
            backgroundSize: "20px 20px",
          }}
        />

        {/* Top-Right Partner Logos Badge Inside Schematic Canvas (Tiny 8px on Mobile S <375px, 10px on Mobile M/L >=375px, 20px on sm/md tablet, 28px on lg 1024px, 36px on xl 1440px) */}
        <div className="absolute top-1 right-1 sm:top-1.5 sm:right-1.5 md:top-1.5 md:right-1.5 lg:top-2 lg:right-2 xl:top-3 xl:right-3 2xl:top-4 2xl:right-4 [@media(max-height:500px)]:top-1 [@media(max-height:500px)]:right-1.5 z-20 flex items-center gap-0.5 sm:gap-1.5 md:gap-1 lg:gap-1.5 xl:gap-2 2xl:gap-3 [@media(max-height:500px)]:gap-0.5 bg-white/95 backdrop-blur-xs p-0.5 min-[375px]:px-1 min-[375px]:py-0.5 sm:px-1.5 sm:py-0.5 md:px-1.5 md:py-0.5 lg:px-2 lg:py-1 xl:px-2.5 xl:py-1.5 2xl:px-3 2xl:py-2 [@media(max-height:500px)]:p-0.5 rounded-xs sm:rounded-md lg:rounded-lg xl:rounded-xl 2xl:rounded-2xl border border-sky-200/90 shadow-xs sm:shadow-md shadow-sky-950/10 pointer-events-auto">
          <div className="relative h-2 w-2 min-[375px]:h-2.5 min-[375px]:w-2.5 sm:h-5 sm:w-5 md:h-5 md:w-5 lg:h-7 lg:w-7 xl:h-9 xl:w-9 2xl:h-11 2xl:w-11 [@media(max-height:500px)]:h-2.5 [@media(max-height:500px)]:w-2.5 flex items-center justify-center">
            <Image
              src="/images/prestige-group-logo.png"
              alt="Prestige Group Logo"
              width={80}
              height={80}
              className="h-2 w-2 min-[375px]:h-2.5 min-[375px]:w-2.5 sm:h-5 sm:w-5 md:h-5 md:w-5 lg:h-7 lg:w-7 xl:h-9 xl:w-9 2xl:h-11 2xl:w-11 [@media(max-height:500px)]:h-2.5 [@media(max-height:500px)]:w-2.5 object-contain"
              priority
            />
          </div>
          <div className="h-1.5 min-[375px]:h-2 sm:h-3.5 md:h-3.5 lg:h-4.5 xl:h-6 2xl:h-8 [@media(max-height:500px)]:h-2 w-px bg-slate-200" aria-hidden="true" />
          <div className="relative h-2 w-2 min-[375px]:h-2.5 min-[375px]:w-2.5 sm:h-5 sm:w-5 md:h-5 md:w-5 lg:h-7 lg:w-7 xl:h-9 xl:w-9 2xl:h-11 2xl:w-11 [@media(max-height:500px)]:h-2.5 [@media(max-height:500px)]:w-2.5 flex items-center justify-center">
            <Image
              src="/images/ppms-logo.jpg"
              alt="PPMS Logo"
              width={80}
              height={80}
              className="h-2 w-2 min-[375px]:h-2.5 min-[375px]:w-2.5 sm:h-5 sm:w-5 md:h-5 md:w-5 lg:h-7 lg:w-7 xl:h-9 xl:w-9 2xl:h-11 2xl:w-11 [@media(max-height:500px)]:h-2.5 [@media(max-height:500px)]:w-2.5 object-contain rounded-full"
              priority
            />
          </div>
        </div>

        <svg
          viewBox="-65 0 1405 710"
          className="w-full h-full max-h-full max-w-full block"
          preserveAspectRatio="none"
        >
          <defs>
            {/* 1. Raw Sewage / Influent & Collection Tank Water (Dark Sludge Brown Influent) */}
            <linearGradient id="rawSewageGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#795548" stopOpacity="0.90" />
              <stop offset="45%" stopColor="#5D4037" stopOpacity="0.94" />
              <stop offset="100%" stopColor="#3E2723" stopOpacity="0.97" />
            </linearGradient>

            {/* Collection Tank Wave Gradients & Fluid Mask */}
            <linearGradient id="rawSewageWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#A1887F" stopOpacity="0.90" />
              <stop offset="40%" stopColor="#6D4C41" stopOpacity="0.92" />
              <stop offset="100%" stopColor="#3E2723" stopOpacity="0.96" />
            </linearGradient>
            <linearGradient id="rawSewageWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#8D6E63" stopOpacity="0.75" />
              <stop offset="100%" stopColor="#4E342E" stopOpacity="0.92" />
            </linearGradient>
            <clipPath id="collectionTankFluidClip">
              <path d="M 2 16 Q 87.5 24 173 16 L 173 76 Q 87.5 93 2 76 Z" />
            </clipPath>

            {/* 2. MBBR Aeration Tank (Aerated Mixed Liquor - Murky Raw Sewage / Bio-Mix) */}
            <linearGradient id="mbbrWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#A1887F" stopOpacity="0.88" />
              <stop offset="45%" stopColor="#8D6E63" stopOpacity="0.92" />
              <stop offset="100%" stopColor="#5D4037" stopOpacity="0.96" />
            </linearGradient>
            <linearGradient id="mbbrWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#D7CCC8" stopOpacity="0.88" />
              <stop offset="40%" stopColor="#8D6E63" stopOpacity="0.88" />
              <stop offset="100%" stopColor="#5D4037" stopOpacity="0.96" />
            </linearGradient>
            <linearGradient id="mbbrWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#A1887F" stopOpacity="0.65" />
              <stop offset="100%" stopColor="#4E342E" stopOpacity="0.90" />
            </linearGradient>
            <clipPath id="mbbrTankFluidClip">
              <path d="M 2 16 Q 70 24 138 16 L 138 76 Q 70 93 2 76 Z" />
            </clipPath>

            {/* 4. Clarifier Tank with Arm (Phase Separation: Settling Supernatant Water) */}
            <linearGradient id="clarifierWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#D2C59D" stopOpacity="0.88" />
              <stop offset="35%" stopColor="#B8AA7B" stopOpacity="0.86" />
              <stop offset="68%" stopColor="#8D6E63" stopOpacity="0.90" />
              <stop offset="100%" stopColor="#3E2723" stopOpacity="0.98" />
            </linearGradient>
            <linearGradient id="clarifierWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#EFE8D0" stopOpacity="0.88" />
              <stop offset="45%" stopColor="#D2C59D" stopOpacity="0.85" />
              <stop offset="100%" stopColor="#A69865" stopOpacity="0.92" />
            </linearGradient>
            <linearGradient id="clarifierWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#C4B788" stopOpacity="0.65" />
              <stop offset="100%" stopColor="#8C7C4E" stopOpacity="0.88" />
            </linearGradient>
            <clipPath id="clarifierWaterClip">
              <path d="M 2 16 Q 70 24 138 16 L 138 54 L 119 67 L 21 67 L 2 54 Z" />
            </clipPath>

            {/* 5. Sludge Holding Tank (Dense Thickened Waste Activated Sludge) */}
            <linearGradient id="sludgeWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#5D4037" stopOpacity="0.95" />
              <stop offset="50%" stopColor="#3E2723" stopOpacity="0.97" />
              <stop offset="100%" stopColor="#211109" stopOpacity="0.99" />
            </linearGradient>
            <linearGradient id="sludgeWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#8D6E63" stopOpacity="0.88" />
              <stop offset="40%" stopColor="#5D4037" stopOpacity="0.92" />
              <stop offset="100%" stopColor="#211109" stopOpacity="0.98" />
            </linearGradient>
            <linearGradient id="sludgeWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#6D4C41" stopOpacity="0.70" />
              <stop offset="100%" stopColor="#1B0000" stopOpacity="0.95" />
            </linearGradient>
            <clipPath id="sludgeTankFluidClip">
              <path d="M 2 16 Q 57.5 24 113 16 L 113 46 L 73 68 Q 57.5 73 42 68 L 2 46 Z" />
            </clipPath>

            {/* 6. Filter Feed Tank (Pre-Filtered Secondary Effluent - Translucent Greenish Aquamarine) */}
            <linearGradient id="filterFeedGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#D1F4EC" stopOpacity="0.88" />
              <stop offset="45%" stopColor="#80CBC4" stopOpacity="0.86" />
              <stop offset="100%" stopColor="#00897B" stopOpacity="0.92" />
            </linearGradient>
            <linearGradient id="filterFeedWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#E6FAF5" stopOpacity="0.88" />
              <stop offset="40%" stopColor="#A7F3D0" stopOpacity="0.86" />
              <stop offset="100%" stopColor="#2DD4BF" stopOpacity="0.95" />
            </linearGradient>
            <linearGradient id="filterFeedWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#A7F3D0" stopOpacity="0.65" />
              <stop offset="100%" stopColor="#0F766E" stopOpacity="0.88" />
            </linearGradient>
            <clipPath id="filterFeedTankFluidClip">
              <path d="M 2 16 Q 70 24 138 16 L 138 76 Q 70 93 2 76 Z" />
            </clipPath>

            {/* 7. Treated Water Tank (Disinfected Clean Tertiary Water - Bright Sky-Blue) */}
            <linearGradient id="treatedWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#E0F2FE" stopOpacity="0.95" />
              <stop offset="45%" stopColor="#38BDF8" stopOpacity="0.92" />
              <stop offset="100%" stopColor="#0284C7" stopOpacity="0.95" />
            </linearGradient>
            <linearGradient id="treatedWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#E0F2FE" stopOpacity="0.9" />
              <stop offset="40%" stopColor="#38BDF8" stopOpacity="0.88" />
              <stop offset="100%" stopColor="#0284C7" stopOpacity="0.96" />
            </linearGradient>
            <linearGradient id="treatedWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#38BDF8" stopOpacity="0.65" />
              <stop offset="100%" stopColor="#0369A1" stopOpacity="0.90" />
            </linearGradient>
            <clipPath id="treatedWaterTankFluidClip">
              <path d="M 2 16 Q 70 24 138 16 L 138 74 Q 70 89 2 74 Z" />
            </clipPath>

            {/* 8. Soft Water Tank (Pristine Polished Crystal Soft Water - Electric Pure Cyan) */}
            <linearGradient id="softWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#ECFEFF" stopOpacity="0.98" />
              <stop offset="45%" stopColor="#06B6D4" stopOpacity="0.95" />
              <stop offset="100%" stopColor="#0284C7" stopOpacity="0.98" />
            </linearGradient>
            <linearGradient id="softWaterWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.96" />
              <stop offset="40%" stopColor="#67E8F9" stopOpacity="0.90" />
              <stop offset="100%" stopColor="#0EA5E9" stopOpacity="0.96" />
            </linearGradient>
            <linearGradient id="softWaterWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#A5F3FC" stopOpacity="0.70" />
              <stop offset="100%" stopColor="#0891B2" stopOpacity="0.92" />
            </linearGradient>
            <clipPath id="softWaterTankFluidClip">
              <path d="M 2 16 Q 70 24 138 16 L 138 74 Q 70 89 2 74 Z" />
            </clipPath>

            {/* 9. Polished Stainless Steel 316 Pipe Gradients (Horizontal & Vertical) */}
            <linearGradient id="ssPipeH" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#64748B" />
              <stop offset="25%" stopColor="#FFFFFF" />
              <stop offset="55%" stopColor="#CBD5E1" />
              <stop offset="85%" stopColor="#94A3B8" />
              <stop offset="100%" stopColor="#475569" />
            </linearGradient>

            <linearGradient id="ssPipeV" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#64748B" />
              <stop offset="25%" stopColor="#FFFFFF" />
              <stop offset="55%" stopColor="#CBD5E1" />
              <stop offset="85%" stopColor="#94A3B8" />
              <stop offset="100%" stopColor="#475569" />
            </linearGradient>

            {/* Architectural Building Facade & Glass Gradients (Light Theme) */}
            <linearGradient id="buildingFacadeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.45" />
              <stop offset="25%" stopColor="#F0F9FF" stopOpacity="0.40" />
              <stop offset="70%" stopColor="#E0F2FE" stopOpacity="0.45" />
              <stop offset="100%" stopColor="#BAE6FD" stopOpacity="0.55" />
            </linearGradient>
            <linearGradient id="buildingGlassGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#E0F2FE" stopOpacity="0.55" />
              <stop offset="50%" stopColor="#BAE6FD" stopOpacity="0.50" />
              <stop offset="100%" stopColor="#7DD3FC" stopOpacity="0.60" />
            </linearGradient>

            {/* 10. 2.5D Cylindrical Glass Vessel Walls (Specular Highlight & Fresnel Backlight) */}
            <linearGradient id="glassCylinderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.5" />
              <stop offset="8%" stopColor="#FFFFFF" stopOpacity="0.85" />
              <stop offset="22%" stopColor="#F8FAFC" stopOpacity="0.3" />
              <stop offset="70%" stopColor="#E0F2FE" stopOpacity="0.2" />
              <stop offset="92%" stopColor="#38BDF8" stopOpacity="0.35" />
              <stop offset="100%" stopColor="#0284C7" stopOpacity="0.5" />
            </linearGradient>

            {/* 11. Top Glass Vessel Flange / Lip Gradient */}
            <linearGradient id="glassRimGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#94A3B8" stopOpacity="0.8" />
              <stop offset="25%" stopColor="#FFFFFF" stopOpacity="0.95" />
              <stop offset="70%" stopColor="#E2E8F0" stopOpacity="0.7" />
              <stop offset="100%" stopColor="#64748B" stopOpacity="0.9" />
            </linearGradient>

            {/* 12. Sand & Media Layers for PSF / ACF */}
            <linearGradient id="sandMediaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#FDE68A" stopOpacity="0.95" />
              <stop offset="45%" stopColor="#D97706" stopOpacity="0.95" />
              <stop offset="75%" stopColor="#78350F" stopOpacity="0.98" />
              <stop offset="100%" stopColor="#451A03" stopOpacity="0.98" />
            </linearGradient>

            <linearGradient id="carbonMediaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#475569" stopOpacity="0.95" />
              <stop offset="50%" stopColor="#1E293B" stopOpacity="0.98" />
              <stop offset="100%" stopColor="#0F172A" stopOpacity="0.99" />
            </linearGradient>

            <linearGradient id="resinMediaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#FBBF24" stopOpacity="0.95" />
              <stop offset="60%" stopColor="#D97706" stopOpacity="0.98" />
              <stop offset="100%" stopColor="#92400E" stopOpacity="0.99" />
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

            {/* UKL Multiport Valve (MPV) Gradients */}
            <radialGradient id="mpvCasingGrad" cx="45%" cy="40%" r="60%">
              <stop offset="0%" stopColor="#27272A" />
              <stop offset="60%" stopColor="#18181B" />
              <stop offset="100%" stopColor="#09090B" />
            </radialGradient>
            <linearGradient id="mpvDialGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#38BDF8" />
              <stop offset="30%" stopColor="#0284C7" />
              <stop offset="85%" stopColor="#1D4ED8" />
              <stop offset="100%" stopColor="#1E3A8A" />
            </linearGradient>
            <linearGradient id="mpvBoltGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#FFFFFF" />
              <stop offset="40%" stopColor="#E2E8F0" />
              <stop offset="80%" stopColor="#94A3B8" />
              <stop offset="100%" stopColor="#475569" />
            </linearGradient>
            <linearGradient id="mpvHandleGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#3F3F46" />
              <stop offset="45%" stopColor="#27272A" />
              <stop offset="100%" stopColor="#18181B" />
            </linearGradient>
          </defs>

          {/* Master Schematic Canvas Group - Shifted to balanced left margin */}
          <g id="scada-schematic-canvas" transform="translate(110, 0)">

            {/* ====================================================================== */}
            {/* PIPELINE NETWORK (100% FAITHFUL TO THE REFERENCE PHOTO)                */}
            {/* ====================================================================== */}

            {/* ====================================================================== */}
            {/* 2.5D FACILITY / BUILDING INFLUENT SOURCE (LIGHT ARCHITECTURAL THEME)   */}
            {/* 2x WIDTH (104px) & 3x HEIGHT (240px) TRANSPARENT CORPORATE TOWER       */}
            {/* ====================================================================== */}
            <g id="facility-building" transform="translate(-76, 10)">
              {/* 1. 3D Grounding Soft Contact Shadow */}
              <ellipse cx="52" cy="244" rx="52" ry="7" fill="#64748B" opacity="0.18" />
              <ellipse cx="52" cy="244" rx="36" ry="4.2" fill="#334155" opacity="0.22" />

              {/* 2. Architectural Concrete Foundation Pedestal (Translucent) */}
              <rect x="0" y="234" width="104" height="8" rx="2" fill="#E2E8F0" fillOpacity="0.55" stroke="#CBD5E1" strokeWidth="1" strokeOpacity="0.75" />
              <line x1="1" y1="235" x2="103" y2="235" stroke="#FFFFFF" strokeWidth="1" opacity="0.7" />

              {/* 3. Main Architectural Skyscraper Body (Transparent 2.5D Glass Monolith - 2x Width) */}
              <rect x="6" y="26" width="92" height="208" rx="3" fill="url(#buildingFacadeGrad)" stroke="#38BDF8" strokeWidth="1.2" strokeOpacity="0.8" />

              {/* 4. Rooftop Parapet, Terrace & Perimeter Railing (Translucent) */}
              <rect x="3" y="20" width="98" height="6.5" rx="1.5" fill="#F1F5F9" fillOpacity="0.55" stroke="#CBD5E1" strokeWidth="0.8" strokeOpacity="0.75" />
              <line x1="7" y1="17" x2="97" y2="17" stroke="#38BDF8" strokeWidth="1" strokeDasharray="3 1.5" opacity="0.85" />

              {/* Rooftop HVAC Mechanical Penthouse */}
              <rect x="16" y="10" width="32" height="10" rx="1.5" fill="#F8FAFC" fillOpacity="0.5" stroke="#CBD5E1" strokeWidth="0.8" strokeOpacity="0.7" />
              <line x1="20" y1="13" x2="44" y2="13" stroke="#94A3B8" strokeWidth="0.7" opacity="0.7" />
              <line x1="20" y1="16" x2="44" y2="16" stroke="#94A3B8" strokeWidth="0.7" opacity="0.7" />

              {/* Telecommunications Mast & Active Beacon */}
              <line x1="82" y1="20" x2="82" y2="4" stroke="#64748B" strokeWidth="1.4" />
              <circle cx="82" cy="4" r="2.2" fill="#0284C7">
                <animate attributeName="opacity" values="1; 0.3; 1" dur="1.2s" repeatCount="indefinite" />
              </circle>

              {/* 5. Triple-Bay Curtain-Wall Panoramic Window Bays & Spandrels (Transparent Crystal Glass) */}
              {/* Floor 8 */}
              <rect x="11" y="30" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <rect x="40" y="30" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <rect x="69" y="30" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <line x1="23" y1="30" x2="23" y2="43" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="52" y1="30" x2="52" y2="43" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="81" y1="30" x2="81" y2="43" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="6" y1="46" x2="98" y2="46" stroke="#CBD5E1" strokeWidth="1.2" strokeOpacity="0.6" />

              {/* Floor 7 (Manifold Level at y=50) */}
              <rect x="11" y="50" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <rect x="40" y="50" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <rect x="69" y="50" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <line x1="23" y1="50" x2="23" y2="63" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="52" y1="50" x2="52" y2="63" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="81" y1="50" x2="81" y2="63" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="6" y1="66" x2="98" y2="66" stroke="#CBD5E1" strokeWidth="1.2" strokeOpacity="0.6" />

              {/* Floor 6 */}
              <rect x="11" y="70" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <rect x="40" y="70" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <rect x="69" y="70" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <line x1="23" y1="70" x2="23" y2="83" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="52" y1="70" x2="52" y2="83" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="81" y1="70" x2="81" y2="83" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="6" y1="86" x2="98" y2="86" stroke="#CBD5E1" strokeWidth="1.2" strokeOpacity="0.6" />

              {/* Floor 5 */}
              <rect x="11" y="90" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <rect x="40" y="90" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <rect x="69" y="90" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <line x1="23" y1="90" x2="23" y2="103" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="52" y1="90" x2="52" y2="103" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="81" y1="90" x2="81" y2="103" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="6" y1="106" x2="98" y2="106" stroke="#CBD5E1" strokeWidth="1.2" strokeOpacity="0.6" />

              {/* Floor 4 */}
              <rect x="11" y="110" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <rect x="40" y="110" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <rect x="69" y="110" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <line x1="23" y1="110" x2="23" y2="123" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="52" y1="110" x2="52" y2="123" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="81" y1="110" x2="81" y2="123" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="6" y1="126" x2="98" y2="126" stroke="#CBD5E1" strokeWidth="1.2" strokeOpacity="0.6" />

              {/* Floor 3 */}
              <rect x="11" y="130" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <rect x="40" y="130" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <rect x="69" y="130" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <line x1="23" y1="130" x2="23" y2="143" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="52" y1="130" x2="52" y2="143" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="81" y1="130" x2="81" y2="143" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="6" y1="146" x2="98" y2="146" stroke="#CBD5E1" strokeWidth="1.2" strokeOpacity="0.6" />

              {/* Floor 2 */}
              <rect x="11" y="150" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <rect x="40" y="150" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <rect x="69" y="150" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <line x1="23" y1="150" x2="23" y2="163" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="52" y1="150" x2="52" y2="163" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="81" y1="150" x2="81" y2="163" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="6" y1="166" x2="98" y2="166" stroke="#CBD5E1" strokeWidth="1.2" strokeOpacity="0.6" />

              {/* Floor 1 */}
              <rect x="11" y="170" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <rect x="40" y="170" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <rect x="69" y="170" width="24" height="13" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" strokeWidth="0.6" strokeOpacity="0.8" />
              <line x1="23" y1="170" x2="23" y2="183" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="52" y1="170" x2="52" y2="183" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="81" y1="170" x2="81" y2="183" stroke="#0284C7" strokeWidth="0.5" opacity="0.35" />
              <line x1="6" y1="186" x2="98" y2="186" stroke="#CBD5E1" strokeWidth="1.2" strokeOpacity="0.6" />

              {/* Ground Floor Entrance Lobby & Canopy (Transparent Glass) */}
              <rect x="28" y="196" width="48" height="38" rx="1.5" fill="#FFFFFF" fillOpacity="0.45" stroke="#0284C7" strokeWidth="0.9" strokeOpacity="0.8" />
              {/* Modern Entrance Canopy */}
              <rect x="24" y="193" width="56" height="3" rx="0.8" fill="#0284C7" opacity="0.75" />
              {/* Double Glass Lobby Doors */}
              <rect x="34" y="200" width="17" height="34" fill="#E0F2FE" fillOpacity="0.5" stroke="#38BDF8" strokeWidth="0.5" />
              <rect x="53" y="200" width="17" height="34" fill="#E0F2FE" fillOpacity="0.5" stroke="#38BDF8" strokeWidth="0.5" />
              <line x1="52" y1="200" x2="52" y2="234" stroke="#0284C7" strokeWidth="0.6" opacity="0.6" />

              {/* 6. Cylindrical Glass Specular Reflection Glare (Matches Tanks & Vessels) */}
              <rect x="9" y="28" width="14" height="200" rx="2" fill="url(#specularSheen)" opacity="0.45" />

              {/* 7. Industrial Sewer Discharge Manifold (ANSI Flange at Ground Floor Yellow Marker, local y=208 / canvas y=218) */}
              <g id="building-sewer-discharge-manifold" transform="translate(94, 204)">
                {/* Stainless Steel Flange Ring */}
                <rect x="0" y="0" width="9" height="8" rx="1" fill="url(#metalRingGrad)" stroke="#64748B" strokeWidth="0.8" />
                {/* Flange Bolts */}
                <circle cx="4.5" cy="1.6" r="0.75" fill="#334155" />
                <circle cx="4.5" cy="6.4" r="0.75" fill="#334155" />
              </g>

              {/* 8. Precision SCADA Identification Badge (Light Mode) */}
              <g transform="translate(52, 2)">
                <rect x="-32" y="-8" width="64" height="15" rx="3" fill="#FFFFFF" fillOpacity="0.92" stroke="#0284C7" strokeWidth="1" />
                <circle cx="-25" cy="-0.5" r="2" fill="#16A34A">
                  <animate attributeName="opacity" values="1; 0.4; 1" dur="2s" repeatCount="indefinite" />
                </circle>
                <text x="3" y="-2" fill="#0369A1" fontSize="5" fontWeight="bold" textAnchor="middle" fontFamily="monospace">BUILDING</text>
                <text x="3" y="3.5" fill="#64748B" fontSize="3.5" fontWeight="bold" textAnchor="middle" fontFamily="monospace">SEWER SOURCE</text>
              </g>
            </g>

            {/* 1. RAW INFLUENT INLET FROM BUILDING (MURKY SEWAGE WATER) */}
            <g id="raw-influent-from-building">
              {/* Pipe from Building Ground Floor (27, 218) across to x=70, rises to y=60, then across to Collection Tank top inlet at (152, 60), down to (152, 68) */}
              <path d="M 27 218 L 70 218 L 70 60 L 152 60 L 152 68" stroke="#8D6E63" strokeWidth="5" fill="none" strokeLinejoin="round" />
              {/* Flow Arrows along the route */}
              <polygon points="46,214 54,218 46,222" fill="#8D6E63" />
              <polygon points="66,142 70,134 74,142" fill="#8D6E63" />
              <polygon points="107,56 115,60 107,64" fill="#8D6E63" />
              {isPlaying && (
                <path d="M 27 218 L 70 218 L 70 60 L 152 60 L 152 68" stroke="#D7CCC8" strokeWidth="2.5" strokeDasharray="5 7" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="32" to="0" dur={`${1.2 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              )}
              {/* Discharge Nozzle Flange at Pipe Mouth */}
              <rect x="148" y="66" width="8" height="3" rx="1" fill="#5D4037" stroke="#3E2723" strokeWidth="0.8" />
            </g>

            {/* 2. RED DRAIN & BACKWASH RETURN PIPELINE */}
            <g id="red-drain-pipeline">
              {/* Backwash Drain Line from PSF Valve (610, 480) to Central Riser (545, 480) */}
              <path d="M 610 480 L 545 480" stroke="#DC2626" strokeWidth="4.5" fill="none" />
              <polygon points="582,476 572,480 582,484" fill="#DC2626" />

              {/* Central vertical red riser from y=480 up to y=270 (Cleanly above ACF unit) */}
              <path d="M 545 480 L 545 270" stroke="#DC2626" strokeWidth="4.5" fill="none" />
              <polygon points="541,380 545,370 549,380" fill="#DC2626" />

              {/* Header running across completely ABOVE ACF and outside dashed boundary into Collection Tank left side (y=76) */}
              <path d="M 545 270 L 105 270 L 105 76 L 135 76" stroke="#DC2626" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
              <polygon points="265,266 255,270 265,274" fill="#DC2626" />
              <polygon points="101,165 105,155 109,165" fill="#DC2626" />
              <polygon points="126,72 134,76 126,80" fill="#DC2626" />

              {/* Animated backwash/rinse flow (Active ONLY during backwash/rinse, NO flow in standby) */}
              {isPlaying && (psfValveMode === "BACKWASH" || psfValveMode === "RINSE") && (
                <path
                  d="M 610 480 L 545 480 L 545 270 L 105 270 L 105 76 L 135 76"
                  stroke="#FCA5A5"
                  strokeWidth="2.5"
                  strokeDasharray="6 8"
                  fill="none"
                  strokeLinejoin="round"
                >
                  <animate attributeName="stroke-dashoffset" from="56" to="0" dur={`${1.4 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              )}
            </g>

            {/* 3. COLLECTION TANK TO MBBR AERATION TANK (VIA M1 / M2) */}
            <g id="collection-to-mbbr-lines">
              {/* Wall Flange Nozzle on Collection Tank */}
              <rect x="307" y="88" width="6" height="8" rx="1.5" fill="#64748B" stroke="#0284C7" strokeWidth="1" />
              {/* Stainless Steel Outer Casing */}
              <path d="M 308 92 L 360 92 L 360 75 L 470 75 L 470 92 L 510 92" stroke="url(#ssPipeH)" strokeWidth="6.5" fill="none" strokeLinejoin="round" />
              <path d="M 360 92 L 360 115 L 470 115 L 470 92" stroke="url(#ssPipeH)" strokeWidth="6.5" fill="none" strokeLinejoin="round" />
              {/* Inner Fluid Core */}
              <path d="M 308 92 L 360 92 L 360 75 L 470 75 L 470 92 L 510 92" stroke="#0284C7" strokeWidth="4" fill="none" strokeLinejoin="round" />
              <path d="M 360 92 L 360 115 L 470 115 L 470 92" stroke="#0284C7" strokeWidth="4" fill="none" strokeLinejoin="round" />
              <polygon points="500,88 510,92 500,96" fill="#0284C7" />
              {/* Duty Pump M1 fluid animation */}
              {isPlaying && pumps.M1.status === "RUNNING" && (
                <path d="M 312 92 L 360 92 L 360 75 L 470 75 L 470 92 L 510 92" stroke="#D7CCC8" strokeWidth="2.5" strokeDasharray="5 7" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.9 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              )}
              {/* Duty Pump M2 fluid animation (active only when M2 is running) */}
              {isPlaying && pumps.M2.status === "RUNNING" && (
                <path d="M 312 92 L 360 92 L 360 115 L 470 115 L 470 92 L 510 92" stroke="#D7CCC8" strokeWidth="2.5" strokeDasharray="5 7" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.9 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              )}
            </g>

            {/* 4. MBBR AERATION OVERFLOW TO CLARIFIER TANK (RUNS ACROSS THE TOP AT Y=65 - BIO-MIX LIQUOR) */}
            <g id="mbbr-to-clarifier-line">
              <path d="M 640 65 L 960 65" stroke="url(#ssPipeH)" strokeWidth="6.5" fill="none" />
              <path d="M 640 65 L 960 65" stroke="#8D6E63" strokeWidth="4" fill="none" />
              <polygon points="948,61 958,65 948,69" fill="#8D6E63" />
              {isPlaying && (
                <path d="M 640 65 L 960 65" stroke="#D7CCC8" strokeWidth="2.5" strokeDasharray="5 7" fill="none">
                  <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              )}
            </g>

            {/* 5. CLARIFIER THROUGH CLARIFIER VALVE STRAIGHT DOWN INTO FILTER FEED TANK (SETTLED SUPERNATANT) */}
            <g id="clarifier-to-filter-feed-line">
              <path d="M 1030 138 L 1030 252" stroke="url(#ssPipeV)" strokeWidth="6.5" fill="none" />
              <path d="M 1030 138 L 1030 252" stroke="#B8AA7B" strokeWidth="4" fill="none" />
              <polygon points="1026,242 1030,252 1034,242" fill="#B8AA7B" />
              {isPlaying && clarifierValveOpen && (
                <path d="M 1030 138 L 1030 252" stroke="#EFE8D0" strokeWidth="2.5" strokeDasharray="5 7" fill="none">
                  <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              )}
            </g>

            {/* 6. CLARIFIER SLUDGE UNDERFLOW -> M3/M4 -> SLUDGE HOLDING TANK & MBBR RECIRCULATION */}
            <g id="clarifier-to-sludge-lines">
              {/* Feeds from Clarifier bottom underflow (781, 128) moving LEFT into M3 & M4 suction */}
              <path d="M 1001 128 L 880 128 L 880 95 L 850 95" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
              <path d="M 880 128 L 850 128" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />

              {/* Suction flow arrow pointing LEFT leaving Clarifier underflow */}
              <polygon points="985,124 975,128 985,132" fill="#D97706" />

              {/* From M3/M4 discharge moving LEFT to manifold at x=600 */}
              <path d="M 810 95 L 685 95" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
              <path d="M 810 128 L 685 128" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />

              {/* 1. Primary Sludge Discharge: Downward branch into SLUDGE HOLDING TANK */}
              <path d="M 685 95 L 685 177" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
              <polygon points="681,168 685,177 689,168" fill="#D97706" />

              {/* 2. Secondary Sludge Feed from MBBR AERATION TANK into manifold */}
              <path d="M 640 95 L 685 95" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
              <polygon points="672,91 680,95 672,99" fill="#D97706" />

              {/* Active Dual-Feed Sludge Fluid Animation when M4 is RUNNING */}
              {isPlaying && pumps.M4.status === "RUNNING" && (
                <>
                  {/* Feed 1 (Major): Clarifier Underflow -> M4 -> Sludge Holding Tank */}
                  <path d="M 1001 128 L 685 128 L 685 177" stroke="#FDE68A" strokeWidth="2.2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                    <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.85 / simSpeed}s`} repeatCount="indefinite" />
                  </path>
                  {/* Feed 2 (Secondary): MBBR Aeration Tank -> Manifold -> Sludge Holding Tank */}
                  <path d="M 640 95 L 685 95 L 685 177" stroke="#FDE68A" strokeWidth="2.0" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                    <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${1.0 / simSpeed}s`} repeatCount="indefinite" />
                  </path>
                </>
              )}

              {/* Active Dual-Feed Sludge Fluid Animation when M3 is RUNNING */}
              {isPlaying && pumps.M3.status === "RUNNING" && (
                <>
                  {/* Feed 1 (Major): Clarifier Underflow -> M3 -> Sludge Holding Tank */}
                  <path d="M 1001 128 L 880 128 L 880 95 L 685 95 L 685 177" stroke="#FDE68A" strokeWidth="2.2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                    <animate attributeName="stroke-dashoffset" from="28" to="0" dur={`${0.95 / simSpeed}s`} repeatCount="indefinite" />
                  </path>
                  {/* Feed 2 (Secondary): MBBR Aeration Tank -> Manifold -> Sludge Holding Tank */}
                  <path d="M 640 95 L 670 95 L 670 177" stroke="#FDE68A" strokeWidth="2.0" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                    <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${1.0 / simSpeed}s`} repeatCount="indefinite" />
                  </path>
                </>
              )}
            </g>

            {/* 7. BLOWERS & COMPRESSED AIR PIPING NETWORK (YELLOW AIR DISTRIBUTED TO MBBR & COLLECTION TANK) */}
            <g id="yellow-air-network">
              {/* Main Blower output headers connecting BL1 (y=180) and BL2 (y=240) */}
              <path d="M 551 180 L 525 180 L 525 238 L 551 238" stroke="#D97706" strokeWidth="4" fill="none" strokeLinejoin="round" />

              {/* Branch 1: UP into MBBR Aeration Tank Diffuser Grid */}
              <path d="M 525 180 L 525 122" stroke="#D97706" strokeWidth="4" fill="none" />
              <polygon points="521,130 525,122 529,130" fill="#D97706" />

              {/* Branch 2: UP into COLLECTION TANK Diffuser Line (Zero Gap) */}
              <path d="M 525 195 L 295 195 L 295 122" stroke="#D97706" strokeWidth="4" fill="none" strokeLinejoin="round" />
              <polygon points="291,130 295,122 299,130" fill="#D97706" />

              {isPlaying && (pumps.BL1.status === "RUNNING" || pumps.BL2.status === "RUNNING") && (
                <>
                  {/* Active Blower 1 (BL1) Horizontal Discharge into Header */}
                  {pumps.BL1.status === "RUNNING" && (
                    <path d="M 551 180 L 525 180" stroke="#FDE047" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                      <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                    </path>
                  )}

                  {/* Active Blower 2 (BL2) Horizontal Discharge into Header */}
                  {pumps.BL2.status === "RUNNING" && (
                    <path d="M 551 238 L 525 238" stroke="#FDE047" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                      <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                    </path>
                  )}

                  {/* Vertical Manifold Air Distribution to MBBR Diffusers */}
                  <path d={`M 525 ${pumps.BL2.status === "RUNNING" ? 238 : 180} L 525 122`} stroke="#FDE047" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                    <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                  </path>

                  {/* Air Branch to Collection Tank Diffuser Line */}
                  <path d="M 525 195 L 295 195 L 295 122" stroke="#FDE047" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                    <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                  </path>
                </>
              )}
            </g>

            {/* 10. FILTER FEED PUMPS (M10 & M11) DOWN TO INLET PRESSURE & PSF VALVE INLET (AQUAMARINE SECONDARY EFFLUENT) */}
            <g id="filter-feed-to-psf-lines">
              <path d="M 1000 321 L 1000 350" stroke="#0D9488" strokeWidth="3.5" fill="none" />
              <path d="M 1060 321 L 1060 350" stroke="#0D9488" strokeWidth="3.5" fill="none" />
              <path d="M 1000 380 L 1000 405 L 1030 405" stroke="#0D9488" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
              <path d="M 1060 380 L 1060 405 L 1030 405" stroke="#0D9488" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
              {/* Feed line drops to y=405, runs left into top nozzle of PSF Valve at (630, 460) */}
              <path d="M 1030 405 L 630 405 L 630 460" stroke="#0D9488" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
              <polygon points="830,401 820,405 830,409" fill="#0D9488" />
              <polygon points="626,452 630,460 634,452" fill="#0D9488" />
              {/* Active Duty Pump M10 Flow Animation (Suction from Filter Feed Tank at 1000, 321 -> M10 -> Manifold -> PSF Valve) */}
              {isPlaying && pumps.M10.status === "RUNNING" && (
                <path
                  d="M 1000 321 L 1000 405 L 630 405 L 630 460"
                  stroke="#99F6E4"
                  strokeWidth="2.5"
                  strokeDasharray="5 7"
                  fill="none"
                  strokeLinejoin="round"
                >
                  <animate attributeName="stroke-dashoffset" from="28" to="0" dur={`${0.9 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              )}

              {/* Active Duty Pump M11 Flow Animation (Suction from Filter Feed Tank at 1060, 321 -> M11 -> Manifold -> PSF Valve) */}
              {isPlaying && pumps.M11.status === "RUNNING" && (
                <path
                  d="M 1060 321 L 1060 405 L 630 405 L 630 460"
                  stroke="#99F6E4"
                  strokeWidth="2.5"
                  strokeDasharray="5 7"
                  fill="none"
                  strokeLinejoin="round"
                >
                  <animate attributeName="stroke-dashoffset" from="28" to="0" dur={`${0.9 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              )}
            </g>

            {/* 11. PSF VALVE TO/FROM PSF VESSEL (100% CONNECTED COMPACT DUAL MANIFOLD) */}
            <g id="psf-valve-to-vessel">
              {/* Trunk from PSF Valve Right Nozzle (650, 480) into Manifold Tee at (665, 480) */}
              <path d="M 650 480 L 665 480" stroke="#0284C7" strokeWidth="4.5" fill="none" />

              {/* Upper Branch: Tee (665, 480) up to (665, 465) and into Top Distributor at (680, 465) */}
              <path d="M 665 480 L 665 465 L 680 465" stroke="#0284C7" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
              <polygon points="672,462 680,465 672,468" fill="#0284C7" />
              <line x1="680" y1="460" x2="680" y2="470" stroke="#0369A1" strokeWidth="2.5" />

              {/* Lower Branch: Tee (665, 480) down to (665, 495) and into Bottom Collector at (680, 495) */}
              <path d="M 665 480 L 665 495 L 680 495" stroke="#0284C7" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
              <polygon points="670,492 662,495 670,498" fill="#0284C7" />
              <line x1="680" y1="490" x2="680" y2="500" stroke="#0369A1" strokeWidth="2.5" />

              {/* Manifold Tee Junction Fitting */}
              <circle cx="665" cy="480" r="3.5" fill="#0284C7" stroke="#0369A1" strokeWidth="1" />

              {/* Animated fluid flow pulses */}
              {isPlaying && (
                <>
                  <path d="M 650 480 L 665 480 L 665 465 L 680 465" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                    <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                  </path>
                  <path d="M 680 495 L 665 495 L 665 480 L 650 480" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                    <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                  </path>
                </>
              )}
            </g>

            {/* 12. PSF VALVE OUTLET THROUGH 0.15 Bar OUTLET PRESSURE, ACROSS TO ACF VALVE INLET */}
            <g id="psf-to-acf-line">
              {/* Exits bottom of PSF valve at (630, 500), drops to y=535, runs across left to x=360, turns UP into ACF VALVE INLET at (360, 380) */}
              <path d="M 630 500 L 630 535 L 360 535 L 360 380" stroke="#0284C7" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
              <polygon points="495,531 485,535 495,539" fill="#0284C7" />
              <polygon points="356,388 360,380 364,388" fill="#0284C7" />
              {isPlaying && (
                <path d="M 630 500 L 630 535 L 360 535 L 360 380" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="5 7" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${1.2 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              )}
            </g>

            {/* 13. ACF VALVE TO/FROM ACF VESSEL (100% CONNECTED ZERO GAPS DUAL MANIFOLD) */}
            <g id="acf-valve-to-vessel">
              {/* Trunk from ACF Valve Left Nozzle (340, 360) into Manifold Tee at (305, 360) */}
              <path d="M 340 360 L 305 360" stroke="#0284C7" strokeWidth="4.5" fill="none" />

              {/* Upper Branch: Tee (305, 360) up to (305, 345) and into Top Distributor at (275, 345) */}
              <path d="M 305 360 L 305 345 L 275 345" stroke="#0284C7" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
              <polygon points="283,342 275,345 283,348" fill="#0284C7" />
              <line x1="275" y1="340" x2="275" y2="350" stroke="#0369A1" strokeWidth="2.5" />

              {/* Lower Branch: Tee (305, 360) down to (305, 375) and into Bottom Collector at (275, 375) */}
              <path d="M 305 360 L 305 375 L 275 375" stroke="#0284C7" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
              <polygon points="285,372 293,375 285,378" fill="#0284C7" />
              <line x1="275" y1="370" x2="275" y2="380" stroke="#0369A1" strokeWidth="2.5" />

              {/* Manifold Tee Junction Fitting */}
              <circle cx="305" cy="360" r="3.5" fill="#0284C7" stroke="#0369A1" strokeWidth="1" />

              {/* Animated fluid flow pulses */}
              {isPlaying && (
                <>
                  <path d="M 340 360 L 305 360 L 305 345 L 275 345" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                    <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                  </path>
                  <path d="M 275 375 L 305 375 L 305 360 L 340 360" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                    <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                  </path>
                </>
              )}
            </g>

            {/* 14. ACF VALVE OUTLET UP, LEFT ACROSS TOP OF ACF, DOWN INTO UV LIGHT */}
            <g id="acf-to-uv-line">
              {/* Exits OUTLET at top of ACF Valve (360, 340) with arrow UP ^, runs across above ACF at y=310, drops down at x=135 into UV Light at (135, 620) */}
              <path d="M 360 340 L 360 310 L 135 310 L 135 620" stroke="#0284C7" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
              <polygon points="356,330 360,320 364,330" fill="#0284C7" />
              <polygon points="230,306 220,310 230,314" fill="#0284C7" />
              <polygon points="131,540 135,550 139,540" fill="#0284C7" />
              {isPlaying && (
                <path d="M 360 340 L 360 310 L 135 310 L 135 620" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="5 7" fill="none" strokeLinejoin="round">
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

            {/* 16. TREATED WATER TANK OUT THROUGH M12, TO FLUSH, TO GARDENING & INTO SOFTENER */}
            <g id="treated-to-softener-line">
              <path d="M 460 645 L 860 645" stroke="#0284C7" strokeWidth="4.5" fill="none" />

              {/* Feeder Pipe 1: TO FLUSH */}
              <path d="M 640 645 L 640 590" stroke="#0284C7" strokeWidth="3.5" fill="none" />
              <polygon points="636,595 640,585 644,595" fill="#0284C7" />
              {renderMiniTag(640, 572, "FLUSHING", 64)}

              {/* Feeder Pipe 2: TO GARDENING */}
              <path d="M 720 645 L 720 590" stroke="#16A34A" strokeWidth="3.5" fill="none" />
              <polygon points="716,595 720,585 724,595" fill="#16A34A" />
              {renderMiniTag(720, 572, "GARDENING", 70)}

              <polygon points="845,641 855,645 845,649" fill="#0284C7" />

              {/* Animated flow when M12 is running */}
              {isPlaying && pumps.M12.status === "RUNNING" && (
                <>
                  {/* Treated Water Tank outlet through M12 into Softener inlet */}
                  <path d="M 460 645 L 860 645" stroke="#BAE6FD" strokeWidth="2" strokeDasharray="3 5" fill="none">
                    <animate attributeName="stroke-dashoffset" from="16" to="0" dur={`${0.6 / simSpeed}s`} repeatCount="indefinite" />
                  </path>
                  {/* Branch to Flush */}
                  <path d="M 640 645 L 640 590" stroke="#BAE6FD" strokeWidth="2" strokeDasharray="3 5" fill="none">
                    <animate attributeName="stroke-dashoffset" from="16" to="0" dur={`${0.6 / simSpeed}s`} repeatCount="indefinite" />
                  </path>
                  {/* Branch to Gardening */}
                  <path d="M 720 645 L 720 590" stroke="#BBF7D0" strokeWidth="2" strokeDasharray="3 5" fill="none">
                    <animate attributeName="stroke-dashoffset" from="16" to="0" dur={`${0.6 / simSpeed}s`} repeatCount="indefinite" />
                  </path>
                </>
              )}
            </g>

            {/* 17. SOFTENER OUT INTO SOFT WATER TANK (PRISTINE POLISHED CYAN WATER) */}
            <g id="softener-to-soft-water-line">
              <path d="M 940 645 L 1080 645" stroke="#06B6D4" strokeWidth="4.5" fill="none" />
              <polygon points="1070,641 1080,645 1070,649" fill="#06B6D4" />
              {isPlaying && pumps.M12.status === "RUNNING" && (
                <path d="M 940 645 L 1080 645" stroke="#A5F3FC" strokeWidth="2.5" strokeDasharray="4 6" fill="none">
                  <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.7 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              )}
            </g>

            {/* ====================================================================== */}
            {/* TANKS & VESSELS (2.5D ISOMETRIC / GLASSMORPHIC HIGH-FIDELITY MODELS)   */}
            {/* ====================================================================== */}

            {/* TANK 1: COLLECTION TANK (2.5D GLASS CYLINDER WITH RAW SEWAGE & 3D FLUID MENISCUS) */}
            <g id="tank-collection" transform="translate(135, 48)">
              {/* 2.5D Glass Cylinder Body & Dish Bottom */}
              <path
                d="M 0 76 Q 87.5 94 175 76 L 175 14 Q 87.5 30 0 14 Z"
                fill="url(#glassCylinderGrad)"
                stroke="#0284C7"
                strokeWidth="2"
              />

              {/* Raw Sewage Fluid Body (Volume below Meniscus with Dynamic Waves) */}
              {(() => {
                const rawY = Math.round(76 - (62 * collectionLevel) / 100)
                return (
                  <g clipPath="url(#collectionTankFluidClip)">
                    {/* Baseline Fluid Body Fill */}
                    <path
                      d={`M 2 ${rawY} Q 87.5 ${rawY + 12} 173 ${rawY} L 173 76 Q 87.5 93 2 76 Z`}
                      fill="url(#rawSewageGrad)"
                    />

                    {/* Wave Layer 1: Back secondary wave moving left to right (Amplitude 5.5px) */}
                    <path
                      d={`M -60 ${rawY} q 15 -5.5, 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 L 240 95 L -60 95 Z`}
                      fill="url(#rawSewageWaveBack)"
                    >
                      {isPlaying && (
                        <animateTransform
                          attributeName="transform"
                          type="translate"
                          from="-60 0"
                          to="0 0"
                          dur={`${3.2 / simSpeed}s`}
                          repeatCount="indefinite"
                        />
                      )}
                    </path>

                    {/* Wave Layer 2: Primary undulating wave moving right to left (Amplitude 6.5px) */}
                    <path
                      d={`M -88 ${rawY} q 22 -6.5, 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 L 264 95 L -88 95 Z`}
                      fill="url(#rawSewageWaveFront)"
                    >
                      {isPlaying && (
                        <animateTransform
                          attributeName="transform"
                          type="translate"
                          from="0 0"
                          to="-88 0"
                          dur={`${2.2 / simSpeed}s`}
                          repeatCount="indefinite"
                        />
                      )}
                    </path>

                    {/* 3D Liquid Meniscus (Top Surface Soft Fluid Blend - Dark Sludge) */}
                    <ellipse cx="87.5" cy={rawY} rx="85.5" ry="6.5" fill="#5D4037" opacity="0.35" />

                    {/* Dynamic Water Dropping Effect from Inlet Pipe Mouth (x=17, y=20 down to rawY) */}
                    {isPlaying && (
                      <g id="collection-tank-water-drops">
                        {/* Cascading wastewater stream */}
                        <line x1="17" y1="20" x2="17" y2={rawY} stroke="#8D6E63" strokeWidth="1.6" strokeDasharray="3 3" opacity="0.6">
                          <animate attributeName="stroke-dashoffset" from="12" to="0" dur={`${0.5 / simSpeed}s`} repeatCount="indefinite" />
                        </line>

                        {/* Droplet 1 */}
                        <ellipse cx="17" cy="22" rx="1.6" ry="2.2" fill="#8D6E63">
                          <animate
                            attributeName="cy"
                            values={`20; ${rawY}`}
                            dur={`${0.65 / simSpeed}s`}
                            repeatCount="indefinite"
                          />
                          <animate
                            attributeName="opacity"
                            values="0.9; 1; 0.2"
                            dur={`${0.65 / simSpeed}s`}
                            repeatCount="indefinite"
                          />
                        </ellipse>

                        {/* Droplet 2 (offset) */}
                        <ellipse cx="17" cy="22" rx="1.3" ry="1.9" fill="#A1887F">
                          <animate
                            attributeName="cy"
                            values={`20; ${rawY}`}
                            begin={`${0.22 / simSpeed}s`}
                            dur={`${0.65 / simSpeed}s`}
                            repeatCount="indefinite"
                          />
                          <animate
                            attributeName="opacity"
                            values="0.9; 1; 0.2"
                            begin={`${0.22 / simSpeed}s`}
                            dur={`${0.65 / simSpeed}s`}
                            repeatCount="indefinite"
                          />
                        </ellipse>

                        {/* Droplet 3 (offset) */}
                        <ellipse cx="17" cy="22" rx="1.5" ry="2.0" fill="#6D4C41">
                          <animate
                            attributeName="cy"
                            values={`20; ${rawY}`}
                            begin={`${0.44 / simSpeed}s`}
                            dur={`${0.65 / simSpeed}s`}
                            repeatCount="indefinite"
                          />
                          <animate
                            attributeName="opacity"
                            values="0.9; 1; 0.2"
                            begin={`${0.44 / simSpeed}s`}
                            dur={`${0.65 / simSpeed}s`}
                            repeatCount="indefinite"
                          />
                        </ellipse>

                        {/* Impact Splashing / Expanding Surface Ripples */}
                        <ellipse cx="17" cy={rawY} rx="2" ry="0.8" fill="none" stroke="#D7CCC8" strokeWidth="0.8">
                          <animate attributeName="rx" values="1.5; 8" dur={`${0.65 / simSpeed}s`} repeatCount="indefinite" />
                          <animate attributeName="ry" values="0.6; 2.2" dur={`${0.65 / simSpeed}s`} repeatCount="indefinite" />
                          <animate attributeName="opacity" values="0.9; 0" dur={`${0.65 / simSpeed}s`} repeatCount="indefinite" />
                        </ellipse>
                        <ellipse cx="17" cy={rawY} rx="2" ry="0.8" fill="none" stroke="#D7CCC8" strokeWidth="0.8">
                          <animate attributeName="rx" values="1.5; 8" begin={`${0.32 / simSpeed}s`} dur={`${0.65 / simSpeed}s`} repeatCount="indefinite" />
                          <animate attributeName="ry" values="0.6; 2.2" begin={`${0.32 / simSpeed}s`} dur={`${0.65 / simSpeed}s`} repeatCount="indefinite" />
                          <animate attributeName="opacity" values="0.9; 0" begin={`${0.32 / simSpeed}s`} dur={`${0.65 / simSpeed}s`} repeatCount="indefinite" />
                        </ellipse>
                      </g>
                    )}
                  </g>
                )
              })()}

              {/* Cylindrical Specular Light Glare (Left Bright Streak) */}
              <rect x="6" y="16" width="16" height="58" rx="3" fill="url(#specularSheen)" />

              {/* 3D Top Glass Vessel Flange & Rim Opening */}
              <ellipse cx="87.5" cy="14" rx="87.5" ry="8" fill="url(#glassRimGrad)" stroke="#0284C7" strokeWidth="1.5" />
              <ellipse cx="87.5" cy="14" rx="82" ry="5.5" fill="none" stroke="#CBD5E1" strokeWidth="1" strokeDasharray="3 3" opacity="0.6" />

              {/* Tank Identifier Name Tag - Centered in Tank Body */}
              {renderMiniTag(87.5, 62, "COLLECTION TANK", 125)}
            </g>

            {/* DOTTED BOUNDING BOX FOR MBBR PUMPS */}
            <rect x="340" y="50" width="90" height="92" rx="4" fill="none" stroke="#93C5FD" strokeWidth="1" strokeDasharray="3 3" />

            {/* PUMPS M1 & M2 (COLLECTION -> MBBR) */}
            {renderPump("M1", 385, 75, "right", "MBBR PUMP 1", undefined, "top")}
            {renderPump("M2", 385, 115, "right", "MBBR PUMP 2", undefined, "bottom")}

            {/* TANK 3: MBBR AERATION TANK (2.5D GLASS CYLINDER WITH K1 BIO-MEDIA & 3D FLUID MENISCUS) */}
            <g id="tank-mbbr" transform="translate(500, 48)">
              {/* 2.5D Glass Cylinder Body & Dish Bottom */}
              <path
                d="M 0 76 Q 70 94 140 76 L 140 14 Q 70 30 0 14 Z"
                fill="url(#glassCylinderGrad)"
                stroke="#0284C7"
                strokeWidth="2"
              />

              {/* Aerated Mixed Liquor Fluid Volume with Active Aeration Waves (50% Level matching Filter Feed Tank) */}
              <g clipPath="url(#mbbrTankFluidClip)">
                <path d="M 2 45 Q 70 59 138 45 L 138 76 Q 70 93 2 76 Z" fill="url(#mbbrWaterGrad)" />

                {/* MBBR Wave Layer 1: Back secondary wave moving left to right (Amplitude 5.5px) */}
                <path
                  d="M -60 45 q 15 -5.5, 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 L 210 95 L -60 95 Z"
                  fill="url(#mbbrWaveBack)"
                >
                  {isPlaying && (
                    <animateTransform
                      attributeName="transform"
                      type="translate"
                      from="-60 0"
                      to="0 0"
                      dur={`${3.2 / simSpeed}s`}
                      repeatCount="indefinite"
                    />
                  )}
                </path>

                {/* MBBR Wave Layer 2: Primary undulating wave moving right to left (Amplitude 6.5px) */}
                <path
                  d="M -88 45 q 22 -6.5, 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 L 264 95 L -88 95 Z"
                  fill="url(#mbbrWaveFront)"
                >
                  {isPlaying && (
                    <animateTransform
                      attributeName="transform"
                      type="translate"
                      from="0 0"
                      to="-88 0"
                      dur={`${2.2 / simSpeed}s`}
                      repeatCount="indefinite"
                    />
                  )}
                </path>

                {/* Soft Meniscus Blend at 50% Waterline (Bio-Mix) */}
                <ellipse cx="70" cy="45" rx="68" ry="6.5" fill="#A1887F" opacity="0.35" />
              </g>

              {/* Rising Aeration Micro-Bubbles (Bottom to 50% Water Surface) */}
              <g>
                {[
                  { cx: 24, r: 1.8, dur: 3.4, delay: 0.0, sway: 2.0 },
                  { cx: 32, r: 2.4, dur: 2.8, delay: 0.8, sway: -2.5 },
                  { cx: 42, r: 1.5, dur: 3.8, delay: 1.6, sway: 1.8 },
                  { cx: 50, r: 2.2, dur: 3.0, delay: 0.4, sway: -1.5 },
                  { cx: 60, r: 1.6, dur: 3.6, delay: 2.0, sway: 2.2 },
                  { cx: 68, r: 2.5, dur: 2.7, delay: 1.1, sway: -2.0 },
                  { cx: 78, r: 1.7, dur: 3.5, delay: 0.2, sway: 1.6 },
                  { cx: 86, r: 2.3, dur: 2.9, delay: 1.9, sway: -2.4 },
                  { cx: 96, r: 1.5, dur: 3.9, delay: 0.6, sway: 1.5 },
                  { cx: 104, r: 2.2, dur: 3.1, delay: 2.3, sway: -1.8 },
                  { cx: 114, r: 1.8, dur: 3.3, delay: 1.4, sway: 2.0 },
                  { cx: 28, r: 1.4, dur: 4.1, delay: 2.7, sway: -1.2 },
                  { cx: 56, r: 2.0, dur: 3.2, delay: 1.0, sway: 1.7 },
                  { cx: 74, r: 1.6, dur: 3.7, delay: 2.5, sway: -1.9 },
                  { cx: 92, r: 2.1, dur: 3.0, delay: 0.9, sway: 2.1 },
                  { cx: 110, r: 1.5, dur: 4.0, delay: 1.7, sway: -1.4 },
                ].map((b, i) => (
                  <circle
                    key={`aeration-bubble-${i}`}
                    cx={b.cx}
                    cy={78}
                    r={b.r}
                    fill="#FFFFFF"
                    stroke="#7DD3FC"
                    strokeWidth="0.5"
                    opacity="0.85"
                  >
                    {isPlaying && (
                      <>
                        <animate
                          attributeName="cy"
                          values="78; 67; 56; 46"
                          keyTimes="0; 0.35; 0.75; 1"
                          dur={`${b.dur / simSpeed}s`}
                          begin={`${b.delay / simSpeed}s`}
                          repeatCount="indefinite"
                        />
                        <animate
                          attributeName="cx"
                          values={`${b.cx}; ${b.cx + b.sway}; ${b.cx - b.sway}; ${b.cx}`}
                          keyTimes="0; 0.33; 0.66; 1"
                          dur={`${b.dur / simSpeed}s`}
                          begin={`${b.delay / simSpeed}s`}
                          repeatCount="indefinite"
                        />
                        <animate
                          attributeName="opacity"
                          values="0.1; 0.85; 0.9; 0"
                          keyTimes="0; 0.15; 0.85; 1"
                          dur={`${b.dur / simSpeed}s`}
                          begin={`${b.delay / simSpeed}s`}
                          repeatCount="indefinite"
                        />
                      </>
                    )}
                  </circle>
                ))}
              </g>

              {/* Cylindrical Specular Glare */}
              <rect x="5" y="16" width="14" height="58" rx="3" fill="url(#specularSheen)" />

              {/* 3D Top Glass Vessel Flange & Rim */}
              <ellipse cx="70" cy="14" rx="70" ry="7.5" fill="url(#glassRimGrad)" stroke="#0284C7" strokeWidth="1.5" />
              <ellipse cx="70" cy="14" rx="65" ry="5.0" fill="none" stroke="#93C5FD" strokeWidth="1" strokeDasharray="2 2" />

              {/* Tank Identifier Name Tag - Centered in Tank Body */}
              {renderMiniTag(70, 62, "MBBR AERATION", 110)}
            </g>

            {/* DOTTED BOUNDING BOX FOR SLUDGE RECIRCULATION PUMPS M3 & M4 */}
            <rect x="615" y="70" width="85" height="84" rx="4" fill="none" stroke="#93C5FD" strokeWidth="1" strokeDasharray="3 3" />

            {/* SLUDGE PUMPS M3 & M4 (POINTING LEFT: CLARIFIER UNDERFLOW TO SLUDGE HOLDING TANK) */}
            {renderPump("M3", 830, 95, "left", "MBBR PUMP 3", undefined, "top")}
            {renderPump("M4", 830, 128, "left", "MBBR PUMP 4", undefined, "bottom")}

            {/* TANK 4: CLARIFIER TANK WITH CONICAL HOPPER & ROTATING SCRAPER ARM (2.5D CUTAWAY) */}
            <g id="tank-clarifier" transform="translate(960, 48)">
              {/* 2.5D Conical Hopper Tank Hull (Cylindrical Upper + 60° Conical Funnel Bottom) */}
              <path
                d="M 0 14 L 0 54 L 54 88 Q 70 93 86 88 L 140 54 L 140 14 Z"
                fill="url(#glassCylinderGrad)"
                stroke="#0284C7"
                strokeWidth="2"
              />

              {/* Supernatant Clarified Water Zone (Water level matches other tanks at y=45; Sludge occupies half the balance space from y=67 to y=88) */}
              {(() => {
                const clrY = Math.round(76 - (62 * clarifierLevel) / 100)
                return (
                  <g clipPath="url(#clarifierWaterClip)">
                    {/* Baseline Supernatant Water Fill down to Sludge Interface at y=67 */}
                    <path
                      d={`M 2 ${clrY} L 2 54 L 21 67 L 119 67 L 138 54 L 138 ${clrY} Z`}
                      fill="url(#clarifierWaterGrad)"
                      opacity="0.90"
                    />

                    {/* Clarifier Wave 1: Back secondary wave moving left to right (Amplitude 5.5px) */}
                    <path
                      d={`M -60 ${clrY} q 15 -5.5, 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 L 210 68 L -60 68 Z`}
                      fill="url(#clarifierWaveBack)"
                    >
                      {isPlaying && (
                        <animateTransform
                          attributeName="transform"
                          type="translate"
                          from="-60 0"
                          to="0 0"
                          dur={`${3.2 / simSpeed}s`}
                          repeatCount="indefinite"
                        />
                      )}
                    </path>

                    {/* Clarifier Wave 2: Primary undulating wave moving right to left (Amplitude 6.5px) */}
                    <path
                      d={`M -88 ${clrY} q 22 -6.5, 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 L 264 68 L -88 68 Z`}
                      fill="url(#clarifierWaveFront)"
                    >
                      {isPlaying && (
                        <animateTransform
                          attributeName="transform"
                          type="translate"
                          from="0 0"
                          to="-88 0"
                          dur={`${2.2 / simSpeed}s`}
                          repeatCount="indefinite"
                        />
                      )}
                    </path>

                    {/* 3D Liquid Meniscus Soft Blend at Waterline (Previous Version Settling Amber Supernatant) */}
                    <ellipse cx="70" cy={clrY} rx="68" ry="6.5" fill="#D2C59D" opacity="0.35" />
                  </g>
                )
              })()}

              {/* Settled Biological Sludge Blanket in Conical Hopper Apex (Occupies half the balance space from y=67 to y=88) */}
              <path d="M 21 67 L 54 88 Q 70 93 86 88 L 119 67 Z" fill="url(#sludgeWaterGrad)" />
              {/* Sludge-Water Settling Interface Meniscus */}
              <ellipse cx="70" cy="67" rx="49" ry="4" fill="#3E2723" opacity="0.45" />

              {/* Peripheral V-Notch Overflow Weir Trough */}
              <path d="M 4 20 L 136 20" stroke="#38BDF8" strokeWidth="1.2" strokeDasharray="3 2" opacity="0.75" />

              {/* Submerged Rotating Clarifier Bridge & Scraper Rake Arm */}
              <g transform="translate(70, 58)" className="cursor-pointer" onClick={() => handleTogglePump("ARM")}>
                <circle cx="0" cy="0" r="16" fill="url(#metalRingGrad)" stroke="#16A34A" strokeWidth="1.5" />
                <circle cx="0" cy="0" r="12" fill="#DCFCE7" stroke="#16A34A" strokeWidth="1.2" />
                <g>
                  {isPlaying && pumps.ARM.status === "RUNNING" && (
                    <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur={`${2.5 / simSpeed}s`} repeatCount="indefinite" />
                  )}
                  <line x1="-12" y1="0" x2="12" y2="0" stroke="#15803D" strokeWidth="2.5" strokeLinecap="round" />
                  <line x1="0" y1="-12" x2="0" y2="12" stroke="#15803D" strokeWidth="2.5" strokeLinecap="round" />
                  {/* Rake Teeth Sweepers */}
                  <line x1="-8" y1="-3" x2="-8" y2="3" stroke="#15803D" strokeWidth="1.2" />
                  <line x1="8" y1="-3" x2="8" y2="3" stroke="#15803D" strokeWidth="1.2" />
                  <line x1="-3" y1="-8" x2="3" y2="-8" stroke="#15803D" strokeWidth="1.2" />
                  <line x1="-3" y1="8" x2="3" y2="8" stroke="#15803D" strokeWidth="1.2" />
                </g>
                <circle cx="0" cy="0" r="3.5" fill="#15803D" />
              </g>

              {/* Specular Glare */}
              <rect x="5" y="16" width="14" height="42" rx="3" fill="url(#specularSheen)" />

              {/* 3D Top Glass Vessel Flange & Rim Opening */}
              <ellipse cx="70" cy="14" rx="70" ry="7.5" fill="url(#glassRimGrad)" stroke="#0284C7" strokeWidth="1.5" />
              <ellipse cx="70" cy="14" rx="65" ry="5.0" fill="none" stroke="#93C5FD" strokeWidth="1" strokeDasharray="2 2" />

              {/* Tank Identifier Name Tag - Centered in Tank Body */}
              {renderMiniTag(70, 30, "CLARIFIER TANK", 110)}
            </g>

            {/* TANK 5: SLUDGE HOLDING TANK (2.5D CONICAL VESSEL WITH DENSE ACTIVATED SLUDGE) */}
            <g id="tank-sludge" transform="translate(680, 165)">
              {/* Conical Hopper Vessel Hull */}
              <path
                d="M 0 12 L 0 46 L 42 68 Q 57.5 73 73 68 L 115 46 L 115 12 Z"
                fill="url(#glassCylinderGrad)"
                stroke="#94A3B8"
                strokeWidth="1.5"
              />

              {/* Thickened Sludge Body (50% Waterline) */}
              <path d="M 2 39 L 2 46 L 42 68 Q 57.5 73 73 68 L 113 46 L 113 39 Z" fill="url(#sludgeWaterGrad)" />
              {/* 3D Sludge Meniscus at 50% */}
              <ellipse cx="57.5" cy="39" rx="55.5" ry="5.5" fill="#5D4037" stroke="#8D6E63" strokeWidth="0.8" opacity="0.95" />
              {/* Thickened Sludge Body with Dynamic Dual-Layer Waves */}
              {(() => {
                const sldLevel = sludgeLevel > 0 ? sludgeLevel : 50
                const sldY = Math.round(52 - (26 * sldLevel) / 100)
                return (
                  <g clipPath="url(#sludgeTankFluidClip)">
                    {/* Thickened Sludge Baseline Fill */}
                    <path d={`M 2 ${sldY} L 2 46 L 42 68 Q 57.5 73 73 68 L 113 46 L 113 ${sldY} Z`} fill="url(#sludgeWaterGrad)" />

                    {/* Sludge Wave 1: Back secondary wave moving left to right (Amplitude 4.5px) */}
                    <path
                      d={`M -50 ${sldY} q 12.5 -4.5, 25 0 t 25 0 t 25 0 t 25 0 t 25 0 t 25 0 t 25 0 L 165 75 L -50 75 Z`}
                      fill="url(#sludgeWaveBack)"
                    >
                      {isPlaying && (
                        <animateTransform
                          attributeName="transform"
                          type="translate"
                          from="-50 0"
                          to="0 0"
                          dur={`${3.4 / simSpeed}s`}
                          repeatCount="indefinite"
                        />
                      )}
                    </path>

                    {/* Sludge Wave 2: Primary undulating wave moving right to left (Amplitude 5.5px) */}
                    <path
                      d={`M -72 ${sldY} q 18 -5.5, 36 0 t 36 0 t 36 0 t 36 0 t 36 0 t 36 0 L 180 75 L -72 75 Z`}
                      fill="url(#sludgeWaveFront)"
                    >
                      {isPlaying && (
                        <animateTransform
                          attributeName="transform"
                          type="translate"
                          from="0 0"
                          to="-72 0"
                          dur={`${2.4 / simSpeed}s`}
                          repeatCount="indefinite"
                        />
                      )}
                    </path>

                    {/* 3D Sludge Meniscus */}
                    <ellipse cx="57.5" cy={sldY} rx="55.5" ry="5.5" fill="#8D6E63" opacity="0.3" />
                  </g>
                )
              })()}

              {/* Specular Highlight Glare */}
              <rect x="4" y="14" width="12" height="32" rx="2" fill="url(#specularSheen)" />

              {/* 3D Top Glass Vessel Flange & Rim */}
              <ellipse cx="57.5" cy="12" rx="57.5" ry="6.5" fill="url(#glassRimGrad)" stroke="#94A3B8" strokeWidth="1.5" />

              {/* Tank Identifier Name Tag - Centered in Tank Body */}
              {renderMiniTag(57.5, 26, "SLUDGE TANK", 80)}
            </g>

            {/* CLARIFIER VALVE (Industrial 2-Way In-Line Vertical Valve on Downcomer at x=1030) */}
            <g
              id="valve-clarifier"
              transform="translate(1030, 195)"
              className="cursor-pointer"
              onClick={() => setClarifierValveOpen(!clarifierValveOpen)}
            >
              <title>{`Clarifier Isolation Valve (V-CLR): ${clarifierValveOpen ? "OPEN (Click to Close)" : "CLOSED (Click to Open)"}`}</title>
              {renderMiniTag(54, 0, "CLARIFIER VALVE", 92)}

              {/* Vertical In-Line Pipe Connection Flanges */}
              <rect x="-7" y="-17" width="14" height="3" rx="0.8" fill="url(#metalRingGrad)" stroke="#64748B" strokeWidth="0.8" />
              <rect x="-7" y="14" width="14" height="3" rx="0.8" fill="url(#metalRingGrad)" stroke="#64748B" strokeWidth="0.8" />

              {/* ASME Twin Triangular Valve Body */}
              <polygon points="-7,-14 0,0 7,-14" fill="#334155" stroke="#0F172A" strokeWidth="1.2" />
              <polygon points="-7,14 0,0 7,14" fill="#334155" stroke="#0F172A" strokeWidth="1.2" />

              {/* Center Valve Seat & Stem Boss */}
              <circle cx="0" cy="0" r="6.5" fill={clarifierValveOpen ? "#DCFCE7" : "#FEE2E2"} stroke={clarifierValveOpen ? "#16A34A" : "#DC2626"} strokeWidth="1.3" />
              <circle cx="0" cy="0" r="2.2" fill={clarifierValveOpen ? "#16A34A" : "#DC2626"} />

              {/* Side Solenoid / Electric Actuator Head */}
              <line x1="0" y1="0" x2="-10" y2="0" stroke="#64748B" strokeWidth="2" />
              <rect x="-19" y="-6" width="9" height="12" rx="1.5" fill="#1E293B" stroke={clarifierValveOpen ? "#16A34A" : "#DC2626"} strokeWidth="1" />
              <circle cx="-14.5" cy="0" r="1.5" fill={clarifierValveOpen ? "#22C55E" : "#EF4444"} />
            </g>

            {/* TANK 6: FILTER FEED TANK (2.5D CYLINDRICAL GLASS VESSEL WITH CALIBRATED SIGHT-SCALE) */}
            <g id="tank-filter-feed" transform="translate(960, 238)">
              {/* 2.5D Glass Cylinder Body & Dish Bottom */}
              <path
                d="M 0 76 Q 70 94 140 76 L 140 14 Q 70 30 0 14 Z"
                fill="url(#glassCylinderGrad)"
                stroke="#0284C7"
                strokeWidth="2"
              />

              {/* Secondary Settled Effluent Fluid Body with Dynamic Dual-Layer Waves */}
              {(() => {
                const ffY = Math.round(76 - (62 * filterFeedLevel) / 100)
                return (
                  <g clipPath="url(#filterFeedTankFluidClip)">
                    {/* Baseline Fluid Fill */}
                    <path
                      d={`M 2 ${ffY} Q 70 ${ffY + 12} 138 ${ffY} L 138 76 Q 70 93 2 76 Z`}
                      fill="url(#filterFeedGrad)"
                    />

                    {/* Filter Feed Wave 1: Back secondary wave moving left to right (Amplitude 5.5px) */}
                    <path
                      d={`M -60 ${ffY} q 15 -5.5, 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 L 210 95 L -60 95 Z`}
                      fill="url(#filterFeedWaveBack)"
                    >
                      {isPlaying && (
                        <animateTransform
                          attributeName="transform"
                          type="translate"
                          from="-60 0"
                          to="0 0"
                          dur={`${3.2 / simSpeed}s`}
                          repeatCount="indefinite"
                        />
                      )}
                    </path>

                    {/* Filter Feed Wave 2: Primary undulating wave moving right to left (Amplitude 6.5px) */}
                    <path
                      d={`M -88 ${ffY} q 22 -6.5, 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 L 264 95 L -88 95 Z`}
                      fill="url(#filterFeedWaveFront)"
                    >
                      {isPlaying && (
                        <animateTransform
                          attributeName="transform"
                          type="translate"
                          from="0 0"
                          to="-88 0"
                          dur={`${2.2 / simSpeed}s`}
                          repeatCount="indefinite"
                        />
                      )}
                    </path>

                    {/* 3D Liquid Meniscus Blend (Translucent Pre-Filter Aquamarine) */}
                    <ellipse cx="70" cy={ffY} rx="68" ry="6.5" fill="#80CBC4" opacity="0.35" />
                  </g>
                )
              })()}

              {/* Cylindrical Glare Streak */}
              <rect x="5" y="16" width="14" height="58" rx="3" fill="url(#specularSheen)" />

              {/* 3D Top Glass Vessel Flange & Rim Opening */}
              <ellipse cx="70" cy="14" rx="70" ry="7.5" fill="url(#glassRimGrad)" stroke="#0284C7" strokeWidth="1.5" />
              <ellipse cx="70" cy="14" rx="65" ry="5.0" fill="none" stroke="#93C5FD" strokeWidth="1" strokeDasharray="2 2" />

              {/* Tank Identifier Name Tag - Centered in Tank Body */}
              {renderMiniTag(70, 62, "FILTER FEED", 100)}
            </g>

            {/* BLOWERS 1 & 2 (EXPANDED DUAL-BLOWER DECK WITH ADJACENT TELEMETRY) */}
            <g id="blower-1" transform="translate(565, 180)" className="cursor-pointer" onClick={() => handleTogglePump("BL1")}>
              {renderMiniTag(0, -22, "BLOWER 1")}
              <circle cx="0" cy="0" r="14" fill="url(#metalRingGrad)" stroke="#F43F5E" strokeWidth="1" />
              <circle cx="0" cy="0" r="11" fill="#FCE7F3" stroke="#F43F5E" strokeWidth="1.8" />
              <g>
                <path d="M -5 0 L 5 0 M 0 -5 L 0 5 M -3.5 -3.5 L 3.5 3.5 M -3.5 3.5 L 3.5 -3.5" stroke="#BE123C" strokeWidth="1.6" strokeLinecap="round" />
              </g>
            </g>

            <g id="blower-2" transform="translate(565, 238)" className="cursor-pointer" onClick={() => handleTogglePump("BL2")}>
              {renderMiniTag(0, -22, "BLOWER 2")}
              <circle cx="0" cy="0" r="14" fill="url(#metalRingGrad)" stroke="#16A34A" strokeWidth="1" />
              <circle cx="0" cy="0" r="11" fill="#DCFCE7" stroke="#16A34A" strokeWidth="1.8" />
              <g>
                {isPlaying && pumps.BL2.status === "RUNNING" && (
                  <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur={`${0.4 / simSpeed}s`} repeatCount="indefinite" />
                )}
                <path d="M -6 0 L 6 0 M 0 -6 L 0 6 M -4 -4 L 4 4 M -4 4 L 4 -4" stroke="#15803D" strokeWidth="1.8" strokeLinecap="round" />
              </g>
            </g>

            {/* FILTER FEED PUMPS: M10 & M11 */}
            {renderPump("M10", 1000, 365, "down", "FF PUMP 1", undefined, "top")}
            {renderPump("M11", 1060, 365, "down", "FF PUMP 2", undefined, "top")}

            {/* ====================================================================== */}
            {/* BOTTOM SECTION: PSF, ACF, UV, DOSING, TREATED & SOFT WATER             */}
            {/* ====================================================================== */}

            {/* GREY DASHED BORDER AROUND ACF AREA */}
            <rect x="110" y="295" width="285" height="150" rx="6" fill="none" stroke="#CBD5E1" strokeWidth="1.5" strokeDasharray="4 4" />

            {/* PSF VALVE MULTIPORT BLOCK (Industrial 4-Port Multiport Valve) */}
            <g id="psf-valve-block" transform="translate(600, 450)">
              {renderMiniTag(-15, -14, "PSF MPV")}
              {renderMultiportValve("PSF", psfValveMode, () => {
                const nextModes: Record<MultiportValveMode, MultiportValveMode> = {
                  SERVICE: "BACKWASH",
                  BACKWASH: "RINSE",
                  RINSE: "DRAIN",
                  DRAIN: "SERVICE",
                }
                setPsfValveMode(prev => nextModes[prev] ?? "SERVICE")
              })}
            </g>

            {/* PSF VESSEL (680, 425) - Dynamic 4-Option Filter Vessel */}
            <g transform="translate(680, 425)">
              {renderFilterVessel("PSF", filterVesselOption)}
            </g>

            {/* ACF VALVE MULTIPORT BLOCK (Industrial 4-Port Multiport Valve) */}
            <g id="acf-valve-block" transform="translate(330, 330)">
              {renderMiniTag(72, -4, "ACF MPV")}
              {renderMultiportValve("ACF", acfValveMode, () => {
                const nextModes: Record<MultiportValveMode, MultiportValveMode> = {
                  SERVICE: "BACKWASH",
                  BACKWASH: "RINSE",
                  RINSE: "DRAIN",
                  DRAIN: "SERVICE",
                }
                setAcfValveMode(prev => nextModes[prev] ?? "SERVICE")
              })}
            </g>

            {/* ACF VESSEL (195, 305) - Dynamic 4-Option Filter Vessel */}
            <g transform="translate(195, 305)">
              {renderFilterVessel("ACF", filterVesselOption)}
            </g>

            {/* DOSING PUMP (Precision Solenoid Diaphragm Metering Pump) */}
            <g id="dosing-pump" transform="translate(225, 595)">
              {renderMiniTag(20, -12, "DOSING PUMP")}
              {/* Base Mounting Foot Bracket */}
              <rect x="22" y="34" width="18" height="4" rx="1" fill="#334155" stroke="#0F172A" strokeWidth="0.8" />
              <circle cx="25" cy="36" r="0.9" fill="#94A3B8" />
              <circle cx="37" cy="36" r="0.9" fill="#94A3B8" />

              {/* Heavy-Duty Chemical-Resistant Solenoid Drive Enclosure */}
              <rect x="22" y="14" width="18" height="20" rx="3" fill="#1E293B" stroke="#64748B" strokeWidth="1" />

              {/* Rear Motor Heat Dissipation Fins */}
              <line x1="33" y1="17" x2="33" y2="31" stroke="#334155" strokeWidth="1.2" />
              <line x1="36" y1="17" x2="36" y2="31" stroke="#334155" strokeWidth="1.2" />

              {/* Electronic Stroke Control Dial / Knob */}
              <circle cx="27" cy="24" r="3.2" fill="#0F172A" stroke="#94A3B8" strokeWidth="0.8" />
              <circle cx="27" cy="24" r="1.4" fill="#16A34A" />

              {/* Top Discharge Valve Union Nut & Chemical Injection Line */}
              <rect x="12" y="5" width="6" height="8" rx="1" fill="#475569" stroke="#94A3B8" strokeWidth="0.8" />
              <rect x="11" y="9" width="8" height="4" rx="0.5" fill="#334155" stroke="#64748B" strokeWidth="0.8" />
              <polygon points="15,4 12,8 18,8" fill="#16A34A" />

              {/* Bottom Suction Valve Union Nut & Chemical Feed Line Downward Injection */}
              <rect x="12" y="35" width="6" height="8" rx="1" fill="#475569" stroke="#94A3B8" strokeWidth="0.8" />
              <rect x="11" y="35" width="8" height="4" rx="0.5" fill="#334155" stroke="#64748B" strokeWidth="0.8" />
              <line x1="15" y1="43" x2="15" y2="50" stroke="#16A34A" strokeWidth="2" />
              <polygon points="12,50 15,55 18,50" fill="#16A34A" />

              {/* Manual Degassing / Priming Relief Valve Knob */}
              <rect x="6" y="9" width="4" height="4" rx="1" fill="#D97706" stroke="#B45309" strokeWidth="0.6" />

              {/* PVDF Transparent Chemical Liquid-End Dosing Head Block */}
              <rect x="8" y="13" width="14" height="22" rx="2.5" fill="url(#metalRingGrad)" stroke="#0284C7" strokeWidth="1.2" />

              {/* Optical Diaphragm Stroke Sight Chamber */}
              <circle cx="15" cy="24" r="7" fill="#064E3B" stroke="#22C55E" strokeWidth="1.2" />

              {/* Reciprocating Diaphragm Stroke Core */}
              <circle cx="15" cy="24" r="4.2" fill="#16A34A" stroke="#FFFFFF" strokeWidth="0.6">
                {isPlaying && (
                  <>
                    <animate attributeName="r" values="3.2; 5.2; 3.2" dur={`${0.75 / simSpeed}s`} repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0.7; 1; 0.7" dur={`${0.75 / simSpeed}s`} repeatCount="indefinite" />
                  </>
                )}
              </circle>

              {/* Specular Sheen Glare Arc */}
              <path d="M 10 21 A 5.5 5.5 0 0 1 20 21" stroke="#FFFFFF" strokeWidth="1" fill="none" opacity="0.6" strokeLinecap="round" />
            </g>

            {/* UV LIGHT */}
            <g id="uv-light" transform="translate(105, 620)">
              {renderMiniTag(32.5, 48, "UV DISINFECTION")}
              <rect x="0" y="0" width="65" height="38" rx="6" fill="#FAF5FF" stroke="#9333EA" strokeWidth="1.5" />
              {/* Animated UV Radiation Rays */}
              {isPlaying && (
                <rect x="4" y="4" width="57" height="30" rx="4" fill="#C084FC" opacity="0.15">
                  <animate attributeName="opacity" values="0.1;0.35;0.1" dur={`${1.2 / simSpeed}s`} repeatCount="indefinite" />
                </rect>
              )}
              <line x1="8" y1="9" x2="57" y2="9" stroke="#A855F7" strokeWidth="3" strokeLinecap="round" />
              <line x1="8" y1="19" x2="57" y2="19" stroke="#16A34A" strokeWidth="3" strokeLinecap="round" />
              <line x1="8" y1="29" x2="57" y2="29" stroke="#A855F7" strokeWidth="3" strokeLinecap="round" />
            </g>

            {/* TANK 7: TREATED WATER TANK (2.5D PURE WATER CYLINDER WITH 3D CRYSTAL MENISCUS) */}
            <g id="tank-treated" transform="translate(320, 603)">
              {/* 2.5D Glass Cylinder Body & Dish Bottom */}
              <path
                d="M 0 74 Q 70 90 140 74 L 140 14 Q 70 28 0 14 Z"
                fill="url(#glassCylinderGrad)"
                stroke="#0284C7"
                strokeWidth="2"
              />

              {/* Treated Pure Water Volume Body with Crystal Dynamic Dual-Layer Waves */}
              {(() => {
                const trY = Math.round(74 - (52 * treatedLevel) / 100)
                return (
                  <g clipPath="url(#treatedWaterTankFluidClip)">
                    {/* Baseline Fluid Fill */}
                    <path
                      d={`M 2 ${trY} Q 70 ${trY + 11} 138 ${trY} L 138 74 Q 70 89 2 74 Z`}
                      fill="url(#treatedWaterGrad)"
                    />

                    {/* Treated Water Wave 1: Back secondary wave moving left to right (Amplitude 5.5px) */}
                    <path
                      d={`M -60 ${trY} q 15 -5.5, 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 L 210 95 L -60 95 Z`}
                      fill="url(#treatedWaveBack)"
                    >
                      {isPlaying && (
                        <animateTransform
                          attributeName="transform"
                          type="translate"
                          from="-60 0"
                          to="0 0"
                          dur={`${3.2 / simSpeed}s`}
                          repeatCount="indefinite"
                        />
                      )}
                    </path>

                    {/* Treated Water Wave 2: Primary undulating wave moving right to left (Amplitude 6.5px) */}
                    <path
                      d={`M -88 ${trY} q 22 -6.5, 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 L 264 95 L -88 95 Z`}
                      fill="url(#treatedWaveFront)"
                    >
                      {isPlaying && (
                        <animateTransform
                          attributeName="transform"
                          type="translate"
                          from="0 0"
                          to="-88 0"
                          dur={`${2.2 / simSpeed}s`}
                          repeatCount="indefinite"
                        />
                      )}
                    </path>

                    {/* 3D Liquid Meniscus Soft Blend */}
                    <ellipse cx="70" cy={trY} rx="68" ry="6.0" fill="#E0F2FE" opacity="0.3" />
                  </g>
                )
              })()}

              {/* Cylindrical Glare Streak */}
              <rect x="5" y="16" width="14" height="54" rx="3" fill="url(#specularSheen)" />

              {/* 3D Top Glass Vessel Flange & Rim */}
              <ellipse cx="70" cy="14" rx="70" ry="7.0" fill="url(#glassRimGrad)" stroke="#0284C7" strokeWidth="1.5" />

              {/* Tank Identifier Name Tag - Centered in Tank Body */}
              {renderMiniTag(70, 62, "TREATED WATER", 100)}
            </g>

            {/* M12: FLUSHING PUMP */}
            {renderPump("M12", 515, 645, "right", "FLUSHING PUMP", undefined, "bottom")}

            {/* WATER SOLENOID VALVE (Industrial 2-Way In-Line Horizontal Solenoid Valve) */}
            <g
              id="valve-water-solenoid"
              transform="translate(615, 645)"
              className="cursor-pointer"
              onClick={() => setWaterSolenoidOpen(!waterSolenoidOpen)}
            >
              <title>{`Treated Water Solenoid Valve (V-SOL): ${waterSolenoidOpen ? "OPEN (Click to Close)" : "CLOSED (Click to Open)"}`}</title>
              {renderMiniTag(0, 24, "SOLENOID VALVE")}

              {/* Horizontal In-Line Pipe Connection Flanges */}
              <rect x="-17" y="-7" width="3" height="14" rx="0.8" fill="url(#metalRingGrad)" stroke="#64748B" strokeWidth="0.8" />
              <rect x="14" y="-7" width="3" height="14" rx="0.8" fill="url(#metalRingGrad)" stroke="#64748B" strokeWidth="0.8" />

              {/* ASME Twin Triangular Valve Body */}
              <polygon points="-14,-7 0,0 -14,7" fill="#334155" stroke="#0F172A" strokeWidth="1.2" />
              <polygon points="14,-7 0,0 14,7" fill="#334155" stroke="#0F172A" strokeWidth="1.2" />

              {/* Center Valve Seat & Stem Boss */}
              <circle cx="0" cy="0" r="6.5" fill={waterSolenoidOpen ? "#DCFCE7" : "#FEE2E2"} stroke={waterSolenoidOpen ? "#16A34A" : "#DC2626"} strokeWidth="1.3" />
              <circle cx="0" cy="0" r="2.2" fill={waterSolenoidOpen ? "#16A34A" : "#DC2626"} />

              {/* Top Solenoid Electrical Actuator Coil Head */}
              <line x1="0" y1="0" x2="0" y2="-10" stroke="#64748B" strokeWidth="2" />
              <rect x="-6" y="-19" width="12" height="9" rx="1.5" fill="#1E293B" stroke={waterSolenoidOpen ? "#16A34A" : "#DC2626"} strokeWidth="1" />
              <circle cx="0" cy="-14.5" r="1.5" fill={waterSolenoidOpen ? "#22C55E" : "#EF4444"} />
            </g>

            {/* SOFTENER VESSEL (675, 595) - Dynamic 4-Option Filter Vessel */}
            <g id="vessel-softener" transform="translate(860, 595)">
              {renderFilterVessel("SOFTENER", filterVesselOption)}
            </g>

            {/* TANK 8: SOFT WATER TANK (840, 603) - 2.5D PRISTINE POLISHED WATER CYLINDER */}
            <g id="tank-soft-water" transform="translate(1080, 603)">
              {/* 2.5D Glass Cylinder Body & Dish Bottom */}
              <path
                d="M 0 74 Q 70 90 140 74 L 140 14 Q 70 28 0 14 Z"
                fill="url(#glassCylinderGrad)"
                stroke="#0284C7"
                strokeWidth="2"
              />

              {/* Polished Soft Water Volume Body with Pristine Dynamic Dual-Layer Waves */}
              {(() => {
                const swY = Math.round(74 - (52 * softWaterLevel) / 100)
                return (
                  <g clipPath="url(#softWaterTankFluidClip)">
                    {/* Baseline Fluid Fill */}
                    <path
                      d={`M 2 ${swY} Q 70 ${swY + 11} 138 ${swY} L 138 74 Q 70 89 2 74 Z`}
                      fill="url(#softWaterGrad)"
                    />

                    {/* Soft Water Wave 1: Back secondary wave moving left to right (Amplitude 5.5px) */}
                    <path
                      d={`M -60 ${swY} q 15 -5.5, 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 L 210 95 L -60 95 Z`}
                      fill="url(#softWaterWaveBack)"
                    >
                      {isPlaying && (
                        <animateTransform
                          attributeName="transform"
                          type="translate"
                          from="-60 0"
                          to="0 0"
                          dur={`${3.2 / simSpeed}s`}
                          repeatCount="indefinite"
                        />
                      )}
                    </path>

                    {/* Soft Water Wave 2: Primary undulating wave moving right to left (Amplitude 6.5px) */}
                    <path
                      d={`M -88 ${swY} q 22 -6.5, 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 L 264 95 L -88 95 Z`}
                      fill="url(#softWaterWaveFront)"
                    >
                      {isPlaying && (
                        <animateTransform
                          attributeName="transform"
                          type="translate"
                          from="0 0"
                          to="-88 0"
                          dur={`${2.2 / simSpeed}s`}
                          repeatCount="indefinite"
                        />
                      )}
                    </path>

                    {/* 3D Liquid Meniscus Soft Blend */}
                    <ellipse cx="70" cy={swY} rx="68" ry="6.0" fill="#F0F9FF" opacity="0.35" />
                  </g>
                )
              })()}

              {/* Cylindrical Glare Streak */}
              <rect x="5" y="16" width="14" height="54" rx="3" fill="url(#specularSheen)" />

              {/* 3D Top Glass Vessel Flange & Rim */}
              <ellipse cx="70" cy="14" rx="70" ry="7.0" fill="url(#glassRimGrad)" stroke="#0284C7" strokeWidth="1.5" />

              {/* Tank Identifier Name Tag - Centered in Tank Body */}
              {renderMiniTag(70, 62, "SOFT WATER", 90)}
            </g>

            {/* ====================================================================== */}
            {/* TELEMETRY OVERLAY LAYER (ALL BADGES POSITIONED DIRECTLY ON ELEMENT TOP)*/}
            {/* ====================================================================== */}
            {showTelemetryBadges && (
              <g id="telemetry-details-overlay">
                {/* 1. Collection Tank (Top Center, y=6..38 - Clean 10px air gap above rim at y=48) */}
                {renderTelemetryCard(178, 12, "TK-01", [
                  { label: "Level", value: `${collectionLevel}`, unit: "%" },
                  { label: "Volume", value: (collectionLevel * 0.5).toFixed(1), unit: "m³" },
                ], "NORMAL")}

                {/* 2. Feed Pumps M1 & M2 (M1 above loop at y=10, M2 below loop at y=150 - Zero Pipe/Tag Overlap) */}
                {renderTelemetryCard(402, 10, "M1", [
                  { label: "Flow", value: pumps.M1.flowRate.toFixed(1), unit: "m³/h" },
                  { label: "Power", value: pumps.M1.powerKw.toFixed(1), unit: "kW" },
                ], pumps.M1.status)}
                {renderTelemetryCard(402, 150, "M2", [
                  { label: "Flow", value: pumps.M2.flowRate.toFixed(1), unit: "m³/h" },
                  { label: "Power", value: pumps.M2.powerKw.toFixed(1), unit: "kW" },
                ], pumps.M2.status)}

                {/* 3. MBBR Aeration Tank (Top Center, y=6..38 - Clean 10px air gap above rim at y=48) */}
                {renderTelemetryCard(526, 12, "MBBR", [
                  { label: "Level", value: `${mbbrLevel}`, unit: "%" },
                  { label: "DO", value: do1.toFixed(2), unit: "mg/L" },
                ], "NORMAL")}

                {/* 4. Aeration Blowers BL1 & BL2 (BL1 at y=130 between MBBR base & Blower 1; BL2 at y=276 below Blower 2) */}
                {renderTelemetryCard(587, 168, "BL1", [
                  { label: "Flow", value: `${pumps.BL1.flowRate.toFixed(0)}`, unit: "m³/h" },
                  { label: "Power", value: pumps.BL1.powerKw.toFixed(1), unit: "kW" },
                ], pumps.BL1.status, 78)}
                {renderTelemetryCard(587, 226, "BL2", [
                  { label: "Flow", value: `${pumps.BL2.flowRate.toFixed(0)}`, unit: "m³/h" },
                  { label: "Power", value: pumps.BL2.powerKw.toFixed(1), unit: "kW" },
                ], pumps.BL2.status, 78)}

                {/* 5. Sludge Recirculation Pumps M3 & M4 (M3 above at y=14, M4 under pump 4 at y=166) */}
                {renderTelemetryCard(788, 14, "M3", [
                  { label: "Flow", value: pumps.M3.flowRate.toFixed(1), unit: "m³/h" },
                  { label: "Power", value: pumps.M3.powerKw.toFixed(1), unit: "kW" },
                ], pumps.M3.status, 84)}
                {renderTelemetryCard(795, 166, "M4", [
                  { label: "Flow", value: pumps.M4.flowRate.toFixed(1), unit: "m³/h" },
                  { label: "Power", value: pumps.M4.powerKw.toFixed(1), unit: "kW" },
                ], pumps.M4.status, 84)}

                {/* 6. Sludge Holding Tank (Cleanly placed directly below conical bottom & tag at y=268) */}
                {renderTelemetryCard(693, 268, "SLUDGE", [
                  { label: "Level", value: `${sludgeLevel}`, unit: "%" },
                  { label: "Volume", value: (sludgeLevel * 0.25).toFixed(1), unit: "m³" },
                ], "NORMAL")}

                {/* 7. Clarifier Tank (Top Center, y=6..38 - Clean 10px air gap above rim at y=48) */}
                {renderTelemetryCard(986, 12, "CLR-01", [
                  { label: "Level", value: `${clarifierLevel}`, unit: "%" },
                  { label: "Turbidity", value: "1.8", unit: "NTU" },
                ], "NORMAL")}

                {/* 8. Filter Feed Tank (Positioned on clear right flank at x=1115, y=246 - Zero Downcomer Pipe Overlap) */}
                {renderTelemetryCard(1105, 238, "FF-TK", [
                  { label: "Level", value: `${filterFeedLevel}`, unit: "%" },
                  { label: "Volume", value: (filterFeedLevel * 0.36).toFixed(1), unit: "m³" },
                ], "NORMAL", 80)}

                {/* 9. Filter Feed Pumps M10 & M11 (Directly under respective pumps at y=418) */}
                {renderTelemetryCard(945, 418, "M10", [
                  { label: "Flow", value: pumps.M10.flowRate.toFixed(1), unit: "m³/h" },
                  { label: "Power", value: pumps.M10.powerKw.toFixed(1), unit: "kW" },
                ], pumps.M10.status, 78)}
                {renderTelemetryCard(1037, 418, "M11", [
                  { label: "Flow", value: pumps.M11.flowRate.toFixed(1), unit: "m³/h" },
                  { label: "Power", value: pumps.M11.powerKw.toFixed(1), unit: "kW" },
                ], pumps.M11.status, 78)}

                {/* 10. Media Filter Vessels PSF & ACF (PSF on right flank at x=775, y=442; ACF below stand at x=194, y=465) */}
                {renderTelemetryCard(775, 442, "PSF", [
                  { label: "ΔP", value: (inletPressure - outletPressure).toFixed(2), unit: "Bar" },
                  { label: "Timer", value: formatTime(psfSeconds), unit: "" },
                ], "NORMAL", 84)}
                {renderTelemetryCard(194, 465, "ACF", [
                  { label: "ΔP", value: (inletPressure - outletPressure * 0.9).toFixed(2), unit: "Bar" },
                  { label: "Timer", value: formatTime(acfSeconds), unit: "" },
                ], "NORMAL", 84)}

                {/* 10b. PSF & ACF Multiport Valves (Clean clearance from risers & horizontal lines) */}
                {renderTelemetryCard(535, 496, "PSF-MPV", [
                  { label: "Mode", value: psfValveMode, unit: "" },
                  { label: "Status", value: psfValveMode === "SERVICE" ? "SEATED" : "CYCLING", unit: "" },
                ], psfValveMode === "SERVICE" ? "NORMAL" : "STANDBY", 84)}
                {renderTelemetryCard(385, 345, "ACF-MPV", [
                  { label: "Mode", value: acfValveMode, unit: "" },
                  { label: "Status", value: acfValveMode === "SERVICE" ? "SEATED" : "CYCLING", unit: "" },
                ], acfValveMode === "SERVICE" ? "NORMAL" : "STANDBY", 84)}

                {/* 11. Treated Water Tank (Top Center, y=558..590 - Clean 13px gap above rim at y=603) */}
                {renderTelemetryCard(346, 562, "TREATED", [
                  { label: "Level", value: `${treatedLevel}`, unit: "%" },
                  { label: "pH", value: "7.40", unit: "" },
                ], "NORMAL")}

                {/* 12. Flushing Pump M12 (Centered directly beneath M12 at x=471, y=680 - 13px clear of pump tag) */}
                {renderTelemetryCard(471, 680, "M12", [
                  { label: "Flow", value: pumps.M12.flowRate.toFixed(1), unit: "m³/h" },
                  { label: "Power", value: pumps.M12.powerKw.toFixed(1), unit: "kW" },
                ], pumps.M12.status)}

                {/* 13. Soft Water Tank (Top Center, y=558..590 - Clean 13px gap above rim at y=603) */}
                {renderTelemetryCard(1106, 562, "SOFT-TK", [
                  { label: "Level", value: `${softWaterLevel}`, unit: "%" },
                  { label: "Volume", value: (softWaterLevel * 0.44).toFixed(1), unit: "m³" },
                ], "NORMAL")}

                {/* 14. Softener Vessel (Centered directly above vessel at x=857, y=546 - 17px gap above dome at y=595) */}
                {renderTelemetryCard(857, 546, "SOFTENER", [
                  { label: "Hardness", value: softwaterHardness.toFixed(2), unit: "mg/L" },
                  { label: "Flow", value: "12.0", unit: "m³/h" },
                ], "NORMAL", 88)}</g>
            )}
          </g>
        </svg>
      </div>

      {/* 2.5 Water Purification Progression Indicator (Fixed 40px single-line row on mobile) */}
      <div className="shrink-0 px-2.5 sm:px-4 h-10 max-h-10 [@media(max-height:500px)]:hidden bg-gradient-to-r from-stone-100 via-sky-50 to-cyan-50 border-t border-sky-100 flex items-center justify-between gap-2 text-[10px] sm:text-[11px] font-mono overflow-x-auto">
        <div className="shrink-0 flex items-center gap-1.5 font-bold text-slate-700 whitespace-nowrap">
          <span className="w-2 h-2 rounded-full bg-sky-500 animate-pulse" />
          <span>PURIFICATION PROGRESSION:</span>
        </div>
        <div className="flex items-center gap-1.5 sm:gap-2 shrink-0 text-[9px] sm:text-[10px] whitespace-nowrap">
          <span className="flex items-center gap-1 px-1.5 sm:px-2 py-0.5 rounded bg-stone-200 text-stone-800 border border-stone-300 font-semibold">
            <span className="w-2 h-2 sm:w-2.5 sm:h-2.5 rounded-full bg-[#8D6E63] border border-stone-400" />
            1. Raw Sewage
          </span>
          <span className="text-slate-400 font-bold">→</span>
          <span className="flex items-center gap-1 px-1.5 sm:px-2 py-0.5 rounded bg-amber-50 text-amber-900 border border-amber-200 font-semibold">
            <span className="w-2 h-2 sm:w-2.5 sm:h-2.5 rounded-full bg-[#6B7852] border border-amber-400" />
            2. Biological MLSS
          </span>
          <span className="text-slate-400 font-bold">→</span>
          <span className="flex items-center gap-1 px-1.5 sm:px-2 py-0.5 rounded bg-sky-100 text-sky-900 border border-sky-200 font-semibold">
            <span className="w-2 h-2 sm:w-2.5 sm:h-2.5 rounded-full bg-[#7DD3FC] border border-sky-400" />
            3. Clarified Effluent
          </span>
          <span className="text-slate-400 font-bold">→</span>
          <span className="flex items-center gap-1 px-1.5 sm:px-2 py-0.5 rounded bg-cyan-100 text-cyan-900 border border-cyan-200 font-semibold">
            <span className="w-2 h-2 sm:w-2.5 sm:h-2.5 rounded-full bg-[#38BDF8] border border-cyan-400" />
            4. Media Filtered
          </span>
          <span className="text-slate-400 font-bold">→</span>
          <span className="flex items-center gap-1 px-1.5 sm:px-2 py-0.5 rounded bg-emerald-50 text-emerald-900 border border-emerald-200 font-bold">
            <span className="w-2 h-2 sm:w-2.5 sm:h-2.5 rounded-full bg-[#0284C7] border border-emerald-400" />
            5. Pure Soft Water
          </span>
        </div>
      </div>

      {/* 3. SCADA Bottom Telemetry Bar */}
      <div className="shrink-0 px-2 sm:px-4 py-1 [@media(max-height:500px)]:py-0.5 bg-sky-50/50 border-t border-sky-100 grid grid-cols-2 sm:grid-cols-3 [@media(max-height:500px)]:grid-cols-6 lg:grid-cols-6 gap-1 sm:gap-1.5 text-xs">
        <div className="p-1 sm:p-1.5 [@media(max-height:500px)]:p-0.5 rounded-md sm:rounded-lg bg-white border border-sky-100 shadow-xs flex flex-col justify-center">
          <span className="text-[10px] sm:text-[11px] [@media(max-height:500px)]:text-[8px] text-slate-500 uppercase font-mono font-semibold truncate">Aeration DO1</span>
          <span className="text-sm sm:text-base [@media(max-height:500px)]:text-[10px] font-bold text-sky-700 font-mono truncate">{do1.toFixed(2)} mg/L</span>
          <span className="text-[9px] sm:text-[10px] [@media(max-height:500px)]:hidden text-emerald-600 font-medium truncate">Normal (0.5–2.0)</span>
        </div>

        <div className="p-1 sm:p-1.5 [@media(max-height:500px)]:p-0.5 rounded-md sm:rounded-lg bg-white border border-sky-100 shadow-xs flex flex-col justify-center">
          <span className="text-[10px] sm:text-[11px] [@media(max-height:500px)]:text-[8px] text-slate-500 uppercase font-mono font-semibold truncate">Clarifier TSS</span>
          <span className="text-sm sm:text-base [@media(max-height:500px)]:text-[10px] font-bold text-purple-700 font-mono truncate">{clarifierTss.toFixed(2)} mg/L</span>
          <span className="text-[9px] sm:text-[10px] [@media(max-height:500px)]:hidden text-slate-500 truncate">Underflow OK</span>
        </div>

        <div className="p-1 sm:p-1.5 [@media(max-height:500px)]:p-0.5 rounded-md sm:rounded-lg bg-white border border-sky-100 shadow-xs flex flex-col justify-center">
          <span className="text-[10px] sm:text-[11px] [@media(max-height:500px)]:text-[8px] text-slate-500 uppercase font-mono font-semibold truncate">PSF Differential</span>
          <span className="text-sm sm:text-base [@media(max-height:500px)]:text-[10px] font-bold text-emerald-700 font-mono truncate">
            {(inletPressure - outletPressure).toFixed(2)} Bar
          </span>
          <span className="text-[9px] sm:text-[10px] [@media(max-height:500px)]:hidden text-slate-500 truncate">In: {inletPressure} · Out: {outletPressure}</span>
        </div>

        <div className="p-1 sm:p-1.5 [@media(max-height:500px)]:p-0.5 rounded-md sm:rounded-lg bg-white border border-sky-100 shadow-xs flex flex-col justify-center">
          <span className="text-[10px] sm:text-[11px] [@media(max-height:500px)]:text-[8px] text-slate-500 uppercase font-mono font-semibold truncate">PSF Service</span>
          <span className="text-sm sm:text-base [@media(max-height:500px)]:text-[10px] font-bold text-emerald-700 font-mono truncate">{formatTime(psfSeconds)}</span>
          <span className="text-[9px] sm:text-[10px] [@media(max-height:500px)]:hidden text-slate-500 truncate">Backwash in 20h</span>
        </div>

        <div className="p-1 sm:p-1.5 [@media(max-height:500px)]:p-0.5 rounded-md sm:rounded-lg bg-white border border-sky-100 shadow-xs flex flex-col justify-center">
          <span className="text-[10px] sm:text-[11px] [@media(max-height:500px)]:text-[8px] text-slate-500 uppercase font-mono font-semibold truncate">ACF Service</span>
          <span className="text-sm sm:text-base [@media(max-height:500px)]:text-[10px] font-bold text-emerald-700 font-mono truncate">{formatTime(acfSeconds)}</span>
          <span className="text-[9px] sm:text-[10px] [@media(max-height:500px)]:hidden text-slate-500 truncate">Adsorption active</span>
        </div>

        <div className="p-1 sm:p-1.5 [@media(max-height:500px)]:p-0.5 rounded-md sm:rounded-lg bg-white border border-sky-100 shadow-xs flex flex-col justify-center">
          <span className="text-[10px] sm:text-[11px] [@media(max-height:500px)]:text-[8px] text-slate-500 uppercase font-mono font-semibold truncate">Softener Hardness</span>
          <span className="text-sm sm:text-base [@media(max-height:500px)]:text-[10px] font-bold text-emerald-700 font-mono truncate">{softwaterHardness.toFixed(2)} mg/L</span>
          <span className="text-[9px] sm:text-[10px] [@media(max-height:500px)]:hidden text-emerald-600 font-medium truncate">Zero Hardness</span>
        </div>
      </div>

      {/* 4. Asset Inspector Bar */}
      <div className="shrink-0 px-2 sm:px-4 py-0.5 sm:py-1 [@media(max-height:500px)]:py-0.5 bg-slate-50 border-t border-sky-100 flex flex-wrap items-center justify-between text-xs text-slate-600 gap-1 sm:gap-2">
        <div className="flex items-center gap-3 sm:gap-4 flex-wrap text-[10px] sm:text-[11px] [@media(max-height:500px)]:text-[8.5px] font-mono">
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 [@media(max-height:500px)]:w-2 [@media(max-height:500px)]:h-2 rounded-full bg-emerald-500 inline-block" />
            <span className="text-slate-700 font-semibold">RUNNING</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 [@media(max-height:500px)]:w-2 [@media(max-height:500px)]:h-2 rounded-full bg-rose-500 inline-block" />
            <span className="text-slate-700 font-semibold">STANDBY / STOPPED</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-1 [@media(max-height:500px)]:w-2.5 bg-sky-500 inline-block" />
            <span className="text-slate-700">Process Water</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-1 [@media(max-height:500px)]:w-2.5 bg-amber-500 inline-block" />
            <span className="text-slate-700">Compressed Air</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-1 [@media(max-height:500px)]:w-2.5 bg-rose-500 inline-block" />
            <span className="text-slate-700">Drain / Backwash</span>
          </span>
        </div>
      </div>
    </div>
  )
}
