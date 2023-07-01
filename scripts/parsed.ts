interface ValidationResult {
  issues: string[];
  isValid: boolean;
}

export interface Parsed<T> {
  value: T | null;
  validationResult: ValidationResult;
}

export const Parsed = {
  issues: <T>(issues: string[]): Parsed<T> => ({
    value: null,
    validationResult: {
      issues,
      isValid: false,
    },
  }),
  of: <T>(value: T): Parsed<T> => ({
    value,
    validationResult: {
      issues: [],
      isValid: true,
    },
  }),
};
