import { describe, it, expect } from 'vitest';
import { contentFormSchema, emailSchema, passwordSchema } from '@/lib/validations';

describe('emailSchema', () => {
  it('accepts valid emails', () => {
    const result = emailSchema.safeParse('user@example.com');
    expect(result.success).toBe(true);
  });

  it('rejects invalid emails', () => {
    const result = emailSchema.safeParse('not-an-email');
    expect(result.success).toBe(false);
  });

  it('rejects empty string', () => {
    const result = emailSchema.safeParse('');
    expect(result.success).toBe(false);
  });
});

describe('passwordSchema', () => {
  it('accepts passwords with 8+ characters', () => {
    const result = passwordSchema.safeParse('12345678');
    expect(result.success).toBe(true);
  });

  it('rejects short passwords', () => {
    const result = passwordSchema.safeParse('short');
    expect(result.success).toBe(false);
  });
});

describe('contentFormSchema', () => {
  it('accepts valid content form data', () => {
    const result = contentFormSchema.safeParse({
      section: 'aboutme',
      title: 'Test Content',
      slug: 'test-content',
      body: 'This is test content.',
      isPublished: true,
      sortOrder: 1,
    });
    expect(result.success).toBe(true);
  });

  it('rejects empty title', () => {
    const result = contentFormSchema.safeParse({
      section: 'aboutme',
      title: '',
      slug: 'test-content',
      body: 'Body',
      isPublished: true,
      sortOrder: 1,
    });
    expect(result.success).toBe(false);
  });

  it('rejects invalid slug format', () => {
    const result = contentFormSchema.safeParse({
      section: 'aboutme',
      title: 'Test',
      slug: 'Invalid Slug With Spaces',
      body: 'Body',
      isPublished: true,
      sortOrder: 1,
    });
    expect(result.success).toBe(false);
  });

  it('accepts valid slug with hyphens', () => {
    const result = contentFormSchema.safeParse({
      section: 'aboutme',
      title: 'Test',
      slug: 'valid-slug-format',
      body: 'Body',
      isPublished: true,
      sortOrder: 1,
    });
    expect(result.success).toBe(true);
  });

  it('rejects negative sort order', () => {
    const result = contentFormSchema.safeParse({
      section: 'aboutme',
      title: 'Test',
      slug: 'test',
      body: 'Body',
      isPublished: true,
      sortOrder: -1,
    });
    expect(result.success).toBe(false);
  });

  it('rejects too long body', () => {
    const result = contentFormSchema.safeParse({
      section: 'aboutme',
      title: 'Test',
      slug: 'test',
      body: 'a'.repeat(50001),
      isPublished: true,
      sortOrder: 1,
    });
    expect(result.success).toBe(false);
  });

  it('rejects invalid section', () => {
    const result = contentFormSchema.safeParse({
      section: 'invalid-section' as any,
      title: 'Test',
      slug: 'test',
      body: 'Body',
      isPublished: true,
      sortOrder: 1,
    });
    expect(result.success).toBe(false);
  });

  it('accepts draft content (isPublished: false)', () => {
    const result = contentFormSchema.safeParse({
      section: 'trade4me',
      title: 'Draft Project',
      slug: 'draft-project',
      body: '',
      isPublished: false,
      sortOrder: 0,
    });
    expect(result.success).toBe(true);
  });
});
