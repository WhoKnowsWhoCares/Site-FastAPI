import '@testing-library/jest-dom/vitest';
import { vi } from 'vitest';

// Mock next/navigation
vi.mock('next/navigation', () => ({
  useRouter() {
    return {
      push: vi.fn(),
      replace: vi.fn(),
      prefetch: vi.fn(),
      back: vi.fn(),
      forward: vi.fn(),
      pathname: '/',
      query: {},
      isReady: true,
    };
  },
  usePathname() {
    return '/';
  },
}));

// Mock next/link
vi.mock('next/link', () => ({
  default: ({ children, href, ...props }: any) =>
    React.createElement('a', { href, ...props }, children),
}));

// Mock next/image
vi.mock('next/image', () => ({
  default: (props: any) => React.createElement('img', props),
}));

import React from 'react';
