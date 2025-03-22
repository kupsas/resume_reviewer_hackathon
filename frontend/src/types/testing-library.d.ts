import '@testing-library/jest-dom';

declare global {
  namespace Vi {
    interface Assertion {
      toBeInTheDocument(): void;
      toBeVisible(): void;
      toHaveAttribute(name: string, value?: string): void;
      toHaveTextContent(text: string | RegExp): void;
      toHaveValue(value: string | string[] | number): void;
      toBeDisabled(): void;
      toBeEnabled(): void;
      toBeRequired(): void;
      toBeValid(): void;
      toBeInvalid(): void;
      toBeChecked(): void;
      toBeFocused(): void;
      toBeEmptyDOMElement(): void;
      toHaveClass(className: string): void;
      toHaveStyle(css: Record<string, any>): void;
      toContainElement(element: HTMLElement | null): void;
      toContainHTML(htmlText: string): void;
    }
  }
} 