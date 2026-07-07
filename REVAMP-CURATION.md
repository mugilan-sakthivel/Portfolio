# Portfolio Revamp — Curation (July 2026)

Goal: reposition mugilans.in from "student who does hackathons" to **AI engineer who ships
production agents**. This doc is the curated content inventory; the redesign implements it.

## Positioning

**Headline:** AI Engineer — I build production AI agents: marketing agents, video-editing
agents, voice agents, and the harnesses that make them reliable.

**The narrative arc** (what the site should communicate in 10 seconds):
1. I ship agentic products used in production (Metaflow, caption engine, reel-radar).
2. I go deep — from training a GPT from scratch on my own GPU to dissecting production
   agent harnesses file-by-file.
3. I've done this across modalities: text agents, voice agents, video automation, RAG.

## FINAL SELECTION (Mugilan's picks, July 2026)

**Hero projects (in order):**
1. Caption Engine — github.com/mugilan-sakthivel/caption-engine (PUBLIC)
2. Voice AI Workspace Agent — github.com/mugilan-sakthivel/voice-ai-workspace-agent (PUBLIC)
3. WhatsApp Personal Agent — github.com/mugilan-sakthivel/whatsapp-agent (PUBLIC)
4. Lua — AI landing-page designer, the end-to-end build — github.com/tryLua/lua (PUBLIC)

**Learning section:** Train-Your-Own-GPT + Agent Harness (both PUBLIC).

**Work experience:** Kalvium Labs — Software Engineer · Lua Labs — Founder ·
Metaflow — Head of Engineering.

Note: caption-engine went public per Mugilan's call, with client template styles
(Akarshana/Ephaphra profiles) inside — flagged; get client OK or scrub if it becomes an issue.

## Experience (proposed)

### 1. Metaflow — AI Engineer (≈ Mar 2026 – present) ⚠️ confirm framing
The anchor of the whole portfolio. 515+ commits on the core platform since March 2026.
- Built and hardened an AI marketing-agent platform: LangGraph/deepagents harness,
  multi-tenant tool execution, subagent orchestration.
- Ads operator agents for Google Ads, Meta, and LinkedIn (skills architecture,
  GAQL/protos-level payload correctness, eval-gated migrations).
- Skills system: 2000+ marketing skills, Sanity CMS directory (Next.js 15) + Python
  scraping/ingestion pipeline.
- Production ops: Stripe webhook debugging, PostHog analytics pipelines, env/cron
  isolation between prod and dev, streaming/thinking UX.
- ⚠️ OPEN QUESTION: is this under Kalvium Labs, a client contract, or a startup with
  Narayan? Determines whether it's one work entry or two.

### 2. Kalvium Labs — Software Engineer Intern (Mar 2025 – ?)
Keep, with an end date if it ended. Sharpen the description: built AI products (RAG
document-query services, etc.) rather than the current generic line.

### 3. Freelance / Client AI Engineering (2025 – present)
Roll the client work into one entry:
- **Caption engine factory** — AI that learns a video editor's caption style from one AE
  project and auto-captions new videos as editable AEPs, with SSIM pixel-diff
  self-verification (0.98–0.99). CEP panel + gpt-5.5 agent. Shipped.
- **Outreach tooling feasibility** (client: Omkar) — engineering feasibility, ban-risk
  analysis, cost modeling, formal proposals.
- **Twilio voice agent** — ConversationRelay + Gemini outbound phone agent (FastAPI).
- Web builds (royal-rental, thagai, etc.) — mention in aggregate, don't itemize.

### 4. Education — keep as-is (Kalvium + Mysore BCA), move below work.

## Projects — Tier 1 (hero cards, ~7)

| Project | One-liner | Stack | Status/proof |
|---|---|---|---|
| **Caption Engine** | AI learns an editor's caption style → auto-captions any raw video as a real editable AE project; verifies its own output pixel-by-pixel (SSIM 0.98–0.99) | Claude Agent SDK, ExtendScript, CEP, Node | Shipped, 2 real client styles, ~3 min/video |
| **Reel Radar** | IG growth tool: finds breakout reel *concepts* (views ÷ channel median), writes remake scripts from transcripts, real analytics + auto-DM funnels | Next.js 16, Groq Whisper+Llama, Composio, Apify, Supabase | Production-shaped: DB, cron, tests, deploy |
| **Lua — AI Video Editor** | Natural language → After Effects/Premiere automation; extracts timelines via JSX, self-healing error loops, LangFuse observability. Full startup pitch deck | Python, DeepAgents, LangFuse, ExtendScript | Working automation + pitch deck |
| **Luna — AI Web Builder** | Learns design from real websites via a Chrome extension → generates production React; token billing, full architecture docs | React, FastAPI, LangChain, Chrome ext, Postgres | Extensively documented, multi-version |
| **WhatsApp Personal Agent** | AI assistant living in WhatsApp: 3-tier memory (pgvector semantic + short/long-term), per-user Composio Google Workspace tools | Python DeepAgents, FastAPI, Node bridge, Supabase | Working multi-service prototype |
| **Voice Workspace Agent** | Voice-first mobile agent for Google Workspace/M365 with write-approval gates, audit logs, graceful degradation | Expo RN, FastAPI, DeepAgents, Composio, Groq Whisper, Gemini TTS | Full-stack w/ architecture docs |
| **Train-Your-Own-GPT** | Autograd from scratch → makemore → nanoGPT trained on my own M2 Pro GPU — Karpathy ladder, done by hand | Python, PyTorch (MPS) | Stage 1 done, in progress — frame as learning-in-public |

## Projects — Tier 2 (grid, shorter cards)

- **Agent Harness** — reliable deep-agent harness: deepagents + LangGraph + Gemini + MCP, full-stack.
- **Scren** — LLM sales-call auditing; Next.js + AWS Fargate async worker architecture.
- **UnifiedAI** — RAG workspace assistant (pgvector) with source attribution + action-item detection.
- **Agent Engineering Masterclass** — original course dissecting production agent harnesses file-by-file.
- **CTO Masterclass** — first-principles course: machine internals → distributed systems → eng leadership.
- **Template Studio** — Remotion "style template" proof (word-level transcription → styled captions).
- **Scout AI** (keep from old site) — AI hiring agent, 100x Engineers hackathon.
- **Q-Space** (keep, one entry not two) — AI quiz generation from any content; multiple hackathon wins.
- **DataMotion AI** (keep) — AI animated-infographic generator.

## Hackathons — prune to wins + recent

Keep: HackerRank Orchestrate (June 2026, multi-modal evidence review), Scout AI/100x (May 2025),
LangChain Kochi (Best Data Hack), TinkerHub Prisma (Best Project), Vue.js (Best Project),
Q-Space V2/Kalvium. **Cut:** CampusLeet, Cryptera, generic participation entries.

## Cut from current site

Funky Fumbles, Review-Club, Rosenau, Hogwarts LMS, Strix as separate cards (pre-AI era,
dilutes the story). Fix the broken bits regardless: Scout AI's source link points at
q-space; typos ("Javacript", "Expres.js"); dead `initials: "S"`.

## Skills refresh

Agents: LangGraph, DeepAgents, LangChain, Claude Agent SDK, Vercel AI SDK, MCP, Composio,
evals/LangFuse • Models: Claude, Gemini, GPT/Codex, Groq/Whisper • Retrieval: RAG,
pgvector, embeddings • Product: Next.js 15/16, React 19, FastAPI, Supabase, Prisma,
Postgres, Tailwind v4 • Video/creative: Remotion, After Effects ExtendScript/CEP •
Infra: GCP, AWS (Fargate), Vercel, E2B, Docker • Foundations: PyTorch, Python, TypeScript

## GitHub push status (done July 7, 2026)

All previously local-only projects are now on GitHub as PRIVATE repos under
`mugilan-sakthivel` (secrets excluded, media >50MB excluded): caption-engine,
agent-harness, whatsapp-agent, voxa-mail, unifiedai, train-your-own-gpt,
template-studio, neural-networks-explained, linkedin-lead-extractor, lua-pitch-deck,
orchestrator-lab, agent-loop-lab. Unpushed WIP committed+pushed on
voice-ai-workspace-agent (full app impl) and tryLua/lua develop (image-upload WIP).
Skipped: nex (AlwinSunil's repo), nexsesLandingpage + Lua_Video_editing roots (thin
wrappers; the real Lua AE-automation code already lives in private Lua/Lua-V2 repos),
luna root iterations (nexsus/luna design — superseded by tryLua/lua).

## Private-repo problem

Most Tier-1 work is private or client-owned. Plan per project:
- **Case-study pages** with demo videos/GIFs instead of source links (caption engine, Lua,
  Metaflow work — get client/employer OK for what's shareable).
- **Make public** where there's no client conflict: reel-radar(?), Agent_Harness,
  train-your-own-gpt, agent-engineering-masterclass, whatsapp-agent (strip secrets first).
- Never link the study forks (trustclaw, opencode, pixel-agents, t3code) as own work.

## Redesign notes (next phase)

- Current site = dillionverma magic-portfolio template, Next.js 14. Decide: refresh content
  on the same template (fast) vs. full redesign (new IA: hero → experience → case studies →
  projects grid → writing/courses → contact).
- Case-study detail pages are the real differentiator — the MDX blog scaffold already exists.
- GitHub cleanup is part of the revamp: pin the right 6 repos, write READMEs with demos,
  update profile repo (mugilan-sakthivel/mugilan-sakthivel).
