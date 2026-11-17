import { NextResponse } from "next/server"
import nodemailer from "nodemailer"

interface ContactRequestBody {
  type?: "assessment" | "report"
  email: string
  name?: string
  buildingType?: string
  capacity?: string
  improvement?: string
  message?: string
}

export async function POST(req: Request) {
  try {
    const body: ContactRequestBody = await req.json()

    const { email, name, buildingType, capacity, improvement, message, type = "assessment" } = body

    if (!email || !email.includes("@")) {
      return NextResponse.json(
        { success: false, error: "A valid email address is required." },
        { status: 400 }
      )
    }

    const host = process.env.SMTP_HOST || "smtp.gmail.com"
    const port = Number(process.env.SMTP_PORT) || 465
    const secure = process.env.SMTP_SECURE === "true" || port === 465
    const user = process.env.SMTP_USER || ""
    const pass = process.env.SMTP_PASS || ""
    const from = process.env.SMTP_FROM || `"Nanneer Consultancy" <${user || "no-reply@nanneerconsultancy.com"}>`
    const to = process.env.CONTACT_RECIPIENT_EMAIL || "info@nanneerconsultancy.com"

    const isPlaceholder = !user || user.includes("your-email@gmail.com") || !pass || pass.includes("your-16-char")

    const subject =
      type === "report"
        ? `[STP Report Request] New Inquiry from ${name || email}`
        : `[Technical STP Assessment] New Inquiry for ${buildingType || "Commercial Facility"}`

    const htmlContent = `
      <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden;">
        <div style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); padding: 24px 28px; color: #ffffff;">
          <h2 style="margin: 0 0 6px 0; font-size: 20px; font-weight: 800; letter-spacing: -0.02em;">NANNEER CONSULTANCY</h2>
          <p style="margin: 0; font-size: 13px; opacity: 0.9;">${type === "report" ? "Confidential Sample STP Report Request" : "Technical STP Assessment Inquiry"}</p>
        </div>

        <div style="padding: 28px;">
          <div style="margin-bottom: 20px; padding: 14px 18px; background: #f0f9ff; border-left: 4px solid #0284c7; border-radius: 4px;">
            <p style="margin: 0; font-size: 14px; color: #0c4a6e; font-weight: 600;">
              New lead received from landing page contact form.
            </p>
          </div>

          <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
            ${name ? `
            <tr>
              <td style="padding: 10px 0; border-bottom: 1px solid #f1f5f9; color: #64748b; width: 150px; font-weight: 500;">Requester Name:</td>
              <td style="padding: 10px 0; border-bottom: 1px solid #f1f5f9; color: #0f172a; font-weight: 600;">${name}</td>
            </tr>` : ""}
            <tr>
              <td style="padding: 10px 0; border-bottom: 1px solid #f1f5f9; color: #64748b; width: 150px; font-weight: 500;">Work Email:</td>
              <td style="padding: 10px 0; border-bottom: 1px solid #f1f5f9; color: #0284c7; font-weight: 600;">
                <a href="mailto:${email}" style="color: #0284c7; text-decoration: none;">${email}</a>
              </td>
            </tr>
            ${buildingType ? `
            <tr>
              <td style="padding: 10px 0; border-bottom: 1px solid #f1f5f9; color: #64748b; font-weight: 500;">Facility Type:</td>
              <td style="padding: 10px 0; border-bottom: 1px solid #f1f5f9; color: #0f172a;">${buildingType}</td>
            </tr>` : ""}
            ${capacity ? `
            <tr>
              <td style="padding: 10px 0; border-bottom: 1px solid #f1f5f9; color: #64748b; font-weight: 500;">STP Capacity:</td>
              <td style="padding: 10px 0; border-bottom: 1px solid #f1f5f9; color: #0f172a;">${capacity}</td>
            </tr>` : ""}
            ${improvement ? `
            <tr>
              <td style="padding: 10px 0; border-bottom: 1px solid #f1f5f9; color: #64748b; font-weight: 500;">Priority Goal:</td>
              <td style="padding: 10px 0; border-bottom: 1px solid #f1f5f9; color: #0f172a;">${improvement}</td>
            </tr>` : ""}
            ${message ? `
            <tr>
              <td style="padding: 10px 0; border-bottom: 1px solid #f1f5f9; color: #64748b; font-weight: 500;">Details / Notes:</td>
              <td style="padding: 10px 0; border-bottom: 1px solid #f1f5f9; color: #0f172a; white-space: pre-line;">${message}</td>
            </tr>` : ""}
            <tr>
              <td style="padding: 10px 0; color: #64748b; font-weight: 500;">Received At:</td>
              <td style="padding: 10px 0; color: #64748b;">${new Date().toLocaleString()}</td>
            </tr>
          </table>
        </div>

        <div style="background: #f8fafc; padding: 16px 28px; border-top: 1px solid #e2e8f0; font-size: 12px; color: #94a3b8; text-align: center;">
          Sent automatically from Nanneer Consultancy STP Operations Portal
        </div>
      </div>
    `

    if (isPlaceholder) {
      console.warn(
        "[Contact API] SMTP credentials not configured yet in .env.local. Submission logged successfully:\n",
        { type, email, name, buildingType, capacity, improvement, message }
      )

      return NextResponse.json({
        success: true,
        message: "Inquiry received. (SMTP running in development mode - add credentials to .env.local to send live emails).",
      })
    }

    const transporter = nodemailer.createTransport({
      host,
      port,
      secure,
      auth: {
        user,
        pass,
      },
    })

    await transporter.sendMail({
      from,
      to,
      replyTo: email,
      subject,
      html: htmlContent,
    })

    return NextResponse.json({
      success: true,
      message: "Thank you! Your inquiry has been sent successfully.",
    })
  } catch (error: any) {
    console.error("[Contact API Error]:", error)
    return NextResponse.json(
      {
        success: false,
        error: error?.message || "Failed to send inquiry. Please try again later.",
      },
      { status: 500 }
    )
  }
}
