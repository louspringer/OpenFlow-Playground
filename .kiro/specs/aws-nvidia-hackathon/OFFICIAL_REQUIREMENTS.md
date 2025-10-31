# AWS×NVIDIA Hackathon - Official Requirements

**Source**: https://nvidia-aws.devpost.com/rules  
**Extracted**: 2025-10-30  
**Status**: ✅ VERIFIED FROM OFFICIAL RULES

---

## 🚨 CRITICAL TIMELINE

**Official Name**: "Agentic AI Unleashed: AWS & NVIDIA Hackathon"

### Deadlines (ALL TIMES EASTERN)
- **Registration Closes**: Monday, November 3, 2025 @ 2:00pm ET
- **Submission Deadline**: Monday, November 3, 2025 @ 2:00pm ET ⏰
- **Judging Period**: Nov 13 - Nov 26, 2025
- **Winners Announced**: Friday, December 5, 2025 @ 2:00pm ET

**TIME REMAINING**: ~3.5 days from Oct 30, 2025!

**⚠️ MASTER PLANNER WAS WRONG**: Said Nov 4 @ 17:00 PT, actual is Nov 3 @ 14:00 ET (11:00am PT)

---

## 📋 MANDATORY REQUIREMENTS

### What to Create

**Build an Agentic Application that includes ALL of the following**:

1. **NVIDIA NIM - LLM**: 
   - Use `llama-3.1-nemotron-nano-8B-v1` large language reasoning model
   - Deployed as NVIDIA NIM inference microservice
   - Link: https://build.nvidia.com/nvidia/llama-3_1-nemotron-70b-instruct (verify model name)

2. **NVIDIA NIM - Retrieval**:
   - At least ONE Retrieval Embedding NIM
   - Link: https://build.nvidia.com/explore/retrieval

3. **AWS Platform** (choose ONE):
   - Amazon Elastic Kubernetes Service (Amazon EKS) Cluster, OR
   - Amazon SageMaker AI endpoint

### What to Submit

**Required on Devpost by Nov 3 @ 2:00pm ET**:

1. **Text Description**
   - Explain features and functionality of your project
   - No specific word limit mentioned

2. **Demo Video**
   - **Maximum length**: Under 3 minutes (judges not required to watch beyond 3 min)
   - Must show project functioning on intended platform
   - Upload to: YouTube, Vimeo, Facebook Video, or Youku (public)
   - Provide link on Devpost submission form
   - Must NOT include unlicensed third-party trademarks or copyrighted content

3. **Public Code Repository**
   - URL to publicly accessible repository
   - Must include ALL relevant project code
   - Must include README with deployment instructions
   - Must allow judges to test project

4. **Deployment Instructions**
   - README must contain step-by-step deployment instructions
   - Must enable judges to replicate and test your project

### Functionality Requirements

- Project must successfully install and run consistently on intended platform
- Must function as depicted in video and described in text
- Must be deployed on Amazon EKS or Amazon SageMaker AI

### New vs Existing Projects

**Allowed**:
- Newly created projects during hackathon
- Existing projects if **significantly updated** after Oct 13, 2025 (submission period start)

**Required**:
- Must be original work
- Must be solely owned by entrant
- No IP rights conflicts

---

## ⚖️ JUDGING CRITERIA

### Stage 1: Pass/Fail Viability Check
- Does project reasonably fit the theme?
- Does it reasonably apply required APIs/SDKs?

### Stage 2: Scoring (Equally Weighted - 25% each)

1. **Technological Implementation**
   - Quality software development
   - Effective use of NVIDIA and AWS
   - Technical execution quality

2. **Design**
   - User experience quality
   - Design thoughtfulness
   - Interface polish

3. **Potential Impact**
   - Size of impact on target audience
   - Real-world applicability
   - Value proposition

4. **Quality of the Idea**
   - Creativity
   - Uniqueness
   - Innovation

**Tie-Breaking**: Highest score in Technological Implementation wins

---

## 🏆 PRIZES

### Prize Structure (4 Non-Cash Prizes)

1. **Grand Prize** (1 winner)
   - NVIDIA GPU: PNY RTX 6000 ADA (~$6,900 value)
   - Promotion on NVIDIA developer social channels
   - Swag
   - 1,000 Brev.dev credits
   - Credits for NVIDIA DLI platform

2. **Second Place** (1 winner)
   - NVIDIA GPU: MSI RTX 5090 32G (~$2,500 value)
   - Promotion on NVIDIA developer social channels
   - Swag
   - 500 Brev.dev credits
   - Credits for NVIDIA DLI platform

3. **Third Place** (1 winner)
   - NVIDIA GPU: NVIDIA GeForce RTX 5080 Founders Edition (~$1,250 value)
   - Promotion on NVIDIA developer social channels
   - Swag
   - 300 Brev.dev credits
   - Credits for NVIDIA DLI platform

4. **Most Valuable Participant** (1 individual)
   - NVIDIA GPU: MSI RTX 5090 32G (~$2,500 value)
   - Promotion on NVIDIA developer social channels
   - Swag
   - Credits for NVIDIA DLI platform
   - **Awarded for community engagement** (Discord, Discussion Forum)

**Important**:
- Each project eligible for MAX 1 prize
- MVP prize is individual, not project-based
- Prizes non-transferable

---

## 💰 AWS CREDITS

**$100 Promotional Credits Available**:
- Per team/project (one-time, non-transferable)
- Request via form: https://forms.gle/rsZ2foGBjve1Ceqb9
- Must demonstrate valid submission idea
- Covers ~24 hours of 2 required NIM microservices on SageMaker/EKS
- NOT redeemable for cash
- Once exhausted, access cut off (no overages charged)

**Budget Coverage**:
- NVIDIA NIM microservices (LLM + Retrieval)
- Storage, networking, security services
- Monitor dashboard to avoid running out

**Alternative**: AWS Free Tier available at https://aws.amazon.com/free

---

## ✅ ELIGIBILITY

### Open To:
- Individuals (age of majority, corporate/professional email required)
- Teams of eligible individuals
- Organizations (corporations, nonprofits, LLCs, partnerships)

### NOT Open To:
- Residents of prohibited countries/territories:
  - Brazil, Germany, Italy, France, Spain, Argentina, Australia
  - Hong Kong, Indonesia, Malaysia, Poland, Thailand, Philippines, Vietnam, Singapore
  - UAE, Quebec, Russia, Crimea, Cuba, Iran, North Korea, Syria
  - Any OFAC-designated countries
- Sponsor/Administrator employees, agents, affiliates
- Judges or their employers
- Anyone with conflict of interest

**Team Structure**:
- Can join multiple teams
- Can enter individually AND as team member
- Must appoint one Representative per team/org

---

## 📝 SUBMISSION RULES

### Ownership & IP
- Must be original work
- Must be solely owned by entrant
- No IP conflicts with third parties
- No financial/preferential support from Sponsors/Administrator

### Third-Party Integrations
- Must be authorized to use any third-party SDKs/APIs/data
- Must comply with licensing requirements
- NVIDIA and AWS integrations obviously allowed

### Multiple Submissions
- Can submit multiple projects
- Each must be unique and substantially different
- Each judged independently

### Language
- All materials must be in English
- OR provide English translation of video/description/instructions

### Testing Access
- Must provide access to working project for judges
- Must be functional and testable
- If requires proprietary hardware, must provide demo video showing actual usage

---

## 🔧 TECHNICAL SPECIFICATIONS

### Required Stack

**NVIDIA Components** (MANDATORY):
- llama-3.1-nemotron-nano-8B-v1 (NIM LLM)
- At least 1 Retrieval Embedding NIM

**AWS Platform** (choose ONE):
- Amazon EKS (Elastic Kubernetes Service)
- Amazon SageMaker AI

**Resources**:
- NVIDIA NIMs on build.nvidia.com for testing
- AWS Free Tier for development

### Testing Requirements
- Project must install successfully
- Must run consistently
- Must function as demonstrated

---

## 🎯 STRATEGIC RECOMMENDATIONS

### Maximize Score

**Technological Implementation (25%)**:
- Clean, production-quality code
- Proper AWS architecture (EKS best practices or SageMaker optimization)
- Efficient NIM integration
- Error handling and resilience

**Design (25%)**:
- Intuitive UX
- Professional UI
- Clear workflows
- Polish and attention to detail

**Potential Impact (25%)**:
- Solve real problem
- Clear target audience
- Measurable value proposition
- Scalability story

**Quality of Idea (25%)**:
- Novel application of agentic AI
- Creative use of NIMs
- Unique approach
- Differentiation from other submissions

### Competitive Edge

**1,871 participants registered** - competition is fierce!

**Differentiation opportunities**:
- Enterprise-grade observability (beast-observability)
- Security/compliance focus (beast-redaction-client)
- Multi-agent coordination (Beast Mode framework)
- Production readiness (testing, monitoring, deployment automation)
- Cross-cloud portability narrative (even if targeting AWS)

---

## ⚠️ DISQUALIFICATION RISKS

### Avoid These:
- Late submission (after Nov 3 @ 2:00pm ET)
- Missing required components (LLM NIM, Retrieval NIM, AWS platform)
- Non-functional code
- Missing deployment instructions
- Video over 3 minutes
- Unlicensed third-party content in video
- IP conflicts
- Prohibited countries/territories
- Financial support from sponsors

---

## 📊 DELIVERABLES CHECKLIST

### Code Repository
- [ ] Public GitHub repo
- [ ] README with deployment instructions
- [ ] All relevant code included
- [ ] Working on EKS or SageMaker
- [ ] llama-3.1-nemotron-nano-8B-v1 NIM integrated
- [ ] At least 1 Retrieval Embedding NIM integrated
- [ ] Functional and testable

### Demo Video
- [ ] Under 3 minutes
- [ ] Shows project functioning
- [ ] Uploaded to YouTube/Vimeo/Facebook/Youku
- [ ] Public visibility
- [ ] Link provided on Devpost
- [ ] No unlicensed content

### Devpost Submission
- [ ] Text description (features/functionality)
- [ ] Demo video link
- [ ] Code repository URL
- [ ] Submitted by Nov 3 @ 2:00pm ET

### Optional (for MVP Prize)
- [ ] Engage in Discord/Discussion Forum
- [ ] Help other participants
- [ ] Active community contribution

---

## 🚀 NEXT STEPS

### Immediate (TODAY - Oct 30)
1. ✅ Official requirements captured
2. ⏳ Register team on Devpost
3. ⏳ Request $100 AWS credits (https://forms.gle/rsZ2foGBjve1Ceqb9)
4. ⏳ Create detailed spec with `/kiro:spec-init`

### Day 1 (Oct 31)
- Set up AWS environment (EKS or SageMaker decision)
- Test NVIDIA NIMs on build.nvidia.com
- Architecture design
- Component integration plan

### Day 2 (Nov 1)
- Build core agentic application
- Integrate llama-3.1-nemotron-nano-8B-v1 NIM
- Integrate Retrieval Embedding NIM
- Deploy to AWS

### Day 3 (Nov 2)
- Polish implementation
- Create demo video
- Write deployment instructions
- Test end-to-end

### Day 4 (Nov 3) - DEADLINE DAY
- Final testing
- Upload video
- Submit to Devpost by 2:00pm ET
- BUFFER: Submit by noon to be safe

---

## 🎯 CRITICAL DECISIONS NEEDED

### 1. Platform Choice
- **Amazon EKS**: More complex, more impressive, full container orchestration
- **Amazon SageMaker AI**: Simpler deployment, managed service, faster to build

**Recommendation**: SageMaker for speed (3.5 days!), can showcase EKS in architecture diagram

### 2. Application Focus
**What agentic application should we build?**

Options based on our assets:
- **Document classifier agent** (leverage beast-redaction-client)
- **Development automation agent** (leverage beast-ai-dev-agent)
- **Multi-agent orchestration demo** (leverage Beast Mode framework)
- **Compliance automation agent** (leverage security/redaction capabilities)

### 3. Leveraging Existing Components
- beast-mailbox-core for messaging
- beast-observability for telemetry
- beast-redaction-client for security
- Beast Mode framework for coordination

**Question**: Which application showcases our strengths best while meeting requirements?

---

## 📞 CONTACT

**Questions**: support@devpost.com  
**Official URL**: https://nvidia-aws.devpost.com/  
**Rules**: https://nvidia-aws.devpost.com/rules  
**AWS Event**: https://aws.amazon.com/startups/events/aws-generative-ai-hackathon-challenge-2025

---

**READY TO EXECUTE** - Need to decide application focus and platform, then create full spec.

