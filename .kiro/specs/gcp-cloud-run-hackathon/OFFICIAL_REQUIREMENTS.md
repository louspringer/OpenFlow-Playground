# Cloud Run Hackathon - Official Requirements

**Source**: https://run.devpost.com/rules  
**Extracted**: 2025-10-30  
**Status**: ✅ VERIFIED FROM OFFICIAL RULES

---

## 🚨 CRITICAL TIMELINE

**Official Name**: "Cloud Run Hackathon"

### Deadlines (ALL TIMES PACIFIC)
- **Registration Opens**: Monday, October 6, 2025 @ 9:00am PT
- **Submission Deadline**: Monday, November 10, 2025 @ 5:00pm PT ⏰
- **Judging Period**: Nov 10 - Dec 5, 2025
- **Potential Winners Notified**: ~December 9, 2025
- **Winners Announced**: ~December 12, 2025

**TIME REMAINING**: ~11 days from Oct 30, 2025

**COMPARED TO AWS×NVIDIA**: 
- AWS×NVIDIA: Nov 3 @ 2:00pm ET (3.5 days)
- Cloud Run: Nov 10 @ 5:00pm PT (11 days)
- **7.5 day gap** between submissions!

---

## 📋 MANDATORY REQUIREMENTS

### Choose ONE Category

#### 🤖 **AI Studio Category**
**Requirements**:
- **MUST use AI Studio** to generate a portion of your application
- **MUST deploy to Cloud Run** (can use "Deploy to Run" button in AI Studio)
- **Challenge**: Vibe-code an idea into existence with AI Studio
- **Project types**: Web service, data pipeline, mobile backend, or any serverless solution

**Submission Extra**:
- **MUST provide AI Studio prompts link** (Share App functionality)

#### 🤝 **AI Agents Category** ⭐ PERFECT FIT FOR BEAST MODE
**Requirements**:
- **MUST use Google Agent Development Kit (ADK)**
- **MUST deploy agents to Cloud Run**
- **Challenge**: Build multi-agent application
- **Details**: At least 2 AI agents that communicate to complete a workflow, solving real-world problem

**This is BEAST MODE's sweet spot!**

#### ⚡ **GPU Category**
**Requirements**:
- **MUST utilize NVIDIA L4 GPUs** on Cloud Run (Service, Job, or Worker Pool)
- **SHOULD use** europe-west1 or europe-west4 region
- **Challenge**: Run performant AI/ML models on GPUs
- **Details**: Deploy and run open-source model (like Gemma) on GPU-configured Cloud Run service

---

### General Requirements (ALL Categories)

**Cloud Run Deployment** (MANDATORY):
- Must use ONE or MORE of these resource types:
  1. **Service**: HTTP requests, events, functions (stateless, auto-scaling)
  2. **Job**: Parallelizable tasks that run to completion
  3. **Worker Pool**: Pull-based workloads (Kafka, Pub/Sub consumers, RabbitMQ)

**Project Status**:
- **New projects ONLY** - Must be created during contest period (Oct 6 - Nov 10)
- Cannot be modification/extension of existing project
- Must be original work

---

## 📤 SUBMISSION REQUIREMENTS

### Required Submissions

1. **Text Description**
   - Project features and functionality
   - Technologies used
   - Data sources
   - Findings and results

2. **Demonstration Video**
   - **Maximum**: 3 minutes (only first 3 min evaluated)
   - Show project functioning
   - Upload to YouTube or Vimeo (public)
   - Must be in English or include English subtitles

3. **Public Code Repository**
   - Public GitHub repo
   - Must allow judging and testing access
   - Include all relevant code

4. **Architecture Diagram**
   - Visual representation of components
   - Data flow diagram
   - Technology stack visualization

5. **Hosted Project URL** (highly encouraged)
   - Live demo link
   - Functional deployment on Cloud Run

6. **AI Studio Link** (AI Studio category only)
   - Share App functionality link
   - Prompts in AI Studio

---

## 🎁 BONUS POINTS (Optional)

### Optional Google Cloud Contributions (Max +0.4 points each)

1. **Use Google AI models**: Gemini, Gemma, Imagen, Veo
2. **Multiple Cloud Run services**: Front-end + back-end, multiple services

### Optional Developer Contributions (Max +0.4 points each)

1. **Publish content** (blog, podcast, video): How project was built using Cloud Run
   - Public platform (medium.com, dev.to, YouTube)
   - Must be public (not unlisted)

2. **Social media post**: Promote project on X, LinkedIn, Instagram, Facebook
   - **MUST include hashtag**: #CloudRunHackathon

**Maximum Bonus**: +0.8 points (could push score from 6.0 → 6.8)

---

## ⚖️ JUDGING CRITERIA

### Weighted Scoring (Max 6.0 base + 0.8 bonus = 6.8 total)

1. **Technical Implementation (40%)** - 2.4 points max
   - Code quality (clean, efficient, well-documented)
   - Cloud Run core concepts utilized
   - Intuitive and user-friendly app
   - Proper architecture

2. **Demo & Presentation (40%)** - 2.4 points max
   - Problem clearly defined
   - Solution effectively presented
   - Cloud Run usage explained
   - Documentation quality

3. **Innovation & Creativity (20%)** - 1.2 points max
   - Novelty and originality
   - Addresses significant problem
   - Unique solution
   - Creative approach

### Judging Process

**Stage 1**: Pass/Fail viability check
- Meets baseline requirements
- Addresses challenges
- Applies required tools

**Stage 2**: Weighted scoring (above criteria)

**Stage 3**: Bonus points applied

**Winner Selection**:
- Highest score per category wins category prize
- Highest score overall wins Grand Prize
- Ties broken by comparing Technical Implementation scores

---

## 🏆 PRIZES ($50,000 Total!)

### Grand Prize (1 winner - highest score overall)
- **$20,000 USD**
- $3,000 Google Cloud Credits
- 1 year Google Developer Program Premium subscription (up to 2 subscriptions)
- Virtual coffee with Google team member
- Social media promotion

### Category Prizes (1 winner each - 3 total)
**Best of AI Studio** | **Best of AI Agents** | **Best of GPUs**
- **$8,000 USD**
- $1,000 Google Cloud Credits
- Virtual coffee with Google team member
- Social media promotion

### Honorable Mentions (3 winners)
- **$2,000 USD**
- $500 Google Cloud Credits

**Total Winners**: 7 (1 Grand + 3 Category + 3 Honorable)

---

## 💰 GOOGLE CLOUD CREDITS

**$100 GCP Credits Available**:
- Request by **November 7, 2025 @ 12:00pm PT** ⏰
- Form: https://forms.gle/YKSxTsJffi9Wow4a8
- Approval within 72 business hours (Google's discretion)
- Not guaranteed, need valid submission idea

**Alternative**: Google Cloud Free Tier at https://cloud.google.com/free

---

## ✅ ELIGIBILITY

### Open To:
- Individuals (age of majority in residence country, 20+ in Taiwan)
- Teams of eligible individuals
- Organizations (companies, nonprofits, LLCs)

### NOT Open To:
- Residents of prohibited regions:
  - Italy, Quebec, Crimea, Cuba, Iran, Syria, North Korea, Sudan, Belarus, Russia
  - Or other US OFAC-designated countries
- Google employees, affiliates, judges
- Sponsor/administrator employees, agents, affiliates

**2,263 participants registered** - competition level!

---

## 🔧 ALLOWED TECHNOLOGIES (Optional/Encouraged)

### Foundation Models (Highly Encouraged)
- **Gemini** (all models)
- **Gemma** (open-source)
- **Imagen** (image generation)
- **Veo** (video generation)
- Anthropic Claude, Llama, other models also allowed

### CLI-Based AI Assistance
- **Gemini CLI** (encouraged)
- Anthropic Claude Code
- Other AI coding tools

### Google Cloud Services
- **Cloud Storage** (blob store)
- **BigQuery** (data warehousing/analysis)
- **Firestore** (NoSQL)
- **Cloud Run MCP server**
- Many more GCP services

### Use Cases
- Web services
- IoT devices
- Mobile backends
- Data pipelines
- Any serverless solution

---

## 🎯 STRATEGIC RECOMMENDATIONS

### Category Selection

**AI Agents Category = BEST FIT**:
- We have **Beast Mode multi-agent framework**
- We have **beast-mailbox-core** for agent messaging
- We have **beast-ai-dev-agent** ready to deploy
- **At least 2 agents** requirement? We have 12 message types!
- **Google ADK** requirement? We integrate it

**Why AI Agents Category**:
- Leverages our core strength (multi-agent coordination)
- Shows production-ready framework
- Demonstrates real-world problem solving
- Differentiates from "yet another chatbot"
- Can showcase observability/security (beast-observability, beast-redaction-client)

### Maximize Score Strategy

**Base Score (6.0)**:
1. **Technical Implementation (2.4)**: Production-quality code, tests, CI/CD
2. **Demo & Presentation (2.4)**: Clear problem, polished demo, docs
3. **Innovation (1.2)**: Multi-agent enterprise automation

**Bonus Points (+0.8)**:
1. **Use Gemini** (+0.4): Integrate Gemini model in agents
2. **Multiple Services** (+0.4): Front-end + back-end + agent orchestrator
3. **Publish blog** (+0.4): "Building Enterprise Multi-Agent Systems on Cloud Run"
4. **Social post** (+0.4): #CloudRunHackathon promotion

**Target Score**: 6.8/6.8 (maximum possible)

---

## 📊 DELIVERABLES CHECKLIST

### Code Repository
- [ ] Public GitHub repo
- [ ] All relevant code
- [ ] README with setup instructions
- [ ] Deployed on Cloud Run (Service/Job/Worker Pool)
- [ ] Google ADK agents (AI Agents category)
- [ ] At least 2 agents communicating
- [ ] Functional and testable

### Demo Video
- [ ] Under 3 minutes
- [ ] Shows functioning project
- [ ] Uploaded to YouTube/Vimeo (public)
- [ ] Link on Devpost
- [ ] English or English subtitles

### Devpost Submission
- [ ] Text description (comprehensive)
- [ ] Demo video link
- [ ] Code repository URL
- [ ] Architecture diagram
- [ ] Hosted project URL (live Cloud Run)
- [ ] Category selected (AI Agents)
- [ ] Submitted by Nov 10 @ 5:00pm PT

### Bonus Deliverables
- [ ] Blog post (medium.com/dev.to/YouTube)
- [ ] Social media post (#CloudRunHackathon)
- [ ] Use Gemini model
- [ ] Multiple Cloud Run services

---

## 🚀 TIMELINE STRATEGY

**We have 7.5 days AFTER AWS×NVIDIA submission!**

### After AWS×NVIDIA (Nov 3)
**Day 1-2 (Nov 4-5)**: Adapt AWS solution to Cloud Run
- Port agents to Google ADK
- Deploy to Cloud Run services
- Integrate Gemini models
- Set up worker pools

**Day 3-4 (Nov 6-7)**: Polish and enhance
- Multi-service architecture (front/back/agents)
- Request $100 GCP credits (by Nov 7 @ noon PT!)
- Architecture diagram
- Documentation

**Day 5-6 (Nov 8-9)**: Content creation
- Demo video (3 min max)
- Blog post on dev.to/medium
- Social media posts

**Day 7 (Nov 10)**: Final submission
- Submit to Devpost by 5:00pm PT
- BUFFER: Submit by 3:00pm to be safe

---

## 🎯 CRITICAL DECISIONS

### 1. Category: AI Agents ⭐
**Why**: We have multi-agent framework ready, shows real innovation

### 2. Application Focus
**Build**: Enterprise multi-agent automation system
- Agent 1: Task planner (decides what to do)
- Agent 2: Code executor (implements tasks)
- Agent 3: Quality validator (checks work)
- Orchestrator: Coordinates workflow
- Use beast-mailbox-core for messaging
- Use beast-observability for telemetry

### 3. Leverage Existing Components
- **beast-mailbox-core**: Agent messaging
- **beast-observability**: Telemetry
- **beast-redaction-client**: Security/compliance
- **Beast Mode framework**: Multi-agent coordination

### 4. Google ADK Integration
- Build agents using Google ADK
- Deploy to Cloud Run
- Show production-ready pattern

---

## ⚠️ DISQUALIFICATION RISKS

### Avoid These:
- Late submission (after Nov 10 @ 5:00pm PT)
- Not using required category tools (ADK for AI Agents, AI Studio for that category, GPUs for GPU category)
- Project not new (must be created Oct 6 - Nov 10)
- Not deployed on Cloud Run
- Video over 3 minutes
- Missing required submissions
- Inappropriate content
- IP conflicts

---

## 🔄 REUSE STRATEGY FROM AWS×NVIDIA

### What Transfers Directly
- **beast-redaction-client**: Platform-agnostic
- **beast-observability**: Platform-agnostic
- **beast-mailbox-core**: Platform-agnostic
- **Agentic framework**: Platform-agnostic

### What Needs Adaptation
- **Deployment**: EKS/SageMaker → Cloud Run
- **Models**: NVIDIA NIMs → Google Gemini/Gemma
- **Platform services**: AWS services → GCP services
- **Agent framework**: Custom → Google ADK

### Portability Story
**Judges LOVE cross-cloud portability**:
- "Built for AWS×NVIDIA, ported to Cloud Run in 7 days"
- "Shows true cloud-native architecture"
- "Production-ready, not hackathon-ware"
- "Enterprise deployable"

---

## 📞 CONTACT

**Questions**: support@devpost.com  
**Privacy questions**: cloudhackathons@google.com  
**Official URL**: https://run.devpost.com/  
**Rules**: https://run.devpost.com/rules  
**Credits Form**: https://forms.gle/YKSxTsJffi9Wow4a8

---

## 🎯 WINNING STRATEGY

### AI Agents Category Focus
1. **Multi-agent system** (Beast Mode framework)
2. **Google ADK integration** (required)
3. **Cloud Run deployment** (Service + Worker Pool)
4. **Real-world problem** (enterprise automation)
5. **Production quality** (tests, docs, observability)

### Bonus Points Maximization
1. **Gemini integration** (+0.4) - Use for agent reasoning
2. **Multiple services** (+0.4) - Front-end + agents + orchestrator
3. **Blog post** (+0.4) - Technical deep-dive
4. **Social promotion** (+0.4) - #CloudRunHackathon

**Target**: 6.8/6.8 score (maximum with bonuses)

### Differentiation
- **Not another chatbot** - Real multi-agent coordination
- **Enterprise-ready** - Security, compliance, observability
- **Production-proven** - beast-mailbox-core has 90% coverage
- **Cross-cloud portable** - Works on AWS and GCP
- **Open source** - All packages published to PyPI

---

**NEXT**: Create detailed spec with architecture leveraging Google ADK + Beast Mode framework.

