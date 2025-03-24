import { describe, expect, test } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import SectionAnalysis from '@/components/SectionAnalysis';
import { EducationPoint, ResumePoint, ResumeSection } from '@/types/resume';

describe('SectionAnalysis', () => {
    const mockEducationPoint: EducationPoint = {
        text: "Bachelor of Science in Computer Science University of California, Berkeley | 2015-2019",
        subject: "Computer Science",
        course: "Bachelor of Science",
        school: "University of California, Berkeley",
        subject_course_school_reputation: {
            domestic_score: 9,
            domestic_score_rationale: "UC Berkeley is renowned for its strong computer science program in the U.S.",
            international_score: 8,
            international_score_rationale: "UC Berkeley is globally recognized for its excellence in computer science education."
        },
        improvement: "Consider highlighting specific projects completed during your coursework."
    };

    const mockExperiencePoint: ResumePoint = {
        text: "Led development of cloud-based microservices architecture",
        star: {
            situation: true,
            task: true,
            action: true,
            result: true,
            complete: true
        },
        metrics: ["99.9%"],
        technical_score: 5,
        improvement: "Add more specific details about the impact."
    };

    test('renders education section with EducationCard', () => {
        const section: ResumeSection = {
            type: 'Education',
            points: [mockEducationPoint]
        };

        render(
            <SectionAnalysis
                title="Education"
                section={section}
            />
        );

        // Check for section title
        expect(screen.getByText('Education')).toBeInTheDocument();

        // Check for course and subject in the heading
        const headings = screen.getAllByRole('heading', { level: 3 });
        const courseHeading = headings.find(h => h.textContent?.includes(mockEducationPoint.course));
        expect(courseHeading).toBeTruthy();
        expect(courseHeading).toHaveTextContent(mockEducationPoint.subject);
    });

    test('renders experience section with StarAnalysisCard', () => {
        const section: ResumeSection = {
            type: 'Experience',
            points: [mockExperiencePoint]
        };

        render(
            <SectionAnalysis
                title="Experience"
                section={section}
            />
        );

        expect(screen.getByText('Experience')).toBeInTheDocument();
        expect(screen.getByText(mockExperiencePoint.text)).toBeInTheDocument();
    });

    test('displays section title correctly', () => {
        const section: ResumeSection = {
            type: 'Education',
            points: [mockEducationPoint]
        };

        render(
            <SectionAnalysis
                title="Education"
                section={section}
            />
        );

        expect(screen.getByText('Education')).toBeInTheDocument();
    });

    test('handles empty points array', () => {
        const section: ResumeSection = {
            type: 'Education',
            points: []
        };

        render(
            <SectionAnalysis
                title="Education"
                section={section}
            />
        );

        // Section title should still be visible
        expect(screen.getByText('Education')).toBeInTheDocument();
        
        // No education cards should be rendered
        expect(screen.queryByText(mockEducationPoint.text)).not.toBeInTheDocument();
    });

    test('renders multiple education points correctly', () => {
        const secondEducationPoint: EducationPoint = {
            ...mockEducationPoint,
            course: "Master of Science",
            subject: "Artificial Intelligence",
            school: "Stanford University"
        };

        const section: ResumeSection = {
            type: 'Education',
            points: [mockEducationPoint, secondEducationPoint]
        };

        render(
            <SectionAnalysis
                title="Education"
                section={section}
            />
        );

        // Check for section title
        expect(screen.getByText('Education')).toBeInTheDocument();

        // Check for course and subject in both headings
        const headings = screen.getAllByRole('heading', { level: 3 }).filter(h => h.textContent !== 'Education');
        expect(headings).toHaveLength(2);

        expect(headings[0]).toHaveTextContent(`${mockEducationPoint.course} in ${mockEducationPoint.subject}`);
        expect(headings[1]).toHaveTextContent(`${secondEducationPoint.course} in ${secondEducationPoint.subject}`);
    });

    test('handles section expansion/collapse', () => {
        const section: ResumeSection = {
            type: 'Education',
            points: [mockEducationPoint]
        };

        render(
            <SectionAnalysis
                title="Education"
                section={section}
            />
        );

        // Section should be expanded by default
        expect(screen.getByText(mockEducationPoint.text)).toBeInTheDocument();

        // Click to collapse
        fireEvent.click(screen.getByText('Education'));
        expect(screen.queryByText(mockEducationPoint.text)).not.toBeInTheDocument();

        // Click to expand
        fireEvent.click(screen.getByText('Education'));
        expect(screen.getByText(mockEducationPoint.text)).toBeInTheDocument();
    });

    test('handles section with mixed point types', () => {
        const section: ResumeSection = {
            type: 'Mixed',
            points: [mockEducationPoint, mockExperiencePoint]
        };

        render(
            <SectionAnalysis
                title="Mixed Section"
                section={section}
            />
        );

        // Check section title
        expect(screen.getByText('Mixed Section')).toBeInTheDocument();
        
        // Check education point
        expect(screen.getByText(mockEducationPoint.text)).toBeInTheDocument();
        
        // Check experience point
        expect(screen.getByText(mockExperiencePoint.text)).toBeInTheDocument();
        
        // Check metrics are displayed
        expect(screen.getByText('99.9%')).toBeInTheDocument();
    });
}); 