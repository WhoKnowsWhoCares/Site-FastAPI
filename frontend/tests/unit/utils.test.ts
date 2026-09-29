import { describe, it, expect } from 'vitest';
import { cn } from '@/lib/utils';

describe('cn', () => {
  it('merges class names correctly', () => {
    expect(cn('flex', 'bg-red-500')).toBe('flex bg-red-500');
  });

  it('handles duplicate classes', () => {
    expect(cn('flex', 'flex', 'p-2')).toBe('flex p-2');
  });

  it('handles conditional classes', () => {
    const isActive = true;
    expect(cn('base', isActive && 'active')).toBe('base active');
  });

  it('ignores falsy values', () => {
    const isHidden = false;
    expect(cn('visible', isHidden && 'hidden')).toBe('visible');
  });

  it('handles object syntax', () => {
    expect(cn('base', { 'active': true, 'disabled': false })).toBe('base active');
  });

  it('returns empty string for no args', () => {
    expect(cn()).toBe('');
  });
});
