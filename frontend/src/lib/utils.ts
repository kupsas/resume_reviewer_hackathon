import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
import { EducationPoint, ResumePoint } from '@/types/resume'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Type guard function to check if a ResumePoint is an EducationPoint
 * @param point The point to check
 * @returns True if the point is an EducationPoint, false otherwise
 */
export function isEducationPoint(point: ResumePoint): point is EducationPoint {
  if (!point) return false;
  
  return (
    'subject' in point && 
    'course' in point && 
    'school' in point && 
    'subject_course_school_reputation' in point
  );
}
