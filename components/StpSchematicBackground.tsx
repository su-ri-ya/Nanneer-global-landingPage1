"use client"

import React, { useEffect, useRef } from "react"

interface StpSchematicBackgroundProps {
  className?: string
  variant?: "hero" | "solution" | "performance" | "contact"
}

export const StpSchematicBackground: React.FC<StpSchematicBackgroundProps> = ({
  className = "",
  variant = "hero",
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext("2d")
    if (!ctx) return

    let animationFrameId: number
    let width = (canvas.width = canvas.offsetWidth)
    let height = (canvas.height = canvas.offsetHeight)

    const handleResize = () => {
      if (!canvas) return
      width = canvas.width = canvas.offsetWidth
      height = canvas.height = canvas.offsetHeight
    }

    window.addEventListener("resize", handleResize)

    // Define 3 main pipeline routes across the section background
    // Points are in normalized (0..1) coordinates
    const pipelines = [
      // Pipeline A: Top/Right loop (Influent -> Equalization -> Aeration)
      [
        { x: 0.04, y: 0.18 },
        { x: 0.28, y: 0.18 },
        { x: 0.28, y: 0.38 },
        { x: 0.52, y: 0.38 },
        { x: 0.52, y: 0.14 },
        { x: 0.94, y: 0.14 },
      ],
      // Pipeline B: Diagonal / Intermediate treatment route (Aeration -> Clarifier -> Filter)
      [
        { x: 0.08, y: 0.62 },
        { x: 0.35, y: 0.62 },
        { x: 0.35, y: 0.82 },
        { x: 0.72, y: 0.82 },
        { x: 0.72, y: 0.60 },
        { x: 0.96, y: 0.60 },
      ],
      // Pipeline C: Low return loop (Sludge Return / Recirculation)
      [
        { x: 0.15, y: 0.88 },
        { x: 0.88, y: 0.88 },
        { x: 0.88, y: 0.40 },
      ],
    ]

    // Animated water droplet packets
    const packets = [
      { pipeIndex: 0, progress: 0.05, speed: 0.0007, size: 3.5, color: "#0EA5E9" },
      { pipeIndex: 0, progress: 0.42, speed: 0.0006, size: 3.0, color: "#38BDF8" },
      { pipeIndex: 0, progress: 0.78, speed: 0.0008, size: 3.2, color: "#0284C7" },
      { pipeIndex: 1, progress: 0.15, speed: 0.00065, size: 3.5, color: "#0EA5E9" },
      { pipeIndex: 1, progress: 0.55, speed: 0.0007, size: 3.0, color: "#06B6D4" },
      { pipeIndex: 1, progress: 0.85, speed: 0.0006, size: 3.2, color: "#38BDF8" },
      { pipeIndex: 2, progress: 0.30, speed: 0.0005, size: 2.8, color: "#0284C7" },
      { pipeIndex: 2, progress: 0.70, speed: 0.00055, size: 3.0, color: "#0EA5E9" },
    ]

    // Helper to interpolate along a segmented polyline
    const getPointAtProgress = (
      points: { x: number; y: number }[],
      progress: number
    ) => {
      if (points.length < 2) return { x: 0, y: 0 }
      const totalSegments = points.length - 1
      const scaledProgress = Math.max(0, Math.min(1, progress)) * totalSegments
      const segmentIndex = Math.min(Math.floor(scaledProgress), totalSegments - 1)
      const segmentT = scaledProgress - segmentIndex

      const p0 = points[segmentIndex]
      const p1 = points[segmentIndex + 1]

      return {
        x: (p0.x + (p1.x - p0.x) * segmentT) * width,
        y: (p0.y + (p1.y - p0.y) * segmentT) * height,
      }
    }

    let frame = 0

    const render = () => {
      frame++
      ctx.clearRect(0, 0, width, height)

      // 1. Draw static schematic conduit pipes
      pipelines.forEach((pipe, pIdx) => {
        if (pipe.length < 2) return

        // Pipe outer halo
        ctx.beginPath()
        ctx.moveTo(pipe[0].x * width, pipe[0].y * height)
        for (let i = 1; i < pipe.length; i++) {
          ctx.lineTo(pipe[i].x * width, pipe[i].y * height)
        }
        ctx.strokeStyle = "rgba(14, 165, 233, 0.12)"
        ctx.lineWidth = 4
        ctx.stroke()

        // Pipe inner core line with subtle dashed flow cadence
        ctx.beginPath()
        ctx.moveTo(pipe[0].x * width, pipe[0].y * height)
        for (let i = 1; i < pipe.length; i++) {
          ctx.lineTo(pipe[i].x * width, pipe[i].y * height)
        }
        ctx.strokeStyle = "rgba(2, 132, 199, 0.28)"
        ctx.lineWidth = 1.2
        ctx.setLineDash([8, 12])
        ctx.lineDashOffset = -frame * 0.4
        ctx.stroke()
        ctx.setLineDash([])

        // Draw joint nodes at corners
        pipe.forEach((pt, idx) => {
          const px = pt.x * width
          const py = pt.y * height

          // Outer ring
          ctx.beginPath()
          ctx.arc(px, py, 4.5, 0, Math.PI * 2)
          ctx.fillStyle = "#FFFFFF"
          ctx.fill()
          ctx.strokeStyle = "rgba(14, 165, 233, 0.4)"
          ctx.lineWidth = 1.2
          ctx.stroke()

          // Inner pin
          ctx.beginPath()
          ctx.arc(px, py, 2, 0, Math.PI * 2)
          ctx.fillStyle = idx === 0 || idx === pipe.length - 1 ? "#0284C7" : "#0EA5E9"
          ctx.fill()
        })
      })

      // 2. Draw animated moving water packets
      packets.forEach((packet) => {
        packet.progress += packet.speed
        if (packet.progress > 1) packet.progress = 0

        const pt = getPointAtProgress(pipelines[packet.pipeIndex], packet.progress)

        // Droplet glow
        const gradient = ctx.createRadialGradient(
          pt.x,
          pt.y,
          0,
          pt.x,
          pt.y,
          packet.size * 2.5
        )
        gradient.addColorStop(0, packet.color)
        gradient.addColorStop(1, "rgba(14, 165, 233, 0)")

        ctx.beginPath()
        ctx.arc(pt.x, pt.y, packet.size * 2.5, 0, Math.PI * 2)
        ctx.fillStyle = gradient
        ctx.fill()

        // Solid core
        ctx.beginPath()
        ctx.arc(pt.x, pt.y, packet.size, 0, Math.PI * 2)
        ctx.fillStyle = "#FFFFFF"
        ctx.fill()
        ctx.strokeStyle = packet.color
        ctx.lineWidth = 1.5
        ctx.stroke()
      })

      animationFrameId = requestAnimationFrame(render)
    }

    render()

    return () => {
      window.removeEventListener("resize", handleResize)
      cancelAnimationFrame(animationFrameId)
    }
  }, [variant])

  return (
    <div
      aria-hidden="true"
      className={`absolute inset-0 pointer-events-none select-none overflow-hidden z-0 ${className}`}
    >
      {/* Dynamic Animated Canvas Pipes & Flow Droplets */}
      <canvas
        ref={canvasRef}
        className="w-full h-full block opacity-60 lg:opacity-75 transition-opacity duration-1000"
      />

      {/* Engineering Schematic HUD Badges in periphery */}
      <div className="absolute top-4 left-6 hidden xl:flex items-center gap-2 px-2.5 py-1 rounded bg-white/70 backdrop-blur-xs border border-sky-200/60 shadow-2xs">
        <span className="w-1.5 h-1.5 rounded-full bg-sky-500 animate-pulse" />
        <span className="text-[9px] font-mono font-bold tracking-wider text-sky-800 uppercase">
          STP FLOW CIRCUIT // ACTIVE PROCESS
        </span>
      </div>

      <div className="absolute bottom-4 right-8 hidden xl:flex items-center gap-3 px-3 py-1 rounded bg-white/70 backdrop-blur-xs border border-sky-200/60 shadow-2xs text-[9px] font-mono text-slate-600">
        <div className="flex items-center gap-1.5">
          <span className="text-slate-400">EQ-01:</span>
          <span className="text-sky-700 font-bold">120 m³/d</span>
        </div>
        <span className="text-sky-300">|</span>
        <div className="flex items-center gap-1.5">
          <span className="text-slate-400">AER-02 (DO):</span>
          <span className="text-emerald-600 font-bold">2.4 mg/L</span>
        </div>
        <span className="text-sky-300">|</span>
        <div className="flex items-center gap-1.5">
          <span className="text-slate-400">RECOVERY:</span>
          <span className="text-sky-700 font-bold">98.4%</span>
        </div>
      </div>
    </div>
  )
}
