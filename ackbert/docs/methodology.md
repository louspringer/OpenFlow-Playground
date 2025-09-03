# Ack-Bert Methodology Guide

## Overview

The Ack-Bert methodology provides a structured approach to candidate evaluation and comparison using ontology-based frameworks. It transforms subjective hiring decisions into evidence-based evaluations with traceable reasoning.

## Core Principles

### 1. Evidence-Based Evaluation

- All assessments must be backed by concrete evidence
- Evidence is classified by strength levels (1-3)
- Gaps are explicitly identified and documented

### 2. Structured Comparison

- Requirements are systematically mapped to candidate capabilities
- Comparisons are generated using standardized matrices
- Risk assessments are based on objective criteria

### 3. Traceable Decisions

- All recommendations include clear reasoning
- Decision provenance is tracked using W3C PROV standards
- Artifacts are linked to the procedures that generated them

## Methodology Steps

### Step 1: Job Description (JD) Extraction

**Objective**: Enumerate and structure job requirements

**Process**:

1. Extract requirements from job description
1. Classify requirements by domain (technical, soft skills, etc.)
1. Assign weights to requirements based on importance
1. Create structured requirement ontology

**Outputs**:

- Structured job requirements in RDF/Turtle format
- Requirement classification and weighting
- Success criteria definition

**Example**:

```turtle
jd:LLMTraining a ab:JDRequirement ;
    rdfs:label "LLM training at scale" ;
    rdfs:comment "Experience with large-scale language model training" .
```

### Step 2: Evidence Collection and Review

**Objective**: Gather and classify candidate evidence

**Process**:

1. Collect evidence from multiple sources:
   - Resumes and application materials
   - Portfolios and public repositories
   - Publications and presentations
   - References and recommendations
1. Classify evidence by strength level:
   - **Level 1**: Self-asserted resume evidence
   - **Level 2**: Partial demo / internal artifact
   - **Level 3**: Third-party/public validation
1. Map evidence to job requirements
1. Identify knowledge gaps

**Evidence Sources**:

- Resume/CV claims
- GitHub repositories
- Published papers
- Conference presentations
- Portfolio projects
- Reference letters
- Technical interviews

**Example**:

```turtle
cand:Lou a ab:Candidate ;
    ab:hasEvidenceStrength ab:Level1 ;
    ab:showsStrength jd:LLMTraining, jd:Governance ;
    ab:lacksArtifact jd:PostTraining, jd:Multimodal .
```

### Step 3: Comparison Matrix Generation

**Objective**: Create systematic head-to-head comparison

**Process**:

1. Map each candidate to each requirement
1. Classify mapping as:
   - ✓ Strength (evidence of capability)
   - ✗ Gap (lack of evidence)
   - ? Unknown (insufficient information)
1. Generate summary statistics
1. Create visual comparison matrix

**Matrix Structure**:

```
                | Req 1 | Req 2 | Req 3 |
Candidate A     |   ✓   |   ✗   |   ?   |
Candidate B     |   ✗   |   ✓   |   ✓   |
```

### Step 4: Risk Assessment

**Objective**: Evaluate hiring risks for each candidate

**Risk Factors**:

- Number of knowledge gaps
- Evidence strength level
- Number of demonstrated strengths
- Domain expertise alignment

**Risk Levels**:

- **Low Risk**: High evidence strength, many strengths, few gaps
- **Medium Risk**: Moderate evidence, some gaps, adequate strengths
- **High Risk**: Low evidence, many gaps, few strengths

**Mitigation Strategies**:

- Address knowledge gaps through training
- Request additional evidence or demonstrations
- Conduct technical screening
- Propose trial projects

### Step 5: Recommendation Synthesis

**Objective**: Generate actionable hiring recommendations

**Recommendation Types**:

- **Advance**: Proceed to next stage (technical screen, interview)
- **Keep Warm**: Maintain in talent pipeline for future opportunities
- **Request More Info**: Gather additional evidence before decision
- **Reject**: Decline at current time

**Decision Criteria**:

- Risk level assessment
- Strength-to-gap ratio
- Evidence quality
- Role requirements alignment

### Step 6: Report Generation

**Objective**: Create comprehensive evaluation report

**Report Components**:

- Executive summary
- Comparison matrix
- Risk assessments
- Recommendations with reasoning
- Next steps and action items
- Supporting evidence references

## Evidence Strength Levels

### Level 1: Self-Asserted Evidence

- Claims made in resume or application
- Self-reported experience and skills
- **Validation**: Requires verification through other sources

### Level 2: Partial Demonstration

- Internal artifacts or demos
- Non-public code repositories
- Internal presentations or documents
- **Validation**: Shows partial capability, needs public validation

### Level 3: Public Validation

- Publicly available repositories
- Published papers or articles
- Conference presentations
- Open source contributions
- **Validation**: Third-party verification and peer review

## Quality Assurance

### Validation Checks

- Ontology structural validation
- Evidence completeness verification
- Requirement coverage analysis
- Risk assessment consistency
- Recommendation traceability

### Review Process

- Independent evidence review
- Cross-validation of assessments
- Stakeholder feedback integration
- Continuous improvement based on outcomes

## Tools and Artifacts

### Core Tools

- **Ontology Manager**: RDF/Turtle ontology handling
- **Comparison Engine**: Matrix generation and analysis
- **Evidence Collector**: Evidence gathering and classification
- **Visualization Generator**: Diagram and report creation

### Generated Artifacts

- Comparison matrices
- Risk assessment reports
- Recommendation summaries
- Process flow diagrams
- Decision trees
- Evidence catalogs

## Best Practices

### Evidence Collection

- Gather evidence from multiple sources
- Prioritize Level 3 (public) evidence
- Document evidence collection process
- Maintain evidence provenance

### Comparison Process

- Use consistent evaluation criteria
- Document reasoning for all assessments
- Include uncertainty where appropriate
- Validate assessments with stakeholders

### Risk Management

- Be explicit about risk factors
- Provide mitigation strategies
- Consider role-specific requirements
- Balance risk with potential

### Decision Making

- Base recommendations on evidence
- Provide clear reasoning
- Include actionable next steps
- Document decision rationale

## Extensions and Customization

### Domain-Specific Adaptations

- Technical roles: Focus on code repositories and technical artifacts
- Research roles: Emphasize publications and research contributions
- Management roles: Include leadership and organizational evidence
- Creative roles: Consider portfolio and creative artifacts

### Process Variations

- Multi-stage evaluations
- Team-based assessments
- Peer review integration
- Continuous evaluation cycles

### Integration Points

- Applicant tracking systems
- HR information systems
- Performance management
- Learning and development

## Success Metrics

### Process Metrics

- Evidence collection completeness
- Comparison matrix accuracy
- Risk assessment validation
- Recommendation acceptance rate

### Outcome Metrics

- Hiring success rate
- Candidate performance correlation
- Time-to-hire reduction
- Stakeholder satisfaction

### Quality Metrics

- Evidence strength distribution
- Gap identification accuracy
- Risk prediction validity
- Decision traceability completeness
