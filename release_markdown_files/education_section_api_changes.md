# Education Section API Changes 🎓

## Overview
This document outlines the changes made to the education section of our resume analysis API. The new format provides more structured and detailed information about educational background, including reputation scores.

## Changes Summary
- New education section format with structured fields
- Added reputation scoring system
- Removed STAR format and technical scores for education sections
- Enhanced validation and error handling

## New Response Format

### Education Section
```json
{
  "type": "Education",
  "text": "{{all the text in the education section}}",
  "subject": "Electrical and Electronics Engineering",
  "course": "Bachelor of Engineering",
  "school": "BITS Pilani",
  "subject_course_school_reputation": {
    "domestic_score": 9,
    "domestic_score_rationale": "BITS Pilani is one of the most prestigious engineering institutions in India...",
    "international_score": 6,
    "international_score_rationale": "BITS Pilani has a growing international presence..."
  }
}
```

## Field Descriptions

### Required Fields
- `type`: Always "Education"
- `text`: Raw text from the education section
- `subject`: Main field of study
- `course`: Degree or certification type
- `school`: Institution name

### Reputation Scores
- `domestic_score`: Score from 0-10 for domestic reputation
- `domestic_score_rationale`: Explanation for domestic score
- `international_score`: Score from 0-10 for international reputation
- `international_score_rationale`: Explanation for international score

## Frontend Implementation Guidelines

### 1. Display Updates
- Update education section display to show new structured fields
- Add reputation scores with visual indicators (e.g., star ratings)
- Display rationales in tooltips or expandable sections

### 2. Data Handling
- Update type definitions to match new schema
- Implement proper null checks for optional fields
- Handle both old and new format responses during transition

### 3. UI Components
- Create new components for reputation score display
- Update existing education section components
- Add tooltips for score rationales

## Example Implementation

```typescript
interface EducationReputation {
  domestic_score: number;
  domestic_score_rationale: string;
  international_score: number;
  international_score_rationale: string;
}

interface EducationSection {
  type: "Education";
  text: string;
  subject: string;
  course: string;
  school: string;
  subject_course_school_reputation: EducationReputation;
}

// Example React component
const EducationSection: React.FC<{ education: EducationSection }> = ({ education }) => {
  return (
    <div className="education-section">
      <h3>{education.course} in {education.subject}</h3>
      <p>{education.school}</p>
      <div className="reputation-scores">
        <div className="score">
          <span>Domestic Reputation: {education.subject_course_school_reputation.domestic_score}/10</span>
          <Tooltip content={education.subject_course_school_reputation.domestic_score_rationale}>
            <InfoIcon />
          </Tooltip>
        </div>
        <div className="score">
          <span>International Reputation: {education.subject_course_school_reputation.international_score}/10</span>
          <Tooltip content={education.subject_course_school_reputation.international_score_rationale}>
            <InfoIcon />
          </Tooltip>
        </div>
      </div>
    </div>
  );
};
```

## Migration Notes
1. The API will support both old and new formats during the transition period
2. Frontend should handle both formats gracefully
3. Plan to remove old format support in future releases

## Questions?
For any questions or clarifications, please contact:
- Backend Team Lead: [Contact Info]
- API Documentation: [Link to API Docs]

## Additional Resources
- [Design System Documentation](link-to-design-system)
- [Component Library](link-to-component-library)
- [API Testing Guide](link-to-api-testing)
- [Migration Checklist](link-to-migration-checklist) 