import { useState } from 'react';
import {
  ArrowDown,
  ArrowUpRight,
  Building2,
  Check,
  HeartHandshake,
  Lightbulb,
  Mail,
  MapPin,
  Phone,
  Search,
  ShieldCheck,
  Users,
} from 'lucide-react';
import { articles, contact, data, properties, services } from '../../data.js';
import {
  BlogCard,
  Button,
  ContactForm,
  CTA,
  FAQ,
  Gallery,
  Heading,
  Office,
  Pagination,
  Picture,
  PropertyCard,
  ServiceGrid,
  TeamGrid,
} from '../../components/index.js';
import { AboutHeroSection } from './sections/AboutHeroSection.js';
import { StorySection } from './sections/StorySection.js';
import { ValuesSection } from './sections/ValuesSection.js';
import { OfficeSection } from './sections/OfficeSection.js';
import { TeamSection } from './sections/TeamSection.js';
import { FaqSection } from './sections/FaqSection.js';
export function AboutPage() {
  return (
    <>
      <AboutHeroSection />
      <StorySection />
      <ValuesSection />
      <OfficeSection />
      <TeamSection />
      <FaqSection />
    </>
  );
}
