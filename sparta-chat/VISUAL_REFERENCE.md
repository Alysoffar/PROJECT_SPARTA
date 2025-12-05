# SPARTA Mechanical Engineering Theme - Visual Reference

## Color Palette Reference

```
┌─────────────────────────────────────────────────────────────┐
│ PRIMARY COLORS                                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ████████  STEEL GRAY     #3A3F44  RGB(58, 63, 68)         │
│  Primary background, panels, buttons                        │
│                                                             │
│  ████████  MATTE BLACK    #1A1C1E  RGB(26, 28, 30)         │
│  Deep backgrounds, inputs, code blocks                      │
│                                                             │
│  ████████  ENGINEERING BLUE #3C6EAA RGB(60, 110, 170)      │
│  Borders, accents, highlights, links                        │
│                                                             │
│  ████████  BRASS/GOLD     #C8A951  RGB(200, 169, 81)       │
│  Headers, important text, captions                          │
│                                                             │
│  ████████  BORDER COLOR   #4A4F54  RGB(74, 79, 84)         │
│  Subtle borders, separators                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ STATUS COLORS                                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ████████  SUCCESS GREEN  #4CAF50  RGB(76, 175, 80)        │
│  Completed operations, successful states                    │
│                                                             │
│  ████████  ERROR RED      #F44336  RGB(244, 67, 54)        │
│  Errors, failures, critical warnings                        │
│                                                             │
│  ████████  WARNING ORANGE #FF9800  RGB(255, 152, 0)        │
│  Warnings, cautions, in-progress states                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Typography Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│ H1 - MAIN TITLE                                             │
│ Font: Orbitron 900 | Size: 28-32px | Color: Brass/Gold     │
│ SPARTA HARDWARE DESIGN WORKSTATION                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ H2 - SECTION HEADERS                                        │
│ Font: Orbitron 700 | Size: 20px | Color: Brass/Gold        │
│ DESIGN CONSOLE                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ H3 - SUBSECTION HEADERS                                     │
│ Font: Orbitron 400 | Size: 16px | Color: Brass/Gold        │
│ SYSTEM STATUS                                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ BODY TEXT                                                   │
│ Font: Roboto Mono 400 | Size: 14px | Color: #E0E0E0        │
│ Regular content text with monospace precision               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ TECHNICAL LABELS                                            │
│ Font: Roboto Mono 700 | Size: 12-14px | Color: Brass/Gold  │
│ **RESPONSE** | **WAVEFORM ANALYSIS** | **SYSTEM DIAGNOSTICS**│
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ CAPTIONS                                                    │
│ Font: Roboto Mono 400 | Size: 11px | Color: #888           │
│ GENERATED DIAGRAM | filename.png                            │
└─────────────────────────────────────────────────────────────┘
```

## Layout Structure

```
┌──────────────────────────────────────────────────────────────────────┐
│ ███████████████████████████████████████████████████████████████████  │
│ │ SPARTA HARDWARE DESIGN WORKSTATION                              │  │
│ │ MULTI-AGENT RTL GENERATION SYSTEM | VERSION 2.0                 │  │
│ ███████████████████████████████████████████████████████████████████  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ ┌────────────────────────┐ ┌──────────────────────────────────────┐ │
│ │ LEFT PANEL             │ │ RIGHT PANEL                          │ │
│ │ DESIGN CONSOLE         │ │ SYSTEM STATUS                        │ │
│ ├────────────────────────┤ ├──────────────────────────────────────┤ │
│ │                        │ │                                      │ │
│ │ ┌────────────────────┐ │ │ ┌──────────────────────────────────┐ │ │
│ │ │ USER MESSAGE       │ │ │ │ SESSION INFORMATION              │ │ │
│ │ │ (Right-aligned)    │ │ │ │ ID: xxxx-xxxx...                 │ │ │
│ │ └────────────────────┘ │ │ │ MESSAGES: 5                      │ │ │
│ │                        │ │ │ TIMESTAMP: 2025-11-28 12:00:00   │ │ │
│ │ ┌────────────────────┐ │ │ └──────────────────────────────────┘ │ │
│ │ │ ASSISTANT RESPONSE │ │ │                                      │ │
│ │ │ (Left-aligned)     │ │ │ ┌──────────────────────────────────┐ │ │
│ │ │                    │ │ │ │ DESIGN METRICS                   │ │ │
│ │ │ [DIAGRAM IMAGE]    │ │ │ │ AREA: 1.2 mm²                    │ │ │
│ │ │                    │ │ │ │ POWER: 45 mW                     │ │ │
│ │ │ [WAVEFORM]         │ │ │ │ LATENCY: 5 ns                    │ │ │
│ │ │                    │ │ │ └──────────────────────────────────┘ │ │
│ │ │ [DOWNLOADS]        │ │ │                                      │ │
│ │ └────────────────────┘ │ │ ┌──────────────────────────────────┐ │ │
│ │                        │ │ │ DESIGN TEMPLATES                 │ │ │
│ │                        │ │ │ [4-BIT RIPPLE CARRY ADDER]       │ │ │
│ │                        │ │ │ [8-BIT ALU WITH OPERATIONS]      │ │ │
│ │                        │ │ │ [TRAFFIC LIGHT FSM CONTROLLER]   │ │ │
│ └────────────────────────┘ │ │ [UART TRANSMITTER MODULE]        │ │ │
│                            │ └──────────────────────────────────┘ │ │
│ ┌────────────────────────┐ │                                      │ │
│ │ ENTER DESIGN SPEC...   │ │ ┌──────────────────────────────────┐ │ │
│ └────────────────────────┘ │ │ DESIGN ARCHIVE                   │ │ │
│                            │ │ [SEARCH FIELD]                   │ │ │
│                            │ └──────────────────────────────────┘ │ │
└────────────────────────────┴──────────────────────────────────────┘
```

## UI Element Examples

### Button States
```
┌─────────────────────────────────────────────┐
│ NORMAL STATE                                │
├─────────────────────────────────────────────┤
│  ╔═══════════════════════════════════════╗  │
│  ║  NEW SESSION                          ║  │
│  ╚═══════════════════════════════════════╝  │
│  Background: Steel Gray | Text: Brass/Gold  │
│  Border: Engineering Blue (2px)             │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ HOVER STATE                                 │
├─────────────────────────────────────────────┤
│  ╔═══════════════════════════════════════╗  │
│  ║  NEW SESSION                          ║  │
│  ╚═══════════════════════════════════════╝  │
│  Background: Engineering Blue               │
│  Text: White | Border: Brass/Gold           │
│  Glow: Blue halo effect                     │
└─────────────────────────────────────────────┘
```

### Message Boxes
```
┌─────────────────────────────────────────────┐
│ USER MESSAGE (Right-aligned)                │
├─────────────────────────────────────────────┤
│                    ┌─────────────────────┐  │
│                    │ Design a 4-bit      │  │
│                    │ ripple carry adder  │  │
│                    └─────────────────────┘  │
│  Background: Blue tint (20% opacity)        │
│  Border-left: Engineering Blue (3px)        │
│  Margin-left: 20%                           │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ ASSISTANT MESSAGE (Left-aligned)            │
├─────────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐    │
│  │ **RESPONSE**                        │    │
│  │ ───────────────────────────────     │    │
│  │ I'll create a 4-bit adder...        │    │
│  │                                     │    │
│  │ [DIAGRAM IMAGE]                     │    │
│  │                                     │    │
│  │ **AVAILABLE DOWNLOADS**             │    │
│  │ [RTL FILE] [TESTBENCH] [REPORT]     │    │
│  └─────────────────────────────────────┘    │
│  Background: Steel Gray (80% opacity)       │
│  Border-left: Brass/Gold (3px)              │
│  Margin-right: 20%                          │
└─────────────────────────────────────────────┘
```

### Image Display
```
┌─────────────────────────────────────────────┐
│ DIAGRAM IMAGE                               │
├─────────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐    │
│  │                                     │    │
│  │         [CIRCUIT DIAGRAM]           │    │
│  │                                     │    │
│  │         ┌───┐   ┌───┐              │    │
│  │    A ───┤XOR├───┤   │              │    │
│  │    B ───┤   │   │ FA├─── Sum       │    │
│  │    Cin─ └───┘   │   │              │    │
│  │                 └───┘─── Cout      │    │
│  │                                     │    │
│  └─────────────────────────────────────┘    │
│  GENERATED DIAGRAM | openai_12345.png       │
│                                             │
│  Border: Engineering Blue (2px)             │
│  Shadow: 0 4px 10px rgba(0,0,0,0.5)        │
│  Caption: Brass/Gold, 11px monospace        │
└─────────────────────────────────────────────┘
```

### Technical Panel
```
┌─────────────────────────────────────────────┐
│ TECHNICAL PANEL                             │
├─────────────────────────────────────────────┤
│  ╔═══════════════════════════════════════╗  │
│  ║ SESSION INFORMATION                   ║  │
│  ║                                       ║  │
│  ║ ID: a1b2c3d4-e5f6...                  ║  │
│  ║ MESSAGES: 12                          ║  │
│  ║ TIMESTAMP: 2025-11-28 12:00:00        ║  │
│  ╚═══════════════════════════════════════╝  │
│                                             │
│  Background: Steel Gray                     │
│  Border: Engineering Blue (2px)             │
│  Shadow: Inset 0 0 10px rgba(0,0,0,0.3)    │
└─────────────────────────────────────────────┘
```

### Status Indicators
```
┌─────────────────────────────────────────────┐
│ SUCCESS                                     │
│ ✓ Diagram: matplotlib                      │
│ Color: #4CAF50 | Font: Roboto Mono 700     │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ ERROR                                       │
│ IMAGE LOAD FAILED: path/to/image.png       │
│ Color: #F44336 | Font: Roboto Mono 700     │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ WARNING                                     │
│ Attempting reload from: http://...          │
│ Color: #FF9800 | Font: Roboto Mono 700     │
└─────────────────────────────────────────────┘
```

## Grid Background Pattern

```
Blueprint Grid (20px × 20px spacing):

····│····│····│····│····│····│····│····│····│····│
────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼
····│····│····│····│····│····│····│····│····│····│
────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼
····│····│····│····│····│····│····│····│····│····│
────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼
····│····│····│····│····│····│····│····│····│····│

Color: rgba(60, 110, 170, 0.03) - Very subtle blue
Pattern: Overlapping horizontal and vertical lines
Effect: Technical drafting table aesthetic
```

## Border Styles

```
┌─────────────────────────────────────────────┐
│ THIN SEPARATOR                              │
├─────────────────────────────────────────────┤
│ ─────────────────────────────────────────   │
│ Height: 1px | Color: Engineering Blue       │
│ Opacity: 50% | Margin: 20px 0               │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ THICK ACCENT BORDER                         │
├─────────────────────────────────────────────┤
│ ║                                            │
│ ║ Content with left accent                  │
│ ║                                            │
│ Width: 3px | Color: Engineering Blue/Gold   │
│ Style: Solid | Position: Left side          │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ PANEL BORDER                                │
├─────────────────────────────────────────────┤
│ ╔══════════════════════════════════════════╗│
│ ║ Panel content with full border           ║│
│ ╚══════════════════════════════════════════╝│
│ Width: 2px | Color: Engineering Blue        │
│ Radius: 2px (minimal) | Style: Solid        │
└─────────────────────────────────────────────┘
```

## Shadow Effects

```
┌─────────────────────────────────────────────┐
│ DROP SHADOW (Buttons, Messages)             │
│ box-shadow: 2px 2px 8px rgba(0,0,0,0.4)    │
│                                             │
│ Effect: Slight elevation, subtle depth      │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ INSET SHADOW (Panels, Inputs)               │
│ box-shadow: inset 0 0 10px rgba(0,0,0,0.3) │
│                                             │
│ Effect: Recessed appearance, depth          │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ GLOW EFFECT (Hover states)                  │
│ box-shadow: 0 0 15px rgba(60,110,170,0.5)  │
│                                             │
│ Effect: Blue halo, interactive feedback     │
└─────────────────────────────────────────────┘
```

## Quick Reference Chart

```
┌──────────────────┬──────────────────┬──────────────────┐
│ Element          │ Background       │ Border/Accent    │
├──────────────────┼──────────────────┼──────────────────┤
│ App Background   │ Matte Black      │ Blue Grid        │
│ Sidebar          │ Steel Gray       │ Blue Right       │
│ Chat Message     │ Steel Gray       │ Subtle Gray      │
│ User Message     │ Blue Tint        │ Blue Left        │
│ Assistant Msg    │ Steel Gray       │ Gold Left        │
│ Button           │ Steel Gray       │ Blue 2px         │
│ Button Hover     │ Eng. Blue        │ Gold 2px         │
│ Input Field      │ Matte Black      │ Gray 1px         │
│ Technical Panel  │ Steel Gray       │ Blue 2px         │
│ Image            │ N/A              │ Blue 2px         │
│ Code Block       │ Matte Black      │ Blue 1px         │
│ Scrollbar Thumb  │ Eng. Blue        │ Gray 1px         │
└──────────────────┴──────────────────┴──────────────────┘

┌──────────────────┬──────────────────┬──────────────────┐
│ Text Element     │ Font             │ Color            │
├──────────────────┼──────────────────┼──────────────────┤
│ H1 Title         │ Orbitron 900     │ Brass/Gold       │
│ H2 Section       │ Orbitron 700     │ Brass/Gold       │
│ H3 Subsection    │ Orbitron 400     │ Brass/Gold       │
│ Body Text        │ Roboto Mono 400  │ Light Gray       │
│ Label Bold       │ Roboto Mono 700  │ Brass/Gold       │
│ Caption          │ Roboto Mono 400  │ Dark Gray        │
│ Success          │ Roboto Mono 700  │ Green            │
│ Error            │ Roboto Mono 700  │ Red              │
│ Warning          │ Roboto Mono 700  │ Orange           │
└──────────────────┴──────────────────┴──────────────────┘
```

## Implementation Checklist

### Theme Application
- ✅ Blueprint grid background
- ✅ Orbitron font for headers
- ✅ Roboto Mono for body
- ✅ Color variables defined
- ✅ All emojis removed
- ✅ Uppercase headers
- ✅ Technical separators
- ✅ CAD-style borders
- ✅ Industrial shadows
- ✅ Custom scrollbar

### Chat Interface
- ✅ User messages right-aligned
- ✅ Assistant messages left-aligned
- ✅ Message borders styled
- ✅ Technical labels added
- ✅ Status indicators
- ✅ Image display fixed
- ✅ Image captions added
- ✅ Download links styled
- ✅ Diagnostics expandable

### Panels & Layout
- ✅ Two-column layout
- ✅ Technical panels
- ✅ Session info styled
- ✅ Metrics display
- ✅ Template buttons
- ✅ Search field
- ✅ Sidebar themed

---

**SPARTA V2.0** | MECHANICAL ENGINEERING VISUAL REFERENCE
