import { describe, it, expect } from 'vitest';
import { isEducationPoint } from '@/lib/utils';
import { ResumePoint, EducationPoint } from '@/types/resume';

describe('isEducationPoint', () => {
  it('identifies valid education points', () => {
    const validEducationPoint: EducationPoint = {
      text: "Bachelor of Science in Computer Science",
      subject: "Computer Science",
      course: "Bachelor of Science",
      school: "University of California, Berkeley",
      subject_course_school_reputation: {
        domestic_score: 9,
        domestic_score_rationale: "Strong program",
        international_score: 8,
        international_score_rationale: "Well recognized"
      },
      improvement: "Add more details"
    };

    expect(isEducationPoint(validEducationPoint)).toBe(true);
  });

  it('rejects non-education points', () => {
    const nonEducationPoint: ResumePoint = {
      text: "Led development team",
      star: {
        situation: true,
        task: true,
        action: true,
        result: true,
        complete: true
      },
      metrics: ["10%"],
      technical_score: 5,
      improvement: "Add metrics"
    };

    expect(isEducationPoint(nonEducationPoint)).toBe(false);
  });

  it('handles null and undefined', () => {
    // Type assertion to handle null/undefined in tests
    expect(isEducationPoint(null as unknown as ResumePoint)).toBe(false);
    expect(isEducationPoint(undefined as unknown as ResumePoint)).toBe(false);
  });

  it('handles partial education points', () => {
    const partialPoint = {
      text: "Some text",
      subject: "Computer Science"
    };

    expect(isEducationPoint(partialPoint as unknown as ResumePoint)).toBe(false);
  });
}); 