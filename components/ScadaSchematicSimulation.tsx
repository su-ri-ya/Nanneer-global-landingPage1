"use client"

import React, { useState, useEffect } from "react"
import {
  Play,
  Pause,
  RotateCcw,
  Sliders,
  Info,
  Activity,
  Droplets,
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

export type MultiportValveMode = "SERVICE" | "BRINE" | "BACKWASH" | "RINSE" | "REFILL"

export function ScadaSchematicSimulation() {
  const [isPlaying, setIsPlaying] = useState<boolean>(true)
  const [simSpeed, setSimSpeed] = useState<number>(1)
  const [controlMode, setControlMode] = useState<"AUTO" | "MANUAL">("AUTO")
  const [selectedAsset, setSelectedAsset] = useState<string | null>(null)
  const [showTelemetryBadges, setShowTelemetryBadges] = useState<boolean>(true)
  const [telemetryMode, setTelemetryMode] = useState<"EMBEDDED" | "BADGES">("EMBEDDED")
  const [filterVesselOption, setFilterVesselOption] = useState<1 | 2 | 3 | 4>(3)

  // Live sensor readings with micro-jitter
  const [do1, setDo1] = useState<number>(0.88)
  const [clarifierTss, setClarifierTss] = useState<number>(0.0)
  const [inletPressure, setInletPressure] = useState<number>(0.35)
  const [outletPressure, setOutletPressure] = useState<number>(0.15)
  const [softwaterHardness, setSoftwaterHardness] = useState<number>(0.0)

  // Tank levels (Uniform 50% Water Level matching Filter Feed Tank)
  const [collectionLevel, setCollectionLevel] = useState<number>(50)
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
    M1: { id: "M1", name: "MBBR RSTP 1", code: "M1", status: "RUNNING", powerKw: 4.0, flowRate: 18.5 },
    M2: { id: "M2", name: "MBBR RSTP 2", code: "M2", status: "STOPPED", powerKw: 4.0, flowRate: 0 },
    M3: { id: "M3", name: "MBBR RCP 1", code: "M3", status: "STOPPED", powerKw: 1.5, flowRate: 0 },
    M4: { id: "M4", name: "MBBR RCP 2", code: "M4", status: "RUNNING", powerKw: 1.5, flowRate: 6.8 },
    M10: { id: "M10", name: "FF PUMP 1", code: "M10", status: "STOPPED", powerKw: 3.0, flowRate: 0 },
    M11: { id: "M11", name: "FF PUMP 2", code: "M11", status: "STOPPED", powerKw: 3.0, flowRate: 0 },
    M12: { id: "M12", name: "FLUSHING PUMP", code: "M12", status: "STOPPED", powerKw: 5.5, flowRate: 0 },
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

    // Strictly Green (Running) & Red (Stopped)
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

        {/* 5. Glowing Status LED Indicator */}
        <circle cx="9" cy="-9" r="2.8" fill={color} stroke="#FFFFFF" strokeWidth="0.8">
          {isPlaying && isRunning && (
            <animate attributeName="opacity" values="0.7;1;0.7" dur="1s" repeatCount="indefinite" />
          )}
        </circle>

        {/* 7. Flow Direction Arrow */}
        {arrow}
      </g>
    )
  }

  // Mini Equipment Identifier Tag (Hidden per user request: "remove the all name for now m2,m1,........")
  const renderMiniTag = (_x: number, _y: number, _label: string) => {
    return null
  }

  // 4 Design Options for PSF, ACF & Softener Filter Vessels
  const renderFilterVessel = (type: "PSF" | "ACF" | "SOFTENER", option: 1 | 2 | 3 | 4) => {
    return (
      <g id={`vessel-${type.toLowerCase()}-internals`}>
        {/* Mini Tag at top of vessel */}
        {renderMiniTag(41, 10, type)}

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
              <circle cx="0" cy="0" r="7.5" fill="#FFFFFF" stroke="#0284C7" strokeWidth="1.2" />
              <circle cx="0" cy="0" r="6" fill="#F0F9FF" />
              <line x1="0" y1="0" x2="3.5" y2="-3" stroke="#DC2626" strokeWidth="1" />
              <circle cx="0" cy="0" r="1.2" fill="#0F172A" />
              <text x="0" y="12" textAnchor="middle" fill="#0369A1" fontSize="5" fontWeight="bold" fontFamily="monospace">
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
      </g>
    )
  }

  // Industrial UKL 5-Port Multiport Valve (MPV) Component
  const renderMultiportValve = (
    name: string,
    mode: MultiportValveMode,
    onToggle: () => void
  ) => {
    // Mode to angle mapping for 5 operational cycles:
    // 1. SERVICE: 0 deg (Top / 12 o'clock - Port 1 Inlet to Port 2 Outlet)
    // 2. BRINE: 45 deg (Diagonal 45° - Port 5 Brine Eductor Draw)
    // 3. REFILL: 115 deg (Lower Right - Port 5 Brine Tank Fresh Refill)
    // 4. BACKWASH: 180 deg (Bottom / 6 o'clock - Reverse Flow to Port 4 Drain)
    // 5. RINSE: -50 deg (Upper Left / 10 o'clock - Downward Fast Rinse to Port 4 Drain)
    const angleMap: Record<MultiportValveMode, number> = {
      SERVICE: 0,
      BRINE: 45,
      REFILL: 115,
      BACKWASH: 180,
      RINSE: -50,
    }
    const nextModeMap: Record<MultiportValveMode, MultiportValveMode> = {
      SERVICE: "BRINE",
      BRINE: "BACKWASH",
      BACKWASH: "RINSE",
      RINSE: "REFILL",
      REFILL: "SERVICE",
    }
    const angle = angleMap[mode] ?? 0
    const nextMode = nextModeMap[mode] ?? "SERVICE"

    return (
      <g
        className="cursor-pointer group transition-transform duration-200 hover:scale-[1.03]"
        onClick={onToggle}
      >
        <title>{`${name} 5-Port Multiport Valve: Mode ${mode} (Click to switch to ${nextMode})`}</title>

        {/* 5 Threaded Pipe Union Nozzles (Option A Configuration) */}

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

        {/* Port 2: Bottom Nozzle (6 o'clock - Treated/Softened Water Outlet) */}
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

        {/* Port 3: Left Nozzle (9 o'clock - Top Vessel Distributor) */}
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

        {/* Port 4: Right Nozzle (3 o'clock - Drain / Backwash Return) */}
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

        {/* Port 5: Diagonal Nozzle (45° Upper-Right - Brine / Auxiliary Eductor Port) */}
        <g id={`${name}-p5-diagonal`} transform="rotate(45 30 30)">
          <rect x="24" y="1" width="12" height="9" rx="1" fill="#18181B" stroke="#09090B" strokeWidth="0.8" />
          <line x1="25" y1="3" x2="35" y2="3" stroke="#F59E0B" strokeWidth="0.8" />
          <line x1="25" y1="5.5" x2="35" y2="5.5" stroke="#F59E0B" strokeWidth="0.8" />
          <line x1="25" y1="8" x2="35" y2="8" stroke="#F59E0B" strokeWidth="0.8" />
          {/* Heavy Union Nut with Amber Accent */}
          <rect x="21.5" y="8" width="17" height="4.5" rx="1.2" fill="#27272A" stroke="#B45309" strokeWidth="0.8" />
          <line x1="25" y1="8" x2="25" y2="12.5" stroke="#D97706" strokeWidth="0.6" />
          <line x1="30" y1="8" x2="30" y2="12.5" stroke="#D97706" strokeWidth="0.6" />
          <line x1="35" y1="8" x2="35" y2="12.5" stroke="#D97706" strokeWidth="0.6" />
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

            {/* Mode: BRINE / REFILL - Fluid draw through 45° Port 5 */}
            {(mode === "BRINE" || mode === "REFILL") && (
              <path d="M 43 17 L 34 26" stroke="#FDE68A" strokeWidth="2" strokeLinecap="round" strokeDasharray="3 3">
                <animate attributeName="stroke-dashoffset" from="12" to="0" dur={`${0.7 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}

            {/* Mode: BACKWASH / RINSE - Flush discharge stream to Port 4 Drain */}
            {(mode === "BACKWASH" || mode === "RINSE") && (
              <path d="M 30 30 L 50 30" stroke="#FCA5A5" strokeWidth="2" strokeLinecap="round" strokeDasharray="3 3">
                <animate attributeName="stroke-dashoffset" from="12" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>
        )}

        {/* 5 Dial Cycle Step Markings */}
        {/* 1. Top (0°): SERVICE */}
        <g transform="rotate(0 30 30)">
          <polygon points="30,16.5 28,18.8 32,18.8" fill="#FACC15" />
          <text x="30" y="21.5" fill="#FEF08A" fontSize="2.4" fontWeight="900" textAnchor="middle" fontFamily="sans-serif">SERVICE</text>
        </g>

        {/* 2. Upper-Right (45°): BRINE REGEN */}
        <g transform="rotate(45 30 30)">
          <polygon points="30,16.5 28,18.8 32,18.8" fill="#F59E0B" />
          <text x="30" y="21.5" fill="#FEF08A" fontSize="2.2" fontWeight="900" textAnchor="middle" fontFamily="sans-serif">BRINE</text>
        </g>

        {/* 3. Lower-Right (115°): REFILL */}
        <g transform="rotate(115 30 30)">
          <polygon points="30,16.5 28,18.8 32,18.8" fill="#FACC15" />
          <text x="30" y="21.5" fill="#FEF08A" fontSize="2.0" fontWeight="900" textAnchor="middle" fontFamily="sans-serif">REFILL</text>
        </g>

        {/* 4. Bottom (180°): BACKWASH */}
        <g transform="rotate(180 30 30)">
          <polygon points="30,16.5 28,18.8 32,18.8" fill="#FACC15" />
          <text x="30" y="21.5" fill="#FEF08A" fontSize="2.1" fontWeight="900" textAnchor="middle" fontFamily="sans-serif">BACKWASH</text>
        </g>

        {/* 5. Upper-Left (-50°): RINSE */}
        <g transform="rotate(-50 30 30)">
          <polygon points="30,16.5 28,18.8 32,18.8" fill="#FACC15" />
          <text x="30" y="21.5" fill="#FEF08A" fontSize="2.2" fontWeight="900" textAnchor="middle" fontFamily="sans-serif">RINSE</text>
        </g>

        {/* Miniature UKL Brand Badge (Lower-Left 225°) */}
        <g transform="translate(17, 32)">
          <rect x="0" y="0" width="4.8" height="3.5" rx="0.5" fill="#FFFFFF" stroke="#16A34A" strokeWidth="0.3" />
          <text x="2.4" y="2.2" fill="#15803D" fontSize="1.6" fontWeight="900" textAnchor="middle" fontFamily="sans-serif">UKL</text>
          <circle cx="2.4" cy="2.8" r="0.35" fill="#0284C7" />
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
    )
  }
  const renderTelemetryBadge = (
    x: number,
    y: number,
    _tag: string,
    paramLabel: string,
    paramValue: string | number,
    unit: string,
    status: "RUNNING" | "STANDBY" | "STOPPED" | "NORMAL" = "NORMAL",
    width: number = 68,
    height: number = 16
  ) => {
    const isOk = status === "RUNNING" || status === "NORMAL"
    const isStandby = status === "STANDBY"
    const borderColor = isOk ? "#86EFAC" : isStandby ? "#FDE68A" : "#FECACA"

    return (
      <g transform={`translate(${x}, ${y})`} className="pointer-events-none select-none">
        {/* Compact pill container with crisp frosted white background */}
        <rect
          x="0"
          y="0"
          width={width}
          height={height}
          rx="3.5"
          fill="#FFFFFF"
          fillOpacity="0.96"
          stroke={borderColor}
          strokeWidth="1"
        />

        {/* Parameter Label & Value */}
        <text x="6" y="10.5" fill="#475569" fontSize="6" fontFamily="monospace" fontWeight="500">
          {paramLabel}:
        </text>
        <text x={width - 5} y="10.5" textAnchor="end" fill="#0F172A" fontSize="6.5" fontWeight="bold" fontFamily="monospace">
          {paramValue}{unit ? <tspan fill="#64748B" fontSize="5.5"> {unit}</tspan> : ""}
        </text>
      </g>
    )
  }

  // Option 1: Embedded In-Element Readouts (ISA-101 High Performance SCADA)
  const renderEmbeddedTankPill = (
    cx: number,
    cy: number,
    tag: string,
    lvlText: string,
    qualityText?: string,
    borderCol = "#38BDF8"
  ) => (
    <g transform={`translate(${cx}, ${cy})`} className="pointer-events-none select-none">
      <rect
        x="-62"
        y="-8.5"
        width="124"
        height="17"
        rx="8.5"
        fill="#0F172A"
        fillOpacity="0.82"
        stroke={borderCol}
        strokeWidth="0.9"
      />
      <circle cx="-52" cy="0" r="2.2" fill={borderCol} />
      <text x="-45" y="3" fill="#F8FAFC" fontSize="6.5" fontFamily="monospace" fontWeight="bold">
        {tag}
      </text>
      <text x="-14" y="3" fill="#38BDF8" fontSize="6.5" fontFamily="monospace" fontWeight="bold">
        {lvlText}
      </text>
      {qualityText && (
        <text x="54" y="3" textAnchor="end" fill="#94A3B8" fontSize="5.5" fontFamily="monospace">
          {qualityText}
        </text>
      )}
    </g>
  )

  const renderEmbeddedPumpFlow = (
    cx: number,
    cy: number,
    _code: string,
    flowRate: number,
    status: PumpStatus
  ) => {
    const isRunning = status === "RUNNING"
    const strokeColor = isRunning ? "#22C55E" : "#EF4444"
    return (
      <g transform={`translate(${cx}, ${cy})`} className="pointer-events-none select-none">
        <rect
          x="-24"
          y="-7"
          width="48"
          height="14"
          rx="4"
          fill="#0F172A"
          fillOpacity="0.88"
          stroke={strokeColor}
          strokeWidth="0.8"
        />
        <circle cx="-17" cy="0" r="2" fill={strokeColor} />
        <text x="-11" y="3" fill="#F8FAFC" fontSize="5.8" fontFamily="monospace" fontWeight="bold">
          {flowRate.toFixed(1)}
          <tspan fill="#94A3B8" fontSize="4.6"> m³/h</tspan>
        </text>
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
                System Tag: STP-NANNEER-PLANT-01 · MBBR Aeration &amp; Tertiary Media Polishing
              </span>
            </div>
          </div>
        </div>

        {/* Live Controls */}
        <div className="flex items-center gap-2 flex-wrap">
          <button
            onClick={() => setControlMode((prev) => (prev === "AUTO" ? "MANUAL" : "AUTO"))}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-mono font-bold border transition-colors ${controlMode === "AUTO"
              ? "bg-sky-100 text-sky-800 border-sky-300"
              : "bg-amber-100 text-amber-800 border-amber-300"
              }`}
          >
            <Sliders className="w-3.5 h-3.5" />
            <span>MODE: {controlMode}</span>
          </button>

          {/* Telemetry Display Style Selector */}
          <div className="flex items-center gap-1 bg-sky-100/80 p-0.5 rounded-md border border-sky-200 shadow-xs">
            <span className="text-[10px] font-bold text-sky-900 font-mono px-1.5 hidden sm:inline">TELEMETRY:</span>
            <button
              onClick={() => {
                setShowTelemetryBadges(true)
                setTelemetryMode("EMBEDDED")
              }}
              className={`px-2 py-0.5 text-[10px] font-mono rounded font-bold transition-all ${
                showTelemetryBadges && telemetryMode === "EMBEDDED"
                  ? "bg-sky-600 text-white shadow-xs"
                  : "text-slate-600 hover:text-sky-900 hover:bg-white/70"
              }`}
              title="Option 1: Embedded in-element readouts (Zero pipe collisions)"
            >
              1. Embedded
            </button>
            <button
              onClick={() => {
                setShowTelemetryBadges(true)
                setTelemetryMode("BADGES")
              }}
              className={`px-2 py-0.5 text-[10px] font-mono rounded font-bold transition-all ${
                showTelemetryBadges && telemetryMode === "BADGES"
                  ? "bg-sky-600 text-white shadow-xs"
                  : "text-slate-600 hover:text-sky-900 hover:bg-white/70"
              }`}
              title="Option 2: Safe Floating Badges Grid (Optimized coordinates)"
            >
              2. Floating Badges
            </button>
          </div>

          <div className="flex items-center bg-white rounded-md p-0.5 border border-sky-200 shadow-xs">
            {[1, 2, 5].map((speed) => (
              <button
                key={speed}
                onClick={() => setSimSpeed(speed)}
                className={`px-2 py-0.5 text-[10px] font-mono rounded ${simSpeed === speed ? "bg-sky-600 text-white font-bold" : "text-slate-600 hover:text-slate-900"
                  }`}
              >
                {speed}x
              </button>
            ))}
          </div>

          {/* Interactive PSF / ACF Design Option Selector */}
          {/* Interactive Filter Vessels Design Option Selector (PSF, ACF, Softener) */}
          <div className="flex items-center gap-1 bg-sky-100/80 p-0.5 rounded-md border border-sky-200 shadow-xs">
            <span className="text-[10px] font-bold text-sky-900 font-mono px-1.5 hidden sm:inline">PSF/ACF:</span>
            <span className="text-[10px] font-bold text-sky-900 font-mono px-1.5 hidden sm:inline">FILTERS:</span>
            {[
              { id: 1, label: "1. Modern FRP" },
              { id: 2, label: "2. Animated Flow" },
              { id: 3, label: "3. SCADA P&ID" },
              { id: 4, label: "4. Full Cutaway" },
            ].map((opt) => (
              <button
                key={opt.id}
                onClick={() => setFilterVesselOption(opt.id as 1 | 2 | 3 | 4)}
                className={`px-2 py-0.5 text-[10px] font-mono rounded font-bold transition-all ${filterVesselOption === opt.id
                  ? "bg-sky-600 text-white shadow-xs"
                  : "text-slate-600 hover:text-sky-900 hover:bg-white/70"
                  }`}
              >
                {opt.label}
              </button>
            ))}
          </div>

          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className={`p-1.5 rounded-md border text-xs font-medium transition-colors ${isPlaying
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

      {/* Water Quality & Treatment Progression Ribbon */}
      <div className="px-4 py-1.5 bg-gradient-to-r from-stone-100 via-amber-50/70 to-cyan-50/70 border-b border-sky-100 flex items-center justify-between gap-2 overflow-x-auto text-[11px] font-mono">
        <span className="font-bold text-slate-700 whitespace-nowrap flex items-center gap-1.5">
          <Droplets className="w-3.5 h-3.5 text-sky-600" />
          WATER CLARITY PROGRESSION:
        </span>
        <div className="flex items-center gap-2 flex-nowrap">
          <span className="flex items-center gap-1 px-2 py-0.5 rounded bg-[#5D4037]/10 border border-[#5D4037]/30 text-[#4E342E] font-semibold" title="Raw untreated sewage (turbid, high TSS)">
            <span className="w-2.5 h-2.5 rounded-full bg-[#5D4037]" />
            1. Raw Sewage (15%)
          </span>
          <span className="text-slate-400">→</span>
          <span className="flex items-center gap-1 px-2 py-0.5 rounded bg-[#8D7B68]/15 border border-[#8D7B68]/40 text-[#5D4037] font-semibold" title="MBBR biological digestion mixed liquor (faded sewage broth)">
            <span className="w-2.5 h-2.5 rounded-full bg-[#8D7B68]" />
            2. Aeration Bio-Mix (35%)
          </span>
          <span className="text-slate-400">→</span>
          <span className="flex items-center gap-1 px-2 py-0.5 rounded bg-[#B8AA7B]/25 border border-[#B8AA7B]/60 text-[#786940] font-semibold" title="Clarifier solid-liquid settling supernatant (slightly bad/turbid)">
            <span className="w-2.5 h-2.5 rounded-full bg-[#D2C59D] border border-[#8C7C4E]" />
            3. Clarifier Settling (55%)
          </span>
          <span className="text-slate-400">→</span>
          <span className="flex items-center gap-1 px-2 py-0.5 rounded bg-[#80CBC4]/20 border border-[#80CBC4]/50 text-[#00695C] font-semibold" title="Pre-filtered secondary effluent">
            <span className="w-2.5 h-2.5 rounded-full bg-[#80CBC4]" />
            4. Pre-Filter (75%)
          </span>
          <span className="text-slate-400">→</span>
          <span className="flex items-center gap-1 px-2 py-0.5 rounded bg-sky-100 border border-sky-300 text-sky-800 font-semibold" title="Filtered & disinfected clean treated water">
            <span className="w-2.5 h-2.5 rounded-full bg-[#38BDF8]" />
            5. Treated Clean (95%)
          </span>
          <span className="text-slate-400">→</span>
          <span className="flex items-center gap-1 px-2 py-0.5 rounded bg-cyan-100 border border-cyan-300 text-cyan-900 font-semibold" title="Polished zero-hardness soft water">
            <span className="w-2.5 h-2.5 rounded-full bg-[#00E5FF] shadow-xs" />
            6. Pristine Soft (99.9%)
          </span>
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

            {/* Collection Tank Wave Gradients & Fluid Mask */}
            <linearGradient id="rawSewageWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#D7CCC8" stopOpacity="0.88" />
              <stop offset="40%" stopColor="#8D6E63" stopOpacity="0.88" />
              <stop offset="100%" stopColor="#5D4037" stopOpacity="0.96" />
            </linearGradient>
            <linearGradient id="rawSewageWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#A1887F" stopOpacity="0.65" />
              <stop offset="100%" stopColor="#4E342E" stopOpacity="0.90" />
            </linearGradient>
            <clipPath id="collectionTankFluidClip">
              <path d="M 2 16 Q 87.5 24 173 16 L 173 76 Q 87.5 93 2 76 Z" />
            </clipPath>

            {/* 2. MBBR Aeration Tank (Aerated Mixed Liquor - Faded Raw Sewage Brown Broth) */}
            <linearGradient id="mbbrWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#C4B5A5" stopOpacity="0.85" />
              <stop offset="45%" stopColor="#A1887F" stopOpacity="0.88" />
              <stop offset="100%" stopColor="#6D554D" stopOpacity="0.92" />
            </linearGradient>
            <linearGradient id="mbbrWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#EFEBE9" stopOpacity="0.88" />
              <stop offset="40%" stopColor="#BCAAA4" stopOpacity="0.85" />
              <stop offset="100%" stopColor="#8D7B68" stopOpacity="0.92" />
            </linearGradient>
            <linearGradient id="mbbrWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#BCAAA4" stopOpacity="0.65" />
              <stop offset="100%" stopColor="#6D554D" stopOpacity="0.88" />
            </linearGradient>
            <clipPath id="mbbrTankFluidClip">
              <path d="M 2 16 Q 70 24 138 16 L 138 76 Q 70 93 2 76 Z" />
            </clipPath>

            {/* 4. Clarifier Tank with Arm (Phase Separation: Slightly Bad/Murky Amber Supernatant on top, Settling Sludge at bottom) */}
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
              <path d="M 2 16 Q 70 24 138 16 L 138 54 L 2 54 Z" />
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
            {/* Common Drain Manifold connecting ACF Valve (390, 480) and PSF Valve (870, 480) directly into Central Riser (545, 480) */}
            {/* From ACF Valve DRAIN port at (390, 480) going right to central tee */}
            <path d="M 390 480 L 545 480" stroke="#DC2626" strokeWidth="4.5" fill="none" />
            <polygon points="465,476 475,480 465,484" fill="#DC2626" />

            {/* From PSF Valve DRAIN port at (870, 480) going left to central tee (100% connected, zero gaps) */}
            <path d="M 870 480 L 545 480" stroke="#DC2626" strokeWidth="4.5" fill="none" />
            <polygon points="625,476 615,480 625,484" fill="#DC2626" />

            {/* Central vertical red riser from y=480 up to y=390 */}
            <path d="M 545 480 L 545 390" stroke="#DC2626" strokeWidth="4.5" fill="none" />
            <polygon points="541,435 545,425 549,435" fill="#DC2626" />

            {/* Header running across above ACF to far left margin and cleanly into Collection Tank left side (y=68) */}
            <path d="M 545 390 L 75 390 L 75 68 L 135 68" stroke="#DC2626" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
            <polygon points="260,386 250,390 260,394" fill="#DC2626" />
            <polygon points="71,210 75,200 79,210" fill="#DC2626" />
            <polygon points="127,64 135,68 127,72" fill="#DC2626" />

            {/* Animated backwash/rinse flow */}
            {isPlaying && (
              <>
                {/* Active Backwash/Rinse Flow from ACF Multiport Valve */}
                {(acfValveMode === "BACKWASH" || acfValveMode === "RINSE") && (
                  <path
                    d="M 390 480 L 545 480 L 545 390 L 75 390 L 75 68 L 135 68"
                    stroke="#FCA5A5"
                    strokeWidth="2.5"
                    strokeDasharray="6 8"
                    fill="none"
                    strokeLinejoin="round"
                  >
                    <animate attributeName="stroke-dashoffset" from="56" to="0" dur={`${1.4 / simSpeed}s`} repeatCount="indefinite" />
                  </path>
                )}

                {/* Active Backwash/Rinse Flow from PSF Multiport Valve */}
                {(psfValveMode === "BACKWASH" || psfValveMode === "RINSE") && (
                  <path
                    d="M 870 480 L 545 480 L 545 390 L 75 390 L 75 68 L 135 68"
                    stroke="#FCA5A5"
                    strokeWidth="2.5"
                    strokeDasharray="6 8"
                    fill="none"
                    strokeLinejoin="round"
                  >
                    <animate attributeName="stroke-dashoffset" from="56" to="0" dur={`${1.4 / simSpeed}s`} repeatCount="indefinite" />
                  </path>
                )}

                {/* Subtle Standby Connectivity Flow when neither valve is actively backwashing */}
                {acfValveMode !== "BACKWASH" && acfValveMode !== "RINSE" && psfValveMode !== "BACKWASH" && psfValveMode !== "RINSE" && (
                  <path
                    d="M 390 480 L 545 480 L 545 390 L 75 390 L 75 68 L 135 68"
                    stroke="#FCA5A5"
                    strokeWidth="1.8"
                    strokeDasharray="4 10"
                    opacity="0.4"
                    fill="none"
                    strokeLinejoin="round"
                  >
                    <animate attributeName="stroke-dashoffset" from="56" to="0" dur={`${2.2 / simSpeed}s`} repeatCount="indefinite" />
                  </path>
                )}
              </>
            )}
          </g>

          {/* 3. COLLECTION TANK TO MBBR AERATION TANK (VIA M1 / M2) */}
          <g id="collection-to-mbbr-lines">
            {/* Wall Flange Nozzle on Collection Tank */}
            <rect x="307" y="88" width="6" height="8" rx="1.5" fill="#64748B" stroke="#0284C7" strokeWidth="1" />
            {/* Stainless Steel Outer Casing */}
            <path d="M 308 92 L 340 92 L 340 75 L 420 75 L 420 92 L 440 92" stroke="url(#ssPipeH)" strokeWidth="6.5" fill="none" strokeLinejoin="round" />
            <path d="M 340 92 L 340 115 L 420 115 L 420 92" stroke="url(#ssPipeH)" strokeWidth="6.5" fill="none" strokeLinejoin="round" />
            {/* Inner Fluid Core */}
            <path d="M 308 92 L 340 92 L 340 75 L 420 75 L 420 92 L 440 92" stroke="#0284C7" strokeWidth="4" fill="none" strokeLinejoin="round" />
            <path d="M 340 92 L 340 115 L 420 115 L 420 92" stroke="#0284C7" strokeWidth="4" fill="none" strokeLinejoin="round" />
            <polygon points="430,88 440,92 430,96" fill="#0284C7" />
            {isPlaying && pumps.M1.status === "RUNNING" && (
              <path d="M 312 92 L 340 92 L 340 75 L 420 75 L 420 92 L 440 92" stroke="#D7CCC8" strokeWidth="2.5" strokeDasharray="5 7" fill="none" strokeLinejoin="round">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.9 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 4. MBBR AERATION OVERFLOW TO CLARIFIER TANK (RUNS ACROSS THE TOP AT Y=65 - FADED BIO-SLUDGE LIQUOR) */}
          <g id="mbbr-to-clarifier-line">
            <path d="M 570 65 L 740 65" stroke="url(#ssPipeH)" strokeWidth="6.5" fill="none" />
            <path d="M 570 65 L 740 65" stroke="#8D7B68" strokeWidth="4" fill="none" />
            <polygon points="728,61 738,65 728,69" fill="#8D7B68" />
            {isPlaying && (
              <path d="M 570 65 L 740 65" stroke="#E0D7D3" strokeWidth="2.5" strokeDasharray="5 7" fill="none">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 5. CLARIFIER THROUGH CLARIFIER VALVE STRAIGHT DOWN INTO FILTER FEED TANK (SETTLED SUPERNATANT) */}
          <g id="clarifier-to-filter-feed-line">
            <path d="M 810 138 L 810 252" stroke="url(#ssPipeV)" strokeWidth="6.5" fill="none" />
            <path d="M 810 138 L 810 252" stroke="#B8AA7B" strokeWidth="4" fill="none" />
            <polygon points="806,242 810,252 814,242" fill="#B8AA7B" />
            {isPlaying && clarifierValveOpen && (
              <path d="M 810 138 L 810 252" stroke="#EFE8D0" strokeWidth="2.5" strokeDasharray="5 7" fill="none">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 6. CLARIFIER SLUDGE UNDERFLOW -> M3/M4 -> MBBR AERATION TANK & SLUDGE HOLDING TANK */}
          <g id="clarifier-to-sludge-lines">
            {/* Feeds from Clarifier bottom/left into M3 & M4 suction */}
            <path d="M 781 128 L 705 128 L 705 95 L 675 95" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
            <path d="M 705 128 L 675 128" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />

            {/* From M3/M4 discharge to manifold at x=600 */}
            <path d="M 635 95 L 600 95" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
            <path d="M 635 128 L 600 128" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />

            {/* 1. Downward branch into SLUDGE HOLDING TANK */}
            <path d="M 600 95 L 600 177" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
            <polygon points="596,168 600,177 604,168" fill="#D97706" />

            {/* 2. Recirculation branch into MBBR AERATION TANK (x=570, y=95) */}
            <path d="M 600 95 L 570 95" stroke="#D97706" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
            <polygon points="578,91 570,95 578,99" fill="#D97706" />


            {isPlaying && pumps.M4.status === "RUNNING" && (
              <>
                <path d="M 781 128 L 705 128 L 600 128 L 600 177" stroke="#FDE68A" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${1.0 / simSpeed}s`} repeatCount="indefinite" />
                </path>
                <path d="M 600 128 L 600 95 L 570 95" stroke="#FDE68A" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              </>
            )}

            {isPlaying && pumps.M3.status === "RUNNING" && (
              <>
                <path d="M 781 128 L 705 128 L 705 95 L 570 95" stroke="#FDE68A" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.9 / simSpeed}s`} repeatCount="indefinite" />
                </path>
                <path d="M 600 95 L 600 177" stroke="#FDE68A" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${1.0 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              </>
            )}
          </g>

          {/* 7. BLOWERS & COMPRESSED AIR PIPING NETWORK (YELLOW AIR DISTRIBUTED TO MBBR & COLLECTION TANK) */}
          <g id="yellow-air-network">
            {/* Main Blower output headers connecting BL1 (y=180) and BL2 (y=240) */}
            <path d="M 495 180 L 460 180 L 460 240 L 495 240" stroke="#D97706" strokeWidth="4" fill="none" strokeLinejoin="round" />

            {/* Branch 1: UP into MBBR Aeration Tank Diffuser Grid */}
            <path d="M 460 180 L 460 122" stroke="#D97706" strokeWidth="4" fill="none" />
            <polygon points="456,130 460,122 464,130" fill="#D97706" />

            {/* Branch 2: UP into COLLECTION TANK Diffuser Line (Zero Gap) */}
            <path d="M 460 195 L 295 195 L 295 122" stroke="#D97706" strokeWidth="4" fill="none" strokeLinejoin="round" />
            <polygon points="291,130 295,122 299,130" fill="#D97706" />

            {isPlaying && (pumps.BL1.status === "RUNNING" || pumps.BL2.status === "RUNNING") && (
              <>
                {/* Air to MBBR */}
                <path d="M 460 240 L 460 122" stroke="#FDE047" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                </path>
                {/* Air to Collection Tank */}
                <path d="M 460 195 L 295 195 L 295 122" stroke="#FDE047" strokeWidth="2" strokeDasharray="4 6" fill="none" strokeLinejoin="round">
                  <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              </>
            )}
          </g>

          {/* 10. FILTER FEED PUMPS (M10 & M11) DOWN TO INLET PRESSURE & PSF VALVE INLET (AQUAMARINE SECONDARY EFFLUENT) */}
          <g id="filter-feed-to-psf-lines">
            <path d="M 780 321 L 780 350" stroke="#0D9488" strokeWidth="3.5" fill="none" />
            <path d="M 840 321 L 840 350" stroke="#0D9488" strokeWidth="3.5" fill="none" />
            <path d="M 780 380 L 780 405 L 810 405" stroke="#0D9488" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
            <path d="M 840 380 L 840 405 L 810 405" stroke="#0D9488" strokeWidth="3.5" fill="none" strokeLinejoin="round" />
            {/* Feed line drops to y=420, passes horizontally right through 0.35 Bar, enters INLET at top of PSF Valve at (900, 450) */}
            <path d="M 810 405 L 810 420 L 900 420 L 900 450" stroke="#0D9488" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
            <polygon points="896,442 900,450 904,442" fill="#0D9488" />
            {isPlaying && (pumps.M10.status === "RUNNING" || pumps.M11.status === "RUNNING") && (
              <path
                d="M 810 405 L 810 420 L 900 420 L 900 450"
                stroke="#99F6E4"
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

            {/* VOUT: From left edge of PSF vessel (970, 495) into right edge of valve (930, 495) */}
            <path d="M 970 495 L 930 495" stroke="#0284C7" strokeWidth="4" fill="none" />
            <polygon points="938,492 930,495 938,498" fill="#0284C7" />
          </g>

          {/* 12. PSF VALVE OUTLET THROUGH 0.15 Bar OUTLET PRESSURE, ACROSS TO ACF VALVE INLET */}
          <g id="psf-to-acf-line">
            {/* Exits bottom of PSF valve at (900, 510), drops to y=535, runs across left to x=360, turns UP into ACF VALVE INLET at (360, 510) */}
            <path d="M 900 510 L 900 535 L 360 535 L 360 510" stroke="#0284C7" strokeWidth="4.5" fill="none" strokeLinejoin="round" />
            <polygon points="760,531 750,535 760,539" fill="#0284C7" />
            <polygon points="560,531 550,535 560,539" fill="#0284C7" />
            <polygon points="356,518 360,510 364,518" fill="#0284C7" />
            {isPlaying && (
              <path d="M 900 510 L 900 535 L 360 535 L 360 510" stroke="#BAE6FD" strokeWidth="2.5" strokeDasharray="5 7" fill="none" strokeLinejoin="round">
                <animate attributeName="stroke-dashoffset" from="24" to="0" dur={`${1.2 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* 13. ACF VALVE TO/FROM ACF VESSEL (100% CONNECTED ZERO GAPS) */}
          <g id="acf-valve-to-vessel">
            {/* VIN: From left edge of valve (330, 465) into right edge of ACF vessel (275, 465) */}
            <path d="M 330 465 L 275 465" stroke="#0284C7" strokeWidth="4" fill="none" />
            <polygon points="283,462 275,465 283,468" fill="#0284C7" />

            {/* VOUT: From right edge of ACF vessel (275, 495) into left edge of valve (330, 495) */}
            <path d="M 275 495 L 330 495" stroke="#0284C7" strokeWidth="4" fill="none" />
            <polygon points="322,492 330,495 322,498" fill="#0284C7" />
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

          {/* 16. TREATED WATER TANK OUT THROUGH M12, TO FLUSH, TO GARDENING & INTO SOFTENER */}
          <g id="treated-to-softener-line">
            <path d="M 460 645 L 675 645" stroke="#0284C7" strokeWidth="4.5" fill="none" />

            {/* Feeder Pipe 1: TO FLUSH */}
            <path d="M 550 645 L 550 590" stroke="#0284C7" strokeWidth="3.5" fill="none" />
            <polygon points="546,595 550,585 554,595" fill="#0284C7" />

            {/* Feeder Pipe 2: TO GARDENING */}
            <path d="M 595 645 L 595 590" stroke="#16A34A" strokeWidth="3.5" fill="none" />
            <polygon points="591,595 595,585 599,595" fill="#16A34A" />

            <polygon points="660,641 670,645 660,649" fill="#0284C7" />

            {/* Animated flow when M12 is running */}
            {isPlaying && pumps.M12.status === "RUNNING" && (
              <>
                <path d="M 515 645 L 675 645" stroke="#BAE6FD" strokeWidth="2" strokeDasharray="3 5" fill="none">
                  <animate attributeName="stroke-dashoffset" from="16" to="0" dur={`${0.6 / simSpeed}s`} repeatCount="indefinite" />
                </path>
                <path d="M 550 645 L 550 590" stroke="#BAE6FD" strokeWidth="2" strokeDasharray="3 5" fill="none">
                  <animate attributeName="stroke-dashoffset" from="16" to="0" dur={`${0.6 / simSpeed}s`} repeatCount="indefinite" />
                </path>
                <path d="M 595 645 L 595 590" stroke="#BBF7D0" strokeWidth="2" strokeDasharray="3 5" fill="none">
                  <animate attributeName="stroke-dashoffset" from="16" to="0" dur={`${0.6 / simSpeed}s`} repeatCount="indefinite" />
                </path>
              </>
            )}
          </g>

          {/* 17. SOFTENER OUT INTO SOFT WATER TANK (PRISTINE POLISHED CYAN WATER) */}
          <g id="softener-to-soft-water-line">
            <path d="M 755 645 L 840 645" stroke="#06B6D4" strokeWidth="4.5" fill="none" />
            <polygon points="830,641 840,645 830,649" fill="#06B6D4" />
            {isPlaying && (
              <path d="M 755 645 L 840 645" stroke="#A5F3FC" strokeWidth="2.5" strokeDasharray="4 6" fill="none">
                <animate attributeName="stroke-dashoffset" from="20" to="0" dur={`${0.7 / simSpeed}s`} repeatCount="indefinite" />
              </path>
            )}
          </g>

          {/* ====================================================================== */}
          {/* TANKS & VESSELS (2.5D ISOMETRIC / GLASSMORPHIC HIGH-FIDELITY MODELS)   */}
          {/* ====================================================================== */}

          {/* TANK 1: COLLECTION TANK (2.5D GLASS CYLINDER WITH RAW SEWAGE & 3D FLUID MENISCUS) */}
          <g id="tank-collection" transform="translate(135, 48)">
            {renderMiniTag(87.5, 6, "TK-01")}
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

                  {/* 3D Liquid Meniscus (Top Surface Soft Fluid Blend) */}
                  <ellipse cx="87.5" cy={rawY} rx="85.5" ry="6.5" fill="#8D6E63" opacity="0.25" />
                </g>
              )
            })()}

            {/* Cylindrical Specular Light Glare (Left Bright Streak) */}
            <rect x="6" y="16" width="16" height="58" rx="3" fill="url(#specularSheen)" />

            {/* 3D Top Glass Vessel Flange & Rim Opening */}
            <ellipse cx="87.5" cy="14" rx="87.5" ry="8" fill="url(#glassRimGrad)" stroke="#0284C7" strokeWidth="1.5" />
            <ellipse cx="87.5" cy="14" rx="82" ry="5.5" fill="none" stroke="#CBD5E1" strokeWidth="1" strokeDasharray="3 3" opacity="0.6" />
          </g>

          {/* DOTTED BOUNDING BOX FOR MBBR RSTP PUMPS */}
          <rect x="340" y="50" width="90" height="92" rx="4" fill="none" stroke="#93C5FD" strokeWidth="1" strokeDasharray="3 3" />

          {/* PUMPS M1 & M2 (COLLECTION -> MBBR) */}
          {renderPump("M1", 385, 75, "right", "MBBR RSTP 1", undefined, "top")}
          {renderPump("M2", 385, 115, "right", "MBBR RSTP 2", undefined, "bottom")}

          {/* TANK 3: MBBR AERATION TANK (2.5D GLASS CYLINDER WITH K1 BIO-MEDIA & 3D FLUID MENISCUS) */}
          <g id="tank-mbbr" transform="translate(430, 48)">
            {renderMiniTag(70, 6, "MBBR")}
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

              {/* Soft Meniscus Blend at 50% Waterline (Faded Bio-Sludge Brown) */}
              <ellipse cx="70" cy="45" rx="68" ry="6.5" fill="#BCAAA4" opacity="0.3" />
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
          </g>

          {/* DOTTED BOUNDING BOX FOR SLUDGE RECIRCULATION PUMPS M3 & M4 */}
          <rect x="615" y="70" width="85" height="84" rx="4" fill="none" stroke="#93C5FD" strokeWidth="1" strokeDasharray="3 3" />

          {/* SLUDGE PUMPS M3 & M4 (POINTING LEFT, RECIRCULATING TO MBBR & WASTING TO SLUDGE TANK) */}
          {renderPump("M3", 655, 95, "left", "MBBR RCP 1", undefined, "top")}
          {renderPump("M4", 655, 128, "left", "MBBR RCP 2", undefined, "bottom")}

          {/* TANK 4: CLARIFIER TANK WITH CONICAL HOPPER & ROTATING SCRAPER ARM (2.5D CUTAWAY) */}
          <g id="tank-clarifier" transform="translate(740, 48)">
            {renderMiniTag(70, 6, "CLR-01")}
            {/* 2.5D Conical Hopper Tank Hull (Cylindrical Upper + 60° Conical Funnel Bottom) */}
            <path
              d="M 0 14 L 0 54 L 54 88 Q 70 93 86 88 L 140 54 L 140 14 Z"
              fill="url(#glassCylinderGrad)"
              stroke="#0284C7"
              strokeWidth="2"
            />

            {/* Supernatant Clarified Water Zone (Upper Section) with Animated Dual-Layer Waves */}
            <g clipPath="url(#clarifierWaterClip)">
              <path d="M 2 45 L 2 54 L 138 54 L 138 45 Z" fill="url(#clarifierWaterGrad)" opacity="0.88" />

              {/* Clarifier Wave 1: Back secondary wave moving left to right (Amplitude 5.5px) */}
              <path
                d="M -60 45 q 15 -5.5, 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 L 210 54 L -60 54 Z"
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
                d="M -88 45 q 22 -6.5, 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 L 264 54 L -88 54 Z"
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

              {/* 3D Liquid Meniscus Soft Blend at 50% Waterline (Amber Settling Supernatant) */}
              <ellipse cx="70" cy="45" rx="68" ry="6.5" fill="#D2C59D" opacity="0.35" />
            </g>

            {/* Settled Biological Sludge Blanket in Conical Hopper Apex */}
            <path d="M 2 54 L 54 88 Q 70 93 86 88 L 138 54 Z" fill="url(#rawSewageGrad)" />

            {/* Peripheral V-Notch Overflow Weir Trough */}
            <path d="M 4 20 L 136 20" stroke="#38BDF8" strokeWidth="1.2" strokeDasharray="3 2" opacity="0.75" />

            {/* Submerged Rotating Clarifier Bridge & Scraper Rake Arm */}
            <g transform="translate(70, 52)" className="cursor-pointer" onClick={() => handleTogglePump("ARM")}>
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
          </g>

          {/* TANK 5: SLUDGE HOLDING TANK (2.5D CONICAL VESSEL WITH DENSE ACTIVATED SLUDGE) */}
          <g id="tank-sludge" transform="translate(595, 165)">
            {renderMiniTag(57.5, 4, "SLUDGE")}
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
          </g>

          {/* CLARIFIER VALVE */}
          <g id="valve-clarifier" transform="translate(810, 185)" className="cursor-pointer" onClick={() => setClarifierValveOpen(!clarifierValveOpen)}>
            {renderMiniTag(0, -18, "V-CLR")}
            <circle cx="0" cy="0" r="13" fill="url(#metalRingGrad)" stroke="#16A34A" strokeWidth="1" />
            <circle cx="0" cy="0" r="10.5" fill="#DCFCE7" stroke="#16A34A" strokeWidth="1.8" />
            <circle cx="7" cy="-7" r="2.2" fill="#16A34A" stroke="#FFFFFF" strokeWidth="0.6" />
          </g>

          {/* TANK 6: FILTER FEED TANK (2.5D CYLINDRICAL GLASS VESSEL WITH CALIBRATED SIGHT-SCALE) */}
          <g id="tank-filter-feed" transform="translate(740, 238)">
            {renderMiniTag(70, 6, "FF-TK")}
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
          </g>

          {/* BLOWERS 1 & 2 (CLEAR VERTICAL STACK AT X=510, NO OVERLAP) */}
          <g id="blower-1" transform="translate(510, 180)" className="cursor-pointer" onClick={() => handleTogglePump("BL1")}>
            {renderMiniTag(0, -18, "BL1")}
            <circle cx="0" cy="0" r="14" fill="url(#metalRingGrad)" stroke="#F43F5E" strokeWidth="1" />
            <circle cx="0" cy="0" r="11" fill="#FCE7F3" stroke="#F43F5E" strokeWidth="1.8" />
            <g>
              <path d="M -5 0 L 5 0 M 0 -5 L 0 5 M -3.5 -3.5 L 3.5 3.5 M -3.5 3.5 L 3.5 -3.5" stroke="#BE123C" strokeWidth="1.6" strokeLinecap="round" />
            </g>
            <circle cx="9" cy="-9" r="2.5" fill="#DC2626" stroke="#FFFFFF" strokeWidth="0.6" />
          </g>

          <g id="blower-2" transform="translate(510, 240)" className="cursor-pointer" onClick={() => handleTogglePump("BL2")}>
            {renderMiniTag(0, -18, "BL2")}
            <circle cx="0" cy="0" r="14" fill="url(#metalRingGrad)" stroke="#16A34A" strokeWidth="1" />
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
          </g>

          {/* FILTER FEED PUMPS: M10 & M11 */}
          {renderPump("M10", 780, 365, "down", "FF PUMP 1", undefined, "top")}
          {renderPump("M11", 840, 365, "down", "FF PUMP 2", undefined, "top")}

          {/* ====================================================================== */}
          {/* BOTTOM SECTION: PSF, ACF, UV, DOSING, TREATED & SOFT WATER             */}
          {/* ====================================================================== */}

          {/* GREY DASHED BORDER AROUND ACF AREA */}
          <rect x="110" y="415" width="285" height="185" rx="6" fill="none" stroke="#CBD5E1" strokeWidth="1.5" strokeDasharray="4 4" />

          {/* PSF VALVE MULTIPORT BLOCK (UKL 5-Port Multiport Valve) */}
          <g id="psf-valve-block" transform="translate(870, 450)">
            {renderMultiportValve("PSF", psfValveMode, () => {
              const nextModes: Record<MultiportValveMode, MultiportValveMode> = {
                SERVICE: "BRINE",
                BRINE: "BACKWASH",
                BACKWASH: "RINSE",
                RINSE: "REFILL",
                REFILL: "SERVICE",
              }
              setPsfValveMode(prev => nextModes[prev] ?? "SERVICE")
            })}
          </g>

          {/* PSF VESSEL (970, 425) - Dynamic 4-Option Filter Vessel */}
          <g transform="translate(970, 425)">
            {renderFilterVessel("PSF", filterVesselOption)}
          </g>

          {/* ACF VALVE MULTIPORT BLOCK (UKL 5-Port Multiport Valve) */}
          <g id="acf-valve-block" transform="translate(330, 450)">
            {renderMultiportValve("ACF", acfValveMode, () => {
              const nextModes: Record<MultiportValveMode, MultiportValveMode> = {
                SERVICE: "BRINE",
                BRINE: "BACKWASH",
                BACKWASH: "RINSE",
                RINSE: "REFILL",
                REFILL: "SERVICE",
              }
              setAcfValveMode(prev => nextModes[prev] ?? "SERVICE")
            })}
          </g>

          {/* ACF VESSEL (195, 425) - Dynamic 4-Option Filter Vessel */}
          <g transform="translate(195, 425)">
            {renderFilterVessel("ACF", filterVesselOption)}
          </g>

          {/* DOSING PUMP */}
          <g id="dosing-pump" transform="translate(230, 595)">
            {renderMiniTag(16, -7, "DOSING")}
            <polygon points="16,0 32,9 32,27 16,36 0,27 0,9" fill="#DCFCE7" stroke="#16A34A" strokeWidth="2" />
            {/* Animated Stroke Diaphragm Pulse */}
            {isPlaying && (
              <circle cx="16" cy="18" r="6" fill="#16A34A" opacity="0.25">
                <animate attributeName="r" values="3;7;3" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
                <animate attributeName="opacity" values="0.4;0.1;0.4" dur={`${0.8 / simSpeed}s`} repeatCount="indefinite" />
              </circle>
            )}
            <line x1="16" y1="36" x2="16" y2="50" stroke="#16A34A" strokeWidth="2" />
            <polygon points="13,50 16,55 19,50" fill="#16A34A" />
          </g>

          {/* UV LIGHT */}
          <g id="uv-light" transform="translate(105, 620)">
            {renderMiniTag(32.5, -7, "UV")}
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
            {renderMiniTag(70, 6, "TREATED")}
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

            {/* Internal UV Submerged Dip-Pipe (Left Inlet) */}
            <line x1="12" y1="14" x2="12" y2="60" stroke="#0284C7" strokeWidth="2.5" />
            <polygon points="9,58 12,65 15,58" fill="#0284C7" />

            {/* Cylindrical Glare Streak */}
            <rect x="5" y="16" width="14" height="54" rx="3" fill="url(#specularSheen)" />

            {/* 3D Top Glass Vessel Flange & Rim */}
            <ellipse cx="70" cy="14" rx="70" ry="7.0" fill="url(#glassRimGrad)" stroke="#0284C7" strokeWidth="1.5" />
          </g>

          {/* M12: FLUSHING PUMP */}
          {renderPump("M12", 515, 645, "right", "FLUSHING PUMP", undefined, "bottom")}

          {/* WATER SOLENOID VALVE */}
          <g id="valve-water-solenoid" transform="translate(615, 645)" className="cursor-pointer" onClick={() => setWaterSolenoidOpen(!waterSolenoidOpen)}>
            {renderMiniTag(0, -18, "V-SOL")}
            <circle cx="0" cy="0" r="14" fill="url(#metalRingGrad)" stroke={waterSolenoidOpen ? "#16A34A" : "#DC2626"} strokeWidth="1" />
            <circle cx="0" cy="0" r="11" fill={waterSolenoidOpen ? "#DCFCE7" : "#FEE2E2"} stroke={waterSolenoidOpen ? "#16A34A" : "#DC2626"} strokeWidth="1.8" />
            <circle cx="8" cy="-8" r="2.5" fill={waterSolenoidOpen ? "#16A34A" : "#DC2626"} stroke="#FFFFFF" strokeWidth="0.6" />
          </g>

          {/* SOFTENER VESSEL (675, 595) - 2.5D ION-EXCHANGE COLUMN WITH CATION RESIN BED */}
          {/* SOFTENER VESSEL (675, 595) - Dynamic 4-Option Filter Vessel */}
          <g id="vessel-softener" transform="translate(675, 595)">
            {renderMiniTag(40, 6, "SOFTENER")}
            {/* Torispherical Upper Head Dome */}
            <path d="M 1 18 C 1 3, 79 3, 79 18 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="2" />

            {/* Cylindrical Shell Body */}
            <rect x="1" y="18" width="78" height="68" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="2" />

            {/* Torispherical Lower Dish Head */}
            <path d="M 1 86 C 1 100, 79 100, 79 86 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" strokeWidth="2" />

            {/* Circumferential Weld Seams */}
            <line x1="1" y1="28" x2="79" y2="28" stroke="#38BDF8" strokeWidth="1.2" strokeDasharray="3 2" opacity="0.8" />
            <line x1="1" y1="76" x2="79" y2="76" stroke="#38BDF8" strokeWidth="1.2" strokeDasharray="3 2" opacity="0.8" />

            {/* 3D Cutaway Inspection Sight-Glass Window (Cation Resin Bed) */}
            <g transform="translate(10, 32)">
              <rect x="0" y="0" width="58" height="40" rx="3" fill="#0F172A" stroke="#7DD3FC" strokeWidth="1.2" />
              {/* Golden Cation Ion-Exchange Resin Bed */}
              <rect x="2" y="2" width="54" height="28" fill="url(#resinMediaGrad)" opacity="0.95" />
              <rect x="2" y="30" width="54" height="8" rx="2" fill="#78350F" opacity="0.95" />
              {/* Bottom Resin Retention Strainer */}
              <line x1="8" y1="34" x2="50" y2="34" stroke="#CBD5E1" strokeWidth="1.8" />
              {/* Sight Glass Glare */}
              <rect x="2" y="2" width="18" height="36" rx="2" fill="url(#specularSheen)" opacity="0.4" />
            </g>

            {/* Specular Glare Strip */}
            <rect x="4" y="8" width="9" height="80" rx="2" fill="url(#specularSheen)" opacity="0.55" />
            {renderFilterVessel("SOFTENER", filterVesselOption)}
          </g>

          {/* TANK 8: SOFT WATER TANK (840, 603) - 2.5D PRISTINE POLISHED WATER CYLINDER */}
          <g id="tank-soft-water" transform="translate(840, 603)">
            {renderMiniTag(70, 6, "SOFT-TK")}
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
          </g>

          {/* ====================================================================== */}
          {/* LIVE TELEMETRY OVERLAY: OPTION 1 (EMBEDDED) VS OPTION 2 (FLOATING BADGES) */}
          {/* ====================================================================== */}
          {showTelemetryBadges && (
            <g id="telemetry-details-overlay">
              {telemetryMode === "EMBEDDED" ? (
                // OPTION 1: EMBEDDED IN-ELEMENT READOUTS (ZERO PIPE COLLISION)
                <g id="telemetry-embedded-mode">
                  {/* Tanks: Embedded vapor headspace capsules */}
                  {renderEmbeddedTankPill(222.5, 70, "TK-01", `${collectionLevel}%`, "Turbid 15%")}
                  {renderEmbeddedTankPill(500, 70, "MBBR", `${do1.toFixed(2)} DO`, "Bio 35%")}
                  {renderEmbeddedTankPill(810, 70, "CLR-01", `${clarifierTss.toFixed(1)} TSS`, "Settling 55%", "#A855F7")}
                  {renderEmbeddedTankPill(652.5, 185, "SLUDGE", `${sludgeLevel}%`, "WAS Recirc", "#D97706")}
                  {renderEmbeddedTankPill(810, 262, "FF-TK", `${filterFeedLevel}%`, "Pre-Filt 75%", "#14B8A6")}
                  {renderEmbeddedTankPill(390, 625, "TREATED", `${treatedLevel}%`, "Clean 95%", "#0284C7")}
                  {renderEmbeddedTankPill(910, 625, "SOFT-TK", `${softWaterLevel}%`, "Pure 99.9%", "#06B6D4")}
                  {renderEmbeddedTankPill(715, 621, "SOFTENER", `${softwaterHardness.toFixed(1)} mg/L`, "Zero Hardness", "#10B981")}

                  {/* Pumps: Docked micro-flow readouts */}
                  {renderEmbeddedPumpFlow(380, 36, "M1", pumps.M1.flowRate, pumps.M1.status)}
                  {renderEmbeddedPumpFlow(380, 81, "M2", pumps.M2.flowRate, pumps.M2.status)}
                  {renderEmbeddedPumpFlow(448, 175, "BL1", pumps.BL1.flowRate, pumps.BL1.status)}
                  {renderEmbeddedPumpFlow(448, 235, "BL2", pumps.BL2.flowRate, pumps.BL2.status)}
                  {renderEmbeddedPumpFlow(655, 71, "M3", pumps.M3.flowRate, pumps.M3.status)}
                  {renderEmbeddedPumpFlow(655, 152, "M4", pumps.M4.flowRate, pumps.M4.status)}
                  {renderEmbeddedPumpFlow(738, 365, "M10", pumps.M10.flowRate, pumps.M10.status)}
                  {renderEmbeddedPumpFlow(882, 365, "M11", pumps.M11.flowRate, pumps.M11.status)}
                  {renderEmbeddedPumpFlow(500, 621, "M12", pumps.M12.flowRate, pumps.M12.status)}

                  {/* Filter Vessels & Multiport Valves */}
                  {renderTelemetryBadge(980, 398, "PSF", "ΔP", (inletPressure - outletPressure).toFixed(2), "Bar", "NORMAL")}
                  {renderTelemetryBadge(205, 398, "ACF", "Time", formatTime(acfSeconds), "", "NORMAL", 78)}
                  {renderTelemetryBadge(870, 398, "PSF-MPV", "Mode", psfValveMode, "", psfValveMode === "SERVICE" ? "NORMAL" : "STANDBY", 72)}
                  {renderTelemetryBadge(330, 398, "ACF-MPV", "Mode", acfValveMode, "", acfValveMode === "SERVICE" ? "NORMAL" : "STANDBY", 72)}
                </g>
              ) : (
                // OPTION 2: MATHEMATICALLY SAFE FLOATING BADGES GRID (OPTIMIZED NON-COLLIDING COORDINATES)
                <g id="telemetry-badges-mode">
                  {/* 1. Collection Tank (Upper margin clear of nozzles) */}
                  {renderTelemetryBadge(225, 20, "TK-01", "Level", `${collectionLevel}`, "%", "NORMAL")}
                  {renderTelemetryBadge(225, 38, "TK-01", "Quality", "Turbid 15%", "", "STOPPED", 76)}

                  {/* 2. Feed Pumps M1 & M2 (Shifted off discharge pipe line) */}
                  {renderTelemetryBadge(346, 32, "M1", "Flow", pumps.M1.flowRate.toFixed(1), "m³/h", pumps.M1.status)}
                  {renderTelemetryBadge(346, 78, "M2", "Flow", pumps.M2.flowRate.toFixed(1), "m³/h", pumps.M2.status)}

                  {/* 3. MBBR Aeration Tank (Upper clear zone) */}
                  {renderTelemetryBadge(485, 20, "MBBR", "DO", do1.toFixed(2), "mg/L", "NORMAL")}
                  {renderTelemetryBadge(485, 38, "MBBR", "Quality", "Bio-Mix 35%", "", "NORMAL", 80)}

                  {/* 4. Aeration Blowers BL1 & BL2 (Shifted left of vertical riser) */}
                  {renderTelemetryBadge(415, 166, "BL1", "Flow", `${pumps.BL1.flowRate.toFixed(0)}`, "m³/h", pumps.BL1.status)}
                  {renderTelemetryBadge(415, 226, "BL2", "Flow", `${pumps.BL2.flowRate.toFixed(0)}`, "m³/h", pumps.BL2.status)}

                  {/* 5. Sludge Recirculation Pumps M3 & M4 (Shifted above/below suction pipes) */}
                  {renderTelemetryBadge(620, 68, "M3", "Flow", pumps.M3.flowRate.toFixed(1), "m³/h", pumps.M3.status)}
                  {renderTelemetryBadge(620, 104, "M4", "Flow", pumps.M4.flowRate.toFixed(1), "m³/h", pumps.M4.status)}

                  {/* 6. Sludge Holding Tank */}
                  {renderTelemetryBadge(618, 142, "SLUDGE", "Level", `${sludgeLevel}`, "%", "NORMAL")}

                  {/* 7. Clarifier Tank */}
                  {renderTelemetryBadge(800, 20, "CLR-01", "TSS", clarifierTss.toFixed(2), "mg/L", "NORMAL")}
                  {renderTelemetryBadge(800, 38, "CLR-01", "Quality", "Settling 55%", "", "STANDBY", 82)}

                  {/* 8. Filter Feed Tank */}
                  {renderTelemetryBadge(800, 214, "FF-TK", "Level", `${filterFeedLevel}`, "%", "NORMAL")}
                  {renderTelemetryBadge(800, 232, "FF-TK", "Quality", "Pre-Filt 75%", "", "NORMAL", 80)}

                  {/* 9. Filter Feed Pumps M10 & M11 (Shifted away from vertical suction lines) */}
                  {renderTelemetryBadge(705, 356, "M10", "Flow", pumps.M10.flowRate.toFixed(1), "m³/h", pumps.M10.status)}
                  {renderTelemetryBadge(864, 356, "M11", "Flow", pumps.M11.flowRate.toFixed(1), "m³/h", pumps.M11.status)}

                  {/* 10. Media Filter Vessels PSF & ACF (Uniform ribbon at y=398) */}
                  {renderTelemetryBadge(980, 398, "PSF", "ΔP", (inletPressure - outletPressure).toFixed(2), "Bar", "NORMAL")}
                  {renderTelemetryBadge(205, 398, "ACF", "Time", formatTime(acfSeconds), "", "NORMAL", 78)}

                  {/* 10b. PSF & ACF Multiport Valve Mode Badges */}
                  {renderTelemetryBadge(870, 398, "PSF-MPV", "Mode", psfValveMode, "", psfValveMode === "SERVICE" ? "NORMAL" : "STANDBY", 72)}
                  {renderTelemetryBadge(330, 398, "ACF-MPV", "Mode", acfValveMode, "", acfValveMode === "SERVICE" ? "NORMAL" : "STANDBY", 72)}

                  {/* 11. Treated Water Tank */}
                  {renderTelemetryBadge(390, 580, "TREATED", "Level", `${treatedLevel}`, "%", "NORMAL")}
                  {renderTelemetryBadge(390, 598, "TREATED", "Quality", "Clean 95%", "", "NORMAL", 78)}

                  {/* 12. Flushing Pump M12 */}
                  {renderTelemetryBadge(465, 618, "M12", "Flow", pumps.M12.flowRate.toFixed(1), "m³/h", pumps.M12.status)}

                  {/* 13. Soft Water Tank */}
                  {renderTelemetryBadge(910, 580, "SOFT-TK", "Level", `${softWaterLevel}`, "%", "NORMAL")}
                  {renderTelemetryBadge(910, 598, "SOFT-TK", "Quality", "Pure 99.9%", "", "NORMAL", 78)}

                  {/* 14. Softener Telemetry Badge */}
                  {renderTelemetryBadge(680, 565, "SOFTENER", "Hardness", softwaterHardness.toFixed(2), "mg/L", "NORMAL", 80)}
                </g>
              )}
            </g>
          )}
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
      <div className="px-4 py-2.5 bg-sky-50/50 border-t border-sky-100 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5 text-xs">
        <div className="p-2 rounded-lg bg-white border border-sky-100 shadow-xs flex flex-col">
          <span className="text-[10px] text-slate-500 uppercase font-mono">Aeration DO1</span>
          <span className="text-sm font-bold text-sky-700 font-mono">{do1.toFixed(2)} mg/L</span>
          <span className="text-[9px] text-emerald-600 font-medium">Normal (0.5–2.0)</span>
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
