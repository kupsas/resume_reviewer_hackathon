import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import EducationCard from '@/components/EducationCard';
import { EducationPoint } from '@/types/resume';

describe('EducationCard', () => {
  const mockEducation: EducationPoint = {
    text: "Bachelor of Science in Computer Science University of California, Berkeley | 2015-2019 - GPA: 3.8/4.0",
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

  const mockEducationWithLowScores: EducationPoint = {
    ...mockEducation,
    subject_course_school_reputation: {
      domestic_score: 3,
      domestic_score_rationale: "Program is relatively new and building reputation.",
      international_score: 2,
      international_score_rationale: "Limited international recognition."
    }
  };

  const mockEducationWithPerfectScores: EducationPoint = {
    ...mockEducation,
    subject_course_school_reputation: {
      domestic_score: 10,
      domestic_score_rationale: "Top-ranked program in the country.",
      international_score: 10,
      international_score_rationale: "Globally recognized as the best program."
    }
  };

  it('renders education information correctly', () => {
    render(<EducationCard education={mockEducation} />);
    
    // Check if all education details are displayed
    expect(screen.getByText(mockEducation.school || '')).toBeInTheDocument();
    expect(screen.getByText(`${mockEducation.course} in ${mockEducation.subject}`)).toBeInTheDocument();
    expect(screen.getByText(mockEducation.text || '')).toBeInTheDocument();
    expect(screen.getByText(mockEducation.improvement || '')).toBeInTheDocument();
  });

  it('displays reputation scores with progress bars', () => {
    render(<EducationCard education={mockEducation} />);
    
    // Check if progress bars are present
    const progressBars = screen.getAllByRole('progressbar');
    expect(progressBars).toHaveLength(2); // One for domestic, one for international
    
    // Check if scores are displayed
    const scoreElements = screen.getAllByText(/\d+\/10/);
    expect(scoreElements).toHaveLength(2);
    expect(scoreElements[0]).toHaveTextContent('9/10');
    expect(scoreElements[1]).toHaveTextContent('8/10');
  });

  it('displays tooltips with rationales', async () => {
    const user = userEvent.setup();
    render(<EducationCard education={mockEducation} />);
    
    // Find and hover over info buttons to show tooltips
    const infoButtons = screen.getAllByRole('button');
    expect(infoButtons).toHaveLength(2);
    
    // Hover over domestic info button
    await user.hover(infoButtons[0]);
    const domesticTooltips = await screen.findAllByText(mockEducation.subject_course_school_reputation.domestic_score_rationale);
    expect(domesticTooltips.length).toBeGreaterThan(0);
    
    // Hover over international info button
    await user.hover(infoButtons[1]);
    const internationalTooltips = await screen.findAllByText(mockEducation.subject_course_school_reputation.international_score_rationale);
    expect(internationalTooltips.length).toBeGreaterThan(0);
  });

  it('handles low reputation scores correctly', async () => {
    const user = userEvent.setup();
    render(<EducationCard education={mockEducationWithLowScores} />);
    
    // Check if low scores are displayed
    const scoreElements = screen.getAllByText(/\d+\/10/);
    expect(scoreElements).toHaveLength(2);
    expect(scoreElements[0]).toHaveTextContent('3/10');
    expect(scoreElements[1]).toHaveTextContent('2/10');
    
    // Find and hover over info buttons to show tooltips
    const infoButtons = screen.getAllByRole('button');
    
    // Hover over domestic info button
    await user.hover(infoButtons[0]);
    const domesticTooltips = await screen.findAllByText(mockEducationWithLowScores.subject_course_school_reputation.domestic_score_rationale);
    expect(domesticTooltips.length).toBeGreaterThan(0);
    
    // Hover over international info button
    await user.hover(infoButtons[1]);
    const internationalTooltips = await screen.findAllByText(mockEducationWithLowScores.subject_course_school_reputation.international_score_rationale);
    expect(internationalTooltips.length).toBeGreaterThan(0);
  });

  it('handles perfect reputation scores correctly', async () => {
    const user = userEvent.setup();
    render(<EducationCard education={mockEducationWithPerfectScores} />);
    
    // Check if perfect scores are displayed
    const scoreElements = screen.getAllByText(/\d+\/10/);
    expect(scoreElements).toHaveLength(2);
    expect(scoreElements[0]).toHaveTextContent('10/10');
    expect(scoreElements[1]).toHaveTextContent('10/10');
    
    // Find and hover over info buttons to show tooltips
    const infoButtons = screen.getAllByRole('button');
    
    // Hover over domestic info button
    await user.hover(infoButtons[0]);
    const domesticTooltips = await screen.findAllByText(mockEducationWithPerfectScores.subject_course_school_reputation.domestic_score_rationale);
    expect(domesticTooltips.length).toBeGreaterThan(0);
    
    // Hover over international info button
    await user.hover(infoButtons[1]);
    const internationalTooltips = await screen.findAllByText(mockEducationWithPerfectScores.subject_course_school_reputation.international_score_rationale);
    expect(internationalTooltips.length).toBeGreaterThan(0);
  });

  it('handles missing improvement text', () => {
    const educationWithoutImprovement: EducationPoint = {
      ...mockEducation,
      improvement: ''
    };
    
    render(<EducationCard education={educationWithoutImprovement} />);
    
    // Check that improvement section is not displayed
    expect(screen.queryByText('Suggested Improvement')).not.toBeInTheDocument();
  });
}); 