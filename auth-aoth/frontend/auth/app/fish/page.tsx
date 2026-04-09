'use client'

import { useEffect, useRef } from 'react'

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
type Pt = [number, number]

function normalize(dx: number, dy: number): Pt {
  const l = Math.sqrt(dx * dx + dy * dy) || 1
  return [dx / l, dy / l]
}

// Body half-width profile.  t = 0 → head tip, t = 1 → tail base
function halfWidth(t: number): number {
  if (t < 0.08) return (t / 0.08) * 11              // snout narrows to a gentle point
  if (t > 0.86) return ((1 - t) / 0.14) * 14        // peduncle narrows before tail
  return 11 + 28 * Math.pow(Math.sin(Math.PI * Math.pow((t - 0.08) / 0.92, 0.60)), 1.05)
}

// ---------------------------------------------------------------------------
// Main drawing routine
// ---------------------------------------------------------------------------
function drawKoi(ctx: CanvasRenderingContext2D, W: number, H: number, time: number) {
  // ── background ──────────────────────────────────────────────────────────
  const bg = ctx.createRadialGradient(W / 2, H / 2, 40, W / 2, H / 2, W * 0.75)
  bg.addColorStop(0, '#1e6652')
  bg.addColorStop(0.5, '#14503e')
  bg.addColorStop(1, '#0a3028')
  ctx.fillStyle = bg
  ctx.fillRect(0, 0, W, H)

  // subtle ripple lines
  ctx.save()
  ctx.globalAlpha = 0.06
  ctx.strokeStyle = '#5af0c0'
  ctx.lineWidth = 1.2
  for (let r = 60; r < Math.max(W, H) * 0.9; r += 60) {
    const phase = (time * 0.4 + r * 0.02) % (Math.PI * 2)
    const dynamicR = r + Math.sin(phase) * 8
    ctx.beginPath()
    ctx.ellipse(W / 2, H / 2, dynamicR, dynamicR * 0.55, 0, 0, Math.PI * 2)
    ctx.stroke()
  }
  ctx.restore()

  // ── spine ────────────────────────────────────────────────────────────────
  const cx = W / 2
  const cy = H / 2
  const FISH_LEN = Math.min(W * 0.55, 260)
  const N = 48  // spine segments

  // t=0 → head (right side), t=1 → tail base (left side)
  const spine: Pt[] = []
  for (let i = 0; i <= N; i++) {
    const t = i / N
    const baseX = cx + (0.5 - t) * FISH_LEN
    // amplitude envelope: zero at head, grows toward tail
    const amp = Math.pow(t, 1.6) * 32
    const waveY = Math.sin(t * 7.5 - time * 2.8) * amp
    spine.push([baseX, cy + waveY])
  }

  // pre-compute normals at each spine point
  const normals: Pt[] = spine.map((_, i) => {
    let dx: number, dy: number
    if (i === 0) { dx = spine[1][0] - spine[0][0]; dy = spine[1][1] - spine[0][1] }
    else if (i === N) { dx = spine[N][0] - spine[N - 1][0]; dy = spine[N][1] - spine[N - 1][1] }
    else { dx = spine[i + 1][0] - spine[i - 1][0]; dy = spine[i + 1][1] - spine[i - 1][1] }
    const [tx, ty] = normalize(dx, dy)
    return [-ty, tx]   // perpendicular
  })

  // body outline
  const topEdge: Pt[] = []
  const botEdge: Pt[] = []
  for (let i = 0; i <= N; i++) {
    const [px, py] = spine[i]
    const [nx, ny] = normals[i]
    const w = halfWidth(i / N)
    topEdge.push([px + nx * w, py + ny * w])
    botEdge.push([px - nx * w, py - ny * w])
  }

  // helper: world coord of a fish-local point (t along spine, frac of halfWidth laterally)
  function fishLocal(t: number, lateralFrac: number): Pt {
    const idx = Math.min(Math.floor(t * N), N)
    const [px, py] = spine[idx]
    const [nx, ny] = normals[idx]
    const w = halfWidth(t)
    return [px + nx * w * lateralFrac, py + ny * w * lateralFrac]
  }

  // ── tail fin ─────────────────────────────────────────────────────────────
  const tailIdx = N
  const [tx_tail, ty_tail] = (() => {
    const [x1, y1] = spine[N]
    const [x0, y0] = spine[N - 2]
    return normalize(x1 - x0, y1 - y0)
  })()
  const [nx_tail, ny_tail] = [-ty_tail, tx_tail]

  const [tp0x, tp0y] = topEdge[N]
  const [bp0x, bp0y] = botEdge[N]
  const spread = 36
  const tailReach = FISH_LEN * 0.23
  const tailWobble = Math.sin(time * 2.8 + 7.0) * 10

  function drawTailLobe(sign: number) {
    const [sx, sy] = sign > 0 ? [tp0x, tp0y] : [bp0x, bp0y]
    ctx.beginPath()
    ctx.moveTo(sx, sy)
    ctx.bezierCurveTo(
      sx + tx_tail * tailReach * 0.4 + nx_tail * sign * spread * 0.5,
      sy + ty_tail * tailReach * 0.4 + ny_tail * sign * spread * 0.5,
      sx + tx_tail * tailReach + nx_tail * sign * (spread + tailWobble),
      sy + ty_tail * tailReach + ny_tail * sign * (spread + tailWobble),
      sx + tx_tail * tailReach * 1.15,
      sy + ty_tail * tailReach * 1.15
    )
    ctx.bezierCurveTo(
      sx + tx_tail * tailReach + nx_tail * sign * (spread * 0.3 + tailWobble * 0.5),
      sy + ty_tail * tailReach + ny_tail * sign * (spread * 0.3 + tailWobble * 0.5),
      sx + tx_tail * tailReach * 0.4,
      sy + ty_tail * tailReach * 0.4,
      sx, sy
    )
    ctx.closePath()
    const g = ctx.createLinearGradient(sx, sy, sx + tx_tail * tailReach * 1.15, sy + ty_tail * tailReach * 1.15)
    g.addColorStop(0, 'rgba(210,205,230,0.9)')
    g.addColorStop(1, 'rgba(175,168,200,0.5)')
    ctx.fillStyle = g
    ctx.fill()
    ctx.strokeStyle = 'rgba(140,132,160,0.4)'
    ctx.lineWidth = 0.8
    ctx.stroke()
  }

  ctx.save()
  drawTailLobe(1)
  drawTailLobe(-1)
  ctx.restore()

  // ── pectoral fins ─────────────────────────────────────────────────────────
  ctx.save()
  for (const sign of [1, -1] as const) {
    const edge = sign > 0 ? topEdge : botEdge

    const rootIdx  = Math.round(0.19 * N)
    const trailIdx = Math.round(0.34 * N)
    const [rx, ry]         = edge[rootIdx]
    const [trailX, trailY] = edge[trailIdx]

    // outward direction (perpendicular to spine, away from center)
    const [nx, ny] = normals[rootIdx]
    const outX = nx * sign, outY = ny * sign
    // forward tangent toward tail: normal = [-ty, tx] → tx = ny, ty = -nx
    const fwdX = ny, fwdY = -nx

    // fin tip: spread outward and slightly toward tail, with gentle wag
    const wag = Math.sin(time * 2.8 + (sign < 0 ? Math.PI : 0)) * 5
    const tipX = rx + outX * 48 + fwdX * 18 + outX * wag * 0.3
    const tipY = ry + outY * 48 + fwdY * 18 + outY * wag * 0.3

    ctx.beginPath()
    ctx.moveTo(rx, ry)
    // leading edge: arcs outward curving slightly toward head, then sweeps to tip
    ctx.bezierCurveTo(
      rx + outX * 20 - fwdX * 10,  ry + outY * 20 - fwdY * 10,
      tipX - fwdX * 16,             tipY - fwdY * 16,
      tipX, tipY
    )
    // trailing edge: tip swings toward tail then back to body
    ctx.bezierCurveTo(
      tipX + fwdX * 22,   tipY + fwdY * 22,
      trailX + outX * 20, trailY + outY * 20,
      trailX, trailY
    )
    // close along body edge from trail back to root
    for (let i = trailIdx - 1; i > rootIdx; i--) ctx.lineTo(edge[i][0], edge[i][1])
    ctx.closePath()

    const g = ctx.createLinearGradient(rx, ry, tipX, tipY)
    g.addColorStop(0,    'rgba(200, 210, 240, 0.90)')
    g.addColorStop(0.55, 'rgba(180, 195, 228, 0.65)')
    g.addColorStop(1,    'rgba(160, 176, 215, 0.38)')
    ctx.fillStyle = g
    ctx.fill()
    ctx.strokeStyle = 'rgba(140, 158, 200, 0.42)'
    ctx.lineWidth = 0.9
    ctx.stroke()

    // fin rays — lines from root-area toward outer edge
    ctx.save()
    ctx.strokeStyle = 'rgba(130, 150, 196, 0.52)'
    ctx.lineWidth = 0.65
    for (let r = 0; r < 7; r++) {
      const f = r / 6
      const rayRootX = rx + (trailX - rx) * f * 0.28
      const rayRootY = ry + (trailY - ry) * f * 0.28
      const rayEndX  = tipX + (trailX - tipX) * f * 0.55
      const rayEndY  = tipY + (trailY - tipY) * f * 0.55
      ctx.beginPath()
      ctx.moveTo(rayRootX, rayRootY)
      ctx.lineTo(rayEndX, rayEndY)
      ctx.stroke()
    }
    ctx.restore()
  }
  ctx.restore()

  // ── body fill (clipped path) ──────────────────────────────────────────────
  ctx.save()
  ctx.beginPath()

  // smooth catmull-rom through top edge
  ctx.moveTo(topEdge[0][0], topEdge[0][1])
  for (let i = 1; i <= N; i++) {
    const [ax, ay] = topEdge[i - 1]
    const [bx, by] = topEdge[i]
    ctx.quadraticCurveTo(ax, ay, (ax + bx) / 2, (ay + by) / 2)
  }
  ctx.lineTo(topEdge[N][0], topEdge[N][1])
  ctx.lineTo(botEdge[N][0], botEdge[N][1])
  for (let i = N - 1; i >= 0; i--) {
    const [ax, ay] = botEdge[i + 1]
    const [bx, by] = botEdge[i]
    ctx.quadraticCurveTo(ax, ay, (ax + bx) / 2, (ay + by) / 2)
  }
  ctx.lineTo(botEdge[0][0], botEdge[0][1])
  ctx.closePath()

  // pearlescent white body
  const bodyGrad = ctx.createLinearGradient(
    cx + FISH_LEN / 2, cy - 40,
    cx - FISH_LEN * 0.1, cy + 40
  )
  bodyGrad.addColorStop(0, '#d8d2c0')
  bodyGrad.addColorStop(0.25, '#f4f0e4')
  bodyGrad.addColorStop(0.6, '#faf7f0')
  bodyGrad.addColorStop(1, '#e8e2d4')
  ctx.fillStyle = bodyGrad
  ctx.fill()
  ctx.strokeStyle = '#ccc4b0'
  ctx.lineWidth = 1.2
  ctx.stroke()
  ctx.restore()

  // ── spots (black / dark patches in fish-local coords) ─────────────────────
  // Each spot: [spineT, lateralFrac, radiusX, radiusY, angle, color]
  const spots: [number, number, number, number, number, string][] = [
    [0.22, 0.1, 18, 14, 0.3, '#1a1a1a'],    // large dorsal spot near head
    [0.38, 0.3, 15, 12, -0.4, '#1c1c1c'],
    [0.38, -0.4, 12, 10, 0.2, '#1c1c1c'],
    [0.55, 0.15, 20, 16, 0.1, '#181818'],   // big mid-body spot
    [0.55, -0.35, 13, 11, -0.2, '#1a1a1a'],
    [0.70, 0.3, 11, 9, 0.5, '#1e1e1e'],
    [0.78, -0.1, 9, 7, -0.3, '#202020'],
    [0.86, 0.2, 8, 6, 0.0, '#1e1e1e'],
  ]

  ctx.save()
  for (const [st, lf, rx, ry, angle, color] of spots) {
    const [wx, wy] = fishLocal(st, lf)
    // get the local tangent angle so the spot rotates with the fish body
    const idx = Math.min(Math.round(st * N), N - 1)
    let tang = 0
    if (idx < N) {
      const [x1, y1] = spine[idx + 1]
      const [x0, y0] = spine[idx]
      tang = Math.atan2(y1 - y0, x1 - x0)
    }
    ctx.beginPath()
    ctx.ellipse(wx, wy, rx, ry, tang + angle, 0, Math.PI * 2)
    ctx.fillStyle = color
    ctx.globalAlpha = 0.88
    ctx.fill()
  }
  ctx.globalAlpha = 1
  ctx.restore()

  // ── dorsal fin ridge (thin translucent strip along back) ──────────────────
  ctx.save()
  ctx.beginPath()
  const dorsalStart = 0.12, dorsalEnd = 0.72
  let first = true
  for (let i = 0; i <= N; i++) {
    const t = i / N
    if (t < dorsalStart || t > dorsalEnd) continue
    const env = Math.sin(Math.PI * (t - dorsalStart) / (dorsalEnd - dorsalStart))
    const [px, py] = spine[i]
    const [nx, ny] = normals[i]
    const dorsalH = env * 7 + 1
    const dx = px + nx * dorsalH
    const dy = py + ny * dorsalH
    if (first) { ctx.moveTo(dx, dy); first = false }
    else ctx.lineTo(dx, dy)
  }
  for (let i = Math.floor(dorsalEnd * N); i >= Math.ceil(dorsalStart * N); i--) {
    const [px, py] = topEdge[i]
    ctx.lineTo(px, py)
  }
  ctx.closePath()
  ctx.fillStyle = 'rgba(180,170,155,0.30)'
  ctx.fill()
  ctx.restore()

  // ── scales texture (light semicircle arcs) ────────────────────────────────
  ctx.save()
  ctx.globalAlpha = 0.09
  ctx.strokeStyle = '#a09080'
  ctx.lineWidth = 0.7
  for (let row = 0; row < 5; row++) {
    for (let col = 0; col < 9; col++) {
      const t = 0.08 + col * 0.1
      const lf = -0.75 + row * 0.38
      if (Math.abs(lf) > 0.85) continue
      const [wx, wy] = fishLocal(t, lf)
      const idx = Math.min(Math.round(t * N), N - 1)
      const tang = idx < N
        ? Math.atan2(spine[idx + 1][1] - spine[idx][1], spine[idx + 1][0] - spine[idx][0])
        : 0
      ctx.beginPath()
      ctx.arc(wx, wy, 8, tang, tang + Math.PI)
      ctx.stroke()
    }
  }
  ctx.globalAlpha = 1
  ctx.restore()

  // ── eye ───────────────────────────────────────────────────────────────────
  // t=0.12 puts eyes on the widened head; lateral 0.78 pushes them to the outer edge
  for (const sign of [1, -1] as const) {
    const [ex, ey] = fishLocal(0.12, sign * 0.78)
    // dark iris ring
    ctx.beginPath()
    ctx.arc(ex, ey, 5.8, 0, Math.PI * 2)
    ctx.fillStyle = '#2a2a2a'
    ctx.fill()
    // white sclera
    ctx.beginPath()
    ctx.arc(ex, ey, 5.0, 0, Math.PI * 2)
    ctx.fillStyle = '#e8e4dc'
    ctx.fill()
    // pupil
    ctx.beginPath()
    ctx.arc(ex, ey, 3.0, 0, Math.PI * 2)
    ctx.fillStyle = '#0a0a0a'
    ctx.fill()
    // specular highlight
    ctx.beginPath()
    ctx.arc(ex - 1.2, ey - 1.2, 1.1, 0, Math.PI * 2)
    ctx.fillStyle = 'rgba(255,255,255,0.82)'
    ctx.fill()
  }

  // ── barbels (whiskers) ────────────────────────────────────────────────────
  ctx.save()
  ctx.strokeStyle = '#b0a888'
  ctx.lineWidth = 1.0
  ctx.lineCap = 'round'
  // head-forward unit vector: from spine[1] toward spine[0] (toward mouth)
  const [hfRawX, hfRawY] = normalize(spine[0][0] - spine[1][0], spine[0][1] - spine[1][1])
  for (const sign of [1, -1] as const) {
    // two barbels per side: inner (0.42) and outer (0.74)
    for (const lat of [0.42, 0.74] as const) {
      const [bx, by] = fishLocal(0.025, sign * lat)
      const wiggle = Math.sin(time * 2.5 + sign * lat * 2) * 5
      ctx.beginPath()
      ctx.moveTo(bx, by)
      ctx.bezierCurveTo(
        bx + hfRawX * 12 + wiggle * 0.3,           by + hfRawY * 12 + wiggle * 0.2,
        bx + hfRawX * 22 + sign * 4 + wiggle * 0.7, by + hfRawY * 22 + sign * 3,
        bx + hfRawX * 30 + sign * 6 + wiggle,       by + hfRawY * 30 + sign * 5
      )
      ctx.stroke()
    }
  }
  ctx.restore()

  // ── water shimmer overlay ─────────────────────────────────────────────────
  ctx.save()
  ctx.globalAlpha = 0.04
  for (let i = 0; i < 4; i++) {
    const shimX = W * 0.2 + i * W * 0.2 + Math.sin(time * 0.7 + i) * 20
    const shimY = H * 0.15 + Math.cos(time * 0.5 + i * 1.3) * 30
    const shim = ctx.createRadialGradient(shimX, shimY, 0, shimX, shimY, 80)
    shim.addColorStop(0, '#ffffff')
    shim.addColorStop(1, 'transparent')
    ctx.fillStyle = shim
    ctx.fillRect(0, 0, W, H)
  }
  ctx.restore()
}

// ---------------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------------
export default function FishPage() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Retina / HiDPI
    const dpr = window.devicePixelRatio || 1
    const W = 700, H = 480
    canvas.width = W * dpr
    canvas.height = H * dpr
    canvas.style.width = `${W}px`
    canvas.style.height = `${H}px`
    ctx.scale(dpr, dpr)

    let animId: number
    let start: number | null = null

    function frame(ts: number) {
      if (!start) start = ts
      const t = (ts - start) / 1000  // seconds
      drawKoi(ctx!, W, H, t)
      animId = requestAnimationFrame(frame)
    }

    animId = requestAnimationFrame(frame)
    return () => cancelAnimationFrame(animId)
  }, [])

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#0a3028',
        gap: '20px',
      }}
    >
      <canvas
        ref={canvasRef}
        style={{
          borderRadius: '20px',
          boxShadow: '0 0 60px rgba(30,180,120,0.18), 0 0 120px rgba(0,0,0,0.6)',
        }}
      />
      <p
        style={{
          color: 'rgba(160,220,190,0.5)',
          fontFamily: 'serif',
          fontSize: '14px',
          letterSpacing: '0.15em',
        }}
      >
        koi
      </p>
    </div>
  )
}
