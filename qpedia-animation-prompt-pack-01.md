# QPedia Animation Prompt Pack 01

## Purpose
A reusable prompt system for generating **self-contained HTML educational animations** for QPedia's core quantum topics.

This pack is designed for:
- full-width article embeds
- responsive desktop/mobile behavior
- dark, clean scientific visual style
- seamless looping animations
- English-only labels inside the animation
- easy Persian caption overlay added later by the site owner

---

## 1) Recommended responsive block spec

### HTML wrapper
```html
<section class="qpedia-anim-block">
  <div class="qpedia-anim-stage" role="img" aria-label="Educational animation about TOPIC_NAME">
    <!-- self-contained animation HTML/SVG/JS goes here -->
  </div>
</section>
```

### CSS wrapper
```css
.qpedia-anim-block {
  width: 100%;
  margin: clamp(20px, 4vw, 40px) 0;
}

.qpedia-anim-stage {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  min-height: 300px;
  background: linear-gradient(180deg, #0B1020 0%, #0F172A 100%);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.28);
}

.qpedia-anim-stage > svg,
.qpedia-anim-stage > canvas,
.qpedia-anim-stage > div {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
}

@media (max-width: 768px) {
  .qpedia-anim-stage {
    aspect-ratio: 4 / 5;
    min-height: 360px;
    border-radius: 18px;
  }
}
```

### Layout rules for the animation generator
- Use **SVG** as the main rendering layer whenever possible.
- Use a desktop scene based on `viewBox="0 0 1600 900"`.
- Keep all critical moving elements inside a safe area:
  - desktop safe area: `x=160..1440`, `y=120..780`
- Include a **mobile reflow** using CSS media queries for screens below `768px`.
- Do **not** rely on cropping for responsiveness.
- On mobile, re-position groups vertically rather than shrinking them until they become unreadable.
- Use `preserveAspectRatio="xMidYMid meet"` for SVG scenes unless the prompt explicitly asks otherwise.
- Keep important objects away from the extreme left/right/bottom edges.
- Animation should loop seamlessly in **6 to 8 seconds**.
- Motion should be smooth, slow, and readable.
- Avoid fast flicker, strobe, or chaotic particle storms.

---

## 2) Brand overlay recommendation
Use a subtle HTML overlay added after generation, not baked into the scene.

### Suggested overlay
```html
<div class="qpedia-badge">qpedia.ir</div>
```

```css
.qpedia-badge {
  position: absolute;
  right: 14px;
  bottom: 14px;
  z-index: 20;
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(11, 16, 32, 0.72);
  border: 1px solid rgba(255,255,255,0.12);
  color: #E5E7EB;
  font: 600 12px/1 Inter, Segoe UI, Arial, sans-serif;
  letter-spacing: 0.04em;
  backdrop-filter: blur(8px);
}
```

Why this works:
- elegant and non-spammy
- hard to remove casually without re-editing
- does not damage the educational scene
- reusable across all animations

---

## 3) Master base prompt for HTML animation generation

Copy this entire prompt, then append one topic module from section 4.

```text
Generate a single self-contained HTML file with inline CSS and inline JavaScript only. Do not use external libraries, CDNs, fonts, images, videos, or APIs. Build a premium educational scientific animation for a quantum-physics article.

Technical requirements:
- full-width responsive layout
- outer container width: 100%
- desktop stage aspect ratio: 16:9
- mobile stage aspect ratio: 4:5
- include CSS media queries so the composition reflows on screens below 768px instead of being cropped
- use SVG as the primary rendering method whenever possible
- if text labels are used, render them as real SVG or HTML text, not raster text
- English labels only, no Persian, no Arabic, no paragraphs
- maximum 1 to 4 short labels only when necessary
- seamless loop duration: 6 to 8 seconds
- smooth gentle motion, low visual noise, readable educational pacing
- keep all important motion inside a central safe area and away from the edges
- optimized for article embedding, lightweight, clean, and stable on mobile browsers

Visual direction:
- dark scientific editorial style
- background colors based on #0B1020 and #0F172A
- accent colors from #62F0FF, #8B5CF6, #22C55E, #F59E0B, #E5E7EB
- subtle glow, precise line work, modern lab aesthetic, clean depth
- no photoreal humans unless specifically requested
- no stock-photo look
- no clutter
- no comic style
- no fantasy magic look
- no watermark
- no logo
- no random letters
- no fake UI chrome

Composition rules:
- single-concept educational scene only
- do not split the screen into comparisons unless explicitly requested
- prioritize concept clarity over decoration
- use one main focal idea and at most two supporting animated behaviors
- if the topic benefits from labels, keep them minimal and scientifically correct
- reserve visual calm areas so a Persian caption can be added later outside the generated scene if needed

Output rules:
- return only one complete HTML document
- include comments marking the main scene groups
- name animation groups clearly in code
- make the loop restart cleanly with no jump
```

---

## 4) Topic modules
Append one of the following modules to the master base prompt.

### 01) Photon
```text
Topic: Photon.
Create a clean educational animation showing a single photon as a quantum of light moving through space while also hinting at wave behavior. The scene should show a narrow luminous packet traveling along a path, with a subtle oscillatory field envelope around it and a soft detector response at the destination. The animation must avoid making the photon look like a tiny classical marble. Emphasize quantum light, propagation, and measurement. Optional short labels: Photon, Wave packet, Detector.
```

### 02) Electron
```text
Topic: Electron.
Create a dark elegant atomic-scale animation showing an electron as a quantum object associated with a nucleus and a probability cloud, not a little planet orbiting in a fixed classical ring. Use a softly moving density cloud, a nucleus glow, and a subtle spin cue. The story should communicate that the electron is described by a quantum state distribution rather than a simple hard particle on a circular track. Optional short labels: Electron, Probability cloud, Spin.
```

### 03) Pauli Exclusion Principle
```text
Topic: Pauli Exclusion Principle.
Create an educational animation showing two electrons associated with the same orbital region but with opposite spin, while a third identical-state occupancy attempt is visibly rejected or fades out. The animation should make the exclusion rule intuitive without becoming cartoonish. Focus on occupancy structure, spin opposition, and quantum state uniqueness. Optional short labels: Orbital, Spin up, Spin down.
```

### 04) Quantum Number
```text
Topic: Quantum Number.
Create a precise educational animation showing how quantum numbers act like an address system for electron states. Use a stylized atom with shell level transitions, orbital shapes, orientation cues, and a spin indicator that highlights different state descriptors one after another. Avoid crowded text. The viewer should feel that quantum numbers specify where and how a quantum state belongs. Optional short labels: n, l, m, s.
```

### 05) Complementarity Principle
```text
Topic: Complementarity Principle.
Create a single-scene educational animation inspired by a double-slit experiment where the setup can smoothly shift between an interference-dominant view and a path-information-dominant view without turning into a messy split-screen comparison. The idea is that two valid descriptions reveal different aspects of one quantum system. Use one apparatus that changes observational mode over time. Optional short labels: Interference, Path information.
```

### 06) Observer in Quantum Physics
```text
Topic: Observer in quantum physics.
Create a scientific animation showing that observation means physical interaction or measurement, not mystical human consciousness. Use a quantum source, a detector apparatus, and a visible change in the measured outcome when the apparatus engages. The animation should make measurement interaction central. Avoid human faces or spiritual imagery. Optional short labels: System, Detector, Measurement.
```

### 07) Heisenberg Uncertainty Principle
```text
Topic: Heisenberg Uncertainty Principle.
Create an elegant animation of a quantum wavepacket where tighter position localization leads to broader momentum spread, then the reverse, in a continuous readable loop. Use one central wavepacket and a paired abstract distribution cue so the tradeoff becomes intuitive. The scene must feel rigorous and calm, not dramatic. Optional short labels: Position, Momentum, Uncertainty.
```

### 08) Quantum State
```text
Topic: Quantum State.
Create a refined abstract animation showing a quantum state as a full mathematical description of a system. Use a state vector, amplitude layers, evolving probability structure, and a clean abstract state space. The viewer should understand that the state is richer than a hidden classical value. Avoid dense equations. Optional short labels: State vector, Amplitude, Basis.
```

### 09) Hilbert Space
```text
Topic: Hilbert Space.
Create a sophisticated but readable animation of a multidimensional abstract vector space where a highlighted state vector rotates or transforms relative to basis directions. The visual should convey that Hilbert space is the mathematical stage where quantum states live. Keep it elegant and geometric rather than overloaded with formulas. Optional short labels: Hilbert space, Basis, State vector.
```

### 10) Operator
```text
Topic: Operator.
Create an educational animation showing a linear operator acting on a state and transforming it into another state. Use a before-state, transformation field, and after-state inside an abstract mathematical scene. The emphasis should be on action, transformation, and rule-based change. Keep the motion subtle and precise. Optional short labels: Operator, Input state, Output state.
```

### 11) Quantum Computer
```text
Topic: Quantum Computer.
Create a premium technology-style educational animation showing a realistic but clean quantum processor environment with qubits, control lines, and coherent interactions inside a cryogenic or lab-inspired setting. Emphasize that this is a specialized computational machine, not a magical replacement for all computers. Motion should focus on qubit coordination and controlled computation. Optional short labels: Qubit, Gate, Readout.
```

### 12) Quantum Key Distribution
```text
Topic: Quantum Key Distribution.
Create a security-focused educational animation showing two distant communication endpoints exchanging single-photon states across an optical channel. A subtle interception attempt should disturb the transmission statistics or visual regularity. The scene should show security through physics and detectability of eavesdropping. Keep it elegant and minimal. Optional short labels: Alice, Bob, Photon channel, Eavesdropper.
```

### 13) Quantum Gate
```text
Topic: Quantum Gate.
Create a diagrammatic educational animation showing quantum gates acting on qubits, including a single-qubit rotation and one controlled two-qubit interaction. Use circuit logic aesthetics mixed with spatial quantum motion. The viewer should understand gates as the operational alphabet of quantum computation. Avoid cluttered circuit diagrams. Optional short labels: H, X, CNOT, Qubit.
```

### 14) No-Cloning Theorem
```text
Topic: No-Cloning Theorem.
Create an educational animation showing an unknown quantum state approaching a conceptual copying process that fails. One original state remains meaningful while attempted duplicates either decohere, diverge, or visibly fail to match. Make the impossibility intuitive without using comic effects. Emphasize that arbitrary unknown quantum states cannot be perfectly copied. Optional short labels: Unknown state, Copy attempt, Failure.
```

### 15) Quantum Cryptography
```text
Topic: Quantum Cryptography.
Create a modern educational animation about secure quantum communication using quantum states, sensitive measurement, and protected information transfer. The scene should suggest physical-law-based security rather than purely mathematical secrecy. Keep the communication channel central and visually trustworthy. Optional short labels: Secure channel, Quantum state, Detection.
```

### 16) Post-Quantum Cryptography
```text
Topic: Post-Quantum Cryptography.
Create an educational animation showing classical digital security evolving to resist future quantum attacks. Use an abstract data channel, cryptographic shields, lattice-inspired geometry, and a looming quantum-computation threat in the background. Emphasize algorithmic resilience, not quantum light hardware. Optional short labels: Classical systems, PQC, Quantum threat.
```

### 17) Quantum Teleportation
```text
Topic: Quantum Teleportation.
Create a clean educational animation showing one unknown source qubit, one shared entangled pair, and one destination qubit reconstructing the source state after a measurement-and-correction process. Make it visually clear that the state is transferred, not the particle itself. Use a readable flow with entanglement first, then classical bits, then correction. Optional short labels: Source state, Entangled pair, Classical bits, Output state.
```

### 18) Quantum Algorithm
```text
Topic: Quantum Algorithm.
Create an educational animation showing a quantum computation in which many possible paths begin in superposition, interference suppresses wrong paths, and one solution becomes amplified. The scene should communicate algorithmic structure and probability shaping, not just raw speed. Use elegant wave-like amplitude behavior and a final dominant output state. Optional short labels: Superposition, Interference, Solution.
```

### 19) Qubit
```text
Topic: Qubit.
Create a foundational educational animation showing a qubit as a state on a Bloch-sphere-inspired scene. Start from a basis state, rotate into superposition, then show measurement collapsing to a definite result. The animation should communicate that a qubit is not just a fuzzy bit but a controllable quantum state. Keep it clean, central, and beginner-friendly. Optional short labels: |0>, |1>, Superposition, Measurement.
```

### 20) Quantum Superposition
```text
Topic: Quantum Superposition.
Create an educational animation showing one quantum system evolving into a coherent combination of possibilities and then yielding one outcome upon measurement. The scene should clearly distinguish superposition from classical uncertainty. Use layered amplitude motion, phase coherence cues, and a calm final measurement event. Avoid gimmicks. Optional short labels: State, Superposition, Measurement.
```

---

## 5) Optional secondary educational diagram prompts
Use these when a topic needs a second supporting animation inside the article.

### Secondary diagram template
```text
Generate a second smaller educational HTML animation for the same topic. Keep it self-contained, responsive, and visually consistent with the first animation. This version should explain one narrower sub-idea only, using one central mechanism and up to three short English labels. Same colors, same dark background family, same motion smoothness, same loop rules.
```

### Suggested secondary diagrams by topic
- Photon -> detector response or wavepacket propagation
- Electron -> probability cloud vs measurement snapshot
- Pauli Exclusion Principle -> orbital occupancy logic
- Quantum Number -> shell vs orbital vs spin layers
- Complementarity Principle -> mode switch in one apparatus
- Observer -> apparatus engaged vs disengaged
- Uncertainty Principle -> narrow position / wide momentum animation
- Quantum State -> basis decomposition animation
- Hilbert Space -> vector projection onto basis
- Operator -> operator acting step-by-step
- Quantum Computer -> qubit control and readout
- QKD -> disturbance caused by interception
- Quantum Gate -> one H gate then one CNOT
- No-Cloning Theorem -> failed arbitrary copy attempt
- Quantum Cryptography -> secure channel logic
- Post-Quantum Cryptography -> migration from old crypto to PQC
- Quantum Teleportation -> correction stage after classical bits
- Quantum Algorithm -> amplitude amplification loop
- Qubit -> Bloch rotation and measurement
- Quantum Superposition -> coherent phase evolution

---

## 6) Strong generation instructions for consistency
Add these short lines at the end of any prompt if the generator starts producing weak results:

```text
Use crisp SVG geometry instead of decorative noise.
Make the science clearer than the style.
Do not crop the animation on mobile.
Reflow layout with media queries below 768px.
Use a smooth 6-second loop with no abrupt reset.
Keep all key objects inside the central 80 percent of the frame.
Avoid overly literal textbook clipart.
```

---

## 7) Suggested filename pattern
- `01-photon-hero.html`
- `01-photon-diagram-a.html`
- `11-quantum-computer-hero.html`
- `11-quantum-computer-diagram-a.html`
- `17-quantum-teleportation-hero.html`

---

## 8) Publishing note
For article pages:
- use one main animation near the top
- use a second educational diagram only when it truly clarifies a sub-idea
- do not stack too many moving blocks on one page
- keep each animation lazy-loaded if possible
- add a short Persian caption below each block outside the animation itself
