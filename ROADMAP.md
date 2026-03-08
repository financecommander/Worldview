# Roadmap

This document tracks the planned phases of development for Worldview — the compression-first video intelligence and creation platform.

---

## Phase 1 — Foundation

**Goal:** Establish the core ingestion and compression pipeline.

- [ ] Video ingestion from CCTV and uploaded files
- [ ] Frame sampler with configurable rate
- [ ] Triton vision model integration (YOLO/RT-DETR object detection)
- [ ] CLIP/SigLIP embedding generation per frame
- [ ] OCR extraction from video frames
- [ ] Multi-object tracking across frames
- [ ] Event compression engine (raw detections → semantic events)
- [ ] Temporal state graph storage
- [ ] Basic entity / event / state / evidence schema

---

## Phase 2 — Surveillance & Alerts

**Goal:** Deliver actionable real-time monitoring and alerting.

- [ ] Live stream monitoring (CCTV, drones, body cameras, industrial cameras)
- [ ] Rule engine for configurable violation detection (PPE, restricted zones, proximity)
- [ ] Alert generation with plain-language explanations
- [ ] Incident report export (PDF / JSON)
- [ ] Dashboard for live event feed and alert history
- [ ] Integration with super-duper-spork swarm for reasoning escalation (`small → medium → large`)
- [ ] Retention and archival policies for event data

---

## Phase 3 — Video Search

**Goal:** Make every recorded video semantically searchable.

- [ ] Natural-language query interface over the event graph
- [ ] Evidence clip retrieval tied to matching events
- [ ] Timeline view for query results
- [ ] Semantic similarity search using stored embeddings
- [ ] Cross-camera entity linking (same person / object across streams)
- [ ] Compliance audit export with timestamped evidence

---

## Phase 4 — Video Creation

**Goal:** Generate training videos and incident recreations from event data.

- [ ] Event narrative builder (structured events → scene script)
- [ ] Scene planner with camera motion descriptors
- [ ] Keyframe extraction and sparse timeline representation
- [ ] L4 GPU frame interpolation (optical flow + diffusion)
- [ ] Distributed segment generation via swarm node scheduler
- [ ] Output rendering and merge (720p / 1080p)
- [ ] Generation from external sources: prompts, email threads, EDGAR filings
- [ ] Output types: training simulations, incident recreations, compliance tutorials

---

## Phase 5 — Scale & Integration

**Goal:** Harden the platform for production scale and integrate the full ecosystem.

- [ ] Horizontal scaling of Triton inference across GPU cluster
- [ ] Swarm-level load balancing (`cell → dot → small → medium → large → cloud`)
- [ ] Integration with Quantum-Protocol for financial incident video documentation
- [ ] Integration with DFIP for compliance video generation
- [ ] Constitutional-Tender web terminal UI panels for search and surveillance views
- [ ] Multi-tenant support with per-deployment retention rules
- [ ] Full audit trail for all AI decisions (entity, state, timestamp, model tier used)

---

## Future Directions

- **Temporal reasoning engine** — learning motion patterns, scene transitions, and causal event chains across long time horizons
- **Predictive alerting** — detecting precursor event sequences before a violation occurs
- **Federated edge deployment** — running the perception and compression layers on-device (body cameras, edge nodes) and syncing compressed events to central swarm
- **Custom domain adaptation** — fine-tuning vision models for specialized verticals (healthcare, mining, logistics)
- **Video LLM integration** — feeding compressed event timelines as context into large language models for deeper incident narrative generation

---

*Phases are indicative. Priorities may shift based on deployment feedback and partner requirements.*
