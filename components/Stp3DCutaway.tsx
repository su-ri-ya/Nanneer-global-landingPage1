"use client"

import React, { useEffect, useRef, useState, useCallback } from "react"
import { motion, AnimatePresence } from "framer-motion"
import {
  Play,
  Pause,
  RotateCw,
  Activity,
  Droplets,
  Building2,
  Fan,
  Trees,
  ShieldCheck,
  CheckCircle2,
  Gauge,
  Sparkles,
} from "lucide-react"

interface ChamberInfo {
  id: string
  stepNumber: number
  code: string
  name: string
  stage: string
  color: string
  coreMessage: string
  mechanicalDetail: string
  compliance: string
  stats: { label: string; value: string }[]
  targetRotY: number
}

const CHAMBERS: ChamberInfo[] = [
  {
    id: "inlet",
    stepNumber: 1,
    code: "CH-01",
    name: "Bar Screen & Equalization Buffer",
    stage: "STAGE 1 · INTAKE & SCREENING",
    color: "#64748B",
    coreMessage: "Zero Overflows · Prevents Upstream Line Incidents",
    mechanicalDetail: "6mm mechanical bar screen traps debris; sub-surface air mixers prevent septic anaerobic stagnation.",
    compliance: "CPCB Raw Load Normalization",
    stats: [
      { label: "Raw Inflow", value: "120 m³/d" },
      { label: "Peak Buffer", value: "48,000 L" },
    ],
    targetRotY: -0.75,
  },
  {
    id: "aeration",
    stepNumber: 2,
    code: "CH-02",
    name: "MBBR Bioreactor & Disc Diffusers",
    stage: "STAGE 2 · BIOLOGICAL DIGESTION",
    color: "#0EA5E9",
    coreMessage: "Trained Operators · DO & Biomass Monitored 24×7",
    mechanicalDetail: "Fine-bubble EPDM disc diffusers pulse continuous oxygen; HDPE bio-media carriers support high-density biofilm digestion.",
    compliance: "BOD < 10 mg/L (100% Compliant)",
    stats: [
      { label: "Dissolved O₂", value: "2.4 mg/L" },
      { label: "MLSS Bio-load", value: "3,800 mg/L" },
    ],
    targetRotY: -0.25,
  },
  {
    id: "clarifier",
    stepNumber: 3,
    code: "CH-03",
    name: "Clarifier Hopper & RAS Recycling",
    stage: "STAGE 3 · GRAVITY SEDIMENTATION",
    color: "#0284C7",
    coreMessage: "Preventive Maintenance · Continuous Sludge Blanket Audit",
    mechanicalDetail: "Rotating clarifier scraper sweeps settled biomass into conical hopper; Return Activated Sludge (RAS) pumps loop live bacteria.",
    compliance: "TSS < 10 mg/L · Sludge Monitored",
    stats: [
      { label: "Sludge Blanket", value: "0.8 m" },
      { label: "RAS Return", value: "35 L/min" },
    ],
    targetRotY: 0.28,
  },
  {
    id: "recovered",
    stepNumber: 4,
    code: "CH-04",
    name: "Tertiary Filtration & Building Reuse",
    stage: "STAGE 4 · 98.4% WATER RECOVERY",
    color: "#059669",
    coreMessage: "Eliminate Tanker Water Bills · Maximized Building Reuse",
    mechanicalDetail: "Sand & Activated Carbon filters eliminate color and odor; high-pressure pumps supply HVAC towers, flushing & landscaping.",
    compliance: "Turbidity < 2 NTU · Odor Free",
    stats: [
      { label: "HVAC Cooling", value: "54 m³/d" },
      { label: "Flush & Garden", value: "64 m³/d" },
    ],
    targetRotY: 0.78,
  },
]

export function Stp3DCutaway() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const [selectedChamber, setSelectedChamber] = useState<ChamberInfo>(CHAMBERS[0])
  const [isTouring, setIsTouring] = useState(true)
  const [isDragging, setIsDragging] = useState(false)
  const [activeReuseTab, setActiveReuseTab] = useState<"hvac" | "flush" | "garden">("hvac")

  // 3D Rotation angles in radians
  const rotX = useRef<number>(0.36)
  const rotY = useRef<number>(-0.4)
  const targetRotY = useRef<number>(-0.4)
  const lastMousePos = useRef<{ x: number; y: number }>({ x: 0, y: 0 })
  const tourStep = useRef<number>(0)
  const tourTimer = useRef<number>(0)

  // 3D projection math helpers
  const project3D = (
    x: number,
    y: number,
    z: number,
    rx: number,
    ry: number,
    cx: number,
    cy: number,
    scale: number
  ) => {
    // Rotate Y
    const cosY = Math.cos(ry)
    const sinY = Math.sin(ry)
    const x1 = x * cosY - z * sinY
    const z1 = x * sinY + z * cosY

    // Rotate X
    const cosX = Math.cos(rx)
    const sinX = Math.sin(rx)
    const y2 = y * cosX - z1 * sinX
    const z2 = y * sinX + z1 * cosX

    // Perspective projection
    const fov = 430
    const distance = 490
    const factor = fov / (distance + z2)

    return {
      x: cx + x1 * scale * factor,
      y: cy + y2 * scale * factor,
      z: z2,
      scale: factor,
    }
  }

  // Handle Chamber Selection
  const selectChamber = (chamber: ChamberInfo) => {
    setSelectedChamber(chamber)
    targetRotY.current = chamber.targetRotY
    setIsTouring(false)
  }

  // Toggle Automated Flow Tour
  const toggleTour = () => {
    setIsTouring((prev) => !prev)
  }

  // Reset to default isometric angle
  const handleReset = useCallback(() => {
    rotX.current = 0.36
    targetRotY.current = -0.4
    rotY.current = -0.4
    setSelectedChamber(CHAMBERS[0])
    setIsTouring(false)
  }, [])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext("2d")
    if (!ctx) return

    let animationFrameId: number
    let width = (canvas.width = canvas.offsetWidth * 2)
    let height = (canvas.height = canvas.offsetHeight * 2)

    const handleResize = () => {
      if (!canvas) return
      width = canvas.width = canvas.offsetWidth * 2
      height = canvas.height = canvas.offsetHeight * 2
    }

    window.addEventListener("resize", handleResize)

    // A. 3D Fine-Bubble Disc Aeration Plumes for Chamber 2
    const bubbles: {
      x: number
      y: number
      z: number
      radius: number
      speed: number
      wobble: number
    }[] = []
    for (let i = 0; i < 65; i++) {
      bubbles.push({
        x: -12 + (Math.random() - 0.5) * 55,
        y: 45 - Math.random() * 90,
        z: (Math.random() - 0.5) * 48,
        radius: 1.0 + Math.random() * 2.2,
        speed: 0.65 + Math.random() * 1.1,
        wobble: Math.random() * Math.PI * 2,
      })
    }

    // B. MBBR Bio-Carrier Media tumbling in Chamber 2
    const mbbrCarriers: {
      x: number
      y: number
      z: number
      rot: number
      speedRot: number
    }[] = []
    for (let i = 0; i < 22; i++) {
      mbbrCarriers.push({
        x: -12 + (Math.random() - 0.5) * 50,
        y: 25 - Math.random() * 55,
        z: (Math.random() - 0.5) * 42,
        rot: Math.random() * Math.PI,
        speedRot: (Math.random() - 0.5) * 0.05,
      })
    }

    // C. Settling biomass particles for Chamber 3 (Clarifier)
    const settlingParticles: {
      x: number
      y: number
      z: number
      radius: number
      speed: number
    }[] = []
    for (let i = 0; i < 30; i++) {
      settlingParticles.push({
        x: 50 + (Math.random() - 0.5) * 45,
        y: -20 + Math.random() * 65,
        z: (Math.random() - 0.5) * 45,
        radius: 1.0 + Math.random() * 1.8,
        speed: 0.25 + Math.random() * 0.35,
      })
    }

    let time = 0

    const render = () => {
      time += 0.03
      ctx.clearRect(0, 0, width, height)

      // Automated Flow Tour camera stepper
      if (isTouring && !isDragging) {
        tourTimer.current += 1
        if (tourTimer.current > 220) {
          tourTimer.current = 0
          tourStep.current = (tourStep.current + 1) % CHAMBERS.length
          const nextChamber = CHAMBERS[tourStep.current]
          setSelectedChamber(nextChamber)
          targetRotY.current = nextChamber.targetRotY
        }
      }

      // Smooth camera interpolation
      if (!isDragging) {
        rotY.current += (targetRotY.current - rotY.current) * 0.06
      }

      const rx = rotX.current
      const ry = rotY.current
      const cx = width / 2
      const cy = height / 2 + 10
      const scale = width > 800 ? 2.15 : 1.7

      // Tank dimensions
      const tw = 240
      const th = 110
      const td = 100

      // Chamber division points along X: [-120, -50, 25, 75, 120]
      const wallsX = [-120, -50, 25, 75, 120]

      // Helper to draw a projected quad with fill and stroke
      const drawQuad = (
        p1: [number, number, number],
        p2: [number, number, number],
        p3: [number, number, number],
        p4: [number, number, number],
        fillStyle: string,
        strokeStyle?: string,
        lineWidth: number = 1
      ) => {
        const pt1 = project3D(p1[0], p1[1], p1[2], rx, ry, cx, cy, scale)
        const pt2 = project3D(p2[0], p2[1], p2[2], rx, ry, cx, cy, scale)
        const pt3 = project3D(p3[0], p3[1], p3[2], rx, ry, cx, cy, scale)
        const pt4 = project3D(p4[0], p4[1], p4[2], rx, ry, cx, cy, scale)

        ctx.beginPath()
        ctx.moveTo(pt1.x, pt1.y)
        ctx.lineTo(pt2.x, pt2.y)
        ctx.lineTo(pt3.x, pt3.y)
        ctx.lineTo(pt4.x, pt4.y)
        ctx.closePath()

        ctx.fillStyle = fillStyle
        ctx.fill()

        if (strokeStyle) {
          ctx.strokeStyle = strokeStyle
          ctx.lineWidth = lineWidth
          ctx.stroke()
        }
      }

      // Helper to draw a projected 3D pipe segment with flowing pulse
      const drawPipe = (
        from: [number, number, number],
        to: [number, number, number],
        color: string,
        lineWidth: number = 3,
        pulseOffset: number = 0
      ) => {
        const p1 = project3D(from[0], from[1], from[2], rx, ry, cx, cy, scale)
        const p2 = project3D(to[0], to[1], to[2], rx, ry, cx, cy, scale)

        // Outer body
        ctx.beginPath()
        ctx.moveTo(p1.x, p1.y)
        ctx.lineTo(p2.x, p2.y)
        ctx.strokeStyle = "rgba(11, 37, 69, 0.45)"
        ctx.lineWidth = lineWidth + 2
        ctx.stroke()

        // Inner core
        ctx.beginPath()
        ctx.moveTo(p1.x, p1.y)
        ctx.lineTo(p2.x, p2.y)
        ctx.strokeStyle = color
        ctx.lineWidth = lineWidth
        ctx.stroke()

        // Flowing pulse packet
        const t = ((time * 0.85 + pulseOffset) % 1)
        const packetX = p1.x + (p2.x - p1.x) * t
        const packetY = p1.y + (p2.y - p1.y) * t

        ctx.beginPath()
        ctx.arc(packetX, packetY, lineWidth * 1.25, 0, Math.PI * 2)
        ctx.fillStyle = "#FFFFFF"
        ctx.fill()
        ctx.strokeStyle = color
        ctx.lineWidth = 1.3
        ctx.stroke()
      }

      // 1. Concrete Slab Foundation
      drawQuad(
        [-tw / 2 - 16, th / 2 + 10, -td / 2 - 16],
        [tw / 2 + 16, th / 2 + 10, -td / 2 - 16],
        [tw / 2 + 16, th / 2 + 10, td / 2 + 16],
        [-tw / 2 - 16, th / 2 + 10, td / 2 + 16],
        "#E2E8F0",
        "rgba(148, 163, 184, 0.6)",
        2
      )

      // 2. Tank Back Wall & Floor
      drawQuad(
        [-tw / 2, -th / 2, -td / 2],
        [tw / 2, -th / 2, -td / 2],
        [tw / 2, th / 2, -td / 2],
        [-tw / 2, th / 2, -td / 2],
        "#F1F5F9",
        "rgba(148, 163, 184, 0.4)",
        1.5
      )
      drawQuad(
        [-tw / 2, th / 2, -td / 2],
        [tw / 2, th / 2, -td / 2],
        [tw / 2, th / 2, td / 2],
        [-tw / 2, th / 2, td / 2],
        "#E2E8F0",
        "rgba(148, 163, 184, 0.6)",
        1.5
      )

      // 3. Chamber Liquid Volumes (Transformation from Sewage to Crystal-Clear Reusable Water)
      // Chamber 1: Raw Influent
      drawQuad(
        [wallsX[0], -15, -td / 2 + 4],
        [wallsX[1], -15, -td / 2 + 4],
        [wallsX[1], th / 2, -td / 2 + 4],
        [wallsX[0], th / 2, -td / 2 + 4],
        "rgba(100, 116, 139, 0.45)"
      )
      drawQuad(
        [wallsX[0], -15, -td / 2 + 4],
        [wallsX[1], -15, -td / 2 + 4],
        [wallsX[1], -15, td / 2 - 4],
        [wallsX[0], -15, td / 2 - 4],
        "rgba(148, 163, 184, 0.65)",
        "rgba(100, 116, 139, 0.4)"
      )

      // Mechanical Bar Screen representation in Chamber 1
      const screenP1 = project3D(wallsX[0] + 18, -25, -td / 3, rx, ry, cx, cy, scale)
      const screenP2 = project3D(wallsX[0] + 18, th / 2, -td / 3, rx, ry, cx, cy, scale)
      ctx.beginPath()
      ctx.moveTo(screenP1.x, screenP1.y)
      ctx.lineTo(screenP2.x, screenP2.y)
      ctx.strokeStyle = "#475569"
      ctx.lineWidth = 3
      ctx.stroke()

      // Chamber 2: MBBR Bioreactor (Aeration Wave)
      const waveOffset = Math.sin(time * 2.8) * 3.2
      drawQuad(
        [wallsX[1], -25 + waveOffset, -td / 2 + 4],
        [wallsX[2], -25 + waveOffset, -td / 2 + 4],
        [wallsX[2], th / 2, -td / 2 + 4],
        [wallsX[1], th / 2, -td / 2 + 4],
        "rgba(14, 165, 233, 0.42)"
      )
      drawQuad(
        [wallsX[1], -25 + waveOffset, -td / 2 + 4],
        [wallsX[2], -25 + waveOffset, -td / 2 + 4],
        [wallsX[2], -25 + waveOffset, td / 2 - 4],
        [wallsX[1], -25 + waveOffset, td / 2 - 4],
        "rgba(56, 189, 248, 0.72)",
        "rgba(2, 132, 199, 0.45)"
      )

      // Aeration Bottom Disc Diffuser Manifolds (3 Discs in Chamber 2)
      const diffuserXs = [-30, -12, 6]
      diffuserXs.forEach((dx) => {
        const dp = project3D(dx, th / 2 - 2, 0, rx, ry, cx, cy, scale)
        ctx.beginPath()
        ctx.ellipse(dp.x, dp.y, 8 * dp.scale, 3.5 * dp.scale, 0, 0, Math.PI * 2)
        ctx.fillStyle = "#0284C7"
        ctx.fill()
        ctx.strokeStyle = "#FFFFFF"
        ctx.lineWidth = 1
        ctx.stroke()
      })

      // Rising fine-bubbles from diffusers
      bubbles.forEach((b) => {
        b.y -= b.speed
        b.wobble += 0.08
        if (b.y < -25 + waveOffset) {
          b.y = th / 2 - 6
        }
        const bx = b.x + Math.sin(b.wobble) * 2.8
        const p = project3D(bx, b.y, b.z, rx, ry, cx, cy, scale)

        ctx.beginPath()
        ctx.arc(p.x, p.y, b.radius * p.scale * 1.8, 0, Math.PI * 2)
        ctx.fillStyle = "rgba(255, 255, 255, 0.88)"
        ctx.fill()
        ctx.strokeStyle = "rgba(14, 165, 233, 0.65)"
        ctx.lineWidth = 1
        ctx.stroke()
      })

      // Swirling MBBR Bio-Carriers in Chamber 2
      mbbrCarriers.forEach((c) => {
        c.rot += c.speedRot
        const p = project3D(c.x + Math.sin(time + c.rot) * 2, c.y, c.z, rx, ry, cx, cy, scale)
        ctx.save()
        ctx.translate(p.x, p.y)
        ctx.rotate(c.rot)
        ctx.strokeStyle = "rgba(2, 132, 199, 0.75)"
        ctx.lineWidth = 1.2
        ctx.beginPath()
        ctx.rect(-3 * p.scale, -3 * p.scale, 6 * p.scale, 6 * p.scale)
        ctx.stroke()
        ctx.restore()
      })

      // Chamber 3: Clarifier Hopper & Settling Sludge
      drawQuad(
        [wallsX[2], -22, -td / 2 + 4],
        [wallsX[3], -22, -td / 2 + 4],
        [wallsX[3], th / 2, -td / 2 + 4],
        [wallsX[2], th / 2, -td / 2 + 4],
        "rgba(2, 132, 199, 0.32)"
      )
      // Bottom Conical Sludge Blanket
      drawQuad(
        [wallsX[2] + 4, th / 2 - 20, -td / 2 + 6],
        [wallsX[3] - 4, th / 2 - 20, -td / 2 + 6],
        [wallsX[3] - 4, th / 2, td / 2 - 6],
        [wallsX[2] + 4, th / 2, td / 2 - 6],
        "rgba(30, 41, 59, 0.5)",
        "rgba(15, 23, 42, 0.6)",
        1
      )
      drawQuad(
        [wallsX[2], -22, -td / 2 + 4],
        [wallsX[3], -22, -td / 2 + 4],
        [wallsX[3], -22, td / 2 - 4],
        [wallsX[2], -22, td / 2 - 4],
        "rgba(56, 189, 248, 0.58)",
        "rgba(2, 132, 199, 0.3)"
      )

      // Rotating Clarifier Scraper Arm Bridge (Chamber 3)
      const scraperAngle = time * 0.4
      const scrX1 = 50 + Math.cos(scraperAngle) * 20
      const scrZ1 = Math.sin(scraperAngle) * 20
      const scrX2 = 50 - Math.cos(scraperAngle) * 20
      const scrZ2 = -Math.sin(scraperAngle) * 20
      const sp1 = project3D(scrX1, th / 2 - 3, scrZ1, rx, ry, cx, cy, scale)
      const sp2 = project3D(scrX2, th / 2 - 3, scrZ2, rx, ry, cx, cy, scale)
      ctx.beginPath()
      ctx.moveTo(sp1.x, sp1.y)
      ctx.lineTo(sp2.x, sp2.y)
      ctx.strokeStyle = "#0B2545"
      ctx.lineWidth = 2.5
      ctx.stroke()

      // Settling biomass particles in Clarifier
      settlingParticles.forEach((sp) => {
        sp.y += sp.speed
        if (sp.y > th / 2 - 6) {
          sp.y = -20
        }
        const p = project3D(sp.x, sp.y, sp.z, rx, ry, cx, cy, scale)
        ctx.beginPath()
        ctx.arc(p.x, p.y, sp.radius * p.scale, 0, Math.PI * 2)
        ctx.fillStyle = "rgba(30, 41, 59, 0.7)"
        ctx.fill()
      })

      // Chamber 4: Polished Recovered Clean Effluent
      drawQuad(
        [wallsX[3], -20, -td / 2 + 4],
        [wallsX[4], -20, -td / 2 + 4],
        [wallsX[4], th / 2, -td / 2 + 4],
        [wallsX[3], th / 2, -td / 2 + 4],
        "rgba(16, 185, 129, 0.28)"
      )
      drawQuad(
        [wallsX[3], -20, -td / 2 + 4],
        [wallsX[4], -20, -td / 2 + 4],
        [wallsX[4], -20, td / 2 - 4],
        [wallsX[3], -20, td / 2 - 4],
        "rgba(52, 211, 153, 0.7)",
        "rgba(5, 150, 105, 0.45)"
      )

      // 4. ANIMATED FLOW PIPELINES & TRANSFER
      // A. Raw Sewage Inflow Pipe
      drawPipe([-145, -th / 2 - 18, 0], [-105, -th / 2 - 18, 0], "#64748B", 4, 0.1)
      drawPipe([-105, -th / 2 - 18, 0], [-105, -10, 0], "#64748B", 3.5, 0.3)

      // B. Transfer Pipe 1 -> 2: Screened effluent to Aeration
      drawPipe([wallsX[1], 10, -td / 4], [wallsX[1] + 20, 10, -td / 4], "#0EA5E9", 3, 0.4)

      // C. Transfer Pipe 2 -> 3: Mixed liquor to Clarifier
      drawPipe([wallsX[2], -8, td / 4], [wallsX[2] + 18, -8, td / 4], "#0284C7", 3, 0.6)

      // D. Return Activated Sludge (RAS) Loop Pipe: Chamber 3 hopper back to Chamber 2
      drawPipe([wallsX[3] - 25, th / 2 + 5, 0], [wallsX[1] + 15, th / 2 + 5, 0], "#0284C7", 3.5, 0.85)

      // E. Transfer / Overflow Weir to Chamber 4 (Recovered)
      drawPipe([wallsX[3], -18, 0], [wallsX[3] + 15, -18, 0], "#10B981", 3, 0.7)

      // F. Building Reuse Outflow Lines (Triple Distribution)
      // 1. Line to HVAC Cooling Towers
      drawPipe([wallsX[4] - 15, -15, -td / 4], [150, -35, -td / 4], "#059669", 3.5, 0.9)
      // 2. Line to Dual-Flush Plumbing
      drawPipe([wallsX[4] - 15, -2, 0], [150, -2, 0], "#0284C7", 3.5, 0.95)
      // 3. Line to Landscaping & Irrigation
      drawPipe([wallsX[4] - 15, 12, td / 4], [150, 30, td / 4], "#10B981", 3.5, 0.8)

      // 5. Draw Chamber Baffle Divider Glass Plates
      wallsX.slice(1, -1).forEach((wx) => {
        drawQuad(
          [wx, -th / 2, -td / 2],
          [wx, -th / 2, td / 2],
          [wx, th / 2, td / 2],
          [wx, th / 2, -td / 2],
          "rgba(255, 255, 255, 0.35)",
          "rgba(14, 165, 233, 0.45)",
          1.5
        )
      })

      // 6. Transparent Front Glass Cutaway Face
      drawQuad(
        [-tw / 2, -th / 2, td / 2],
        [tw / 2, -th / 2, td / 2],
        [tw / 2, th / 2, td / 2],
        [-tw / 2, th / 2, td / 2],
        "rgba(255, 255, 255, 0.12)",
        "rgba(14, 165, 233, 0.6)",
        2
      )

      // 7. Structural Frame Bevels (Navy / Steel Structural Posts)
      const cornerPosts = [
        [-tw / 2, -th / 2, -td / 2, -tw / 2, th / 2, -td / 2],
        [tw / 2, -th / 2, -td / 2, tw / 2, th / 2, -td / 2],
        [tw / 2, -th / 2, td / 2, tw / 2, th / 2, td / 2],
        [-tw / 2, -th / 2, td / 2, -tw / 2, th / 2, td / 2],
      ]
      cornerPosts.forEach((post) => {
        const p1 = project3D(post[0], post[1], post[2], rx, ry, cx, cy, scale)
        const p2 = project3D(post[3], post[4], post[5], rx, ry, cx, cy, scale)
        ctx.beginPath()
        ctx.moveTo(p1.x, p1.y)
        ctx.lineTo(p2.x, p2.y)
        ctx.strokeStyle = "#0B2545"
        ctx.lineWidth = 3
        ctx.stroke()
      })

      // 8. 3D Floating Chamber Flow Step Badges
      const flowSteps = [
        { name: "1. RAW INTAKE", x: -85, y: -th / 2 - 12, z: 0, color: "#64748B" },
        { name: "2. MBBR AERATION", x: -12, y: -th / 2 - 14, z: 0, color: "#0EA5E9" },
        { name: "3. CLARIFIER & RAS", x: 50, y: -th / 2 - 12, z: 0, color: "#0284C7" },
        { name: "4. BUILDING REUSE", x: 98, y: -th / 2 - 12, z: 0, color: "#059669" },
      ]
      flowSteps.forEach((step) => {
        const p = project3D(step.x, step.y, step.z, rx, ry, cx, cy, scale)
        ctx.font = "bold 9px 'JetBrains Mono', monospace"
        ctx.textAlign = "center"
        ctx.textBaseline = "middle"

        const textWidth = ctx.measureText(step.name).width
        ctx.fillStyle = "rgba(255, 255, 255, 0.95)"
        ctx.strokeStyle = step.color
        ctx.lineWidth = 1.2
        ctx.beginPath()
        ctx.roundRect(p.x - textWidth / 2 - 5, p.y - 7, textWidth + 10, 14, 4)
        ctx.fill()
        ctx.stroke()

        ctx.fillStyle = step.color
        ctx.fillText(step.name, p.x, p.y)
      })

      // 9. Floating Building Destination Badges on Right Side
      const destP1 = project3D(152, -35, -td / 4, rx, ry, cx, cy, scale)
      const destP2 = project3D(152, -2, 0, rx, ry, cx, cy, scale)
      const destP3 = project3D(152, 30, td / 4, rx, ry, cx, cy, scale)

      const drawDestBadge = (p: { x: number; y: number }, label: string, color: string) => {
        ctx.font = "bold 8px 'JetBrains Mono', monospace"
        ctx.textAlign = "left"
        ctx.textBaseline = "middle"
        const tw = ctx.measureText(label).width
        ctx.fillStyle = "rgba(255, 255, 255, 0.95)"
        ctx.strokeStyle = color
        ctx.lineWidth = 1
        ctx.beginPath()
        ctx.roundRect(p.x + 4, p.y - 6, tw + 8, 12, 3)
        ctx.fill()
        ctx.stroke()
        ctx.fillStyle = color
        ctx.fillText(label, p.x + 8, p.y)
      }

      drawDestBadge(destP1, "HVAC COOLING", "#059669")
      drawDestBadge(destP2, "FLUSH PLUMBING", "#0284C7")
      drawDestBadge(destP3, "LANDSCAPING", "#10B981")

      animationFrameId = requestAnimationFrame(render)
    }

    render()

    return () => {
      window.removeEventListener("resize", handleResize)
      cancelAnimationFrame(animationFrameId)
    }
  }, [isDragging, isTouring])

  // Mouse & Touch Orbit Controls
  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true)
    setIsTouring(false)
    lastMousePos.current = { x: e.clientX, y: e.clientY }
  }

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return
    const dx = e.clientX - lastMousePos.current.x
    const dy = e.clientY - lastMousePos.current.y
    targetRotY.current += dx * 0.008
    rotX.current = Math.max(0.15, Math.min(0.65, rotX.current + dy * 0.008))
    lastMousePos.current = { x: e.clientX, y: e.clientY }
  }

  const handleMouseUp = () => {
    setIsDragging(false)
  }

  const handleTouchStart = (e: React.TouchEvent) => {
    if (e.touches.length !== 1) return
    setIsDragging(true)
    setIsTouring(false)
    lastMousePos.current = { x: e.touches[0].clientX, y: e.touches[0].clientY }
  }

  const handleTouchMove = (e: React.TouchEvent) => {
    if (!isDragging || e.touches.length !== 1) return
    const dx = e.touches[0].clientX - lastMousePos.current.x
    const dy = e.touches[0].clientY - lastMousePos.current.y
    targetRotY.current += dx * 0.008
    rotX.current = Math.max(0.15, Math.min(0.65, rotX.current + dy * 0.008))
    lastMousePos.current = { x: e.touches[0].clientX, y: e.touches[0].clientY }
  }

  return (
    <div className="relative w-full aspect-[16/10] h-[330px] sm:h-[380px] lg:h-[420px] xl:h-[460px] rounded-2xl overflow-hidden group select-none">
      {/* 3D WebGL / Canvas Container */}
      <canvas
        ref={canvasRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleMouseUp}
        className="w-full h-full block cursor-grab active:cursor-grabbing"
      />

      {/* Top Header Bar: Live Operations Telemetry & Tour Mode */}
      <div className="absolute top-3 left-3 right-3 flex items-center justify-between pointer-events-none">
        <div className="flex items-center gap-2 pointer-events-auto">
          <div className="bg-white/95 backdrop-blur-md px-3 py-1 rounded-full border border-sky-200 shadow-2xs flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
            <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-800">
              STP 24×7 Operations Simulation
            </span>
          </div>

          {/* Tour Mode Toggle Button */}
          <button
            onClick={toggleTour}
            className={`px-2.5 py-1 rounded-full text-[10px] font-mono font-bold uppercase tracking-wider flex items-center gap-1.5 transition-all shadow-2xs ${
              isTouring
                ? "bg-sky-600 text-white shadow-sky-600/25"
                : "bg-white/95 backdrop-blur-md text-slate-700 border border-sky-200 hover:border-sky-400 hover:text-sky-600"
            }`}
          >
            {isTouring ? (
              <>
                <Pause className="w-3 h-3" />
                <span>Touring Flow</span>
              </>
            ) : (
              <>
                <Play className="w-3 h-3 fill-current" />
                <span>Tour Flow</span>
              </>
            )}
          </button>
        </div>

        {/* Reset 3D View Button */}
        <button
          onClick={handleReset}
          className="bg-white/95 backdrop-blur-md p-1.5 rounded-full border border-sky-200 hover:border-sky-400 text-slate-700 hover:text-sky-600 transition-all shadow-2xs pointer-events-auto"
          title="Reset 3D Angle"
        >
          <RotateCw className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Live Core Mission Ribbon: Mechanical Action & Core Website Value */}
      <div className="absolute top-12 left-3 right-3 pointer-events-none">
        <div className="bg-white/90 backdrop-blur-sm px-3 py-1.5 rounded-lg border border-sky-100 shadow-2xs flex items-center justify-between gap-2">
          <div className="flex items-center gap-1.5 text-[10px] font-bold text-[#0B2545]">
            <ShieldCheck className="w-3.5 h-3.5 text-sky-600 shrink-0" />
            <span className="truncate">{selectedChamber.coreMessage}</span>
          </div>
          <div className="hidden sm:flex items-center gap-1 text-[9px] font-mono font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
            <CheckCircle2 className="w-3 h-3" />
            <span>{selectedChamber.compliance}</span>
          </div>
        </div>
      </div>

      {/* Active Flow Stage Ribbon at Bottom */}
      <div className="absolute bottom-2.5 left-2.5 right-2.5 bg-white/95 backdrop-blur-md rounded-xl border border-sky-200/90 p-2 sm:p-2.5 shadow-xs flex flex-wrap items-center justify-between gap-2 pointer-events-auto">
        {/* Step Selector Pills */}
        <div className="flex items-center gap-1 overflow-x-auto py-0.5">
          {CHAMBERS.map((ch) => {
            const isSelected = selectedChamber.id === ch.id
            return (
              <button
                key={ch.id}
                onClick={() => selectChamber(ch)}
                className={`px-2 py-0.5 rounded text-[9px] font-mono font-bold uppercase tracking-wider transition-all duration-200 shrink-0 flex items-center gap-1 ${
                  isSelected
                    ? "bg-[#0B2545] text-white shadow-2xs"
                    : "bg-slate-100 hover:bg-sky-50 text-slate-600 hover:text-sky-700"
                }`}
              >
                <span>{ch.code}</span>
              </button>
            )
          })}
        </div>

        {/* Live Stage Stats */}
        <div className="flex items-center gap-2 sm:gap-3 text-[9px] font-mono text-slate-700 shrink-0 ml-auto">
          <div className="flex items-center gap-1 text-sky-700 font-bold">
            <Activity className="w-3 h-3 animate-pulse text-sky-600" />
            <span className="hidden md:inline">{selectedChamber.stage}</span>
          </div>
          <span className="text-slate-300">|</span>
          {selectedChamber.stats.map((s, idx) => (
            <div key={idx} className="flex items-center gap-1">
              <span className="text-slate-400">{s.label}:</span>
              <span className="font-bold text-[#0B2545]">{s.value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
