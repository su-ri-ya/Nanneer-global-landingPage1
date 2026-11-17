import { MetadataRoute } from "next"

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Nanneer Consultancy - Commercial STP Operations",
    short_name: "Nanneer Consultancy",
    description:
      "Complete 24×7 commercial STP operations, treated water recovery, and monthly performance reporting with absolute accountability.",
    start_url: "/",
    display: "standalone",
    background_color: "#ffffff",
    theme_color: "#0284c7",
    icons: [
      {
        src: "/favicon.ico",
        sizes: "any",
        type: "image/x-icon",
      },
      {
        src: "/logo.png",
        sizes: "192x192",
        type: "image/png",
      },
      {
        src: "/nanneer_consultancy_logo.png",
        sizes: "512x512",
        type: "image/png",
      },
    ],
  }
}
