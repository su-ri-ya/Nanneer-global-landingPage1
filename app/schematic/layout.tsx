import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Interactive STP SCADA Schematic & 2.5D Digital Twin Simulation",
  description:
    "Explore the interactive SCADA process schematic simulation by Nanneer Consultancy. Models 2.5D glassmorphic tanks, MBBR biological treatment, conical hopper clarifier, and tertiary media pressure vessels in real time.",
  alternates: {
    canonical: "https://nanneerconsultancy.com/schematic",
  },
  openGraph: {
    title: "Interactive STP SCADA Schematic & 2.5D Digital Twin | Nanneer Consultancy",
    description:
      "Real-time interactive SCADA mimic modeling commercial wastewater treatment, secondary clarification, and tertiary media filtration.",
    url: "https://nanneerconsultancy.com/schematic",
  },
}

export default function SchematicLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return <>{children}</>
}
